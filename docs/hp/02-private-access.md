# Connect privately and separate administration from agents

Run HP commands at its console as `labadmin`. Keep the console available, and keep a working SSH session open while testing a second session. These instructions are proposed, not applied. Review [the access research](../research/private-access.md) for current advisories and policy details.

## Create the coding account

If `coder` does not already exist:

```bash
sudo useradd --create-home --shell /bin/bash coder
sudo passwd coder
sudo chmod 700 /home/coder
```

Set a unique password interactively. A usable password avoids locked-account surprises during setup; remote password login is disabled later. Do not add this account to `wheel` or `docker`. Inspect `id coder` and any sudoers rules before relying on that separation. Also make the administration home private after checking that doing so will not break a deliberate shared setup.

## Install a dedicated laptop key

On the laptop, generate a passphrase-protected key at a new path. Do not overwrite an existing key:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/hp-lab_ed25519 -C hp-lab-laptop
```

On the HP console, create the coding account's SSH directory:

```bash
sudo install -d -m 700 -o coder -g coder /home/coder/.ssh
sudoedit /home/coder/.ssh/authorized_keys
```

Paste only the laptop `.pub` line, preserving one key per line. Then set ownership and permissions:

```bash
sudo chown coder:coder /home/coder/.ssh/authorized_keys
sudo chmod 600 /home/coder/.ssh/authorized_keys
```

Repeat for `labadmin` if you want that account to accept the same laptop key, adjusting both the path and ownership. Preserve existing authorized keys rather than replacing the file. Never copy the private key onto the HP. Separate admin and coding keys are an optional further separation.

## Enroll Tailscale locally

Use the current stable Tailscale package. The [October security advisory](https://tailscale.com/blog/tailscale-ssh-findings-fixes) makes old packages unsuitable; see research for the checked minimum and always prefer the latest fixed stable release available through the supported package path.

```bash
sudo systemctl enable --now sshd.service tailscaled.service
sudo tailscale up
```

Complete the printed authentication flow on a trusted device. Enroll the laptop in the same tailnet. Set the HP device name to `hp-lab` in the administration interface, and record its MagicDNS name and Tailscale IP. If Tailscale is already configured, inspect it instead of resetting it.

Keep Tailscale SSH disabled. If it was previously enabled, disable it from the console only after confirming ordinary `sshd` works. Tailnet Tailscale SSH traffic otherwise bypasses the OpenSSH authentication rules proposed below.

On the HP:

```bash
tailscale version
tailscale status
tailscale ip -4
ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
```

On the laptop, connect with the new key and compare the displayed host-key fingerprint with the console value:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 \
  -o PreferredAuthentications=publickey \
  -o PasswordAuthentication=no coder@hp-lab
```

Use the actual MagicDNS name or Tailscale IP if `hp-lab` does not resolve. Do not accept a changed host key by deleting it without investigating.

## Restrict the tailnet policy

Review the existing policy before editing it. Default allow-all rules are broader than this host needs. A new narrow grant does not override an existing broad grant. Preserve access needed by the Raspberry Pi and other devices.

Use the [reviewable grant example](../research/private-access.md#tailnet-policy-and-device-identity) with your real identity and a server tag. Permit TCP 22 from the intended identity or selected device. Add TCP 443 only if you later use private Serve. Test the policy in its editor and from another session before removing broad allowances. A user identity may include several devices; it does not necessarily identify only your laptop.

Review node-key expiry and your identity provider's MFA. Record how to revoke a lost laptop and how to recover from an expired HP node key. Do not store enrollment keys here.

## Harden OpenSSH without locking yourself out

1. Confirm fresh key logins work for both `coder` and the administration account.
2. Inspect `/etc/ssh/sshd_config`, its `Include` directive, included files, and any `Match` blocks.
3. Review [the SSH example](../../config/ssh/00-home-lab.conf.example). Install it as `/etc/ssh/sshd_config.d/00-home-lab.conf` only if that include directory is read in the global configuration.
4. Check syntax and effective settings before reload:

   ```bash
   sudo sshd -t
   sudo sshd -T
   ```

5. Reload only after the syntax check succeeds:

   ```bash
   sudo systemctl reload sshd.service
   ```

6. Test another key login and verify password login and root login are rejected. Evaluate matching configuration for each intended user if the host uses `Match` blocks.

The example keeps PAM enabled and allows local forwarding for browser previews. It disables root login, remote password authentication, agent forwarding, and X11 forwarding. Do not copy the historical Pi article's combined directives or `UsePAM no` setting.

If a new login fails, fix or remove only the new drop-in from the still-open session or console. Re-run `sshd -t` before reload. Do not close recovery access until a fresh login succeeds. [OpenSSH configuration reference](https://man.openbsd.org/sshd_config)

## Audit network exposure

Use `sudo ufw status numbered`, `sudo ss -lntup`, and `tailscale status`. Keep the existing firewall. Inspect and remove only unwanted explicit allowances, including a broad SSH allowance created by a setup menu. Add a reviewed interface-scoped SSH allowance for `tailscale0` if required by the actual rules, and retest before removing temporary LAN access. Do not reset UFW or disable Tailscale's netfilter management.

Tailscale policy controls tailnet traffic; UFW alone is not proof of that restriction. Test laptop access over another network, denial from an unauthorized tailnet device, and denial from a LAN device without Tailscale. Include IPv6. Disable unused LocalSend and discovery exceptions only after identifying their current rules and use.

Use no router port forwarding, public Cloudflare tunnel, or Funnel for SSH or agents. Private application previews use [SSH tunnels](03-remote-coding.md). Docker needs its own exposure checks if enabled later.
