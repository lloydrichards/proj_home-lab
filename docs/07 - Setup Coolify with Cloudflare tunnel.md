# Setup Coolify with Cloudflare tunnel

1. Buy or add a domain to Cloudflare.
1. Add a new tunnel in the Zero Trust tab (separate from SSH in
   [#04](./04%20-%20Setup%20SSH%20through%20Cloudflare.md)).
1. Use the Docker image to add the new tunnel, be sure to name it:

   ```bash
   docker run -d --name cloudflare-tunnel cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <TUNNEL_TOKEN>
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
