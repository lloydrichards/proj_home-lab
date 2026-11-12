# Set up Pi-hole as the LAN DNS server

Configure the existing Pi-hole service on admin-lab and have the Fibre X6 router supply its address to LAN clients through IPv4 DHCP.

This guide starts with Pi-hole already deployed in Docker. It does not cover installing the container or rebuilding admin-lab. Keep deployment paths and actual settings in the private service register described by the [public register](../../_reference/services.md#pi-hole-network-configuration).

IPv6 DNS still uses the router and can bypass Pi-hole. This procedure configures IPv4 DNS only. See [how DNS fits into the lab](../explanations/dns-service.md) for that limitation.

## Before you start

Have the router administrator login and the saved Pi-hole password available. Connect admin-lab to the LAN by Ethernet. Keep private maintenance access through the [SSH guide](../../../docs/how-to/connect-with-ssh.md).

This guide uses example addresses: `192.168.1.1` for the router and `192.168.1.7` for Pi-hole. Substitute your own addresses throughout, including URLs and expected command output. Keep actual addresses and the Ethernet MAC in your ignored local inventory.

Open the router's LAN address. Check **DHCP Leases** for admin-lab's current address.

## Reserve admin-lab's address

1. Open **Network Settings → LAN IP → IP Reservation** in the router.
2. Select **Add Reserved Address**.
3. Choose **admin-lab** from the device list.
4. Confirm the Ethernet MAC matches admin-lab's network interface. Obtain the actual value from your private inventory.
5. Set the reserved address to `192.168.1.7`. Do not use an address assigned to another device.
6. Enable the reservation and click **Apply**.
7. Confirm **Data successfully saved** and the saved reservation.

Keep the router's LAN address and DHCP service enabled. The router supplies client addresses; Pi-hole supplies DNS.

## Configure Pi-hole

1. Open `http://192.168.1.7/admin/` and log in with the saved Pi-hole password.
2. Open **Settings → DNS** and check the upstream DNS servers. The existing service uses Cloudflare at `1.1.1.1` and `1.0.0.1`.
3. Keep Pi-hole's DHCP server disabled because the Fibre X6 already provides DHCP.
4. Confirm that blocking is active and the configured lists contain domains.

For this Docker deployment, DNS must be reachable on both TCP and UDP port 53. The web dashboard uses port 80. Use [Check Pi-hole](check-dns.md) if either endpoint is unavailable.

## Set the router's IPv4 DNS server

1. While logged in to the router, open `http://192.168.1.1/2.0/gui/#/mybox/dns/server`.
2. Confirm that the page is **Static DNS Server Configuration**. This form loads directly on the installed Fibre X6 even though it is absent from the normal menu.
3. Enter `192.168.1.7` as **Primary DNS Server**.
4. Leave **Secondary DNS Server** empty. A public secondary resolver would give clients another path around Pi-hole.
5. Click **Apply**.
6. Confirm **Data successfully saved**.

If this form is unavailable on another firmware version, stop here. This guide does not substitute browser-console changes.

To return to the router's default IPv4 DNS advertisement, clear both DNS fields and click **Apply**. The form states that empty fields restore automatic settings using the box IP.

## Let clients obtain DNS automatically

Use automatic DNS on each client, then renew its DHCP lease or reconnect it to the network. Existing leases can retain the previous DNS setting until renewal.

On the Mac, remove any manual Wi-Fi DNS override if one is present:

```bash
	sudo networksetup -setdnsservers "Wi-Fi" Empty
```

Open **System Settings → Wi-Fi → Details → TCP/IP** and renew the DHCP lease.

## Verify the setup

On the Mac, check the DNS address supplied by DHCP:

```bash
	ipconfig getpacket en0 | grep domain_name_server
```

Use your Wi-Fi interface if it differs from `en0`. Expect `domain_name_server` to contain `192.168.1.7`.

Check the effective resolvers and request a name lookup:

```bash
	scutil --dns
	dscacheutil -q host -a name www.ietf.org
```

Open Pi-hole's **Query Log** and refresh it. Look for the requested domain and the Mac's client address. A VPN or application-specific resolver can override the LAN DNS setting; the DHCP result alone does not prove that every lookup uses Pi-hole.

The current resolver list also contains the router's IPv6 DNS address. Full network filtering remains incomplete. IPv6 router settings are outside this guide's accepted scope.

For a filtering check, use a domain known to be blocked by the configured lists and follow [Check Pi-hole](check-dns.md). A dedicated blocked-domain test and persistence across a router reboot have not yet been verified.
