# Backup research for the HP

Distilled from the earlier proposed operations guide on 6 November 2026. No HP workspace backup or restore has run; its destination, retention, scheduling, and failure notification remain undecided. Incoming [remote-lab backups](../devices/remote-lab/backups.md) were separately installed and restore-checked on 9 November; they do not protect the HP's own workspaces.

## What needs protecting

Repositories include uncommitted work, Git metadata, and worktree dependencies. Agent conversations and tool configuration also need recovery. A Git push does not capture all of these. Keep recovery credentials available outside the HP.

Omarchy root snapshots leave `/home` unchanged. They help with OS recovery but do not replace workspace backups or protect against loss of the SSD. [Omarchy snapshots](https://omarchy.org/manual/system-snapshots/)

## Proposed first experiment

Use an encrypted restic repository on another device or storage service. Confirm that an external destination is actually mounted before writing, so a missing drive cannot redirect the backup onto the HP filesystem. An attached USB drive is a possible first copy; important work also needs an independent offline or off-site copy.

Stop agents for the first consistent session backup. Databases need application-consistent dumps or a documented quiesce procedure. Investigate incomplete backups rather than treating a created snapshot as sufficient. [Restic backups](https://restic.readthedocs.io/en/stable/040_backup.html)

Restore a selected uncommitted file and agent session into a separate private directory, outside the backed-up tree. Check their contents. A normal repository check does not read every stored data block; full data verification is a separate check. [Repository checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html), [restore behavior](https://restic.readthedocs.io/en/stable/050_restore.html)

Choose automation after that experiment works. Check mount availability and last successful backup, report failures, and review retention before deleting snapshots. Avoid giving the coding account the only credentials capable of deleting every copy.

The [restic concept](../.okf/technologies/restic.md) records lab relevance. The [recovery choice](../.okf/decisions/recovery-before-reliance.md) explains why we test restoration before depending on the machine. Write the actual recipe when we choose a destination and perform the experiment.
