# Pi backup reference

This reference describes the maintained [backup scripts](../backup-tools/). Current deployment and dated verification belong in the [service register](../../_reference/services.md). The [design explanation](../../home-lab/explanations/backup-and-recovery.md) describes the tradeoffs.

## Scope and consistency

| Included | Excluded or limited |
|---|---|
| Docker volume `_data` directories, including inactive volumes | Container images and writable container layers |
| Existing regular bind-mount sources | Sockets, including `docker.sock` |
| `/data/coolify` with `.env`, `APP_KEY`, proxy configuration, and SSH material | `/data/coolify/backups` |
| PostgreSQL cluster dumps, separate `coolify.dmp`, manifest, and SHA-256 checksums | Native cloudflared configuration outside mounted storage |
| Container configuration and environment, `/etc/ssh`, `/etc/hostname`, `/etc/hosts` | HP workspaces, host Tailscale identities, and a complete OS image |

The root exporter records running container IDs, stops non-PostgreSQL containers, dumps running PostgreSQL clusters, then stops PostgreSQL and archives cold storage. It restarts only the recorded containers, with PostgreSQL first. Docker receives a 60-second stop grace period. Deployment or container replacement during export can invalidate recovery IDs.

## Hosts, identities, and storage

| Item | Contract |
|---|---|
| Source | Hostname `remote-lab`; Docker and Python 3 |
| Collector | Hostname `home-lab`; systemd, restic, Python 3, ordinary OpenSSH |
| Source transport | Separate sshd on `100.107.227.75:2222`; key restricted to source `100.73.122.94` |
| Source account | `lab-backup`; restricted shell, exact export dispatcher, argument-free exporter sudo grant |
| Destination account | `lab-backup`; `/home/lab-backup`, mode 0700, no login shell |
| Credentials | `/home/lab-backup/credentials/{id_ed25519,known_hosts,restic-password,r2.json}` |
| Source generations | Root-only `/var/lib/lab-backup-export`; latest three successful generations |
| Recovery marker | `/var/lib/lab-backup-export/stopped.json` |
| HP staging | `/home/lab-backup/staging/current`; private plaintext |
| HP repository | `/home/lab-backup/repository`; encrypted restic history |
| R2 repository | Private configured bucket, prefix `remote-lab`; separate restic repository |
| Local status | `/home/lab-backup/last-success.json`, optional `last-failure.txt` |
| R2 status | `/home/lab-backup/r2-last-success.json` |

R2 credentials permit object deletion. Source archives and HP staging contain secrets. The source lacks the HP repository credential. HP root can access both local and cloud credentials.

## Script interfaces

| Source | Installed path | Operations |
|---|---|---|
| `export.py` | `/usr/local/sbin/lab-backup-export` on Pi | Export through the dispatcher; `produce`, `recover` for root services |
| `collect.py` | `/usr/local/sbin/lab-backup-collect` on HP | No argument collects and verifies; `health` checks status and capacity |
| `r2.py` | `/usr/local/sbin/lab-backup-r2` on HP | No argument copies and retains cloud snapshots; `health`; `retention-preview` |
| `restore-test.py` | `/usr/local/sbin/lab-backup-restore-test` on Pi | Isolated PostgreSQL, Coolify credential, and SQLite/WAL drill |
| `install-remote.sh` | Runs on Pi | Requires `id_ed25519.pub` beside installer; installs exporter, restricted sshd, recovery services |
| `install-home.sh` | Runs on HP | Requires ignored `local/backup-bootstrap` keys and host pin; starts one collection before enabling timers |
| `install-home.sh --refresh-services` | Runs on HP | Refreshes reviewed code and units without triggering collection or changing timer activation |
| `install-r2.sh` | Runs on HP | Requires private `r2.json` and restic password; runs cloud copy and health before enabling timers |

These installers are lab-specific. Their hostnames, addresses, account names, paths, and schedule timezone are not command-line configuration options.

## Units and verification

| Unit or policy | Behavior |
|---|---|
| Pi `lab-backup-sshd.service` | Restricted transport after networking and Tailscale |
| Pi `lab-backup-produce.service` | Export generation; `ExecStopPost` retries container recovery |
| Pi `lab-backup-recover.service` | Retries recorded recovery at boot, before backup sshd |
| HP `lab-backup-collect.timer` | Daily 02:00 Europe/Zurich; persistent catch-up |
| HP `lab-backup-health.timer` | Hourly; 26-hour freshness, 20 GiB minimum free, 100 GiB repository review threshold |
| HP collector `OnSuccess` | Starts `lab-backup-r2.service` after successful local collection |
| HP `lab-backup-r2.timer` | Daily 03:00 Europe/Zurich; persistent retry |
| HP `lab-backup-r2-health.timer` | Hourly; copy and source-snapshot status within 26 hours |
| `lab-backup-alert.service` | Local journal and terminal notification; no external email |
| Retention | Union of 14 daily, 8 weekly, and 6 monthly snapshots; overlapping sets |

The collector requires at least five restored SQLite databases, a workload-specific acceptance threshold. Every local collection restores its new restic snapshot, verifies all transferred checksums, checks restored SQLite main files, and checks repository structure. Full local data reads run initially and on Sundays. Local pruning follows restore checks and is followed by another repository check.

R2 copying shares the collector lock. It checks cloud data before retention and repository structure afterward; a full data read runs initially and at least every seven days of successful execution. Hourly cloud health reads recorded status, not R2 itself. PostgreSQL restoration, complete SQLite/WAL recovery, and dashboard credential decryption are separate manual drills.

The R2 JSON schema is shared with the [HP automation reference](../../home-lab/reference/automation.md#credential-files). No R2 lifecycle deletion rule is configured. Retention is not an immutability guarantee.
