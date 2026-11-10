# home-lab

The HP runs Omarchy with TPM automatic disk unlock and key-only SSH. The maintenance account is `lloyd`; coding uses `coder`. Tailscale is connected. The [service register](../_reference/services.md) owns current access details.

Monitor-free cold startup passed on 9 November 2026, with both accounts reachable over Tailscale. Overnight idle availability and AC-loss recovery remain open in the [readiness checklist](preparation.md#before-routine-use-without-a-monitor).

The HP now receives [nightly remote-lab backups](../remote-lab/backups.md) through a dedicated account. This protects the Pi's data; backup of the HP's own workspaces remains open in the preparation checklist.

## Start here

Follow the [preparation checklist](preparation.md), then the [post-install setup guide](setup.md) for repeatable commands and recovery. The checklist is the single list of upcoming HP work. Start with SSH and tmux from the MacBook; the daily client is still undecided.

[OpenCode 2.2.6](setup.md#opencode-on-the-installed-hp) is installed for `coder` and running in a [Rex session over SSH](setup.md#rex-over-ssh). Mac GUI access and logout persistence still need checks. Provider sign-in remains open. See the [OpenCode concept](../../.okf/technologies/opencode.md) for service behavior and access boundaries.

Hardware and name details live in the shared [inventory](../_reference/inventory.md). Service placement and access gaps live in the [service register](../_reference/services.md). Mounting and purchase details live in the [BOM](../_reference/bom.md).

[T3 Code 0.1.7](setup.md#t3-code-remote-environment) is installed as a background service for `coder`, listening only on loopback. Mac connection and provider setup remain pending.

Shared skills are installed for Codex and OpenCode. Edit the source checkout and follow the [synchronization and recovery guide](../../research/shared-agent-skills.md); the service register owns the current selection and verification results.

## Private reports and previews

Use the [publishing guide](publishing.md) for central HTML reports and persistent worktree previews. Shell scripts live in `tools/publishing/`; report content and allocation records stay outside Git. The service register records the current installation and verification limits.

## Choices and evidence

- [Shared agent skills](../../.okf/decisions/shared-agent-skills.md) explains source ownership, pinned upstream content, and conflict protection.
- [Private remote development](../../.okf/decisions/home-lab/private-development.md) records the access and coding approach.
- [TPM unattended boot](../../.okf/decisions/home-lab/unattended-boot.md) records the installed unlock approach and recovery tradeoff.
- [Recovery before reliance](../../.okf/decisions/recovery-before-reliance.md) sets the initial recovery checks.
- [Keep existing Pi hosting separate](../../.okf/decisions/keep-pi-hosting-separate.md) explains the rollout boundary.
- [TPM unlock research](research/tpm-unlock.md) explains the measured-boot policy and its limits.
- [Omarchy research](research/omarchy.md) and [post-install sources](research/setup-sources.md) support the setup guide.
- [Remote desktop research](research/omarchy-remote-desktop.md) compares Mac access, headless operation, responsiveness, and when to retain a monitor.
- [Shared research](../../research/README.md) covers private access, backups, and Mac-to-HP tools.

See the [remote-development concept](../../.okf/technologies/private-remote-development.md) for how the tools fit together, or return to [all devices and lab records](../../README.md).
