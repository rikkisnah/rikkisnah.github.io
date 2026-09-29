# Public Blog MCP Deployment

Target: `https://mcp.rik-kisnah.ai/mcp`

This endpoint is intentionally public and unauthenticated. It must remain read-only and limited to public blog content.

## DNS

In Cloudflare DNS:

```text
Type: A
Name: mcp
Content: 129.146.101.64
Proxy: Enabled or DNS only
```

Do not change `worldcup.rik-kisnah.ai`.

## VM Setup

```bash
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone or update the repo under `/opt/rikkisnah.github.io` (owned by `ubuntu`), then install the service:

```bash
sudo git clone https://github.com/rikkisnah/rikkisnah.github.io.git /opt/rikkisnah.github.io
sudo chown -R ubuntu:ubuntu /opt/rikkisnah.github.io
cd /opt/rikkisnah.github.io/mcp_blog
uv sync
```

## Host firewall

The Ubuntu image ships an iptables INPUT chain that only allows port 22. Open 80 and 443 above the final REJECT rule and persist it (the OCI security list already allows both):

```bash
for p in 80 443; do
  sudo iptables -I INPUT 5 -p tcp -m state --state NEW -m tcp --dport $p -j ACCEPT
done
sudo apt-get install -y iptables-persistent
sudo netfilter-persistent save
```

## systemd

Create `/etc/systemd/system/rik-blog-mcp.service`:

```ini
[Unit]
Description=Rik Blog Public MCP
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/rikkisnah.github.io/mcp_blog
# Run the venv entry point directly. `uv run` needs a writable ~/.cache/uv,
# which ProtectHome=true blocks.
ExecStart=/opt/rikkisnah.github.io/mcp_blog/.venv/bin/rik-blog-mcp --repo-root /opt/rikkisnah.github.io --transport streamable-http --host 127.0.0.1 --port 8765
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/rikkisnah.github.io/mcp_blog/.venv

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rik-blog-mcp
sudo systemctl status rik-blog-mcp
```

## nginx

Create `/etc/nginx/sites-available/mcp.rik-kisnah.ai`:

```nginx
limit_req_zone $binary_remote_addr zone=mcp_public:10m rate=30r/m;

server {
    listen 80;
    server_name mcp.rik-kisnah.ai;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name mcp.rik-kisnah.ai;

    ssl_certificate /etc/letsencrypt/live/mcp.rik-kisnah.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mcp.rik-kisnah.ai/privkey.pem;

    location = /healthz {
        add_header Content-Type text/plain;
        return 200 "ok\n";
    }

    location /mcp {
        limit_req zone=mcp_public burst=20 nodelay;
        proxy_pass http://127.0.0.1:8765/mcp;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_read_timeout 300s;
        # The MCP SDK's DNS-rebinding guard only accepts localhost Host values.
        # Passing the public hostname returns "421 Invalid Host header".
        proxy_set_header Host 127.0.0.1:8765;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        return 404;
    }
}
```

Enable TLS and nginx:

```bash
sudo ln -s /etc/nginx/sites-available/mcp.rik-kisnah.ai /etc/nginx/sites-enabled/mcp.rik-kisnah.ai
sudo nginx -t
sudo certbot --nginx -d mcp.rik-kisnah.ai --redirect
sudo systemctl reload nginx
```

Cloudflare proxies the hostname, so the origin must serve TLS on 443 or Cloudflare returns 521. Certbot's HTTP-01 challenge works through the proxy. Renewal runs from `certbot.timer`.

## Content refresh

The VM serves whatever is checked out under `/opt/rikkisnah.github.io`. A cron job in the `ubuntu` crontab fetches `origin/main` every 15 minutes and, when it changed, resets the checkout and restarts the service. It relies on `/etc/sudoers.d/rik-blog-mcp` allowing a passwordless `systemctl restart rik-blog-mcp`:

```cron
*/15 * * * * cd /opt/rikkisnah.github.io && git fetch -q origin main && [ $(git rev-parse HEAD) != $(git rev-parse FETCH_HEAD) ] && git reset -q --hard FETCH_HEAD && sudo -n systemctl restart rik-blog-mcp # rik-blog-refresh
```

To refresh immediately after publishing a post:

```bash
ssh ubuntu@129.146.101.64 'cd /opt/rikkisnah.github.io && git fetch -q origin main && git reset -q --hard FETCH_HEAD && sudo -n systemctl restart rik-blog-mcp'
```

## Verification

```bash
curl -I https://mcp.rik-kisnah.ai/healthz
```

Expected: HTTP success.

Connect MCP Inspector to:

```text
https://mcp.rik-kisnah.ai/mcp
```

Confirm only these tools appear:

- `list_posts`
- `latest_posts`
- `search_posts`
- `get_post`

Confirm write/admin/shell/Git/deploy tools are unavailable.

## Client Install

Codex remote config:

```toml
[mcp_servers.rik_blog]
url = "https://mcp.rik-kisnah.ai/mcp"
enabled_tools = ["list_posts", "latest_posts", "search_posts", "get_post"]
default_tools_approval_mode = "auto"
```

Claude Code remote install:

```bash
claude mcp add --transport http rik_blog https://mcp.rik-kisnah.ai/mcp
```

For local stdio installs in either client, use the examples in `mcp_blog/client-configs/`.
