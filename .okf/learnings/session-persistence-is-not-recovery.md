---
type: Learning
title: "Session persistence is not recovery"
description: "Disconnection, reboot, and storage loss need different recovery mechanisms."
status: draft
sources:
  - id: session-research
    resource: "../../docs/research/remote-coding.md"
  - id: service-research
    resource: "../../docs/research/omarchy-headless.md"
  - id: source-1
    resource: "../../docs/hp-preparation.md"
---

# Session persistence is not recovery

[Tmux](../technologies/tmux.md "distinguishes continuity supplied by") preserves a running terminal across a laptop disconnect. It does not preserve processes across reboot. Saved agent sessions may preserve conversations, but do not restore a running compiler or browser.

A supervised [systemd](../technologies/systemd.md "distinguishes restart supplied by") service can restart a reviewed workload after boot. [Backups](../technologies/restic.md "distinguishes data recovery supplied by") recover stored state after deletion or disk loss. None of these mechanisms alone provides all three behaviors.

The HP checklist therefore tests disconnect and reattach, reboot behavior, and a restore drill separately. Those tests remain unperformed.
