---
type: Concept
title: "Omarchy"
description: "The selected operating system for the arriving HP."
status: draft
sources:
  - id: hp-setup
    resource: "../../docs/devices/home-lab/setup.md"
  - id: source-1
    resource: "../../docs/devices/home-lab/research/omarchy.md"
  - id: source-3
    resource: "../../docs/research/backups.md"
---

# Omarchy

The HP plan selects bare-metal Omarchy with a local desktop for installation and recovery. Normal remote coding uses [OpenSSH](openssh.md "supports headless access through") rather than a remote desktop. This is an installation plan, not a running host description.

The research separates desktop idle controls from system-wide power policy and firmware AC-loss recovery. An always-on host needs cold-boot, idle, and reconnect tests; see the [unattended-boot decision](../decisions/home-lab/unattended-boot.md "must support").

The research recommends Omarchy's supported update path and maintenance windows with recovery access. Its researched root snapshots exclude home data, which motivates [separate backups](restic.md "needs for home data") and the [snapshot learning](../learnings/snapshots-are-not-backups.md "illustrates").

The post-install guide cited in source `hp-setup` checks installed defaults before changing services and keeps the desktop for initial recovery. Commands in that guide and the research need checking against the installed release. No HP configuration has been performed. Progress remains in the preparation checklist.
