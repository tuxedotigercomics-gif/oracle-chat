# AI handoff — start here

Read this file first, then the other documents in this folder in order. This
folder is deliberately self-contained: a new assistant with **only this repo**
should be able to resume the work without access to the original Mac workspace.

## Where things stand

| Item | Value |
|---|---|
| Current build marker | `2026-11-21g` |
| Current app SHA (sha256) | `9cc5d5cd5d3eb02d1378d3b51f8f7b219c069a593db505117acb991453fdefa3` |
| Service-worker SHA | `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35` |
| Previous verified build | `2026-11-21f` (`f8727fd41386698bb039ef41cbecd9dcf3493ff24bbbf85d7d353b6da3ce4fc4`) |
| Pages commit (app build) | `5f86cd4` |
| Previous app commit | `10bacba`; handoff docs `763983c` |
| Canonical site | https://oracle-chat.pages.dev/ |
| Backup site | https://tuxedotigercomics-gif.github.io/oracle-chat/ |
| Repo | `tuxedotigercomics-gif/oracle-chat` (this repository) |
| Last fully verified build | `2026-11-21g` (harness + both live sites, zero console errors) |

## Open items

1. **Physical iPhone confirmation** of build `2026-11-21g`. Build `2026-11-21g`
   also turns Web search on by default for the owner phone (guests and host
   remain offline): ask a current/local question and confirm source links
   appear under the answer. If you want the phone fully offline again, switch
   Web search off in Profile and it stays off. Build `2026-11-21e`
   revealed that the on-device model hang was not about model size: both 0.6B
   and 350M stayed at "Loading saved … from this device…". This was traced to
   upstream wllama issue #297 — iOS Safari 27 accepts a 64-bit `WebAssembly.Memory`
   object but cannot compile a memory64 module, so wllama picked the wrong WASM
   build. Build `2026-11-21f` validates a real memory64 module and forces
   wllama's compat/Asyncify build when that probe fails. On the phone now:
   select Smart 0.6B (or Balanced 350M), confirm the model finishes loading and
   answers a real question; confirm reopening loads the saved model silently
   and works offline. Then tap the sparkle button and confirm the "Images
   aren't available on iPhone" message appears with no white flash; confirm
   chat and voice still work. In Profile → Web search, turn search on and set
   your city, then ask what is happening tomorrow and confirm source links.
2. **Intermittent iPhone chat `Model error:`** — unresolved. The exact error
   text was never captured. Do not guess at a fix; get the exact message first.
3. Host web search was added in `2026-11-21b`; the physical-device pass for the
   phone search setting is still open.
4. Everything else listed as unchecked in
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
