# home-lab

The arriving HP EliteDesk is the planned home development and AI coding host. `home-lab` is its planned hostname; installation, access, and recovery have not been checked on the machine.

## Start here

Follow the [preparation checklist](preparation.md), then the [post-install setup guide](setup.md) once Omarchy is installed. The checklist is the single list of upcoming HP work. Start with SSH and tmux from the MacBook; the daily client is still undecided.

Hardware and name details live in the shared [inventory](../reference/inventory.md). Service placement and access gaps live in the [service register](../reference/services.md). Mounting and purchase details live in the [BOM](../reference/bom.md).

## Choices and evidence

- [Private remote development](../.okf/decisions/home-lab/private-development.md) records the access and coding approach.
- [Unencrypted unattended boot](../.okf/decisions/home-lab/unattended-boot.md) records the boot preference and physical-access tradeoff.
- [Recovery before reliance](../.okf/decisions/recovery-before-reliance.md) sets the initial recovery checks.
- [Keep existing Pi hosting separate](../.okf/decisions/keep-pi-hosting-separate.md) explains the rollout boundary.
- [Omarchy research](research/omarchy.md) and [post-install sources](research/setup-sources.md) support the setup guide.
- [Remote desktop research](research/omarchy-remote-desktop.md) compares Mac access, headless operation, responsiveness, and when to retain a monitor.
- [Shared research](../research/README.md) covers private access, backups, and Mac-to-HP tools.

See the [remote-development concept](../.okf/technologies/private-remote-development.md) for how the tools fit together, or return to [all devices and lab records](../README.md).
