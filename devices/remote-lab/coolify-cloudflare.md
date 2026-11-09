> Historical Raspberry Pi setup. Do not use this as the HP/Omarchy security baseline. For the arriving HP, start with [its preparation checklist](../home-lab/preparation.md).

# Setup Coolify with Cloudflare tunnel

1. Buy or add a domain to Cloudflare.
1. Add a new tunnel in the Zero Trust tab (separate from SSH in
   [SSH through Cloudflare](cloudflare-ssh.md)).
1. Use the Docker image to add the new tunnel, be sure to name it:

   ```bash
   docker run -d --name cloudflare-tunnel --restart unless-stopped --network coolify cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <TUNNEL_TOKEN>
   ```

1. Connect the tunnel to the coolify network:

   ```bash
   docker network connect coolify cloudflare-tunnel
   ```

1. Add a new public hostname for the tunnel:

   ```text
   Public hostname: *.<domain>
   Service: http://coolify-proxy:80
   ```

1. Add a DNS record for the new tunnel:

   ```text
   Type: CNAME
   Name: *
   Target: <tunnel-id>.cfargotunnel.com
   ```

1. Login into the Coolify dashboard.
1. Go to `Settings` -> `Configuration` -> `Instance Settings` and change the
   Instance's Domain to somethign like `http://coolify.<domain>`.
1. Click Save
1. Go to your localhost Server and change the wildcard domain to
   `http://<domain>`.
1. Test by going to `http://coolify.<domain>`.

## Verified recovery

On 9 November 2026, the Pi 5 at `192.168.8.142`, hostname `homelab`, ran Coolify 4.4.7 and `cloudflare/cloudflared:2026.10.3`. The tunnel container ran on `bridge` only. Logs reported `lookup coolify-proxy on 192.168.8.1:53: no such host`. Local app routes worked, but public Yamtrack returned 502.

Check attachment without printing container environment variables or token-bearing commands:

```bash
docker inspect --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' cloudflare-tunnel
```

If `coolify` is missing and the proxy still belongs to that network, repair it:

```bash
docker network connect coolify cloudflare-tunnel
```

This restored the apps. A subsequent `docker restart cloudflare-tunnel` retained `bridge coolify`; six public app roots returned 200 or login redirects after reconnection. Full host reboot recovery remains untested.

Docker is enabled at boot; the tunnel and proxy have restart policy `unless-stopped`. Preserve both `--restart unless-stopped` and `--network coolify` when recreating the tunnel. The historical command above now includes these settings. Network attachment survives restarting an existing container, but replacement must declare the network again. See [Docker network connection semantics](https://docs.docker.com/reference/cli/docker/network/connect/).

The original loss mechanism is unknown. A separate native `cloudflared.service` is also active; establish its purpose before changing or removing it. Keep existing tunnel tokens private and avoid copying full `docker inspect` or service command output into the notebook.

## Pending connector update

On **9 November 2026**, [upstream latest](https://api.github.com/repos/cloudflare/cloudflared/releases/latest) reported [2026.10.7](https://github.com/cloudflare/cloudflared/releases/tag/2026.10.7). The proposed Docker update is **2026.10.3 → 2026.10.7**, not an observed deployment. The historical `latest` command above is not an update instruction for the running container.

The Docker Registry manifest for `cloudflare/cloudflared:2026.10.7` was checked read-only and includes **linux/arm64** for the Pi 5. Its multi-platform digest is `sha256:4955524aeaa379e154023d5a027c250f7b35041a2e7e950cf13f144bc9b9c5ba`. Recheck before use:

```sh
docker manifest inspect cloudflare/cloudflared:2026.10.7
docker inspect --format '{{.Config.Image}} {{.Image}}' cloudflare-tunnel
docker inspect --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' cloudflare-tunnel
```

For separately approved maintenance, retain the old image ID and privately preserve the existing launch configuration and token for rollback. Recreate only this Docker connector using the explicit target tag or digest, its existing options, `--restart unless-stopped` and `--network coolify`. Do not copy the placeholder token from the historical example or change the separate native connector. Container replacement can briefly interrupt all routed applications.

Check container state, network attachment, the local proxy and every public application route, including login redirects. On failure, restore the saved image and configuration with the same network. Schedule full reboot recovery separately; it remains untested. No container was pulled, replaced or restarted during this documentation review.
