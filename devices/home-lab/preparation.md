# HP readiness and remaining work

This is the single list of remaining HP work. Current facts live in the [inventory](../_reference/inventory.md), access in the [service register](../_reference/services.md), and commands in the [task guides](README.md#operate-and-recover).

## Completed on 9 November 2026

- [x] Install Omarchy on the internal SSD and update through Omarchy, user reported.
- [x] Confirm CPU, usable memory, SSD model, firmware identity and hostname `home-lab`.
- [x] Check Ethernet, internet, DNS and synchronized clock.
- [x] Create separate `lloyd` maintenance and `coder` coding accounts; key login works for both.
- [x] Disable password and root SSH login; test key login and rejection without keys.
- [x] Configure TPM disk unlock with retained password recovery; repair and verify Limine image hash; pass an untouched reboot.
- [x] Join Tailscale with Tailscale SSH disabled; user confirmed Mac SSH works over the private address, and assistant verified `lloyd` over that address.
- [x] Install OpenCode 2.2.6 for `coder`; verify terminal startup in tmux and a loopback-only server. See the [recipe](how-to/install-agent-tools.md#install-or-verify-opencode).

## Before routine use without a monitor

- [x] Repair IPv4 after the router replacement. DHCP renewal restored the gateway and IPv4 HTTPS to GitHub and its API on 12 November; Tailscale remained connected. [Repair and checks](../_reference/services.md#private-ssh-access).
- [ ] Test a fresh Mac SSH login after the router replacement. The old LAN SSH allowance may not cover the replacement router subnet; check the private network record. Keep Tailscale and console recovery available.

- [x] Apply system-wide sleep prevention; privileged output confirms all four sleep modes disabled.
- [x] Collect privileged SSD health, firewall, sudo policy and boot-hash checks; SMART passed with no media errors.
- [ ] Complete RAM module inventory after installing `dmidecode`; optional before monitor removal.
- [ ] Recheck effective SSH settings without the empty-output filter from the audit; installed configuration and key-login tests already passed.
- [ ] Check firmware AC-loss recovery at the console; select power-on recovery if wanted and available. Do not interrupt power to a running filesystem to test it.
- [ ] Confirm disk-unlock and root recovery passwords are saved off the HP. Keep monitor, keyboard and installer available for recovery.
- [x] Shut down normally, disconnect the monitor, power on, and verify both accounts over Tailscale without local input. Passed 9 November 2026; no failed system services.
- [ ] Leave headless and idle overnight; verify uptime, remote login, temperatures and failed services the next day.
- [ ] Confirm rack mounting, power-adapter support, airflow and cable clearance before racking.

## T3 remote environment

- [x] Install T3 Code 0.1.7 as `coder`; confirm active and enabled user service, lingering, and loopback-only listener.
- [ ] Connect the Mac T3 app through SSH, authenticate a provider on the HP, and test one trusted project and disconnect/reconnect.
- [ ] Verify T3 service startup after a planned reboot. See the [recipe](how-to/install-agent-tools.md#choose-terminal-persistence-or-a-client).

## Shared agent skills

- [x] Verify installation, conflict protection, Codex/OpenCode discovery, and a cross-machine source update. See [verified behavior and limits](../../research/shared-agent-skills.md#verified-behavior-and-limits). Migration backups remain retained.

## Before relying on important work

- [ ] Review Tailscale security maintenance: recorded HP **1.104.2-1** is below the **1.104.4** advisory fix; **1.104.5** is the stable target checked 9 November 2026. Follow the [lockout-safe maintenance guidance](../../research/private-access.md#pending-tailscale-maintenance) through Omarchy, then record the actual version. No update is recorded here.
- [x] Configure incoming remote-lab backups through a dedicated account; first encrypted backup, file/SQLite checks and isolated PostgreSQL restores passed on 9 November. See [operations](../remote-lab/backups.md).
- [x] Save the incoming backup's restic password and the Pi's Coolify `APP_KEY` in the password manager outside both hosts. Lloyd confirmed both saved on 11 November 2026; retrieval without either host remains to verify.
- [x] Add an independent off-site copy of incoming Pi backups in Cloudflare R2. Copying, a full data check, eight restored file checksums, initial automation and 14-daily/8-weekly/6-monthly retention passed on 11 November 2026. Future scheduled execution remains to observe. See [R2 operations](../remote-lab/how-to/configure-backups.md#add-the-off-site-repository).
- [ ] Configure email backup notifications outside the HP. Lloyd deferred this on 11 November 2026; current alerts remain local journal/terminal only.
- [x] Install and verify the [agent-session backup](agent-backups.md). Local and R2 backups, both restore checks and freshness passed on 11 November 2026; nightly 04:00 Zurich and hourly health timers are enabled. Lloyd excluded project checkouts and worktrees; GitHub recovery omits uncommitted/unpushed work.
- [x] Reopen a restored Codex conversation in an isolated profile. Lloyd's screenshot on 11 November showed the original 9 November user message and assistant reply from the R2-restored test profile.
- [ ] Observe the next scheduled agent backup and check its service result. Other agent interfaces and replacement-host authentication have not undergone reopening tests.
- [ ] Review Tailscale policy, device-key expiry and denial from an unauthorized device. Keep LAN SSH recovery until private access survives a cold start.
- [ ] Review listeners and unused sharing rules without breaking Docker DNS. Confirm router has no public SSH port forwarding.
- [ ] Run memory diagnostics and check firmware updates for the actual HP SKU during a recovery-ready maintenance window.
- [ ] Try one trusted project as `coder` with tmux; test disconnect/reconnect and a Mac/HP Git handoff. tmux survives disconnects, not reboots.
- [ ] Finish [Rex SSH access](how-to/install-agent-tools.md#choose-terminal-persistence-or-a-client): open the native remote host in Rex for Mac and test reconnect; user lingering is already enabled. Remote Rex/OpenCode startup and SSH socket access passed.
- [ ] Connect OpenCode to the chosen provider and test one model request in a trusted project. No provider is authenticated yet.
- [ ] If needed, trial remote desktop separately. SSH is the current access method. See [remote desktop research](research/omarchy-remote-desktop.md).

The earlier unencrypted-install preference was superseded by authorized TPM unlock of the installed encrypted disk. See the [boot decision](../../.okf/decisions/home-lab/unattended-boot.md). Local devvm remains the choice for selected isolated Mac projects; HP project VMs remain deferred.

## Agent backup review fixes

- [x] Install the patched agent-backup script and repeat local/R2 restore checks. Lloyd reported both passing on 11 November; live script hashes and successful service results match. Ancestor and frozen-root regressions pass. Full restored skill-installer reconciliation remains untested; see the [service register](../_reference/services.md#home-lab-agent-state-backups).
