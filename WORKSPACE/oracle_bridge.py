#!/usr/bin/env python3
"""
Oracle Chat bridge.

Serves the chat UI and forwards messages to either:
  - local: Ollama qwen2.5:3b (runs offline on this Mac)
  - cloud: OpenCode's free models (Big Pickle etc.) via the bundled CLI

Also provides a vault backed by macOS Keychain. Secrets never leave this
process toward the model: the model only ever sees credential NAMES. When a
`[[USE:key|url]]` marker appears, this bridge resolves the secret from the
Keychain and performs the request server-side, returning only a redacted
result.

Binds to 127.0.0.1 only. Uses Python stdlib only.
"""

import glob
import json
import os
import re
import secrets
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import oracle_routines
import oracle_browser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
UI_FILE = ROOT / "Oracle-Chat-Live.html"
PORT = 8765
OLLAMA_URL = "http://127.0.0.1:11434"
LOCAL_MODEL = "qwen2.5:3b"
DEEP_MODEL = "qwen3:4b"
VISION_MODEL = "qwen2.5vl:3b"
CLOUD_MODEL = "big-pickle"
VAULT_PREFIX = "oracle-vault:"
SKILLS_FILE = ROOT / "oracle-skills.json"
TOOLS_MODE_FILE = ROOT / "oracle-tools-mode.json"
KNOWLEDGE_DIR = ROOT / "oracle-knowledge"
MEMORY_FILE = KNOWLEDGE_DIR / "memories.md"
SHARE_DIR = ROOT / "oracle-shared"
SHARE_FILE = SHARE_DIR / "sessions.json"
ROUTINES_FILE = oracle_routines.CFG_FILE
COMPUTER_FILE = ROOT / "oracle-computer-state.json"
STARTED = time.time()

USE_RE = re.compile(r"\[\[USE:([^|\]]+)\|([^\]]+)\]\]")
TOOL_RE = re.compile(r"^\s*TOOL:\s*(\{.*\})\s*$")

MAX_READ = 20000
MAX_OUT = 8000
MAX_WRITE = 50000
MAX_PATCH = 50000
BACKUP_DIR = ROOT / ".oracle-backups"
BLOCKED_SHELL = (
    "sudo", "rm -rf", "rm -r ", "mkfs", "dd if=", "shutdown", "restart",
    "killall", "security ", "keychain", "oracle-vault", "printenv", "env ",
    "..", "~/.", "$home/.", "/etc/", "/var/", "id_rsa", ".env",
    "credentials", "password", "token", "chmod 777", "curl |", "wget |",
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def find_cli():
    hits = glob.glob(str(Path.home() / "Library/Application Support/ai.opencode.desktop/cli/*/opencode-cli"))
    if not hits:
        return None
    return sorted(hits)[-1]


def cli(api_method, path, data=None, timeout=120):
    exe = find_cli()
    if not exe:
        raise RuntimeError("OpenCode CLI not found")
    cmd = [exe, "api", api_method, path]
    if data is not None:
        cmd += ["--data", json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout)[:300])
    j = json.loads(r.stdout)
    return j.get("data", j) if isinstance(j, dict) else j


# OpenCode's /api/model catalog marks free models with zero cost. Pick the
# newest active free chat model automatically, and refresh on a free-limit so a
# quota-exhausted model is replaced without any user action.
CLOUD_MODEL_CACHE = {"model": "", "updated": 0.0, "models": []}
CLOUD_MODEL_TTL = 6 * 60 * 60


def _model_cost_is_free(cost):
    if not isinstance(cost, dict):
        return False
    vals = [cost.get("input"), cost.get("output")]
    cache = cost.get("cache")
    if isinstance(cache, dict):
        vals += [cache.get("read"), cache.get("write")]
    for v in vals:
        if v in (None, 0, 0.0, "0", "0.0"):
            continue
        try:
            if float(v) == 0:
                continue
        except (TypeError, ValueError):
            pass
        return False
    return True


def cloud_models(force=False, exclude=()):
    """Return (active model id, short free-model list) from OpenCode's catalog."""
    excluded = {exclude} if isinstance(exclude, str) else set(exclude or ())
    now = time.time()
    cached = CLOUD_MODEL_CACHE.get("model") or ""
    if (not force and cached and cached not in excluded
            and now - float(CLOUD_MODEL_CACHE.get("updated") or 0) < CLOUD_MODEL_TTL):
        return cached, CLOUD_MODEL_CACHE.get("models") or []

    try:
        data = cli("get", "/api/model", timeout=20)
        items = data.get("data") if isinstance(data, dict) else data
        if not isinstance(items, list):
            items = []
        free = []
        for m in items:
            if not isinstance(m, dict):
                continue
            if m.get("providerID") != "opencode" or m.get("type") not in (None, "chat"):
                continue
            if m.get("status") not in (None, "active") or m.get("enabled") is False:
                continue
            cost = m.get("cost")
            costs = cost if isinstance(cost, list) else [cost]
            if not costs or not all(_model_cost_is_free(c) for c in costs):
                continue
            mid = str(m.get("modelID") or m.get("id") or "").strip()
            if not mid or mid in excluded:
                continue
            tm = m.get("time") if isinstance(m.get("time"), dict) else {}
            lim = m.get("limit") if isinstance(m.get("limit"), dict) else {}
            free.append({
                "id": mid,
                "name": str(m.get("name") or mid),
                "released": int(tm.get("released") or 0),
                "context": int(lim.get("context") or 0),
            })
        free.sort(key=lambda x: (x["released"], x["context"], x["id"]), reverse=True)
        if free:
            CLOUD_MODEL_CACHE.update(
                model=free[0]["id"], updated=now,
                models=[{k: v for k, v in m.items()
                         if k in ("id", "name", "released", "context")}
                        for m in free[:8]],
            )
            return free[0]["id"], CLOUD_MODEL_CACHE["models"]
    except Exception:
        pass

    models = CLOUD_MODEL_CACHE.get("models") or []
    still_free = [m for m in models
                  if isinstance(m, dict) and m.get("id") and m["id"] not in excluded]
    if still_free:
        CLOUD_MODEL_CACHE.update(model=still_free[0]["id"], updated=now)
        return still_free[0]["id"], models
    fallback = CLOUD_MODEL if CLOUD_MODEL not in excluded else ""
    return fallback, models


