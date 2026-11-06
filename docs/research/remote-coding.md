# Pi and legacy OpenCode 1 research

For the new host, use [the OpenCode 2 note](opencode-v2.md). V1 commands below are retained for comparison and deliberate legacy installations.

Checked 2026-11-06 against first-party documentation and release source. Commands below were checked against those interfaces, not executed on the future server. `coder` is an example non-root account, `hp-lab` is the server's Tailscale hostname, and workspace paths must already exist.

## Workflow findings

The [remote-development choice](../../.okf/decisions/private-development.md) records why we prefer private terminal access. The researched starting workflow uses SSH over Tailscale and one tmux session per coding task. This works for both Pi and OpenCode, keeps the checkout and tools on the server, and survives a laptop disconnect. Add OpenCode's browser/server interface when it improves the workflow. Keep stable hosted services on the Raspberry Pi initially.

Three to five agent conversations are a reasonable **starting experiment** on 32 GB RAM when model inference runs at a remote provider. That is not a measured concurrency guarantee. TypeScript checkers, test workers, browsers, language servers, and databases consume the local RAM and CPU. Initially allow only one or two heavy build/test jobs at once, leave roughly 8–12 GB for the OS and shared services, and measure memory pressure before increasing concurrency. These are planning estimates, not vendor requirements.

## Product and version identity

