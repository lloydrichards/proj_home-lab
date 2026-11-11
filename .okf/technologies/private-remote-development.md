---
type: Concept
title: "Private remote development"
description: "Mac interfaces, persistent HP execution, and private delivery of reviewable work."
status: draft
sources:
  - id: architecture
    resource: "../../docs/explanations/architecture.md"
  - id: security
    resource: "../../docs/explanations/security-and-access.md"
  - id: publishing
    resource: "../../devices/home-lab/publishing.md"
  - id: service-register
    resource: "../../devices/_reference/services.md"
  - id: research
    resource: "../../research/remote-agent-tools.md"
---

# Private remote development

The Mac supplies the interface while home-lab keeps project files, agents, builds, and tests running. Hosted providers can supply model inference independently. Private transport does not mean the model runs on the HP.

The [private-development decision](../decisions/home-lab/private-development.md "governs") combines [Tailscale](tailscale.md "connects through"), [OpenSSH](openssh.md "authenticates through"), and separate maintenance and coding accounts. [Agent isolation](agent-isolation.md "requires") remains a process and credential question: every agent under coder shares that account's accessible data. HP project VMs are deferred; local Mac VMs remain the chosen option for selected stronger-isolation work.

Terminal persistence, service supervision, and data recovery solve different failures. [Tmux](tmux.md "provides disconnect continuity through") can keep a terminal alive after a client disconnect. [Systemd](systemd.md "supervises services through") can restart configured services. [Restic](restic.md "recovers saved data through") preserves selected state after data loss. None alone establishes all three forms of continuity.

Private publishing gives reports stable canonical links and worktree services distinct preview allocations. Reports remain until explicitly deleted. Preview cleanup requires an explicit stop or both task completion and merged code; active services keep their worktrees. Retired URL allocations are not reassigned. Reservation validation and readiness checks prevent an old link from silently naming another app.

A fixed administrator helper manages only reviewed private HTTPS route operations. That exception is narrower than general sudo, but still part of the authority boundary. The [publishing guide](../../devices/home-lab/publishing.md) owns its commands and lifecycle.

The [architecture explanation](../../docs/explanations/architecture.md) is the reader's complete overview. The service register owns installed client results and recovery gaps. One restored Codex conversation has reopened, but that does not prove all Rex/T3/OpenCode client, provider, or reboot paths. Remaining HP work stays in [preparation](../../devices/home-lab/preparation.md).
