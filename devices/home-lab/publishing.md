# Private reports and development previews

Use these scripts on home-lab as coder. The maintained scripts are in `tools/publishing/`; installed runtime copies live in `~/.local/lib/lab-publish/`. They work from SSH, Codex, OpenCode, or a terminal. They require Bash, Python 3, jq, flock, Git, curl, systemd user services, and the installed Tailscale CLI.

Reports and preview records live outside Git under `~/.local/share/lab-publish/`. This store needs inclusion in the future HP workspace backup. Keeping content on this disk does not protect it from disk loss.

## Install and update

On home-lab as coder:

```bash
bash /home/coder/projects/proj_home-lab/tools/publishing/install.sh
```

This installs runtime copies and enables `lab-reports.service` on loopback port 8379. Existing user lingering enables boot startup without an interactive login. Installation does not reset Tailscale or replace the existing root HTTPS handler.

The one-time route helper requires administrator access. Review `tools/publishing/lab-publish-route` and `install-admin.sh`, then run on home-lab from the lloyd maintenance account:

```bash
sudo bash /home/coder/projects/proj_home-lab/tools/publishing/install-admin.sh
```

The helper is copied root-owned to `/usr/local/sbin/lab-publish-route`; the sudoers rule permits coder to invoke that helper. Its accepted operations add the fixed loopback report proxy, add a preview proxy in HTTPS ports 8400–9999 to loopback ports 20000–29999, or remove an exact preview proxy. It refuses collisions, public Funnel listeners, and unrelated handler removal. It does not run user-provided code or accept arbitrary paths or Serve configurations.

Reinstall the administrator helper after reviewing changes to that file. Updating the source checkout alone does not change the privileged runtime copy.

The report URL is `https://home-lab.tailc118cc.ts.net/reports/`. Private HTTPS delivery has been verified from home-lab, including report navigation and preview live updates. Verify the index from the Mac as a separate client check. Review effective tailnet policy if new ports are unreachable; adding a narrow rule does not cancel an existing broad allow. Do not change SSH, DNS, enrollment, or Pi services as part of publication setup.

## Publish a report

Prepare a directory outside all repositories with `index.html` and companion files. Remove secrets and private raw output first. Bundles cannot contain symlinks or special files.

```bash
bash ~/.local/lib/lab-publish/publish-report.sh \
  --source /absolute/path/to/prepared-report \
  --project stack-effect \
  --name graph-redesign-review \
  --title 'Graph redesign review' \
  --summary 'Compare the catalog layouts.'
```

Add `--draft` for a coherent report with open questions. The id uses the Europe/Zurich first publication date, repository name, and report topic. Include the topic when worktrees need distinction. The index searches title, project, and optional summary, and filters by project.

The script stores the complete bundle before checking private HTTPS delivery. Failure leaves the report in the store and returns pending delivery. A successful transport check compares the returned HTML with the published bundle. Verify companion files and browser behavior separately before sharing the canonical URL.

For a revision, read the current record from `~/.local/share/lab-publish/state/reports.json` before editing. Supply `--id EXISTING_ID --expected-revision EXISTING_REVISION` and the normal source, project, name, and title arguments. A stale revision preserves the draft under `staging/` and refuses to overwrite the winner. Reconcile conflicting edits before retrying.

Canonical links redirect to immutable release directories. Their relative assets remain tied to the same revision even during an update. Share the canonical URL, not the revision URL shown after redirect. Old release bundles remain available until explicit report deletion.

Only after the user explicitly requests deletion:

```bash
bash ~/.local/lib/lab-publish/delete-report.sh --id REPORT_ID
```

Deletion removes the report's releases and its index entry. Preview cleanup never deletes reports.

## Start and inspect a preview

Use a worktree root and a distinct service name. For a nested Vite app:

```bash
bash ~/.local/lib/lab-publish/start-preview.sh \
  /absolute/path/to/worktree docs -- \
  bun run --cwd apps/docs dev --host 127.0.0.1 --port '{port}' --strictPort
```

