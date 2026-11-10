#!/usr/bin/env bash
source "$(dirname -- "$0")/common.sh"
result=$(python3 "$LIB/report-files.py" publish "$ROOT" "$@")
id=$(jq -r .id <<<"$result"); revision=$(jq -r .revision <<<"$result")
host=$(tailscale status --json | jq -er '.Self.DNSName | rtrimstr(".")') || { echo "$result"; fail 'Content saved; publication pending. Cannot discover the Tailscale hostname.'; }
[[ $host =~ ^[a-zA-Z0-9.-]+$ ]] || fail 'Invalid hostname; publication pending.'
url=https://$host$(jq -r .path <<<"$result")
response=$(mktemp "$ROOT/staging/verify.XXXXXX")
trap 'rm -f "$response"' EXIT
if curl --fail --silent --show-error --location --max-redirs 3 --connect-timeout 5 --max-time 15 "$url" -o "$response" &&
   cmp -s "$response" "$ROOT/public/_releases/$id/$revision/index.html"; then
  jq --arg id "$id" '.[$id].delivery="transport-verified"' "$ROOT/state/reports.json" >"$ROOT/state/reports.tmp"
  mv "$ROOT/state/reports.tmp" "$ROOT/state/reports.json"
  jq --arg url "$url" '. + {url:$url,delivery:"transport-verified"}' <<<"$result"
  echo 'Verify companion files and browser behavior before sharing.' >&2
else
  echo "$result"
  fail 'Content saved; publication pending. Run preview-status.sh for preview diagnostics or inspect lab-reports.service and the /reports route.'
fi
