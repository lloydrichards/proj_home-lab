#!/usr/bin/env bash
set -euo pipefail
[[ $(hostname -s) == home-lab && $EUID == 0 ]] || { echo 'Run on home-lab with sudo from the lloyd maintenance account.' >&2; exit 1; }
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
# Install a reviewed snapshot. The privileged helper never sources this checkout at runtime.
install -o root -g root -m 755 "$source_dir/lab-publish-route" /usr/local/sbin/lab-publish-route
rule=$(mktemp)
trap 'rm -f "$rule"' EXIT
printf '%s\n' 'coder ALL=(root) NOPASSWD: /usr/local/sbin/lab-publish-route' >"$rule"
visudo -cf "$rule"
install -o root -g root -m 440 "$rule" /etc/sudoers.d/lab-publish
/usr/local/sbin/lab-publish-route reports
