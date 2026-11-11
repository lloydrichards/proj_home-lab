# Evidence for the HP post-install guide

Sources checked on 7 November 2026. These are researched upstream behaviors and examples, not observations of the HP. Moving `master` links may differ from the installed release. Compare the local scripts and effective configuration during setup. The [HP preparation checklist](../preparation.md) owns upcoming work; [Omarchy and headless operation](omarchy.md), [private access](../../../research/private-access.md), and [backups](../../../research/backups.md) explain the existing recommendations.

## What Omarchy already supplies

| Area | Primary-source evidence | Consequence for our guide |
|---|---|---|
| Networking | The [networking manual](https://github.com/omacom/omarchy/blob/master/manual/35-networking.md) describes NetworkManager, DHCP-provided DNS, `nmtui`, and an optional Tailscale service install. | Use wired Ethernet and keep working DHCP/DNS initially. Check for Tailscale before installing it. |
| Firewall | The [installer firewall script](https://github.com/omacom/omarchy/blob/master/install/config/firewall.sh) sets incoming deny and outgoing allow, opens LocalSend TCP/UDP 53317, adds Docker-to-host DNS allowances, installs `ufw-docker`, and enables UFW. The [security manual](https://github.com/omacom/omarchy/blob/master/manual/48-security.md) also calls out multicast DNS and UFW's standard protocol allowances. | Inspect effective rules rather than calling this an SSH-only machine. Remove unnecessary sharing exceptions deliberately. Preserve container DNS and Tailscale's own rules. |
| SSH | The [SSHD helper](https://github.com/omacom/omarchy/blob/master/bin/omarchy-setup-security-sshd) authorizes a key, writes `/etc/ssh/sshd_config.d/10-omarchy-hardening.conf`, disables password and keyboard-interactive authentication, validates effective settings, enables SSHD, and adds a broad `ufw limit 22/tcp` rule. | The helper's default network exposure is wider than our private-only baseline. Replace that allowance after testing Tailscale access. Check `sshd -T`, including root login and forwarding settings, rather than assuming the helper covers every hardening choice. |
| Docker privileges | The [Docker configuration](https://github.com/omacom/omarchy/blob/master/install/config/docker.sh) deliberately avoids adding the installer user to `docker`. Its comments explain that Docker group membership permits root-level host changes. | Do not copy older recipes that add the coding account to `docker`. Leave optional sudoless Docker and passwordless sudo off. |
| Services | The [service-enabling script](https://github.com/omacom/omarchy/blob/master/install/config/enable-services.sh) includes CUPS, Avahi, Docker socket activation, NetworkManager, and systemd-resolved. | Inspect active services and sockets. Disable printing/discovery only after checking dependencies and whether the HP needs them. Stopping `docker.service` alone does not prevent socket activation. |
| Recovery | The [snapshot configuration](https://github.com/omacom/omarchy/blob/master/install/config/snapper.sh) configures root snapshots, disables the timeline timer, and enables cleanup and Limine snapshot synchronization. The [snapshot manual](https://learn.omacom.io/2/the-omarchy-manual/101/system-snapshots) describes manual creation with `omarchy-snapshot create` and restoration through Limine. `/home` stays unchanged. | Rehearse root recovery while a console is attached. Back up workspaces and agent sessions separately. Do not assume hourly snapshots exist. |

The [security manual](https://github.com/omacom/omarchy/blob/master/manual/48-security.md) describes encryption as the default with an installer opt-out. That earlier unencrypted preference was superseded on 9 November by [TPM unlock with a retained passphrase](../../../.okf/decisions/home-lab/unattended-boot.md). The inventory owns the installed layout. The same manual describes optional passwordless sudo, which grants all processes under that user unrestricted root access while enabled.

The current [Omarchy updates manual](https://omarchy.org/manual/updates/) is the update authority for this derivative. Use `omarchy update` and inspect its installed help. The earlier [Omarchy research](omarchy.md) records its combined migrations, configuration, package, and snapshot behavior. Avoid substituting generic Arch full-upgrade commands without checking Omarchy's current guard and mirror policy.

## Arch maintenance that still matters

The [Arch system-maintenance page](https://wiki.archlinux.org/title/System_maintenance) recommends regular full upgrades, reading Arch news, acting on package-manager warnings, handling `.pacnew` and `.pacsave` files, checking failed services and logs, testing backups, keeping installation media, and reviewing firmware updates. It explicitly rejects partial upgrades such as `pacman -Sy package`. Apply those principles through Omarchy's supported updater. This page's search-index content was available; direct retrieval encountered ArchWiki's anti-bot page.

For our guide, schedule attended updates with time for recovery, keep a USB installer, and check `systemctl --failed` after reboot. Treat `.pacnew` changes as a review and merge task, not a command to overwrite working SSH or firewall settings.

## Private access and container boundaries

[Tailscale's firewall documentation](https://tailscale.com/docs/integrations/firewalls) says most networks need no extra inbound ports; relays provide a fallback when direct connections fail. Its [UFW tutorial](https://tailscale.com/docs/how-to/secure-ubuntu-server-with-ufw) demonstrates restricting ordinary incoming traffic to Tailscale. That tutorial targets Ubuntu, so use its access principle rather than its package/service commands or a firewall reset on Omarchy.

Tailscale can manage its own packet-filtering path. A restrictive UFW input rule does not establish least-privilege access within the tailnet. Review tailnet grants separately, keep Tailscale SSH off for the chosen OpenSSH baseline, and test authorized tailnet access and denied LAN access independently. The detailed policy and lockout-safe procedure remain in [private access](../../../research/private-access.md).

[Docker's firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/) explains that published container traffic can bypass UFW input rules. Keep databases unpublished, bind development HTTP ports to `127.0.0.1`, and use SSH forwarding. Test from another LAN machine. Omarchy's `ufw-docker` integration is useful defense but does not remove the need to inspect actual published ports.

[Restic's repository guide](https://restic.readthedocs.io/en/stable/045_working_with_repos.html) distinguishes repository consistency checks from reading backup data. A successful metadata check is not a complete data-read or restoration test. Use an encrypted off-host destination, restore selected work into a separate directory, and verify contents before relying on a scheduled backup.

## What other homelabs contribute

These are owners describing their own setups, not requirements to reproduce their scale.

- [Jeff Geerling's homelab automation presentation](https://www.youtube.com/watch?v=yoFTL0Zm3tw) discusses using Ansible for configuration, backups, testing, patching, upgrades, and hardware replacement. Adaptation here: record repeatable steps first; automate them after the first machine proves the procedure. We do not need Ansible on arrival day.
- [Tuero's home-lab documentation](https://tuero.github.io/homelab/home-lab) separates inventory, routing, deployment, recovery, and manual prerequisites. It explicitly distinguishes what its automation configures from what it does not create or restore. Adaptation here: record machine identity, access, disk layout, and manual recovery steps, and keep setup instructions distinct from deployment evidence.
- [smdion's homelab-ops repository](https://github.com/smdion/homelab-ops) separates backups, backup verification, restores, rollback, and health checks. Its verification includes restoring databases to temporary instances. Adaptation here: a completed backup command is only one check; rehearse restoring uncommitted work and agent state before the HP becomes essential. Its orchestration and monitoring stack would add unnecessary first-day work.

The proposed guide should adopt these operational habits without adding Kubernetes, Proxmox, a metrics stack, or a migration of the existing Pi services to the first setup.

## Hostname and first-access review

On 7 November 2026, Lloyd suggested `home_lab`, `remote_lab`, and `admin_lab`. [systemd's hostname manual](https://www.freedesktop.org/software/systemd/man/258/hostname.html) recommends a single DNS label with lowercase letters, digits, and hyphens. The guide uses the hyphenated forms; the inventory records the device mapping as proposed.

[Tailscale machine names](https://tailscale.com/docs/concepts/machine-names) are initially derived from the OS hostname but must be unique and can be edited independently. With automatic naming enabled, an OS name change is reflected when Tailscale next starts. A duplicate name may receive a suffix. Setup therefore names the HP before enrollment, checks its registered name, and tests MagicDNS resolution from the Mac. It does not rename the running Pis.

The [Arch SSH key manual](https://man.archlinux.org/man/ssh-keygen.1.en) documents `ssh-keygen -A` for missing default host keys. Generate missing keys and validate a key-only configuration at the console before first starting SSH. The [sshd manual](https://man.archlinux.org/man/sshd.8.en) documents `-t`, `-T`, and connection-specific `-C` checks. Test an unlisted key as well as password rejection.

The [restic restore manual](https://restic.readthedocs.io/en/stable/050_restore.html) supports `--include` for selected paths. The first recovery exercise needs only the uncommitted file and saved agent state, rather than a second full copy of the home directory. Create those files before taking the backup.
