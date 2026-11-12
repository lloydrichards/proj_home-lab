# Connect to the lab with SSH

Addresses below are documentation examples. Substitute hosts from your ignored local inventory and verify their fingerprints against the private service register.

Use this guide from the Mac or another deliberately authorized maintenance client. The [service register](../../devices/_reference/services.md#private-ssh-access) owns current endpoints, fingerprints, and authorization. Ordinary OpenSSH handles login on all three hosts; Tailscale supplies private transport.

For the existing Pis, use the current Mac key. Home-lab's `coder` key was deliberately revoked. Adding a shortcut does not authorize a key or establish that one lab machine may administer another.

## Add shortcuts on the originating machine

1. Connect Tailscale.
2. Prepare account-local SSH configuration:

	```bash
	mkdir -p ~/.ssh
	chmod 700 ~/.ssh
	if [ -f ~/.ssh/config ]; then
		cp -p ~/.ssh/config ~/.ssh/config.before-lab-shortcuts
	fi
	```

3. Edit `~/.ssh/config`. Add or update these blocks before general defaults. Replace the addresses for another installation:

	```sshconfig
	Host home-lab
		HostName 192.0.2.176
		User lloyd

	Host home-lab-code
		HostName 192.0.2.176
		User coder

	Host remote-lab
		HostName 192.0.2.175
		User lloyd

	Host admin-lab
		HostName 192.0.2.186
		User lloyd
	```

	Do not append duplicate blocks. Each block ends at the next `Host` or `Match` directive. If inserting them before existing global settings, put `Host *` before those settings.

4. Check the selected destination:

	```bash
	chmod 600 ~/.ssh/config
	ssh -G remote-lab 2>/dev/null | awk '$1 == "hostname" || $1 == "user"'
	```

	Expect `user lloyd` and the registered Pi address. Check `home-lab-code` separately; it must select `coder`.

These shortcuts also work with SCP and SFTP. They do not configure browser or system DNS. For another originating account, repeat the configuration there; accounts do not share SSH settings.

## Install a public key for ordinary OpenSSH

1. On the authorized client, inspect an existing public key:

	```bash
	ls -l ~/.ssh/*.pub
	ssh-keygen -lf ~/.ssh/id_ed25519.pub
	```

2. If no suitable key exists, run `ssh-keygen -t ed25519` and choose a passphrase. Do not overwrite an existing key. If using another filename, configure its `IdentityFile` in the relevant host block.
3. Through an existing trusted destination login or console, add only the selected public key to the intended account. For example, from the Mac to admin-lab:

	```bash
	cat ~/.ssh/id_ed25519.pub | ssh lloyd@192.0.2.186 '
	set -eu
	IFS= read -r key
	case "$key" in
		ssh-ed25519\ *) ;;
		*) echo "Expected one Ed25519 public key" >&2; exit 1 ;;
	esac
	mkdir -p "$HOME/.ssh"
	chmod 700 "$HOME/.ssh"
	touch "$HOME/.ssh/authorized_keys"
	chmod 600 "$HOME/.ssh/authorized_keys"
	if ! grep -qxF "$key" "$HOME/.ssh/authorized_keys"; then
		printf "\n%s\n" "$key" >> "$HOME/.ssh/authorized_keys"
	fi
	'
	```

	Replace the destination for another intended connection. Use a console if no trusted remote login exists. Do not copy a private key to a server or enable SSH agent forwarding.
4. Test a fresh connection before ending the recovery session.

To revoke access, remove only the exact public-key line while retaining a tested maintenance login. Keep private recovery copies outside Git. Restoring an old `authorized_keys` copy also restores its revoked authorizations.

## Verify the destination and test login

1. Read the ordinary OpenSSH host fingerprint through a trusted session or console:

	```bash
	hostname
	ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
	```

2. Compare that fingerprint with the first new connection before accepting it. Investigate unexpected changes; do not delete trust entries to silence a warning.
3. Test without reusing an authenticated connection:

	```bash
	ssh -o ControlPath=none \
		-o BatchMode=yes \
		-o PreferredAuthentications=publickey \
		-o StrictHostKeyChecking=yes \
		-o ConnectTimeout=5 \
		admin-lab 'hostname; whoami'
	```

	Expect `admin-lab` and `lloyd`. Repeat for each intended host/account pair, including `home-lab-code`. A connection to the source machine itself does not test remote access.

## Keep the authentication modes distinct

The existing lab has already migrated to ordinary OpenSSH. Use this sequence only when deliberately changing another host from Tailscale SSH:

1. Keep a tested LAN OpenSSH session or console open. Validate the server with `sudo sshd -t` and verify the required public keys.
2. Record `/etc/ssh/ssh_host_ed25519_key.pub` through that trusted path. Preserve the client's Tailscale SSH trust entry for rollback.
3. Through the recovery session, run `sudo tailscale set --ssh=false`.
4. On the client, inspect `ssh -G HOST` for the selected endpoint, port, `HostKeyAlias`, and known-hosts files. Back up the affected file. Replace only that endpoint's old entry with the trusted OpenSSH key.
5. Repeat the strict fresh-login test above. Keep the recovery path until every required client passes.

Do not trust a replacement key solely because `ssh-keyscan` or a new connection presents it. To roll back a failed mode change, use the recovery session to restore `sudo tailscale set --ssh=true`, restore or independently verify the returning Tailscale SSH host identity, and test a fresh connection. A Tailscale identity approval does not prove acceptance of an OpenSSH public key.

## Diagnose a failed connection

| Result | Next check |
|---|---|
| `Could not resolve hostname` | Inspect `ssh -G NAME`; confirm `HostName` selects the intended Tailscale IP. |
| `Permission denied (publickey)` | Check the offered key, username, and destination `authorized_keys`. Use `ssh -v NAME`. |
| `Host key verification failed` | Compare the fingerprint through trusted access before updating the exact trust entry. |
| Timeout | Check Tailscale connectivity, policy, host firewall, and destination SSH service. |
| Tailscale identity approval | Check whether Tailscale SSH is enabled on the destination; it is not the current lab mode. |

To undo shortcut changes, restore the saved configuration if it contains the intended prior state. Otherwise remove only the new blocks. Keep admin-lab's Tailscale DNS acceptance disabled unless its resolver dependencies have been reviewed; SSH aliases do not require editing `/etc/hosts`.

## Pi maintenance permissions

Use `lloyd` for human maintenance and `sudo docker` for container administration. Ordinary SSH key login and sudo password authentication are separate checks. The [service register](../../devices/_reference/services.md#pi-maintenance-permissions) records the current permissions and verification limits.

1. Open a fresh Mac SSH session and run `id`. Expect no `docker` group.
2. Run `docker ps`. Expect a Docker socket permission error.
3. Run `sudo -k`, then `sudo -n true`. Expect a password-required error.
4. Run `sudo -v` and enter the host's maintenance password. Run `sudo id -u`; expect `0`.
5. Run `sudo docker ps`. Expect the container list without a restart.
6. Open another fresh terminal. Confirm that the first terminal's sudo authentication does not authorize it.

During a permission change, keep a root recovery shell until fresh-session checks pass. Save the preceding configuration privately and record its location in the local service register. Validate sudoers changes with `visudo -c` before closing recovery access. Restoring an older rule can restore broad passwordless privilege; review it before use.

After successful checks, close old recovery and SSH sessions. Existing processes can retain prior groups. Do not stop production processes or reboot a DNS host solely to clear groups without checking dependencies.

## Admin-lab root SSH

The installed `/etc/ssh/sshd_config.d/00-lab-no-root-login.conf` sets `PermitRootLogin no`. The main daemon includes that directory. Keep remote-lab's separate Coolify root key path unchanged.

If a future change breaks maintenance access, use an existing trusted root shell or console. Remove only that drop-in if rollback requires it, validate with `sshd -t`, and reload SSH. Removing it restores the preceding root-login policy; inspect effective settings before treating rollback as the final state.

## Remote-lab SSH password hardening

The inspected remote-lab daemon reads global settings from `/etc/ssh/sshd_config` without an active drop-in `Include`. Its installed `PasswordAuthentication no` and `KbdInteractiveAuthentication no` preserve public-key authentication and `PermitRootLogin prohibit-password` for Coolify.

For recovery during a future change:

1. Confirm `hostname -s` reports `remote-lab` and `whoami` reports `root` in the trusted remote recovery shell.
2. Restore your privately recorded configuration backup only if reverting to the preceding policy is required.
3. Run `sshd -t` before reloading SSH.
4. Verify effective settings and fresh Mac login. Reapply key-only authentication after correcting the failure.

The saved configuration re-enables earlier password methods. A quoted SSH command returns to the client when it finishes; subsequent shell commands do not continue on the Pi. The backup daemon on port 2222 has separate configuration.

## Sources

- [OpenSSH client configuration](https://man.openbsd.org/ssh_config)
- [Tailscale MagicDNS](https://tailscale.com/docs/features/magicdns)
- [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh)
- [Private-access research](../../research/private-access.md)
