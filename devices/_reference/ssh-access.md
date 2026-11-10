# Connect to the lab with SSH shortcuts

Use `ssh admin-lab`, `ssh remote-lab`, or `ssh home-lab` to reach the lab through Tailscale. Use `ssh home-lab-code` for the HP coding account. Configure each originating account separately; `coder` and `lloyd` do not share SSH settings or keys.

The [service register](services.md#private-ssh-access) owns current addresses, authentication modes, fingerprints, and tested connections. This guide explains how to repeat the setup. It does not establish that every machine can log into every other machine.

## Add shortcuts on the originating machine

Connect Tailscale first. No `sudo` is needed for these account-local files.

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if [ -f ~/.ssh/config ]; then
    cp -p ~/.ssh/config ~/.ssh/config.before-lab-shortcuts
fi
```

Edit `~/.ssh/config`. Add or update these blocks before general `Host *` defaults, preserving existing entries. Do not append duplicate blocks each time you run the setup. The addresses below are the setup examples from 10 November 2026; check the service register before reusing them.

```sshconfig
Host home-lab
    HostName 100.73.122.94
    User lloyd

Host home-lab-code
    HostName 100.73.122.94
    User coder

Host remote-lab
    HostName 100.107.227.75
    User lloyd

Host admin-lab
    HostName 100.122.53.80
    User lloyd
```

Each block ends at the next `Host` or `Match` directive. If inserting these before existing global settings, put a `Host *` line between the new blocks and those settings so they remain global. Then run:

```bash
chmod 600 ~/.ssh/config
ssh -G remote-lab 2>/dev/null | awk '$1 == "hostname" || $1 == "user"'
```

Expect `user lloyd` and the Pi's Tailscale IP. `Host` is the shortcut you type; `HostName` selects the destination. These aliases also work with SCP and SFTP. They do not configure names for browsers or other applications.

MagicDNS is an alternative for system name resolution. It worked for the Pi names from home-lab, but the Mac could not resolve them during setup. IP-based shortcuts avoid that dependency. Keep admin-lab's Tailscale DNS acceptance disabled unless its Pi-hole resolver dependencies have been reviewed. There is no need to edit `/etc/hosts` for these SSH shortcuts.

## Install a public key for ordinary OpenSSH

On the originating account, check for an existing key:

```bash
ls -l ~/.ssh/*.pub
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

If no suitable key exists, create one with `ssh-keygen -t ed25519` and choose a passphrase when prompted. Reuse an existing suitable key rather than overwriting it. If its filename differs, use that path below and configure `IdentityFile` in the relevant host blocks when needed.

Keep each private key on its originating machine. Copy only the `.pub` file. For an ordinary OpenSSH destination, use an existing trusted login to add the public key to the destination account:

```bash
cat ~/.ssh/id_ed25519.pub | ssh lloyd@100.122.53.80 '
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

Replace the destination IP and username for each intended connection. Installing your own account's key needs no `sudo`. Installing a key in another user's account may require an administrator. Do not copy a Mac private key to a server or enable SSH agent forwarding.

During this setup, Lloyd used the Mac's existing access to install home-lab's `coder` public key on both Pis. The command above normally installs the key of the account running it, so choose the public key deliberately when using a third machine to bootstrap access.

## Verify the destination and test login

Read the destination's fingerprint through an existing trusted session or local console:

```bash
hostname
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Compare it with the fingerprint shown by the first new connection before accepting. If the key changes unexpectedly, investigate rather than deleting the saved key to bypass the warning. A host-key failure happens before user-key authentication.

After saving the verified host key, test a fresh login:

```bash
ssh -o BatchMode=yes \
    -o PreferredAuthentications=publickey \
    -o StrictHostKeyChecking=yes \
    -o ConnectTimeout=5 \
    admin-lab 'hostname; whoami'
```

Expect the destination hostname and `lloyd`. Repeat for each intended source account and destination. Test `home-lab-code` separately. A successful login to your own machine is not evidence of another machine's access.

`remote-lab` still uses Tailscale SSH on its Tailscale address. A successful connection there proves Tailscale identity access, not acceptance of the installed OpenSSH public key. From the home LAN, test its ordinary OpenSSH endpoint separately:

```bash
ssh -o BatchMode=yes \
    -o PreferredAuthentications=publickey \
    -o StrictHostKeyChecking=yes \
    -o ConnectTimeout=5 \
    lloyd@192.168.8.142 'hostname; whoami'
```

Check the current LAN fallback in the service register before using this example.

## Keep the authentication modes distinct

OpenSSH over Tailscale uses the private network for transport and `authorized_keys` for login. Tailscale SSH uses tailnet identity and SSH policy, and can require a browser identity check. It intercepts Tailscale connections to port 22 while ordinary OpenSSH remains available through other interfaces.

Changing remote-lab to ordinary OpenSSH over Tailscale remains proposed. Before switching, obtain explicit approval, keep a tested LAN OpenSSH session open, validate the server configuration with `sudo sshd -t`, and verify the required keys are installed. Disabling Tailscale SSH requires `sudo tailscale set --ssh=false`. Immediately test a fresh key login through the Tailscale IP. If it fails, use the open LAN session to restore `sudo tailscale set --ssh=true`. These commands have not been run during this setup.

## Diagnose a failed connection

| Result | Check next |
|---|---|
| `Could not resolve hostname` | Run `ssh -G NAME`; confirm `HostName` is the Tailscale IP. |
| `Permission denied (publickey)` | Check the source key, selected username, and destination `authorized_keys`. Use `ssh -v NAME` to inspect offered keys. |
| `Host key verification failed` | Compare the destination fingerprint through trusted access before saving it. |
| Connection timeout | Check Tailscale connectivity, tailnet policy, firewall, and destination SSH service. |
| Tailscale identity approval request | Complete the identity check; this is Tailscale SSH rather than ordinary public-key login. |

To undo shortcut changes, restore the saved config if it contains the intended previous settings. If no config existed before setup, remove only the blocks added here. Revoke an installed public key by removing its exact line from the destination account's `authorized_keys` while retaining another working login.

## Sources

- [OpenSSH client configuration](https://man.openbsd.org/ssh_config)
- [Tailscale MagicDNS](https://tailscale.com/docs/features/magicdns)
- [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh)
- [Private-access research](../../research/private-access.md)
