---
type: Concept
title: "Restic"
description: "Proposed encrypted off-machine backup and restore tooling."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/04-operations.md"
  - id: source-2
    resource: "../../docs/hp/05-acceptance.md"
---

# Restic

The HP operations guide proposes an encrypted restic repository on another device or storage service. Destination, schedule, retention, and notifications remain undecided. No successful backup or restore is recorded.

The backup scope includes uncommitted repositories, agent conversations, configuration, and recovery material. A Git push does not preserve all of that state. Keep the backup password available outside the HP.

The first drill restores selected data into a separate private directory and checks useful files. Repository checks and a restore drill answer different questions; a default repository check does not read every stored data block.

A mounted destination check prevents a missing external drive from silently redirecting writes onto the HP filesystem. Automation through [systemd](systemd.md "may later use") follows the manual drill. This supports the [recovery-first decision](../decisions/recovery-before-reliance.md "implements") and [snapshot learning](../learnings/snapshots-are-not-backups.md "addresses").
