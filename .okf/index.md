---
okf_version: "0.2"
---

# Home lab knowledge

The assistant's context for the lab: technologies, the reasons for choices, alternatives, and reusable learnings. Start with [private remote development](technologies/private-remote-development.md) for home-lab, [Coolify](technologies/coolify.md) for remote-lab hosting, or [Pi-hole](technologies/pi-hole.md) for admin-lab DNS.

Machine and service facts live in `reference/`. The HP starts with `home-lab/preparation.md`; repeatable recipes are recorded as we do the setup. Root-level device pages link their guides and decisions. Research lives with its device or in `research/` when shared. This library owns the why, with Git keeping previous versions.

All concepts use `draft` while setup and research remain unsettled. A user-confirmed choice is identified in its decision text. Learning entries are conclusions from research unless an actual observation is stated. No HP setup check has been completed, and live Pi inspection is deferred.

## Technologies and workflows

- [Agent isolation](technologies/agent-isolation.md)
- [Cloudflare Tunnel](technologies/cloudflare-tunnel.md)
- [Coolify](technologies/coolify.md)
- [Docker](technologies/docker.md)
- [Omarchy](technologies/omarchy.md)
- [OpenCode](technologies/opencode.md)
- [OpenSSH](technologies/openssh.md)
- [Pi coding agent](technologies/pi-coding-agent.md)
- [Pi-hole](technologies/pi-hole.md)
- [PostgreSQL](technologies/postgresql.md)
- [Private remote development](technologies/private-remote-development.md)
- [Restic](technologies/restic.md)
- [systemd](technologies/systemd.md)
- [Tailscale](technologies/tailscale.md)
- [tmux](technologies/tmux.md)

## Choices and why

Device-specific choices live under `decisions/<device>/`. Choices spanning devices stay directly under `decisions/`; technologies and learnings remain shared. The device READMEs provide navigation without duplicating decision text.

- [Keep existing Pi hosting during HP setup](decisions/keep-pi-hosting-separate.md)
- [Keep remote development private](decisions/home-lab/private-development.md)
- [Test recovery before relying on the HP](decisions/recovery-before-reliance.md)
- [Choose unencrypted unattended boot](decisions/home-lab/unattended-boot.md)

## Learnings

- [Keep recovery access during access changes](learnings/access-changes-need-recovery.md)
- [Measure tools before increasing agent concurrency](learnings/measure-agent-capacity.md)
- [Private networking does not isolate agent tools](learnings/private-network-is-not-isolation.md)
- [Session persistence is not recovery](learnings/session-persistence-is-not-recovery.md)
- [Root snapshots do not protect workspace data](learnings/snapshots-are-not-backups.md)
- [Test effective network exposure](learnings/test-effective-exposure.md)
- [Identify the version before copying a recipe](learnings/version-identity-before-recipes.md)

## Read across topics

- Private access: [architecture](decisions/home-lab/private-development.md), [Tailscale](technologies/tailscale.md), [OpenSSH](technologies/openssh.md), and [effective exposure](learnings/test-effective-exposure.md).
- Agent execution: [isolation](technologies/agent-isolation.md), [Pi](technologies/pi-coding-agent.md), [OpenCode](technologies/opencode.md), and [capacity](learnings/measure-agent-capacity.md).
- Continuity and recovery: [tmux](technologies/tmux.md), [systemd](technologies/systemd.md), [boot preference](decisions/home-lab/unattended-boot.md), and [backups](technologies/restic.md).
- Existing hosting: [Coolify](technologies/coolify.md), [Cloudflare Tunnel](technologies/cloudflare-tunnel.md), [Docker](technologies/docker.md), and [migration boundaries](decisions/keep-pi-hosting-separate.md).

## Next work

Upcoming HP tasks live in `home-lab/preparation.md`. Host-specific unknowns live in the inventory and service register; open technology questions stay with their concepts. Research supplies detailed evidence when a task needs it.

Use `README.md` to find device guides, device research, and shared investigations. Keep raw private evidence in ignored `local/`.
