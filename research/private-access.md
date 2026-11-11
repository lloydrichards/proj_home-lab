# Private access for the HP home lab

Sources checked **2026-11-06**. This is a proposed configuration, not evidence that the HP or tailnet has been configured. Commands were checked against documentation; they have not been run on the new server. Replace example usernames, addresses and account identities before use.

## How this research is used

The [private-development choice](../.okf/decisions/home-lab/private-development.md) owns the proposed access approach and its rationale. Upcoming setup and checks belong in the [HP checklist](../devices/home-lab/preparation.md). The examples below explain the relevant mechanisms; adapt them when we perform the setup.

## OpenSSH over Tailscale versus Tailscale SSH

OpenSSH over Tailscale uses Tailscale for connectivity and OpenSSH keys for login. Tailscale SSH instead intercepts tailnet connections to TCP 22 and uses tailnet identity plus separate `ssh` policy rules. It leaves the ordinary OpenSSH configuration unchanged for non-tailnet connections. Switching modes can disrupt current SSH sessions; establish local-console or independent recovery access first. [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh), [SSH over Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale)

Keep the built-in Tailscale SSH server off for this baseline. If it was enabled, change it only from a recovery session after confirming OpenSSH is installed and running:

```sh
sudo tailscale set --ssh=false
```

As of this check, Tailscale's October 28 security update fixes Tailscale SSH privilege-boundary issues and Serve/Funnel issues in **1.104.4**. Use the current stable package, at least that version. This advisory does not establish that ordinary OpenSSH over Tailscale has the same vulnerabilities. [Vendor security update](https://tailscale.com/blog/tailscale-ssh-findings-fixes)

### Pending Tailscale maintenance

