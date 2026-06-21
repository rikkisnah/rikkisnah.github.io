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

Clone or update the repo under `/opt/rikkisnah.github.io`, then install the service:

```bash
cd /opt/rikkisnah.github.io/mcp_blog
uv sync
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
WorkingDirectory=/opt/rikkisnah.github.io/mcp_blog
ExecStart=/usr/local/bin/uv run rik-blog-mcp --repo-root /opt/rikkisnah.github.io --transport streamable-http --host 127.0.0.1 --port 8765
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/rikkisnah.github.io/mcp_blog/.venv /opt/rikkisnah.github.io/mcp_blog/uv.lock

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
        proxy_set_header Host $host;
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
sudo certbot --nginx -d mcp.rik-kisnah.ai
sudo systemctl reload nginx
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
