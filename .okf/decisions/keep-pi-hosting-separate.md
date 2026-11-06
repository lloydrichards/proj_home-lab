---
type: Decision
title: "Keep existing Pi hosting during HP setup"
description: "A proposed rollout boundary between running services and new development."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/00-design.md"
  - id: source-2
    resource: "../../docs/hp/07-optional-services.md"
  - id: source-3
    resource: "../../docs/reference/services.md"
---

# Keep existing Pi hosting during HP setup

The HP design keeps existing Coolify workloads on the Raspberry Pi while private development is established. The user reports the Pi hosting is running; workloads and backup arrangements remain uninspected.

A migration is conditional on capacity or reliability needs and a separate backup, restore, and network test plan. The HP's arrival is not itself a migration decision.

This keeps [Coolify](../technologies/coolify.md "retains on the existing Pi") and its [Cloudflare tunnel](../technologies/cloudflare-tunnel.md "leaves separate from HP administration") distinct from the [private HP architecture](private-development.md "supports"). The [Pi-hole](../technologies/pi-hole.md "requires separate dependency review for") DNS role also needs inspection before network changes.
