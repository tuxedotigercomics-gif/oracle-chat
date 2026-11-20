# AI handoff — start here

Read this file first, then the other documents in this folder in order. This
folder is deliberately self-contained: a new assistant with **only this repo**
should be able to resume the work without access to the original Mac workspace.

## Where things stand

| Item | Value |
|---|---|
| Current build marker | `2026-11-21a` |
| Current app SHA (sha256) | `1aa44729b87ba0123ce49b96e05eb2f02fab3b3612b51406f21e2618f6d975f0` |
| Service-worker SHA | `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35` |
| Pages commit (app build) | `49d1b5e` |
| Handoff docs commit | `2cc8b47` (documentation only; app unchanged) |
| Canonical site | https://oracle-chat.pages.dev/ |
| Backup site | https://tuxedotigercomics-gif.github.io/oracle-chat/ |
| Repo | `tuxedotigercomics-gif/oracle-chat` (this repository) |
| Last fully verified build | `2026-11-21a` (both live sites, zero console errors) |

## Open items

1. **Physical iPhone confirmation** of build `2026-11-21a`: tap the sparkle
   button, confirm the "Images aren't available on iPhone" message appears and
   the white flash is gone; confirm chat and voice still work.
2. **Intermittent iPhone chat `Model error:`** — unresolved. The exact error
   text was never captured. Do not guess at a fix; get the exact message first.
3. Everything else listed as unchecked in
   [`TRACKING/PHONE-BROWSER-REGRESSION.md`](TRACKING/PHONE-BROWSER-REGRESSION.md)
   is awaiting a physical device pass, not a code change.

## The single most important thing

**Do not re-attempt iPhone image generation with engine tweaks.** Five builds
already proved the U-Net compute kills the tab under every provider. The full
evidence and the decision to show a graceful unsupported message are in
[`IMAGE-GENERATION-HISTORY.md`](IMAGE-GENERATION-HISTORY.md). Read it before
touching any image code.

## What is in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — current state and open items |
| `RULES-AND-DECISIONS.md` | Non-negotiable privacy/scope rules and settled design decisions |
| `WORKFLOW.md` | Exact change → test → publish → verify → re-freeze process |
| `IMAGE-GENERATION-HISTORY.md` | Every image build, what failed, and why we stopped |
| `TRACKING/` | Snapshots of the changelog, both regression checklists, active SHA index and rollback script |

The `TRACKING/` files are snapshots. The authoritative working copies live in
the original Mac workspace at `/Users/macbookair/Documents/Default Project/Regression Check/`.
If both exist, the local copies win; use these snapshots for continuity only.

## Source map

| Path (relative to the original workspace) | Role |
|---|---|
| `Oracle-Chat-Offline.html` | **Frozen.** Never edit. |
| `Oracle-Chat-Live.html` | The live app source. All UI work happens here. |
| `oracle_bridge.py` | Host bridge. Owner-only tools, routines, vision, status. |
| `oracle-pages/index.html` | Published copy of `Oracle-Chat-Live.html`. |
| `oracle-pages/sw.js` | Published service worker. |
| `Regression Check/baseline/Oracle-Chat-Live.html` | Frozen rollback baseline; matches the current build. |
| `Regression Check/restore-live.command` | Rollback script. |

This repo contains only the browser-published build. `oracle_bridge.py` and the
other local Python/host files are **not** in this repo; request them from the
workspace if host-side work is needed.

## Diagnostics

Owner/static path: **Profile → Command palette → Copy image diagnostics**.
That copies build, engine, last checkpoint, update state and the last 8 labelled
image errors to the clipboard. Guests never see this command.
