---
type: Concept
title: "Restic"
description: "Encrypted backup history, consistency boundaries, and tested data recovery."
status: draft
sources:
  - id: design
    resource: "../../devices/home-lab/explanations/backup-and-recovery.md"
  - id: hp-automation
    resource: "../../devices/home-lab/reference/automation.md"
  - id: pi-automation
    resource: "../../devices/remote-lab/reference/backups.md"
  - id: evidence
    resource: "../../devices/_reference/services.md"
  - id: research
    resource: "../../research/backups.md"
---

# Restic

Encrypted repositories preserve data independently of a running service. A successful snapshot, repository check, restored file, and reopened application establish different recovery properties. The [recovery decision](../decisions/recovery-before-reliance.md "requires") prefers tested restoration before reliance.

The lab uses separate local and R2 repositories for Pi application data and HP agent state. Local copies avoid a cloud download; R2 adds geographic separation. Both remain accessible to HP root, and R2 write credentials permit deletion. This is not immutable storage or protection from every administrator compromise. R2 also shares the Cloudflare account used for application hosting.

Source consistency comes before encryption. The Pi job stops writes and archives cold data. The HP job reads selected agent paths from a temporary Btrfs snapshot, preserving SQLite journals with their databases. The snapshot freezes a filesystem view, not a completed multi-file application transaction. Nested storage needs explicit handling.

Lloyd's [agent-state scope decision](../decisions/home-lab/agent-state-backups.md "limits") excludes projects and worktrees. GitHub does not preserve uncommitted edits or unpushed commits. Shared-skill links require their omitted source repositories to be recovered separately.

Initial local and cloud recovery checks passed. One R2-restored Codex conversation reopened in an isolated profile; its copied index needed transcript-path rebasing. This does not establish recovery of every agent interface, production Pi browser behavior, or a whole replacement machine. The [service register](../../devices/_reference/services.md) owns dates and results; the [backup explanation](../../devices/home-lab/explanations/backup-and-recovery.md) and its linked task guides own operation.

[Systemd](systemd.md "schedules") runs the jobs. Local alerts cannot report an offline HP. Outside email alerts are deferred, and remaining verification belongs in [preparation](../../devices/home-lab/preparation.md).
