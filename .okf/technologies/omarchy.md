---
type: Concept
title: "Omarchy"
description: "The selected operating system for the installed HP."
status: draft
sources:
  - id: hp-setup
    resource: "../../devices/home-lab/setup.md"
  - id: source-1
    resource: "../../devices/home-lab/research/omarchy.md"
  - id: source-3
    resource: "../../research/backups.md"
  - id: remote-desktop
    resource: "../../devices/home-lab/research/omarchy-remote-desktop.md"
---

# Omarchy

The HP plan selects bare-metal Omarchy with a local desktop for installation and recovery. Normal remote coding starts with [OpenSSH](openssh.md "supports headless access through"). A remote desktop can complement that access. Omarchy 4.5.0 is installed on the HP; the inventory owns observed configuration and test results.

Research on 7 November 2026 recommends trying Sunshine on the HP with Moonlight on the Mac for the full desktop, while retaining SSH for coding and recovery. Native `hypr-rdp` is a desktop-focused alternative that needs version and authentication checks. WayVNC is another option for occasional graphical access. These are proposals, not a selected or tested deployment. Gliff is an upstream alternative for Hyprland clients, but its current requirement for Hyprland at both ends does not fit the Mac client.

Headless desktop access still needs a running graphical session, an available display output, and working capture and input permissions. A virtual output can replace the physical monitor, but hardware encoding and reconnection after reboot need host tests. Unencrypted boot does not by itself establish desktop availability. Keep a monitor and keyboard available for firmware, boot-menu, and network recovery. The remote-desktop source compares options and defines the proposed checks; the preparation checklist remains the single task list.

The research separates desktop idle controls from system-wide power policy and firmware AC-loss recovery. An always-on host needs cold-boot, idle, and reconnect tests; see the [unattended-boot decision](../decisions/home-lab/unattended-boot.md "must support").

The research recommends Omarchy's supported update path and maintenance windows with recovery access. Its researched root snapshots exclude home data, which motivates [separate backups](restic.md "needs for home data") and the [snapshot learning](../learnings/snapshots-are-not-backups.md "illustrates").

The post-install guide cited in source `hp-setup` checks installed defaults before changing services and keeps the desktop for initial recovery. Commands in that guide and the research need checking against the installed release. TPM disk unlock and SSH are configured; monitor-free cold startup passed; idle and power-loss recovery checks remain pending. Progress remains in the preparation checklist.
