# Back up agent sessions

Use the maintenance account on home-lab. This procedure installs the lab-specific agent backup job. For the design and exclusions, read [backup and recovery](../../../docs/explanations/backup-and-recovery.md). For exact inputs and paths, use the [automation reference](../reference/automation.md).

If you are replacing a lost machine, retrieve the existing repository password and R2 credentials before proceeding. Do not initialize a new repository over the existing cloud prefix. Restore the required state before starting agents on the replacement.

## Check the installation contract

1. Confirm the destination and filesystem:

```bash
	hostname -s
	findmnt --target /home
	command -v restic btrfs python3 findmnt
```

The current installer requires hostname `home-lab`, account `coder`, Btrfs home storage, and the paths in the reference. Stop and review the script constants if your new machine differs. The backup preflight also expects saved Codex transcripts and an OpenCode data directory.

2. Review the agent allowlist and exclusions in [agents.py](../backup-tools/agents.py). Projects, worktrees, and the report store are outside this job. Confirm that this matches your recovery choice.
3. Save the restic password and R2 credentials in a password manager outside the HP. Use a private Standard-class R2 bucket with public access disabled and bucket-scoped Object Read & Write credentials. Keep an existing bucket and credentials if they already meet this contract.

## Prepare private credentials on a new host

Skip this section when both credential files already exist. Inspect their ownership and permissions instead. This bootstrap does not install or run the Pi collector.

1. If `lab-backup` does not exist, create it:

```bash
	sudo useradd --system --user-group --create-home --home-dir /home/lab-backup --shell /usr/bin/nologin lab-backup
```

2. Create the protected directories:

```bash
	sudo install -d -m 700 -o lab-backup -g lab-backup /home/lab-backup /home/lab-backup/credentials
```

3. Use `sudoedit` to create `/home/lab-backup/credentials/r2.json` with the [documented schema](../reference/automation.md#credential-files). Fill its values from your password manager. Do not put populated JSON in Git or a command argument.
4. For a new repository, generate a strong password in your password manager. For an existing cloud repository, retrieve its original password. Use `sudoedit` to create `/home/lab-backup/credentials/restic-password` containing that password on one line.
5. Set permissions without printing either file:

```bash
	sudo chown lab-backup:lab-backup /home/lab-backup/credentials/r2.json /home/lab-backup/credentials/restic-password
	sudo chmod 600 /home/lab-backup/credentials/r2.json /home/lab-backup/credentials/restic-password
	sudo stat -c '%U %G %a %n' /home/lab-backup/credentials/r2.json /home/lab-backup/credentials/restic-password
```

Expect `lab-backup lab-backup 600` for both files. Stop if a credential is missing, incorrect, or accessible to the coding account.

## Install and verify the first backup

1. Review the source, then run the installer from the maintenance terminal:

```bash
	sudo bash /home/coder/projects/proj_home-lab/devices/home-lab/backup-tools/install-agents.sh
```

The installer takes a temporary filesystem snapshot, creates local and R2 copies, restores both, checks files and SQLite databases, and checks saved transcript metadata. It enables timers only after success. Agents and Pi containers stay running.

2. Expect `Agent-state local backup, R2 copy and restore checks passed`. Confirm the service result and timers:

```bash
	systemctl show lab-agent-backup.service lab-agent-backup-health.service -p Id -p Result -p ExecMainStatus
	systemctl list-timers 'lab-agent-backup*' --all
```

Both results must be `success` with exit status `0`. Expect the next daily run at 04:00 Europe/Zurich and an hourly freshness check.

3. [Reopen a restored conversation](restore-agent-conversation.md). Confirm the next scheduled run separately; timer enablement is not evidence of scheduled execution.

## Run, pause, or diagnose

Run an additional backup with `sudo systemctl start lab-agent-backup.service`. This also tests both restores and applies retention. Pause future daily runs with `sudo systemctl disable --now lab-agent-backup.timer`; existing backups remain intact and the hourly check eventually reports stale success.

If a run fails, inspect the job before rerunning it:

```bash
	sudo journalctl -u lab-agent-backup.service --since today --no-pager -n 60
	sudo cat /var/lib/lab-agent-backup/last-success.json
```

A remaining `/var/lib/lab-agent-backup/home` is a temporary snapshot. Ensure the backup service is inactive, inspect the subvolume identity and read-only property, and remove only the job's confirmed snapshot. Never delete `/home` or a project directory to clear this condition. Restore the reviewed script if an update caused the failure.

Alerts currently reach the local journal and logged-in terminals. Outside email delivery remains deferred. Keep unfinished checks in [preparation](../preparation.md).
