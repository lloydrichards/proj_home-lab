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
---

# systemd

The HP research uses systemd for SSH and networking services and now has a sleep-policy drop-in disabling suspend, hibernation, hybrid sleep and suspend-then-hibernate, confirmed by user-supplied privileged output on 9 November 2026. Overnight behavior remains to test. It distinguishes power sleep from desktop locking and firmware restart behavior.

A reviewed user service can use lingering to run without an interactive login. Lingering does not restart arbitrary shell processes. [Tmux](tmux.md "differs from supervision by") solves client disconnection, not service restart after boot.

A backup timer is deferred until a manual [restic restore](restic.md "can schedule after validation") succeeds. The planned job checks its destination mount and reports failures and stale last-success time. Enabling a timer does not establish that the backup works.

Persistent agent services are optional and need actual executable paths, authentication, and secret storage reviewed before deployment.
