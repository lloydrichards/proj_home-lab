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
