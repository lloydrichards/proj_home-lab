# Private access for the HP home lab

Sources checked **2026-11-06**. This is a proposed configuration, not evidence that the HP or tailnet has been configured. Commands were checked against documentation; they have not been run on the new server. Replace example usernames, addresses and account identities before use.

## How this research is used

The [private-development choice](../../.okf/decisions/private-development.md) owns the proposed access approach and its rationale. Upcoming setup and checks belong in the [HP checklist](../hp-preparation.md). The examples below explain the relevant mechanisms; adapt them when we perform the setup.

## OpenSSH over Tailscale versus Tailscale SSH

OpenSSH over Tailscale uses Tailscale for connectivity and OpenSSH keys for login. Tailscale SSH instead intercepts tailnet connections to TCP 22 and uses tailnet identity plus separate `ssh` policy rules. It leaves the ordinary OpenSSH configuration unchanged for non-tailnet connections. Switching modes can disrupt current SSH sessions; establish local-console or independent recovery access first. [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh), [SSH over Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale)

Keep the built-in Tailscale SSH server off for this baseline. If it was enabled, change it only from a recovery session after confirming OpenSSH is installed and running:

```sh
sudo tailscale set --ssh=false
```

As of this check, Tailscale's October 28 security update fixes Tailscale SSH privilege-boundary issues and Serve/Funnel issues in **1.104.4**. Use the current stable package, at least that version. This advisory does not establish that ordinary OpenSSH over Tailscale has the same vulnerabilities. [Vendor security update](https://tailscale.com/blog/tailscale-ssh-findings-fixes)

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
