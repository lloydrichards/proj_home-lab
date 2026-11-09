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

Live inspection on 9 November 2026 confirmed a Docker cloudflared connector routing to `http://coolify-proxy:80` on the Pi 5. The connector must share the proxy's `coolify` network. A missing attachment caused public 502 responses despite running apps; reattachment restored routing and survived a container restart. Full host reboot recovery remains untested. Preserve the network declaration when replacing the container. Authentication policy remains unverified. A separate native connector is active, with purpose unresolved.

Historical guides describe two uses: SSH through Cloudflare Access and public application routing to the [Coolify](coolify.md "routes historical application traffic to") proxy. The Docker app route is confirmed; the native connector has not been mapped to the historical SSH route. Tokens remain outside Git.

A connector route and a hostname do not establish who may use the application. The [private-network learning](../learnings/private-network-is-not-isolation.md "requires separate authentication reasoning from") distinguishes reachability from authentication and process permissions.

The [HP private-development decision](../decisions/home-lab/private-development.md "is separate from") instead proposes Tailscale and OpenSSH. Do not copy the historical public routing recipe into HP agent administration.
