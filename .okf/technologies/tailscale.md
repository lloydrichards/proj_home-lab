---
type: Concept
title: "Tailscale"
description: "Private connectivity for the proposed HP development host."
status: draft
sources:
  - id: source-1
    resource: "../../docs/research/private-access.md"
  - id: source-2
    resource: "../../docs/hp/02-private-access.md"
---

# Tailscale

The HP plan uses Tailscale to connect the laptop to the server without publishing administration endpoints. Installation and access checks remain pending.

Tailscale supplies connectivity and tailnet access policy. [OpenSSH](openssh.md "authenticates Linux logins over") separately authenticates the laptop key and selects the Linux account. Tailscale SSH is a different mode with separate identity and policy behavior; the proposed baseline leaves it disabled.

The access research warns that a narrow new grant does not cancel an existing broad allow. Review effective access across existing ACLs and grants, and test denial from an unauthorized device. Device expiry and recovery also need an explicit plan.

Tailscale Serve is a researched option for private HTTPS. Funnel publishes publicly and is excluded from the [private development decision](../decisions/private-development.md "implements"). Neither private transport nor a policy rule replaces [application authentication](../learnings/private-network-is-not-isolation.md "does not replace").
