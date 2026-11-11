---
type: Concept
title: "OpenSSH"
description: "Key authorization, private transport, and recovery-aware access changes."
status: draft
sources:
  - id: live-access
    resource: "../../devices/_reference/services.md"
  - id: guide
    resource: "../../devices/home-lab/how-to/secure-remote-access.md"
  - id: client-guide
    resource: "../../devices/_reference/ssh-access.md"
  - id: research
    resource: "../../research/private-access.md"
---

# OpenSSH

The lab uses ordinary OpenSSH over [Tailscale](tailscale.md "runs over"). Tailscale controls device reachability; OpenSSH checks the destination account and authorized key. Tailscale SSH is an alternative authentication mode with different host identity and policy behavior, not another name for this setup.

Client aliases, OS hostnames, and private DNS names are separate. Explicit private addresses in account-local aliases can avoid short-name DNS failures, but do not configure DNS or reverse access. Each source account needs its own key and destination authorization.

Fresh Mac logins established independent maintenance access before coder's Pi administrator key was revoked. Removing an authorized key does not delete its stored private key or terminate existing sessions. Changing groups likewise does not revoke supplementary groups from existing processes. The service register owns the current keys, host fingerprints, accounts, and verification dates.

Root SSH is disabled on the HP and admin-lab. Remote-lab intentionally retains Coolify's root deployment connection. Password-required sudo after login is a different boundary from SSH password authentication. A credential that authenticates as root bypasses the human account's sudo restrictions.

The [access-change learning](../learnings/access-changes-need-recovery.md "requires") keeps console or independent recovery access until syntax, effective configuration, and a fresh second login pass. Connection sharing can hide a broken new login; the guide disables reuse for its test. Switching authentication modes requires deliberate host-trust verification.

Loopback forwarding can expose an HP service to the Mac without publishing it on the LAN. Application authentication remains necessary. Do not forward the Mac's SSH agent into the coding account; [agent isolation](agent-isolation.md "protects credentials within") depends on limiting credentials as well as network paths.
