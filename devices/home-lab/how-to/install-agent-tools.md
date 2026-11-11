# Install agent tools

Run agent tools as `coder` on home-lab. Complete [private access](secure-remote-access.md) first. Keep administrator credentials and Docker access outside the coding account.

Use one terminal agent first. Add a client or background service only when you need it. Check recorded versions and installed endpoints in the [service register](../../_reference/services.md); the commands below do not select a permanent release version.

## Prepare the coding account

1. Log in as `coder` and check its tool paths:

```bash
	whoami
	command -v git mise node npm
	mkdir -p ~/projects
```

Use a user-owned runtime environment. Do not install an agent or run project package scripts as root.

2. Clone the required project from GitHub and configure its runtimes. Supply scoped Git credentials without forwarding the Mac's SSH agent.
3. Check existing agent installations before adding another:

```bash
	command -v codex opencode
```

## Install or verify Codex

1. Follow the current [official Codex CLI instructions](https://learn.chatgpt.com/docs/codex/cli). With a user-owned npm environment, the documented installation is:

```bash
	npm install -g @openai/codex
	codex --version
```

2. Run `codex` inside the selected project and authenticate in the interactive flow. Keep authentication files out of Git and chat.
3. Complete a small task and close the client. Use `codex resume` to check that its saved conversation is discoverable.

If installation fails, inspect the executable path and runtime ownership before adding a competing installation. Do not solve a user-directory permission error with a root npm installation.

## Install or verify OpenCode

1. Check the selected generation against the [OpenCode research and official links](../../../research/opencode-v2.md). This lab uses v2; v1 package and service examples differ.
2. Download and inspect the standalone installer before running it as `coder`:

```bash
	curl -fsSL https://opencode.ai/v2/install -o /tmp/opencode-install.sh
	less /tmp/opencode-install.sh
	bash /tmp/opencode-install.sh
	~/.opencode/bin/opencode --version
```

3. In a fresh interactive shell, confirm `command -v opencode`. Start `opencode` in the chosen project and use `/connect` for provider sign-in.
4. Inspect `ss -lntup` before enabling browser access. Keep its service on loopback and use a reviewed SSH forward. Do not substitute a public pairing tunnel.

## Choose terminal persistence or a client

For a persistent terminal, start `tmux new -s work`. Detach with **Ctrl+B**, then **D**. Reconnect and run `tmux attach -t work`. Confirm the same terminal remains after SSH disconnects.

For Rex, follow its [official user installation](https://www.superlogical.com/rex/docs/linux/remote-access#ssh-forwarding). Start the personal server as `coder`, inspect its Unix socket, and forward that actual socket from the Mac. Do not copy another machine's numeric user ID. Use the [shared SSH guide](../../_reference/ssh-access.md) for the host alias.

For T3, review its [installer](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md) and [service lifecycle](https://github.com/pingdotgg/t3code/blob/main/docs/user/background-service.md). For a new installation, keep it on loopback before installing the user service. If `~/.t3/service.env` already exists, edit its host setting instead of running the `printf` line:

```bash
	curl -fsSL https://t3.codes/install.sh -o /tmp/t3-install.sh
	less /tmp/t3-install.sh
	sh /tmp/t3-install.sh
	mkdir -p ~/.t3
	printf 'T3CODE_HOST=127.0.0.1\n' > ~/.t3/service.env
	chmod 600 ~/.t3/service.env
	~/.local/bin/t3 service install
	~/.local/bin/t3 service status
```

Connect the Mac client to the HP SSH environment and test one authenticated provider request. Check logout persistence and reboot recovery separately.

For shared skills, clone the [skills source repository](https://github.com/lloydrichards/skills), review its installation plan, and apply through its own CLI. Follow [source synchronization and recovery](../../../research/shared-agent-skills.md). Do not copy generated skill directories between machines or edit installed ownership hashes.

Stop or disable only the service you are replacing. Terminal persistence, saved conversations, and [backups](back-up-agent-sessions.md) require separate checks.
