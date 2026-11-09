# Service register

HP updated from SSH inspection and user reports on 9 November 2026. Both Pis inspected over SSH on 9 November 2026.

| Service | Host | Access and dependencies | Evidence and gaps |
|---|---|---|---|
| Coolify | Pi 5 `remote-lab`, `192.168.8.142` | Dashboard TCP 8000; Docker cloudflared to Caddy `coolify-proxy:80` on network `coolify` | Coolify 4.7.2 observed during backup setup; tunnel 2026.10.3. Earlier public route repair passed. All 30 original containers running with none unhealthy after backup; local dashboard HTTP 302. See backup row. |
| Remote-lab backups | Pi source, HP destination | Restricted `lab-backup@100.107.227.75:2222`, only from HP `100.73.122.94`; HP account `lab-backup`, restic repository `/home/lab-backup/repository` | Installed 9 November: 02:00 Europe/Zurich, hourly freshness checks; 3 source generations and 14 daily/8 weekly/6 monthly snapshots. First encrypted backup/restore and four PostgreSQL restore tests passed. Local journal/terminal alerts only; password escrow and independent copy remain open. [Operations and scope](../remote-lab/backups.md). |
| Pi-hole | Pi 4 `admin-lab`, `192.168.8.138` | Dashboard `/admin/`; SSH as `lloyd` | Docker container healthy; DNS query to this host succeeded. Core v6.5, Web v6.6.1, FTL v6.8; Pi-hole DHCP disabled. Upstream DNS, network DHCP ownership, client configuration and backup unknown. |
| Pi 4 database and administration | Pi 4 `admin-lab` | PostgreSQL TCP 5432 and Portainer TCP 9000 listen on all IPv4 and IPv6 interfaces | Containers running; consumers, authentication and backups need review before restricting access. Native cloudflared observed activating; purpose unresolved. |
| Remote coding | HP `home-lab` | OpenSSH over Tailscale `100.73.122.94`, accounts `lloyd` and `coder`; LAN fallback `192.168.8.223` is DHCP | Tailscale connected; fresh key logins passed for both accounts. Key-only SSH; Tailscale SSH disabled. Monitor-free cold-start logins passed for both accounts on 9 November; overnight idle check pending. |

