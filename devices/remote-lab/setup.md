# Build a Pi application host

This guide connects the steps for a private maintenance path, Coolify application hosting, and recoverable data on a replacement Pi. The complete sequence has not been rehearsed. Individual access, routing, and backup checks are recorded in the [service register](../_reference/services.md).

Use a spare Pi and storage while the existing host stays available. You need a trusted maintenance client, console access, your own SSH key, a Tailscale account, and a Cloudflare domain. For recovery, also retrieve the restic password, original Coolify `APP_KEY`, connector credentials, and compatible database images before touching production.

## Prepare the operating system

1. Use [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#raspberry-pi-imager) to install a supported 64-bit OS on the spare storage. Recheck OS and Coolify ARM64 compatibility before selecting the image.
2. Choose a temporary hostname and a maintenance account. The installed lab uses `remote-lab` and `lloyd`; keep the temporary host distinct until cutover.
3. Configure Ethernet and the maintenance public key. Keep the private key on the maintenance client.
4. Boot with console access available. Connect to the address assigned to the new Pi, then check its identity and architecture:

```bash
	hostname -s
	uname -m
	cat /etc/os-release
```

Expect the temporary hostname and a 64-bit architecture compatible with the selected images. On a Debian-based installation, update packages:

```bash
	sudo apt update
	sudo apt upgrade
```

## Establish private maintenance access

1. Install and enroll Tailscale using its [Linux installation instructions](https://tailscale.com/docs/install/linux) for the selected OS.
2. Follow [Connect with SSH](../../docs/how-to/connect-with-ssh.md) to pin the new host key and test a fresh maintenance login.
3. Confirm password-required `sudo` from that login. Keep human maintenance outside the Docker group.
4. Verify the intended Tailscale grants and actual reachability from the maintenance client. Preserve console access before tightening SSH.

Expect a fresh private login and successful administrative access before proceeding. Do not copy the [historical SSH configuration](ssh-hardening.md). It does not represent the installed baseline or Coolify's deployment exception.

## Establish the deployment controller

1. Recheck Coolify's supported OS, ARM64 images, and installation procedure at [Coolify documentation](https://coolify.io/docs/).
2. Inspect the installer and its required privileges before running it on the spare host. Follow the selected release's Docker prerequisites.
3. Open the private dashboard. Create the administrator account and configure the local deployment server.
4. Verify the deployment connection and one disposable app through private access. Check its container health and response separately.

Coolify's current root deployment connection is an intentional host-control exception. Preserve the human maintenance account separately. The [hosting explanation](explanations/application-hosting.md) describes the distinction.

Do not use the old [Docker and Portainer recipe](docker.md) as a prerequisite. Portainer is retired, and human Docker-group membership is outside the current baseline. The [old Coolify installation note](coolify.md) is historical, not a version-pinned installer contract.

## Choose new workloads or recovery

For a new installation, create a disposable application and persistent storage first. Confirm its data survives a controlled redeployment before adding production workloads.

For replacement recovery, follow [Restore Pi application data](how-to/restore-backups.md). Keep the restored controller and apps private. Restore compatible data and credentials before reconnecting source integrations or enabling deployments. A fresh controller with an unrelated `APP_KEY` cannot decrypt the original saved credentials.

Do not apply the [historical PostgreSQL Compose recipe](postgres.md) to restored data. Its floating image and published database port are not the current application database contract. Preserve the observed major version, explicit volume mapping, and image identity during recovery.

## Connect public routing

1. Follow [Route Coolify through Cloudflare Tunnel](coolify-cloudflare.md) with a separate test hostname.
2. Check an app through public HTTPS. Check the dashboard's Access challenge from a private browser window.
3. If using a GitHub App, test a signed event separately from the browser callback and ping handler.
4. Confirm the connector and proxy retain their network declarations after container replacement.

Expect the app to load publicly and the dashboard to require the intended identity. Keep the retired [public SSH route](cloudflare-ssh.md) absent.

## Prove recovery before cutover

1. Adapt the lab-specific inputs in [Configure Pi backups](how-to/configure-backups.md), then complete the local and cloud restore checks.
2. Test reboot recovery on the spare host. Check private SSH, the dashboard, app data, and public routing afterward.
3. During an agreed maintenance window, stop production writes before the final data transfer. Verify restored login and editing before directing production traffic to the replacement.
4. Keep the original host and recovery data available until the replacement passes its checks.

Whole-host cutover and reboot recovery remain unverified for this lab. A failed check means keeping production on the original host. Use the [backup operating guide](how-to/check-backups.md) for later checks and failures.
