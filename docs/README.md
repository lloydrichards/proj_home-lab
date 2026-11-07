# Find a useful note

Start with the relevant device. Names below are the planned hostnames, not verified access addresses.

| Device | Purpose | Start here |
|---|---|---|
| [home-lab](devices/home-lab/README.md) | HP development and AI coding | [Preparation checklist](devices/home-lab/preparation.md), then [post-install setup](devices/home-lab/setup.md) |
| [remote-lab](devices/remote-lab/README.md) | Pi 5 hosting with Coolify and Cloudflare Tunnel | Device status and historical Pi recipes |
| [admin-lab](devices/admin-lab/README.md) | Pi 4 with Pi-hole | Known gaps and DNS dependency checks |

Each device page links its guides, research, and relevant decisions. Historical recipes and researched plans are identified as such; neither proves installed behavior.

## Shared lab records

- [Inventory](reference/inventory.md) owns hardware facts, planned names, and verification gaps.
- [BOM](reference/bom.md) owns purchases, costs, and shared rack parts.
- [Service register](reference/services.md) owns service placement, access, and dependencies.
- [Shared research](research/README.md) covers topics that span devices or the Mac client.
- [OKF notebook](../.okf/index.md) owns concepts, decisions, alternatives, and reusable learnings.

Keep device procedures in `docs/devices/<device>/`. Put device-specific research in that device's `research/` directory when needed. Decisions live once in `.okf/decisions/<device>/` and are linked from the device page; decisions spanning the lab stay directly under `.okf/decisions/`. Shared technologies and learnings stay in their existing OKF directories.

Add a new device with a directory and a short `README.md`. Create more files or subdirectories only when there is useful material to put in them. Keep one source for each fact and link related records. See [agent instructions](../AGENTS.md) or return to the [home page](../README.md).
