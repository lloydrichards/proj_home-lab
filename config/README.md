# Reviewable configuration examples

These files are examples, not an installer. Nothing is applied automatically.

| File | Proposed destination | Required validation |
|---|---|---|
| `ssh/00-home-lab.conf.example` | `/etc/ssh/sshd_config.d/00-home-lab.conf` | Global include, effective settings, `sshd -t`, second login |
| `systemd/90-home-lab-sleep.conf.example` | `/etc/systemd/sleep.conf.d/90-home-lab.conf` | Other drop-ins, idle/reboot tests, rollback |

Back up existing files before editing. Keep console access during access-control changes. Do not overwrite unrelated configuration. Verify syntax with the installed tool version on the HP.

No provider secrets, SSH private keys, reusable enrollment keys, populated `.env` files, or credentials belong here. `.gitignore` helps avoid accidental additions but does not detect secrets or remove them from Git history.

A persistent OpenCode service is deliberately deferred until its interactive workflow, executable path, provider authentication, resource use, and protected secret storage are verified. Do not improvise a root service to work around a missing user PATH.
