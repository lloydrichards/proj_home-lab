# remote-lab

The Raspberry Pi 5 is the user-reported Coolify and Cloudflare Tunnel host. `remote-lab` is its planned hostname, not a verified access address. Current SSH details, installed versions, workloads, and backups await inspection. Live inspection was deferred while Wi-Fi was unavailable.

## Start here

Keep existing workloads in place during HP setup. When access is available, use the [service register's inspection guidance](../../reference/services.md#next-inspection) to establish what runs here before changing it. Check name and network dependencies before applying the planned hostname.

The shared [inventory](../../reference/inventory.md) owns hardware and naming facts. The [service register](../../reference/services.md) owns service placement and access gaps. Purchases stay in the [BOM](../../reference/bom.md).

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

The shared [keep-existing-hosting decision](../../../.okf/decisions/keep-pi-hosting-separate.md) explains why this machine keeps its services during HP setup. [Coolify](../../../.okf/technologies/coolify.md), [Cloudflare Tunnel](../../../.okf/technologies/cloudflare-tunnel.md), [Docker](../../../.okf/technologies/docker.md), and [PostgreSQL](../../../.okf/technologies/postgresql.md) record the related knowledge and open questions.

There are no separate confirmed Pi 5 decisions yet. Add device-specific decisions under `.okf/decisions/remote-lab/` when needed and link them here. Return to [all devices and lab records](../../README.md).
