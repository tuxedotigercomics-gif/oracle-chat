# Web Routines — Oracle Chat

This adds **real web actions** to the Mac/host build: reading email, posting
through an automation webhook, and running recorded browser routines. The
model picks a routine and supplies the text; the bridge executes it.

## Where this runs

| | Mac / host build | Phone / static guest build |
|---|---|---|
| Email via IMAP | Yes | No |
| Webhook posting | Yes | No |
| Browser routines (Playwright) | Yes | No |
| Vault | macOS Keychain | Device-local encrypted vault |

This is deliberate. A static phone page cannot run a background browser, and
guests must never be able to use the owner's credentials. iOS Safari offers no
browser-automation API to a website — that would need a native app or
Shortcuts. The Mac bridge is the "model's computer."

## Security model

- The model only ever sees credential **names**.
- Secrets (passwords, tokens, webhook URLs) go in **Profile → Credential
  Vault** and stay in the macOS Keychain.
- `oracle-routines.json` contains **names and non-secret settings only**. Never
  paste a secret into it or into chat.
- Browser steps can use `{{cred:NAME}}` — the bridge fills the value locally and
  redacts every result. The value is never returned or logged.
- All routine endpoints reject guest sessions.
- Posting/sending/deleting is a real side effect. Tell the model explicitly
  when you want it to act ("post this now"); otherwise it should confirm first.

## Setup

Open **Profile → Web Routines**. The configuration is a JSON text editor; save
reloads it into the bridge immediately.

### 1. Email (IMAP)

Put the password in the vault under a name you choose, e.g. `gmail-app`.

```json
{
  "accounts": {
    "email": {
      "gmail": {
        "host": "imap.gmail.com",
        "port": 993,
        "user": "you@gmail.com",
        "password_cred": "gmail-app"
      }
    }
  }
}
```

For Gmail, use an **App Password**, not your account password. Then ask:

- "check my gmail" / "summarize my unread email"
- "read message 123 from gmail"

Actions: `summary` (unread digest, default), `check` (unread list), `read`
(needs `uid`), `search` (needs `query`).

### 2. Webhook (Make / Zapier / n8n)

Create a scenario in your automation tool that receives a webhook and posts to
Instagram/Facebook/etc. Store the **webhook URL** in the vault under a name,
e.g. `social-webhook`.

```json
{
  "webhooks": {
    "social": { "cred": "social-webhook" }
  }
}
```

Then ask: "post this to social: ..." or "schedule this for tomorrow at 9".
The bridge POSTs your JSON payload to the webhook; your automation service
handles the login and the actual post. This avoids storing platform passwords
in Oracle and avoids Meta app review.

### 3. Browser routines (Playwright)

Playwright and its Chromium are installed in the project-local `.oracle-venv`.
Enable it and define recorded steps:

```json
{
  "browser": {
    "enabled": true,
    "routines": {
      "example-login": {
        "url": "https://example.com/login",
        "steps": [
          { "action": "fill", "selector": "input[name=username]", "value": "{{cred:site-user}}" },
          { "action": "fill", "selector": "input[name=password]", "value": "{{cred:site-pass}}" },
          { "action": "click", "selector": "button[type=submit]" },
          { "action": "wait", "selector": "#dashboard", "timeout": 20000 },
          { "action": "text", "selector": "#dashboard" }
        ]
      }
    }
  }
}
```

Supported steps: `goto`, `fill`, `click`, `press`, `wait`, `text`, `sleep`,
`screenshot`. Values support `{{cred:NAME}}` and `{{param:name}}`.

Then ask: "run the example-login routine with param text = hello".

You can also ask the model to open a page directly:
`TOOL: {"tool":"browser","action":"open","url":"https://example.com"}`.

## Honest limitations

- The local 3B model is reliable at **choosing a defined routine and filling
  text**, not at free-form multi-step browsing. Define the routine once.
- Automating logins to Instagram/Facebook/email can violate their terms and
  get accounts limited. Prefer official APIs/IMAP/webhooks where possible.
- Browser routines are headless and selector-based; sites that change their
  markup will need the selectors updated.
- `dev_allow_local` exists only for local testing; leave it `false`.

## Files

- `oracle_routines.py` — config, email (IMAP), webhook posting
- `oracle_browser.py` — Playwright routine runner, credential placeholders
- `oracle-routines.json` — non-secret configuration
- `.oracle-venv/` — local Playwright install (not published)
