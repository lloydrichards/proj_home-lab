# Automation reference

This reference describes the maintained lab scripts and their installation contracts. Current deployment evidence and versions belong in the [service register](../../_reference/services.md). Hardware, disk identities, and device addresses belong in the [inventory](../../_reference/inventory.md).

## Installation contract

| Component | Required environment | Credential boundary |
|---|---|---|
| Agent backup | Hostname `home-lab`; account `coder`; Btrfs `/home`; restic, btrfs-progs, Python 3, findmnt, and systemd | Root-owned script reads protected files under `/home/lab-backup/credentials` |
| Pi collector on HP | Hostname `home-lab`; account `lab-backup`; restic and systemd; dedicated source SSH identity | `lab-backup` owns its private home, repository, and credentials |
| Pi R2 copy on HP | Existing Pi repository and collector unit; R2 credential file | Runs as `lab-backup` |
| Private publishing | Hostname `home-lab`; user `coder`; Bash, Python 3, jq, flock, Git, curl, systemd user services, and Tailscale CLI | Fixed root-owned route helper is the only publishing sudo exception |

The scripts contain lab-specific users, hostnames, paths, ports, source addresses, and repository prefixes. They are not parameterized new-hardware installers. Agent backup preflight requires `.codex/sessions` and `.local/share/opencode`; its restore checks require at least two SQLite databases and one readable Codex transcript.

## Credential files

`/home/lab-backup/credentials` is private. Its credential files have mode `600`; `r2.json` and `restic-password` are owned by `lab-backup`. Agent backup reads them as root. The coding account does not receive repository deletion credentials.

| File | Content |
|---|---|
| `restic-password` | One-line repository password; the local and corresponding cloud repositories use this password |
| `r2.json` | R2 endpoint, bucket, Access Key ID, and Secret Access Key |
| `id_ed25519` | Pi collector SSH identity; not needed by the agent-only job |
| `known_hosts` | Pinned source backup-SSH host key; not needed by the agent-only job |

The unpopulated R2 schema is:

```json
	{
	  "endpoint": "https://ACCOUNT_ID.r2.cloudflarestorage.com",
	  "bucket": "YOUR_PRIVATE_BUCKET",
	  "access_key_id": "YOUR_ACCESS_KEY_ID",
	  "secret_access_key": "YOUR_SECRET_ACCESS_KEY"
	}
```

The scripts append `remote-lab` for Pi snapshots and `home-lab` for agent snapshots. R2 Object Read & Write credentials permit deletion. This is an off-site copy, not immutable storage. Secret values and the original repository password are recovery inputs held outside both lab hosts.

## Installer effects

Paths below are relative to this repository.

| Installer | Account | Effects |
|---|---|---|
| `devices/home-lab/backup-tools/install-agents.sh` | root | Installs the agent script and units, runs the complete local/cloud backup and restore checks, then enables daily and hourly timers |
| `devices/remote-lab/backup-tools/install-home.sh` | root | Installs the HP Pi collector, runs a source cold backup with a Pi maintenance outage, checks recovery, then enables timers |
| Same installer with `--refresh-services` | root | Refreshes installed collector and service definitions without starting a backup or changing timer activation |
| `devices/remote-lab/backup-tools/install-r2.sh` | root | Installs cloud-copy script and units, adds the collector's `OnSuccess` dependency, runs cloud copying and health, then enables retry and health timers |
| `tools/publishing/install.sh` | `coder` | Replaces user runtime copies, enables and restarts `lab-reports.service`, and configures its private route if the helper exists |
| `tools/publishing/install-admin.sh` | root | Installs the fixed route helper and narrow sudoers exception, validates sudoers, and creates the private report route |

Editing repository source does not replace installed runtime copies. The agent and R2 installers do not provide a refresh-only mode.

## Agent backup interface

| Command or path | Meaning |
|---|---|
| `/usr/local/sbin/lab-agent-backup` | Complete snapshot, local backup, local restore, cloud copy, cloud restore, verification, and retention job |
| `/usr/local/sbin/lab-agent-backup health` | Checks the recorded last successful local/cloud verification against a 26-hour limit |
| `/var/lib/lab-agent-backup/repository` | Encrypted local repository |
| `/var/lib/lab-agent-backup/home` | Temporary read-only Btrfs home snapshot |
| `/var/lib/lab-agent-backup/backup.lock` | Prevents simultaneous agent-backup runs |
| `/var/lib/lab-agent-backup/last-success.json` | Successful snapshot identities and restore-check counts |
| R2 prefix `home-lab` | Separate cloud repository for host `home-lab`, tag `agent-state` |

