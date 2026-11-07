# Service register

Recorded 6 November 2026 from the user's description. Live inspection is deferred because the user reported that Wi-Fi is down and asked to skip SSH.

| Service | Host | Access and dependencies | Evidence and gaps |
|---|---|---|---|
| Coolify | Raspberry Pi 5, user identified 7 November 2026 | Cloudflare tunnel, user reported | Version, deployed apps, storage, backup, and tunnel implementation unknown |
| Pi-hole | Raspberry Pi 4 | DNS service, user reported | Upstream DNS, DHCP ownership, client configuration, access, and backup unknown |
| Remote coding | Future HP | Proposed OpenSSH over Tailscale | Not installed or verified. See [HP preparation](../devices/home-lab/preparation.md). |

Planned hostnames are recorded in the [inventory](inventory.md#planned-device-names). They are not current access details; do not replace existing Pi endpoints until separately checked.

## Next inspection

Record hostname, hardware, OS, service versions, failed services, storage use, and backup arrangements. For Coolify, inspect container names and images without dumping environment variables. For Pi-hole, establish whether it also supplies DHCP before planning restarts or migration.

Record how the tunnel runs, its destination, and whether Cloudflare Access protects administration. A tunnel alone does not establish application authentication. Keep tokens and populated tunnel configuration out of Git.

Before moving any service to the HP, record its data location, dependencies, backup, restore check, and rollback procedure. No migration has been selected.
