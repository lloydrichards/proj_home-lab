---
type: Concept
title: "Agent isolation"
description: "Boundaries around coding tools, credentials, and host administration."
status: draft
sources:
  - id: source-1
    resource: "../../home-lab/preparation.md"
  - id: source-2
    resource: "../../research/remote-coding.md"
  - id: client-isolation-research
    resource: "../../research/remote-agent-tools.md"
---

# Agent isolation

The HP plan separates a maintenance account from a coding account without sudo or host Docker access. This limits what a compromised tool can administer, but every task under the coding account still shares its accessible files and credentials.

Separate worktrees and terminal sessions prevent some workflow collisions. They are not security boundaries. Permission prompts express consent; they do not sandbox shell commands, extensions, plugins, hooks, or MCP servers.

On 7 November 2026, Lloyd chose devvm on the MacBook for selected projects needing isolation. Ordinary HP coding remains under the unprivileged coding account without project VMs. A disposable HP VM with scoped credentials remains a deferred option for work requiring a stronger boundary there. The explored T3 design places its server, agents, Git operations, tests, and browser inside that guest; a host-side agent wrapper alone does not isolate all T3 operations. No devvm installation or combined T3 integration has been verified.

Devvm normally reuses a VM for a project folder, so one VM per task requires distinct VM identities. Its default writable project mount exposes that host checkout to edits. Its separate-clone mode is the proposed option when protecting the host working tree matters. Credential proxying and network restrictions still need provider-specific checks, and this is not a tested security assessment. VM creation and destruction remain host-side operations outside the guest agent's authority.

Both [Pi](pi-coding-agent.md "applies to") and [OpenCode](opencode.md "applies to") execute tools under these constraints. [Docker](docker.md "does not automatically provide") socket access can defeat the intended boundary. See [private networks and isolation](../learnings/private-network-is-not-isolation.md "distinguishes transport from").
