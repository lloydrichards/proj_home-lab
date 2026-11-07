---
type: Learning
title: "Session persistence is not recovery"
description: "Disconnection, reboot, and storage loss need different recovery mechanisms."
status: draft
sources:
  - id: session-research
    resource: "../../research/remote-coding.md"
  - id: service-research
    resource: "../../devices/home-lab/research/omarchy.md"
  - id: source-1
    resource: "../../devices/home-lab/preparation.md"
  - id: client-research
    resource: "../../research/remote-agent-tools.md"
---

# Session persistence is not recovery

[Tmux](../technologies/tmux.md "distinguishes continuity supplied by") preserves a running terminal across a laptop disconnect. It does not preserve processes across reboot. Saved agent sessions may preserve conversations, but do not restore a running compiler or browser.

A supervised [systemd](../technologies/systemd.md "distinguishes restart supplied by") service can restart a reviewed workload after boot. [Backups](../technologies/restic.md "distinguishes data recovery supplied by") recover stored state after deletion or disk loss. None of these mechanisms alone provides all three behaviors.

Remote agent interfaces have the same distinction. Closing a client can leave its server running, while closing a terminal pane can end the program inside it. A service starting at boot does not prove that an interrupted agent turn, build, or browser resumes. Restored layouts and conversations must be checked separately from running processes.

The HP checklist therefore tests disconnect and reattach, reboot behavior, and a restore drill separately. Those tests remain unperformed.
