---
type: Decision
title: "Keep remote development private"
description: "The proposed HP access architecture and its exposure limits."
status: draft
sources:
  - id: source-1
    resource: "../../docs/decisions/0001-private-development-host.md"
  - id: source-2
    resource: "../../docs/hp/06-security.md"
---

# Keep remote development private

The architecture decision proposes Ethernet, [Tailscale](../technologies/tailscale.md "uses for connectivity"), and ordinary [OpenSSH](../technologies/openssh.md "uses for login") for the HP. Administration stays private; selected browser interfaces bind to loopback and use SSH forwarding.

Public SSH, router forwarding, Funnel, and public agent APIs are excluded from the baseline. Existing Pi hosting remains separate. This architecture is proposed; the user-confirmed choices recorded in the source are Pi coding agent identity and unencrypted unattended boot, not a completed installation.

The coding account lacks administrative and Docker privileges. [Agent isolation](../technologies/agent-isolation.md "constrains") still needs separate treatment because private access does not make repository code trustworthy.

The decision is implemented by the [remote-development workflow](../technologies/private-remote-development.md "governs") and depends on [recovery before reliance](recovery-before-reliance.md "requires").
