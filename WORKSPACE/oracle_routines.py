#!/usr/bin/env python3
"""Web routines for Oracle Chat.

Non-secret settings (mail hosts, usernames, routine names, webhook labels) live
in oracle-routines.json. Secrets stay in the macOS Keychain and are fetched
through the bridge's credential lookup. This module NEVER returns a secret
value - only names, status and redacted results.
"""

import email as email_lib
import imaplib
import json
import urllib.error
import urllib.request
from email.header import decode_header, make_header
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
CFG_FILE = ROOT / "oracle-routines.json"
MAX_OUT = 8000


def load_config():
    try:
        cfg = json.loads(CFG_FILE.read_text())
        return cfg if isinstance(cfg, dict) else {}
    except Exception:
        return {}


def save_config(cfg):
    CFG_FILE.write_text(json.dumps(cfg, indent=2))


def _safe_error(exc, secrets=()):
    msg = f"{type(exc).__name__}: {exc}"
    for s in secrets:
        if s:
            msg = msg.replace(str(s), "[REDACTED]")
    return msg[:400]


def _decode(raw):
    try:
        return str(make_header(decode_header(raw or "")))
    except Exception:
        return str(raw or "")


def _body_of(msg):
    """Return the readable text of an email message."""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get_filename():
                    payload = part.get_payload(decode=True) or b""
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, "replace")
            return ""
        payload = msg.get_payload(decode=True) or b""
        charset = msg.get_content_charset() or "utf-8"
        return payload.decode(charset, "replace")
    except Exception:
        return ""


def _headers(msg):
    return {
        "from": _decode(msg.get("From")),
        "subject": _decode(msg.get("Subject")),
        "date": _decode(msg.get("Date")),
    }


def email_action(account, cred_get, action="summary", limit=10, uid=None, query=None):
    """Read email through IMAP. Credential names are resolved bridge-side."""
    cfg = load_config()
    acct = cfg.get("accounts", {}).get("email", {}).get(account)
    if not acct:
        return {"ok": False, "error": f"No email account named '{account}'. Add it in Routines."}
    host = acct.get("host")
    port = int(acct.get("port", 993))
    user = acct.get("user")
    cred = acct.get("password_cred")
    if not (host and user and cred):
        return {"ok": False, "error": "Account needs host, user and password_cred."}
    password = cred_get(cred)
    if not password:
        return {"ok": False, "error": f"Credential '{cred}' was not found in the vault."}

    conn = None
    try:
        conn = imaplib.IMAP4_SSL(host, port, timeout=25)
        conn.login(user, password)
        conn.select("INBOX")
        if action == "read":
            if not uid:
                return {"ok": False, "error": "read needs a uid from a check or summary."}
            typ, data = conn.fetch(str(uid), "(RFC822)")
            if typ != "OK" or not data or not data[0]:
                return {"ok": False, "error": f"Message {uid} was not found."}
            msg = email_lib.message_from_bytes(data[0][1])
            h = _headers(msg)
            text = _body_of(msg).strip()[:MAX_OUT]
            return {"ok": True, "result": f"From: {h['from']}\nSubject: {h['subject']}\nDate: {h['date']}\n\n{text}"}

        criteria = "UNSEEN" if action in ("summary", "check") else "ALL"
        if action == "search":
            criteria = f'TEXT "{str(query or "").replace(chr(34), "")}"'
        typ, data = conn.search(None, criteria)
        if typ != "OK":
            return {"ok": False, "error": "Mail search failed."}
        ids = (data[0].split() if data and data[0] else [])
        limit = max(1, min(int(limit or 10), 50))
        picked = ids[-limit:][::-1]
        label = {"summary": "unread", "check": "unread", "search": "matching"}.get(action, "recent")
        lines = [f"{account} — {len(picked)} {label} message(s)"]
        for mid in picked:
            typ, md = conn.fetch(mid, "(BODY.PEEK[HEADER])")
            if typ != "OK" or not md or not md[0]:
                continue
            h = _headers(email_lib.message_from_bytes(md[0][1]))
            lines.append(f"- [{mid.decode()}] {h['subject']} — {h['from']} ({h['date']})")
        if action == "summary" and not picked:
            lines.append("No unread mail.")
        lines.append("Ask me to read a message by its [number] for the full text.")
        return {"ok": True, "result": "\n".join(lines)}
    except Exception as exc:
        return {"ok": False, "error": _safe_error(exc, (password, user))}
    finally:
        if conn is not None:
            try:
                conn.logout()
            except Exception:
                pass


def webhook_post(name, cred_get, payload):
    """POST JSON to a private automation webhook (Make/Zapier/n8n)."""
    cfg = load_config()
    hook = cfg.get("webhooks", {}).get(name)
    if not hook:
        return {"ok": False, "error": f"No webhook named '{name}'. Add it in Routines."}
    cred = hook.get("cred")
    if not cred:
        return {"ok": False, "error": f"Webhook '{name}' has no credential name."}
    url = cred_get(cred)
    if not url:
        return {"ok": False, "error": f"Credential '{cred}' was not found in the vault."}
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.netloc:
        return {"ok": False, "error": "The webhook URL is not a valid http(s) URL."}
    if not cfg.get("dev_allow_local") and u.hostname in ("localhost", "127.0.0.1", "::1"):
        return {"ok": False, "error": "Local webhook URLs are blocked unless dev_allow_local is enabled."}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "OracleChat/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(MAX_OUT).decode("utf-8", "replace")
            return {"ok": True, "status": getattr(r, "status", 200), "result": body.replace(url, "[REDACTED]")[:MAX_OUT]}
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read(MAX_OUT).decode("utf-8", "replace")
        except Exception:
            pass
        return {"ok": False, "status": exc.code, "error": _safe_error(exc, (url,)) + " " + body.replace(url, "[REDACTED]")[:2000]}
    except Exception as exc:
        return {"ok": False, "error": _safe_error(exc, (url,))}
