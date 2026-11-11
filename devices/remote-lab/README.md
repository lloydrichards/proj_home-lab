# remote-lab

The Pi 5 hosts existing applications through Coolify and Cloudflare Tunnel. Ordinary OpenSSH over Tailscale is the maintenance path. Coolify retains a root deployment connection; that exception does not apply to the HP or admin-lab.

Hardware belongs in the [inventory](../_reference/inventory.md). Installed services, endpoints, permissions, and dated checks belong in the [service register](../_reference/services.md). The [architecture explanation](../home-lab/explanations/architecture.md) shows this host's role beside the HP.

## Operate and recover

- [Connect with SSH and verify the host](../_reference/ssh-access.md).
- [Configure or repair Coolify's Cloudflare route](coolify-cloudflare.md).
- [Configure Pi backups and R2 copying](how-to/configure-backups.md).
- [Check backups and recover a failed export](how-to/check-backups.md).
- [Restore Pi application data](how-to/restore-backups.md).
- [Look up backup scope and service contracts](reference/backups.md).
- [Roll back Portainer retirement](docker.md#restore-the-retired-dashboard), only if needed.

The [security explanation](../home-lab/explanations/security-and-isolation.md) describes retained deployment and Docker-socket authority. Application network separation is partial; further isolation and build-secret changes remain deferred. The [service register](../_reference/services.md#remaining-security-review-scope) records these limits.

## Rebuild with care

The backup guides describe recovery data and tested drills, not a fully rehearsed replacement Pi. Preserve the original Coolify `APP_KEY`, compatible database images, storage mapping, and connector credentials. Restore into private staging before reconnecting production routes.

These earlier recipes are historical and unverified against the current Pi. They are not the current security baseline:

- [Initial Raspberry Pi setup](setup.md).
- [Earlier SSH hardening](ssh-hardening.md).
- [Docker and Portainer installation](docker.md).
- [Retired public SSH through Cloudflare](cloudflare-ssh.md).
- [Earlier PostgreSQL Compose stack](postgres.md).
- [Initial Coolify installation](coolify.md).

## Choices and knowledge

The [keep-hosting-separate decision](../../.okf/decisions/keep-pi-hosting-separate.md) preserves this host's workloads while HP development is established. [Coolify](../../.okf/technologies/coolify.md), [Cloudflare Tunnel](../../.okf/technologies/cloudflare-tunnel.md), [Docker](../../.okf/technologies/docker.md), and [PostgreSQL](../../.okf/technologies/postgresql.md) connect the concepts and sources. Return to [all devices](../../README.md).
