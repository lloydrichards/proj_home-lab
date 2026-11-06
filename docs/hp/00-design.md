# A private development host that stays available

The HP runs Omarchy on bare metal. Connect from the laptop through Tailscale and SSH. Keep the desktop for local setup and recovery; remote coding does not require remote desktop.

## First-install scope

- Ethernet and a Tailscale device name, `hp-lab`.
- Key-authenticated OpenSSH through Tailscale; Tailscale SSH remains disabled.
- `labadmin` for maintenance, with password-protected sudo.
- `coder` for repositories, Pi, OpenCode, builds, and tests, without sudo or Docker access.
- Persistent terminal sessions with tmux, plus optional localhost browser interfaces through SSH tunnels.
- Off-machine backups and tested recovery before the machine becomes essential.

These names are proposed conventions. Choose alternatives before installation and replace them consistently. Do not recreate `labadmin` if the installer already created it.

## Keep the existing Pi in service

Leave Coolify workloads on the Raspberry Pi during setup. Move a workload only after its backup, restore, and network tests pass. Public application hosting and remote agent administration have different exposure requirements.

## Security boundaries

Tailscale supplies the private network and access policy. OpenSSH authenticates the laptop key and selects the Linux account. This design leaves Tailscale SSH off so OpenSSH settings govern these connections. See [access research](../research/private-access.md).

`coder` must not belong to `wheel` or `docker`, read the administration account's private files, or have a passwordless sudo rule. Every agent running as `coder` can read that account's accessible files, credentials, and other sessions. A worktree prevents editing collisions; it is not a security boundary.

For an untrusted repository or stronger separation, use a disposable VM with scoped credentials. Do not give an agent the host Docker socket, production keys, or the laptop's forwarded SSH agent. [Docker documents the privilege of its group](https://docs.docker.com/engine/install/linux-postinstall/).

## Session and capacity limits

Tmux preserves a running shell after the laptop disconnects, not after the HP reboots. Saved agent sessions may resume a conversation; they do not restore a compiler or browser process.

Start with two simultaneous heavy builds or browser-test jobs. Three to five connected agents may spend much of their time waiting for cloud responses, but their tools still use CPU and RAM. Measure before increasing concurrency. Keep RAM and disk headroom for maintenance and backups.

## Unattended reboot is the chosen behavior

The user selected an **unencrypted installation** on 6 November 2026 so the HP can return after a reboot without a local disk unlock. Follow the documented installer opt-out. This exposes stored files and credentials to someone with physical access to the SSD. Keep the rack physically protected, credentials scoped, and backups encrypted.

A UPS reduces interruption risk. Firmware AC-loss recovery, no-sleep policy, network services, and any persistent agent service still need cold-boot tests; choosing no encryption does not establish those behaviors automatically. See [installation](01-install.md).
