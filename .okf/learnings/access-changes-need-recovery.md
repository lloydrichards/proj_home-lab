---
type: Learning
title: "Keep recovery access during access changes"
description: "A fresh login proves more than an existing connection surviving."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/02-private-access.md"
  - id: source-2
    resource: "../../docs/research/private-access.md"
  - id: source-3
    resource: "../../docs/logs/2026-11-06-documentation-baseline.md"
---

# Keep recovery access during access changes

An established SSH connection can remain usable while new connections are blocked by an authentication, firewall, or policy change. Keeping it open preserves a chance to fix the change; testing a fresh second login establishes that the new route still works.

The [OpenSSH](../technologies/openssh.md "guides changes to") guide checks syntax and effective settings before reload and keeps local-console access available. The [Tailscale](../technologies/tailscale.md "guides changes to") research warns against resetting the only working access route remotely.

The temporary Wi-Fi outage during documentation work deferred SSH inspection. It provides no evidence of the Pis' configuration or health. Connection failures need diagnosis before configuration changes.
