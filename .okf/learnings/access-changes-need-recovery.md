---
type: Learning
title: "Keep recovery access during access changes"
description: "A fresh login proves more than an existing connection surviving."
status: draft
sources:
  - id: source-1
    resource: "../../research/private-access.md"
  - id: source-3
    resource: "../../devices/_reference/services.md"
---

# Keep recovery access during access changes

An established SSH connection can remain usable while new connections are blocked by an authentication, firewall, or policy change. Keeping it open preserves a chance to fix the change; testing a fresh second login establishes that the new route still works.

The [OpenSSH](../technologies/openssh.md "guides changes to") research recommends checking syntax and effective settings before reload and keeping local-console access available. The [Tailscale](../technologies/tailscale.md "guides changes to") research warns against resetting the only working access route remotely.

A failed connection does not establish a host's configuration or health. Diagnose connectivity before changing access settings.
