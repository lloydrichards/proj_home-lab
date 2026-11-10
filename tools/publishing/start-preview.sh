#!/usr/bin/env bash
source "$(dirname -- "$0")/common.sh"
[[ $# -ge 4 ]] || fail 'Usage: start-preview.sh WORKTREE SERVICE -- COMMAND [ARG ...]; {port} is replaced with the allocated port.'
worktree=$(realpath -e -- "$1"); service=$2; shift 2
slug "$service"
environment=; health_path=/; update=false
while [[ $# -gt 0 && $1 != -- ]]; do
  case $1 in
    --update) update=true; shift ;;
    --env-file) [[ $# -ge 2 ]] || fail 'Missing environment file'; environment=$(realpath -e -- "$2"); shift 2 ;;
    --health-path) [[ $# -ge 2 ]] || fail 'Missing health path'; health_path=$2; shift 2 ;;
    *) fail "Unknown option: $1" ;;
  esac
done
[[ $health_path == /* && $health_path != *$'\n'* ]] || fail 'Health path must begin with /.'
if [[ -n $environment ]]; then
  jq -e 'type == "object" and all(to_entries[]; (.key | test("^[A-Za-z_][A-Za-z0-9_]*$")) and (.value | type == "string"))' "$environment" >/dev/null || fail 'Environment file must be a JSON object of strings.'
fi
[[ ${1:-} == -- ]] || fail 'Expected -- before the command.'
shift
[[ $# -gt 0 ]] || fail 'Missing command.'
git -C "$worktree" rev-parse --show-toplevel >/dev/null || fail 'Expected a Git worktree.'
[[ $(git -C "$worktree" rev-parse --show-toplevel) == "$worktree" ]] || fail 'Use the worktree root; use command arguments to select an app directory.'
host=$(tailscale status --json | jq -er '.Self.DNSName | rtrimstr(".")')
[[ $host =~ ^[a-zA-Z0-9.-]+$ ]] || fail 'Invalid Tailscale hostname.'
id=$(printf '%s\0%s' "$worktree" "$service" | sha256sum | cut -c1-20)
record=$ROOT/state/previews/$id.json
# A corrupt reservation must never make an old HTTPS URL appear available.
reservations=$(python3 - "$ROOT/state/previews" <<'PY'
import json
from pathlib import Path
import sys
records=[]
external=set()
active_internal=set()
allowed={'allocated','starting','ready','failed','publication-pending','retired'}
for path in sorted(Path(sys.argv[1]).glob('*.json')):
    try:
        record=json.loads(path.read_text())
        if not isinstance(record,dict) or record.get('status') not in allowed:
            raise ValueError('invalid record or lifecycle status')
        for key,low,high in [('external_port',8400,9999),('internal_port',20000,29999)]:
            value=record.get(key)
            if type(value) is not int or not low <= value <= high:
                raise ValueError('invalid '+key)
        if record['external_port'] in external:
            raise ValueError('duplicate HTTPS reservation')
        external.add(record['external_port'])
        if record['status']!='retired':
            if record['internal_port'] in active_internal:
                raise ValueError('duplicate active internal reservation')
            active_internal.add(record['internal_port'])
        records.append(record)
    except (OSError,ValueError) as error:
        print(f'{path.name}: {error}',file=sys.stderr)
        sys.exit(1)
print(json.dumps(records))
PY
) || fail 'Allocation registry is invalid; refusing to allocate or reuse URLs. Preserve the records for repair.'
record_state() {
  jq --arg status "$1" --arg error "${2:-}" '.status=$status | .last_error=$error' "$record" >"$record.tmp"
  mv "$record.tmp" "$record"
}
activate() {
  unit=$(jq -r .unit "$record")
  external=$(jq -r .external_port "$record")
  internal=$(jq -r .internal_port "$record")
  health_path=$(jq -r '.health_path // "/"' "$record")
  record_state starting
  systemctl --user reset-failed "$unit" || true
  if ! systemctl --user start "$unit"; then
    record_state failed 'User service failed to start'
    fail 'Preview service failed to start; allocation retained.'
  fi
  flock -u 9
  for ((i=0;i<60;i++)); do
    if python3 "$LIB/preview-check.py" "$record"; then
      flock 9
      [[ $(jq -r .status "$record") != retired ]] || fail 'Preview was stopped while starting.'
      if ! route preview "$external" "$internal"; then
        record_state publication-pending 'Private route setup failed'
        fail 'Local service is ready, but private route setup failed; allocation retained.'
      fi
      url=$(jq -r .url "$record")
      if ! curl --fail --silent --show-error --connect-timeout 5 --max-time 10 -o /dev/null "${url%/}$health_path"; then
        record_state publication-pending 'Private HTTPS verification failed'
        fail 'Local service is ready, but private HTTPS verification failed; allocation retained.'
      fi
      record_state ready
      echo "$(jq -r .url "$record")"
      echo 'Transport ready. Verify assets, APIs, and live updates in a browser before sharing.' >&2
      exit 0
    fi
    systemctl --user is-active --quiet "$unit" || break
    sleep 1
  done
  flock 9
  [[ $(jq -r .status "$record") != retired ]] || fail 'Preview was stopped while starting.'
  record_state failed 'Local readiness check failed'
  fail "Preview is not ready. Allocation retained: $id. Run preview-status.sh $id."
}
if [[ -f $record ]]; then
  [[ $(jq -r .status "$record") != retired ]] || fail 'This allocation is retired. Use a new service name for a new preview.'
  if $update; then
    exe=$(command -v -- "$1") || fail "Executable not found: $1"
    shift
    argv=$(jq -cn --args '$ARGS.positional' -- "$exe" "$@")
    if [[ -n $environment ]]; then
      install -m 600 "$environment" "$ROOT/launches/$id/environment.json"
      environment=$ROOT/launches/$id/environment.json
    fi
    jq --argjson argv "$argv" --arg environment "$environment" --arg health_path "$health_path" --arg launch_path "$PATH" '. + {argv:$argv, environment:$environment, health_path:$health_path, launch_path:$launch_path}' "$record" >"$record.tmp"
    mv "$record.tmp" "$record"
    record_state starting
    if ! systemctl --user restart "$(jq -r .unit "$record")"; then
      record_state failed 'Updated user service failed to restart'
      fail 'Updated preview service failed to restart; allocation retained.'
    fi
  fi
  echo 'Reusing the recorded allocation.' >&2
  activate
fi
listeners=$(ss -H -lnt | awk '{print $4}' | sed 's/.*://')
serve=$(tailscale serve status --json)
external=
for ((p=8400;p<=9999;p++)); do
  if ! jq -e --argjson p "$p" 'any(.[]; .external_port == $p)' <<<"$reservations" >/dev/null &&
     ! jq -e --arg p "$p" '.TCP[$p] != null' <<<"$serve" >/dev/null &&
     ! grep -qx "$p" <<<"$listeners"; then external=$p; break; fi
done
[[ -n $external ]] || fail 'HTTPS allocation range exhausted; do not reuse retired URLs.'
internal=
for ((p=20000;p<=29999;p++)); do
  if ! jq -e --argjson p "$p" 'any(.[]; .status != "retired" and .internal_port == $p)' <<<"$reservations" >/dev/null &&
     ! grep -qx "$p" <<<"$listeners"; then internal=$p; break; fi
done
[[ -n $internal ]] || fail 'Internal port range exhausted.'
mkdir -p "$ROOT/launches/$id"
if [[ -n $environment ]]; then
  install -m 600 "$environment" "$ROOT/launches/$id/environment.json"
  environment=$ROOT/launches/$id/environment.json
fi
exe=$(command -v -- "$1") || fail "Executable not found: $1"
shift
argv=$(jq -cn --args '$ARGS.positional' -- "$exe" "$@")
unit=lab-preview-$id.service
jq -n --arg id "$id" --arg worktree "$worktree" --arg service "$service" --arg unit "$unit" --arg host "$host" --argjson external "$external" --argjson internal "$internal" --argjson argv "$argv" --arg launch_path "$PATH" --arg health_path "$health_path" --arg environment "$environment" '{id:$id,worktree:$worktree,service:$service,unit:$unit,host:$host,external_port:$external,internal_port:$internal,argv:$argv,launch_path:$launch_path,health_path:$health_path,environment:$environment,status:"allocated",url:("https://"+$host+":"+($external|tostring)+"/")}' >"$record.tmp"
mv "$record.tmp" "$record"
# A route is not installed until the expected process owns the listener.
python3 "$LIB/service-files.py" "$ROOT" "$record" "$LIB"
systemctl --user daemon-reload
systemctl --user enable --now "$unit"
activate
