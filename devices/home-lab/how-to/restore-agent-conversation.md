# Reopen a restored agent conversation

Use the maintenance terminal on home-lab. This procedure tests a Codex conversation from the last successful R2 backup without replacing live session data. The installed Codex CLI, backup script, credentials, and `/var/lib/lab-agent-backup/last-success.json` must exist.

For another machine or another agent, first review the [replacement-host limits](#recover-on-replacement-hardware). Do not treat this helper as a complete machine restore.

## Prepare the isolated profile

1. Run the maintained helper:

```bash
	sudo python3 /home/coder/projects/proj_home-lab/devices/home-lab/backup-tools/resume-test.py
```

Expect file verification to finish, followed by the restored snapshot ID, conversation ID, and an `open.sh` command. Stop if restoration or verification fails.

2. Run the exact `sudo -u coder -H .../open.sh` command printed by the helper.

The launcher uses a separate `CODEX_HOME`, no shared Codex daemon, read-only tool permissions, and an empty test workspace. The copied SQLite index points to the restored transcripts. Your live profile remains unchanged.

## Check the conversation

1. If Codex asks which working directory to use, keep the test workspace.
2. Confirm that both an old user message and its assistant reply appear. A login prompt or an empty conversation is not a successful reopening.
3. Exit without submitting a new model prompt. Record the snapshot, result, and any failure, without copying private conversation contents into the notebook.

One Codex conversation passed this test on 11 November 2026. Current verification and other agents' limits are in the [service register](../../_reference/services.md).

## Remove the test copy

After closing that Codex process, remove only the exact disposable directory printed by the helper. Replace `TEST_DIRECTORY` with that path under `/var/lib/lab-codex-resume-test/`:

```bash
	sudo rm -r -- TEST_DIRECTORY
```

The directory contains restored private history and file-based authentication. Keep the parent directory, repositories, and live profile intact.

If an older helper reports `open.sh: command not found`, inspect the root-owned parent permissions. `/var/lib/lab-codex-resume-test` must permit traversal with mode `755`; each coder-owned test directory remains mode `700`. Use the corrected helper for subsequent tests.

## Recover on replacement hardware

Before using the current-host helper on a replacement:

1. Retrieve the original R2 endpoint, bucket-scoped credentials, and restic password from the password manager.
2. Install compatible restic and agent versions. Recreate the coding account and protected recovery paths.
3. List the existing `home-lab` repository snapshots with those credentials. Select a verified `agent-state` snapshot rather than initializing over it.
4. Restore into a private staging directory. This standalone command uses the credential files from [credential preparation](back-up-agent-sessions.md#prepare-private-credentials-on-a-new-host), without the old host's installed script or success record:

```bash
	sudo python3 - <<-'PY'
	import json
	import os
	from pathlib import Path
	import re
	import subprocess

	os.umask(0o077)
	credentials = Path("/home/lab-backup/credentials")
	config = json.loads((credentials / "r2.json").read_text())
	env = dict(os.environ,
	    AWS_ACCESS_KEY_ID=config["access_key_id"],
	    AWS_SECRET_ACCESS_KEY=config["secret_access_key"],
	    AWS_DEFAULT_REGION="auto",
	    RESTIC_PASSWORD_FILE=str(credentials / "restic-password"),
	    RESTIC_REPOSITORY=f's3:{config["endpoint"]}/{config["bucket"]}/home-lab')
	subprocess.run(["restic", "snapshots", "--host", "home-lab",
	                "--tag", "agent-state"], env=env, check=True)
	print("Select a snapshot ID from the list: ", end="", flush=True)
	with open("/dev/tty") as terminal:
	    snapshot = terminal.readline().strip()
	if not re.fullmatch(r"[0-9a-f]{8,64}", snapshot):
	    raise SystemExit("Invalid snapshot ID; nothing restored.")
	target = Path("/var/lib/lab-agent-recovery")
	target.mkdir(mode=0o700)
	subprocess.run(["restic", "restore", snapshot, "--target", str(target),
	                "--verify"], env=env, check=True)
	print("Restored and verified into", target)
	PY
```

The destination must not already exist. The command never overwrites the live home. Stop if verification fails. Keep each SQLite database with its WAL and rollback journal files.

5. Map the saved `/var/lib/lab-agent-backup/home/coder` subtree to the replacement account's intended home. Keep destination agents stopped until ownership and path references are reconciled.
6. Clone omitted projects and skill-source repositories from GitHub at the paths required by restored links. Restore installed shared skills together with `.local/state/lab-skills` from the same snapshot. Run the skills installer's doctor before apply; preserve any journal, lock, stage, or backup evidence and follow [manual skill recovery](../../../research/shared-agent-skills.md#recover-an-interrupted-or-unwanted-installation). Older snapshots without ownership metadata need manual reconciliation, not automatic adoption of generated directories. Reauthenticate where needed.
7. Open an isolated copy before replacing the working agent profile.

This replacement-host sequence has not been tested end to end. The existing helper depends on local backup metadata and installed paths. OpenCode, T3, and Rex reopening need their own application checks; terminal-process recovery is outside this test. See the [backup explanation](../../../docs/explanations/backup-and-recovery.md) and [automation reference](../reference/automation.md).
