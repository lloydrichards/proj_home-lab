# Service register

Current service placement, access boundaries, and verification limits. Observations span 9–11 November 2026; dates identify what was checked, not a promise of present reachability. Hardware lives in the [inventory](inventory.md). Procedures live in the linked device guides. The [HP preparation checklist](../home-lab/preparation.md) owns upcoming HP work.

## Services

| Service | Host and endpoint | Verified state and limits |
|---|---|---|
| Remote coding | `home-lab`; OpenSSH at `100.73.122.94:22` | Fresh key logins as `lloyd` and `coder`, including monitor-free cold startup, passed on 9 November. Overnight availability and AC-loss recovery remain untested. |
| Codex | `home-lab`, account `coder`; state under `~/.codex` | Codex 0.167.1 reopened one R2-restored conversation in an isolated profile on 11 November. The disposable profile was removed afterward. |
| OpenCode | `home-lab`, account `coder`; observed `127.0.0.1:49374` | Version 2.2.6 terminal startup and shared-skill discovery passed. Provider authentication and a model request remain untested. |
| T3 Code | `home-lab`, account `coder`; `t3code.service`, `127.0.0.1:3773` | Version 0.1.7 service active and enabled; `Linger=yes` checked on 9 November. Mac connection, provider request, and reboot recovery remain untested. |
| Rex | `home-lab`, account `coder`; `/run/user/1001/rex/server.sock` | Personal server, Mac CLI registration, SSH socket forwarding, OpenCode startup, and terminal capture passed on 9 November. Native remote-host GUI and reboot startup remain unverified. |
| Codeburn | `home-lab`, account `coder`; `codeburn-share.service`, TCP 7777 | Version 0.9.28 combined Mac/HP report passed on 9 November. Mac access uses an SSH tunnel, not a direct firewall exception. Reboot/login recovery remains untested. |
| Reports and previews | `home-lab`, account `coder`; private Tailscale HTTPS | Host-side report navigation, preview assets, APIs, secure WebSockets, live updates, and restart recovery passed on 10 November. Mac browser and full reboot checks remain unverified. [Publishing guide](../home-lab/publishing.md). |
| Shared skills | `home-lab`, account `coder`; source `/home/coder/projects/skills`, installed `~/.agents/skills` | Eleven selected skills and fresh Codex/OpenCode discovery passed on 10 November. Lloyd confirmed matching Mac/HP hashes. [Ownership and synchronization](../../research/shared-agent-skills.md). |
| Coolify | `remote-lab`; private dashboard TCP 8000, public `coolify.lloydrichards.dev` | Coolify 4.7.2; root deployment connection revalidated on 11 November. Public dashboard has Cloudflare Access; GitHub event delivery has a separate bypass. |
| Application tunnel | `remote-lab`; `*.lloydrichards.dev` to `http://coolify-proxy:80` | Docker cloudflared 2026.10.3 and Caddy routing restored. Full Pi reboot recovery remains untested. |
| Pi backups | Source `remote-lab`, collector `home-lab` | Nightly 02:00 Europe/Zurich collection; local encrypted history plus private R2 copy. Post-change collection and health passed at 09:09:20 CET on 11 November. [Scope and recovery](../remote-lab/backups.md). |
| Agent-state backups | `home-lab`; local repository and private R2 prefix `home-lab` | Local/cloud restores, SQLite checks, saved transcripts, and one Codex reopening passed on 11 November. Nightly 04:00 Europe/Zurich and hourly health timers enabled; next scheduled run remains unobserved. Projects/worktrees excluded. [Scope and recovery](../home-lab/agent-backups.md). |
| Pi-hole | `admin-lab`; LAN `192.168.8.138`, dashboard `/admin/` | Core v6.5, Web v6.6.1, FTL v6.8; DHCP disabled. DNS answered on 9–10 November. Lloyd reported browser access unavailable on 11 November and deferred investigation. Container health does not establish current DNS or browser behavior. |
| Pi 4 PostgreSQL | `admin-lab`; TCP 5432 on IPv4 and IPv6 interfaces | Container running at inspection. Consumers, authorization, and backups remain unknown. |
| Portainer | Both Pis; stopped | `restart=no` and exited confirmed on 11 November. Container, image, and `portainer_data` retained. |

