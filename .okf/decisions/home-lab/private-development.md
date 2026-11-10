---
type: Decision
title: "Keep remote development private"
description: "The chosen local-isolation and private remote-coding approach."
status: draft
sources:
  - id: observed-access
    resource: "../../../devices/_reference/services.md"
  - id: source-1
    resource: "../../../devices/home-lab/preparation.md"
  - id: source-2
    resource: "../../../research/remote-coding.md"
---

# Keep remote development private

On 7 November 2026, Lloyd chose local devvm for selected MacBook projects and ordinary remote coding on the HP. Local VMs provide isolation for interactive work; the HP provides independent compute for longer jobs and work that should continue while the Mac sleeps. This avoids making HP VM provisioning, port management, and per-VM services part of the initial setup. HP project VMs remain a deferred alternative if a real project needs isolation there. The decision sets the boundary; the service register records the installed services and their checks.

The HP access plan is Ethernet, [Tailscale](../../technologies/tailscale.md "uses for connectivity"), and ordinary [OpenSSH](../../technologies/openssh.md "uses for login"). The HP runs remote coding tools and project checkouts. Private access limits who can reach those tools without requiring public administration endpoints.

Prefer a separate maintenance account and an unprivileged coding account. Keep browser interfaces on loopback with selected SSH forwarding. Existing Pi hosting stays separate while we establish the HP workflow. The service register records the separate installed accounts and working private SSH access. The earlier unencrypted-install preference was superseded by the [TPM-unlock decision](unattended-boot.md "uses for unattended startup").

Tailscale SSH remains an alternative with separate identity rules and recovery tests. A public Cloudflare or Funnel route would need a specific application use case and authentication plan; neither is needed for the initial coding workflow. A server distribution would be simpler to operate, but Omarchy is the chosen direction.

The daily interface is still undecided; the T3 and Rex installations do not establish a daily client choice. Keep each task in one active checkout on one machine and exchange changes through Git. A branch transfer does not transfer uncommitted work or agent conversations.

Private connectivity does not constrain tool execution. [Agent isolation](../../technologies/agent-isolation.md "requires") and scoped credentials remain necessary. All agents sharing one account share its readable files.

The [remote-development concept](../../technologies/private-remote-development.md "governs") connects the tools. [Recovery before reliance](../recovery-before-reliance.md "requires") covers backup and access failure. Revisit this approach if real use calls for different access or stronger isolation.
