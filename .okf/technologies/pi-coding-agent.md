---
type: Concept
title: "Pi coding agent"
description: "The intended Pi terminal coding agent, distinct from Raspberry Pi hardware."
status: draft
sources:
  - id: source-1
    resource: "../../research/remote-coding.md"
  - id: source-3
    resource: "../../devices/home-lab/preparation.md"
---

# Pi coding agent

Pi here means the coding agent identified in the remote-coding research, not a Raspberry Pi computer. The user confirmed this agent identity for the HP plan.

The research records its package and release identity as checked on 6 November 2026. Consult that note for installation details and recheck the actual executable before installation; this concept does not prescribe an evergreen package version.

The baseline runs Pi as the unprivileged coding account inside [tmux](tmux.md "runs inside"). Extensions and repository tools execute with that account's permissions. Agent prompts do not provide an operating-system sandbox, so [agent isolation](agent-isolation.md "requires") remains a separate concern.

Pi is an alternative to [OpenCode](opencode.md "is an alternative to"), not a dependency of it. The HP has not yet been tested with either tool.
