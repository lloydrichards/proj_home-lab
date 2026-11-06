# OpenCode v2 research

Checked 6 November 2026 against official v2 documentation and a tagged release. These findings were documentation-checked, not tested on the HP. The [remote-coding guide](../hp/03-remote-coding.md) owns the installation, terminal, and browser procedures.

## Package identity and installation rationale

Use a suitable existing Omarchy-managed OpenCode installation when it is available to `coder` and passes a basic test. Adding a competing installation can obscure which executable runs. Pi remains an independent alternative.

The checked release is **2.2.5**, released October 30, with npm package **`@opencode/cli`**. GitHub's generic latest-release redirect previously returned v1.19.5, so the redirect alone did not establish the current generation. This is dated evidence, not a requirement to keep that version forever. [Tagged release](https://github.com/anomalyco/opencode/releases/tag/v2.2.5), [tagged manifest](https://github.com/anomalyco/opencode/blob/v2.2.5/packages/cli/package.json)

The npm installation needs a writable user-owned Node environment. Its postinstall script selects the native binary, so Pi's `--ignore-scripts` flag must not be copied to OpenCode. V1 uses `opencode-ai`; both generations expose `opencode`. See [prepare the coding environment](../hp/03-remote-coding.md#prepare-the-coding-environment) for the executable checks and fallback installation. [Official installation](https://opencode.ai/v2/docs/), [v1 documentation](https://opencode.ai/docs/)

## Sessions and the shared service

V2 normally discovers or starts one shared background server per OS user. It owns sessions, configuration, integrations, and tool execution. Separate terminals are not separate service identities. The researched `--standalone` option selects a private server, but retains the same OS account privileges. [Background service](https://opencode.ai/v2/docs/cli/#background-service)

The HP plan starts with the terminal workflow in [start the first task](../hp/03-remote-coding.md#start-the-first-task). Tmux preserves a running terminal after disconnection; it does not restore processes after reboot. Separate worktrees prevent editing collisions without isolating credentials. [CLI introduction](https://opencode.ai/v2/docs/cli/), [command reference](https://opencode.ai/v2/docs/cli/commands/), [tmux guide](https://github.com/tmux/tmux/wiki/Getting-Started)

## Browser access and authentication

The researched v2 service defaults to loopback, normally port **49374** on Linux. Pairing creates a single-use link expiring after five minutes; opening it establishes a browser session. Inspect the actual service port and listener rather than assuming the default. The [private browser procedure](../hp/03-remote-coding.md#open-a-private-browser-interface) owns pairing and SSH forwarding commands. If installed behavior differs, retain terminal access until the difference is resolved. [Web and SSH documentation](https://opencode.ai/v2/docs/cli/web/)

Remote pairing through OpenTunnel exposes the server to the internet. It is a different access model from SSH over Tailscale and is excluded from the HP baseline. [Remote-access behavior](https://opencode.ai/v2/docs/cli/web/#remote-access)

For an optional supervised foreground service, v2 documents `opencode serve` and a matching client using `opencode --server URL`. Its authentication variable is `OPENCODE_PASSWORD`, with generated authentication by default. V1 instead uses `OPENCODE_SERVER_PASSWORD` and a different attach recipe. Keep the [legacy research](remote-coding.md) separate. A dedicated foreground service is deferred until needed and reviewed. [Standalone service and authentication](https://opencode.ai/v2/docs/cli/web/#standalone)

Pairing, transport encryption, and service authentication restrict access to the agent. They do not isolate its commands from files available to `coder`. The [security guide](../hp/06-security.md) owns the account, credential, and untrusted-work boundaries.
