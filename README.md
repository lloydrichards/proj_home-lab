# Home lab notebook

A guide to a private coding host, existing Pi application hosting, and tested data recovery. It also records the choices and verification limits of Lloyd's installed lab.

| Device | Role | Access |
|---|---|---|
| [home-lab](devices/home-lab/README.md) | HP running Omarchy, coding agents, private previews, and backups | Ordinary OpenSSH over Tailscale; separate maintenance and coding accounts |
| [remote-lab](devices/remote-lab/README.md) | Pi 5 running Coolify and public application routing | Private maintenance SSH; Cloudflare-gated public dashboard |
| [admin-lab](devices/admin-lab/README.md) | Pi 4 running Pi-hole | Private maintenance SSH; DNS and browser status in the service register |

Exact addresses, versions, and dated checks live in the [service register](devices/_reference/services.md) and [inventory](devices/_reference/inventory.md). A written recipe is not proof that its steps ran.

## Choose a starting point

- **Build a machine:** follow [Build a private coding host](devices/home-lab/setup.md). It connects the new-machine tasks; the complete fresh-hardware sequence is not yet rehearsed end to end.
- **Understand the design:** start with [architecture](devices/home-lab/explanations/architecture.md), then [security and isolation](devices/home-lab/explanations/security-and-isolation.md), [unattended boot](devices/home-lab/explanations/unattended-boot.md), or [backup and recovery](devices/home-lab/explanations/backup-and-recovery.md).
- **Operate or recover:** use the [HP task guides](devices/home-lab/README.md#operate-and-recover) or [Pi task guides](devices/remote-lab/README.md#operate-and-recover).
- **Find an unfinished HP check:** use [preparation](devices/home-lab/preparation.md), the single HP work list.

Initial local and R2 backups passed. One R2-restored Codex conversation reopened in an isolated profile. Project checkouts and worktrees are excluded by choice; GitHub does not preserve their uncommitted or unpushed work. Outside email alerts remain deferred.

## Maintain the notebook

Work in `/home/coder/projects/proj_home-lab` as `coder` on home-lab. Keep each task in one active checkout and exchange committed changes through Git. Edit shared skills in their [source repository](research/shared-agent-skills.md), not generated installations.

Reader-facing guides explain and operate the setup. [OKF](.okf/index.md) connects concepts, accepted decisions, and reusable learnings. [Research](research/README.md) retains source evidence and unresolved investigations. [Inventory](devices/_reference/inventory.md), the [service register](devices/_reference/services.md), and the [BOM](devices/_reference/bom.md) own their respective facts. Git keeps change history; secrets and raw private output stay outside Git.
