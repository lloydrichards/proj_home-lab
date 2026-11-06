# Back up, maintain, and recover the HP

Run maintenance as `labadmin`. Run user-level repository backups as `coder` unless a separately reviewed backup service needs wider access. This procedure is proposed. The backup destination, schedule, and notification channel are still to choose.

## Define what must survive

Back up repositories including uncommitted files, agent conversations, tool configuration, and a private inventory of system changes. Keep credentials encrypted in the backup or export a separate recovery method to a password manager. A repository push does not preserve uncommitted files or local agent state.

Use an encrypted restic repository on another device or storage service. A second directory on the HP SSD does not protect against SSD failure or theft. An attached USB drive is a useful first destination; keep an additional offline or off-site copy for important work. Keep the repository password outside the HP too.

Omarchy snapshots cover root recovery but exclude `/home`. They are not a substitute for workspace or conversation backups. [Omarchy snapshot behavior](https://omarchy.org/manual/system-snapshots/)

## Perform a first manual backup and restore

Install restic first. Choose a mounted off-machine destination and substitute its real path below. Check that the device is mounted; otherwise a path under `/mnt` can silently write onto the HP's root filesystem. Do not initialize over an existing repository without checking it.

```bash
findmnt /mnt/backup
restic -r /mnt/backup/hp-lab-restic init
restic -r /mnt/backup/hp-lab-restic backup /home/coder
restic -r /mnt/backup/hp-lab-restic snapshots
```

Use the interactive password prompt for the first run. If `findmnt` fails, stop before the restic commands. Restic can exit nonzero for incomplete backups; treat warnings about unreadable files as failures to investigate. Stop agent processes for a consistent first backup of active session state. Database services need application-consistent dumps or a documented quiesce procedure rather than copying live storage blindly. [Restic backup instructions](https://restic.readthedocs.io/en/stable/040_backup.html)

Check the repository and restore the selected snapshot to a new private directory on a destination with enough free space:

```bash
restic -r /mnt/backup/hp-lab-restic check
mkdir -m 700 /home/coder/restore-check
restic -r /mnt/backup/hp-lab-restic restore SNAPSHOT_ID \
  --target /home/coder/restore-check
```

Replace `SNAPSHOT_ID` with the ID printed by `snapshots`. Verify an uncommitted source file, project configuration, and a saved agent session. Do not restore directly over a live home directory for the drill. Absolute source paths are recreated beneath the target. A normal `check` does not read every stored data block; schedule a full `check --read-data` when practical. [Restic repository checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html), [restore semantics](https://restic.readthedocs.io/en/stable/050_restore.html)

Before scheduling, exclude the restore-test destination from future backups or place future drills outside the backed-up tree. Review exclusions for dependency caches and build output without excluding irreplaceable local files. Keep Git metadata needed to recover worktrees.

## Automate only after the restore drill

Select a daily schedule and retention policy. Configure a systemd timer with a persistent missed-run policy and a service that checks the destination mount before writing. Store backup credentials outside this repository with access only for the backup identity. Alert on nonzero exit, insufficient disk space, missing mounts, or stale last-success time. Merely enabling a timer is not proof of successful backups.

Keep deletion or pruning separate from the first backup job. Preview retention before deleting snapshots. Do not give a compromised coding account the only credentials capable of deleting every backup copy. Document the storage service's append-only or immutable-copy capability if used.

## Maintain in a window with recovery access

Before an upgrade:

1. Stop or finish important builds and save agent sessions.
2. Confirm the latest off-machine backup succeeded and can be read.
3. Confirm local-console and boot-recovery access for the [chosen unencrypted installation](01-install.md#use-the-chosen-cold-boot-behavior). If a later decision enables encryption, also confirm a working unlock method.
4. Review the current Omarchy release notes and run `omarchy update`.
5. Review failed units, disk space, the firewall, Tailscale, and fresh SSH access.
6. Reboot only when needed, then repeat the private-access and workload checks.

Do not schedule blind system upgrades on this rolling desktop host. Omarchy's update path includes migrations and snapshots; a standalone package upgrade can bypass them. [Omarchy update procedure](https://omarchy.org/manual/updates/)

Use `df -h`, `free -h`, `systemctl --failed`, and `journalctl -p warning -b` for initial diagnostics. Check SSD health with the tool appropriate for the detected SATA or NVMe device. Keep diagnostics private until reviewed for secrets and addresses.

## Recover from common failures

| Failure | First action | Recovery |
|---|---|---|
| Laptop cannot connect | Check laptop Tailscale and HP power | Local console; inspect Ethernet, `tailscaled`, SSH, and expiry |
| Unexpected disk-unlock prompt | Inspect from the local console; the chosen installation is unencrypted | Check the actual disk layout and boot entry. If encryption was deliberately enabled later, use its documented unlock method |
| SSH change blocks login | Keep old session open | Restore the changed drop-in, run `sshd -t`, reload |
| Bad update | Use local console and Limine recovery | Follow current Omarchy snapshot restore; `/home` remains separate |
| SSD fails | Replace SSD and reinstall | Recreate users, restore selected backups, re-enroll Tailscale |
| Credential compromise | Isolate affected access | Revoke device and provider tokens, rotate scoped credentials, inspect or rebuild |

Keep a boot USB and the recovery notes accessible from the laptop or another device. Record a successful recovery drill rather than marking the host recoverable on the strength of this guide alone.