## Private SSH access

All three hosts use ordinary OpenSSH over Tailscale; Tailscale SSH is disabled. Hostnames are applied system names, not just directory labels. The Mac's shortcuts use explicit Tailscale IPs because short-name resolution failed during setup. [SSH procedures](ssh-access.md) cover client configuration, host verification, and recovery.

| Host | Tailscale IPv4 | Recorded LAN fallback | Human accounts | Root SSH |
|---|---|---|---|---|
| `home-lab` | `100.73.122.94` | `192.168.8.223`, DHCP | `lloyd`, `coder` | Disabled |
| `remote-lab` | `100.107.227.75` | `192.168.8.142` | `lloyd` from the current Mac | Key-only access retained for Coolify |
| `admin-lab` | `100.122.53.80` | `192.168.8.138` | `lloyd` from the current Mac | Disabled |

Fresh Mac logins passed to all three hosts after the 10 November policy change. Both Pi `lloyd` authorization lists contain only the Mac Ed25519 key, `SHA256:RKoQsfwhQ/AFv1I/qqA/t5GtZoq+z598d0KhP6ttwMA`. The Mac file remains `/Users/lloyd/.ssh/id_ed25519`; Lloyd saved it in 1Password. 1Password SSH-agent integration remains untested.

The revoked `coder@home-lab` key is `SHA256:TzknGFpvGcV1aHASpwwyvHlLiFsc0SvNixGIlI+zOVM`. Fresh attempts offering it were rejected on both Pis over LAN and Tailscale. OpenSSH Ed25519 host fingerprints obtained through trusted maintenance sessions are:

| Host | Recorded host fingerprint |
|---|---|
| `admin-lab` | `SHA256:tS2z8+A4MDRegsC0MQ3Atwd34THAH5in5psMGlq8vQk` |
| `remote-lab` | `SHA256:QeSC9CxruLD01yEzAEAFQTUtjkuPJhcSdU3HkrreTWI` |

### Access cleanup

Password and keyboard-interactive SSH authentication are disabled on both Pis. Remote-lab's effective settings and fresh Mac key login passed after editing the main `sshd_config`; its inspected configuration had no active `Include`. Admin-lab's included `00-lab-no-root-login.conf` disables root SSH; its effective setting and fresh `lloyd`/sudo checks passed on 11 November. Remote-lab's separate backup daemon on port 2222 is unchanged.

The [recorded Tailscale policy](tailscale-policy.json) replaced the allow-all grant on 10 November. It allows selected Mac management ports, HP-to-Pi backup TCP 2222, selected client DNS to admin-lab, limited Pixel web access, and the existing Rex destination. It has no Tailscale SSH rules. Tests reached the backup endpoint and Pi-hole DNS, and denied sampled management connections from home-lab and remote-lab. The checks do not establish every IPv6 path, off-LAN behavior, or Rex/Pixel behavior.

LAN restrictions remain deferred. Home-lab retains its `192.168.8.0/24` SSH allowance; the Mac's observed `192.168.8.232` address is not reserved. LAN traffic is outside the Tailscale policy. All three nodes reported key expiry on 8 May 2027 at inspection.

### Pi maintenance permissions

`lloyd` uses password-required sudo and has no Docker-group membership in fresh Pi sessions. Fresh direct Docker access was denied while `sudo docker` remained usable. The intended per-terminal sudo cache is five minutes through `/etc/sudoers.d/90-lloyd-session`. Remote-lab's complete `visudo -c` passed; admin-lab's fresh-session behavior passed, but its full final validation output was not supplied.

