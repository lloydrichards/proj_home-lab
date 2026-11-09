# Home lab notebook

An assistant-maintained notebook for setting things up, troubleshooting, and remembering what we explored and why.

## The lab

| Device | Machine and purpose | Access |
|---|---|---|
| [home-lab](devices/home-lab/README.md) | HP EliteDesk with Omarchy installed for remote development and AI coding | OpenSSH over Tailscale; `lloyd` for maintenance, `coder` for projects. See [access](devices/_reference/services.md). |
| [remote-lab](devices/remote-lab/README.md) | Pi 5 with Coolify and Cloudflare Tunnel, user reported | SSH details need checking when Wi-Fi returns |
| [admin-lab](devices/admin-lab/README.md) | Pi 4 with Pi-hole, user reported | SSH details not yet recorded |

The HP reports hostname `home-lab`. Pi names remain planned, not verified.

Use devvm locally on the MacBook for selected projects that need isolation. Use the HP for ordinary remote coding and work that should continue while the Mac sleeps. HP project VMs are deferred. The HP is installed; project and backup setup remain open.

## Next

The HP passed startup without a monitor. Finish the [remaining readiness checks](devices/home-lab/preparation.md#before-routine-use-without-a-monitor), then choose and test an off-machine backup. Keep the existing Pi services in place.

## Look something up

- [What we know and why](.okf/index.md): technologies, choices, alternatives, and learnings.
- [Devices and parts](devices/_reference/inventory.md), [services](devices/_reference/services.md), and [BOM](devices/_reference/bom.md).
- [Shared research](research/README.md): private access, backups, and Mac client options.

Each device page links its guides, research, and OKF decisions. Add future devices under `devices/` with a short README; keep lab-wide records in `devices/_reference/`.

The HP was inspected over SSH on 9 November 2026; Pi details remain reported or historical. The assistant updates this notebook as we work. Git keeps the history.
