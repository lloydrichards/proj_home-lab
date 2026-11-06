---
type: Learning
title: "Root snapshots do not protect workspace data"
description: "The proposed host needs separate backup coverage for home data and disk loss."
status: draft
sources:
  - id: source-1
    resource: "../../docs/research/omarchy-headless.md"
  - id: source-2
    resource: "../../docs/research/backups.md"
---

# Root snapshots do not protect workspace data

The Omarchy research describes root snapshots that leave `/home` unchanged. Restoring root can recover an OS change while repositories, user configuration, and agent sessions remain in their newer state.

An on-host snapshot also does not provide an independent copy after the SSD fails or is stolen. The backup research therefore proposes encrypted off-machine [restic](../technologies/restic.md "requires separate copies through") backups and a restore drill.

A successful Git push protects committed remote history. It does not capture every uncommitted file or local conversation. This distinction supports [recovery before reliance](../decisions/recovery-before-reliance.md "motivates").
