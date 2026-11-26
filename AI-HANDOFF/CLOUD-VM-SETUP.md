# Cloud VM setup — free Cloudflare D1

The owner asked for a cloud brain that keeps working when the Mac/PC is off.
GitHub is the source and deploy history, but **GitHub Pages cannot run a live
VM**. Cloudflare Pages is already serving the app, so the free D1 database is
the correct always-on store for non-secret owner workspace state.

## What is stored

Only the owner's bot workspace snapshot:

- room names, titles, descriptions and remembered preferences
- non-secret messages and folder layout
- active room id

Never stored at the edge:

- vault entries or API keys
- host tool results or credential values
- guest sessions (they stay on the guest's own device)

The app generates a random local key (`oracle.cloud.key`). Anyone without that
key cannot read that snapshot. Treat it as a convenience backup, not a login.

## One-time dashboard setup (free)

1. Open Cloudflare dashboard → **Workers & Pages** → **D1**.
2. Create a database named `oracle-chat-cloud`.
3. Open the `oracle-chat` Pages project → **Settings** → **Bindings**.
4. Add a **D1 database** binding:
   - Variable name: `ORACLE_DB`
   - D1 database: `oracle-chat-cloud`
   - Add it to both **Production** and **Preview**.
5. Redeploy the Pages project (push to GitHub is enough).

No API token, secret or paid plan is needed. The free D1 allowance is
5 GB storage, 5 million row reads/day and 100,000 row writes/day — far above
this app's small workspace snapshots.

## Verify

After redeploy:

```sh
curl -s 'https://oracle-chat.pages.dev/api/cloud-state?key=cs-harness-check-123'
```

Expected when the binding is live: `{"ok":true,"state":null}`.
Expected before setup: `{"ok":false,"code":"binding-missing",...}` with HTTP 200
(a 503 would be logged by the browser as a console error). The app falls back
silently to device-local state either way.

Current status: **bound and verified on 2026-11-26**. The free D1 database
`oracle-chat-cloud` is bound as `ORACLE_DB` to both Production and Preview on
the `oracle-chat` Pages project. After the redeploy, the canonical endpoint
returned `{"ok":true,"state":null}`. No further dashboard action is needed.

The backup GitHub Pages host has no Functions runtime, so `/api/cloud-state`
returns 404 there and the app simply keeps working offline.
