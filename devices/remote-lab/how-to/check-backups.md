# Check Pi backups and recover a failed run

Use home-lab as `lloyd` to inspect the collector. Use remote-lab as `lloyd` to inspect container recovery. The [backup reference](../reference/backups.md) lists units, scope, thresholds, and status files.

## Inspect the last result

On home-lab:

```bash
	systemctl show lab-backup-collect.service lab-backup-health.service \
		lab-backup-r2.service lab-backup-r2-health.service \
		-p Id -p LoadState -p Result -p ExecMainStatus -p ExecMainExitTimestamp
	systemctl list-timers 'lab-backup-*' --all
	sudo journalctl -u lab-backup-collect.service -u lab-backup-r2.service --since yesterday
```

Expect loaded units, successful results, exit status 0, and timestamps matching the intended run. An empty timestamp or an active timer does not prove a successful backup.

If needed, read the private `last-success.json` and `r2-last-success.json` under `/home/lab-backup`. Check completion time and source freshness. Do not publish full backup metadata or archive contents.

## Run a manual check

For a cloud copy without stopping Pi containers, on home-lab:

```bash
	sudo systemctl start lab-backup-r2.service
	sudo systemctl start lab-backup-r2-health.service
```

For a new Pi collection, first pause deployments and choose a maintenance window. Then run on home-lab:

```bash
	sudo systemctl start lab-backup-collect.service
	sudo systemctl start lab-backup-health.service
```

This collection stops and restarts the Pi's originally running containers. Check the result and the application's browser routes afterward. Outside email alerts are not configured.

## Recover an interrupted export

On remote-lab:

```bash
	sudo systemctl status lab-backup-produce.service lab-backup-sshd.service
	sudo journalctl -u lab-backup-produce.service --since today
	sudo docker ps -a --format '{{.Names}} | {{.Status}}'
	sudo test ! -e /var/lib/lab-backup-export/stopped.json
```

The final command succeeds when no pending marker exists. If a marker remains, ensure no collection or deployment is active, then run:

```bash
	sudo /usr/local/sbin/lab-backup-export recover
```

Inspect containers and application routes again. If container IDs changed during export, reconcile them manually before deleting recovery state. Do not restart every stopped container: some resources are intentionally retired or stopped.

## Pause or update collection

To pause the nightly Pi outage, on home-lab:

```bash
	sudo systemctl disable --now lab-backup-collect.timer
```

Existing snapshots remain. The independent freshness check will become stale; cloud retries do not create fresh source data.

To refresh reviewed collector code and units without another outage, obtain the exporter overlay IPv4 address from the private inventory. Substitute it below. This provisions the address file required when upgrading an older installation:

```bash
	sudo env BACKUP_EXPORTER_IP="<EXPORTER_OVERLAY_IPV4>" bash /home/coder/projects/proj_home-lab/devices/remote-lab/backup-tools/install-home.sh --refresh-services
```

The installer validates the address before replacing collector code. If `BACKUP_EXPORTER_IP` is omitted, it requires a valid existing `/home/lab-backup/credentials/remote-ip`. Missing or invalid input stops the refresh before changes.

Preserve the installed key and password. Re-enable the collection timer deliberately when ready:

```bash
	sudo systemctl enable --now lab-backup-collect.timer
```

## Preview cloud retention

On home-lab:

```bash
	sudo -u lab-backup /usr/local/sbin/lab-backup-r2 retention-preview
```

Expect a keep/remove plan with no deletions. Review that plan before changing retention policy or invoking pruning manually.
