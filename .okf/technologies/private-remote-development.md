---
type: Concept
title: "Private remote development"
description: "The planned HP workflow and the concepts it depends on."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp-preparation.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
  - id: source-3
    resource: "../../docs/research/remote-agent-tools.md"
---

# Private remote development

The arriving HP is intended as the main remote development and AI coding host. Its setup is still proposed; start with the preparation checklist.

On 6 November 2026, Lloyd confirmed the client is a MacBook and requested several ways to move coding work onto the HP. The desired split keeps the interface on the Mac and the repository, agent tools, builds, and tests on the HP. Model inference can remain with a hosted provider. No particular client was selected.

The [private-development decision](../decisions/private-development.md "is governed by") combines [Tailscale](tailscale.md "connects through") and [OpenSSH](openssh.md "authenticates through") with separate maintenance and coding accounts. [Omarchy](omarchy.md "runs on") supplies the planned operating system.

[Pi coding agent](pi-coding-agent.md "can run") and [OpenCode](opencode.md "can run") are independent terminal options. [Tmux](tmux.md "uses for continuity") preserves their running terminal sessions after laptop disconnection. It does not replace [backups](restic.md "needs for data recovery") or reboot recovery.

[Agent isolation](agent-isolation.md "requires") limits tool authority independently of network access. [Capacity measurements](../learnings/measure-agent-capacity.md "must validate") determine how many heavy jobs the machine can sustain.

The client comparison cited in source-3 researches complementary choices. T3 Code offers a graphical remote-agent interface, Rex a Mac/Linux terminal setup in beta, and Herdr persistent agent terminals with app and TUI variants. A remote editor can handle manual changes in the same HP checkout. These are researched capabilities, not HP-tested integrations.

The deeper comparison on 7 November 2026 separates agent conversation management from terminal management. T3 provides conversation approvals and code review across supported providers. Rex and Herdr retain the agent's terminal interface. Herdr's native app also supplies file and change panels, while its TUI manages worktrees. For unattended work, the HP server must run independently of the Mac client. A disconnected client, a closed terminal pane, and a restarted server are different events. No client choice or deployment was confirmed.

On 7 November 2026, Lloyd chose devvm locally on the MacBook for selected projects and ordinary remote coding on the HP. The decision above owns the rationale. Local VMs use Mac resources and are suitable when work can pause with the laptop. The HP baseline runs coding tools directly under its unprivileged coding account, with separate worktrees for concurrent tasks. No daily client has been chosen.

HP-side devvm and guest-side T3 servers remain researched alternatives, not preparation requirements. Revisit them only when a project needs stronger isolation on the HP. The source-3 research retains the connection design and sizing estimates for that case. Keep each task on one machine and use Git for handoffs, preserving uncommitted work and session state separately.

The plan [retains existing Pi hosting](../decisions/keep-pi-hosting-separate.md "leaves public hosting separate through") during rollout.
