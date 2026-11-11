> Retired access path. The public SSH route and DNS record were removed on 10 November 2026 after private OpenSSH access passed. Use [ordinary SSH over Tailscale](../_reference/ssh-access.md). The commands below are historical, not setup instructions for the current lab.

> Historical Raspberry Pi setup. Do not use this as the HP/Omarchy security baseline. For the arriving HP, start with [its preparation checklist](../home-lab/preparation.md).

# Setup SSH through Cloudflare

1. (From SSH) Cloudflare Repository on the Raspberry Pi:

   ```bash
    sudo apt install curl lsb-release
    curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-archive-keyring.gpg >/dev/null
    echo "deb [signed-by=/usr/share/keyrings/cloudflare-archive-keyring.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee  /etc/apt/sources.list.d/cloudflared.list
   ```

1. Install Cloudflare:

   ```bash
   sudo apt update
   sudo apt install cloudflared
   ```

1. Create Cloudflare account and register a domain.
1. Open Zero Trust tab and create a new tunnel.
1. Use the add service command to add the tunnel to the raspberry pi:

   ```bash
   sudo cloudflared service install <SERVICE KEY>
   ```

1. Add a subdomain for the ssh tunnel:

   ```text
   Public hostname: machine.<domain>
   Service: ssh://localhost:22
   ```

1. Add access to ssh config, edit `~/.ssh/config` with following:

   ```text
   Host machine.<domain>
     ProxyCommand /opt/homebrew/bin/cloudflared access ssh --hostname %h
   ```

1. Test the tunnel:

   ```bash
   ssh <username>@machine.<domain>
   ```
