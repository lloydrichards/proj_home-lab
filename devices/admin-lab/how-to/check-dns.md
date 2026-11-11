# Check Pi-hole without changing the service

Use these read-only checks to separate DNS failure, container health, and dashboard failure. They do not install, restart, or update Pi-hole. Run client checks from the Mac or another intended DNS client; run Docker checks on admin-lab as `lloyd` with password-required sudo.

## Select the client path

1. Find admin-lab's current LAN address in the [service register](../../_reference/services.md#services). Use the LAN address when testing LAN DNS. A Tailscale test covers a different path.
2. On the client, set the address for this shell:

   ```bash
	printf 'Pi-hole address to test: '
	read -r PIHOLE_IP
   ```

3. If `dig` is available, query that resolver explicitly over UDP and TCP:

   ```bash
	dig +time=3 +tries=1 @"$PIHOLE_IP" example.com A
	dig +tcp +time=3 +tries=1 @"$PIHOLE_IP" example.com A
   ```

   A successful response includes `status: NOERROR`, an answer, and the selected server address. A timeout indicates this path failed; it does not prove the container stopped. Record the client and path with the result.
4. Query a domain known to be blocked by this Pi's current policy:

   ```bash
	printf 'Domain known to be blocked here: '
	read -r BLOCKED_DOMAIN
	dig +time=3 +tries=1 @"$PIHOLE_IP" "$BLOCKED_DOMAIN" A
   ```

   Compare the result with the configured blocking mode. Do not assume every installation returns `0.0.0.0`, or use an arbitrary domain as proof of filtering.

## Check the web endpoint separately

On the same client, request the documented dashboard path:

```bash
	curl --connect-timeout 3 --max-time 10 -sS -o /dev/null \
	  -w 'HTTP %{http_code}\n' "http://$PIHOLE_IP/admin/"
```

An HTTP response establishes web reachability, not successful administrator login. A redirect needs its destination checked separately. Avoid publishing cookies, credentials, or full dashboard output.

## Inspect the container

1. Connect through the [SSH guide](../../../docs/how-to/connect-with-ssh.md), then verify the host:

   ```bash
	hostname -s
   ```

   Continue only if it prints `admin-lab`.
2. List containers and select the Pi-hole name:

   ```bash
	sudo docker ps -a --format '{{.Names}} | {{.Image}} | {{.Status}}'
	printf 'Pi-hole container name: '
	read -r PIHOLE_CONTAINER
   ```

3. Inspect its state without dumping environment variables or credentials:

   ```bash
	sudo docker inspect --format \
	  'State={{.State.Status}} Health={{if .State.Health}}{{.State.Health.Status}}{{else}}not configured{{end}} Image={{.Config.Image}} ImageID={{.Image}}' \
	  "$PIHOLE_CONTAINER"
   ```

Keep DNS, web, and health results separate in the [service register](../../_reference/services.md). If a check fails, retain independent SSH access and investigate the path before changing DNS or restarting the container. The [DNS explanation](../explanations/dns-service.md) lists the unresolved dependencies.
