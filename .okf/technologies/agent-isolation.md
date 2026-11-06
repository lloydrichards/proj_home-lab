---
type: Concept
title: "Agent isolation"
description: "Boundaries around coding tools, credentials, and host administration."
status: draft
sources:
  - id: source-1
    resource: "../../docs/hp/00-design.md"
  - id: source-2
    resource: "../../docs/hp/06-security.md"
  - id: source-3
    resource: "../../docs/hp/07-optional-services.md"
---

# Agent isolation

The HP plan separates a maintenance account from a coding account without sudo or host Docker access. This limits what a compromised tool can administer, but every task under the coding account still shares its accessible files and credentials.

Separate worktrees and terminal sessions prevent some workflow collisions. They are not security boundaries. Permission prompts express consent; they do not sandbox shell commands, extensions, plugins, hooks, or MCP servers.

A disposable VM with scoped credentials is the proposed stronger boundary for untrusted repositories. Its file sharing, network access, credentials, browser tests, and resource limits still need a concrete design. This option is deferred.

Both [Pi](pi-coding-agent.md "applies to") and [OpenCode](opencode.md "applies to") execute tools under these constraints. [Docker](docker.md "does not automatically provide") socket access can defeat the intended boundary. See [private networks and isolation](../learnings/private-network-is-not-isolation.md "distinguishes transport from").
