---
type: Decision
title: "Test recovery before relying on the HP"
description: "Recovery checks required before relying on access, backups, and unattended services."
status: draft
sources:
  - id: architecture-decision
    resource: "../../devices/home-lab/preparation.md"
  - id: source-2
    resource: "../../research/backups.md"
---

# Test recovery before relying on the HP

Test recovery before depending on the HP. A working login or successful backup does not establish that we can recover after a reboot, lockout, or lost SSD. The preparation checklist separates completed checks from outstanding ones. A written recipe or enabled service is not evidence of a successful recovery. Initial Pi data drills and one restored Codex conversation have passed; complete machine recovery remains untested.

The initial evidence should include a fresh second SSH login, controlled cold boot, restored data within the accepted backup scope, and reachable local recovery tools. [Restic](../technologies/restic.md "uses for backup and restore") covers data recovery; it does not replace console access or boot recovery.

Add optional services one at a time after the basic workflow and recovery checks. Back up, restore, and test network behavior before migrating existing workloads. Automate backups after the manual drill.

This connects [safe access changes](../learnings/access-changes-need-recovery.md "requires"), [backup scope](../learnings/snapshots-are-not-backups.md "depends on"), and [unattended boot](home-lab/unattended-boot.md "must verify").

The [agent-state scope decision](home-lab/agent-state-backups.md "limits") explicitly excludes project checkouts and worktrees. Requiring recovery checks does not silently override that choice.
