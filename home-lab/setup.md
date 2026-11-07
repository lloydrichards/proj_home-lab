# Set up the HP after installing Omarchy

Use this guide at the HP console after Omarchy is installed. It takes the machine from its first desktop login to private remote coding from the MacBook. Keep a monitor, keyboard, and bootable USB available until the reboot and recovery checks pass.

Prepared on 7 November 2026 from upstream documentation and [setup research](research/setup-sources.md). These are proposed instructions, not steps already run on the HP. Recheck the installed release before making changes. Track progress only in the [HP preparation checklist](preparation.md).

The starting arrangement is Ethernet, an unencrypted boot disk as already chosen, Tailscale for private connectivity, ordinary OpenSSH for login, and a separate unprivileged `coder` account. Existing Pi hosting stays where it is. The daily Mac client remains open; begin with SSH and tmux.

Complete sections 1 through 8, 10, and 11 for the first setup. Section 9 applies only when a project needs containers. For later reference, jump to [updates and packages](#2-update-omarchy-and-install-missing-tools), [accounts](#3-separate-maintenance-from-coding), [private access](#5-establish-private-connectivity), [SSH hardening](#6-harden-ssh-without-losing-access), [power and services](#7-remove-unused-listeners-and-prevent-sleep), [coding](#8-start-one-trusted-coding-project), [backups](#10-make-and-restore-the-first-off-machine-backup), or [acceptance checks](#11-prove-access-and-recovery-before-putting-it-in-the-rack).

## 1. Record the machine and check basic operation

Run these on the HP as the account created by the installer. This is the maintenance account. Keep its password outside the HP in your password manager.

```sh
hostnamectl
cat /etc/os-release
uname -r
lscpu
free -h
lsblk -o NAME,SIZE,MODEL,FSTYPE,MOUNTPOINTS
findmnt --target /
findmnt --target /home
timedatectl
ip -br address
ip route
systemctl --failed
```

Confirm the delivered hardware against the [inventory](../reference/inventory.md). Record hostname, installed Omarchy version from its About screen or installed version command, BIOS version, disk layout, and Ethernet address. Keep raw output and serial numbers in ignored `local/`, not Git.

Use `home-lab` for the HP, following the [planned device names](../reference/inventory.md#planned-device-names). Keep lowercase letters and hyphens, not underscores such as `home_lab`. This follows [systemd's hostname guidance](https://www.freedesktop.org/software/systemd/man/258/hostname.html) and gives us a name suitable for DNS.

Set the name before enrolling in Tailscale:

```sh
sudo hostnamectl set-hostname home-lab
hostnamectl --static
sudo timedatectl set-timezone Europe/Zurich
```

Expect `home-lab` from `hostnamectl --static`. If `/etc/hosts` contains the old hostname, update that entry while preserving the localhost entries. Do not add the Tailscale address there; check private name resolution in step 5. The Pi names are future proposals, not changes to make during HP setup.

Check that the clock reports synchronization. Inspect `systemctl status systemd-timesyncd` if it does not. Use one time synchronization service rather than enabling a second one blindly. Confirm normal DNS resolution with `getent hosts archlinux.org`. Reserve the HP's Ethernet address in the router's DHCP settings if convenient; retain automatic network configuration on the HP. Record its LAN address for denial tests later.

At the next firmware visit, record existing settings and look for the HP option to power on after AC loss. Choose power-on recovery if available. Do not clear TPM keys or flash guessed firmware. Match any firmware download to the actual HP product number, use reliable power, and follow HP's instructions.

## 2. Update Omarchy and install missing tools

Read current [Omarchy update instructions](https://omarchy.org/manual/updates/) and release notices. Run the supported updater from the maintenance account:

```sh
omarchy update
```

Use the stable channel. Do not replace its updater with `pacman -Syu`, `yay -Syu`, or a scheduled unattended upgrade. Omarchy updates include its own migrations and snapshot handling. Review any requested intervention before continuing.

Check packages before adding them:

```sh
pacman -Q openssh tailscale tmux restic smartmontools git
```

A missing package produces an error for that name. Add each missing package through the documented [package command](https://omarchy.org/manual/other-packages/), for example:

```sh
omarchy pkg add openssh
omarchy pkg add tailscale
omarchy pkg add tmux
omarchy pkg add restic
omarchy pkg add smartmontools
```

Run only the lines you need. Add `git` through the same command if absent. Use official packages where available. Review third-party build recipes before installing AUR packages. Avoid `pacman -Sy` followed by individual package installs: Arch does not support partial upgrades. See [Arch maintenance](https://wiki.archlinux.org/title/System_maintenance).

Inspect the SSD after identifying its device:

```sh
sudo smartctl --scan
```

Run `sudo smartctl -a DEVICE` using the device reported above, such as `/dev/nvme0`. Review critical warnings, media errors, temperature, and wear. A successful health summary alone does not prove a used SSD is sound. If errors appear, resolve them before storing important work. Keep firmware and memory testing available through HP diagnostics.

## 3. Separate maintenance from coding

Keep the installer account for updates and administration. Create a second account for repositories and agents:

```sh
sudo useradd --create-home --shell /bin/bash coder
sudo passwd coder
sudo chmod 700 /home/coder
id coder
sudo -l -U coder
```

Choose a local recovery password and save it outside the HP. `coder` must not have sudo permission or membership in `wheel`, `docker`, or `disk`. Stop if `sudo -l -U coder` grants commands. Review `/etc/sudoers` and `/etc/sudoers.d/` with `visudo` before using agents. Do not enable Omarchy's optional passwordless sudo or sudoless Docker settings.

Run `chmod 700 "$HOME"` while logged in as the maintenance account if its home is accessible to other users. This prevents ordinary reads by `coder`; it does not isolate projects that all run as `coder`. Keep maintenance keys, backup deletion credentials, and unrelated personal files out of that account. See [agent isolation](../.okf/technologies/agent-isolation.md).

## 4. Prepare laptop SSH keys before restricting login

On the Mac, inspect existing public keys with `ls ~/.ssh/*.pub`. Use an existing suitable key or create a dedicated one:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/hp_homelab -C hp-homelab
cat ~/.ssh/hp_homelab.pub
```

Use a passphrase. Transfer only the public key to the HP console, for example with a USB drive. Never copy the private key to the HP.

On the HP, create the coding account's key file. The example uses Omarchy's Neovim editor; use another installed editor if you prefer:

```sh
sudo install -d -m 700 -o coder -g coder /home/coder/.ssh
sudo -u coder nvim /home/coder/.ssh/authorized_keys
sudo chmod 600 /home/coder/.ssh/authorized_keys
```

Paste the public key on one line. Add your public key to the maintenance account's own `~/.ssh/authorized_keys` with directory mode 700 and file mode 600. Both accounts need the public key installed before starting SSH. Keep the console available to fix a mistyped key.

## 5. Establish private connectivity

Install or update Tailscale on the Mac through its official distribution. Enable multifactor authentication on the identity account used for Tailscale. At the HP console:

```sh
sudo systemctl enable --now tailscaled.service
sudo tailscale up
sudo tailscale set --ssh=false
tailscale version
tailscale status
tailscale ip -4
```

Follow the enrollment URL. In the Tailscale admin console, confirm this device is named `home-lab`, without an unexpected numeric suffix. If it is not, inspect duplicate or stale device records before renaming the intended device. Do not delete another active device to free the name. Enable MagicDNS if you want to use `home-lab` as a private network name, then check `dscacheutil -q host -a name home-lab` on the Mac. The result must match the HP's Tailscale address. Use the full MagicDNS name shown in the console if the short name does not resolve. A LAN DNS name and a Tailscale name are separate; do not expose either through public DNS. See [Tailscale machine names](https://tailscale.com/docs/concepts/machine-names).

`tailscale up` is for initial enrollment; do not use reset or logout commands through your only working connection. This guide uses OpenSSH rather than Tailscale SSH.

Review the tailnet access policy before relying on it. Allow your intended Mac identity or device to reach this HP on TCP 22. Review existing broad allow rules too; adding a narrow grant does not remove them. Preserve access needed by existing devices. The [private access research](../research/private-access.md#tailnet-policy-and-device-identity) has an example to adapt, policy references, and device-expiry details. Review the HP's key expiry so it does not unexpectedly lose access. Keep router port forwarding, Tailscale Funnel, exit-node advertising, and subnet routing off for this baseline.

Inspect the firewall at the console:

```sh
sudo ufw status verbose
sudo ufw status numbered
sudo ss -lntup
```

Confirm UFW is active with default incoming denial and outgoing allowance. If it is inactive or has different defaults, review the existing rules at the console before enabling or correcting it; do not continue on the assumption that it protects SSH. If needed, add the interface-specific SSH allowance:

```sh
sudo ufw allow in on tailscale0 to any port 22 proto tcp
```

Tailscale manages additional firewall rules, so its policy also controls access. This UFW rule alone is not the access boundary. Do not reset the firewall or copy an Ubuntu rule set over Omarchy's existing Docker integration. See [Tailscale firewall guidance](https://tailscale.com/docs/how-to/secure-ubuntu-server-with-ufw).

Keep SSH stopped until the key-only configuration in step 6 passes its syntax check. If it is already running, stop it with `sudo systemctl stop sshd.service` at the local console while you configure it. This ends any existing SSH sessions.

## 6. Harden SSH without losing access

At the HP console, save the original configuration and create any missing host keys:

```sh
sudo install -d -m 700 /root/hp-setup-recovery
sudo cp -a /etc/ssh /root/hp-setup-recovery/ssh-before-hardening
sudo ssh-keygen -A
```

Run the backup once before editing; keep it for rollback. `ssh-keygen -A` creates missing host keys without replacing existing ones. See the [Arch SSH key manual](https://man.archlinux.org/man/ssh-keygen.1.en). Inspect the main file's `Include` directive and existing files in `/etc/ssh/sshd_config.d/`. Omarchy's SSH setup helper can already have written a hardening file and opened port 22 broadly. OpenSSH usually takes the first obtained setting, so a later file does not necessarily override an earlier one.

Use `sudoedit` to edit the appropriate administrator configuration. Apply these global values before any `Match` section. Replace `MAINTENANCE_USER` with the real installer account:

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
AllowUsers MAINTENANCE_USER coder
AllowAgentForwarding no
X11Forwarding no
AllowTcpForwarding local
GatewayPorts no
```

Preserve local forwarding for development tools. Validate before starting or restarting SSH:

```sh
sudo sshd -t
sudo sshd -T
```

Stop on any syntax error. Check that effective settings match the intended values. If existing `Match` sections apply, also inspect `sshd -T -C user=coder,host=CLIENT_NAME,addr=CLIENT_TAILSCALE_IP` with real client values. Then enable SSH at boot and start it with the validated configuration:

```sh
sudo systemctl enable sshd.service
sudo systemctl restart sshd.service
sudo ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
```

The restart happens at the local console, with recovery available. From a Mac terminal, replace `HP_TAILSCALE_IP` with the actual Tailscale address:

```sh
ssh -i ~/.ssh/hp_homelab -o IdentitiesOnly=yes -o PreferredAuthentications=publickey coder@HP_TAILSCALE_IP
```

Compare the first-connect fingerprint with the console before accepting it. Repeat for the maintenance account. Keep these working sessions open while removing broader firewall access. Test rejection from a fresh Mac terminal. The first command must fail because passwords are disabled. The second must fail with a key that is not listed in `authorized_keys`; replace `UNAUTHORIZED_KEY` with that private key's actual path. `-F /dev/null` skips client shortcuts and connection sharing, and `IdentityAgent=none` prevents an agent from supplying an authorized key.

```sh
ssh -F /dev/null -o PubkeyAuthentication=no -o PreferredAuthentications=password,keyboard-interactive coder@HP_TAILSCALE_IP
ssh -F /dev/null -i UNAUTHORIZED_KEY -o IdentitiesOnly=yes -o IdentityAgent=none -o PreferredAuthentications=publickey coder@HP_TAILSCALE_IP
```

A missing key file is not a successful rejection test. Confirm the client actually offers the unlisted key with `ssh -v` if needed. Root login must fail too. These controls follow the [OpenSSH configuration manual](https://man.openbsd.org/sshd_config).

Now remove broad UFW SSH allow or limit rules using their current numbered entries, one at a time with `sudo ufw delete NUMBER`. Numbers change after deletion. Keep the `tailscale0` allowance. Recheck both new remote logins. Do not remove Docker-specific rules as part of SSH cleanup.

On the Mac, add an alias to `~/.ssh/config`:

```sshconfig
Host home-lab
    HostName HP_TAILSCALE_IP
    User coder
    IdentityFile ~/.ssh/hp_homelab
    IdentitiesOnly yes
    ForwardAgent no
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Replace the address with the actual Tailscale IP, or the full MagicDNS name you checked in step 5. `Host home-lab` is a Mac SSH shortcut; `HostName` selects the actual destination. Test `ssh home-lab`. Add a second block called `home-lab-admin` with the same destination and maintenance username for administration. Avoid `ssh -A`.

## 7. Remove unused listeners and prevent sleep

Keep this pass focused on services with a confirmed purpose or a listening network port. Bulk removal of desktop packages, a different firewall, and extra intrusion-detection tools are not arrival-day requirements.

Inspect actual enabled services rather than assuming desktop defaults are useful on a server:

```sh
systemctl list-unit-files --state=enabled
systemctl list-sockets --all
sudo ss -lntup
sudo ufw status numbered
```

If printing and local discovery are unused, stop and disable the installed CUPS and Avahi service and socket units shown by these commands. If LocalSend is unused, remove its UFW exceptions after identifying them. Remove any other unneeded desktop-sharing exceptions. Leave DNS, network management, time synchronization, and Tailscale intact. Do not disable a service just because its name is unfamiliar.

Inspect `docker.service` and `docker.socket`. If you do not yet need containers, disable both installed units. Socket activation can otherwise restart Docker. When containers become necessary, follow section 9 before starting any published service.

Create the drop-in directory, then edit the sleep policy:

```sh
sudo install -d -m 755 /etc/systemd/sleep.conf.d
sudoedit /etc/systemd/sleep.conf.d/90-home-lab.conf
```

Save this content:

```ini
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
```

Inspect all merged settings with `systemd-analyze cat-config systemd/sleep.conf`. Resolve any later conflicting drop-in. Keep desktop screen locking enabled. Omarchy's idle and suspend menu toggles do not establish this host-wide policy. See [systemd sleep settings](https://man.archlinux.org/man/systemd-sleep.conf.5.en).

Keep the desktop for local recovery at first. Investigate autologin separately if present. Do not remove the desktop or change its startup services before remote access works after reboot. To undo the sleep policy, remove only this drop-in and recheck the merged settings.

## 8. Start one trusted coding project

Log in as `coder`. Create `~/projects`, configure your Git name and email, and clone one trusted repository. Give the HP its own limited Git credentials. Keep laptop private keys and agent forwarding out of this workflow.

Install only that project's required runtimes and package manager. Omarchy uses mise for many tools, but the new account does not automatically inherit the desktop user's setup. Check `command -v git node mise` and the project's version files. Follow the runtime's official setup instructions under `coder`; do not copy the administrator's entire home or run package scripts as root. See [Omarchy development tools](https://omarchy.org/manual/development-tools/).

Install one agent, Pi or OpenCode, from its current official instructions linked in [remote coding research](../research/remote-coding.md) and [OpenCode research](../research/opencode-v2.md). Confirm the exact executable and version. Use a scoped provider credential, store it privately, and verify the account's file permissions. Keep approvals on for actions that need review. A private connection does not sandbox shell commands.

Start a persistent terminal:

```sh
tmux new -s work
```

Run a small build or test inside it. Detach with `Ctrl+b`, then `d`. Disconnect SSH, reconnect, and run `tmux attach -t work`. Confirm the same session remains. tmux survives connection loss, not reboot. Reopen saved agent sessions after reboot using that tool's documented resume command. Record the actual session-storage paths for backups.

Use separate worktrees for concurrent tasks. Begin with one agent and inspect `free -h`, `df -h`, and `top` during a representative build before increasing concurrency. Keep each active task on one machine. Push committed work for a Mac handoff and separately preserve uncommitted files and conversations.

For a browser UI or development server, bind the application to HP loopback and use an SSH tunnel from the Mac:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:3000:127.0.0.1:3000 home-lab
```

Open `http://127.0.0.1:3000` on the Mac. Inspect the HP listener with `ss -lntup`. Require application authentication where supported. Add a persistent systemd service only when you select a daily interface and have tested its authentication and restart behavior; do not enable lingering for every user in advance.

## 9. Keep future containers private

Skip this section until a project needs containers.

When a trusted project needs Docker, inspect the existing installation rather than reinstalling it. Keep `coder` out of the `docker` group; access to the rootful Docker socket grants powerful host control. Provision required containers from the maintenance account after reviewing the Compose file. Rootless containers or project VMs are separate options if the project needs them.

For a service the Mac needs, publish only on loopback:

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

Do not publish databases needed only by other containers. Avoid host networking, privileged containers, and mounting the Docker socket into agent tools. Inspect `sudo docker ps` port mappings and test from another LAN device. Docker publishing can bypass ordinary UFW filtering; keep Docker's own firewall management enabled. Verify the current engine's localhost-publishing behavior against [Docker's firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/). See [network exposure research](../research/private-access.md#firewall-and-docker).

## 10. Make and restore the first off-machine backup

Choose the destination before relying on the HP. Use another device or a storage service, with encrypted restic data and recovery credentials saved outside the HP. Root snapshots and Git pushes do not protect all home-directory work. See [backup research](../research/backups.md).

Before the backup, create a small uncommitted file in the test project and save an agent conversation. Identify both exact absolute paths and stop agents for a consistent first copy. Include any Git worktrees and their common repository data, even when they live outside `~/projects`.

For a first manually mounted external-disk experiment, replace `/mnt/backup` with the actual mount. Do not proceed unless `findmnt` confirms the intended external filesystem. Run each command separately from the maintenance account. Stop if the mount check fails or reports the HP root filesystem:

```sh
findmnt --mountpoint /mnt/backup
sudo restic -r /mnt/backup/hp-restic init
sudo restic -r /mnt/backup/hp-restic backup /home/coder /etc
sudo restic -r /mnt/backup/hp-restic snapshots
sudo restic -r /mnt/backup/hp-restic check
```

Run `init` only for a new repository. After reconnecting a disk, repeat the mount check before every backup command. The example backs up `/home/coder` and `/etc`; extend it if required data lives elsewhere, and separately preserve the maintenance account's needed configuration in the encrypted backup. Enter the repository password when prompted, not in a command argument. If a backup exits nonzero or reports unreadable files, investigate before calling it successful. Full-home backup captures secrets as well as work, so protect repository access. Use application-consistent dumps for databases. See [restic backup instructions](https://restic.readthedocs.io/en/stable/040_backup.html).

Choose the resulting snapshot ID from `snapshots`. Restore only the two test paths to a new private directory. Replace `SNAPSHOT_ID`, `UNCOMMITTED_FILE_PATH`, and `AGENT_SESSION_PATH` with the actual values:

```sh
sudo install -d -m 700 /var/tmp/hp-restore-test
sudo restic -r /mnt/backup/hp-restic restore SNAPSHOT_ID --target /var/tmp/hp-restore-test --include UNCOMMITTED_FILE_PATH --include AGENT_SESSION_PATH
```

Compare the restored file with the original. Copy the restored agent data into an isolated test profile and verify it can reopen without overwriting the working session. Restore paths include the original directory hierarchy. See [restic restore instructions](https://restic.readthedocs.io/en/stable/050_restore.html). Remove the private restore directory after inspection.

Once this works, configure a daily backup timer for the chosen backend. It must check mount availability when relevant, use protected credentials, report failures, and expose the last successful run. Test its service manually and deliberately test an unavailable destination. Scheduling, retention, and notifications depend on the destination; record the actual units and recovery steps here when chosen. Do not run pruning before agreeing retention. Keep an independent offline or off-site copy, and prevent the coding account from deleting every copy.

## 11. Prove access and recovery before putting it in the rack

Run the matching checks in the [preparation checklist](preparation.md) and record measured facts in the inventory and service register.

1. Open fresh SSH sessions to both accounts. Confirm password login, root login, and a key absent from `authorized_keys` fail. Confirm `coder` cannot use sudo or read maintenance credentials.
2. From another LAN device, try the HP's LAN address on port 22 and each application port. These connections must fail. Test IPv6 too if the HP has it. Use `nc -vz -w 3 ADDRESS PORT` or a browser as appropriate.
3. Test an unauthorized tailnet identity or device where available. It must fail according to policy. A test from another device with the same authorized identity does not prove identity denial.
4. Move the Mac onto a phone hotspot. Confirm Tailscale and a fresh SSH login work without router forwarding. Confirm the tmux session survives a laptop disconnect.
5. Reboot the HP with the console attached. Verify it boots without a disk prompt, Tailscale and SSH return, and a new login works before anyone logs into the desktop. Start a new tmux session as needed.
6. Disconnect the monitor and leave the HP idle overnight. Recheck access, uptime, temperatures, disk space, and `systemctl --failed` the next morning.
7. After a clean shutdown, test AC restoration behavior with no important jobs active. Do not pull power from a running filesystem for this test. Verify cooling and cable clearance in the final rack position.
8. Complete the off-machine restore test. Keep the USB installer, account recovery information, Tailscale identity recovery, and backup password accessible without the HP.

If a check fails, keep the console available and fix it before depending on unattended operation. Do not mark an unavailable unauthorized-device test as passed.

A backup destination, scheduled backup job, retention policy, failure notification route, and daily Mac client still need choosing. The restore test and scheduled backups are required before the HP holds the only copy of important work. Client selection and container setup can wait; the baseline works with SSH and tmux.

## Maintain it and recover from mistakes

Review updates weekly, plus urgent vendor security notices when issued. Before an update, finish important jobs, confirm a recent backup, and ensure local recovery access. Run `omarchy update`, review configuration changes and `.pacnew` files, then repeat fresh-login and reboot checks when the update affects them. Avoid long gaps between rolling-release upgrades.

Check free space, failed units, SSD health, and backup success during maintenance. Investigate growth before deleting caches, snapshots, or containers. Skip automatic cleanup that might remove the recovery copy you need.

If SSH changes lock you out, use the console. Restore the saved SSH configuration, run `sshd -t`, reload SSH, and inspect UFW plus Tailscale policy separately. If only the application fails, inspect its listener and logs before changing the firewall.

If an update prevents boot, use the Limine snapshot recovery path from the [current Omarchy snapshot manual](https://omarchy.org/manual/system-snapshots/). Recheck the exact recovery command before use. Root restoration leaves `/home` unchanged, so user configuration may still reflect the newer release. Recover projects and agent data from the off-machine backup when needed. The boot USB and local console remain the fallback for broken networking or an unusable boot menu.
