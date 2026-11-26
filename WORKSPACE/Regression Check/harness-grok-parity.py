#!/usr/bin/env python3
"""Harness for build 2026-11-27b (deep search, source cards, own-account connectors).

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
GDELT_FN = os.path.join(PAGES, "functions", "api", "gdelt.js")
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


def source_checks(html, cloud, bridge, gdelt):
    expect('content="2026-11-27b"' in html, "build marker is 2026-11-27b")
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
    expect("function ensureOracleBot(" in html and "function oracleBotGuide(" in html
           and "How to use Oracle" in html and "id:ORACLE_BOT_ID" in html,
           "every workspace gets one seeded Oracle Bot guide room")
    expect("const TEAM_KEY='oracle.teams.'+vaultId" in html and "function openTeams(" in html
           and 'id="openTeams"' in html and "guestMode?'':" in html,
           "Teams & Triggers manager is owner-only on both hosts")
    expect("approved:false,paused:false" in html and "if(guestMode)return 0" in html
           and "if(!t||!t.active||t.paused)return 0" in html,
           "team rules start unapproved and paused/guest chains cannot run")
    expect("'manual','keyword','schedule'" in html and "data-team-toggle=" in html
           and "r.paused=!r.paused" in html,
           "manual/keyword/daily rules expose pause and resume")
    expect("function teamRule(" in html and "const r=teamRule(" in html,
           "rule form uses the real rule validator")
    expect("const state={convs,folders,activeId},body=JSON.stringify({key,state});" in html
           and "oracle.teams." not in cloud,
           "cloud state still contains only workspace data, never team/vault state")
    expect('cli("get", "/api/model", timeout=20)' in bridge
           and "cloud_models(force=True, exclude=tried)" in bridge
           and '"provider.free-limit"' in bridge,
           "bridge auto-pulls free models and switches on free-limit")
    expect('(("", []) if self.guest_token else cloud_models(force=False))' in bridge
           and '"free cloud: " + cloud_model_used' in bridge,
           "cloud model status is owner-only and chat notes show the active model")
    expect("function deepQueries(query,city)" in html
            and "function mergeSources(batches,cap)" in html
            and "webSources(text,!!c.deep)" in html,
            "per-chat Deep Search fans out queries and dedupes sources")
    expect('<details class="source-card">' in html and "Why this source?" in html
            and "source-list" in html,
            "source cards show dated links, snippets and a why-this-source panel")
    expect("function migrateSeededWording()" in html
            and "migrateSeededWording();" in html
            and "oldSocial=/Plan, draft and\\s+review social posts/i" in html,
            "saved chats migrate old Socials Bot and Oracle Bot wording")
    expect("function openConnectors(preset)" in html
            and "CONNECTOR_KEY='oracle.connectors.'+vaultId" in html
            and "gvSet('connector.'+id+'.secret',secret)" in html,
            "own-account connectors keep metadata local and encrypt tokens on device")
    expect("parseConnectorRequest(answer)" in html and "data-conn-approve=" in html
            and "data-conn-deny=" in html,
            "connector actions require a one-time approval card")
    expect("function connectorIntent(text,files)" in html
            and "function runConnectorIntent(raw,c,intent)" in html
            and "if(intent){await runConnectorIntent(text,c,intent);return}" in html,
            "plain-language connector intents run locally without model syntax")
    expect('data-quick="check"' in html and 'data-quick="draft"' in html
            and 'data-quick="connect"' in html and 'data-quick="monitor"' in html
            and "function openConnectors(preset)" in html,
            "quick buttons and guided setup use the same plain-language path")
    expect("I cannot watch it in the background" in html
            and "use your own iOS Shortcut or webhook" in html,
            "monitor intent explains the foreground limit and offers user-owned automation")
    expect("cannot log into, read, post to, or manage any external account" in html
            and "publishing needs your own approved connector" in html
            and "cannot log into Instagram" in html,
            "bot wording no longer promises an Instagram login")
    expect("cannot drive the device browser like a person" in html
            and "backgrounded iPhone tab is suspended by iOS" in html,
            "bot wording refuses phone-browser and background-control claims")
    expect("External accounts (Instagram, email, social networks) are not yours to access by default."
            in bridge,
            "bridge system prompt also refuses unapproved external-account actions")
    expect("snippet: snippet(tag(item, 'description'))" in gdelt,
            "news proxy returns snippets for source cards")


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
    guide_src = between("const ORACLE_BOT_ID=", "// A phone tab can be killed")
    search_src = between("function searchDomains(){", "async function fetchGdeltItems(")
    web_src = between("function webSearchOn(){", "function setWebSearchOn(")
    conn_src = between("const CONNECTOR_KEY=", "// ---- Host-only approval rules ----")
    team_src = between("const TEAM_KEY=", "function chatTranscript(")

    script = r'''
var localStorage={_v:{},getItem:function(k){return this._v[k]===undefined?null:this._v[k]},setItem:function(k,v){this._v[k]=String(v)}};
var navigator={onLine:true};
var vaultId='self',guestMode=false;
function connectorNames(){return ['My IG']}
var convs=[{id:'a',name:'Alpha Bot',job:'Research assistant',desc:'',hero:'vision',folder:'f',persona:'oracle',messages:[]},
           {id:'b',name:'Beta Bot',job:'Social media planner',desc:'',hero:'deadpool',folder:'f',persona:'playful',messages:[]}];
var folders=[{id:'f',name:'Chats',open:true}];
function showToast(s){}
function render(){}
function saveState(){}
var botJob=function(c){return String((c&&c.job)||'General assistant').slice(0,60)};
''' + bot_src + "\n" + guide_src + "\n" + search_src + "\n" + web_src + "\n" + conn_src + "\n" + team_src + r'''
localStorage.setItem('oracle.botprefs.x','Use short answers');
var social=botOpener('Socials Bot','Social media planner','Plan and review social posts');
var identity=botIdentityPrompt({id:'x',name:'Socials Bot',job:'Social media planner',desc:'Social media planning'});
var q=newsSearchQuery('Please look up Whats going on this week in idaho falls','');
var xq=newsSearchQuery('What are people saying on X about Idaho Falls','');
localStorage.setItem('oracle.websearch','0');navigator.onLine=false;
var off=webSearchOn();
navigator.onLine=true;

var teamA=teamValidate({name:'News team',roles:['a','b'],chain:['a','b'],
  triggers:[{type:'keyword',value:'idaho'}]});
teams[teamA.id]=teamA;
var needsApproval=teamA.triggers[0].approved===false&&teamA.triggers[0].paused===false;
var ruleFromForm=teamRule({id:'rule-1',type:'keyword',value:'idaho',approved:false,paused:false});
var ruleFormOk=!!ruleFromForm&&ruleFromForm.type==='keyword'&&ruleFromForm.value==='idaho'&&ruleFromForm.approved===false;
teamOnUserText('idaho');
var blockedBeforeApproval=convs.length===2;
teamA.triggers[0].approved=true;
var before=convs.length;
var ran=teamOnUserText('what about idaho');
var order=convs.slice(before).map(function(c){return c.name}).join('|');
teamA.paused=true;
var beforePaused=convs.length;
var pausedBlocked=teamOnUserText('idaho')===0&&convs.length===beforePaused;
teamA.paused=false;
teamA.triggers[0].paused=true;
var beforeRule=convs.length;
var rulePausedBlocked=teamOnUserText('idaho')===0&&convs.length===beforeRule;
teamA.triggers[0].paused=false;
teamA.triggers.push({id:'daily',type:'schedule',value:'00:00',approved:true,paused:false,
  created:Date.now(),lastRun:0,lastRunDay:''});
teamA=teamValidate(teamA);teams[teamA.id]=teamA;
var beforeSchedule=convs.length;
teamTick();
var scheduled=convs.length-beforeSchedule===2;
var beforeSecond=convs.length;
teamTick();
var once=convs.length===beforeSecond;
localStorage.setItem('oracle.search.domains','Reuters.com, apnews.com, <script>');
var dq=deepQueries('Please look up Whats going on this week in idaho falls','');
var deepOk=dq.length===3&&dq.every(function(x){return x.indexOf('site:')>=0&&x.indexOf('<')<0});
var merged=mergeSources([[{url:'https://a.test/1',title:'A'},{url:'https://a.test/1',title:'dup'},{url:'https://b.test/2',title:'B'}]],12);
var mergeOk=merged.length===2;
localStorage.setItem('oracle.connectors.self',JSON.stringify({x:{id:'x',name:'My IG',type:'instagram',target:'12345'}}));
var parsed=parseConnectorRequest('Draft ready.\nCONNECTOR {"name":"My IG","action":"publish","text":"Hello","imageUrl":"https://img.test/a.jpg"}');
var parseOk=!!parsed.request&&parsed.request.id==='x'&&parsed.request.action==='publish'&&parsed.clean.indexOf('CONNECTOR')<0;
var noConnector=parseConnectorRequest('No action.').request===null;
var ciCheck=connectorIntent('Check my Instagram',[]);
var ciConnect=connectorIntent('Connect my Instagram',[]);
var ciPublish=connectorIntent('Post this to Instagram https://img.test/a.jpg',[]);
var ciMonitor=connectorIntent('Monitor my Instagram DMs',[]);
var ciDraft=connectorIntent('Draft a social post about my comic',[]);
var intentOk=ciCheck&&ciCheck.kind==='check'&&ciConnect&&ciConnect.kind==='connect'&&
  ciPublish&&ciPublish.kind==='publish'&&ciPublish.imageUrl==='https://img.test/a.jpg'&&
  ciMonitor&&ciMonitor.kind==='monitor'&&ciDraft===null;
var payload=JSON.stringify({key:'k',state:{convs:convs,folders:folders,activeId:'a'}});
var noTeamInCloud=payload.indexOf('oracle.teams.')<0;
var noConnectorInCloud=payload.indexOf('connector.')<0;
var oldSocialChat={id:'socials-old',name:'Socials Bot',
  desc:'Plan, draft and review social posts; ask about platforms, audience and posting goals.',
  preview:"Hi — I'm Socials Bot. Plan, draft and review social posts",messages:[]};
var oldOracle={id:'oracle-bot',name:'Oracle Bot',preview:'How to use Oracle',
  messages:[{from:'bot',text:"Hi — I'm Oracle Bot, your built-in guide and technical assistant.\\n\\nold text",note:'Guide'}]};
convs.push(oldSocialChat,oldOracle);
var migrated=migrateSeededWording();
var migrationOk=!!migrated&&oldSocialChat.desc.indexOf('own approved connector')>=0&&
  oldOracle.messages[0].text.indexOf('foreground')>=0;
JSON.stringify({social:social,identity:identity,q:q,xq:xq,off:off,
  needsApproval:needsApproval,ruleFormOk:ruleFormOk,blockedBeforeApproval:blockedBeforeApproval,ran:ran,order:order,
  pausedBlocked:pausedBlocked,rulePausedBlocked:rulePausedBlocked,scheduled:scheduled,
  once:once,noTeamInCloud:noTeamInCloud,deepOk:deepOk,mergeOk:mergeOk,
  parseOk:parseOk,noConnector:noConnector,noConnectorInCloud:noConnectorInCloud,
  intentOk:intentOk,migrationOk:migrationOk});
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


def bridge_model_checks():
    """Pure check of automatic free-model discovery without touching the CLI."""
    sys.path.insert(0, PROJECT)
    import oracle_bridge

    free_cost = [{"input": 0, "output": 0, "cache": {"read": 0, "write": 0}}]
    catalog = {"data": [
        {"id": "newest-free", "modelID": "newest-free", "providerID": "opencode",
         "type": "chat", "status": "active", "cost": free_cost,
         "time": {"released": 3000}, "limit": {"context": 100}},
        {"id": "second-free", "modelID": "second-free", "providerID": "opencode",
         "type": "chat", "status": "active", "cost": free_cost,
         "time": {"released": 2000}, "limit": {"context": 100}},
        {"id": "paid-model", "modelID": "paid-model", "providerID": "opencode",
         "type": "chat", "status": "active",
         "cost": [{"input": 1, "output": 2}], "time": {"released": 9999},
         "limit": {"context": 100}},
    ]}
    original_cli = oracle_bridge.cli
    oracle_bridge.cli = lambda *a, **k: catalog
    try:
        oracle_bridge.CLOUD_MODEL_CACHE.update(model="", updated=0.0, models=[])
        newest, models = oracle_bridge.cloud_models(force=True)
        expect(newest == "newest-free", "bridge picks the newest active free model")
        expect([m["id"] for m in models] == ["newest-free", "second-free"],
               "paid and inactive models never enter the free list")
        alternate, _ = oracle_bridge.cloud_models(force=True, exclude={newest})
        expect(alternate == "second-free", "free-limit fallback selects the next free model")
    finally:
        oracle_bridge.cli = original_cli


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
    expect(status == 200 and 'content="2026-11-27b"' in body,
           "canonical serves build 2026-11-27b")
    expect(h.get("cross-origin-opener-policy") == "same-origin" and
           h.get("cross-origin-embedder-policy") == "require-corp",
           "canonical still sends COOP/COEP")

    expect(hashlib.sha256(raw(CANONICAL)).hexdigest() == sha(APP),
           "canonical app bytes match the local build")
    status, headers, body = get(BACKUP)
    expect(status == 200 and 'content="2026-11-27b"' in body,
           "backup serves build 2026-11-27b")
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
    with open(GDELT_FN, encoding="utf-8") as f:
        gdelt = f.read()

    source_checks(html, cloud, bridge, gdelt)
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
    expect(out["needsApproval"] and out["blockedBeforeApproval"],
           "team keyword rules start unapproved and cannot run early")
    expect(out["ruleFormOk"], "rule form creates a valid unapproved keyword rule")
    expect(out["ran"] == 2 and out["order"] == "Alpha Bot · team|Beta Bot · team",
           "approved keyword rule runs the full handoff chain in order")
    expect(out["pausedBlocked"] and out["rulePausedBlocked"],
           "paused teams and paused rules block chain execution")
    expect(out["scheduled"] and out["once"],
           "daily schedule fires once per day while the app is open")
    expect(out["noTeamInCloud"], "team state is excluded from cloud payloads")
    expect(out["deepOk"], "deep queries fan out three safe domain-filtered searches")
    expect(out["mergeOk"], "source dedupe drops repeated URLs")
    expect(out["parseOk"] and out["noConnector"], "connector requests create approval cards only")
    expect(out["noConnectorInCloud"], "connector state is excluded from cloud payloads")
    expect(out["intentOk"], "plain phrases map to check, connect, publish and monitor intents")
    expect(out["migrationOk"], "saved chats migrate to the corrected bot wording")
    bridge_model_checks()

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
