> Portainer was retired on both Pis on 11 November 2026. Do not reinstall it as part of routine maintenance. See [current status and recovery](../_reference/services.md#portainer-retirement).

> Historical installation recipe. Do not add human maintenance accounts to the Docker group or reinstall Portainer as a setup prerequisite. Use the [new-host guide](setup.md). The explicit retirement rollback below remains available.

# Installing Docker

1. Install Docker:

   ```bash
   curl -fsSL https://get.docker.com | sh
   ```

1. Add the user to the docker group:

   ```bash
    sudo usermod -aG docker $USER
   ```

1. Log out and log back in to apply the changes.
1. Install Portainer:

   ```bash
   sudo docker pull portainer/portainer-ce:latest
   sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
   ```

1. Access Portainer at `http://<rpi hostname>:9000`.
1. Create a new user and password.

## Restore the retired dashboard

Use this only to roll back the deliberate Portainer retirement on the selected Pi. Its container, image, and `portainer_data` volume were retained. On that Pi as the maintenance account:

```bash
	sudo docker update --restart=always portainer
	sudo docker start portainer
```

Check its endpoint and confirm that application containers remain unchanged. Do not recreate a Portainer stack or delete volumes as part of this rollback. The preceding installation recipe remains historical.
