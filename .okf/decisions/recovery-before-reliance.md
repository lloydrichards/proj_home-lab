---
type: Decision
title: "Test recovery before relying on the HP"
description: "A proposed acceptance rule for backups, access, and later services."
status: draft
sources:
  - id: architecture-decision
    resource: "../../docs/decisions/0001-private-development-host.md"
  - id: source-1
    resource: "../../docs/hp/05-acceptance.md"
  - id: source-2
    resource: "../../docs/hp/04-operations.md"
  - id: source-3
    resource: "../../docs/hp/07-optional-services.md"
---

# Test recovery before relying on the HP

ADR 0001 owns the proposed rollout and recovery requirements. The guides turn those requirements into procedures and acceptance checks. All acceptance checks remain not run. A guide or enabled service is not evidence of a successful recovery.

The initial evidence should include a fresh second SSH login, controlled cold boot, restored uncommitted files and agent state, and reachable local recovery tools. [Restic](../technologies/restic.md "uses for backup and restore") covers data recovery; it does not replace console access or boot recovery.

Add optional services one at a time after the base checks. Back up, restore, and test network behavior before migrating existing workloads. Automate backups after the manual drill.

This connects [safe access changes](../learnings/access-changes-need-recovery.md "requires"), [backup scope](../learnings/snapshots-are-not-backups.md "depends on"), and [unattended boot](unattended-boot.md "must verify").