The intended Pi is Mario Zechner's coding agent, historically `badlogic/pi-mono` and `@mariozechner/pi-coding-agent`. The old repository now redirects to `earendil-works/pi`. The current package is **`@earendil-works/pi-coding-agent`**; the tagged manifest still names Mario Zechner as author. GitHub's latest release resolved to **v1.5.0**. Its tagged docs and manifest, rather than similarly named forks or cached older README files, are the basis here. [Canonical repository](https://github.com/earendil-works/pi), [Pi v1.5.0](https://github.com/earendil-works/pi/releases/tag/v1.5.0), [Package identity](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/package.json)

The checked OpenCode **v1 release** is **v1.19.5**. This note deliberately documents the v1 `/docs/` interface and verifies its important server/attach commands against that tag. It does not describe the newer v2 interface. The v1 repository's latest-release redirect alone is not evidence that v1 is the newest product generation. [OpenCode v1 release](https://github.com/anomalyco/opencode/releases/tag/v1.19.5)

The official installation page now says the Arch `opencode` package and default Homebrew `opencode` formula install **v2**, while npm package `opencode-ai` installs **v1**. Both generations use the same default executable and cannot be installed side by side under that name. Check `command -v opencode` and `opencode --version` before installing. An existing Omarchy v2 installation should remain on its own reviewed v2 path; use Pi first rather than accidentally replacing it. On a coding account with no conflicting OpenCode installation, the explicit v1 path for this note is:

```bash
npm install -g opencode-ai@1.19.5
opencode --version
```

A compatible user-owned Node environment is a prerequisite for these npm examples. Choose and verify that environment during the HP setup, then record the resolved tool versions in the resulting recipe. [Official v1 installation options and v2 conflict notice](https://opencode.ai/docs/)

Pi's official npm installation requires Node.js 22.19 or newer. For a reproducible starting version, use a user-owned Node installation and pin the package:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@1.5.0
pi --version
```

Pi's official installer pins dependencies more fully; npm's transitive dependencies are not fully pinned by this command. Do not install as root merely to make a global npm command work. [Pi installation](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/quickstart.md)

## First workflow: SSH and tmux

From the laptop, connect without forwarding its SSH agent:

```bash
ssh -a coder@hp-lab
```

On the server:

```bash
tmux new-session -s task-1 -c /home/coder/workspaces/project-task-1
pi
```

Alternatively run `opencode` in that workspace. Detach with `Ctrl-b`, then `d`. Reconnect later with:

```bash
ssh -a coder@hp-lab
tmux attach-session -t task-1
```

Use `task-2`, `task-3`, and separate checkout paths for other tasks. tmux protects running programs from connection drops. It does **not** restore running processes after a server reboot. Pi saves conversation state and `pi --continue` resumes the latest session for the directory; OpenCode provides `opencode --continue` and session selection. Restarting a conversation does not resume a killed build automatically. [tmux upstream guide](https://github.com/tmux/tmux/wiki/Getting-Started), [Pi CLI](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md), [OpenCode CLI](https://opencode.ai/docs/cli/)

Pi also supports `pi --print "task"`, JSON event output, and `pi --mode rpc`. RPC is a stdin/stdout process protocol, not a ready authenticated HTTP service. For this setup, SSH/tmux avoids having to build and secure a Pi network wrapper. [Pi CLI and modes](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/cli.md)

## Optional workflow: OpenCode browser and attach

Inside a server tmux shell, set a server password without putting its literal value in shell history. The following password prompt uses Bash syntax:

```bash
read -r -s -p 'OpenCode server password: ' OPENCODE_SERVER_PASSWORD
printf '\n'
export OPENCODE_SERVER_PASSWORD
opencode web --hostname 127.0.0.1 --port 4096
```

`web` supplies the browser interface. `serve` is the headless HTTP API option. Both accept the server-password variable, with `opencode` as the default basic-auth username. Keep the explicit loopback bind; do not enable mDNS or bind to every interface for this workflow. [Server documentation](https://opencode.ai/docs/server/), [Web documentation](https://opencode.ai/docs/web/), [Tagged web command](https://github.com/anomalyco/opencode/blob/v1.19.5/packages/opencode/src/cli/cmd/web.ts)

In another laptop terminal, forward a laptop loopback port through SSH:

```bash
ssh -a -N -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:14096:127.0.0.1:4096 coder@hp-lab
```

Open `http://127.0.0.1:14096` in the laptop browser and authenticate. This leaves port 4096 off the LAN/public interfaces and carries the connection inside SSH over Tailscale. Router port forwarding is unnecessary. [OpenSSH forwarding options](https://man.openbsd.org/ssh.1)

A laptop OpenCode TUI can attach through the same tunnel. Set `OPENCODE_SERVER_PASSWORD` in that laptop shell using the hidden prompt above, then:

```bash
opencode attach http://127.0.0.1:14096 \
  --dir /home/coder/workspaces/project-task-1
```

Use matching OpenCode versions on client and server. `--dir` identifies the server workspace, not a checkout to synchronize from the laptop. Session selection is available through `--session` or `--continue`. The tagged implementation confirms remote paths can pass through even when they do not exist locally. [Tagged attach implementation](https://github.com/anomalyco/opencode/blob/v1.19.5/packages/opencode/src/cli/cmd/attach.ts)

A server is not confined to the directory where it starts. Do not treat a port or project path as a filesystem isolation boundary. For persistence across reboot, replace the tmux-hosted backend with a supervised user service after the basic workflow works. Configure its secret separately from the repository and test restart behavior.

## Credentials, permissions, and isolation

Authenticate the provider on the server under the agent account. Pi supports `/login`; its remote OAuth flow can accept the final redirect URL or authorization code when the callback cannot reach the server. Pi stores credentials in `auth.json` in its agent directory. OpenCode uses `opencode auth login` and `~/.local/share/opencode/auth.json`. These are provider credentials, distinct from the OpenCode server password. Keep them private and out of repositories and shared session exports. [Pi providers](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/providers.md), [OpenCode credentials](https://opencode.ai/docs/cli/#auth)

Do not forward the laptop's SSH agent or copy its entire credential directory. OpenSSH explicitly warns that a compromised remote machine can use a forwarded agent to authenticate as its loaded identities. Give the server its own narrowly scoped Git credentials. [OpenSSH agent-forwarding warning](https://man.openbsd.org/ssh.1#A)

Pi can read, edit, and execute anything its OS account can access. Its project-trust prompts control loading of project resources, not later tool access. Extensions run inside the process. Inspect packages and project resources before trusting them; neither the working directory nor tool-selection flags replace OS isolation. [Pi security model](https://github.com/earendil-works/pi/blob/v1.5.0/packages/coding-agent/docs/security.md)

OpenCode's `allow`/`ask`/`deny` permissions help control tools, but its own security policy explicitly says they are not a sandbox. Start with approval prompts for shell actions rather than blanket auto-approval, especially for unfamiliar projects. For unattended or untrusted work, place the entire agent in a constrained container or VM. [OpenCode permissions](https://opencode.ai/docs/permissions/), [Tagged security policy](https://github.com/anomalyco/opencode/blob/v1.19.5/SECURITY.md)

OpenCode automatically loads project/global plugins and can install configured npm plugins at startup. Treat plugins, MCP servers, language-server executables, repository scripts, and dependency installation as code execution requiring the same trust as the agent. [Plugin loading](https://opencode.ai/docs/plugins/)

Use one worktree or clone and one branch per task to prevent concurrent edits to the same files. Worktrees are organizational separation, not a security boundary. Processes under the same account can generally reach each other's files and credentials. Use separate OS users with private directories, separate clones, or separate containers/VMs when trust differs. Keep the administrative account separate from agent accounts and do not give agents sudo access.

Do not mount `/var/run/docker.sock`, give an agent membership in the host `docker` group, or grant privileged containers to simplify builds. Ordinary Docker daemon access can grant control over the host. Put Docker-dependent agent workloads in a dedicated VM with its own daemon when needed, separate from stable Coolify services. [Docker daemon security](https://docs.docker.com/engine/security/), [Docker group privileges](https://docs.docker.com/engine/install/linux-postinstall/)

Upcoming work and checks live in the [HP preparation checklist](../hp-preparation.md). The [capacity learning](../../.okf/learnings/measure-agent-capacity.md) explains why heavy build jobs must be measured separately from connected conversations.