On **9 November 2026**, the [stable package registry](https://pkgs.tailscale.com/stable/?mode=json) was rechecked and reported **1.104.5**. This is a maintenance target, not a new host observation. The inventory records HP **1.104.2-1**; Pi 4 already records **1.104.5**. Pi 5 uses Tailscale SSH but its installed version is unknown, so check it first and prioritize remediation if below **1.104.4**. HP Tailscale SSH is disabled; the advisory does not prove that HP OpenSSH is vulnerable.

For a separately authorized maintenance window:

1. Check `tailscale version` and `tailscale status` on each host. Keep an independent LAN SSH session and console recovery available.
2. On HP, use `omarchy update` on the stable channel, not a direct package replacement or partial Arch upgrade. Inspect the resulting version. If its curated channel does not yet provide at least **1.104.4**, stop and review the supported security-update path rather than bypassing Omarchy's updater.
3. On Debian Pis, inspect `apt-cache policy tailscale` and use the configured official stable repository during approved package maintenance. Do not change SSH mode, DNS acceptance or enrollment as part of a version update.
4. Recheck version, connectivity and a fresh private SSH login from a second terminal before closing recovery access. Record actual resulting versions only after those checks.

This notebook review updated no hosts. The HP action remains in the [readiness checklist](../devices/home-lab/preparation.md).

## Lockout-safe setup order

1. Keep a keyboard/display available on the HP. Keep the current working session open throughout changes. Do not run `tailscale down`, `logout`, `up --reset`, force reauthentication, firewall resets or a mode switch through the only remote connection.
2. Install/update packages through the normal Omarchy update path. Arch provides `openssh` and `tailscale`; their services are `sshd.service` and `tailscaled.service`. Set up the intended non-root account and its laptop public key before disabling password login. Keep the private key on the laptop. [Arch OpenSSH](https://wiki.archlinux.org/title/OpenSSH), [Arch Tailscale](https://wiki.archlinux.org/title/Tailscale)
3. From the HP console, start the services and authenticate Tailscale if needed:

   ```sh
   sudo systemctl enable --now sshd.service tailscaled.service
   sudo tailscale up
   tailscale version
   tailscale status
   tailscale ip -4
   ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
   ```

   `tailscale up` is for initial enrollment; do not rerun it to reset an existing configuration. Compare the HP's displayed SSH host-key fingerprint with the laptop's first connection. [Tailscale CLI](https://tailscale.com/docs/reference/tailscale-cli), [OpenSSH client manual](https://man.openbsd.org/ssh)

4. From a **second laptop terminal**, verify key-only login using the actual HP Tailscale address or MagicDNS name:

   ```sh
   ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no USER@HP_TAILSCALE_IP
   ```

5. Configure and preview the intended tailnet policy. Confirm a new login still works before restricting LAN access or changing OpenSSH authentication. Back up each configuration before editing it. Validate SSH syntax before reload:

   ```sh
   sudo sshd -t
   sudo systemctl reload sshd.service
   ```

   A nonzero syntax check means stop and fix the file before reload. Inspect `sudo sshd -T` for effective options; files and `Match` blocks can change the result. Suitable baseline options are `PermitRootLogin no`, `PubkeyAuthentication yes`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `AllowAgentForwarding no`, and `X11Forwarding no`. Preserve local TCP forwarding for development tools. [OpenSSH server configuration](https://man.openbsd.org/sshd_config)

6. Test from the laptop over an external network, then test a reboot while console recovery remains available. Disk encryption and sleep can prevent Tailscale from returning even when networking is configured correctly.

## HTTP access and SSH forwarding

Start an agent server with its application's explicit loopback bind option. Confirm its listening address with `ss -lntup`; a listener on `0.0.0.0` or `[::]` is not loopback-only. From the laptop:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:3000:127.0.0.1:3000 USER@HP_TAILSCALE_IP
```

Open `http://127.0.0.1:3000` on the laptop. The first address is the laptop listener; the second is the HP's destination. This needs `AllowTcpForwarding local` or `yes` on OpenSSH. A `PermitOpen` restriction can narrow destinations, but may break remote editor ports, so apply only after identifying the required ports. Disabling forwarding is not a sandbox for a user with shell access. Avoid `ssh -A`: someone controlling the remote agent socket can authenticate with identities loaded in the laptop agent. [OpenSSH client](https://man.openbsd.org/ssh), [OpenSSH forwarding controls](https://man.openbsd.org/sshd_config)

## Optional private HTTPS with Serve

For an existing HTTP service on HP loopback port 3000:

```sh
tailscale serve --bg 3000
tailscale serve status
tailscale funnel status
```

`--bg` persists sharing through terminal closure and restarts. Follow the printed setup link if HTTPS has not been enabled. The reported URL must say it is available within the tailnet; verify no Funnel is active. To remove this HTTPS listener:

```sh
tailscale serve --https=443 off
```

Serve is tailnet-private, but the default allow-all policy makes it reachable by every permitted tailnet device. Funnel is public internet exposure; it is disabled by default and should stay disabled here. Do not substitute `funnel` for `serve`. [Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve), [Private Docker service tutorial](https://tailscale.com/docs/solutions/host-private-server-docker), [Funnel](https://tailscale.com/docs/features/tailscale-funnel)

## Tailnet policy and device identity

Tailscale recommends grants for new policy. A default tailnet is not automatically least privilege: it commonly allows all tailnet traffic. Adding a narrow grant does not cancel an existing broad allow. Review existing ACLs and grants together, preview the result, and retain unrelated rules needed by the Pi and other devices. [ACL defaults](https://tailscale.com/docs/features/access-control/acls), [Migration and preview](https://tailscale.com/docs/reference/migrate-acls-grants)

Example to adapt in the policy editor, not a replacement for the whole existing policy:

```json
{
  "tagOwners": { "tag:home-lab": ["OWNER_LOGIN"] },
  "grants": [
    {
      "src": ["OWNER_LOGIN"],
      "dst": ["tag:home-lab"],
      "ip": ["tcp:22", "tcp:443"]
    }
  ]
}
```

Use the actual identity-provider login in place of `OWNER_LOGIN`. Omit 443 if using only SSH tunnels. Assign the server tag only after defining its owner and incoming grant. User identity as source permits that user's eligible devices, not only one laptop; use a reviewed device-specific selector if that distinction matters. No `ssh` rule is required for ordinary OpenSSH. [Grant examples](https://tailscale.com/docs/reference/examples/grants)

For the always-on HP, review node-key expiry in the admin console. Node keys normally expire after 180 days; tagged-device expiry defaults to disabled. Changing an existing device's tags does not itself change expiry without reauthentication. An enrollment auth key's expiry is separate and does not immediately expire enrolled devices. Prefer interactive enrollment or a one-use key rather than storing a reusable key in the repository. [Auth keys and expiry](https://tailscale.com/docs/features/access-control/auth-keys)

## Firewall and Docker

Use the existing host firewall to deny unsolicited non-tailnet incoming services, including IPv6. Preserve Tailscale's own network rules. Do not paste Ubuntu firewall-reset instructions into Omarchy or assume UFW alone filters tailnet traffic: Tailscale manages its own netfilter rules, and grants are the tailnet authorization layer. Validate LAN denial and laptop tailnet access independently. [Tailscale firewall guidance](https://tailscale.com/docs/how-to/secure-ubuntu-server-with-ufw)

Docker published ports can bypass UFW. Publish application ports explicitly on loopback, for example Compose:

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

Keep databases un-published on their private Docker network when only containers need them. Do not use `network_mode: host` for this isolation pattern. Do not disable Docker's firewall management to solve exposure. Use Docker Engine **28.0.0 or newer**; older versions have a documented same-LAN exception to localhost publishing. Audit `docker ps` port mappings as well as host sockets, then try the service from another LAN machine and an unauthorized tailnet device. [Docker firewall behavior](https://docs.docker.com/engine/network/packet-filtering-firewalls/), [Publishing ports and localhost caveat](https://docs.docker.com/engine/network/port-publishing/)


## Device access policy, 10 November 2026

Lloyd supplied the active policy showing an unrestricted `*` to `*` grant and Tailscale SSH check access from members to their own devices. He agreed to replace broad connectivity with device-specific access and give the Pixel private web/report access without SSH administration. This is user-supplied policy evidence, not a live console read.

The [device policy](../devices/_reference/tailscale-policy.json) was shown as eight matching grants in Lloyd's Tailscale console screenshot after replacement. The general-access view does not independently show the saved IP sets, SSH section or test results. Live home-lab checks below establish partial enforcement. Device names, IPv4/IPv6 addresses, tags and online status were read from home-lab's Tailscale peer view on 10 November. The Mac is `Lloyd's Mech`, `100.65.0.2`; the separate identities are `lloyds-mech-rex`, `100.76.12.16`, and `home-lab-rex`, `100.118.157.118`. IP sets explicitly include both address families. Re-enrollment or address changes require checking these definitions. A shared user-email source would include the user's server identities, so this first policy uses device addresses.

The candidate permits Mac SSH and named management ports, private HP report/preview HTTPS, the existing HP-to-Pi restricted backup connection, and DNS to admin-lab. The Pixel can reach HP report/preview HTTPS and remote-lab proxy HTTP/HTTPS. Web reachability does not constrain application roles or guarantee read-only access; application authentication still applies. Direct published application ports outside the named rules are omitted. Existing Codeburn and development SSH tunnels use port 22.

For Rex, the candidate provisionally permits all protocols/ports from the Mac and Mac Rex identity to the HP Rex identity only. This preserves the expected client-to-server direction, not a verified Rex integration. Required ports and real client behavior still need checking; no reverse initiation into the Mac Rex identity is granted. Both Rex identities remain part of the host review because they provide additional networking on the same physical devices.

The prepared policy removes Tailscale SSH authorization with an empty `ssh` list. No host is intended to use that mode now. JSON parsing and IP-set reference checks passed locally; the console now displays the proposed grants. Embedded positive and negative TCP/UDP tests are policy assertions; their individual console results were not supplied. Keep the old policy as a private rollback copy and the Mac's tested LAN maintenance sessions open while saving. After saving, test fresh Mac private SSH, reports/previews, Rex, DNS and the backup endpoint, plus denied initiation from remote-lab. LAN and container forwarding restrictions remain separate work. Taildrop has separate same-user behavior and is not proven blocked by these network tests.

Sources checked on 10 November 2026: [grants syntax](https://tailscale.com/docs/reference/syntax/grants), [policy reference and tests](https://tailscale.com/docs/reference/syntax/policy-file). Grants are additive, so the candidate replaces the old allow-all rule rather than appending exceptions.


Live checks from home-lab as coder after the console change on 10 November: remote-lab TCP 2222 returned an OpenSSH banner; admin-lab TCP 53 accepted a connection; a UDP A query for example.com returned a successful DNS response with two answers. Fresh TCP 22 connections to both Pis timed out over Tailscale IPv4, and remote-lab TCP 22 also timed out over Tailscale IPv6. These denials differ from the pre-policy authentication failures and support network enforcement. The endpoint/banner check does not establish a complete authenticated backup or a fresh snapshot. Lloyd subsequently confirmed fresh Mac SSH logins as lloyd to all three Tailscale IPv4 addresses. His remote-lab TCP 22 probes to home-lab, admin-lab and the Mac all reported not reached. This supports the intended SSH restriction but does not test all denied ports or remote-lab outbound IPv6. Rex and Pixel behavior remain untested. No backup or production restart was triggered. `dig` was unavailable on home-lab, so the successful UDP check used Python's socket library.
