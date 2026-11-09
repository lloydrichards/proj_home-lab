# Back up remote-lab to home-lab

Installed and tested on 9 November 2026. This is an external backup workflow; Coolify's own backup schedules remain unconfigured. The [service register](../_reference/services.md) owns placement and access facts. Remaining HP backup work stays in the [preparation checklist](../home-lab/preparation.md#before-relying-on-important-work).

## What runs

home-lab's dedicated `lab-backup` account collects a backup every day at **02:00 Europe/Zurich**, including summer-time changes. `lab-backup-collect.timer` is persistent: a missed run starts when the HP returns. An hourly `lab-backup-health.timer` checks for a successful run within 26 hours, at least 20 GiB free, and repository growth beyond the 100 GiB review threshold. That threshold alerts; it is not a disk quota.

The collector uses ordinary OpenSSH over Tailscale to `lab-backup@100.107.227.75:2222`. A separate sshd listens only on that Tailscale address. Its pinned Ed25519 host key was obtained through authenticated Tailscale SSH. Only the dedicated public key, from home-lab's `100.73.122.94`, is accepted. Passwords, forwarding, PTYs and arbitrary commands are disabled. The backup account's restricted shell also blocks an alternate interactive session through Tailscale SSH on port 22. Its only sudo permission is the fixed exporter without arguments.

The home-lab account has no login shell and owns `/home/lab-backup`, mode 0700. The scripts are root-owned under `/usr/local/sbin/`. Its SSH identity, host-key pin and restic password live in `/home/lab-backup/credentials/`. `coder` cannot read this account's data or credentials. The temporary private bootstrap key under ignored `local/backup-bootstrap/` was removed after installing and checking the destination account; only its public key and host-key pin remain there.

## Consistency and scope

The exporter records which containers were running, stops all non-PostgreSQL containers, then dumps every running PostgreSQL cluster with its installed `pg_dumpall`. It also creates a custom-format `coolify.dmp`. It then stops PostgreSQL and archives the cold data. A 60-second grace period precedes Docker's forced stop if a container does not exit. The first stop/archive/restart sequence took **83.6 seconds**; application readiness can take longer.

The backup contains:

- All Docker volume `_data` directories, including inactive volumes.
- Existing regular bind-mount sources, excluding sockets such as `docker.sock`.
- `/data/coolify`, including `.env`, `APP_KEY`, deployment files, proxy data and SSH keys. `/data/coolify/backups` is excluded to avoid copying another backup tree.
- `/etc/ssh`, `/etc/hostname` and `/etc/hosts` for reference and recovery.
- Full private Docker container configuration, image IDs and environment values, including the container-based Cloudflare tunnel's recovery configuration.
- PostgreSQL logical dumps, a scope/timestamp manifest and SHA-256 checksums.

All originally running containers are restarted, PostgreSQL first. `ExecStopPost` retries recovery after an error, and `lab-backup-recover.service` handles a host reboot that interrupted a backup. A remaining `/var/lib/lab-backup-export/stopped.json` means recovery still needs attention. This recovery mechanism is installed; a power-interruption drill has not been performed.

The exporter keeps the latest **three successful generations** under root-only `/var/lib/lab-backup-export/`. Partial generations are never exported and are retained for diagnosis. Review them if repeated failures consume space. These local copies are plaintext and contain secrets.

home-lab verifies checksums and source freshness before creating an encrypted restic snapshot under `/home/lab-backup/repository`. Staging under `/home/lab-backup/staging/current` is private but plaintext on the HP's encrypted filesystem. Each run restores the new snapshot into a temporary private directory, verifies every transferred file, checks SQLite main database integrity, then removes that restore directory. SQLite WAL/SHM files remain in the complete data archive for real restoration. It performs a repository check daily and reads all repository data on the first successful run and each Sunday. Retention is **14 daily, 8 weekly and 6 monthly snapshots**, applied after successful restore checks; pruning is followed by another check.

This is not a full machine image. Container images and writable container layers are not archived. Custom apps must be rebuilt from their source; retain access to those repositories and the recorded image versions. The inspected custom server containers had no writable-layer changes. Native host cloudflared configuration outside mounted storage is not covered; its purpose remains unresolved. Neither host's Tailscale identity nor the HP's own workspaces are backed up by this job.

## Checks and first restore evidence

The first generation, `20261109T194742Z`, contained **611,997,440 bytes** (about 584 MiB). home-lab's collector and health service both exited successfully and both timers were enabled. The installer reported that repository restore, checksums and SQLite checks passed. All 30 originally running production containers were running afterward, none reported unhealthy, Coolify returned HTTP 302 locally, and no pending recovery state remained.

The additional [restore test](backup-tools/restore-test.py), installed as `/usr/local/sbin/lab-backup-restore-test` on remote-lab, restored all four PostgreSQL cluster dumps into disposable containers using their original image IDs. Tests used `--network none`, no published ports, temporary database storage, and removed the containers and anonymous volumes afterward. All cluster restores and database reads passed:

| Source | Restored databases |
|---|---|
| Coolify | `coolify`, `postgres` |
| Umami | `umami`, `postgres` |
| Custom app PostgreSQL | `ghost`, `postgres` |
| Other PostgreSQL container | `postgres` |

The separate Coolify custom-format dump also restored successfully. The archived `APP_KEY` decrypted a saved SSH private key from that restored database, without printing either secret. An additional isolated restore of **nine SQLite databases**, including accompanying WAL files where present, passed integrity checks. The private test log and result are `/var/lib/lab-backup-export/restore-test.log` and `restore-test.json`.

