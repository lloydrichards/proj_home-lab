---
type: Concept
title: "Restic"
description: "Encrypted Pi backup history on the HP and proposed HP workspace protection."
status: draft
sources:
  - id: source-1
    resource: "../../research/backups.md"
  - id: source-2
    resource: "../../devices/home-lab/preparation.md"
  - id: incoming-pi-backups
    resource: "../../devices/remote-lab/backups.md"
---

# Restic

For HP workspaces, the backup research still proposes an encrypted restic repository on another device or storage service. Its destination, schedule, retention and notifications remain undecided; no HP workspace restore is recorded.

For incoming Pi data, Lloyd authorized and installed encrypted history on home-lab on 9 November 2026. A dedicated account pulls consistent [Coolify and application backups](coolify.md "protects data managed through") over Tailscale. The source has no repository credential, so it cannot delete retained HP history. `coder` cannot read the repository credentials. Daily retention is 14 daily, 8 weekly and 6 monthly snapshots; full data reads occur initially and each Sunday. The first actual repository restore, byte checksums and SQLite main-file integrity checks passed. PostgreSQL restores, nine complete SQLite/WAL restores and Coolify credential decryption passed in separate isolated tests against the matching source generation. These tests have narrower scope than a restored app UI or dashboard.

The restic password and Coolify key still need confirmed independent password-manager storage. Local journal/terminal alerts do not notify Lloyd if the HP itself is down. An independent off-site or disconnected copy and outside notification destination remain open in the HP preparation checklist.

The proposed HP backup scope includes uncommitted repositories, agent conversations, configuration, and recovery material. A Git push does not preserve all of that state. Keep the backup password available outside the HP.

The first drill restores selected data into a separate private directory and checks useful files. Repository checks and a restore drill answer different questions; a default repository check does not read every stored data block.

A mounted destination check is needed if an external drive is later selected, to prevent a missing drive redirecting writes onto the HP filesystem. The incoming Pi repository currently uses the internal HP filesystem. Automation through [systemd](systemd.md "is scheduled by") followed the manual drill. This supports the [recovery-first decision](../decisions/recovery-before-reliance.md "implements") and [snapshot learning](../learnings/snapshots-are-not-backups.md "addresses").