def kv_get(key):
    """Read a secret from Keychain. Never log or return it to the model."""
    svc = VAULT_PREFIX + key
    r = subprocess.run(
        ["security", "find-generic-password", "-a", os.environ.get("USER", "user"),
         "-s", svc, "-w"],
        capture_output=True, text=True, timeout=20,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip("\n")


def kv_set(key, value):
    svc = VAULT_PREFIX + key
    r = subprocess.run(
        ["security", "add-generic-password", "-a", os.environ.get("USER", "user"),
         "-s", svc, "-w", value, "-U"],
        capture_output=True, text=True, timeout=20,
    )
    return r.returncode == 0, (r.stderr or "").strip()[:200]


def kv_delete(key):
    svc = VAULT_PREFIX + key
    r = subprocess.run(
        ["security", "delete-generic-password", "-a", os.environ.get("USER", "user"), "-s", svc],
        capture_output=True, text=True, timeout=20,
    )
    return r.returncode == 0


def kv_list():
    """List credential names by scanning Keychain metadata for our prefix."""
    r = subprocess.run(
        ["security", "dump-keychain"],
        capture_output=True, text=True, timeout=30,
    )
    names = set()
    for m in re.finditer(r'"svce"<blob>="(' + re.escape(VAULT_PREFIX) + r'[^"]+)"', r.stdout):
        names.add(m.group(1)[len(VAULT_PREFIX):])
    return sorted(names)


def skill_list():
    try:
        return json.loads(SKILLS_FILE.read_text())
    except Exception:
        return []


def skill_save(skills):
    SKILLS_FILE.write_text(json.dumps(skills, indent=2))


def tools_mode():
    """auto = local model may run sandboxed tools without a prompt; ask = approval cards."""
    try:
        return json.loads(TOOLS_MODE_FILE.read_text()).get("mode", "auto")
    except Exception:
        return "auto"


def set_tools_mode(mode):
    mode = "ask" if str(mode).lower() in ("ask", "ask-first", "approval") else "auto"
    TOOLS_MODE_FILE.write_text(json.dumps({"mode": mode}, indent=2))
    return mode


def computer_load():
    """Owner-only Computer panel state. Never contains a secret value."""
    try:
        x = json.loads(COMPUTER_FILE.read_text(encoding="utf-8"))
    except Exception:
        x = {}
    if not isinstance(x, dict):
        x = {}
    def names(key):
        return sorted({str(v).strip()[:80] for v in (x.get(key) or [])
                       if isinstance(v, (str, int, float)) and str(v).strip()})[:100]
    connectors = []
    for c in (x.get("connectors") or []):
        if not isinstance(c, dict):
            continue
        name = str(c.get("name", "")).strip()[:80]
        if not name:
            continue
        raw = str(c.get("target", "")).strip()
        host = ""
        if raw:
            parsed = urlparse(raw if "://" in raw else "https://" + raw)
            host = parsed.hostname or ""
        connectors.append({"name": name, "kind": str(c.get("kind", "custom"))[:30],
                           "targetHost": host[:120]})
    forms = []
    for f in (x.get("secureForms") or []):
        if not isinstance(f, dict):
            continue
        name = str(f.get("name", "")).strip()[:80]
        if not name:
            continue
        fields = sorted({str(v).strip()[:60] for v in (f.get("fields") or [])
                         if isinstance(v, (str, int, float)) and str(v).strip()})[:20]
        forms.append({"name": name, "fields": fields})
    return {"pausedRoutines": names("pausedRoutines"),
            "connectors": connectors[:50], "secureForms": forms[:50]}


def computer_save(state):
    COMPUTER_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def computer_snapshot():
    try:
        loaded = oracle_routines.load_config()
    except Exception:
        loaded = {}
    cfg = loaded if isinstance(loaded, dict) else {}
    try:
        browser = oracle_browser.list_routines()
    except Exception:
        browser = {}
    st = computer_load()
    cloud_model, cloud_choices = cloud_models(force=False)
    cloud_name = next((m.get("name") for m in cloud_choices
                       if isinstance(m, dict) and m.get("id") == cloud_model), cloud_model)
    emails = sorted((cfg.get("accounts", {}).get("email") or {}).keys())
    hooks = sorted((cfg.get("webhooks") or {}).keys())
    brouts = browser.get("routines", []) if isinstance(browser, dict) else []
    routine_names = sorted(set(emails + hooks + [str(x) for x in brouts]
                               + st["pausedRoutines"]))
    connectors = {}
    for n in emails:
        connectors.setdefault(n, {"name": n, "kind": "email", "targetHost": ""})
    for n in hooks:
        connectors.setdefault(n, {"name": n, "kind": "webhook", "targetHost": ""})
    for n in brouts:
        connectors.setdefault(str(n), {"name": str(n), "kind": "browser", "targetHost": ""})
    for c in st["connectors"]:
        connectors[c["name"]] = c
    return {
        "ok": True,
        "ownerOnly": True,
        "uptime": int(time.time() - STARTED),
        "tools": {"mode": tools_mode(),
                  "scope": ["read", "write", "shell", "fetch", "email", "webhook", "browser"]},
        "browserEnabled": bool(browser.get("enabled")) if isinstance(browser, dict) else False,
        "cloud": {"model": cloud_model, "name": cloud_name,
                  "choices": [{"id": m["id"], "name": m["name"]}
                              for m in (cloud_choices or [])[:6]]},
        "routines": [{"name": n, "paused": n in st["pausedRoutines"]} for n in routine_names],
        "pausedRoutines": st["pausedRoutines"],
        "connectors": sorted(connectors.values(), key=lambda c: c["name"]),
        "secureForms": st["secureForms"],
        "credentialNames": kv_list(),
        "note": "Names only. Secret values stay in the macOS Keychain and never reach the model.",
    }


def knowledge_chunks():
    """Load every knowledge note as small titled chunks for recall."""
    chunks = []
    if not KNOWLEDGE_DIR.exists():
        return chunks
    for f in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        title = f.stem
        for block in re.split(r"\n\s*\n", text):
            block = block.strip()
            if len(block) >= 20:
                chunks.append((title, block))
    return chunks


def recall(query, top_k=3):
    """Keyword-overlap recall over the knowledge folder + memories."""
    if not query:
        return []
    words = set(re.findall(r"[a-z0-9]+", query.lower())) - {"the", "a", "an", "is", "to", "and", "or", "of", "in", "it", "you", "my", "me", "do", "for", "on", "with", "how", "what", "can", "was", "are"}
    scored = []
    for title, block in knowledge_chunks():
        low = (title + " " + block).lower()
        score = sum(1 for w in words if w in low)
        if score:
            scored.append((score, title, block))
    scored.sort(key=lambda x: -x[0])
    return [f"[{t}] {b}" for _, t, b in scored[:top_k]]


def memory_save(text):
    text = str(text).strip()[:1000]
    if not text:
        return False
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {text}\n")
    return True


def memory_list(limit=100):
    try:
        return [l[2:].strip() for l in MEMORY_FILE.read_text(encoding="utf-8").splitlines()
                if l.startswith("- ")][-limit:]
    except Exception:
        return []


def share_load():
    try:
        return json.loads(SHARE_FILE.read_text())
    except Exception:
        return {}


def share_save(sessions):
    SHARE_DIR.mkdir(parents=True, exist_ok=True)
    SHARE_FILE.write_text(json.dumps(sessions, indent=2))


def lan_ip():
    """Best-effort local network IP; no packets are actually sent."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def redact(text):
    """Remove every known Keychain secret from a string before it can be shown."""
    out = str(text)
    for key in kv_list():
        value = kv_get(key)
        if value and len(value) >= 3:
            out = out.replace(value, "[REDACTED]")
    return out


def safe_path(raw):
    """Resolve a path inside the project folder only."""
    root = ROOT.resolve()
    target = (ROOT / str(raw)).resolve()
    if target != root and root not in target.parents:
        raise ValueError("Path is outside the project folder")
    return target


def _tool_span(text):
    """Find a TOOL: {...} call anywhere, including multi-line JSON or code fences."""
    idx = text.find("TOOL:")
    if idx < 0:
        return None
    start = idx + len("TOOL:")
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] != "{":
        return None
    depth, in_str, esc, end = 0, False, False, None
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
    if end is None:
        return None
    return idx, end, text[start:end]


def parse_tool(text):
    """Read a TOOL: {...} call from the model's reply, however it is formatted."""
    span = _tool_span(str(text))
    if not span:
        return None
    try:
        tool = json.loads(span[2])
        return tool if isinstance(tool, dict) else None
    except Exception:
        return None


def strip_tool(text):
    s = str(text)
    span = _tool_span(s)
    if span:
        s = s[:span[0]] + s[span[1]:]
    s = re.sub(r"```(?:json)?\s*TOOL:.*?```", "", s, flags=re.DOTALL)
    s = re.sub(r"```(?:json)?\s*```", "", s)
    return s.strip()


def tool_summary(tool):
    name = str(tool.get("tool", "")).lower()
    if name == "read":
        return "Read file or folder: " + str(tool.get("path", ""))
    if name == "write":
        return "Write file: " + str(tool.get("path", ""))
    if name == "patch":
        return "Patch file (with backup): " + str(tool.get("path", ""))
    if name == "shell":
        return "Run command: " + str(tool.get("command", ""))
    if name == "fetch":
        return "Fetch web page: " + str(tool.get("url", ""))
    if name == "search":
        return "Web search: " + str(tool.get("query", ""))
    if name == "email":
        act = str(tool.get("action", "summary")).lower()
        return f"Email {act}: " + str(tool.get("account", ""))
    if name == "webhook":
        return "Post via automation: " + str(tool.get("name", ""))
    if name == "browser":
        return "Browser routine: " + str(tool.get("routine", tool.get("action", "")))
    if name == "memory":
        act = str(tool.get("action", "")).lower()
        return ("Remember: " if act == "save" else "Recall: ") + str(tool.get("text", tool.get("query", "")))[:60]
    return "Unknown tool request"


def browser_action(tool, cred_get):
    """Run a recorded browser routine; import lazily so the bridge still starts
    if the optional Playwright venv is missing."""
    try:
        import oracle_browser
        return oracle_browser.run(tool, cred_get, redact)
    except Exception as exc:
        return {"ok": False, "error": f"Browser routines unavailable: {type(exc).__name__}"}


_LAST_SEARCH = 0.0


def web_search(query, limit=5):
    """Current public sources for a question. Read-only, owner-only via run_tool.

    GDELT's DOC API supplies recent news articles with dates and URLs; Wikipedia
    supplies background. Both are public and need no key. GDELT asks for at most
    one request every five seconds, so calls are spaced out here.
    """
    global _LAST_SEARCH
    q = str(query or "").strip()[:200]
    if not q:
        return {"ok": False, "error": "search needs a query"}
    n = max(1, min(int(limit or 5), 10))
    rows = []
    try:
        wait = 5.0 - (time.time() - _LAST_SEARCH)
        if wait > 0:
            time.sleep(wait)
        _LAST_SEARCH = time.time()
        url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode({
            "query": q + " sourcelang:english", "mode": "artlist", "format": "json",
            "sort": "datedesc", "timespan": "1month", "maxrecords": n,
        })
        req = urllib.request.Request(url, headers={"User-Agent": "OracleChat/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read(MAX_OUT).decode("utf-8", "replace"))
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            # GDELT asks for at most one request every five seconds and its limit
            # is shared; wait a little longer and try once more.
            time.sleep(8)
            _LAST_SEARCH = time.time()
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read(MAX_OUT).decode("utf-8", "replace"))
        for a in (data.get("articles") or [])[:n]:
            title = re.sub(r"\s+", " ", str(a.get("title", ""))).strip()[:180]
            if not title:
                continue
            d = str(a.get("seendate", ""))[:8]
            date = f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else d
            rows.append(f"- {title} ({date}, {a.get('domain', '')}) {a.get('url', '')}")
    except Exception as exc:
        rows.append(f"- News lookup unavailable: {type(exc).__name__}")
    try:
        wiki_q = q if str(time.localtime().tm_year) in q else q + " " + str(time.localtime().tm_year)
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "list": "search", "srsearch": wiki_q,
            "format": "json", "origin": "*", "srlimit": 3,
        })
        req = urllib.request.Request(url, headers={"User-Agent": "OracleChat/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read(MAX_OUT).decode("utf-8", "replace"))
        for it in (data.get("query", {}).get("search") or [])[:3]:
            title = re.sub(r"\s+", " ", str(it.get("title", ""))).strip()[:180]
            if re.search(r"\b(film|television|TV series|album|song|novel)\b", title, re.I):
                continue
            snippet = re.sub(r"<[^>]+>", "", str(it.get("snippet", "")))[:300]
            wiki = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
            rows.append(f"- Wiki: {title} — {snippet} {wiki}")
    except Exception as exc:
        rows.append(f"- Encyclopedia lookup unavailable: {type(exc).__name__}")
    return {"ok": True, "result": redact("\n".join(rows) or "No current sources found.")[:MAX_OUT]}


_CURRENT_RE = re.compile(
    r"\b(today|tonight|tomorrow|yesterday|this week|this weekend|now|current|"
    r"currently|news|happening|events?|schedule|latest|recent|prices?|weather|"
    r"sports?|results?|open|closed|hours)\b", re.I)


def needs_web_search(text):
    """Cheap gate so cloud chats only search when the question needs fresh facts."""
    return bool(_CURRENT_RE.search(str(text or "")[:1000]))


def run_tool(tool, approved):
    """Execute one validated tool. Reads run freely; everything else needs approval."""
    name = str(tool.get("tool", "")).lower()
    targets = {name, str(tool.get("name", "")), str(tool.get("routine", "")),
               str(tool.get("account", ""))}
    if targets.intersection(set(computer_load()["pausedRoutines"])):
        return {"ok": False, "error": "That routine is paused by the owner."}

    if name == "memory":
        action = str(tool.get("action", "")).lower()
        if action == "save":
            ok = memory_save(tool.get("text", ""))
            return {"ok": ok, "result": "Saved to memory." if ok else "Nothing to save."}
        if action == "recall":
            return {"ok": True, "result": "\n".join(recall(str(tool.get("query", "")), 5)) or "No memories matched."}
        return {"ok": False, "error": "memory action must be save or recall"}

    if name == "read":
        target = safe_path(tool.get("path", ""))
        if target.is_dir():
            body = "\n".join(sorted(p.name for p in target.iterdir()))[:MAX_READ]
        else:
            body = target.read_text(encoding="utf-8", errors="replace")[:MAX_READ]
        return {"ok": True, "result": redact(body)}

    if name == "search":
        return web_search(tool.get("query", ""), tool.get("limit", 5))

    if not approved:
        return {"ok": False, "error": "Action was not approved."}

    if name == "write":
        target = safe_path(tool.get("path", ""))
        content = str(tool.get("content", ""))
        if len(content) > MAX_WRITE:
            return {"ok": False, "error": "Content too large (50,000 character limit)."}
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"ok": True, "result": f"Wrote {len(content)} characters to {target.relative_to(ROOT)}"}

    if name == "patch":
        # Exact-match edit with an automatic backup and post-write verification.
        # This is the safe way for the model to change a large file such as the UI.
        target = safe_path(tool.get("path", ""))
        old = str(tool.get("old", ""))
        new = str(tool.get("new", ""))
        if not old:
            return {"ok": False, "error": "patch needs a non-empty 'old' string — the exact text to replace."}
        if len(new) > MAX_PATCH:
            return {"ok": False, "error": f"Replacement too large ({MAX_PATCH} character limit)."}
        if not target.is_file():
            return {"ok": False, "error": "File not found: " + str(target.relative_to(ROOT))}
        original = target.read_text(encoding="utf-8")
        count = original.count(old)
        if count == 0:
            return {"ok": False, "error": "Exact text not found — nothing changed. Read the file and copy the text exactly."}
        if count > 1:
            return {"ok": False, "error": f"Text appears {count} times — include more surrounding context so it is unique. Nothing changed."}
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup = BACKUP_DIR / f"{target.name}.{time.strftime('%Y%m%d-%H%M%S')}.bak"
        backup.write_text(original, encoding="utf-8")
        updated = original.replace(old, new, 1)
        target.write_text(updated, encoding="utf-8")
        verified = target.read_text(encoding="utf-8") == updated
        return {
            "ok": verified,
            "result": (f"Patched {target.relative_to(ROOT)} — 1 exact replacement, verified={verified}. "
                       f"Backup saved to {backup.relative_to(ROOT)}."),
        }

    if name == "shell":
        command = str(tool.get("command", ""))
        low = command.lower()
        if any(word in low for word in BLOCKED_SHELL):
            return {"ok": False, "error": "Command blocked by safety rules (secrets/Keychain/destructive commands)."}
        r = subprocess.run(command, shell=True, cwd=str(ROOT), capture_output=True,
                           text=True, timeout=30)
        return {"ok": r.returncode == 0,
                "result": redact((r.stdout + r.stderr)[:MAX_OUT]),
                "exit": r.returncode}

    if name == "fetch":
        url = str(tool.get("url", ""))
        u = urlparse(url)
        if u.scheme not in ("http", "https") or not u.netloc:
            return {"ok": False, "error": "Only http/https URLs are allowed."}
        if u.hostname in ("localhost", "127.0.0.1", "::1"):
            return {"ok": False, "error": "Local/internal URLs are not allowed."}
        req = urllib.request.Request(url, headers={"User-Agent": "OracleChat/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(MAX_OUT).decode("utf-8", "replace")
        return {"ok": True, "result": redact(body)}

    if name == "email":
        result = oracle_routines.email_action(
            str(tool.get("account", "")), kv_get,
            action=str(tool.get("action", "summary")),
            limit=tool.get("limit", 10), uid=tool.get("uid"), query=tool.get("query"),
        )
        return {"ok": bool(result.get("ok")), "result": redact(result.get("result", "")),
                "error": redact(result.get("error", "")) or None}

    if name == "webhook":
        result = oracle_routines.webhook_post(str(tool.get("name", "")), kv_get, tool.get("payload", {}))
        return {"ok": bool(result.get("ok")), "result": redact(result.get("result", "")),
                "error": redact(result.get("error", "")) or None,
                "status": result.get("status")}

    if name == "browser":
        result = browser_action(tool, kv_get)
        return {"ok": bool(result.get("ok")), "result": redact(result.get("result", "")),
                "error": redact(result.get("error", "")) or None}

    return {"ok": False, "error": "Unknown tool: " + name}


def system_prompt(cred_names, skills, tools_enabled=False, tool_context=None, tool_mode="auto", knowledge=None, personality=None):
    parts = [
        "You are Oracle, a helpful assistant running on the user's Mac.",
        "Accuracy rules: answer from what you actually know. If you are unsure about a fact, date, "
        "person, or pop-culture detail, say so plainly instead of inventing one. " +
        ("Use the search tool for current, local, recent or post-training questions, and the fetch tool "
         "to open a specific page when you have it. " if tools_enabled else "") +
        "Never present a guess as a fact.",
        "Problem solving: for math, logic, or multi-step questions, work through it step by step "
        "internally, check the result against the question, then give the answer with the key steps shown. "
        "Watch for trick wording (e.g. 'all but 9').",
        "Be useful and direct: give the answer first, then brief supporting detail. Ask one clarifying "
        "question only when the request is genuinely ambiguous.",
        "Tool restraint: never call a tool for greetings, simple conversation, instructions, or anything "
        "you can already answer. Do not read your own knowledge, skill, or note files just to answer a "
        "greeting or a one-word request. Use a tool only when the answer truly needs current, external, "
        "or system information you do not have.",
        "You have a private credential vault. You may know a credential's NAME but never its VALUE.",
        "Never ask for, guess, print, or repeat a password or secret.",
        "Web routines: use the email tool to check or summarize mail, the webhook tool to post "
        "through a user-configured automation, and the browser tool to run a recorded routine. "
        "Routines use credential NAMES only - never put a secret in a tool call. Confirm a "
        "destructive or public action (posting, deleting, sending) with the user first unless they "
        "explicitly asked for it in this message.",
    ]
    if knowledge:
        parts.append("Relevant notes from your own memory (use them when helpful):\n" + "\n\n".join(knowledge[:4]))
    if cred_names:
        parts.append("Available saved credentials (names only): " + ", ".join(cred_names) + ".")
        parts.append(
            "If a task genuinely needs one, output a line exactly "
            "[[USE:NAME|https://example.com/path]] and the app will fill the secret "
            "server-side. The user will see only 'Used saved login'."
        )
    if skills:
        parts.append("The user taught you these skills: " + "; ".join(
            f"{s.get('name','skill')}: {s.get('desc','')}" for s in skills
        ))
    if tools_enabled:
        parts.extend([
            "You have tools on this Mac. To use one, output ONE line and nothing else:",
            'TOOL: {"tool":"read","path":"file.txt"}',
            'TOOL: {"tool":"write","path":"file.txt","content":"text"}',
            'TOOL: {"tool":"patch","path":"file.txt","old":"exact existing text","new":"replacement text"}',
            'TOOL: {"tool":"shell","command":"python3 script.py"}',
            'TOOL: {"tool":"fetch","url":"https://example.com"}',
            'TOOL: {"tool":"search","query":"events in Toronto tomorrow","limit":5}',
            'TOOL: {"tool":"email","account":"main","action":"summary","limit":10}',
            'TOOL: {"tool":"email","account":"main","action":"read","uid":"123"}',
            'TOOL: {"tool":"webhook","name":"social","payload":{"text":"post text"}}',
            'TOOL: {"tool":"browser","routine":"instagram-post","params":{"text":"post text"}}',
            'TOOL: {"tool":"memory","action":"save","text":"a fact worth remembering"}',
            'TOOL: {"tool":"memory","action":"recall","query":"what to recall"}',
            "For any code or UI edit, use patch rather than write: it saves a backup, requires the "
            "old text to appear exactly once, and verifies the result. Read the file first so you "
            "copy the old text exactly, and change one small thing at a time. After patching, tell "
            "the user exactly what changed and that they should reload the page. For Oracle-Chat-Live.html, "
            "state your plan before patching so the user can review it.",
            "Use the memory tool to save only durable facts the user explicitly says to remember " +
            "(preferences, names, recurring context) — never one-off instructions or test phrases. " +
            "Use recall to check your own notes when a question matches them. " +
            "Paths are relative to the project folder. " + (
                "Tools run automatically inside a sandbox when you output the line; use them whenever they help answer." if tool_mode == "auto"
                else "Reads run immediately; write, shell, and fetch need user approval, so output the tool line and wait."
            ),
            "For anything current — news, local events, schedules, prices, weather, sports results, or "
            "facts that may have changed since your training — call the search tool BEFORE answering. "
            "Use the article titles, dates and links it returns, and mention the sources in your answer. "
            "If the search says no sources were found, say that plainly instead of inventing details.",
            "Never place passwords, tokens, or credential values in a tool call. Do not use the shell to read Keychain secrets.",
        ])
    if tool_context:
        follow = ("Use the result to answer; request one more tool only if truly needed." if tool_mode == "auto"
                  else "Answer the user now without another tool.")
        parts.append("A tool already ran. Its result is below. " + follow + " " + tool_context[:2000])
    if personality:
        parts.append("Personality for this chat (style only — never override the rules above): " + str(personality)[:600])
    parts.append("Answer directly and briefly.")
    return "\n".join(parts)


def history_to_text(messages):
    lines = []
    for m in messages:
        role = "User" if m.get("from") == "user" else "Assistant"
        lines.append(f"{role}: {m.get('text','')}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# backends
# ---------------------------------------------------------------------------

def call_local(messages, cred_names, skills, tools_enabled=False, tool_context=None, tool_mode="auto", knowledge=None, model=None, personality=None):
    payload = {
        "model": model or LOCAL_MODEL,
        "system": system_prompt(cred_names, skills, tools_enabled, tool_context, tool_mode, knowledge, personality),
        "prompt": history_to_text(messages),
        "stream": False,
    }
    req = urllib.request.Request(
        OLLAMA_URL + "/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    return d.get("response", "").strip()


def call_vision(image_b64, question, personality=None):
    """Describe one still frame with the local Ollama vision model."""
    prompt = "Answer the question about the image accurately and briefly. "
    "If you cannot see something clearly, say so instead of guessing.\n"
    if personality:
        prompt += "Style for this chat: " + str(personality)[:600] + "\n"
    prompt += "Question: " + str(question)[:500]
    payload = {
        "model": VISION_MODEL,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
        "options": {"temperature": 0.2},
    }
    req = urllib.request.Request(
        OLLAMA_URL + "/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    return d.get("response", "").strip()


def _cloud_once(model_id, messages, cred_names, skills, perms_deny=True,
                knowledge=None, personality=None, search_context=None):
    """One cloud session against a specific free model id."""
    sess = cli("post", "/api/session", {
        "title": "oracle-chat-bridge",
        "model": {"providerID": "opencode", "id": model_id},
        "permissions": [{"action": "*", "resource": "*", "effect": "deny"}] if perms_deny else [],
    })
    sid = sess["id"]
    try:
        text = system_prompt(cred_names, skills, knowledge=knowledge, personality=personality)
        if search_context:
            text += ("\n\nCurrent web sources for this question. Use them for facts that may have "
                     "changed recently; cite the links and say so if they do not answer the question:\n"
                     + str(search_context)[:2000])
        text += "\n\n" + history_to_text(messages)
        cli("post", f"/api/session/{sid}/prompt", {"text": text})
        for _ in range(60):
            msgs = cli("get", f"/api/session/{sid}/message")
            for m in msgs:
                err = m.get("error") or {}
                if err.get("type") == "provider.free-limit":
                    return None, "free-limit"
                if err.get("type"):
                    return None, "error"
            answers = []
            for m in msgs:
                if m.get("role") == "assistant":
                    for part in m.get("parts", []):
                        if part.get("type") == "text" and part.get("text", "").strip():
                            answers.append(part["text"])
            if answers:
                return answers[-1].strip(), None
            time.sleep(1)
        return None, "timeout"
    finally:
        try:
            cli("delete", f"/api/session/{sid}")
        except Exception:
            pass


def call_cloud(messages, cred_names, skills, perms_deny=True, knowledge=None,
               personality=None, search_context=None):
    """Return (answer, error, model id). A free-limit auto-switches models."""
    tried = set()
    model_id, _ = cloud_models(force=False)
    for _ in range(3):
        if not model_id or model_id in tried:
            break
        tried.add(model_id)
        answer, err = _cloud_once(model_id, messages, cred_names, skills,
                                  perms_deny=perms_deny, knowledge=knowledge,
                                  personality=personality, search_context=search_context)
        if answer:
            CLOUD_MODEL_CACHE.update(model=model_id, updated=time.time())
            return answer, None, model_id
        if err != "free-limit":
            return None, err, model_id
        # Quota hit: force a catalog refresh and pick the next newest free model.
        model_id, _ = cloud_models(force=True, exclude=tried)
    return None, "free-limit", ""


def silent_fill(text):
    """Resolve [[USE:key|url]] markers server-side; return (text, notes)."""
    notes = []

    def repl(m):
        key, url = m.group(1).strip(), m.group(2).strip()
        secret = kv_get(key)
        if secret is None:
            notes.append(f"Credential '{key}' was not found in the vault.")
            return f"[credential '{key}' not found]"
        # Inject the secret server-side only. Default: Bearer header.
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {secret}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status = r.status
            notes.append(f"Used saved login '{key}' to contact {url} (HTTP {status}); value hidden.")
        except urllib.error.HTTPError as e:
            notes.append(f"Used saved login '{key}' for {url} (HTTP {e.code}); value hidden.")
        except Exception as e:
            notes.append(f"Tried saved login '{key}' for {url} but the request failed ({type(e).__name__}); value hidden.")
        return f"[used saved login '{key}' — value hidden]"

    return USE_RE.sub(repl, text), notes


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep console quiet; never log message bodies or secrets

    def send_json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def send_html(self, path):
        if not path.exists():
            self.send_error(404)
            return
        b = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n).decode() or "{}")

    def route(self):
        return urlparse(self.path).path

    def token(self):
        q = parse_qs(urlparse(self.path).query)
        tok = (q.get("token") or q.get("share") or [None])[0]
        return tok or self.headers.get("X-Oracle-Token")

    def setup_access(self):
        tok = self.token()
        sessions = share_load()
        self.guest_token = tok if tok and tok in sessions else None
        loopback = self.client_address[0] in ("127.0.0.1", "::1", "localhost")
        if (not loopback and not self.guest_token
                and self.route().startswith("/api/")
                and self.route() != "/api/share/open"):
            self.send_json({"error": "A valid share token is required."}, 403)
            return False
        return True

    def do_GET(self):
        if not self.setup_access():
            return
        path = self.route()
        if path in ("/", "/index.html", "/chat"):
            return self.send_html(UI_FILE)
        if path == "/api/status":
            local_ok = False
            deep_ok = False
            vision_ok = False
            try:
                with urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=3) as r:
                    names = [m["name"] for m in json.loads(r.read())["models"]]
                    local_ok = any(n.startswith(LOCAL_MODEL) for n in names)
                    deep_ok = any(n.startswith(DEEP_MODEL) for n in names)
                    vision_ok = any(n.startswith(VISION_MODEL) for n in names)
            except Exception:
                pass
            tools = ({"mode": "guest — chat only"} if self.guest_token else
                     {"mode": tools_mode(),
                      "scope": ["read", "write", "shell", "fetch", "email", "webhook", "browser"]})
            cloud_model, cloud_choices = (("", []) if self.guest_token else cloud_models(force=False))
            return self.send_json({
                "local": {"ok": local_ok, "model": LOCAL_MODEL, "deepModel": DEEP_MODEL, "deepOk": deep_ok},
                "vision": {"ok": vision_ok, "model": VISION_MODEL},
                "cloud": {"configured": find_cli() is not None,
                          "model": cloud_model,
                          "choices": [{"id": m["id"], "name": m["name"]}
                                      for m in (cloud_choices or [])[:6]]},
                "vault": {"ok": True, "storage": "macOS Keychain"},
                "tools": tools,
            })
        if path == "/api/vault/list":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot access the vault."}, 403)
            return self.send_json({"keys": kv_list()})
        if path == "/api/skills":
            if self.guest_token:
                return self.send_json({"skills": []})
            return self.send_json({"skills": skill_list()})
        if path == "/api/tools/mode":
            if self.guest_token:
                return self.send_json({"mode": "guest"})
            return self.send_json({"mode": tools_mode()})
        if path == "/api/routines":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot use routines."}, 403)
            cfg = oracle_routines.load_config()
            return self.send_json({
                "config": cfg,
                "browser": oracle_browser.list_routines(),
                "credentialNames": kv_list(),
            })
        if path == "/api/memory":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot access memory."}, 403)
            notes = [f.name for f in sorted(KNOWLEDGE_DIR.glob("*.md"))] if KNOWLEDGE_DIR.exists() else []
            return self.send_json({"memories": memory_list(), "notes": notes})
        if path == "/api/computer":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot access the owner computer."}, 403)
            return self.send_json(computer_snapshot())
        if path == "/api/share/open":
            token = self.token()
            session = share_load().get(token)
            if not session:
                return self.send_json({"error": "This share link is not valid."}, 404)
            mode = "chat" if session.get("sharedChat") else ("folder" if session.get("sharedFolder") else "own")
            return self.send_json({
                "mode": mode,
                "sharedChat": session.get("sharedChat"),
                "sharedFolder": session.get("sharedFolder"),
            })
        self.send_error(404)

    def do_POST(self):
        if not self.setup_access():
            return
        path = self.route()
        if path == "/api/vision":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot use the host camera."}, 403)
            d = self.body()
            image = str(d.get("image", ""))
            if not image or len(image) > 8000000:
                return self.send_json({"error": "No usable frame was captured."}, 400)
            question = str(d.get("question", "What do you see?"))[:500]
            personality = str(d.get("personality", ""))[:600]
            try:
                answer = call_vision(image, question, personality)
            except Exception as e:
                return self.send_json({"error": "Local vision failed: " + type(e).__name__}, 500)
            return self.send_json({
                "answer": answer,
                "backend": "local-vision",
                "model": VISION_MODEL,
                "note": "Local vision · on this Mac",
            })

        if path == "/api/chat":
            d = self.body()
            all_messages = d.get("messages", [])
            persona = " ".join(str(m.get("text", "")) for m in all_messages
                               if m.get("from") == "system" and m.get("text"))
            messages = [m for m in all_messages if m.get("from") != "system"][-20:]
            backend = d.get("backend", "auto")
            local_model = DEEP_MODEL if backend == "local-deep" else None
            cred_names = [] if self.guest_token else [str(x) for x in d.get("credentials", [])]
            skills = [] if self.guest_token else skill_list()
            last_user = next((str(m.get("text", "")) for m in reversed(messages)
                              if m.get("from") == "user"), "")
            knowledge = [] if self.guest_token else recall(last_user)
            tool_result = d.get("toolResult")
            context = None
            if tool_result is not None:
                context = "Tool result: " + json.dumps(tool_result)[:2000]
            elif d.get("toolDenied"):
                context = "The user denied that action. Answer without using tools."
            if context:
                messages = messages + [{"from": "user", "text": context}]
            # Owner cloud chats get the same public source context the local
            # tool loop gets, but only for questions that need fresh facts.
            # Guests get no search and no tools.
            cloud_sources = None
            if not self.guest_token and backend in ("auto", "cloud") and needs_web_search(last_user):
                found = web_search(last_user, 3)
                if found.get("ok"):
                    cloud_sources = found.get("result") or ""
            answer, used, note = "", backend, None
            cloud_model_used = ""
            if backend in ("auto", "cloud"):
                a, err, cloud_model_used = call_cloud(
                    messages, cred_names, skills, knowledge=knowledge,
                    personality=persona, search_context=cloud_sources)
                if a:
                    answer, used = a, "cloud"
                    note = "free cloud: " + cloud_model_used
                    if cloud_sources:
                        note += " · current web sources"
                else:
                    note = "Cloud free quota is exhausted; used local model."
                    if backend == "cloud":
                        used = "cloud-blocked"
            tool = None
            needs_approval = False
            tool_ran = None
            tool_notes = []
            if not answer and self.guest_token:
                try:
                    answer = call_local(messages, cred_names, skills, tools_enabled=False, knowledge=knowledge, model=local_model, personality=persona)
                    used = "local-deep" if local_model else "local"
                    answer = strip_tool(answer) or answer
                except Exception as e:
                    return self.send_json({"error": f"Local model failed: {type(e).__name__}"}, 500)
            elif not answer:
                mode = tools_mode()
                try:
                    loop_context = context
                    auto_loop = False
                    seen_tools = set()
                    for _ in range(5):
                        answer = call_local(messages, cred_names, skills,
                                            tools_enabled=True, tool_context=loop_context,
                                            tool_mode=mode, knowledge=knowledge, model=local_model,
                                            personality=persona)
                        used = "local-deep" if local_model else "local"
                        parsed = parse_tool(answer) if (auto_loop or not context) else None
                        if not parsed:
                            answer = strip_tool(answer) or answer
                            break
                        tool = parsed
                        tname = str(tool.get("tool", "")).lower()
                        needs_approval = tname != "read"
                        if mode == "auto":
                            key = json.dumps(tool, sort_keys=True)
                            if key in seen_tools and tool_ran:
                                body = tool_ran["result"].get("result") or tool_ran["result"].get("error") or ""
                                answer = "Here is what I found:\n" + str(body)[:1200]
                                tool = None
                                break
                            seen_tools.add(key)
                            try:
                                result = run_tool(tool, True)
                            except Exception as e:
                                result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
                            tool_ran = {"tool": tool, "summary": tool_summary(tool), "result": result}
                            if tool_summary(tool) not in tool_notes:
                                tool_notes.append(tool_summary(tool))
                            loop_context = "Tool result: " + json.dumps(result)[:2000]
                            answer = strip_tool(answer) or "Let me check that…"
                            auto_loop = True
                            tool = None
                            continue
                        answer = strip_tool(answer) or (
                            "I need to do that on your Mac — approve the action below." if needs_approval
                            else "Let me check that…"
                        )
                        break
                except Exception as e:
                    return self.send_json({"error": f"Both backends failed: {type(e).__name__}"}, 500)
            if tool_ran and (not answer.strip() or answer.strip() in ("Let me check that…", "Let me check that...")):
                body = tool_ran["result"].get("result") or tool_ran["result"].get("error") or ""
                answer = "Here is what I found:\n" + str(body)[:1200]
            answer, fill_notes = silent_fill(answer)
            notes = [x for x in [note] + tool_notes + fill_notes if x]
            response = {
                "answer": answer,
                "backend": used,
                "note": " · ".join(notes),
            }
            if cloud_model_used and used == "cloud":
                response["model"] = cloud_model_used
            if tool_ran:
                response["toolRan"] = tool_ran
            if tool:
                if tool.get("tool") == "write":
                    tool["preview"] = str(tool.get("content", ""))[:200]
                response["tool"] = tool
                response["toolSummary"] = tool_summary(tool)
                response["needsApproval"] = needs_approval
            return self.send_json(response)

        if path == "/api/tool/execute":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot run tools."}, 403)
            d = self.body()
            tool = d.get("tool")
            if not isinstance(tool, dict):
                return self.send_json({"ok": False, "error": "No tool supplied"}, 400)
            try:
                result = run_tool(tool, bool(d.get("approved")))
            except Exception as e:
                result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            return self.send_json(result)

        if path == "/api/vault/set":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot use the vault."}, 403)
            d = self.body()
            key = str(d.get("key", "")).strip()
            value = str(d.get("value", ""))
            if not key or not value:
                return self.send_json({"ok": False, "error": "key and value required"}, 400)
            ok, err = kv_set(key, value)
            return self.send_json({"ok": ok, "error": err or None})

        if path == "/api/vault/delete":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot use the vault."}, 403)
            d = self.body()
            ok = kv_delete(str(d.get("key", "")).strip())
            return self.send_json({"ok": ok})

        if path == "/api/skills":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot change skills."}, 403)
            d = self.body()
            skills = skill_list()
            skills.append({"name": str(d.get("name", "skill")), "desc": str(d.get("desc", ""))})
            skill_save(skills)
            return self.send_json({"ok": True, "skills": skills})

        if path == "/api/tools/mode":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot change tool mode."}, 403)
            d = self.body()
            mode = set_tools_mode(d.get("mode", "auto"))
            return self.send_json({"ok": True, "mode": mode})

        if path == "/api/routines":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot change routines."}, 403)
            d = self.body()
            cfg = d.get("config")
            if not isinstance(cfg, dict):
                return self.send_json({"ok": False, "error": "config must be an object"}, 400)
            try:
                oracle_routines.save_config(cfg)
                return self.send_json({"ok": True, "browser": oracle_browser.list_routines()})
            except Exception as exc:
                return self.send_json({"ok": False, "error": str(exc)})

        if path == "/api/memory":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot change memory."}, 403)
            d = self.body()
            ok = memory_save(d.get("text", ""))
            return self.send_json({"ok": ok, "memories": memory_list()})

        if path == "/api/computer":
            if self.guest_token:
                return self.send_json({"ok": False, "error": "Guest sessions cannot control the owner computer."}, 403)
            d = self.body()
            action = str(d.get("action", "")).strip().lower()
            state = computer_load()
            if action in ("pause", "resume"):
                name = str(d.get("name", "")).strip()[:80]
                if not name:
                    return self.send_json({"ok": False, "error": "Routine name required."}, 400)
                paused = set(state["pausedRoutines"])
                if action == "pause":
                    paused.add(name)
                else:
                    paused.discard(name)
                state["pausedRoutines"] = sorted(paused)[:100]
                computer_save(state)
                return self.send_json({"ok": True, "action": action, "name": name,
                                       "paused": name in state["pausedRoutines"]})
            if action == "connector/add":
                name = str(d.get("name", "")).strip()[:80]
                if not name:
                    return self.send_json({"ok": False, "error": "Connector name required."}, 400)
                kind = str(d.get("kind", "custom")).strip()[:30] or "custom"
                raw = str(d.get("target", "")).strip()
                host = ""
                if raw:
                    parsed = urlparse(raw if "://" in raw else "https://" + raw)
                    host = (parsed.hostname or "")[:120]
                state["connectors"] = [c for c in state["connectors"] if c["name"] != name]
                state["connectors"].append({"name": name, "kind": kind, "targetHost": host})
                computer_save(state)
                return self.send_json({"ok": True, "added": name, "targetHost": host})
            if action == "connector/remove":
                name = str(d.get("name", "")).strip()[:80]
                state["connectors"] = [c for c in state["connectors"] if c["name"] != name]
                computer_save(state)
                return self.send_json({"ok": True, "removed": name})
            if action == "form/add":
                name = str(d.get("name", "")).strip()[:80]
                if not name:
                    return self.send_json({"ok": False, "error": "Form name required."}, 400)
                fields = []
                for f in (d.get("fields") or []):
                    v = str(f).strip()[:60]
                    if v and v not in fields:
                        fields.append(v)
                state["secureForms"] = [f for f in state["secureForms"] if f["name"] != name]
                state["secureForms"].append({"name": name, "fields": fields[:20]})
                computer_save(state)
                return self.send_json({"ok": True, "added": name, "fields": fields[:20]})
            if action == "form/remove":
                name = str(d.get("name", "")).strip()[:80]
                state["secureForms"] = [f for f in state["secureForms"] if f["name"] != name]
                computer_save(state)
                return self.send_json({"ok": True, "removed": name})
            return self.send_json({"ok": False, "error": "Unknown computer action."}, 400)

        if path == "/api/share/create":
            if self.guest_token:
                return self.send_json({"error": "Guest sessions cannot create links."}, 403)
            d = self.body()
            chat = d.get("chat")
            folder = d.get("folder")
            if not isinstance(chat, dict) and not isinstance(folder, dict):
                return self.send_json({"error": "No chat or folder supplied"}, 400)

            def chat_snap(c):
                return {
                    "id": str(c.get("id", "shared")),
                    "name": str(c.get("name", "Shared chat")),
                    "hero": str(c.get("hero", "ironman")),
                    "messages": [
                        {"from": str(m.get("from", "user")), "text": str(m.get("text", ""))}
                        for m in c.get("messages", [])[-100:]
                    ],
                }

            snap = chat_snap(chat) if isinstance(chat, dict) and d.get("includeChat") else None
            folder_snap = None
            if isinstance(folder, dict) and d.get("includeFolder"):
                folder_snap = {
                    "id": str(folder.get("id", "shared-folder")),
                    "name": str(folder.get("name", "Shared folder")),
                    "chats": [chat_snap(c) for c in folder.get("chats", [])[:50] if isinstance(c, dict)],
                }
            token = secrets.token_urlsafe(12)
            sessions = share_load()
            sessions[token] = {
                "created": time.time(),
                "sharedChat": snap,
                "sharedFolder": folder_snap,
            }
            share_save(sessions)
            return self.send_json({
                "ok": True,
                "token": token,
                "url": f"http://{lan_ip()}:{PORT}/?share={token}",
            })

        self.send_error(404)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Oracle Chat bridge listening on http://127.0.0.1:{PORT}")
    print(f"LAN share address: http://{lan_ip()}:{PORT} (guests need a token link)")
    print(f"UI: {UI_FILE.name}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
