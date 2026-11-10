---
type: Decision
title: "Share agent skills through Git and selected local installations"
description: "Editable source, pinned upstream content, and conflict-aware local installation across Mac and HP."
status: stable
sources:
  - id: workflow-and-verification
    resource: "../../research/shared-agent-skills.md"
  - id: installed-selection
    resource: "../../devices/_reference/services.md"
  - id: hp-preparation
    resource: "../../devices/home-lab/preparation.md"
---

# Share agent skills through Git and selected local installations

On 10 November 2026, Lloyd selected the personal skills repository as the shared source for Mac and HP. Keep authored skills and maintained adaptations editable in source, with attribution intact. Fetch unchanged third-party skills from explicitly pinned commits rather than treating an installed folder as their source of truth.

Separate source synchronization from installation. Review and integrate changes through Git, preserving local source edits, then preview and apply the machine's selected profiles. Avoid automatic pulls and bidirectional synchronization of live installation folders. The installer owns only its recorded copies and refuses changed or unowned content. This makes installed edits visible conflicts instead of silently losing them during updates.

Use one shared user discovery root for Codex and OpenCode. Preserve project-specific skills and application-managed skills under their existing owners. Keep machine configuration, credentials, caches, native binaries, and GitButler workspace state outside portable skill source. GitButler and Rex remain externally managed. Optional workflows still depend on the machine's actual tools and permissions.

The initial HP conflict tests and fresh Codex/OpenCode discovery passed. Lloyd subsequently reported a successful cross-machine Effect update with matching installed hashes and unchanged ownership state on repeat application. The workflow-and-verification source records the evidence and its limits; the installed-selection source owns revisions and enabled profiles. Retain migration backups for recovery. Successful synchronization does not establish execution of every skill or provide off-machine workspace protection.

MCP-hosted skills remain deferred because native loading in the intended clients was not established. This is not a claim that the extension is unsupported. Git source plus native discovery meets the current requirement without adding a running service.

This supports [private remote development](../technologies/private-remote-development.md "supports consistent workflows for"). Shared instructions do not restrict tool authority; [agent isolation](../technologies/agent-isolation.md "remains independent of") is a separate boundary. Local migration copies also need [independent backups](../technologies/restic.md "does not replace") for protection against host loss.