The `last-success.json` fields are `completed_unix`, `local_snapshot`, `cloud_snapshot`, `local_checks`, and `cloud_checks`. Each check object has `sqlite_databases` and `session_transcripts`. A health success reads this record; it does not contact R2 again.

The maintained [agent script](../backup-tools/agents.py) owns the exact allowlist and exclusions. Its allowlist covers `.codex`, `.agents`, OpenCode configuration and state, `.t3/userdata`, `.t3/service.env`, and Rex state under `.local/state/rex`. Project roots, embedded worktrees, OpenCode project checkpoints, selected runtime controls, and Rex's Tailscale identity are excluded. The report store `~/.local/share/lab-publish` is outside this allowlist.

The job checks for 20 GiB free before starting. It preserves database journals from the filesystem snapshot, restores both repositories with restic file verification, and checks recovered SQLite integrity. It reads all cloud repository data each run. Retention keeps the union of 14 daily, 8 weekly, and 6 monthly snapshots, grouped by host and tag; repository checks follow pruning.

## Agent units and recovery helper

| Unit or helper | Schedule or interface |
|---|---|
| `lab-agent-backup.service` | Root oneshot with four-hour timeout and writable state restricted to `/var/lib/lab-agent-backup` |
| `lab-agent-backup.timer` | Daily 04:00 Europe/Zurich; persistent missed-run catch-up |
| `lab-agent-backup-health.service` | Recorded-success freshness check |
| `lab-agent-backup-health.timer` | Hourly |
| `lab-agent-backup-alert.service` | Local journal and logged-in-terminal alert |
| `backup-tools/resume-test.py` | Root helper; restores Codex from the saved successful cloud snapshot and prints a private launcher command |
| `/var/lib/lab-codex-resume-test/test-*` | Disposable coder-owned profiles; parent mode `755`, individual directories mode `700` |

The resume helper depends on the installed backup script, its success record, its credential paths, and the installed Codex executable path. It rebases the copied SQLite `threads.rollout_path` values. It omits saved hooks and connection settings, launches without the shared daemon, and uses an empty working directory with read-only tool permissions.

## Pi backup units on home-lab

| Unit | Schedule or interface |
|---|---|
| `lab-backup-collect.service` | Consistent source export, encrypted local backup, restore checks, and local retention |
| `lab-backup-collect.timer` | Daily 02:00 Europe/Zurich; persistent missed-run catch-up |
| `lab-backup-health.timer` | Hourly local freshness and capacity check |
| `lab-backup-r2.service` | Snapshot copy and cloud checks; starts after successful local collection |
| `lab-backup-r2.timer` | Daily 03:00 Europe/Zurich retry; persistent missed-run catch-up |
| `lab-backup-r2-health.timer` | Hourly copy/source-snapshot freshness check |
| `lab-backup-alert.service` | Local journal and terminal alert |

`/usr/local/sbin/lab-backup-r2 retention-preview` runs the agreed cloud policy with `forget --dry-run`. The source and cloud copy serialize through `/home/lab-backup/collector.lock`. Detailed source-export behavior and installation are in [Pi backup operations](../../remote-lab/backups.md).

## Publishing interfaces

The maintained [publishing scripts](../../../tools/publishing/) are installed under `~/.local/lib/lab-publish`. Data and reservation files live under `~/.local/share/lab-publish`; `lab-reports.service` serves the report store on loopback port `8379`.

| Script or helper | Interface |
|---|---|
| `publish-report.sh` | Publishes a report bundle; named options include `--source`, `--project`, `--name`, `--title`, `--summary`, and `--draft` |
| `start-preview.sh` | Allocates or resumes one worktree/service preview, with its saved command and optional environment/health settings |
| `preview-status.sh` | Shows all preview records or one preview ID |
| `stop-preview.sh` | Stops one exact preview, removes its route, and reserves its retired HTTPS allocation |
| `delete-report.sh` | Explicit report deletion interface |
| `/usr/local/sbin/lab-publish-route reports` | Adds `/reports/` on private HTTPS port `443` to loopback `8379` |
| Same helper with `preview HTTPS_PORT INTERNAL_PORT` | Adds a private preview route for HTTPS `8400–9999` to loopback `20000–29999` |
| Same helper with `stop HTTPS_PORT INTERNAL_PORT` | Removes that exact preview route |

The route helper rejects public Funnel listeners, collisions, invalid ranges, and unrelated handler removal. Its sudo rule does not grant arbitrary root commands. Preview allocation state rejects malformed or conflicting reservations. Retired external allocations are not recycled. The launcher allows the initial launch plus three retries, and route failure retains a pending allocation. [Publishing procedures](../publishing.md) own operation and cleanup.
