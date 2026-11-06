---
type: Decision
title: "Test recovery before relying on the HP"
description: "A proposed acceptance rule for backups, access, and later services."
status: draft
sources:
  - id: architecture-decision
    resource: "../../docs/hp-preparation.md"
  - id: source-2
    resource: "../../docs/research/backups.md"
---

# Test recovery before relying on the HP

Test recovery before depending on the HP. A working login or successful backup does not establish that we can recover after a reboot, lockout, or lost SSD. The preparation checklist remains unchecked. A written recipe or enabled service is not evidence of a successful recovery.

The initial evidence should include a fresh second SSH login, controlled cold boot, restored uncommitted files and agent state, and reachable local recovery tools. [Restic](../technologies/restic.md "uses for backup and restore") covers data recovery; it does not replace console access or boot recovery.

Add optional services one at a time after the basic workflow and recovery checks. Back up, restore, and test network behavior before migrating existing workloads. Automate backups after the manual drill.

This connects [safe access changes](../learnings/access-changes-need-recovery.md "requires"), [backup scope](../learnings/snapshots-are-not-backups.md "depends on"), and [unattended boot](unattended-boot.md "must verify").
