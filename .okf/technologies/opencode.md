---
type: Concept
title: "OpenCode"
description: "The installed HP terminal agent and optional private browser workflow."
status: draft
sources:
  - id: source-1
    resource: "../../research/opencode-v2.md"
  - id: source-2
    resource: "../../research/remote-coding.md"
  - id: source-3
    resource: "../../devices/home-lab/setup.md"
---

# OpenCode

OpenCode 2.2.6 was installed and its terminal interface checked on `home-lab` as `coder` over LAN SSH on 9 November 2026. No existing executable or pacman OpenCode package was found. Mise could not resolve its Node dependency while offline, so the official standalone installer supplied the user-owned binary. The setup guide cited in `source-3` owns the recipe. Provider sign-in and a model request remain untested.

The v2 note describes a shared background server per OS user and local browser pairing. The installed server was observed listening only on `127.0.0.1:49374`. Separate terminal sessions do not imply separate service identities. Use [OpenSSH forwarding](openssh.md "uses for private browser access") for the optional browser workflow and inspect authentication before relying on it. Browser pairing has not been tested on this host.

The v1 section remains historical comparison material. Its package, attach commands, and password variable differ from v2. [Version identity](../learnings/version-identity-before-recipes.md "requires checking") matters before copying a recipe.

Pairing and private transport restrict access to the service. Tool execution still has the coding account's file access. Apply [agent isolation](agent-isolation.md "requires") and use [tmux](tmux.md "uses for terminal continuity") for the initial terminal workflow.

On 9 November 2026, Lloyd requested Rex over SSH instead of tmux. A personal Rex server under `coder` now runs OpenCode in a native terminal; Mac CLI capture through an SSH socket forward verified startup. GUI access, logout persistence and reboot recovery remain untested. The setup guide cited in `source-3` owns connection and recovery commands.
