---
type: Learning
title: "Identify the version before copying a recipe"
description: "Commands and package names can change across product generations."
status: draft
sources:
  - id: source-1
    resource: "../../docs/research/opencode-v2.md"
  - id: source-2
    resource: "../../docs/research/remote-coding.md"
  - id: source-3
    resource: "../../docs/research/omarchy-headless.md"
---

# Identify the version before copying a recipe

The OpenCode notes preserve separate v1 and v2 workflows. Their package names, client commands, service model, and authentication variables differ. A generic latest-release redirect was insufficient to resolve the generation during the original research.

Inspect the executable path, version, and installed help before applying a recipe. Avoid competing installations that happen to share a command name. This applies especially to [OpenCode](../technologies/opencode.md "prevents mixing generations of") and to service units whose PATH differs from an interactive desktop account.

[Pi coding agent](../technologies/pi-coding-agent.md "requires identity checks for") also has an explicitly researched product identity. Date-sensitive details remain in the source notes rather than being presented here as newly checked release facts.