Applied hostnames are recorded in the [inventory](inventory.md#device-names).

OpenCode 2.2.6 was checked on the HP as `coder` over LAN SSH on 9 November 2026. Its background server listened only on `127.0.0.1:49374`; the terminal runs in tmux session `opencode`. No provider integrations are authenticated. See the [setup recipe](../home-lab/setup.md#opencode-on-the-installed-hp). In this setup session the execution environment could not resolve `home-lab` and SSH to `100.73.122.94` timed out; the LAN fallback worked. Earlier private-access checks remain historical evidence, not proof of current reachability from every client.

Codeburn 0.9.28 runs under `coder` via enabled `codeburn-share.service` (systemd user service; linger enabled). Its TCP 7777 listener is reached from the Mac through a local SSH tunnel managed by `local.codeburn.home-lab-tunnel` LaunchAgent; no direct 7777 firewall exception is needed. The Mac and HP combined report was checked after restarting both processes on 9 November 2026. Full reboot/login recovery and DHCP address stability remain untested. See the [setup recipe](../home-lab/setup.md#codeburn-usage-across-mac-and-hp).

## Next inspection

Hardware, OS and filesystem observations live in the inventory. Remote-lab backup and restore procedures are now recorded; resolve remaining recovery limits in the linked guide. For Coolify, inspect container names and images without dumping environment variables. For Pi-hole, establish backups, network DHCP ownership and DNS consumers before planning restarts or migration.

The Docker tunnel route is recorded below. Establish the native connector's purpose and whether Cloudflare Access protects administration. A tunnel alone does not establish application authentication. Keep tokens and populated tunnel configuration out of Git.

Before moving any service to the HP, record its data location, dependencies, backup, restore check, and rollback procedure. No migration has been selected.

## Pi tunnel recovery

On 9 November 2026, public apps failed while local app routes worked. `cloudflare-tunnel` was attached only to Docker `bridge`, so `coolify-proxy` could not resolve. Connecting it to `coolify` restored public routing. The connection survived a container restart; a full host reboot has not been tested. See the [recovery procedure](../remote-lab/coolify-cloudflare.md#verified-recovery).

Docker starts at boot and both tunnel and proxy use `unless-stopped`. The tunnel container was created 26 October 2026 without Compose ownership labels. Available evidence does not establish when or why its network attachment was omitted or removed. A separate host `cloudflared.service` is enabled and active; its tunnel purpose is unverified, so it was left unchanged. Boot logs show temporary DNS failures against the former `192.168.1.140` DNS address, followed by successful connection. Do not treat that historical failure as proof that current DNS is still wrong.

## Access cleanup

- Pi 4: Tailscale was absent. Installed 1.104.5 from the official stable Debian repository, enabled `tailscaled`, and requested login with `--ssh=false --accept-dns=false`. Account sign-in completed; fresh private SSH as `lloyd` passed at `100.122.53.80`. Keeping Tailscale DNS acceptance off avoids changing the DNS host resolver.
- Pi 5: Tailscale signed in at `100.107.227.75`. Its saved configuration enables Tailscale SSH; the login request preserved that setting. Private SSH passed after Lloyd completed the Tailscale identity check. Inspect its SSH policy and decide whether to retain it or use ordinary OpenSSH consistently. The existing Tailscale IP was retained after reauthentication.
- Both Pis: OpenSSH enabled and active. Effective Pi 4 settings disable password and keyboard-interactive authentication; Pi 5 enables both. Both allow root key login with `PermitRootLogin prohibit-password`, reported as `without-password` by `sshd -T`. Plan hardening only with a fresh second login and recovery access.
- HP: private SSH passed at `100.73.122.94` for both accounts. Node key expiry reported as 8 May 2027. Tailnet access-policy denial and off-LAN tests remain unverified.
- Pi 4 has four stopped legacy containers. Check ownership, volumes and backups before removal. Package installation reported 61 packages not upgraded; this pass did not perform a general OS upgrade.

Tailscale setup follows the [official installer](https://tailscale.com/download/linux/rpi). [Key expiry](https://tailscale.com/docs/features/access-control/key-expiry) needs an explicit server renewal plan. Sign-in URLs and credentials are not stored here.

## Pi hostname changes

On 9 November 2026, system hostnames changed from `raspberrypi` to `admin-lab` and from `homelab` to `remote-lab`. Pi 4 Tailscale DNS and fresh `ssh lloyd@admin-lab` passed. Pi 5 now advertises `remote-lab.tailc118cc.ts.net`, and a fresh `ssh lloyd@remote-lab` passed. LAN and Tailscale IPs stayed unchanged. Original `/etc/hostname` and `/etc/hosts` files were preserved on each host with suffix `.before-lab-rename`. No reboot was required. Existing external references to the old names may need updating.

## Private SSH access

For assistant maintenance from `coder` on home-lab, `tailscale ssh lloyd@remote-lab` passed on 9 November 2026. Tailscale handles host verification; this avoids the coding account needing Lloyd's SSH private key. The backup job uses its own pinned OpenSSH endpoint and key, described above.

Fresh connections from the Mac passed on 9 November 2026. Both Pis have `tailscaled` enabled and active. These checks used Tailscale while the Mac was on the LAN; off-LAN access and policy-denial checks remain open.

| Host | Command | Authentication |
|---|---|---|
| Pi 4 | `ssh lloyd@admin-lab` or `ssh lloyd@100.122.53.80` | Ordinary OpenSSH key; Tailscale SSH disabled |
| Pi 5 | `ssh lloyd@remote-lab` or `ssh lloyd@100.107.227.75` | Tailscale SSH, including an identity check when required |
| HP | `ssh lloyd@home-lab` or `ssh lloyd@100.73.122.94`; use `coder` for projects | Ordinary OpenSSH key; Tailscale SSH disabled. Both accounts tested by IP and hostname. |

All three reported node-key expiry on 8 May 2027. Choose a renewal policy before then. The existing Mac Ed25519 client key was imported into Lloyd's 1Password Personal vault as “Home lab SSH key — Lloyd Mac”. The local file remains in place; 1Password SSH-agent integration has not been configured or tested.


## T3 Code on home-lab

T3 Code 0.1.7 runs as `coder` in the active, enabled systemd user service `t3code.service`. Fresh LAN SSH checks on 9 November 2026 confirmed `Linger=yes` and a loopback-only listener at `127.0.0.1:3773`. Access is intended through an SSH environment over Tailscale, with LAN fallback. Mac connection, provider authentication, a real agent request and reboot recovery remain untested. See the [setup recipe](../home-lab/setup.md#t3-code-remote-environment).

Rex personal server installed for `coder` on 9 November 2026. Unix socket `/run/user/1001/rex/server.sock` is forwarded over LAN SSH to Mac `/tmp/rex-home-lab.sock`; host `home-lab` registered by the Mac Rex CLI. Native session `home-lab-opencode` startup and terminal capture passed. GUI access, linger and reboot startup remain incomplete. See the [Rex recipe](../home-lab/setup.md#rex-over-ssh).
