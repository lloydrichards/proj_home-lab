# remote-lab

The Raspberry Pi 5 runs Coolify and Cloudflare Tunnel. `remote-lab` is its applied system and Tailscale name. Fresh SSH through that name passed.

SSH inspection on 9 November 2026 confirmed hostname `remote-lab`, access as `lloyd@192.168.8.142`, and later Coolify 4.7.2 during backup setup. Public routing was restored by repairing the tunnel network connection. See the [recovery procedure](coolify-cloudflare.md#verified-recovery). Tailscale is signed in; `tailscale ssh lloyd@remote-lab` also works from `coder` on home-lab.

SSH password login is enabled on the existing administration endpoint. [Nightly backups to home-lab](backups.md) are installed, with a separate restricted backup account, encrypted history and successful database/file restore checks. The service register owns the endpoint and remaining gaps.

## Start here

Keep existing workloads in place during HP setup. When access is available, use the [service register's inspection guidance](../_reference/services.md#next-inspection) to establish what runs here before changing it. System and Tailscale names now match this device page.

The shared [inventory](../_reference/inventory.md) owns hardware and naming facts. The [service register](../_reference/services.md) owns service placement and access gaps. Purchases stay in the [BOM](../_reference/bom.md).

## Historical recipes

These earlier Pi recipes are grouped here for reference. They have not been checked against the current Pi 5 and do not prove that every described service is deployed. Recheck commands, permissions, versions, and exposure before reuse.

- [Initial Pi setup](setup.md)
- [SSH hardening](ssh-hardening.md)
- [Docker and Portainer](docker.md)
- [SSH through Cloudflare](cloudflare-ssh.md)
- [PostgreSQL on Docker](postgres.md)
- [Coolify](coolify.md)
- [Coolify with Cloudflare Tunnel](coolify-cloudflare.md)

## Choices and knowledge

The shared [keep-existing-hosting decision](../../.okf/decisions/keep-pi-hosting-separate.md) explains why this machine keeps its services during HP setup. [Coolify](../../.okf/technologies/coolify.md), [Cloudflare Tunnel](../../.okf/technologies/cloudflare-tunnel.md), [Docker](../../.okf/technologies/docker.md), and [PostgreSQL](../../.okf/technologies/postgresql.md) record the related knowledge and open questions.

There are no separate confirmed Pi 5 decisions yet. Add device-specific decisions under `.okf/decisions/remote-lab/` when needed and link them here. Return to [all devices and lab records](../../README.md).
