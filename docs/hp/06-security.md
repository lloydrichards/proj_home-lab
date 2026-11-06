# Security boundaries and safe exposure

The purpose of hardening is to limit who can reach the machine and what a compromised process can do. A private network does not make arbitrary repository code safe.

## Protect the administration boundary

Use the maintenance account only for system changes. Keep sudo password-protected. Run agents under `coder`, with private home directories, scoped Git access, and provider spending limits. Give each external service the minimum credentials it needs. Keep a recovery copy in a password manager rather than a repository.

A model's permission prompt is useful consent, not an operating-system sandbox. Pi extensions and OpenCode plugins can execute code. Review repository instructions, hooks, dependency installers, language servers, and MCP servers before allowing them to run. Use a VM and separate credentials when the repository or automation is not trusted. [Agent security research](../research/remote-coding.md#credentials-permissions-and-isolation)

Do not grant passwordless sudo, host Docker socket access, privileged containers, or the laptop's SSH agent to simplify agent work. Do not keep production service secrets in a workspace readable by every coding task.

## Keep three exposure classes separate

| Class | Examples | Access pattern |
|---|---|---|
| Administration | SSH, dashboards, agent APIs | Tailscale plus application authentication |
| Development preview | Local app UI, temporary test server | Loopback listener and selected SSH tunnel |
| Intentionally public application | A site selected for public hosting later | Separate deployment identity, HTTPS, app authentication where needed, explicit exposure review |

No public hostname or router rule is needed for the first two classes. If a private browser URL becomes useful, Tailscale Serve can publish a loopback service inside the tailnet. Keep its application authentication and review the tailnet's grants. Funnel publishes publicly and is not an equivalent substitute. [Tailscale access research](../research/private-access.md#optional-private-https-with-serve)

For any later public application, record its domain, owner, authentication, data, ports, update plan, rate limits, backup needs, and removal procedure. Keep SSH, databases, Coolify administration, and coding-agent APIs private. A Cloudflare tunnel alone is not an application authorization policy.

## Verify what actually listens

Inspect host sockets, effective firewall rules, tailnet policy, and container port mappings. Test from another device. Include IPv6 and repeat after updates or a new service. Listening only on loopback helps network exposure but does not prevent another local account from connecting, so authenticate APIs even when tunneled.

Omarchy documents firewall integration for Docker, but Docker also creates its own packet-filtering rules. Do not rely only on UFW's default deny. Bind necessary published container ports to `127.0.0.1` and keep databases unpublished when only other containers need them. Review version-specific localhost-publishing caveats before enabling containers. [Docker networking research](../research/private-access.md#firewall-and-docker)

## Reduce supply-chain and data risks

Use official package sources and Omarchy's supported updater. Pin the initial agent releases and record upgrades. Inspect AUR recipes and installers before granting execution. Review extension and MCP changes like other executable dependencies.

Source code, prompts, selected files, tool results, and logs may be sent to the configured model provider. Check provider settings before using private or employer repositories. Keep personal and work identities separate. Do not publish session exports or paste diagnostic logs without reviewing them for secrets.

If a token leaks, revoke it at its issuer. Removing a file or rewriting Git history does not revoke the credential. If a privileged process was compromised, plan a clean rebuild instead of assuming a password change restores trust.