These checks establish database, credential and file recovery. They do not establish a full restored Coolify dashboard, end-to-end app UI behavior, or public DNS/tunnel cutover. The PostgreSQL and complete SQLite/WAL tests used the original off-machine generation's matching files retained on remote-lab; the restic restore/checksum test separately verified the copy on home-lab. PostgreSQL and complete SQLite/WAL restore tests are manual, not part of the nightly schedule.

## Operate and troubleshoot

Run these on home-lab in Lloyd's trusted maintenance terminal:

```bash
systemctl list-timers 'lab-backup-*' --all
sudo systemctl start lab-backup-collect.service
sudo journalctl -u lab-backup-collect.service -u lab-backup-health.service --since yesterday
sudo cat /home/lab-backup/last-success.json
sudo cat /home/lab-backup/last-failure.txt
```

`last-failure.txt` exists only after a failure and is removed by a successful collection. A timer being active does not prove a fresh backup. Check the last successful timestamp and service result. Alerts currently go to the system journal and logged-in terminals through `wall`; a deliberate alert test passed on 9 November after correcting argument quoting. Multiple broadcasts reflect multiple terminal sessions, not multiple failed backups. No email, push notification or independent outside monitor is configured. An unavailable HP cannot send its own alert.

Inspect or recover the source through the existing maintenance route:

```bash
tailscale ssh lloyd@remote-lab
sudo systemctl status lab-backup-produce.service lab-backup-sshd.service
sudo journalctl -u lab-backup-produce.service --since yesterday
sudo /usr/local/sbin/lab-backup-export recover
sudo /usr/local/sbin/lab-backup-restore-test
```

Do not deploy, upgrade or recreate containers during the maintenance window. Recovery refers to the container IDs recorded before stopping. If a container was replaced concurrently, inspect and reconcile it manually before deleting recovery state. Check service readiness and public app routes after recovery.

To pause scheduled backups on home-lab:

```bash
sudo systemctl disable --now lab-backup-collect.timer
```

This leaves existing copies intact. The hourly freshness check will alert once the last success becomes stale.

## Recover from home-lab

Use a private restore directory owned by `lab-backup`; do not extract the archive onto `/` or into a running application's volume. In a trusted maintenance terminal:

```bash
sudo -u lab-backup env \
  RESTIC_REPOSITORY=/home/lab-backup/repository \
  RESTIC_PASSWORD_FILE=/home/lab-backup/credentials/restic-password \
  restic snapshots --host remote-lab

sudo -u lab-backup env \
  RESTIC_REPOSITORY=/home/lab-backup/repository \
  RESTIC_PASSWORD_FILE=/home/lab-backup/credentials/restic-password \
  restic restore latest --host remote-lab --tag cold-backup \
  --target /home/lab-backup/manual-restore
```

The restored bundle is under `manual-restore/home/lab-backup/staging/current/`. Verify its `SHA256SUMS`. `postgres/*.sql` restores complete clusters, including roles; `postgres/coolify.dmp` restores only the Coolify database. Consult [Coolify's restore procedure](https://coolify.io/docs/core/backup-and-recovery/instance-restore), match the saved version, and supply the archived `APP_KEY` rather than blindly overwriting a replacement install's whole `.env`. `data.tar` contains the original relative paths; recover selected volume directories, including SQLite journal files, while their consumers are stopped. Preserve numeric ownership and match database versions. Review `containers.json` privately to map source paths to each container.

For a Pi replacement, use ARM-compatible images and restore the application files as well as the databases. Reconstruct Docker networks, the proxy and tunnel from the saved definitions before switching traffic. Restore only selected SSH material deliberately; archived host configuration is reference material, not a command to overwrite the replacement host.

The restic password must be saved outside home-lab. The saved `APP_KEY` should also be independently accessible. Keep both out of Git and chat. A trusted local terminal can read `/home/lab-backup/credentials/restic-password` with sudo for password-manager entry. Both machines are on the same premises, so this setup still needs an independent off-site or disconnected copy. Track these remaining actions in the HP checklist.

## Installation sources

[Backup scripts](backup-tools/) are the maintained installation sources. `install-remote.sh` expects the dedicated `id_ed25519.pub` beside it. `install-home.sh` expects the private key, public key and verified `known_hosts` under ignored `local/backup-bootstrap/` on first installation. Do not regenerate an installed identity casually; rotate both endpoints together. The installed collector is a root-owned copy, so editing the source does not change the running service.

The home installer requires sudo, installs restic, runs a manual backup and enables timers only after its checks pass. Re-running it normally also runs another backup and maintenance window. Use `install-home.sh --refresh-services` to copy reviewed collector/service updates without triggering a backup or changing timer activation. Preserve the existing repository password and identity. If the scripts change, validate them before copying replacements and repeat the relevant restore checks. `sudo systemctl start lab-backup-alert.service` tests the local alert independently of a backup.

Background references: [Coolify instance backup](https://coolify.io/docs/core/backup-and-recovery/instance-backup), [database backups](https://coolify.io/docs/databases/backups), [storage consistency](https://coolify.io/docs/core/persistent-storage/storage-mounts/backups), [Docker stop behavior](https://docs.docker.com/reference/cli/docker/container/stop/), [PostgreSQL cluster dumps](https://www.postgresql.org/docs/current/app-pg-dumpall.html), [restic verification](https://restic.readthedocs.io/en/stable/045_working_with_repos.html).
