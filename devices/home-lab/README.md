# home-lab

The HP runs Omarchy with TPM automatic disk unlock and key-only SSH. The maintenance account is `lloyd`; coding uses `coder`. Tailscale is connected. The [service register](../_reference/services.md) owns current access details.

Monitor-free cold startup passed on 9 November 2026, with both accounts reachable over Tailscale. Overnight idle availability and AC-loss recovery remain open in the [readiness checklist](preparation.md#before-routine-use-without-a-monitor).

## Start here

Follow the [preparation checklist](preparation.md), then the [post-install setup guide](setup.md) for repeatable commands and recovery. The checklist is the single list of upcoming HP work. Start with SSH and tmux from the MacBook; the daily client is still undecided.

Hardware and name details live in the shared [inventory](../_reference/inventory.md). Service placement and access gaps live in the [service register](../_reference/services.md). Mounting and purchase details live in the [BOM](../_reference/bom.md).

## Choices and evidence

- [Private remote development](../../.okf/decisions/home-lab/private-development.md) records the access and coding approach.
- [TPM unattended boot](../../.okf/decisions/home-lab/unattended-boot.md) records the installed unlock approach and recovery tradeoff.
- [Recovery before reliance](../../.okf/decisions/recovery-before-reliance.md) sets the initial recovery checks.
- [Keep existing Pi hosting separate](../../.okf/decisions/keep-pi-hosting-separate.md) explains the rollout boundary.
- [TPM unlock research](research/tpm-unlock.md) explains the measured-boot policy and its limits.
- [Omarchy research](research/omarchy.md) and [post-install sources](research/setup-sources.md) support the setup guide.
- [Remote desktop research](research/omarchy-remote-desktop.md) compares Mac access, headless operation, responsiveness, and when to retain a monitor.
- [Shared research](../../research/README.md) covers private access, backups, and Mac-to-HP tools.

See the [remote-development concept](../../.okf/technologies/private-remote-development.md) for how the tools fit together, or return to [all devices and lab records](../../README.md).
