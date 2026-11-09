---
type: Decision
title: "Keep existing Pi hosting during HP setup"
description: "A proposed rollout boundary between running services and new development."
status: draft
sources:
  - id: architecture-decision
    resource: "../../devices/home-lab/preparation.md"
  - id: source-3
    resource: "../../devices/_reference/services.md"
---

# Keep existing Pi hosting during HP setup

Keep existing Coolify workloads on the Raspberry Pi while establishing private development on the HP. This avoids moving running applications while the new machine and its recovery paths are untested. Live inspection confirmed running Pi hosting on 9 November 2026. The [Coolify concept](../technologies/coolify.md "now has tested backup support described by") records incoming HP backups and partial restore checks installed later that day; these do not select a hosting migration or prove end-to-end cutover recovery.

A migration is conditional on capacity or reliability needs and a separate backup, restore, and network test plan. The HP's arrival is not itself a migration decision.

This keeps [Coolify](../technologies/coolify.md "retains on the existing Pi") and its [Cloudflare tunnel](../technologies/cloudflare-tunnel.md "leaves separate from HP administration") distinct from the [private HP architecture](home-lab/private-development.md "supports"). The [Pi-hole](../technologies/pi-hole.md "requires separate dependency review for") DNS role also needs inspection before network changes.
