---
type: Concept
title: "Coolify"
description: "Deployment management reported on the existing Raspberry Pi."
status: draft
sources:
  - id: source-1
    resource: "../../remote-lab/coolify.md"
  - id: source-2
    resource: "../../remote-lab/coolify-cloudflare.md"
  - id: source-3
    resource: "../../reference/services.md"
---

# Coolify

The user reports Coolify running on a Raspberry Pi alongside a [Cloudflare tunnel](cloudflare-tunnel.md "accessed through"). Version, workloads, data locations, backups, and administration access await live inspection. SSH inspection is deferred while Wi-Fi is unavailable.

The historical installation guide configures localhost as the deployment server. The tunnel guide attaches cloudflared to the Coolify container network and routes traffic to its proxy. These are historical instructions, not a verified topology.

[Docker](docker.md "uses in the historical deployment recipe") permissions and port publication affect this design. A tunnel alone does not establish an authorization policy for the dashboard.

The HP plan [keeps Pi hosting separate](../decisions/keep-pi-hosting-separate.md "is retained by") until there is a reason to migrate and a tested restore plan.
