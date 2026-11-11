# Backup research for the HP

Distilled from the earlier proposed operations guide on 6 November 2026. The HP agent-state local and R2 backups and initial restore checks passed on 11 November 2026, and the nightly 04:00 Zurich schedule is enabled; Lloyd excluded projects and deferred outside email alerts. Incoming [remote-lab backups](../devices/remote-lab/backups.md) were separately installed and restore-checked on 9 November; they do not protect the HP's own workspaces.

## What needs protecting

Repositories include uncommitted work, Git metadata, and worktree dependencies. Agent conversations and tool configuration also need recovery. A Git push does not capture all of these. Keep recovery credentials available outside the HP.

Omarchy root snapshots leave `/home` unchanged. They help with OS recovery but do not replace workspace backups or protect against loss of the SSD. [Omarchy snapshots](https://omarchy.org/manual/system-snapshots/)

## Restore evidence and repository checks

The initial local and cloud restore checks passed. One R2-restored Codex conversation also reopened in an isolated profile. These checks do not establish whole-machine recovery or recovery through every agent interface. The [service register](../devices/_reference/services.md) owns observed results; the [backup explanation](../docs/explanations/backup-and-recovery.md) explains their limits.

A normal repository check does not read every stored data block. Full data verification is a separate check. Retain this distinction when evaluating successful backup jobs. [Repository checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html), [restore behavior](https://restic.readthedocs.io/en/stable/050_restore.html)

## Cloud storage choice

On 11 November 2026, Lloyd chose cloud storage and preferred Cloudflare R2 because he already uses Cloudflare. Initial local and R2 deployment and restore checks passed. R2 offers an S3-compatible API that restic can use directly. Use a private Standard-class bucket, keep credentials within the backup account and scope them to that bucket. Retain the existing local repository. A separate off-site repository should receive restic snapshot copies rather than an unsynchronized file copy of a live repository. This adds geographic separation but retains Cloudflare account dependency; it does not establish deletion-resistant storage.

Sources checked on 11 November 2026: [R2 S3 access](https://developers.cloudflare.com/r2/get-started/s3/), [R2 pricing](https://developers.cloudflare.com/r2/pricing/), and [restic repository backends](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html). Standard pricing and free allowances must be rechecked before estimating an actual retained repository.

## Outside backup notifications

On 11 November 2026, Lloyd selected email notifications, then deferred their setup. Hosted Healthchecks.io is proposed, not yet selected or configured: separate daily completion checks for local collection and the R2 copy would detect missed runs even when home-lab cannot send a failure message. A one-day period and two-hour grace period allow for the nightly maintenance window. Only completion/failure signals should leave the host; do not send backup logs, credentials or archived data. Keep ping URLs private because they authorize status updates. Confirm email delivery with a deliberate alert test before relying on notifications. [Healthchecks cron monitoring](https://healthchecks.io/docs/monitoring_cron_jobs/) and [configuration](https://healthchecks.io/docs/configuring_checks/) were checked on 11 November 2026.

## Home-lab project and session scope

Lloyd authorized this work on 11 November 2026 after the incoming Pi R2 copy passed. Use a separate `home-lab` repository prefix in the existing private R2 bucket so Pi snapshot retention remains separate. Lloyd subsequently excluded projects and worktrees, accepting GitHub as their recovery source. Prepared scope now covers Codex/OpenCode/T3/Rex state, settings and shared-skill links. Use explicit agent paths and exclude embedded worktrees and project checkpoint repositories. This captures credentials as well as work, so keep access restricted and encryption enabled. Maintenance-account files and system-wide configuration are outside this first project/session scope.

The installed job uses a short-lived read-only Btrfs home snapshot for consistent input without stopping agents. Nested subvolumes and mounts need separate consideration: Btrfs snapshots are not recursive. Preserve database files together with WAL and rollback journals from that frozen view. This captures a filesystem point in time, not a completed multi-file application transaction. Test restored SQLite databases by opening writable disposable copies with their journals, and check a saved agent transcript before scheduling. Uncommitted project files are outside the accepted scope. The Codex reopening drill covers one conversation; other agent interfaces remain untested.

References checked on 11 November 2026: [Btrfs subvolume behavior](https://btrfs.readthedocs.io/en/latest/Subvolumes.html), [SQLite backup consistency hazards](https://www.sqlite.org/howtocorrupt.html), and [Codex storage configuration](https://learn.chatgpt.com/docs/config-file/config-advanced). The service register owns measured paths and sizes. The prepared installer performs its filesystem preflight with maintenance privileges; installation and initial local/cloud restore checks passed on 11 November 2026. One Codex conversation subsequently reopened from R2 in an isolated profile, confirmed by Lloyd's screenshot on 11 November. Other agent interfaces and future scheduled execution remain untested. [Agent backup operations](../devices/home-lab/agent-backups.md) owns the scope and procedure.
