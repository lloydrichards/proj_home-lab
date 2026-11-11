# Update and recover home-lab

Use the maintenance account for host updates and `coder` for user tools. Keep local console access, the disk passphrase, and a recovery USB available for boot-related changes. Check current versions and known limits in the [service register](../../_reference/services.md).

## Update the host

1. Finish active jobs and confirm a recent successful backup:

```bash
	systemctl show lab-agent-backup.service -p Result -p ExecMainStatus
	sudo /usr/local/sbin/lab-agent-backup health
	systemctl --failed
	df -h / /home
```

Stop if the backup is stale, disk space is low, or a failed service affects recovery.

2. Read the current [Omarchy update guidance](https://omarchy.org/manual/updates/) and release notices. Run `omarchy update` through the supported workflow. Review requested interventions and `.pacnew` files.
3. After a boot-related update, verify the generated boot entry and image before rebooting. Follow [unattended boot](configure-unattended-boot.md) for the recorded Limine checks.
4. Reboot only after confirming local recovery access. Test fresh SSH logins and inspect `systemctl --failed` after startup.

Do not replace the Omarchy updater with an unattended package-upgrade timer. Do not use `pacman -Sy` followed by individual package installs.

## Update user tools and maintained scripts

1. As `coder`, inspect the executable and version before updating an agent. Use that installation's own manager; avoid adding a second executable with the same name.
2. For shared skills, integrate the reviewed source revision, inspect the installation plan, then apply through the [skills workflow](../../../research/shared-agent-skills.md). Preserve local edits before changing generated installations.
3. For backup or publishing scripts, review the source diff and run its documented checks before reinstalling. Source edits do not update root-owned installed copies.
4. Treat each installer according to its [interface](../reference/automation.md#installer-effects). The agent installer runs a complete backup and restore drill. The Pi home installer normally creates a Pi maintenance outage; use its `--refresh-services` mode only when that narrower update is intended.

## Recover access or boot

If SSH fails after a configuration change, use the console. Restore your saved SSH configuration, run `sshd -t`, and reload the matching SSH service. Inspect UFW and Tailscale policy separately before changing either. Do not reset Tailscale or delete trust records without verifying the intended host.

If TPM unlock fails, enter the retained disk passphrase locally. Inspect the boot logs and restore the reviewed password-based configuration. Do not wipe password slots or clear the TPM as a troubleshooting step.

If an update prevents normal boot, use Limine's recovery entry or the installer environment. Consult the matching [Omarchy snapshot instructions](https://omarchy.org/manual/system-snapshots/) before applying rollback. A root rollback leaves home data on its separate subvolume unchanged. Restore agent state separately with the [conversation recovery guide](restore-agent-conversation.md). Project recovery relies on GitHub and omits uncommitted or unpushed work.

## Check unattended operation

After the machine works at the console, test a fresh remote login. Check the effective sleep policy with `systemd-analyze cat-config systemd/sleep.conf`. Keep desktop locking enabled.

Test cold startup, overnight availability, and AC-restoration behavior separately. Record only checks that actually ran in [preparation](../preparation.md). Stop optional services individually if they prevent recovery; do not disable unfamiliar networking, DNS, time, or backup services in bulk.
