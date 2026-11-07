# Home lab notebook

An assistant-maintained notebook for setting things up, troubleshooting, and remembering what we explored and why.

## The lab

| Device | Machine and purpose | Access |
|---|---|---|
| [home-lab](docs/devices/home-lab/README.md) | Arriving HP EliteDesk for remote development and AI coding | Not set up yet |
| [remote-lab](docs/devices/remote-lab/README.md) | Pi 5 with Coolify and Cloudflare Tunnel, user reported | SSH details need checking when Wi-Fi returns |
| [admin-lab](docs/devices/admin-lab/README.md) | Pi 4 with Pi-hole, user reported | SSH details not yet recorded |

These are planned names, not verified hostnames.

Use devvm locally on the MacBook for selected projects that need isolation. Use the HP for ordinary remote coding and work that should continue while the Mac sleeps. HP project VMs are deferred. This is the chosen direction, not an installed setup.

## Next

[Prepare for the HP](docs/devices/home-lab/preparation.md), then follow the [post-install setup guide](docs/devices/home-lab/setup.md). Leave the existing Pi services in place while we get it working.

## Look something up

- [What we know and why](.okf/index.md): technologies, choices, alternatives, and learnings.
- [Devices and parts](docs/reference/inventory.md), [services](docs/reference/services.md), and [BOM](docs/reference/bom.md).
- [Setup recipes and research](docs/README.md): use the relevant note when doing a task.

Current machine details are user-reported or drawn from earlier notes, not live-verified. The assistant updates this notebook as we work. Git keeps the history.
