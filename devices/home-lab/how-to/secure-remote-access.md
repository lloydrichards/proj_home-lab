# Secure remote access

Use the home-lab console as the maintenance account. Keep a monitor, keyboard, and recovery USB available. This procedure targets Omarchy with OpenSSH, Tailscale, and UFW. Use the [shared SSH guide](../../../docs/how-to/connect-with-ssh.md) for client aliases and Pi-specific differences.

## Prepare the accounts and key

1. Check the destination before changing access:

```bash
	hostname -s
	id
	sudo -l
```

2. If `coder` does not exist, create it from the maintenance account:

```bash
	sudo useradd --create-home --shell /bin/bash coder
	sudo passwd coder
	sudo chmod 700 /home/coder
	id coder
	sudo -l -U coder
```

Stop if `coder` has general sudo rights or belongs to `wheel`, `docker`, or `disk`. Review exceptions individually; the installed publishing helper is a deliberate narrow exception.

3. On the Mac, select an existing Ed25519 key or create a dedicated one:

```bash
	ssh-keygen -t ed25519 -f ~/.ssh/home_lab -C home-lab
	cat ~/.ssh/home_lab.pub
```

Use a passphrase. Transfer only the public key. At the HP console, install it in both accounts' `~/.ssh/authorized_keys`, with directory mode `700` and file mode `600`. Set each file's owner to its account.

## Establish private connectivity

1. At the HP console, enroll a new machine and select ordinary OpenSSH:

```bash
	sudo systemctl enable --now tailscaled.service
	sudo tailscale up
	sudo tailscale set --ssh=false
	tailscale ip -4
```

Do not rerun enrollment or log out through the only working remote connection. Verify the device identity in the Tailscale console. Adapt the [lab policy](../../_reference/tailscale-policy.json) to your own devices; do not copy its addresses.

2. Allow the intended Mac to reach the HP on TCP 22 in the tailnet policy. Remove broad grants only after checking other devices' required access.
3. Inspect existing firewall rules and listeners:

```bash
	sudo ufw status verbose
	sudo ufw status numbered
	sudo ss -lntup
```

Expect an active firewall with incoming denial and outgoing allowance. If UFW is inactive or its defaults differ, stop and review the host policy at the console before relying on it.

If required, add an SSH allowance on `tailscale0` with `sudo ufw allow in on tailscale0 to any port 22 proto tcp`. Preserve a reviewed LAN recovery path until private access survives a cold start. Do not reset UFW or remove Docker rules.

## Validate key-only SSH

1. Save `/etc/ssh` in a private recovery directory. Inspect `/etc/ssh/sshd_config`, its `Include` directives, and existing drop-ins before editing. Create missing host keys without replacing existing keys:

```bash
	sudo ssh-keygen -A
```

OpenSSH normally uses the first obtained value. Put global settings before applicable `Match` blocks and check the effective result.
2. In the effective administrator configuration, set these values. Replace `MAINTENANCE_USER` with your account:

```text
	PermitRootLogin no
	PubkeyAuthentication yes
	PasswordAuthentication no
	KbdInteractiveAuthentication no
	AllowUsers MAINTENANCE_USER coder
	AllowAgentForwarding no
	X11Forwarding no
	AllowTcpForwarding local
	GatewayPorts no
```

These values apply to the HP. Do not copy `PermitRootLogin no` to remote-lab while Coolify still uses its root deployment connection.

3. Validate syntax and effective settings:

```bash
	sudo sshd -t
	sudo sshd -T
```

Stop on a syntax error or unexpected effective value. Inspect applicable `Match` sections with `sshd -T -C` before proceeding.

4. At the console, enable SSH and start the validated configuration:

```bash
	sudo systemctl enable sshd.service
	sudo systemctl restart sshd.service
	sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```
5. From a fresh Mac terminal, connect with an explicit key and compare the fingerprint before accepting it:

```bash
	ssh -F /dev/null -i ~/.ssh/home_lab -o IdentitiesOnly=yes -o ControlPath=none coder@HP_TAILSCALE_IP
```

Repeat for the maintenance account, substituting your actual key and address. Keep the working connections open. From another fresh Mac terminal, test password rejection and a real unlisted key:

```bash
	ssh -F /dev/null -o ControlPath=none -o PubkeyAuthentication=no -o PreferredAuthentications=password,keyboard-interactive coder@HP_TAILSCALE_IP
	ssh -F /dev/null -i UNLISTED_PRIVATE_KEY -o ControlPath=none -o IdentitiesOnly=yes -o IdentityAgent=none -o PreferredAuthentications=publickey coder@HP_TAILSCALE_IP
```

Both attempts must fail. Replace `UNLISTED_PRIVATE_KEY` with an existing key absent from the HP's authorization. A missing key file is not a rejection test. Also confirm `PermitRootLogin no` in effective settings and rejection of a fresh root login.

If the new login fails, keep the console session open. Restore the saved SSH configuration, validate it, reload SSH, and inspect Tailscale policy and UFW separately. Follow the [security explanation](../../../docs/explanations/security-and-access.md) for the boundaries these checks establish.
