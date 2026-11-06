# Home lab

Documentation, inventory, setup guides, operating logs, and research for Lloyd's home lab.

## Current setup

| Device | Role | State on 6 November 2026 |
|---|---|---|
| Raspberry Pi, previously documented as Pi 5 | Coolify with a Cloudflare tunnel | Running, user reported. Model and configuration await inspection. |
| Raspberry Pi 4 | Pi-hole | Running, user reported. Configuration awaits inspection. |
| HP EliteDesk 800 G6 Desktop Mini | Main remote development and AI coding host | Purchased, arriving soon. Installation is planned. |
| DeskPi RackMate T1 | Rack | Recorded in earlier notes. Mounting details await confirmation. |

## Find information

- [Inventory](docs/reference/inventory.md) records devices and what remains unknown.
- [Service register](docs/reference/services.md) records what runs where and its dependencies.
- [Bill of materials](docs/reference/bom.md) records purchases and planned parts.
- [Concept and technology library](.okf/index.md) connects what we have explored and why it matters here.
- [Research](docs/research/README.md) holds source-backed investigations.
- [Operating log](docs/logs/README.md) records changes, incidents, and lessons.
- [Decisions](docs/decisions/0001-private-development-host.md) record choices and their reasons.
- [Documentation workflow](docs/README.md) explains where to put new material.
- [Configuration examples](config/README.md) accompany the guides.

## Prepare the HP

The HP is planned as a private remote development machine. Existing guides propose Omarchy, OpenSSH over Tailscale, persistent terminal sessions, and Pi or OpenCode. Installation and acceptance checks remain unperformed.

1. [Design and scope](docs/hp/00-design.md)
2. [Installation](docs/hp/01-install.md)
3. [Private access](docs/hp/02-private-access.md)
4. [Remote coding](docs/hp/03-remote-coding.md)
5. [Operations and recovery](docs/hp/04-operations.md)
6. [Acceptance checks](docs/hp/05-acceptance.md)
7. [Security boundaries](docs/hp/06-security.md)
8. [Optional services](docs/hp/07-optional-services.md)

## Existing Pi guides

[The earlier overview](docs/reference/earlier-pi-overview.md) and numbered files directly under `docs/` describe the earlier Pi setup. Preserve them as historical instructions until live inspection establishes which steps still apply. They do not establish the running configuration or the HP security baseline.

Keep credentials, private keys, tokens, and raw machine evidence outside Git. Use ignored `local/` for private inspection output. Review addresses, device identifiers, and logs before adding summaries.
