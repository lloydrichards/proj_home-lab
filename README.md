# Home lab notebook

An assistant-maintained notebook for setting things up, troubleshooting, and remembering what we explored and why.

## The lab

| Device | Machine and purpose | Access |
|---|---|---|
| [home-lab](devices/home-lab/README.md) | HP EliteDesk with Omarchy installed for remote development and AI coding | OpenSSH over Tailscale; `lloyd` for maintenance, `coder` for projects. See [access](devices/_reference/services.md). |
| [remote-lab](devices/remote-lab/README.md) | Pi 5 with Coolify and Cloudflare Tunnel | SSH `lloyd@remote-lab` over Tailscale; LAN `192.168.8.142`; [Coolify](http://192.168.8.142:8000) |
| [admin-lab](devices/admin-lab/README.md) | Pi 4 with Pi-hole | SSH `lloyd@admin-lab` over Tailscale; LAN `192.168.8.138`; [Pi-hole](http://192.168.8.138/admin/) |

System names are `home-lab` for HP, `remote-lab` for Pi 5, and `admin-lab` for Pi 4. All three Tailscale names match, with fresh SSH connections verified.

Use devvm locally on the MacBook for selected projects that need isolation. Use the HP for ordinary remote coding and work that should continue while the Mac sleeps. HP project VMs are deferred. The HP receives [nightly Pi backups](devices/remote-lab/backups.md); its own project and workspace backup setup remain open.

## Working on this notebook

Use `/home/coder/projects/proj_home-lab` as `coder` on `home-lab`. Codex is authenticated there, and Lloyd confirmed the Mac app connection. Keep each task in one active checkout and exchange changes through Git. The Mac copies remain recovery fallbacks; see [project handoffs](devices/home-lab/setup.md#project-checkouts-and-source-handoffs).

Edit maintained skills in `/home/coder/projects/skills`, then plan and apply the shared installation. See [synchronization and recovery](research/shared-agent-skills.md). The [service register](devices/_reference/services.md) owns installed versions and verification results.

## Next

The HP passed startup without a monitor. Finish the [remaining readiness checks](devices/home-lab/preparation.md#before-routine-use-without-a-monitor), then choose and test an off-machine backup. Keep the existing Pi services in place.

## Look something up

- [What we know and why](.okf/index.md): technologies, choices, alternatives, and learnings.
- [Devices and parts](devices/_reference/inventory.md), [services](devices/_reference/services.md), and [BOM](devices/_reference/bom.md).
- [Shared research](research/README.md): private access, backups, and Mac client options.

Each device page links its guides, research, and OKF decisions. Add future devices under `devices/` with a short README; keep lab-wide records in `devices/_reference/`.

The assistant maintains the affected records as we work. Git keeps the history.
