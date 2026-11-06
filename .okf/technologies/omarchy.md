---
type: Concept
title: "Omarchy"
description: "The selected operating system for the arriving HP."
status: draft
sources:
  - id: source-1
    resource: "../../docs/research/omarchy-headless.md"
  - id: source-2
    resource: "../../docs/hp/01-install.md"
  - id: source-3
    resource: "../../docs/hp/04-operations.md"
---

# Omarchy

The HP plan selects bare-metal Omarchy with a local desktop for installation and recovery. Normal remote coding uses [OpenSSH](openssh.md "supports headless access through") rather than a remote desktop. This is an installation plan, not a running host description.

The research separates desktop idle controls from system-wide power policy and firmware AC-loss recovery. An always-on host needs cold-boot, idle, and reconnect tests; see the [unattended-boot decision](../decisions/unattended-boot.md "must support").

The guide uses Omarchy's supported update path and maintenance windows with recovery access. Its researched root snapshots exclude home data, which motivates [separate backups](restic.md "needs for home data") and the [snapshot learning](../learnings/snapshots-are-not-backups.md "illustrates").

Installer and release-sensitive commands remain in the source guides. Check them against the actual installed release.
