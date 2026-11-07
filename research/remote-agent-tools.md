# Coding agents on the HP from the MacBook

Researched on 2026-11-06, with T3 Code and Herdr workflows refreshed on 2026-11-07 against the primary sources linked below. These are documented capabilities, not installation or runtime checks on the HP. The user intends to run Omarchy and use Tailscale. Upcoming work stays in the [HP checklist](../home-lab/preparation.md).

## What to try first

Lloyd chose the following approach on 7 November 2026: devvm locally on the MacBook for selected projects needing isolation, and ordinary remote coding on the HP for independent compute and longer work. HP-side devvm is deferred. The daily client remains undecided; T3, Rex, and Herdr are researched candidates. See the private-development decision in OKF for the rationale.

For remote work, the HP owns the repository, dependencies, agent process, tests, and development server. For local devvm work, these run on the Mac inside the selected guest. Hosted models still do inference at their providers. Keep each task on one machine and use Git for handoffs; preserve uncommitted work and agent sessions separately. No installation has been performed.

## Comparison

| Tool | MacBook side | HP side | Why consider it | Main qualification |
|---|---|---|---|---|
| T3 Code | Desktop app or browser | Headless T3 server and authenticated agent providers | Graphical threads, review, and remote environments | New project; keep client and server compatible |
| Rex | Native Mac terminal client | Rex Linux server and agent CLIs | Persistent remote terminals, status and agent-controlled panes | Beta access; transport currently supplies authentication |
| Herdr TUI | Any terminal over SSH, or local Herdr client | Herdr server and agent CLIs | Agent states, persistent panes, several remote machines | Distinct from the new Herdr native app |
| Herdr native app | Native app | herdr-core and agent CLIs, reached through SSH | One sidebar across machines | Does not resume tasks after reboot |
| devvm | SSH terminal or remote editor | Lima project VMs and agent tools inside them | Per-project isolation and optional separate clone | Extra VM resources; exact Omarchy behavior untested |

## T3 Code

