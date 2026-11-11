# home-lab

Home-lab is the HP coding host. The Mac supplies its interface; agent processes and files stay on the HP. Maintenance uses `lloyd`, and coding uses `coder`. Hardware and installed versions belong in the [inventory](../_reference/inventory.md); endpoints and verified behavior belong in the [service register](../_reference/services.md).

## Build a new host

Follow [Build a private coding host](setup.md) from installation to private access, a model response, and a recovered conversation. Use your own keys, addresses, and cloud credentials. The installers contain lab-specific inputs, so review the [automation contract](reference/automation.md) before using different names or hardware.

For the installed HP, use the task guides rather than repeating initial enrollment. [Preparation](preparation.md) is the single list of unfinished HP checks.

## Understand the setup

Start with the shared [lab architecture](../../docs/explanations/architecture.md), then use these explanations.

| Explanation | Question it answers |
|---|---|
| [Coding environment](explanations/coding-environment.md) | How do agent sessions, files, and private previews fit together? |
| [Security and isolation](../../docs/explanations/security-and-access.md) | Which connections and privileges are restricted, and which remain powerful? |
| [Unattended boot](explanations/unattended-boot.md) | How does encrypted storage unlock without a monitor, and how does recovery work? |
| [Backup and recovery](../../docs/explanations/backup-and-recovery.md) | What is protected, what is excluded, and what do the restore checks prove? |

## Operate and recover

- [Secure remote access](how-to/secure-remote-access.md).
- [Configure unattended boot](how-to/configure-unattended-boot.md).
- [Install agent tools](how-to/install-agent-tools.md).
- [Back up agent sessions](how-to/back-up-agent-sessions.md).
- [Reopen a restored conversation](how-to/restore-agent-conversation.md).
- [Update the host and recover from failures](how-to/update-and-recover.md).
- [Publish reports and run private previews](publishing.md).
- [Collect and recover Pi backups](../remote-lab/backups.md).
- [Synchronize shared skills](../../research/shared-agent-skills.md).

The [automation reference](reference/automation.md) lists script contracts, paths, units, and schedules. The [SSH guide](../../docs/how-to/connect-with-ssh.md) covers Mac aliases and Pi differences.

## Verification boundary

Monitor-free cold startup, initial local/R2 data restores, and one isolated Codex conversation reopening passed. Those results do not establish every agent client, replacement-host authentication, or future scheduled execution. Project checkouts, worktrees, and the publishing store are outside the accepted agent backup.

## Choices and sources

The accepted choices are [private development](../../.okf/decisions/home-lab/private-development.md), [TPM unlock](../../.okf/decisions/home-lab/unattended-boot.md), [agent-state backup scope](../../.okf/decisions/home-lab/agent-state-backups.md), [shared skills](../../.okf/decisions/shared-agent-skills.md), and [recovery before reliance](../../.okf/decisions/recovery-before-reliance.md).

[Device research](research/omarchy.md), [TPM source evidence](research/tpm-unlock.md), and [shared research](../../research/README.md) support the guides. They are not prerequisites for following the tutorial. Return to [all devices](../../README.md).
