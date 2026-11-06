# Omarchy as a mostly headless development host

User decision after this research: use an unencrypted disk for unattended restart. The main installation guide reflects that choice; the encryption options below document the tradeoff.

Research checked on 6 November 2026. This is a proposed configuration for the HP EliteDesk 800 G6 Mini, i5-10500T, 32 GB RAM, and 1 TB SSD. No commands in this article have been executed on the HP. Inspect the installed release before applying them.

## Install from the current ISO

Omarchy's supported installation starts from its ISO. A full-disk installation erases the selected drive. The current manual also describes installation in unallocated space, but dual boot adds no benefit to this dedicated host. Use Ethernet and a wired keyboard for initial setup. The encrypted boot prompt cannot use a Bluetooth keyboard. [Omarchy installation manual](https://omarchy.org/manual/getting-started/)

The manual instructs users to turn off Secure Boot and/or TPM for installation. Disable Secure Boot for the documented ISO path. Record existing firmware settings, and change TPM only if the current installer requires it. Do not clear TPM keys as a routine installation step. Firmware changes can affect access to an existing Windows installation. [Omarchy installation manual](https://omarchy.org/manual/getting-started/)

Recommendation: attach a monitor for installation and recovery, record the chosen hostname and user account, and verify the SSD identity before erasing anything. Record firmware version, Omarchy version, partition layout, and actual RAM population after installation. These remain unknown until the hardware is inspected.

## Choose how to unlock the disk

Encryption is enabled by default. The installer permits an unencrypted installation by pressing `Ctrl + C` at the disk-format confirmation. That is a documented option, not a requirement for headless operation. [Omarchy installation manual](https://omarchy.org/manual/getting-started/)

An encrypted machine normally needs someone to unlock it after a cold boot. Tailscale on the installed operating system cannot connect before that system starts. This is an operational consequence of pre-boot disk unlocking, not a Tailscale fault.

Choose one approach before installation:

- Keep encryption and plan local unlock after restarts. This protects a powered-off stolen drive and is the recommended starting point when someone can reach the rack.
- Choose an unencrypted installation only after accepting the physical-access risk. This supports unattended restarts but exposes the drive's contents to someone who removes it.
- Treat remote pre-boot unlock or hardware-assisted unlock as a separate project. Do not copy an unreviewed initramfs recipe into the first installation.

Recommendation: store the encryption recovery information outside this machine, and rehearse a cold boot while a monitor is attached. A UPS reduces power interruptions but does not remove the need to unlock an encrypted disk after restart.

## Inspect the firewall before adding rules

The current Omarchy manual describes UFW enabled with inbound blocking, but includes exceptions for LocalSend on 53317, multicast DNS on 5353, and container DNS through the Docker bridge. SSH starts disabled; the SSHD setup menu opens a rate-limited port 22. Omarchy also documents a `ufw-docker` integration. This is a description of upstream defaults, not proof of this host's effective rules. [Omarchy security manual](https://omarchy.org/manual/security/)

Recommendation: retain the firewall, remove desktop sharing exceptions that this server does not need, and allow administration only through the chosen Tailscale policy. Record the effective rules after installing Tailscale and again after installing container software. Avoid a global LAN or internet SSH allowance left over from setup.

Docker creates its own packet-filtering rules. Published container ports can bypass ordinary UFW input filtering. Docker warns that turning its firewall management off can break container networking. Keep unpublished services private, bind required development ports to loopback, and test reachability from another LAN device. Do not assume that UFW's default deny proves container isolation. [Docker firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/)

## Prevent power sleep without disabling screen locking

Omarchy's `omarchy toggle suspend` controls whether Suspend appears in the menu. It does not establish a server-wide sleep policy. `omarchy toggle idle` controls desktop locking and the screensaver, not power management. Retain local screen locking. [Omarchy system sleep](https://omarchy.org/manual/system-sleep/), [Omarchy idle behavior](https://omarchy.org/manual/toggles-idle-screensaver/)

For an always-on host, create `/etc/systemd/sleep.conf.d/90-home-lab.conf` with this proposed content:

```ini
[Sleep]
AllowSuspend=no
AllowHibernation=no
AllowSuspendThenHibernate=no
AllowHybridSleep=no
```

Systemd supports these settings and recommends administrator drop-ins rather than edits to the vendor file. Inspect other drop-ins because later filenames override earlier values. This blocks systemd-managed sleep paths, not shutdown, firmware behavior, or power failure. Removing this one file reverses the proposed policy. [systemd-sleep.conf manual](https://man.archlinux.org/man/systemd-sleep.conf.5.en)

Recommendation: test the effective policy locally, leave the host idle overnight, and verify access after the monitor is disconnected. Check firmware settings for restoration after AC loss separately.

## Keep services independent of the desktop

SSH access and coding processes do not require a running graphical desktop. Standard systemd supports a console-oriented `multi-user.target`, but changing the target alone is not proof that a distribution-specific autologin path is disabled. [systemd manual](https://man.archlinux.org/man/systemd.1.en)

Inspect before making a change:

```sh
systemctl get-default
systemctl cat getty@tty1.service
systemctl cat display-manager.service
loginctl list-sessions
```

A missing `display-manager.service` is possible and is useful information. Review the actual login service and shell startup files rather than assuming Omarchy uses a particular display manager. [systemctl manual](https://man.archlinux.org/man/systemctl.1.en), [loginctl manual](https://man.archlinux.org/man/loginctl.1.en)

Recommendation: first establish SSH, persistent terminal sessions, and recovery access. Then decide whether removing automatic desktop login saves enough resources to justify maintaining a local override. Do not uninstall the Omarchy desktop to make SSH work.

If a specific non-root service must run before login and after logout, systemd user lingering supports that behavior. Enable it only for the intended service account after reviewing the service:

```sh
sudo loginctl enable-linger ACCOUNT_NAME
loginctl show-user ACCOUNT_NAME -p Linger
```

Replace `ACCOUNT_NAME` with the actual account. Lingering keeps that user's service manager available; it does not restart arbitrary processes launched in an SSH shell. [loginctl manual](https://man.archlinux.org/man/loginctl.1.en)

## Update deliberately and retain recovery access

Use the stable channel and `omarchy update`. Current Omarchy upgrades combine packages, migrations, configuration changes, and a snapshot. Direct `pacman -Syu` or `yay -Syu` misses those steps and is blocked by an upstream guard. The stable Arch mirror currently lags upstream by one month. This trades faster package availability for upstream validation, so do not describe it as immediate access to every security fix. [Omarchy updates](https://omarchy.org/manual/updates/)

Run upgrades in a maintenance window with no important builds active and recovery access available. Review firmware updates separately. A BIOS update may require a restart. Avoid unattended rolling-system upgrades until recovery has been tested. [Omarchy updates](https://omarchy.org/manual/updates/)

Omarchy creates snapshots for updates and exposes `omarchy-snapshot create`. Recovery uses the Limine boot menu, then `omarchy-snapshot restore`. This restores the root filesystem but leaves `/home` unchanged. User configuration and migration records can therefore remain newer than the restored system. Snapshots do not recover deleted repositories or agent sessions in `/home`. [Omarchy snapshots](https://omarchy.org/manual/system-snapshots/)

Recommendation: keep separate encrypted off-host backups of repositories, uncommitted work, agent session files, and configuration. Test restoring one project. Retain a bootable USB and local console access for a failed network or boot update.

## Acceptance checks before removing the monitor

These are proposed checks, not completed results:

- Confirm Ethernet, time synchronization, available disk space, and the actual installed versions.
- Connect from the laptop through Tailscale in a second session before tightening SSH access.
- Verify private administration is rejected from an unauthorized device.
- Confirm a long-running agent survives laptop disconnect and reconnect.
- Verify no development service unexpectedly listens on every interface.
- Verify the host remains reachable after idle time and a controlled reboot.
- Check the chosen disk-unlock procedure after a cold boot.
- Restore a project from an off-host backup.
- Record which firmware and boot-menu steps recover a failed upgrade.

## Install packages through Omarchy

Current Omarchy documents `omarchy pkg add PACKAGE` for an official package. Use that documented path for `openssh`, `tailscale`, `tmux`, `restic`, and `smartmontools` if they are missing. Check the installed command's help before batching packages; this research verified the single-package form. Avoid AUR alternatives when the official repository contains the required package. [Omarchy packages](https://omarchy.org/manual/other-packages/)

Current Omarchy also installs many development tools through mise on their first launch. `mise ls --current` shows configuration, and `mise install gh` installs the GitHub CLI ahead of first use. Mise commands can take precedence over binaries in `~/.local/bin` and system packages. Verify paths and versions under the actual `coder` account before writing service units. That account may not inherit the desktop user's configuration. [Omarchy development tools](https://omarchy.org/manual/development-tools/)

The current default does not add the desktop user to the `docker` group, which Omarchy correctly describes as effectively root access. Keep `coder` out of that group and out of administrative groups. Do not enable the optional passwordless sudo or sudoless Docker features for coding agents. [Omarchy development tools](https://omarchy.org/manual/development-tools/), [Omarchy security manual](https://omarchy.org/manual/security/)
