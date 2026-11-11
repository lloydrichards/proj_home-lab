# Backup research for the HP

Research started on 6 November 2026; the cloud and agent-state sources below were checked on 11 November. The [service register](../devices/_reference/services.md) owns deployment and restore results. The [backup explanation](../docs/explanations/backup-and-recovery.md) explains their limits; [agent backup operations](../devices/home-lab/agent-backups.md) owns procedures.

## What needs protecting

Repositories include uncommitted work, Git metadata, and worktree dependencies. Agent conversations and tool configuration also need recovery. A Git push does not capture all of these. Keep recovery credentials available outside the HP.

Omarchy root snapshots leave `/home` unchanged. They help with OS recovery but do not replace workspace backups or protect against loss of the SSD. [Omarchy snapshots](https://omarchy.org/manual/system-snapshots/)

## Restore evidence and repository checks

A normal repository check does not read every stored data block. Full data verification is a separate check. Retain this distinction when evaluating successful backup jobs. [Repository checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html), [restore behavior](https://restic.readthedocs.io/en/stable/050_restore.html)

## Cloud storage choice

On 11 November 2026, Lloyd chose cloud storage and preferred Cloudflare R2 because he already uses Cloudflare. R2 offers an S3-compatible API that restic can use directly. Use a private Standard-class bucket, keep credentials within the backup account and scope them to that bucket. Retain the existing local repository. A separate off-site repository should receive restic snapshot copies rather than an unsynchronized file copy of a live repository. This adds geographic separation but retains Cloudflare account dependency; it does not establish deletion-resistant storage.

Sources checked on 11 November 2026: [R2 S3 access](https://developers.cloudflare.com/r2/get-started/s3/), [R2 pricing](https://developers.cloudflare.com/r2/pricing/), and [restic repository backends](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html). Standard pricing and free allowances must be rechecked before estimating an actual retained repository.

## Outside backup notifications

On 11 November 2026, Lloyd selected email notifications, then deferred their setup. Hosted Healthchecks.io is proposed, not yet selected or configured: separate daily completion checks for local collection and the R2 copy would detect missed runs even when home-lab cannot send a failure message. A one-day period and two-hour grace period allow for the nightly maintenance window. Only completion/failure signals should leave the host; do not send backup logs, credentials or archived data. Keep ping URLs private because they authorize status updates. Confirm email delivery with a deliberate alert test before relying on notifications. [Healthchecks cron monitoring](https://healthchecks.io/docs/monitoring_cron_jobs/) and [configuration](https://healthchecks.io/docs/configuring_checks/) were checked on 11 November 2026.

## Home-lab project and session scope

The [agent-state scope decision](../.okf/decisions/home-lab/agent-state-backups.md) owns the choice to exclude projects and worktrees. A separate repository prefix keeps agent and Pi retention independent. Agent state can contain credentials, so encryption and restricted access matter even when projects are excluded.

The installed job uses a short-lived read-only Btrfs home snapshot for consistent input without stopping agents. Nested subvolumes and mounts need separate consideration: Btrfs snapshots are not recursive. Preserve database files together with WAL and rollback journals from that frozen view. This captures a filesystem point in time, not a completed multi-file application transaction. Test restored SQLite databases by opening writable disposable copies with their journals, and check a saved agent transcript before scheduling.

References checked on 11 November 2026: [Btrfs subvolume behavior](https://btrfs.readthedocs.io/en/latest/Subvolumes.html), [SQLite backup consistency hazards](https://www.sqlite.org/howtocorrupt.html), and [Codex storage configuration](https://learn.chatgpt.com/docs/config-file/config-advanced).