T3 is free and MIT licensed, and controls installed agent providers using their credentials or subscriptions. Authenticate the provider and Git access on the HP. [README](https://github.com/pingdotgg/t3code/blob/main/README.md), [provider setup](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/install.md).

### A proposed normal session

This is an illustrative sequence built from the documented controls, not a session performed on the HP.

1. Open T3 on the Mac. In Settings, Environments, Add environment, choose SSH and enter an HP alias from the Mac's SSH configuration. T3 starts or reuses the HP server and forwards its port. Provider commands must be available to the remote non-interactive login shell. [Remote access](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md).
2. Select the HP environment and add its repository. Start a thread for the task and choose New worktree for a separate branch and checkout. A new thread alone does not guarantee a separate checkout. [Threads](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/thread-sidebar.md).
3. Choose the provider and explicitly select Supervised for the first trial. The documented initial default is Full access. Supervised requests command and edit approval, subject to provider differences. Requests appear in the conversation, including requests from subagents. [Permission modes](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/permission-modes.md).
4. Describe the task. Paste or drag a Mac screenshot into the composer if useful. T3 uploads attachments to the environment's machine, so the HP agent receives the file. You can queue a follow-up or steer a running turn when the provider supports it. [Messages and attachments](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/composer.md).
5. Read changed files in the Diff pane. Per-turn changes exclude unrelated files brought in by pulls or rebases; use the branch comparison for the complete change. Git actions can commit, push, and open a pull request using HP-side authentication. [Source control](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/source-control.md).
6. For web work, use the environment's browser. It runs on the HP and streams to the Mac, so its localhost reaches HP development servers. Agent browser tabs remain available without connected clients. A normal Mac browser still needs a forwarded development port or another reachable preview address. [Remote browser](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md).

### Leaving and returning

For the always-on arrangement, install the HP background service independently rather than relying on a foreground shell. Linux setup enables systemd user lingering so it starts at boot and survives logout. `t3 service status` checks this. Restarting the service interrupts active turns, terminals, and clients; saved threads are not proof that work automatically continues after reboot. [Background service](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/background-service.md).

Desktop-managed SSH and a service are separate lifecycle choices. Removing a saved SSH connection stops a server that desktop launched; a pre-existing server is left alone. This does not establish what merely closing the Mac app does. Direct pairing and Tailscale HTTPS are supported. T3 Connect is optional; it currently allows three linked machines without a paid T3 Chat plan. [Connection choices](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md).

For a private service, the documented `service.env` supports `T3CODE_HOST=127.0.0.1`; SSH or Tailscale Serve can reach that loopback listener. `t3 up --lan` also allows LAN access, so it is a different exposure choice. Check the actual service and forwarding configuration during setup. [Service configuration](https://raw.githubusercontent.com/pingdotgg/t3code/main/docs/user/background-service.md).

The practical distinction is that prompts, approvals, attachments, diffs, and previews share one interface while tools execute on the HP. This is a proposal for the most integrated graphical trial, not evidence that every provider behaves identically or that laptop sleep has been tested.

## Rex terminal

Rex is Superlogical's terminal system. Its current installation page makes the macOS client and Linux server available to beta testers. Windows and other clients described there are not yet part of public testing. Download access uses an invitation and Discord login. That access requirement is separate from authentication to a self-hosted server. [Installation](https://www.superlogical.com/rex/docs/installation).

Rex has unusually relevant Omarchy documentation. Its installer handles Omarchy's update policy; manually copying a generic Arch `pacman -Syu` recipe is inappropriate. Omarchy configuration refreshes can remove Rex's package repository, leaving updates disabled until repaired. [Linux installation](https://www.superlogical.com/rex/docs/linux/installation).

Remote access can use built-in Tailscale, the host's Tailscale through Serve, or SSH forwarding of a Unix socket. The SSH option needs no public listener. The remote personal server needs to remain running after logout, and the documentation calls out `loginctl enable-linger`. Rex currently trusts identity supplied by the connection transport; a fuller authentication and authorization system is planned. A connected client can start programs as the server's account. For this lab, test a personal server rather than accepting a shared service's account defaults. [Remote access](https://www.superlogical.com/rex/docs/linux/remote-access).

Rex can install skills and hooks for Claude Code, Codex, OpenCode, and Pi. Agents can use its CLI to create panes, start tests, and inspect terminal output. That is terminal automation, not a separate model provider. [Agents](https://www.superlogical.com/rex/docs/automate/agent-skill). No durable pricing commitment was established in the official pages reviewed, so do not treat present beta access as a pricing guarantee.

### A proposed Rex session

1. Start a personal Rex server under the HP coding account. In Rex for Mac, use Add Remote Host with its Tailscale endpoint or a locally forwarded Unix socket. The socket path comes from the HP's `rex server status`, not a guessed user ID. [Connection setup](https://www.superlogical.com/rex/docs/linux/remote-access).
2. Create a named session in the HP checkout and launch the coding CLI there. For example, `rex session new retry-fix -c /home/coder/workspaces/project` creates a session with that working directory. The path is illustrative and must exist. Separate active tasks need separate checkouts; a new terminal alone does not separate their files. [Session commands](https://www.superlogical.com/rex/docs/reference/cli).
3. Work in the agent's terminal interface and answer its own approval prompts. With Rex's skill installed on the HP, ask it to open tests or the development server in another pane and inspect their output. Review in a terminal Git tool or a remote editor. This proposed review arrangement does not assume Rex supplies a complete graphical Git review interface. [Agent automation](https://www.superlogical.com/rex/docs/automate/agent-skill).
4. When an agent reports OSC 7501 status, Rex marks blocked or completed sessions in its picker and reports progress in tabs. This needs reporting support; merely running an arbitrary agent does not guarantee accurate state. Mobile push and a unified priority inbox remain planned in the reviewed protocol documentation. [Status behavior](https://www.superlogical.com/rex/docs/build/program-status).
5. Close the Mac client while leaving the HP server and its sessions running, then reconnect to the same host. Explicitly starting a personal server avoids its empty-server idle shutdown. Stopping that server ends its sessions. Saved-session restoration is documented, but automatic agent-task resumption after HP reboot was not established. [Server lifetime](https://www.superlogical.com/rex/docs/linux/server-modes), [Restore option](https://www.superlogical.com/rex/docs/reference/cli).

For web previews, propose a Mac browser with a separate SSH forward to the HP development server. Remote screenshot paste and an integrated browser workflow were not established in the Rex sources reviewed. These are investigation gaps, not claims that Rex cannot support them.

## Herdr has two separate implementations

Herdr TUI owns terminals in its own background server. The newer native app uses herdr-core, and the two do not share agent sessions. Both are free and Apache 2.0. The native macOS release requires Apple silicon. [Native app FAQ](https://herdr.dev/), [TUI repository](https://github.com/herdrdev/herdr).

### A proposed Herdr TUI session

1. Install a local client on the Mac and run `herdr --remote hp`, using a working SSH alias. Herdr discovers compatible remote software and asks before installing or replacing it. The HP server owns the panes and commands; the Mac client draws the interface. Unlike plain SSH followed by remote `herdr`, the local client can copy a Mac clipboard image to a remote temporary file and paste its path into the agent. [Remote attach](https://herdr.dev/tui/docs/persistence-remote/).
2. Alternatively, run `herdr machine add hp` once, then open local `herdr`. Choose the HP in the sidebar alongside Local. Each machine keeps its own server. A saved profile targets one remote session, not every session on the machine. [Connecting machines](https://herdr.dev/tui/docs/connecting-machines/).
3. Open a repository workspace and create a worktree for an independent task. The built-in worktree commands create a Git checkout and group its workspace under the repository. Start your chosen coding CLI in its pane. Use another pane for tests or a development server. [Worktree commands](https://herdr.dev/tui/docs/cli-reference/).
4. Read and answer approvals in the agent's own terminal interface. Herdr's sidebar helps identify agents that need attention; it does not replace the provider's permission policy. Review through a terminal Git tool or a remote editor. For a Mac browser preview, forward the HP development port. This last arrangement is an illustrative workflow, not a claim of a built-in Herdr browser.
5. Detach with `ctrl+b q`, then reconnect later. The server keeps shells, agent processes, tests, and development servers running while detached. After a server restart those processes are gone. Eligible agent conversations can be resumed using official integrations, after a client attaches. Unsupported panes return as shells. Check `herdr integration status`; native session restore is not arbitrary command recovery. [Session state](https://herdr.dev/tui/docs/session-state/).

This path keeps the familiar coding CLI and adds an overview of its state. Reconnecting after network loss is automatic for saved machines. Dimming means cached state until reconnection, not proof that a task is still working. Herdr does not copy the Mac's executables, secrets, or command plugins to the HP. [Remote machine behavior](https://herdr.dev/tui/docs/connecting-machines/).

### A proposed native Herdr app session

Open the app on the Mac, add the HP through its machine setup, and select a space there. Spaces correspond to repositories or working folders; tabs correspond to tasks. The official guide documents starting an agent from the tab-bar plus menu and asking it to create a worktree or add a remote machine. [Guide](https://herdr.dev/guide/).

The shipped interface includes Files and Changes panels. Its worktree menu opens separate checkouts on the space's machine under `~/.herdr/worktrees`. Clipboard image paste can copy an image to another machine and paste its path into the terminal. Approvals still belong to the underlying CLI. These are useful graphical conveniences, so the native app should not be described as only a plain terminal. [Versioned app guide](https://raw.githubusercontent.com/herdrdev/herdr-app/master/defaults/AGENTS.md).

Closing the app leaves HP agents running in herdr-core. Closing a terminal pane ends its terminal, a different action. A reboot, logout, or lost core terminal returns a shell in its previous directory; the original agent command is not restarted. The native app does not have the TUI's agent-resume behavior. [App state model](https://raw.githubusercontent.com/herdrdev/herdr-app/master/defaults/AGENTS.md), [FAQ](https://herdr.dev/).

No integrated web preview was established in the sources reviewed. A separate Mac browser with port forwarding and a remote editor remain reasonable companions. The configurable app can add panels, but a possible mod is not an installed, supported preview workflow.

herdr-core can also run without the app. Its `hc machine add` and `hc run --on` commands operate remotely over SSH. Status requires the program to report OSC 7501, whereas the TUI also detects status from terminal content. Confirm behavior with the actual provider versions. [Core](https://github.com/herdrdev/herdr-core).

## devvm with T3 Code

HP-side design retained as a deferred alternative. The chosen initial use of devvm is local to the MacBook; the following is not the HP preparation plan.

The proposed arrangement is one T3 server inside each devvm guest, with the Mac connecting to that server through the HP. This puts the agent, Git operations, repository, tests, and browser in the same guest. A T3 server on the HP with only its agent command wrapped in devvm would leave other T3 operations outside that boundary. The complete integration has not been run or verified.

### Project and task isolation

`devvmhq/devvm` supports Linux x86_64 and Lima 2.2 or newer. Install it on the HP to use HP resources. By default it creates one VM per project folder and reopens that VM on later runs. [README](https://github.com/devvmhq/devvm).

On Linux, prefer `--clone`: devvm explicitly recommends it because Linux has no mounted-folder `.git` protection. The guest clone lives on its own disk. Shared tools and agent configuration folders remain mounted, but the HP project folder does not. Committed branches are copied; uncommitted edits, ignored files, `.env`, and `node_modules` are not. For a VM per task, create separate HP repository folders and run `devvm --clone` in each. Merely opening another T3 thread or guest worktree does not create another VM. Worktrees within one guest share that guest's permissions, credentials, network, and resources. [Clone behavior](https://devvm.dev/docs/using/clone/).

### Connect the Mac without exporting guest SSH keys

The following is an illustrative route, not an executed recipe:

1. Inside the first guest, configure T3 to listen on loopback with a unique port, for example `T3CODE_HOST=127.0.0.1` and `T3CODE_PORT=13773`, then run it independently of the interactive shell. Use a different guest port for each other VM.
2. On the HP, in that VM's project folder, set `devvm ports 13773`. Devvm forwards guest TCP port 13773 to HP localhost port 13773, including when the guest server listens only on loopback. It forwards the same port number, not a separate host port. New VMs otherwise forward listening TCP ports from 1024 upward by default. Explicit selection avoids relying on that broad default. [Ports](https://devvm.dev/docs/using/ports-size/).
3. On the Mac, run `ssh -N -L 13773:127.0.0.1:13773 hp`, where `hp` is the HP's SSH alias over Tailscale. Pair the Mac T3 client to this forwarded endpoint. Keep pairing authentication enabled. The tunnel must remain connected for Mac control; the guest service must remain running independently for work to continue when it disconnects.

The HP already gets guest SSH aliases through `devvm host`, but those aliases point to HP loopback and use a guest-specific identity and pinned host keys stored on the HP. The guest SSH port can change on restart. They are not ready-made Mac aliases: `ProxyJump hp` alone does not transfer their identity or host-key configuration. Use the forwarded T3 endpoint first rather than copying guest private keys onto the Mac. [SSH configuration](https://devvm.dev/docs/using/ssh/).

### Authentication and network checks

Devvm provisions Claude Code, Codex, or OpenCode inside the guest. Supported credentials stay in its HP-side store and proxy; the guest receives placeholders. Some unsupported OpenCode provider keys pass through unchanged. Claude authentication follows undocumented upstream behavior. For this trial, have guest T3 use the devvm-provided CLI and home configuration. Do not assume T3-managed runtimes, extra provider instances, or custom credentials retain devvm's placeholder behavior. Confirm with a real provider call and the proxy log. [Agent provisioning and logins](https://devvm.dev/docs/using/coding-agents/).

Confined guests must use the proxy. Devvm sets proxy and certificate variables for guest logins; a T3 background service and its child processes must inherit compatible settings. T3 downloads, updates, browser installation, and websites reached by the guest browser may need additional allowlist entries. A browser that ignores the proxy will fail even for an allowed website. Check blocked requests rather than changing the whole VM to `open`, which permits reaching the HP and LAN. Incoming forwarded control ports are separate from outbound allowlist rules. [Network tiers and proxy limitations](https://devvm.dev/docs/safety/network/).

### Persistence and resource limits

Devvm leaves VMs running after their interactive shell ends, but restarting or stopping a guest stops its programs and proxy. Boot recovery must start devvm through its normal checks, then start guest T3. Do not bypass those checks with raw `limactl`, which devvm identifies as an unconfined debugging path. [VM lifecycle](https://devvm.dev/docs/using/vms/), [CLI](https://devvm.dev/docs/cli/devvm/).

Clone work is guest-disk data. Deleting or rebuilding a VM can lose it; fetch and review committed work and preserve uncommitted work first. Clone-mode VMs currently refuse `devvm update` and layer changes until switched out of clone mode. [Clone lifecycle](https://devvm.dev/docs/using/clone/). Mounted-folder Linux file watching also has 9p limitations. [Known limits](https://devvm.dev/docs/using/limits/).

If HP VMs are reconsidered, the earlier sizing proposal for this 32 GB HP was one VM per active trusted project, with a worktree per task inside it. Use another VM when a task needs stronger separation. Start with one guest; plan for two active 8 GiB guests, or test three 6 GiB guests for lighter work after measurement. Keep configured guest RAM around 16–20 GiB in total, leaving room for Omarchy, host services, and VM overhead. Start with one heavy build at a time. These are planning estimates, not measured capacity.

The documented base is 4 CPUs, 8 GiB RAM, and a 100 GiB virtual disk. For smaller new guests, `devvm size -g --cpus 2 --memory 6` changes future defaults. In an existing project's HP folder, `devvm size --cpus 2 --memory 6` changes that guest on its next start or restart, which interrupts running work. The disk size is a growth ceiling; Linux guests use growing qcow2 overlays. The documentation does not establish automatic reclamation of configured RAM, so budget it conservatively. [Sizing](https://devvm.dev/docs/using/ports-size/).

Stop an unused project VM with `devvm stop` rather than deleting it. Its processes stop while its disk and project remain; `devvm` starts it again. Deletion with `devvm rm` removes guest data and needs the clone-preservation checks described above. [VM lifecycle](https://devvm.dev/docs/using/vms/). Distinct guest control and preview ports remain necessary because another guest or host process can already own a port.

## Other useful options

- VS Code Remote SSH keeps the UI on the Mac and runs extensions and commands against the remote checkout. It is a strong option when manual editing and debugging matter alongside agents. Confirm extension execution location and Arch compatibility. [Remote SSH](https://code.visualstudio.com/docs/remote/ssh).
- Zed remote development runs language servers, tasks, and terminals remotely while its UI and built-in model communication remain local. It supports remote editing well, but that split alone does not provide an autonomous agent that continues with the Mac asleep. [Remote architecture](https://zed.dev/docs/remote-development).
- cmux is a free native macOS terminal with agent notifications. Its remote workflow supports SSH and attaching to remote tmux sessions. It offers a Mac-focused interface while persistence can remain on the HP. [Official site](https://cmux.com/).
- OpenCode's current web interface shares its server with the TUI. Its documentation explicitly supports an SSH forward to the loopback service, pairing links, and authenticated browser access. It is a useful focused alternative when OpenCode is the chosen agent. The `/v2/` documentation URL now redirects to current docs; do not mix these commands with old v1 examples. [Web access](https://opencode.ai/docs/cli/web/), [existing v2 investigation](opencode-v2.md).

## Proposed evaluation

Use one noncritical repository on the HP. Compare a plain persistent SSH session with T3 and one terminal candidate. Keep one checkout per active task using branches or worktrees; separate machines should exchange changes through Git rather than concurrently writing a network-mounted `.git` directory.

The useful outcomes are whether work continues when the Mac sleeps, whether approvals and completed work are easy to find on reconnect, whether tests and preview servers really run on the HP, and whether a second task interferes with the first. Check reboot recovery separately. Local devvm trials are separate from HP preparation. Revisit HP VMs only if a specific remote project needs isolation. These are proposals; the [HP checklist](../home-lab/preparation.md) owns the actual upcoming tasks.
