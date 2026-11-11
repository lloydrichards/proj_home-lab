# Route Coolify through Cloudflare Tunnel

Use remote-lab as `lloyd`, with password-required `sudo docker` for container inspection. Keep private Tailscale dashboard access working throughout changes. You need a Cloudflare domain, a configured Coolify proxy, and the connector credential held privately.

This guide covers the applied routing pattern and repeatable repairs. It does not restore the retired public SSH route or replace the separate native connector whose purpose remains unresolved. Current endpoints and verification belong in the [service register](../_reference/services.md#cloudflare-route-inspection).

## Establish the application route

1. Create or retain the application tunnel in Cloudflare. Select an ARM64-compatible connector image for the Pi and preserve the old image/configuration for rollback.
2. Create the Docker connector with the reviewed private credential, restart policy `unless-stopped`, and the proxy's `coolify` network. Keep populated credentials outside Git and shared output. Follow the [Cloudflare Docker connector instructions](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-remote-tunnel/) for the credential flow.
3. Route `*.YOUR_DOMAIN` to `http://coolify-proxy:80` and configure its tunnel DNS record.
4. Set the Coolify wildcard application domain for your own domain. Check one intended app from the browser before changing dashboard routing.

Expect the connector to resolve `coolify-proxy` and the app to load through the public hostname. A wildcard rule alone does not configure every application's authentication.

## Protect human dashboard access

1. Create a Cloudflare Access application for the whole Coolify hostname. Restrict its Allow policy to the intended administrator identity.
2. Open a private browser window. Confirm the email/identity challenge appears before the dashboard.
3. Retain the private Tailscale dashboard path for recovery.
4. For a GitHub App integration, create a separate bypass only for `/webhooks/source/github/events`. Keep browser installation callbacks behind the human gate.
5. Set the GitHub App webhook, homepage, authorization callback, and setup URL to HTTPS. Preserve the setup URL's source query parameter and the webhook secret. Verify callback matching rather than assuming a wildcard is required.

Use GitHub's delivery view to test a real signed event separately. A ping response establishes reachability, not signature enforcement or a successful deployment. See [GitHub webhook practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks).

## Match the dashboard URL to the tunnel origin

Set the public instance URL to `https://coolify.YOUR_DOMAIN` while keeping dashboard HTTP-to-HTTPS redirection disabled for the HTTP tunnel origin. Preserve unrelated application redirect settings. The [recorded Caddy configuration](../_reference/services.md#coolify-instance-url-and-caddy-tunnel-routing) describes the applied result.

If the redirect control is hidden while the saved URL is HTTP, on remote-lab run the inspected model update before changing the URL:

```bash
	sudo docker exec coolify php artisan tinker --execute='
	$settings = instanceSettings();
	$settings->is_dashboard_force_https_enabled = false;
	$settings->save();
	echo "dashboard_force_https=" . ($settings->fresh()->is_dashboard_force_https_enabled ? "true" : "false") . PHP_EOL;
	'
```

Expect `dashboard_force_https=false`. Reload the private General settings page, then save the HTTPS instance URL. Check private and public dashboard access and the generated HTTP/HTTPS site addresses. Do not patch generated Caddy files or disable HTTPS redirects globally.

## Repair proxy name resolution

<a id="verified-recovery"></a>

If public routes fail while local routes work, inspect the connector's networks without printing its token:

```bash
	sudo docker inspect --format '{{range $name, $_ := .NetworkSettings.Networks}}{{$name}} {{end}}' cloudflare-tunnel
```

If `coolify` is absent and the proxy still belongs to that network, connect the existing container:

```bash
	sudo docker network connect coolify cloudflare-tunnel
```

Check all intended public apps afterward. Preserve the network declaration when replacing the connector; a repair to an existing container does not configure its future replacement. If the repair fails, restore the saved connector image and configuration. Do not change the unrelated native connector to diagnose this Docker path.

## Repair a dashboard self-redirect

<a id="dashboard-url-and-caddy-redirects"></a>

If the browser reports `ERR_TOO_MANY_REDIRECTS` and HTTPS redirects back to the same URL, use private Settings to restore the previous HTTP instance URL. Check the dashboard redirect flag before retrying the sequence above. Keep the GitHub webhook on HTTPS and preserve Access policies. Cookie deletion does not repair a reproduced server-side redirect.

## Diagnose a 503 after an app network move

Inspect the affected container's networks and saved ingress label:

```bash
	sudo docker inspect --format 'networks={{range $name, $_ := .NetworkSettings.Networks}}{{$name}} {{end}} ingress={{index .Config.Labels "caddy_ingress_network"}}' APP_CONTAINER
```

If the proxy can reach the app on its new network but the ingress label names the old network, correct only that saved label in Coolify and redeploy. Preserve the other labels. Check the new container, public route, login, and editing separately.

Do not upgrade a database image or change its volume to repair a routing label. Destination moves and stateful migration need their own backup, identity, and rollback plan; this diagnosis is not a generic in-place migration procedure.
