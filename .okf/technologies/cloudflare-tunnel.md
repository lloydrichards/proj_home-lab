---
type: Concept
title: "Cloudflare Tunnel"
description: "Reported access to the existing Pi, distinct from planned private HP access."
status: draft
sources:
  - id: source-1
    resource: "../../devices/remote-lab/cloudflare-ssh.md"
  - id: source-2
    resource: "../../devices/remote-lab/coolify-cloudflare.md"
  - id: source-3
    resource: "../../research/remote-coding.md"
  - id: source-4
    resource: "../../devices/_reference/services.md"
---

# Cloudflare Tunnel

The user reports a Cloudflare tunnel with the Coolify Pi. The running connector, routing, and authentication configuration have not been inspected.

Historical guides describe two uses: SSH through Cloudflare Access and public application routing to the [Coolify](coolify.md "routes historical application traffic to") proxy. Their existence does not establish that both routes are active now. Tokens remain outside Git.

A connector route and a hostname do not establish who may use the application. The [private-network learning](../learnings/private-network-is-not-isolation.md "requires separate authentication reasoning from") distinguishes reachability from authentication and process permissions.

The [HP private-development decision](../decisions/home-lab/private-development.md "is separate from") instead proposes Tailscale and OpenSSH. Do not copy the historical public routing recipe into HP agent administration.
