#!/usr/bin/env python3
"""Headless browser routines for Oracle Chat (phase 3).

Routines are defined in oracle-routines.json under "browser". They are explicit
recorded steps, not free-form AI browsing: the model chooses a routine and
fills parameters, while the bridge resolves credential placeholders locally.
A credential value is never returned or logged.
"""

import glob
import re
import sys
import time
from pathlib import Path

import oracle_routines

ROOT = Path(__file__).resolve().parent
# Playwright is installed in a project-local venv so the bridge can keep using
# the system Python. Add that site-packages directory only when needed.
for _p in glob.glob(str(ROOT / ".oracle-venv/lib/python*/site-packages")):
    if _p not in sys.path:
        sys.path.append(_p)
SHOT_DIR = ROOT / ".oracle-browser"
MAX_STEPS = 40
MAX_TEXT = 8000
PLACEHOLDER = re.compile(r"\{\{(cred|param):([^}]+)\}\}")


def _resolve(value, cred_get, params):
    """Replace {{cred:NAME}} and {{param:NAME}} without echoing secrets."""
    s = str(value if value is not None else "")

    def repl(m):
        kind, name = m.group(1), m.group(2).strip()
        if kind == "cred":
            return cred_get(name) or ""
        return str(params.get(name, ""))

    return PLACEHOLDER.sub(repl, s)


def list_routines():
    cfg = oracle_routines.load_config()
    b = cfg.get("browser", {})
    return {
        "enabled": bool(b.get("enabled")),
        "routines": sorted(b.get("routines", {}).keys()),
    }


def run(tool, cred_get, redact_fn=lambda s: s):
    """Execute one browser routine. Returns a redacted, JSON-safe result."""
    cfg = oracle_routines.load_config()
    bcfg = cfg.get("browser", {})
    if not bcfg.get("enabled"):
        return {"ok": False, "error": "Browser routines are disabled. Enable them in Routines."}

    name = str(tool.get("routine") or tool.get("name") or "")
    action = str(tool.get("action", "")).lower()
    params = tool.get("params") or {}
    if not isinstance(params, dict):
        return {"ok": False, "error": "params must be an object."}

    # One-off page read: open a URL and return its visible text.
    if action in ("open", "read", "text"):
        url = _resolve(tool.get("url", ""), cred_get, params)
        if not url.startswith(("http://", "https://")):
            return {"ok": False, "error": "Only http(s) URLs are allowed."}
        routine = {"url": url, "steps": [{"action": "text", "selector": "body"}]}
    else:
        routine = bcfg.get("routines", {}).get(name)
        if not routine:
            return {"ok": False, "error": f"No browser routine named '{name}'. Available: {', '.join(list_routines()['routines']) or 'none'}."}

    steps = routine.get("steps", [])
    if not isinstance(steps, list) or len(steps) > MAX_STEPS:
        return {"ok": False, "error": f"A routine needs 1-{MAX_STEPS} steps."}

    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return {"ok": False, "error": "Playwright is not installed on this Mac yet."}

    collected = []
    shot_path = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            try:
                start = routine.get("url")
                if start:
                    page.goto(_resolve(start, cred_get, params), wait_until="domcontentloaded", timeout=45000)
                for step in steps:
                    act = str(step.get("action", "")).lower()
                    sel = str(step.get("selector", ""))
                    value = _resolve(step.get("value", ""), cred_get, params)
                    timeout = int(step.get("timeout", 20000))
                    if act == "goto":
                        page.goto(value, wait_until="domcontentloaded", timeout=45000)
                    elif act == "fill":
                        page.fill(sel, value, timeout=timeout)
                    elif act == "click":
                        page.click(sel, timeout=timeout)
                    elif act == "press":
                        page.press(sel, value, timeout=timeout)
                    elif act == "wait":
                        page.wait_for_selector(sel, timeout=timeout)
                    elif act == "text":
                        collected.append(page.inner_text(sel, timeout=timeout))
                    elif act == "sleep":
                        time.sleep(max(0, min(float(step.get("seconds", 1)), 10)))
                    elif act == "screenshot":
                        SHOT_DIR.mkdir(parents=True, exist_ok=True)
                        shot_path = SHOT_DIR / f"{name or 'page'}.png"
                        page.screenshot(path=str(shot_path), full_page=True)
                    else:
                        return {"ok": False, "error": f"Unknown browser step: {act}"}
                title = page.title()
            finally:
                browser.close()
        result = f"Ran browser routine '{name or action}'." if name else f"Opened {url}."
        if title:
            result += f"\nPage title: {title}"
        if collected:
            result += "\n\n" + "\n".join(collected)
        if shot_path:
            result += f"\nScreenshot: .oracle-browser/{shot_path.name}"
        return {"ok": True, "result": redact_fn(result)[:MAX_TEXT]}
    except Exception as exc:
        # Never include a resolved credential in an error string.
        msg = f"{type(exc).__name__}: {exc}"
        return {"ok": False, "error": redact_fn(msg)[:600]}
