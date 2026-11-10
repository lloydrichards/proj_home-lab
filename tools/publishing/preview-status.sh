#!/usr/bin/env bash
source "$(dirname -- "$0")/common.sh"
if [[ $# == 0 ]]; then
  for record in "$ROOT"/state/previews/*.json; do [[ -f $record ]] && cat "$record"; done
  exit 0
fi
slug "$1"; record=$ROOT/state/previews/$1.json
[[ -f $record ]] || fail 'Unknown preview id.'
if [[ -f ${record%.json}.runtime ]]; then
  jq -s '.[0] + {runtime:.[1]}' "$record" "${record%.json}.runtime"
else
  cat "$record"
fi
unit=$(jq -r .unit "$record")
flock -u 9
systemctl --user status "$unit" --no-pager || true
journalctl --user -u "$unit" -n 20 --no-pager || true
python3 "$LIB/preview-check.py" "$record" && echo 'Expected process owns an HTTP listener.' || echo 'HTTP readiness failed.'
curl --fail --silent --show-error --connect-timeout 5 --max-time 10 -o /dev/null "$(jq -r .url "$record")" && echo 'HTTPS transport passed.' || echo 'HTTPS transport failed.'
