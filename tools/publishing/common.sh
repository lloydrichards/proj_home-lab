#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $(hostname -s) == home-lab ]] || { echo 'Run this on home-lab as coder.' >&2; exit 1; }
[[ $(id -un) == coder ]] || { echo 'Run this as coder.' >&2; exit 1; }
LIB=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=${LAB_PUBLISH_ROOT:-$HOME/.local/share/lab-publish}
[[ $ROOT == /* ]] || { echo 'LAB_PUBLISH_ROOT must be absolute.' >&2; exit 1; }
mkdir -p "$ROOT"/{state/previews,staging,public,launches}
exec 9>"$ROOT/state/lock"
flock 9
fail() { echo "$*" >&2; exit 1; }
slug() { [[ $1 =~ ^[a-z0-9][a-z0-9_-]{0,119}$ ]] || fail "Invalid identifier: $1"; }
route() { sudo -n /usr/local/sbin/lab-publish-route "$@" >&2; }
