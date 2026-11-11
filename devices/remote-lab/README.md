# remote-lab

The Pi 5 hosts applications through Coolify and Cloudflare Tunnel. Human maintenance uses ordinary OpenSSH over Tailscale. Coolify retains its separate root deployment connection.

The [inventory](../_reference/inventory.md) owns hardware facts. The [service register](../_reference/services.md) owns endpoints, permissions, and dated checks.

## Build or understand the host

- [Build a Pi application host](setup.md) connects installation, access, routing, and recovery. The replacement-hardware sequence is unrehearsed.
- [Application hosting](explanations/application-hosting.md) explains public requests, deployments, Docker networks, and persistent data.
- Shared [architecture](../../docs/explanations/architecture.md), [security and access](../../docs/explanations/security-and-access.md), and [backup and recovery](../../docs/explanations/backup-and-recovery.md) explain the cross-device design.

## Operate and recover

- [Connect with SSH and verify the host](../../docs/how-to/connect-with-ssh.md).
- [Configure or repair Coolify's Cloudflare route](coolify-cloudflare.md).
- [Configure Pi backups and R2 copying](how-to/configure-backups.md).
- [Check backups and recover a failed export](how-to/check-backups.md).
- [Restore Pi application data](how-to/restore-backups.md).
- [Look up backup scope and service contracts](reference/backups.md).
- [Roll back Portainer retirement](docker.md#restore-the-retired-dashboard), only if needed.

Application network separation is partial. Further isolation and build-secret changes remain deferred. The [service register](../_reference/services.md#remaining-security-review-scope) records the limits.

## Historical recipes

The earlier [SSH hardening](ssh-hardening.md), [Docker and Portainer installation](docker.md), [public Cloudflare SSH](cloudflare-ssh.md), [PostgreSQL Compose stack](postgres.md), and [Coolify installation](coolify.md) are historical context. They are unverified against the current Pi and do not define its security or recovery baseline.

## Choices and knowledge

The [keep-hosting-separate decision](../../.okf/decisions/keep-pi-hosting-separate.md) preserves this host's workloads while HP development is established. [Coolify](../../.okf/technologies/coolify.md), [Cloudflare Tunnel](../../.okf/technologies/cloudflare-tunnel.md), [Docker](../../.okf/technologies/docker.md), and [PostgreSQL](../../.okf/technologies/postgresql.md) connect the concepts and sources. Return to [all devices](../../README.md).
