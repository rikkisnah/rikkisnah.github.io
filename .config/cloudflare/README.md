# Cloudflare Local Access

Wrangler and Cloudflare API calls should use a local environment variable:

```bash
export CLOUDFLARE_API_TOKEN="..."
```

Or source a local ignored file:

```bash
cp .config/cloudflare/env.example .config/cloudflare/cloudflare.env
$EDITOR .config/cloudflare/cloudflare.env
set -a
. .config/cloudflare/cloudflare.env
set +a
```

Required token permissions for `rik-kisnah.ai`:

- `Zone:Read`
- `DNS:Edit`

Do not commit real tokens or Cloudflare account state.
