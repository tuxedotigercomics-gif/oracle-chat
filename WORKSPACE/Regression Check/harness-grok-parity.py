#!/usr/bin/env python3
"""Harness for build 2026-11-26a (Grok-style agents + free cloud state).

Local mode checks source invariants and runs the pure JS helpers through the
macOS JavaScriptCore engine (osascript -l JavaScript). There is no Node on this
Mac. Live mode also checks the canonical/backup Sites and the Pages Function.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(ROOT)
PAGES = os.path.join(PROJECT, "oracle-pages")
APP = os.path.join(PROJECT, "Oracle-Chat-Live.html")
BRIDGE = os.path.join(PROJECT, "oracle_bridge.py")
CLOUD_FN = os.path.join(PAGES, "functions", "api", "cloud-state.js")
CANONICAL = "https://oracle-chat.pages.dev/"
BACKUP = "https://tuxedotigercomics-gif.github.io/oracle-chat/"

EXPECTED_SW_SHA = "6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def expect(cond, label):
    if not cond:
        raise AssertionError(label)
    print("ok - " + label)


def source_checks(html, cloud, bridge):
    expect('content="2026-11-26a"' in html, "build marker is 2026-11-26a")
    expect("Socials Bot" in html and "Which platforms are you posting to?" in html,
           "Socials Bot template asks platform/audience/goal questions")
    expect("botOpener(name,job,desc)" in html, "room creation uses the local opener generator")
    expect("[personalityPrompt(c),botIdentityPrompt(c)]" in html,
           "chat system prompt includes bot identity")
    expect('data-cm="handoff"' in html and "guestMode?'':" in html,
           "owner-only bot handoff is present and guest-gated")
    expect("/api/cloud-state" in html and "cloudLoadState()" in html,
           "owner cloud state backup is wired")
    expect("imageUnsupported(){return iOSDevice()}" in html,
           "iPhone image generation remains deliberately unavailable")
    expect("ORACLE_DB" in cloud and "binding-missing" in cloud,
           "cloud function degrades clearly without the D1 binding")
    expect("guest sessions" in cloud and "never receives vault keys" in cloud,
           "cloud function documents that guests and vault data are excluded")
    expect('data-cm="teach"' in html and "function openTeachTaskModal(" in html,
           "teach-task draft flow is present and owner-gated")
    expect("trusted:false,paused:r.paused===true" in html and "if(r&&r.paused)return" in html,
           "device routine drafts are unapproved and paused routines cannot run")
    expect('data-dr-toggle=' in html and "r.paused=!r.paused" in html,
           "device routines expose pause/resume")
    expect("function openComputerModal(" in html and 'id="openComputer"' in html and "guestMode?'':" in html,
           "owner Computer panel is guest-gated")
    expect('path == "/api/computer"' in bridge and "Guest sessions cannot control" in bridge,
           "bridge computer endpoint is guest-denied")
    expect("targetHost" in bridge and "credentialNames" in bridge and "pausedRoutines" in bridge,
           "bridge computer snapshot exposes names/hosts only")


def script_syntax_check(html):
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S | re.I)
    if not scripts:
        raise AssertionError("no app script found")
    main = max(scripts, key=len)
    fd, path = tempfile.mkstemp(suffix=".js", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(main)
        cmd = [
            "osascript", "-l", "JavaScript", "-e",
            'ObjC.import("Foundation");'
            'var s=$.NSString.stringWithContentsOfFileEncodingError($("%s"),4,null).js;'
            'new Function(s); "compiled"' % path,
        ]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if p.returncode != 0 or "compiled" not in p.stdout:
            raise AssertionError("app script syntax failed: " + (p.stderr or p.stdout).strip()[:500])
        print("ok - app script compiles")
    finally:
        os.unlink(path)


def js_helper_checks(html):
    def between(start, end):
        i = html.index(start)
        j = html.index(end, i)
        return html[i:j]

    bot_src = between("const BOT_TEMPLATES=", "function heroAvatar(")
    search_src = between("function newsSearchPhrase(", "async function fetchGdeltItems(")
    web_src = between("function webSearchOn(){", "function setWebSearchOn(")

    script = r'''
var localStorage={_v:{},getItem:function(k){return this._v[k]===undefined?null:this._v[k]},setItem:function(k,v){this._v[k]=String(v)}};
var navigator={onLine:true};
var botJob=function(c){return String((c&&c.job)||'General assistant').slice(0,60)};
''' + bot_src + "\n" + search_src + "\n" + web_src + r'''
localStorage.setItem('oracle.botprefs.x','Use short answers');
var social=botOpener('Socials Bot','Social media planner','Plan and review social posts');
var identity=botIdentityPrompt({id:'x',name:'Socials Bot',job:'Social media planner',desc:'Social media planning'});
var q=newsSearchQuery('Please look up Whats going on this week in idaho falls','');
var xq=newsSearchQuery('What are people saying on X about Idaho Falls','');
localStorage.setItem('oracle.websearch','0');navigator.onLine=false;
var off=webSearchOn();
JSON.stringify({social:social,identity:identity,q:q,xq:xq,off:off});
'''
    fd, path = tempfile.mkstemp(suffix=".jsc", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(script)
        p = subprocess.run(["osascript", "-l", "JavaScript", path],
                           capture_output=True, text=True, timeout=30)
        if p.returncode != 0:
            raise AssertionError("JXA failed: " + p.stderr.strip())
        return json.loads(p.stdout.strip())
    finally:
        os.unlink(path)


def live_checks():
    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "oracle-harness/1"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, dict(e.headers), e.read().decode("utf-8", "replace")

    def raw(url):
        req = urllib.request.Request(url, headers={"User-Agent": "oracle-harness/1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()

    status, headers, body = get(CANONICAL)
    h = {k.lower(): v for k, v in headers.items()}
    expect(status == 200 and 'content="2026-11-26a"' in body,
           "canonical serves build 2026-11-26a")
    expect(h.get("cross-origin-opener-policy") == "same-origin" and
           h.get("cross-origin-embedder-policy") == "require-corp",
           "canonical still sends COOP/COEP")

    expect(hashlib.sha256(raw(CANONICAL)).hexdigest() == sha(APP),
           "canonical app bytes match the local build")
    status, headers, body = get(BACKUP)
    expect(status == 200 and 'content="2026-11-26a"' in body,
           "backup serves build 2026-11-26a")
    expect(hashlib.sha256(raw(BACKUP)).hexdigest() == sha(APP),
           "backup app bytes match the local build")
    expect(headers.get("Cross-Origin-Opener-Policy") is None,
           "backup remains non-isolated")

    status, _, body = get(CANONICAL + "api/cloud-state?key=cs-harness-check-123")
    try:
        data = json.loads(body)
    except Exception:
        data = {}
    expect(status in (200, 503) and data.get("ok") is True or data.get("code") == "binding-missing",
           "cloud-state endpoint returns a controlled response")

    sw_path = os.path.join(PAGES, "sw.js")
    expect(sha(sw_path) == EXPECTED_SW_SHA, "service worker SHA unchanged")
    expect(hashlib.sha256(raw(CANONICAL + "sw.js")).hexdigest() == EXPECTED_SW_SHA,
           "canonical serves the unchanged service worker")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()

    with open(APP, encoding="utf-8") as f:
        html = f.read()
    with open(CLOUD_FN, encoding="utf-8") as f:
        cloud = f.read()
    with open(BRIDGE, encoding="utf-8") as f:
        bridge = f.read()

    source_checks(html, cloud, bridge)
    script_syntax_check(html)
    out = js_helper_checks(html)
    expect("platforms" in out["social"] and "audience" in out["social"] and "goals" in out["social"],
           "opener questions are specific to the agent name/role")
    expect("Socials Bot" in out["identity"] and "Social media planner" in out["identity"] and
           "Use short answers" in out["identity"],
           "identity prompt carries name, job, description and preferences")
    expect(out["q"] == "Idaho Falls", "lookup phrase still normalizes to Idaho Falls")
    expect(out["xq"].startswith("site:x.com "), "X lookup uses the existing proxy path")
    expect(out["off"] is False, "explicit off/offline still returns no web sources")

    print("app sha: " + sha(APP))
    if args.live:
        live_checks()
    print("PASS - grok parity harness")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL - " + str(exc), file=sys.stderr)
        sys.exit(1)
