---
type: Concept
title: "Private remote development"
description: "The installed private HP workflow, selected boundaries, and remaining client and recovery checks."
status: draft
sources:
  - id: inventory
    resource: "../../devices/_reference/inventory.md"
  - id: service-register
    resource: "../../devices/_reference/services.md"
  - id: publishing
    resource: "../../devices/home-lab/publishing.md"
  - id: hp-setup
    resource: "../../devices/home-lab/setup.md"
  - id: source-1
    resource: "../../devices/home-lab/preparation.md"
  - id: source-2
    resource: "../../research/remote-coding.md"
  - id: source-3
    resource: "../../research/remote-agent-tools.md"
---

# Private remote development

The HP is the installed remote development and AI coding host. The inventory and service register own machine configuration and access details; the preparation checklist owns remaining readiness work. A working recipe is not evidence that every recovery check has passed.

The [private-development decision](../decisions/home-lab/private-development.md "is governed by") combines [Tailscale](tailscale.md "connects through") and ordinary [OpenSSH](openssh.md "authenticates through") with separate maintenance and coding accounts. [Omarchy](omarchy.md "runs on") is installed. The Mac supplies the interface while repositories, agents, builds, and tests run on the HP. Hosted providers can supply model inference independently of that split.

[OpenCode](opencode.md "runs through") has verified terminal startup and shared-skill discovery on the HP. [Pi coding agent](pi-coding-agent.md "remains an alternative through") is a separate option with no active HP runtime established. [Tmux](tmux.md "uses for continuity") preserves running terminal sessions after disconnection; it does not restore processes after reboot or replace [backups](restic.md "needs for data recovery").

T3 Code is installed as a loopback-only background service, but its Mac connection and provider request remain unverified. Rex terminal startup and SSH socket access passed; GUI access and reboot recovery remain open. Herdr and the remote-desktop options remain researched alternatives. A daily client has not been chosen. A disconnected client, a closed terminal pane, and a restarted server require different recovery checks.

On 7 November 2026, Lloyd chose devvm locally on the MacBook for selected projects and ordinary coding under the HP's unprivileged account. HP project VMs remain deferred until a project needs stronger isolation. [Agent isolation](agent-isolation.md "requires") limits tool authority independently of network access. [Capacity measurements](../learnings/measure-agent-capacity.md "must validate") determine how many heavy jobs the machine can sustain.

Keep a task in one active checkout and use Git for committed source handoffs. Preserve uncommitted work, ignored files, and agent sessions separately. [Shared skills](../decisions/shared-agent-skills.md "shares instructions through") follow the same explicit source integration, followed by installation on each machine.

The device names are applied and fresh SSH through the lab names passed. OS hostnames, Tailscale names, and Mac aliases remain separate records; matching labels alone do not prove connectivity or authorization. Existing [Pi hosting stays separate](../decisions/keep-pi-hosting-separate.md "leaves public hosting separate through") while HP recovery and workspace protection are completed.

## Delivering work to the Mac

On 10 November 2026, Lloyd chose automatic private delivery of reviewable development work. The [publishing guide](../../devices/home-lab/publishing.md "implements") owns the shell-script workflow. Reports live centrally outside project Git history, retain stable canonical links through revisions, and remain until explicitly deleted. A read-only index supports search and project filters.

Each worktree and browser-facing service has its own persistent preview allocation. Keep previews until explicitly stopped or until both the task is finished and its code is merged. Cleanup protects uncommitted and unpushed work, retains retired URLs, and never deletes reports. Enabled user services support disconnect and boot startup; actual reboot recovery still needs a live test. The service register records the installed private report route and successful host-side browser checks, while Mac access and full reboot recovery remain unverified.

Reservation integrity is part of stable-link delivery. Invalid or conflicting allocation metadata blocks allocation and reuse; deleting uncertain records can silently reassign an old URL. Preview activation clears stale readiness, and failed private-route checks retain a pending allocation rather than advertising a ready preview. The publishing guide owns the status and repair procedure.
