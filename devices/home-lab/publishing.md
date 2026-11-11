# Publish reports and run private previews

Use home-lab as `coder`. You need the notebook checkout, Bash, Python 3, jq, flock, Git, curl, systemd user services, and Tailscale. The Mac must have permission to reach the private HTTPS route.

Reports and preview records are outside Git and outside the accepted agent-backup scope. Keep another copy of content you need to recover. See [architecture](explanations/architecture.md) for the delivery path and [automation reference](reference/automation.md) for paths, flags, ports, and statuses.

## Install or update publishing

1. On home-lab as `coder`, install the reviewed runtime scripts:

```bash
	bash /home/coder/projects/proj_home-lab/tools/publishing/install.sh
```

2. On home-lab as `lloyd`, permit the coding account's user services to survive logout:

```bash
	sudo loginctl enable-linger coder
	loginctl show-user coder -p Linger
```

Expect `Linger=yes`. Check that private Tailscale HTTPS is enabled for this tailnet before installing the route helper. Complete any Serve/HTTPS enablement prompt through your trusted administration session; keep Funnel disabled.

3. Review and install the restricted route helper:

```bash
	sudo bash /home/coder/projects/proj_home-lab/tools/publishing/install-admin.sh
```

4. Open the private report index from the Mac using the hostname in the [service register](../_reference/services.md#private-development-publishing).

Expect the report index over HTTPS. Stop if installation would replace an unrelated route. Reinstall the administrator helper when its reviewed source changes; updating the checkout alone does not replace installed scripts.

## Publish a report

1. Prepare a directory outside Git with `index.html` and its companion assets. Remove secrets, raw machine output, symlinks, and special files.
2. On home-lab as `coder`, publish the bundle:

```bash
	bash ~/.local/lib/lab-publish/publish-report.sh \
		--source /absolute/path/to/prepared-report \
		--project YOUR_PROJECT \
		--name REPORT_TOPIC \
		--title 'Report title' \
		--summary 'What this report helps the reader decide.'
```

3. Open the returned canonical URL from the Mac. Check navigation and companion assets before sharing it.

Use `--draft` for a coherent report with unresolved questions. If delivery is pending, retain the bundle and diagnose the route; do not publish another report just to obtain a different URL.

To revise an existing report, read its ID and revision from `~/.local/share/lab-publish/state/reports.json`. Repeat publication with `--id REPORT_ID --expected-revision REVISION` and the normal bundle arguments. If another edit won, reconcile the retained staged copy before retrying. Share the canonical URL rather than an immutable revision URL.

## Run a preview

1. Keep the intended worktree and choose a distinct service name.
2. Start the app with a loopback listener and the allocated port. For Vite:

```bash
	bash ~/.local/lib/lab-publish/start-preview.sh \
		/absolute/path/to/worktree docs -- \
		bun run --cwd apps/docs dev --host 127.0.0.1 --port '{port}' --strictPort
```

3. Inspect its status:

```bash
	bash ~/.local/lib/lab-publish/preview-status.sh
```

4. Open its private URL from the Mac. Check assets, APIs, deep links, and live updates before calling it ready.

Use the app's actual bind options. Add `--health-path /health` before `--` if needed. For credentials, pass `--env-file /private/environment.json`; never put secret values in command arguments. If the app fails, fix it and repeat the same invocation. To change a saved launch command or environment deliberately, pass `--update` and the complete environment file again.

## Stop a preview or delete a report

Leave a preview running until explicitly stopped, or until its task is finished and its code is merged. Preserve its worktree while active.

```bash
	bash ~/.local/lib/lab-publish/stop-preview.sh PREVIEW_ID
```

Check every service, uncommitted edit, and unpushed commit before removing the associated worktree. Do not delete reservation records to reuse retired URLs.

Only after the user requests report deletion:

```bash
	bash ~/.local/lib/lab-publish/delete-report.sh --id REPORT_ID
```

Preview cleanup does not delete reports.

## Diagnose a failed link

On home-lab as `coder`:

```bash
	systemctl --user status lab-reports.service
	journalctl --user -u lab-reports.service --since today
	curl -I http://127.0.0.1:8379/
	bash ~/.local/lib/lab-publish/preview-status.sh PREVIEW_ID
```

If loopback works but private HTTPS fails, inspect the specific Serve route and tailnet grant. If HTTPS works on the HP but fails on the Mac, inspect the Mac's exact browser error, resolver, and route. Do not reset Tailscale, remove SSH access, or change Pi networking to repair a publication link.

Run the focused implementation checks after changing publishing code:

```bash
	python3 -m unittest discover -s tools/publishing/tests -v
```
