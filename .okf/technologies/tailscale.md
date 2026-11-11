---
type: Concept
title: "Tailscale"
description: "Device connectivity, private HTTPS, and authorization boundaries."
status: draft
sources:
  - id: current-policy
    resource: "../../devices/_reference/tailscale-policy.json"
  - id: current-evidence
    resource: "../../devices/_reference/services.md"
  - id: private-access
    resource: "../../devices/home-lab/how-to/secure-remote-access.md"
  - id: publishing
    resource: "../../devices/home-lab/publishing.md"
  - id: research
    resource: "../../research/private-access.md"
---

# Tailscale

Tailscale supplies device connectivity and tailnet authorization. Ordinary [OpenSSH](openssh.md "authenticates Linux accounts over") separately checks the key and Linux account. Tailscale SSH is a distinct authentication mode; it is disabled in the current lab arrangement.

A narrow grant does not override an existing broad allow. The lab replaced its unrestricted grant with selected management, backup, DNS, and client paths. Test both intended access and denial. Device policy does not distinguish lloyd from coder on the same host, restrict LAN paths, or replace application roles. The service register owns the sampled checks and remaining limits.

Machine names, MagicDNS responses, and Mac SSH aliases are separate. Matching labels do not prove DNS or authorization. Explicit private addresses in aliases avoided Mac short-name failures without changing Pi-hole configuration. A running server daemon does not establish client connectivity or successful enrollment.

Serve provides private HTTPS for reports and previews. Funnel would expose them publicly and is excluded by the [private-development decision](../decisions/home-lab/private-development.md "governs"). The fixed route helper preserves that distinction and refuses unrelated route changes.

Key expiry, client state, and host reboot can interrupt access. Maintenance needs independent recovery access and fresh-login tests rather than a reset through the only working session. Release-sensitive update findings belong in dated research and the single preparation checklist, not a permanent claim about the latest release.

The [private-network learning](../learnings/private-network-is-not-isolation.md "limits") explains why reachability controls do not sandbox agent tools. [Architecture](../../devices/home-lab/explanations/architecture.md) shows the reader-facing topology.
