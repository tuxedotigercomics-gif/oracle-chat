# Git-backed workspace snapshot

This folder is the source-of-truth snapshot of the original Mac workspace at
`/Users/macbookair/Documents/Default Project`. It exists so another model or a
new computer can continue the project from GitHub alone.

Snapshot date: 2026-11-26  
Snapshot state: pre-change, before build `2026-11-26b`  
Published build at snapshot: `2026-11-26a`  
App SHA: `5b804997b2c63475a4314c36ffe2806bbf5e246e01017f490fe66d0cfabb7db4`  
Service-worker SHA: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`  
Bridge SHA: `1e7dbcabd5af7637e06b0db51924c2fac2d58d716e4388188d10e5a7e4e59d95`

## Included

- `Oracle-Chat-Live.html` — live app source
- `Oracle-Chat-Offline.html` — frozen offline mockup
- `oracle_bridge.py`, `oracle_browser.py`, `oracle_routines.py`
- `Regression Check/` — changelog, host/phone checklists, harness, baselines, rollback scripts
- `oracle-knowledge/`, `oracle-skills.json`, `oracle-tools-mode.json`, `oracle-routines.json`
- root dev assets: `index.html`, `sw.js`, `manifest.webmanifest`, icons, `package.json`, `vite.config.js`
- `public/` and `src/` development files
- `CLOUDFLARE-SETUP.md` and `WEB-ROUTINES.md`

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
