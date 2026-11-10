#!/usr/bin/env bash
source "$(dirname -- "$0")/common.sh"
exec python3 "$LIB/report-files.py" delete "$ROOT" "$@"
