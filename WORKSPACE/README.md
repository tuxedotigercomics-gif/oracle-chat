# Git-backed workspace snapshot

This folder is the source-of-truth snapshot of the original Mac workspace at
`/Users/macbookair/Documents/Default Project`. It exists so another model or a
new computer can continue the project from GitHub alone.

Snapshot date: 2026-11-27  
Snapshot state: build `2026-12-02` re-frozen after local/live harness and host/emulation checks  
Published build at snapshot: `2026-12-02` verified on canonical and backup (Pages commit `ee9eb4a`)  
App SHA: `9e9b97365df05dc678af1c1c927c34a1f06d62e5b4cc5553d19cf42abfa92bf5`  
OAuth callback SHA: `2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`  
Service-worker SHA: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`  
Bridge SHA: `eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`  

The physical iPhone passes for `2026-12-01` and `2026-12-02` are still open; the
confirmed device passes remain `2026-11-29` and `2026-11-30`. The `2026-12-02`
profile menu is a scrollable, searchable phone sheet with its own Close button;
smart chips, local chat search, the one-time approval coach, Library 2.0 and
voice-first preview remain device-local and approval-first.

## Included

- `Oracle-Chat-Live.html` — live app source
- `Oracle-Chat-Offline.html` — frozen offline mockup
- `oracle_bridge.py`, `oracle_browser.py`, `oracle_routines.py`
- `Regression Check/` — changelog, host/phone checklists, harness, baselines, rollback scripts
- `oracle-knowledge/`, `oracle-skills.json`, `oracle-tools-mode.json`, `oracle-routines.json`
- root dev assets: `index.html`, `sw.js`, `manifest.webmanifest`, icons, `package.json`, `vite.config.js`
- `public/` and `src/` development files
- `CLOUDFLARE-SETUP.md` and `WEB-ROUTINES.md`
- `functions/api/instagram-oauth/callback.js` — config-gated free Pages OAuth callback; the app secret stays server-side only

The deployed Cloudflare Pages app remains at this repo's root (`index.html`,
`sw.js`, `_headers`, `functions/`). This folder is the backup of the wider
Mac workspace that the repo root alone does not contain.

## Deliberately excluded

These are machine-local runtime or cache data, not source:

- `.oracle-venv/` — Python virtual environment
- `__pycache__/` — compiled Python cache
- `.DS_Store` — macOS metadata
- `*.log` — local runtime logs
- `.oracle-backups/` — local patch backups
- `oracle-shared/sessions.json` — live guest share tokens and session text

Do not commit real secrets, tokens, vault values, guest sessions, or local logs.

## Restore on a new computer

1. Clone `tuxedotigercomics-gif/oracle-chat`.
2. Copy the contents of `WORKSPACE/` into a new project folder.
3. Recreate `.oracle-venv/` if needed; do not copy it from another machine.
4. Leave `oracle-shared/sessions.json` absent or empty until real runtime data is created.
5. Use `Regression Check/harness-grok-parity.py` before changing anything.
6. Read `AI-HANDOFF/README.md` first, then `AI-HANDOFF/WORKFLOW.md`.

`MANIFEST.sha256` lists every included file's hash.
