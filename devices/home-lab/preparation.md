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

## Before relying on important work

- [ ] Review Tailscale security maintenance: recorded HP **1.104.2-1** is below the **1.104.4** advisory fix; **1.104.5** is the stable target checked 9 November 2026. Follow the [lockout-safe maintenance guidance](../../research/private-access.md#pending-tailscale-maintenance) through Omarchy, then record the actual version. No update is recorded here.
- [ ] Choose an off-machine backup destination, then back up and restore a file and agent session. Install and configure backup tooling after choosing the destination. See [backup research](../../research/backups.md).
- [ ] Review Tailscale policy, device-key expiry and denial from an unauthorized device. Keep LAN SSH recovery until private access survives a cold start.
- [ ] Review listeners and unused sharing rules without breaking Docker DNS. Confirm router has no public SSH port forwarding.
- [ ] Run memory diagnostics and check firmware updates for the actual HP SKU during a recovery-ready maintenance window.
- [ ] Try one trusted project as `coder` with tmux; test disconnect/reconnect and a Mac/HP Git handoff. tmux survives disconnects, not reboots.
- [ ] If needed, trial remote desktop separately. SSH is the current access method. See [remote desktop research](research/omarchy-remote-desktop.md).

The earlier unencrypted-install preference was superseded by authorized TPM unlock of the installed encrypted disk. See the [boot decision](../../.okf/decisions/home-lab/unattended-boot.md). Local devvm remains the choice for selected isolated Mac projects; HP project VMs remain deferred.
