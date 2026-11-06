---
type: Decision
title: "Keep remote development private"
description: "The proposed HP access architecture and its exposure limits."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp-preparation.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
---

# Keep remote development private

The proposed approach is Ethernet, [Tailscale](../technologies/tailscale.md "uses for connectivity"), and ordinary [OpenSSH](../technologies/openssh.md "uses for login"). The HP will run remote coding sessions, builds, and tests. Private access limits who can reach those tools without requiring public administration endpoints.

Prefer a separate maintenance account and an unprivileged coding account. Keep browser interfaces on loopback with selected SSH forwarding. Existing Pi hosting stays separate while we establish the HP workflow. These are proposals, not observed settings. Pi coding agent identity and unencrypted boot were user-confirmed on 6 November 2026.

Tailscale SSH remains an alternative with separate identity rules and recovery tests. A public Cloudflare or Funnel route would need a specific application use case and authentication plan; neither is needed for the initial coding workflow. A server distribution would be simpler to operate, but Omarchy is the chosen direction.

Private connectivity does not constrain tool execution. [Agent isolation](../technologies/agent-isolation.md "requires") and scoped credentials remain necessary. All agents sharing one account share its readable files.

The [remote-development concept](../technologies/private-remote-development.md "governs") connects the tools. [Recovery before reliance](recovery-before-reliance.md "requires") covers backup and access failure. Revisit this approach if real use calls for different access or stronger isolation.
