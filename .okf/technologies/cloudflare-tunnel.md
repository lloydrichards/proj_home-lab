---
type: Concept
title: "Cloudflare Tunnel"
description: "Public application transport with separate authorization and proxy routing."
status: draft
sources:
  - id: operating-guide
    resource: "../../devices/remote-lab/coolify-cloudflare.md"
  - id: access-record
    resource: "../../devices/_reference/services.md"
  - id: security
    resource: "../../docs/explanations/security-and-access.md"
  - id: retired-ssh-recipe
    resource: "../../devices/remote-lab/cloudflare-ssh.md"
---

# Cloudflare Tunnel

A connector carries public application traffic to the Pi's [Coolify](coolify.md "routes through") proxy. DNS, connector routing, proxy host rules, and application authorization are distinct controls. A wildcard route does not establish that every service is reachable or protected.

The Docker connector must share the proxy network to resolve its hostname. Losing that attachment caused public failures while local application routes worked. Reattachment restored traffic and survived a container restart; replacement must retain the network declaration. Full host reboot recovery remains untested.

Cloudflare Access protects human Coolify login. GitHub's exact event path has a separate browser-gate bypass, so webhook signature validation remains necessary. A successful ping proves handler reachability, not a verified signature or deployment. The service register owns the applied route, gate, and test results.

The old public SSH route and DNS record were removed after private Mac access worked. A native connector process remains with unresolved purpose; removing a route does not prove every connector or credential was removed. The [private-development decision](../decisions/home-lab/private-development.md "separates administration through") uses Tailscale and OpenSSH rather than public HP agent administration.

Public HTTPS can terminate before an HTTP tunnel origin. Redirect settings therefore need to match the full path: the observed dashboard self-redirect was repaired without patching generated Caddy files or globally changing unrelated applications. The operating guide owns diagnosis and recovery.

Private transport, an Access gate, and [process isolation](../learnings/private-network-is-not-isolation.md "does not replace") answer different questions. R2 storage shares this Cloudflare account, adding an account-level dependency beyond the application tunnel.
