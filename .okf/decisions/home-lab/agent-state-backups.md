---
type: Decision
title: "Back up agent state and recover projects from GitHub"
description: "The accepted scope and limits of home-lab's agent backup."
status: stable
sources:
  - id: implementation
    resource: "../../../devices/home-lab/reference/automation.md"
  - id: verification
    resource: "../../../devices/_reference/services.md"
  - id: recovery-guide
    resource: "../../../devices/home-lab/how-to/restore-agent-conversation.md"
---

# Back up agent state and recover projects from GitHub

On 11 November 2026, Lloyd explicitly chose to exclude project checkouts and worktrees from HP backups because the repositories are on GitHub. He accepted that this leaves uncommitted edits, unpushed commits, ignored project files, and local-only branches unprotected.

Back up selected Codex, OpenCode, T3, and Rex state, agent configuration, and shared-skill links. Keep encrypted local history and a separate private R2 repository. The installed policy retains overlapping daily, weekly, and monthly recovery points. Keep repository credentials outside the coding account and recovery secrets outside both hosts.

This scope avoids treating every regenerable checkout as backup data, while preserving conversations that GitHub does not contain. It also excludes the publishing report store. Skill links preserve references rather than the source checkout; recovery must clone the required repositories at compatible paths. Session text and attachments may still contain code and credentials.

A temporary read-only home snapshot supplies stable input while agents run. Only allowed agent paths are uploaded. Initial local/cloud restores and one isolated Codex reopening passed; this is narrower than replacement-host recovery or reopening every agent interface.

Revisit the scope if unpushed work becomes important, repositories leave GitHub, or reports need independent protection. Those are new backup-scope choices, not reasons to silently enlarge the current allowlist. The [restic concept](../../technologies/restic.md "implements through") explains the consistency and authority boundaries, and [recovery before reliance](../recovery-before-reliance.md "follows") explains the acceptance rule.
