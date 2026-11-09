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

The working copy on `home-lab` is `/home/coder/projects/proj_home-lab`, owned by `coder`. It was copied from the Mac on 9 November 2026 with Git history and uncommitted changes preserved. Codex is authenticated with ChatGPT under `coder`; Lloyd confirmed the Mac app connected. Select that host and folder for new Codex chats. The Mac checkout remains as a fallback; avoid editing both copies independently. GitHub push access from the HP has not been tested. Codeburn usage from Mac and HP was paired over an [SSH tunnel](devices/home-lab/setup.md#codeburn-usage-across-mac-and-hp); the HP user service and Mac LaunchAgent restart automatically, but full reboot recovery is untested.

On 9 November 2026, six more Mac checkouts were copied to `/home/coder/projects`: `effect-virtual-fs`, `proj_effect-boxes`, `proj_effect-mcp-conformance`, `proj_okf-graph`, `proj_portfolio-website`, and `shadcn-storybook-registry`. Their Git HEAD and working-tree changes matched after transfer. Ignored files (including local secrets, dependencies, and build output) were excluded; linked Mac worktrees were not copied. `open_effect` was freshly cloned from Lloyd’s GitHub fork instead of transferring its 211 GiB of unreachable Git objects, so its HP HEAD may differ from the Mac’s local-only workspace commit. The Mac copies remain untouched; install dependencies and supply needed secrets separately before running these projects.

## Next

The HP passed startup without a monitor. Finish the [remaining readiness checks](devices/home-lab/preparation.md#before-routine-use-without-a-monitor), then choose and test an off-machine backup. Keep the existing Pi services in place.

## Look something up

- [What we know and why](.okf/index.md): technologies, choices, alternatives, and learnings.
- [Devices and parts](devices/_reference/inventory.md), [services](devices/_reference/services.md), and [BOM](devices/_reference/bom.md).
- [Shared research](research/README.md): private access, backups, and Mac client options.

Each device page links its guides, research, and OKF decisions. Add future devices under `devices/` with a short README; keep lab-wide records in `devices/_reference/`.

The HP and both Pis were inspected over SSH on 9 November 2026. The assistant updates this notebook as we work. Git keeps the history.
