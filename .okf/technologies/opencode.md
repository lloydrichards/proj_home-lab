---
type: Concept
title: "OpenCode"
description: "A researched terminal and browser coding workflow for the HP."
status: draft
sources:
  - id: source-1
    resource: "../../docs/research/opencode-v2.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
---

# OpenCode

The OpenCode v2 research records dated package evidence, service behavior, and workflow options. Write the HP recipe when we try the installed executable. It prefers an existing suitable Omarchy-managed executable available to the coding account before adding a competing installation. The installed version and behavior remain unknown.

The v2 note describes a shared background server per OS user and local browser pairing. Separate terminal sessions do not imply separate service identities. Use [OpenSSH forwarding](openssh.md "uses for private browser access") for the optional browser workflow and inspect the actual listening address and authentication.

The v1 section remains historical comparison material. Its package, attach commands, and password variable differ from v2. [Version identity](../learnings/version-identity-before-recipes.md "requires checking") matters before copying a recipe.

Pairing and private transport restrict access to the service. Tool execution still has the coding account's file access. Apply [agent isolation](agent-isolation.md "requires") and use [tmux](tmux.md "uses for terminal continuity") for the initial terminal workflow.
