---
type: Concept
title: "systemd"
description: "Service supervision, power policy, and proposed scheduled operations."
status: draft
sources:
  - id: source-1
    resource: "../../home-lab/research/omarchy.md"
  - id: source-2
    resource: "../../research/backups.md"
---

# systemd

The HP research uses systemd for SSH and networking services and proposes a sleep-policy drop-in. It distinguishes power sleep from desktop locking and firmware restart behavior.

A reviewed user service can use lingering to run without an interactive login. Lingering does not restart arbitrary shell processes. [Tmux](tmux.md "differs from supervision by") solves client disconnection, not service restart after boot.

A backup timer is deferred until a manual [restic restore](restic.md "can schedule after validation") succeeds. The planned job checks its destination mount and reports failures and stale last-success time. Enabling a timer does not establish that the backup works.

Persistent agent services are optional and need actual executable paths, authentication, and secret storage reviewed before deployment.