The literal `{port}` becomes the reserved internal port. Commands are stored as an argument vector, not evaluated shell text. Use the actual framework bind and port options. The launcher also sets PORT, LAB_PREVIEW_PORT, LAB_PREVIEW_URL, LAB_PREVIEW_HOST, and Vite's additional allowed hostname.

Use `--health-path /health` before `--` for another readiness endpoint. Use `--env-file /private/environment.json` for an explicit JSON object of string environment values. The script copies that file privately and stores the launch PATH. Do not place credentials in command arguments or Git.

Repeating the same worktree and service reuses its allocation and saved command. Repair a failed app, then repeat the invocation to start it and retry publication. Use `--update` before `--` to deliberately replace its saved command, environment, and health path without changing the allocation. Supply the complete environment file again when updating.

```bash
bash ~/.local/lib/lab-publish/preview-status.sh
bash ~/.local/lib/lab-publish/preview-status.sh PREVIEW_ID
```

Each record identifies one worktree and service. The script checks that the service owns its loopback listener before adding a private route. It verifies the HTTPS readiness endpoint before returning a ready link. The agent must still check required APIs, assets, browser origins, deep links, and live updates. Internal dependencies do not need browser URLs.

Once the route helper is installed, the launcher removes its route on process exit and restores it after readiness on startup. Internal allocations stay reserved while failed.

The launcher permits an initial launch and three retries, then exits failed. It does not automatically reset the failure budget for a long-running process. An explicit restart after repair starts a new budget. A running process with failed HTTP readiness is not a working preview. Every activation first clears saved readiness. A service-start or local-readiness failure records failed; route or HTTPS failure records publication-pending and last_error, retaining the same allocation. Runtime status is kept beside the allocation and recent output is in the user journal.

## Stop and clean up

Leave a preview running until explicitly stopped, or until its task is finished and its code is merged. Both conditions are required. Cleanup is agent-driven, not a background merge watcher.

```bash
bash ~/.local/lib/lab-publish/stop-preview.sh PREVIEW_ID
```

The script removes the private route before disabling the unit. When no external route exists, it can stop an unpublished service without administrator access. It retains the retired HTTPS allocation permanently. Ports 8400–9999 provide at most 1,600 lifetime allocations before exclusions. Exhaustion stops allocation rather than recycling an old URL. Extend the reviewed range deliberately if needed. Before allocation or reuse, the launcher parses all reservation files and validates ports, statuses, and uniqueness. Malformed JSON, invalid fields, duplicate HTTPS reservations, or duplicate active internal ports block the operation without changing reservations. Preserve corrupt records for ownership repair rather than deleting them to free a URL.

Keep an active preview's worktree. Before deleting a finished, merged worktree, check all its services, uncommitted files, and unpushed commits. Stop the exact services, then remove the checkout with its owning worktree tool. Reports remain available.

## Diagnose failures

For reports, inspect `systemctl --user status lab-reports.service`, `journalctl --user -u lab-reports.service`, and `curl -I http://127.0.0.1:8379/`. Inspect Serve routes separately. A configured route can outlive its upstream process.

A sandbox-denied Tailscale socket does not prove the daemon is stopped. Use the harness's normal permission mechanism for host access. If HTTPS works from the server but fails on the Mac, inspect the exact browser error and test the Mac resolver and routing separately. A Mac-side curl --resolve check preserves certificate verification while bypassing DNS. Use the actual preview port. A hosts-file change is a deliberate fallback, not the first automatic fix.

Run focused checks from the repository:

```bash
python3 -m unittest discover -s tools/publishing/tests -v
```

The tests use temporary stores and local HTTP sockets. Local socket restrictions can require running through the harness's approved host access. They do not change Tailscale routes or installed services. Reboot recovery remains unverified until a coordinated reboot is tested.
