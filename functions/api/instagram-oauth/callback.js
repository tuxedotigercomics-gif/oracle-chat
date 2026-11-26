// Optional free OAuth callback for Oracle Chat.
//
// Set these as encrypted Cloudflare Pages secrets (never in the HTML):
//   META_APP_ID              public Meta app ID, digits only
//   META_APP_SECRET          app secret, server-side only
//   INSTAGRAM_REDIRECT_URI   exact callback URL registered in Meta
//   ORACLE_APP_ORIGIN        https://oracle-chat.pages.dev
//   INSTAGRAM_SCOPES         optional, defaults to basic + content publish
//
// The browser opens the Meta authorize URL itself. Meta returns here with a
// one-time code. This Function exchanges it and immediately hands the token to
// the opener with postMessage. Nothing is stored in the cloud, logged, or sent
// to a model prompt. The opener encrypts the token into its device vault.

const safeJson = (value) => JSON.stringify(value)
  .replace(/</g, "\\u003c")
  .replace(/>/g, "\\u003e")
  .replace(/&/g, "\\u0026");

function page(title, message, payload, targetOrigin) {
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title><style>body{font:15px/1.5 system-ui,sans-serif;background:#0e1512;color:#eaf3ed;margin:0;padding:32px}
.card{max-width:420px;margin:10vh auto;padding:24px;border:1px solid #35503f;border-radius:16px;background:#142019}
button{margin-top:16px;padding:9px 14px;border-radius:10px;border:0;background:#6cc38a;color:#07130c;font-weight:700;cursor:pointer}</style></head>
<body><div class="card"><h2>${title}</h2><p>${message}</p><button id="close" hidden>Close this window</button></div>
<script>
(function(){
  var payload = ${safeJson(payload)};
  var target = ${safeJson(targetOrigin)};
  if (window.opener) {
    try { window.opener.postMessage(payload, target); } catch (e) {}
  }
  var btn = document.getElementById('close');
  if (window.opener) { window.close(); } else { btn.hidden = false; btn.onclick = function(){ window.close(); }; }
})();
</script></body></html>`;
  return new Response(html, {
    status: 200,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "Referrer-Policy": "no-referrer",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

export async function onRequestGet(context) {
  const { env, request } = context;
  const url = new URL(request.url);
  const state = String(url.searchParams.get("state") || "").slice(0, 120);
  const error = String(url.searchParams.get("error") || "");
  const targetOrigin = String(env.ORACLE_APP_ORIGIN || url.origin).replace(/\/$/, "");
  const type = "oracle-instagram-oauth";

  if (!env.META_APP_ID || !env.META_APP_SECRET || !env.INSTAGRAM_REDIRECT_URI) {
    return page("Not configured", "The Instagram button is not configured on this host yet. You can still add your own token in My Connectors.",
      { type, state, ok: false, error: "not-configured" }, targetOrigin);
  }
  if (error || !state) {
    return page("Connection canceled", "Nothing was saved.",
      { type, state, ok: false, error: error || "missing-state" }, targetOrigin);
  }

  const code = String(url.searchParams.get("code") || "").slice(0, 500);
  if (!code) {
    return page("Missing code", "Meta did not return a code. Nothing was saved.",
      { type, state, ok: false, error: "missing-code" }, targetOrigin);
  }

  try {
    const body = new URLSearchParams({
      client_id: String(env.META_APP_ID),
      client_secret: String(env.META_APP_SECRET),
      grant_type: "authorization_code",
      redirect_uri: String(env.INSTAGRAM_REDIRECT_URI),
      code,
    });
    const res = await fetch("https://api.instagram.com/oauth/access_token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.access_token) {
      return page("Could not connect", "Meta did not return an access token. Nothing was saved.",
        { type, state, ok: false, error: "token-exchange-failed" }, targetOrigin);
    }

    let accessToken = String(data.access_token);
    let expiresIn = 0;
    try {
      const long = await fetch("https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=" + encodeURIComponent(accessToken));
      const ld = await long.json().catch(() => ({}));
      if (long.ok && ld.access_token) {
        accessToken = String(ld.access_token);
        expiresIn = Number(ld.expires_in) || 0;
      }
    } catch (e) {
      // Short-lived token still works; the long-lived refresh is best-effort.
    }

    return page("Connected", "Your own Instagram is now saved encrypted on this device. You can close this window.",
      { type, state, ok: true, accessToken, expiresIn, userId: String(data.user_id || "") }, targetOrigin);
  } catch (e) {
    return page("Could not connect", "The connection handoff failed. Nothing was saved.",
      { type, state, ok: false, error: "handoff-failed" }, targetOrigin);
  }
}
