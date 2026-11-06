---
okf_version: "0.2"
---

# Home lab knowledge

A linked library distilled from repository research, historical setup guides, and the HP plan. Start with [private remote development](technologies/private-remote-development.md) for the HP or [Coolify](technologies/coolify.md) for existing hosting.

Operational records remain in `docs/reference/`. Procedures remain in `docs/hp/` and the historical Pi guides. Source metadata points to the owning documents without duplicating their commands. This expansion synthesizes existing research; it is not a fresh release or hardware verification.

All concepts use `draft` while setup and research remain unsettled. A user-confirmed choice is identified in its decision text. Learning entries are conclusions from the guides unless an actual observation is stated. No HP acceptance check has been completed, and live Pi inspection is deferred.

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

## Decisions

- [Keep existing Pi hosting during HP setup](decisions/keep-pi-hosting-separate.md)
- [Keep remote development private](decisions/private-development.md)
- [Test recovery before relying on the HP](decisions/recovery-before-reliance.md)
- [Choose unencrypted unattended boot](decisions/unattended-boot.md)

## Learnings

- [Keep recovery access during access changes](learnings/access-changes-need-recovery.md)
- [Measure tools before increasing agent concurrency](learnings/measure-agent-capacity.md)
- [Private networking does not isolate agent tools](learnings/private-network-is-not-isolation.md)
- [Session persistence is not recovery](learnings/session-persistence-is-not-recovery.md)
- [Root snapshots do not protect workspace data](learnings/snapshots-are-not-backups.md)
- [Test effective network exposure](learnings/test-effective-exposure.md)
- [Identify the version before copying a recipe](learnings/version-identity-before-recipes.md)

## Read across topics

- Private access: [architecture](decisions/private-development.md), [Tailscale](technologies/tailscale.md), [OpenSSH](technologies/openssh.md), and [effective exposure](learnings/test-effective-exposure.md).
- Agent execution: [isolation](technologies/agent-isolation.md), [Pi](technologies/pi-coding-agent.md), [OpenCode](technologies/opencode.md), and [capacity](learnings/measure-agent-capacity.md).
- Continuity and recovery: [tmux](technologies/tmux.md), [systemd](technologies/systemd.md), [boot preference](decisions/unattended-boot.md), and [backups](technologies/restic.md).
- Existing hosting: [Coolify](technologies/coolify.md), [Cloudflare Tunnel](technologies/cloudflare-tunnel.md), [Docker](technologies/docker.md), and [migration boundaries](decisions/keep-pi-hosting-separate.md).

## Gaps worth investigating

- Inspect the Pi-hole DNS and possible DHCP role, then document recovery and client dependencies.
- Inspect Coolify workloads, authentication, data locations, tunnel routing, and backups.
- Select the HP backup destination, retention, schedule, and failure notification route.
- Verify delivered HP hardware, installed tools, access denial, cold boot, restore, and workload capacity.
- Design and test a disposable VM boundary if untrusted coding work is needed.

Use `docs/README.md` for the contribution workflow and `docs/research/` for source-backed investigations. Keep raw private evidence in ignored `local/`.
