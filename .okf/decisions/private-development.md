---
type: Decision
title: "Keep remote development private"
description: "The chosen local-isolation and private remote-coding approach."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp-preparation.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
---

# Keep remote development private

On 7 November 2026, Lloyd chose local devvm for selected MacBook projects and ordinary remote coding on the HP. Local VMs provide isolation for interactive work; the HP provides independent compute for longer jobs and work that should continue while the Mac sleeps. This avoids making HP VM provisioning, port management, and per-VM services part of the initial setup. HP project VMs remain a deferred alternative if a real project needs isolation there. No installation or live checks are implied.

The HP access plan is Ethernet, [Tailscale](../technologies/tailscale.md "uses for connectivity"), and ordinary [OpenSSH](../technologies/openssh.md "uses for login"). The HP will run remote coding sessions, builds, and tests. Private access limits who can reach those tools without requiring public administration endpoints.

Prefer a separate maintenance account and an unprivileged coding account. Keep browser interfaces on loopback with selected SSH forwarding. Existing Pi hosting stays separate while we establish the HP workflow. These remain planned settings, not observed configuration. Pi coding agent identity and unencrypted boot were user-confirmed on 6 November 2026.

Tailscale SSH remains an alternative with separate identity rules and recovery tests. A public Cloudflare or Funnel route would need a specific application use case and authentication plan; neither is needed for the initial coding workflow. A server distribution would be simpler to operate, but Omarchy is the chosen direction.

The daily interface is still undecided; this choice does not select T3, Rex, or Herdr. Keep each task in one active checkout on one machine and exchange changes through Git. A branch transfer does not transfer uncommitted work or agent conversations.

Private connectivity does not constrain tool execution. [Agent isolation](../technologies/agent-isolation.md "requires") and scoped credentials remain necessary. All agents sharing one account share its readable files.

The [remote-development concept](../technologies/private-remote-development.md "governs") connects the tools. [Recovery before reliance](recovery-before-reliance.md "requires") covers backup and access failure. Revisit this approach if real use calls for different access or stronger isolation.
