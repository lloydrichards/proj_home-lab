---
type: Concept
title: "Coolify"
description: "Deployment management reported on the existing Raspberry Pi."
status: draft
sources:
  - id: source-1
    resource: "../../devices/remote-lab/coolify.md"
  - id: source-2
    resource: "../../devices/remote-lab/coolify-cloudflare.md"
  - id: source-3
    resource: "../../devices/_reference/services.md"
---

# Coolify

SSH inspection on 9 November 2026 confirmed Coolify 4.4.7 on the Pi 5 alongside a [Cloudflare tunnel](cloudflare-tunnel.md "accessed through"). The dashboard and app containers were running. Repairing the tunnel network restored six tested public routes. The service register owns access details and remaining gaps, including backups.

The historical installation guide configures localhost as the deployment server. The tunnel guide attaches cloudflared to the Coolify container network and routes traffic to its proxy. Live inspection confirmed this tunnel-to-proxy topology on 9 November 2026.

[Docker](docker.md "uses in the historical deployment recipe") permissions and port publication affect this design. A tunnel alone does not establish an authorization policy for the dashboard.

The HP plan [keeps Pi hosting separate](../decisions/keep-pi-hosting-separate.md "is retained by") until there is a reason to migrate and a tested restore plan.
