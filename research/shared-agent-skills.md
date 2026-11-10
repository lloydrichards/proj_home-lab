# Shared agent skills across Mac and HP

Maintain authored skills and deliberate adaptations in the [skills source repository](https://github.com/lloydrichards/skills). The HP source is `/home/coder/projects/skills`; installed copies belong under `~/.agents/skills`. The [service register](../devices/_reference/services.md) owns the enabled profiles, installed versions, and last checked revision. The [sharing decision](../.okf/decisions/shared-agent-skills.md) explains the ownership and synchronization choices. Upcoming HP work belongs only in the [preparation checklist](../devices/home-lab/preparation.md).

## Source and installation boundaries

The source checkout contains `skills/`, `manifest.json`, `sources.lock.json`, and the `lab-skills` CLI. Keep maintained adaptations in source with attribution. Unchanged third-party content comes from pinned upstream commits and locked file hashes. Some pins are documented comparison baselines, not proven historical installation revisions.

Installed directories are generated copies. The installer records ownership, file hashes, modes, directory contents, and source identity. It refuses unowned destinations, symlinks, modified owned content, and interrupted-operation evidence. It has no force, adoption, or removal command. Git synchronization, authentication, shell configuration, and tool installation remain outside the CLI.

Keep Codex system skills, project skills, plugin/package skills, GitButler, and Rex with their existing managers. Use the single shared user root rather than parallel copies under Codex or OpenCode. The HP migration created no launcher, machine selection file, or shell configuration.

The source repository owns the current [installation instructions](https://github.com/lloydrichards/skills/blob/main/docs/install.md), [CLI contract](https://github.com/lloydrichards/skills/blob/main/docs/contract.md), [source synchronization](https://github.com/lloydrichards/skills/blob/main/docs/sync.md), and [manual recovery](https://github.com/lloydrichards/skills/blob/main/docs/recovery.md). Consult those before changing installer behavior. Optional profiles and deferred forks remain governed by that repository's manifest and decisions.

## Synchronize a source change

1. Edit maintained skills in the source checkout. Review the diff and attribution, run the relevant checks, then commit and publish through the repository's workflow.
2. On the other machine, inspect local source edits before fetching and integrating the reviewed commit. Use its normal Git or GitButler workflow. Do not reset or overwrite local work.
3. From `/home/coder/projects/skills`, validate the source and inspect the exact installation plan:

```sh
node packages/lab-skills/bin/lab-skills.mjs validate
node packages/lab-skills/bin/lab-skills.mjs plan --home /home/coder --profile default --profile effect --profile releases --profile mutation-audits --target agents
```

4. If the plan contains only the intended updates, apply and check the installation:

```sh
node packages/lab-skills/bin/lab-skills.mjs apply --home /home/coder --profile default --profile effect --profile releases --profile mutation-audits --target agents
node packages/lab-skills/bin/lab-skills.mjs status --home /home/coder --profile default --profile effect --profile releases --profile mutation-audits --target agents
node packages/lab-skills/bin/lab-skills.mjs doctor --home /home/coder --profile default --profile effect --profile releases --profile mutation-audits --target agents
```

Use the Mac's actual home and checkout paths there. These commands select the HP profiles explicitly and do not depend on machine configuration. Planning and status are offline and read-only. Apply recomputes its plan and verifies pinned payloads before changing destinations. Stop concurrent skill editors and installers during apply.

Preserve installed edits and incorporate them into reviewed source before attempting an update. Do not change ownership hashes to hide a conflict. Source revision alone does not trigger an unchanged local payload update; content hashes determine it. Upstream pin changes remain explicit updates.

## Recover an interrupted or unwanted installation

Run doctor and establish whether an installer is still running. Preserve the ownership state, journal, lock, and every stage or backup path it reports. Follow the source repository's recovery procedure to compare old and new directory inventories before restoring or completing a transaction. Do not delete a lock or backup based on age. Multi-directory installation is not crash-atomic.

For rollback after a successful installation, stop editors and installers, preserve any new edits, and compare installed content with its ownership records and the retained backup. Move only verified installer-owned entries to a private holding directory before restoring prior content. Preserve unrelated entries and shared parent directories. The CLI does not uninstall or adopt existing directories automatically.

The HP migration backup and private evidence remain in ignored `local/shared-skills-2026-11-10/` under the home-lab notebook checkout. The archive preserves symlinks and covers the inspected skill roots plus installer state, configuration, and launcher paths, including recorded absence. Its extracted inventory and checksum were checked before cutover. Authentication files and histories were excluded. This local rollback copy does not replace an off-machine workspace backup.

## Verified behavior and limits

On `home-lab` on 10 November 2026, the initial source at `c3c92c6` passed type checking, build, manifest validation, and all 73 CLI tests. Real temporary-home installation resolved 11 skills, preserved an unrelated skill, and supported repeat application. Planning created no target-home files. Modified owned content and an unowned destination both refused apply with exit 3 and retained their content.

The approved HP cutover installed only the selected shared root and ownership state. Fresh Codex 0.167.0 `skills/list` from `/tmp` found all 11 enabled with no discovery errors or matching duplicate names. Fresh OpenCode 2.2.6 catalog discovery also found all 11 after configuration initialization. If an immediate OpenCode catalog query shows only bundled skills, initialize configuration and query again before changing discovery roots. These checks establish discovery, not successful execution of every skill.

Lloyd reported the Mac migration and PRs #1–#4 complete, then confirmed the cross-machine update through [PR #5](https://github.com/lloydrichards/skills/pull/5). Both machines were clean at `927391b`; each planned and applied only the Effect update. Installed content hashes matched, all 11 skills were current, and repeat application left ownership state unchanged. Local HP checks independently confirmed clean `main` at `927391b32e5525c37ec7d32fc9ef964fc70a3b31` and all 11 current. The Mac checks, CI/merge result, cross-machine comparison, and repeated ownership-state comparison are user-reported.

Pi had no active installed runtime at HP inspection and was left alone. GitButler and Rex remain externally managed. The installer does not verify GitButler authentication or supply the external `but` skill, delegation support, or project test runners required by optional workflows. MCP-hosted skills remain deferred because native client loading was not established; no MCP skills service was deployed.

## SSH synchronization failures

The initial HP clone failed before connecting because OpenSSH rejected permissions on `/etc/ssh/ssh_config.d/20-omarchy-keepalive.conf`. An explicit empty SSH configuration and a temporary known-hosts file allowed cloning without changing machine configuration. Later cross-machine source integration succeeded, but that alone does not establish that the system configuration was repaired. If the error recurs, inspect the configuration permissions with the maintenance account or reuse a reviewed explicit configuration and verified host keys. Do not disable host verification.
