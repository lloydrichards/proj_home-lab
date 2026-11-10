#!/usr/bin/env bash
source "$(dirname -- "$0")/common.sh"
[[ $# == 1 ]] || fail 'Usage: stop-preview.sh ID'
slug "$1"; record=$ROOT/state/previews/$1.json
[[ -f $record ]] || fail 'Unknown preview id.'
[[ $(jq -r .status "$record") != retired ]] || { cat "$record"; exit 0; }
# Remove the route before releasing its upstream port.
external=$(jq -r .external_port "$record")
authority=$(jq -r '.host + ":" + (.external_port|tostring)' "$record")
config=$(tailscale serve status --json)
if jq -e --arg authority "$authority" --arg port "$external" '.Web[$authority] == null and .TCP[$port] == null' <<<"$config" >/dev/null; then
  echo 'No external route is installed for this allocation.' >&2
else
  route stop "$external" "$(jq -r .internal_port "$record")"
fi
systemctl --user disable --now "$(jq -r .unit "$record")"
jq '.status="retired"' "$record" >"$record.tmp"; mv "$record.tmp" "$record"
cat "$record"
