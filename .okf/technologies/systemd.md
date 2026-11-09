---
type: Concept
title: "systemd"
description: "Service supervision, power policy, and proposed scheduled operations."
status: draft
sources:
  - id: source-1
    resource: "../../devices/home-lab/research/omarchy.md"
  - id: source-2
    resource: "../../research/backups.md"
  - id: incoming-backup-automation
    resource: "../../devices/remote-lab/backups.md"
---

# systemd

The HP research uses systemd for SSH and networking services and now has a sleep-policy drop-in disabling suspend, hibernation, hybrid sleep and suspend-then-hibernate, confirmed by user-supplied privileged output on 9 November 2026. Overnight behavior remains to test. It distinguishes power sleep from desktop locking and firmware restart behavior.

A reviewed user service can use lingering to run without an interactive login. Lingering does not restart arbitrary shell processes. [Tmux](tmux.md "differs from supervision by") solves client disconnection, not service restart after boot.

Incoming Pi backups now use a system timer at 02:00 Europe/Zurich, with missed runs caught up after HP downtime. It was enabled on 9 November 2026 after a manual [restic restore](restic.md "schedules after validation") and integrity checks passed. An hourly check reports stale success and storage limits. Alerts use the local journal and logged-in terminals only. Root-owned remote services restart stopped containers after an exporter failure or interrupted reboot; the reboot recovery path is installed but has not been exercised by a power-interruption test. HP workspace backup scheduling remains deferred. Enabling a timer alone does not establish that a backup works.

Persistent agent services are optional and need actual executable paths, authentication, and secret storage reviewed before deployment.