Old sessions can retain prior supplementary groups. Recovery material remains root-only under `/root/lab-access-recovery`; removing an authorization does not delete its private key or recovery copy. [Permission checks and rollback](ssh-access.md#pi-maintenance-permissions) retain the commands.

## Security review verification and access boundary

| Identity or component | Current authority | Limit or remaining exposure |
|---|---|---|
| Current Mac | Sole authorized human maintenance key on both Pis; selected Tailscale management grants | A compromised Mac remains an administration risk. LAN restrictions are deferred. |
| `lloyd` | Host administration through password-required sudo | A privileged terminal has full host authority. |
| HP `coder` | Project and agent files, own user services, narrow publishing route helper | Shared account data is shared across agents. No general sudo or host Docker grant is recorded. Pi administrator key access is revoked. |
| Coolify deployment connection | Root SSH on remote-lab; revalidation passed on 11 November | Coolify compromise can control that host. |
| Remote-lab `coolify` account | Shell and authorized key retained; sudo and Docker-group membership removed on 11 November | Dependency review remains incomplete; old sessions can retain groups. |
| Caddy and Sentinel | Docker socket access retained | A read-only socket mount does not restrict Docker API methods. |
| Pi backup account | Dedicated SSH port 2222, HP source restriction, exact exporter sudo command | Exporter has host-wide data-read and container stop/start authority. |
| HP backup accounts and jobs | Private credentials and encrypted repositories; root-owned installed scripts | HP or Cloudflare account compromise can affect backup history. R2 credentials permit deletion. |
| Outlier runtime | Restricted `outlier_app` PostgreSQL role | Migration identity remains privileged. Build-secret handling is deferred. |

The removed remote-lab `coolify` sudo rule and prior groups are retained under `/root/lab-access-recovery/coolify-account-20261111T090600`. `visudo` passed; `id` showed only its primary group and `sudo -l -U coolify` denied sudo. All five observed UID-1001 processes mapped to containers, so their numeric UID overlap did not establish host-account automation.

The backup dispatch, restricted shell, exporter, sudo rule, key file, and parent directories were root-owned and not writable by ordinary users. Readback confirmed that only `SSH_ORIGINAL_COMMAND=export` reaches the fixed exporter without arguments, and the restricted shell accepts only that dispatcher invocation.

### Remaining security review scope

Lloyd deferred further network isolation, application build-secret changes, LAN firewall changes, Pi-hole access troubleshooting, and outside email alerts. Direct host-published application ports remain recorded exposure, not proof of public internet reachability. Full isolation is not established.

## Cloudflare route inspection

| Route or gate | Recorded configuration | Verification |
|---|---|---|
| Application tunnel | `homelab-apps`, wildcard `*.lloydrichards.dev` to `http://coolify-proxy:80` | Healthy dashboard route and public apps checked 10–11 November. |
| Old SSH tunnel route | `ssh.lloydrichards.dev` route and CNAME deleted | Cloudflare deletion confirmed. Native connector remains; process-to-tunnel identity and remaining purpose are unverified. |
| Coolify dashboard Access | Whole hostname, Allow only Lloyd's exact email, one-hour session | Private-window email-PIN gate passed. Private Tailscale dashboard access also passed. |
| GitHub events Access | Exact `/webhooks/source/github/events` path bypasses the browser gate | Anonymous Mac HTTPS ping POST returned HTTP 200 `pong`; signed event delivery and forged-event rejection remain untested. |

### Coolify GitHub integration

The connected source is GitHub App `coolify-lloydrichards`. Its webhook, homepage, authorization callback, and setup URL use HTTPS. The original webhook secret is retained and SSL verification is enabled. Coolify's authenticated Test Connection passed on 10 November. Callback wildcard disablement, OAuth callback completion, signed event delivery, and a Git-triggered deployment remain unverified. The ping handler responds before secret validation, so its successful response does not prove signature enforcement.

### Coolify instance URL and Caddy tunnel routing

The instance URL is `https://coolify.lloydrichards.dev` with `is_dashboard_force_https_enabled=false`. The generated Caddy site contains both explicit HTTP and HTTPS addresses, preserving the HTTP tunnel origin. Caddy routes `/app/*` to `coolify:6001`, `/terminal/ws` to `coolify:6002`, and other dashboard traffic to `coolify:8080`.

The proxy image is `lucaslorentz/caddy-docker-proxy:2.8-alpine`. Host configuration is under `/data/coolify/proxy/caddy/`; dynamic files are imported from `/dynamic/*.caddy`. [Redirect diagnosis and recovery](../remote-lab/coolify-cloudflare.md#dashboard-url-and-caddy-redirects) covers the HTTP 308 self-redirect failure. Generated proxy files were not patched.

## Pi tunnel recovery

The repaired Docker connector joins the management network so it can resolve `coolify-proxy`. Restart recovery passed after the repair on 9 November; full host reboot recovery has not been tested. Both tunnel and proxy use `unless-stopped`. [Tunnel recovery](../remote-lab/coolify-cloudflare.md#verified-recovery) owns the commands.

## Portainer retirement

Both standalone Portainer containers are exited with restart policy `no`. Their image and `portainer_data` volume remain. Retirement checks on 11 November showed other containers retaining their uptime and health. A post-backup check also showed remote-lab Portainer still stopped. [Container guide](../remote-lab/docker.md) provides the historical context; retirement did not delete application stacks or data.

## Plastic Map network separation

| Item | Current value |
|---|---|
| Destination and network | `slmpvttnyt4jqr0vtiuxiu82`, `plastic-map` |
| Production resource | `usshghmcrxppbbxp2ew3detq` |
| Original retained resource | `f008o0o84cog4wwogs0cwc8c`, stopped, manual deployments only |
| Production origin domain | `http://plastic-map.lloydrichards.dev`; public client uses HTTPS |
| Deployment settings | Production clone set to deploy on push; actual push delivery untested |

Inspection on 11 November showed only `plastic-map` and container port 3000 without a host mapping. Health and browser interaction checks passed after stopping the original. The clone changed source from `684f0cf54804e37ec0d3cba5aaacd76c2dbfb2df` to `933c810dbfefda37952234c08999515d73ddd5fa`; it was not a network-only redeployment. The proxy remains shared trusted infrastructure. Coolify destination cloning copies configuration, not persistent data.

## Outlier database permissions

Runtime application `jc0ocgkogko4k0ksgc88os0g` uses database `z84s8oc8wcg40c0os00w4ooc`, database name `postgres`. The `outlier_app` login has no superuser, database/role creation, replication, or row-security bypass privilege. It has database connection, public-schema usage, SELECT/INSERT/UPDATE/DELETE on public tables, and USAGE/SELECT on sequences. Defaults cover future public objects created by `postgres`, not other owners. Public-schema CREATE and drizzle-schema USAGE were false.

Separate checks confirmed all four table privileges on `blocks`, `events`, `speakers`, and `speakers_to_events`. TCP login, `postgres.js` using `outlier_app`, login, and editing passed before the destination move. The `postgres` password was rotated and its new TCP login passed; Lloyd confirmed matching saved Coolify and stopped migration-job credentials. Secrets are not recorded here. The build uses `NIXPACKS_NODE_VERSION=22`; build and start scripts are separate from migrations.

### Outlier destination move

| Item | Current value |
|---|---|
| Destination | `k5wbw4g56sy2u39vzxkzzwtq`, StandaloneDocker ID 5 on server ID 0 |
| Network | `outlier` |
| Application | `jc0ocgkogko4k0ksgc88os0g` |
| Database | `z84s8oc8wcg40c0os00w4ooc` |
| Migration job | `ikoo4occg4co8cks04ss0co0`, stopped |
| Data volume | `postgres-data-z84s8oc8wcg40c0os00w4ooc` at `/var/lib/postgresql/data` |
| Saved PostgreSQL image | `postgres:16-alpine@sha256:d898b0b78a2627cb4ee63464a14efc9d296884f1b28c841b0ab7d7c42f1fffdf` |
| Unused configuration clone | `mheytimuadz5autrfq2eey0l`, stopped, separate volume |

Lloyd moved the original resources in a guarded same-server metadata transaction after inspecting installed Coolify 4.7.2 code and creating private database/globals backups. This was outside the documented UI workflow. The original volume and image ID `sha256:e78e0659deab5c8d1d1c203f13424aac6d65c5451875422c51b45782497395eb` were retained. Queries found four public tables and one drizzle table; row-by-row comparison was not performed.

The application joined only `outlier` with no host port mapping. Correcting its saved `caddy_ingress_network` from `coolify` to `outlier` restored the public schedule after an initial HTTP 503. Post-move login/editing and the latest runtime-role readback were not separately supplied. The previous destination was StandaloneDocker ID 0. Private recovery archives remain under `/root/lab-access-recovery/outlier`; archive-list checks passed, not full restores of those particular archives.

## R2 off-site backup setup

Private Standard-class bucket `lloyd-lab-backups` contains separate `remote-lab` and `home-lab` repositories. Public access is disabled. Bucket-scoped Object Read & Write credentials are private under `/home/lab-backup/credentials/r2.json`; Lloyd saved them, the restic password, and Coolify `APP_KEY` in 1Password. Retrieval without either lab host remains untested.

| Backup | Schedule and retention | Verification |
|---|---|---|
| Pi collection | 02:00 Europe/Zurich; three source generations; local restic 14 daily, 8 weekly, 6 monthly | Initial file/SQLite checks, isolated restores of four PostgreSQL clusters, Coolify credential decryption, and post-hardening manual collection passed. |
| Pi R2 copy | After successful collection, daily retry at 03:00; 14 daily, 8 weekly, 6 monthly | Full cloud data check and eight restored file checksums passed. Initial copy/health services and retention update passed; future trigger and catch-up unobserved. |
| Agent-state backup | 04:00 Europe/Zurich; local and R2 14 daily, 8 weekly, 6 monthly | Both restores and health passed; one cloud-restored Codex conversation reopened. Future scheduled execution and catch-up unobserved. |

On 11 November at 09:09:20 CET, Pi collection and health services returned success after credential, destination, and account changes. All 30 listed production containers were running afterward, reported health checks were healthy, Portainer remained stopped, and no pending recovery marker existed. Lloyd subsequently confirmed the application checks were good.

R2 permits deletion through its installed credentials. The copy is off-site, not deletion-resistant. Outside email alerts are deferred; current alerts use the journal and terminal. An offline HP cannot send its own alert.

## Home-lab agent-state backups

The accepted scope includes Codex, OpenCode, T3, Rex session state, selected configuration, and shared-skill links. Projects and worktrees are excluded by Lloyd's choice; GitHub does not preserve uncommitted edits, unpushed commits, ignored project files, or local-only branches.

The installed root-owned job takes a temporary read-only Btrfs home snapshot, reads only allowed agent paths, restores and checks the local/cloud copies, and deletes its temporary snapshot. Original SQLite files remain untouched. The protected local repository is `/var/lib/lab-agent-backup/repository`; installed job and status paths are documented in [agent backup operations](../home-lab/agent-backups.md).

Lloyd restored R2 snapshot `0d6f779f367e7c430437a0f80820cca6a6c425dbc5481c18598c7d6c468c91cc`, verified 728 Codex files, and reopened conversation `01a1c158-cbd5-7b81-bcff-601dd9bfebe8` with Codex 0.167.1. His screenshot showed the original 9 November user message and assistant reply in an isolated test workspace. He confirmed closing the test and removing its private copy. This verifies one Codex reopening, not OpenCode/T3/Rex reopening, terminal-process recovery, or replacement-host authentication.

## Private development publishing

The recorded report index is `https://home-lab.tailc118cc.ts.net/reports/`. Runtime scripts are installed at `~/.local/lib/lab-publish/`; report content and allocation state are under `~/.local/share/lab-publish/`, outside Git. `lab-reports.service` serves loopback port 8379. The root-owned `/usr/local/sbin/lab-publish-route` helper has a narrow sudoers grant for `coder`; it permits only fixed report/preview route operations and rejects unrelated route removal and Funnel listeners.

Host-side checks on 10 November passed report search/filtering, canonical and immutable revision delivery, separate-worktree previews, API/module requests, WebSockets, live updates, service restart recovery, and exact cleanup. Mac browser and full reboot behavior remain unverified. Retired preview HTTPS allocations remain reserved.

The existing private HTTPS root handler points to `127.0.0.1:5173`; its inspected upstream had no listener and returned HTTP 502. Report-route installation preserved it. Published report content is outside the accepted agent-backup scope and has no verified backup.

## Next inspection

Unresolved service facts are Pi-hole browser/DNS behavior, the Pi 4 database's consumers and backup, native cloudflared connector purpose, and untested signed GitHub event delivery. Upcoming HP checks remain in the [preparation checklist](../home-lab/preparation.md). Historical recipes do not establish current deployment or recovery.
