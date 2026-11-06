# Work on the HP from the laptop

Use this after [private SSH access](02-private-access.md) works. Run agents as `coder`, never as root or `labadmin`. The laptop renders the terminal; source files, build tools, and agent processes live on the HP.

## Prepare the coding environment

Sign in as `coder`. Create a private workspace directory:

```bash
mkdir -p ~/workspaces
chmod 700 ~/workspaces
```

Use Omarchy's system-installed mise binary to install Node for `coder`. If `command -v mise` fails, install the official `mise` package through `omarchy pkg add mise` as `labadmin`, then return to `coder`. From the coding account's home directory:

```bash
cd ~
mise use --global node@24
eval "$(mise activate bash)"
node --version
npm --version
```

Add `eval "$(mise activate bash)"` once to `coder`'s `~/.bashrc`, then verify Node in a fresh SSH session. Do not copy the maintenance user's entire mise configuration. Project configuration can override the global Node version; review it before trusting or executing project tools. Record the resolved Node 24 patch version. [Mise setup and activation](https://mise.jdx.dev/getting-started.html)

Do not use sudo for npm packages to fix a permissions error.

The [verified agent research](../research/remote-coding.md#product-and-version-identity) pins the starting Pi release and identifies its current canonical package. The old `badlogic/pi-mono` name now redirects to `earendil-works/pi`. For the researched Pi v1.5.0, Node must be at least 22.19:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@1.5.0
pi --version
```

Use **OpenCode 2** for the new setup. As `coder`, check `command -v opencode`, `opencode --version`, and `opencode --help`. Reuse a working Omarchy installation rather than replacing it. If no suitable installation exists, the verified user-owned npm option is:

```bash
npm install -g @opencode/cli@2.2.5
opencode --version
```

The checked release is 2.2.5. Its native-binary installation needs postinstall scripts, so do not copy Pi's `--ignore-scripts` flag to OpenCode. V1 uses a different package, `opencode-ai`, but shares the executable name. Keep V1 examples separate and do not install a competing copy over a managed binary. [Current V2 research](../research/opencode-v2.md)

Authenticate model providers under `coder` using Pi's `/login` or OpenCode's `/connect` interface. Check the provider's subscription/API eligibility and spending controls. Keep provider secrets out of shell history and project files. Install only trusted plugins, extensions, MCP servers, and repository tooling. The agent can execute these as your coding account.

Give the HP its own scoped Git credentials. Do not copy the laptop's entire `.ssh` directory or use `ssh -A`. Use a small test repository before adding sensitive work.

## Start the first task

Connect from the laptop:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 coder@hp-lab
```

Create or clone a trusted project under `~/workspaces/project-task-1` first. Use a separate branch and worktree or clone for each concurrent task. Then start on the HP:

```bash
tmux new-session -s task-1 -c "$HOME/workspaces/project-task-1"
pi
```

Run `opencode` instead of `pi` if preferred. Detach with **Ctrl-b**, release the keys, then press **d**. Close the laptop connection and reconnect:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 coder@hp-lab
tmux attach-session -t task-1
```

Use `tmux list-sessions` to find sessions. Use `task-2` and another workspace for another task. Do not run competing agents in the same checkout. Worktrees share account permissions and parts of Git state; use separate clones or VMs when isolation matters.

After a reboot, start a new tmux session and use `pi --continue` or `opencode --continue` in the correct directory. Confirm what the previous run completed before restarting shell commands. Tmux itself does not recover across reboot.

## Open a private browser interface

OpenCode 2 normally uses a shared background server for the coding account. In the HP shell:

```bash
opencode service status
opencode pair
```

The service defaults to loopback. If status reports port 49374 and that port is free on the laptop, open another laptop terminal:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 -N \
  -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:49374:127.0.0.1:49374 coder@hp-lab
```

Open the freshly printed pairing link on the laptop. It is a single-use credential that expires after five minutes; keep it private. If status reports another port, use that actual port in the tunnel. Verify loopback-only binding and rejection of unauthenticated requests. [Official private browser workflow](https://opencode.ai/v2/docs/cli/web/)

Do not use `opencode pair --remote`: that enables public internet exposure through OpenTunnel. Keep this workflow on SSH over Tailscale. Do not substitute V1's `opencode web`, `attach`, or `OPENCODE_SERVER_PASSWORD` recipes. [V2 differences and source notes](../research/opencode-v2.md)

For ordinary app previews, forward an explicit laptop loopback port to the application's HP loopback port. Check the app's bind address, and stop the tunnel with Ctrl-c when finished. No LAN-wide listener is needed.

## Add persistent services only after the workflow passes

Interactive agents do not need a boot-time HTTP server. For supervision across reboot, first inspect the existing V2 background service. If a separate foreground service is needed, create a reviewed systemd user service for `coder`, with an absolute executable path, explicit working directory, protected credentials, resource limits, and restart handling. Enable lingering only for that account if the service must start before login. Test a reboot and unauthorized requests before relying on it.

Pi's RPC mode is a stdin/stdout protocol. It is not an authenticated public HTTP endpoint. Use SSH/tmux first instead of building a network wrapper.
