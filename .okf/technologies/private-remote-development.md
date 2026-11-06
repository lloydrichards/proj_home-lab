---
type: Concept
title: "Private remote development"
description: "The planned HP workflow and the concepts it depends on."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/00-design.md"
  - id: source-2
    resource: "../../docs/hp/03-remote-coding.md"
  - id: source-3
    resource: "../../docs/hp/05-acceptance.md"
---

# Private remote development

The arriving HP is intended as the main remote development and AI coding host. Its guides remain proposed and all acceptance checks remain unperformed.

The [private-development decision](../decisions/private-development.md "is governed by") combines [Tailscale](tailscale.md "connects through") and [OpenSSH](openssh.md "authenticates through") with separate maintenance and coding accounts. [Omarchy](omarchy.md "runs on") supplies the planned operating system.

[Pi coding agent](pi-coding-agent.md "can run") and [OpenCode](opencode.md "can run") are independent terminal options. [Tmux](tmux.md "uses for continuity") preserves their running terminal sessions after laptop disconnection. It does not replace [backups](restic.md "needs for data recovery") or reboot recovery.

[Agent isolation](agent-isolation.md "requires") limits tool authority independently of network access. [Capacity measurements](../learnings/measure-agent-capacity.md "must validate") determine how many heavy jobs the machine can sustain.

The plan [retains existing Pi hosting](../decisions/keep-pi-hosting-separate.md "leaves public hosting separate through") during rollout.
