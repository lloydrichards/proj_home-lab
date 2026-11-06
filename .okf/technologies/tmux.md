---
type: Concept
title: "tmux"
description: "Persistent terminal sessions across client disconnections."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/03-remote-coding.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
---

# tmux

The proposed workflow starts a terminal session per coding task on the HP. Reattaching after the laptop disconnects returns to the same running shell and tools.

Tmux does not preserve running processes across a server reboot. Saved agent conversations are a separate form of persistence, and [backups](restic.md "complements") protect another failure case. See [session persistence and recovery](../learnings/session-persistence-is-not-recovery.md "illustrates").

Use separate workspaces for concurrent tasks. This prevents editing collisions but does not isolate credentials or permissions. Both [Pi](pi-coding-agent.md "hosts terminal sessions for") and [OpenCode](opencode.md "hosts terminal sessions for") can use the terminal workflow.
