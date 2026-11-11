# Restore Pi application data

Use home-lab as `lloyd` to recover a private backup bundle. Keep the live Pi and application volumes unchanged until the recovered data has passed checks. You need restic, the original repository password, and access to the selected repository.

For scope and file names, use the [backup reference](../reference/backups.md). These steps recover data; a full replacement Pi and public-route cutover have not been tested end to end.

## Restore from the local repository

1. List available snapshots on home-lab:

```bash
	sudo -u lab-backup env \
		RESTIC_REPOSITORY=/home/lab-backup/repository \
		RESTIC_PASSWORD_FILE=/home/lab-backup/credentials/restic-password \
		restic snapshots --host remote-lab --tag cold-backup
```

2. Select the snapshot ID and a new private destination. Replace `SNAPSHOT_ID` and `NEW_RESTORE_DIRECTORY`:

```bash
	sudo -u lab-backup env \
		RESTIC_REPOSITORY=/home/lab-backup/repository \
		RESTIC_PASSWORD_FILE=/home/lab-backup/credentials/restic-password \
		restic restore SNAPSHOT_ID --target NEW_RESTORE_DIRECTORY --verify
```

Use a destination beneath `/home/lab-backup`, not an existing application volume. Expect restic verification to pass before using the data.

## Restore from R2

On the installed home-lab, the following restores the newest cloud Pi snapshot into a new private directory and verifies its transferred checksums. It requires the installed R2 script and its protected credentials:

```bash
	sudo -u lab-backup python3 - <<-'PY'
	import os, runpy, subprocess, tempfile
	from pathlib import Path
	os.umask(0o077)
	tool = runpy.run_path('/usr/local/sbin/lab-backup-r2', run_name='restore_helper')
	env = tool['environment']()
	target = Path(tempfile.mkdtemp(prefix='pi-cloud-restore-', dir='/home/lab-backup'))
	subprocess.run(['restic', 'restore', 'latest', '--host', 'remote-lab',
	    '--tag', 'cold-backup', '--target', str(target), '--verify'], env=env, check=True)
	bundle = target / 'home/lab-backup/staging/current'
	subprocess.run(['sha256sum', '--check', 'SHA256SUMS'], cwd=bundle, check=True)
	print(f'Verified private restore: {bundle}')
	PY
```

Expect all checksums to pass. Keep the printed directory private and retain it until application recovery is verified. If you need an older snapshot, select its exact ID rather than `latest`.

On a replacement collector, first reconstruct the protected credential files and install compatible restic. Use their endpoint, bucket, and `remote-lab` prefix to list and restore the existing repository. Do not initialize over the surviving repository. The [R2 credential pattern](configure-backups.md#add-the-off-site-repository) shows how to load credentials without exposing them in command arguments.

## Check the recovered bundle

1. Read `manifest.json` for source identity and capture time.
2. Inspect `containers.json` privately to map original volumes, bind mounts, networks, and image IDs.
3. Match database major versions and machine architecture before restoring PostgreSQL. The Pi's recorded images are ARM-compatible; an x86 replacement needs matching images for that architecture.
4. Restore databases into isolated disposable instances before targeting production. Keep those instances off the network and without published ports.
5. Restore selected application files from `data.tar` while their destination consumers are stopped. Preserve numeric ownership and SQLite journal files. Do not extract the whole archive onto `/`.
6. Restore Coolify with its matching database dump and original `APP_KEY`, following its [instance restore procedure](https://coolify.io/docs/core/backup-and-recovery/instance-restore). Do not overwrite a replacement's complete `.env` blindly.

The manual [restore-test script](../backup-tools/restore-test.py) tested PostgreSQL clusters, SQLite/WAL recovery, and a saved Coolify credential on remote-lab. It reads the source's retained `latest` generation and depends on original images plus the running Coolify PHP runtime. It does not automatically test an arbitrary cloud-restored bundle or rebuild a lost Pi.

## Reconnect applications

Recreate the required networks, proxy, tunnel, and application definitions from the reviewed recovery data. Keep the replacement off production routes until local readiness, database access, browser login, and editing pass.

Switch public routing only after those checks. Retain the old host and verified bundle for rollback. Verify application behavior after the switch; a healthy container is not a complete browser test. Restore SSH material deliberately rather than copying the archived host configuration over a new machine.
