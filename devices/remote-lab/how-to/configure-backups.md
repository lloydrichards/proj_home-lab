# Configure Pi backups and an R2 copy

Use this guide to reproduce the installed Pi-to-HP backup path. You need trusted maintenance sessions on both hosts, the reviewed notebook checkout, Docker on remote-lab, and restic plus systemd on home-lab. The installers require the exact [lab-specific inputs](../reference/backups.md#hosts-identities-and-storage); adapt and review them before use elsewhere.

The supplied collector checks for at least five application SQLite databases, matching this lab's existing workload. A minimal new Pi may not meet that threshold; review and adapt the acceptance check before using the scripts there.

The first collection stops running Pi containers temporarily. Choose a maintenance window and pause deployments. To inspect existing backups without an outage, use [Check backups](check-backups.md).

## Prepare the restricted SSH identity

1. On home-lab as `lloyd`, create the private bootstrap directory:

```bash
	sudo install -d -m 700 -o root -g root \
		/home/coder/projects/proj_home-lab/local/backup-bootstrap
	sudo ssh-keygen -t ed25519 -N '' \
		-f /home/coder/projects/proj_home-lab/local/backup-bootstrap/id_ed25519 \
		-C lab-backup
```

If the identity already exists, retain it; do not overwrite it. The unattended job uses this unencrypted private key inside the protected backup account. Restrict the remote key to the HP source address and fixed command as the supplied installer does.

2. Transfer only `id_ed25519.pub` into `devices/remote-lab/backup-tools/` beside the installer on remote-lab. Keep the private key on home-lab.
3. On remote-lab as `lloyd`, install the reviewed source services:

```bash
	sudo bash /PATH/TO/NOTEBOOK/devices/remote-lab/backup-tools/install-remote.sh
	sudo systemctl status lab-backup-sshd.service
	sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Expect the restricted daemon active on TCP 2222. Retain the fingerprint from this trusted session for the next check.

4. On home-lab, collect the endpoint's public key into a candidate file:

```bash
	sudo sh -c 'ssh-keyscan -t ed25519 -p 2222 100.107.227.75 > /home/coder/projects/proj_home-lab/local/backup-bootstrap/known_hosts'
	sudo ssh-keygen -lf /home/coder/projects/proj_home-lab/local/backup-bootstrap/known_hosts
```

Stop unless the fingerprint matches the trusted Pi result. `ssh-keyscan` alone does not establish identity. The Tailscale policy must permit this HP-to-Pi port without granting general Pi administration.

## Install and verify the local collector

1. On home-lab as `lloyd`, run the reviewed installer during the agreed window:

```bash
	sudo bash /home/coder/projects/proj_home-lab/devices/remote-lab/backup-tools/install-home.sh
```

Expect its backup and restore checks to pass before timers are enabled. If it fails, inspect [collection and recovery state](check-backups.md#recover-an-interrupted-export) before retrying.

2. Verify Pi container recovery and the current application routes. Originally stopped containers must remain stopped.
3. Save `/home/lab-backup/credentials/restic-password` and the Pi's Coolify `APP_KEY` privately in your password manager. Confirm that you can retrieve them without either lab host. Do not paste the values into Git or chat.
4. After checking the installed identity and credential permissions, remove only the temporary bootstrap private key:

```bash
	sudo rm -- /home/coder/projects/proj_home-lab/local/backup-bootstrap/id_ed25519
```

Retain the installed key under `/home/lab-backup/credentials` and the source authorization. Removing bootstrap material must not remove the active identity.

## Add the off-site repository

1. Create a private Standard-class R2 bucket and a bucket-scoped Object Read & Write credential. Save its keys and endpoint in your password manager. [Cloudflare's S3 setup](https://developers.cloudflare.com/r2/get-started/s3/) describes the provider steps.
2. Store the [R2 JSON credential](../../home-lab/reference/automation.md#credential-files) privately as `/home/lab-backup/credentials/r2.json`, owned by `lab-backup`, mode 0600.
3. As `lab-backup`, initialize the `remote-lab` R2 repository with the existing restic password and copied local chunker parameters. Use the credential-loading pattern below; it does not print credentials:

```bash
	sudo -u lab-backup python3 - <<-'PY'
	import json, os, subprocess
	from pathlib import Path
	base = Path('/home/lab-backup')
	config = json.loads((base / 'credentials/r2.json').read_text())
	password = str(base / 'credentials/restic-password')
	env = dict(os.environ, HOME=str(base), AWS_DEFAULT_REGION='auto',
	    AWS_ACCESS_KEY_ID=config['access_key_id'],
	    AWS_SECRET_ACCESS_KEY=config['secret_access_key'],
	    RESTIC_PASSWORD_FILE=password,
	    RESTIC_REPOSITORY=f"s3:{config['endpoint']}/{config['bucket']}/remote-lab")
	subprocess.run(['restic', 'init', '--copy-chunker-params',
	    '--from-repo', str(base / 'repository'),
	    '--from-password-file', password], env=env, check=True)
	PY
```

Run `init` only for a new repository. If one already exists, verify it with its saved password instead of recreating it.

4. Install the reviewed cloud service:

```bash
	sudo bash /home/coder/projects/proj_home-lab/devices/remote-lab/backup-tools/install-r2.sh
```

Expect copy and health checks to pass. This installer does not trigger another Pi collection. Its service applies the reviewed 14-daily, 8-weekly, 6-monthly retention policy, including deletion of snapshots outside that policy.

5. Complete a [restore from the cloud copy](restore-backups.md#restore-from-r2) before relying on the schedule. Observe the next scheduled collection and cloud job separately from this manual success.
