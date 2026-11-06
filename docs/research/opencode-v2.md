# OpenCode v2 on the HP

Checked 2026-11-06 using the official v2 documentation and a tagged release. These commands were documentation-checked, not run on the HP.

## Decision and installation

Use the existing Omarchy OpenCode v2 installation for terminal work if it is available to `coder` and passes a basic test. There is no reason to downgrade a clean new setup merely to match an older v1 recipe. Pi remains an independent alternative. Use the separate v1 research only when deliberately maintaining that generation.

As `coder`, inspect the actual executable before installing anything:

```bash
command -v opencode
opencode --version
opencode --help
```

The checked v2 release is **2.2.5**, released October 30, with npm package **`@opencode/cli`**. This establishes a real current v2 release, not a claim that a future installation must stay pinned forever. GitHub's generic latest-release redirect previously returned v1.19.5, so that redirect alone does not identify the newest generation. [V2.2.5 release](https://github.com/anomalyco/opencode/releases/tag/v2.2.5), [Tagged package identity](https://github.com/anomalyco/opencode/blob/v2.2.5/packages/cli/package.json)

If no suitable system installation exists, the official user-owned npm path is:

```bash
npm install -g @opencode/cli@2.2.5
opencode --version
```

This requires a writable user-owned npm prefix/Node environment. The v2 package's postinstall script selects its native binary, so do **not** copy Pi's `--ignore-scripts` flag onto this installation. Avoid installing a competing copy over an already managed executable. V1 uses `opencode-ai`, and both generations use the default command name `opencode`. [Official v2 installation](https://opencode.ai/v2/docs/), [V1/v2 command conflict](https://opencode.ai/docs/)

## Default remote terminal workflow

Connect from the laptop over the private Tailscale hostname:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 coder@hp-lab
```

On the HP, after creating the trusted task checkout:

```bash
tmux new-session -s task-1 -c "$HOME/workspaces/project-task-1"
opencode
```

Use `/connect` in the TUI to authenticate a provider, or inspect `opencode auth --help` for provider login. Do not transfer the laptop's entire credential directory. Detach with `Ctrl-b`, then `d`; reconnect and run `tmux attach-session -t task-1`. Separate concurrent tasks into separate worktrees/clones and sessions. tmux survives network disconnects, not a reboot. [V2 CLI introduction](https://opencode.ai/v2/docs/cli/), [V2 command reference](https://opencode.ai/v2/docs/cli/commands/), [tmux upstream guide](https://github.com/tmux/tmux/wiki/Getting-Started)

V2 normally discovers or starts **one shared background server per OS user**, which owns sessions, configuration, integrations, and tool execution. Terminal sessions are not separate security identities. `opencode --standalone` is an available private-server option; it still runs with the same OS account privileges. For the initial setup, leave normal defaults in place and inspect `opencode service status` plus host listeners. [V2 background service](https://opencode.ai/v2/docs/cli/#background-service)

## Optional browser access through SSH

V2 has a documented authenticated local web workflow, so it does not require the v1 `opencode web` recipe. Its shared service listens on loopback by default, normally port **49374** on Linux. On the HP:

```bash
opencode service status
opencode pair
```

Pairing prints a single-use link expiring after five minutes. Keep it private. Opening it creates a browser session. Use the actual port reported by status; if it is 49374 and that laptop port is free, run this in a second laptop terminal:

```bash
ssh -a -i ~/.ssh/hp-lab_ed25519 -N \
  -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:49374:127.0.0.1:49374 coder@hp-lab
```

Open the freshly printed loopback pairing URL on the laptop. Check the HP listener is loopback-only and test an unauthenticated request before relying on it. If port/configuration or installed-version behavior differs, keep the SSH terminal workflow and resolve that difference before enabling browser access. [V2 web and SSH instructions](https://opencode.ai/v2/docs/cli/web/)

Do **not** use `opencode pair --remote` for this private setup. The documented action exposes the server to the internet through OpenTunnel, with an explicit first-use confirmation. It is different from SSH over Tailscale. Do not bind the service to `0.0.0.0` merely to open a browser locally. [V2 remote-access behavior](https://opencode.ai/v2/docs/cli/web/#remote-access)

## Keep v1 and v2 authentication separate

For an explicitly supervised foreground v2 server, the documented command is `opencode serve`; the matching client uses `opencode --server URL`. V2 uses **`OPENCODE_PASSWORD`**, with generated authentication by default, rather than the v1 variable `OPENCODE_SERVER_PASSWORD`. Do not copy the old v1 `attach` recipe or password variable into a v2 service. This optional foreground setup is not needed for the default tmux workflow. [V2 standalone server and authentication](https://opencode.ai/v2/docs/cli/web/#standalone)

Pairing, transport encryption, and server authentication restrict access to the agent service. They do not isolate its shell commands from files available to `coder`. Keep the non-root account, private homes, scoped credentials, no host Docker socket, and VM boundary for untrusted work described in the main security guide.
