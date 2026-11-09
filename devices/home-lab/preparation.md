# HP readiness and remaining work

This is the single list of remaining HP work. Current facts live in the [inventory](../_reference/inventory.md), access in the [service register](../_reference/services.md), and commands in the [setup guide](setup.md).

## Completed on 9 November 2026

- [x] Install Omarchy on the internal SSD and update through Omarchy, user reported.
- [x] Confirm CPU, usable memory, SSD model, firmware identity and hostname `home-lab`.
- [x] Check Ethernet, internet, DNS and synchronized clock.
- [x] Create separate `lloyd` maintenance and `coder` coding accounts; key login works for both.
- [x] Disable password and root SSH login; test key login and rejection without keys.
- [x] Configure TPM disk unlock with retained password recovery; repair and verify Limine image hash; pass an untouched reboot.
- [x] Join Tailscale with Tailscale SSH disabled; user confirmed Mac SSH works over the private address, and assistant verified `lloyd` over that address.
- [x] Install OpenCode 2.2.6 for `coder`; verify terminal startup in tmux and a loopback-only server. See the [recipe](setup.md#opencode-on-the-installed-hp).

## Before routine use without a monitor

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
- [ ] Verify T3 service startup after a planned reboot. See the [recipe](setup.md#t3-code-remote-environment).

## Before relying on important work

- [x] Configure incoming remote-lab backups through a dedicated account; first encrypted backup, file/SQLite checks and isolated PostgreSQL restores passed on 9 November. See [operations](../remote-lab/backups.md).
- [ ] Save the incoming backup's restic password and the Pi's Coolify `APP_KEY` in the password manager outside both hosts; confirm retrieval without either host.
- [ ] Add an independent off-site or disconnected copy of the incoming Pi backup and choose a notification destination outside the HP; current alerts are local journal/terminal only.
- [ ] Choose an off-machine backup destination, then back up and restore a file and agent session. Install and configure backup tooling after choosing the destination. See [backup research](../../research/backups.md).
- [ ] Review Tailscale policy, device-key expiry and denial from an unauthorized device. Keep LAN SSH recovery until private access survives a cold start.
- [ ] Review listeners and unused sharing rules without breaking Docker DNS. Confirm router has no public SSH port forwarding.
- [ ] Run memory diagnostics and check firmware updates for the actual HP SKU during a recovery-ready maintenance window.
- [ ] Try one trusted project as `coder` with tmux; test disconnect/reconnect and a Mac/HP Git handoff. tmux survives disconnects, not reboots.
- [ ] Finish [Rex SSH access](setup.md#rex-over-ssh): enable linger with the maintenance password, open the host in Rex for Mac, and test reconnect. Remote Rex/OpenCode startup and SSH socket access passed.
- [ ] Connect OpenCode to the chosen provider and test one model request in a trusted project. No provider is authenticated yet.
- [ ] If needed, trial remote desktop separately. SSH is the current access method. See [remote desktop research](research/omarchy-remote-desktop.md).

The earlier unencrypted-install preference was superseded by authorized TPM unlock of the installed encrypted disk. See the [boot decision](../../.okf/decisions/home-lab/unattended-boot.md). Local devvm remains the choice for selected isolated Mac projects; HP project VMs remain deferred.
