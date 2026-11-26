# AI handoff — start here

Read this file first, then the other documents in this folder in order. This
folder is deliberately self-contained: a new assistant with **only this repo**
should be able to resume the work without access to the original Mac workspace.

## Where things stand

| Item | Value |
|---|---|
| Current build marker | `2026-11-26a` |
| Current app SHA (sha256) | `5b804997b2c63475a4314c36ffe2806bbf5e246e01017f490fe66d0cfabb7db4` |
| Service-worker SHA | `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35` |
| Previous verified build | `2026-11-21m` (`7e83fe68bcef9e7b2b409639d177365bb8d5f864845a1957f75ce370325bb78b`) |
| Pages commits | `5c06979` (app + cloud function), `9546db5` (console-clean missing-binding response) |
| Previous app commit | `866b5a5`; handoff docs `94910ba` |
| Bridge SHA | `1e7dbcabd5af7637e06b0db51924c2fac2d58d716e4388188d10e5a7e4e59d95` |
| Canonical site | https://oracle-chat.pages.dev/ (cross-origin isolated) |
| Backup site | https://tuxedotigercomics-gif.github.io/oracle-chat/ (no COOP/COEP; on-device models show a clear "use canonical" message) |
| Repo | `tuxedotigercomics-gif/oracle-chat` (this repository) |
| Last fully verified build | `2026-11-26a` (harness + both live sites + host smoke, zero console errors) |

## Completed setup

- The free D1 database `oracle-chat-cloud` is bound as `ORACLE_DB` to both
  Production and Preview on the `oracle-chat` Pages project (completed
  2026-11-26). `/api/cloud-state` now returns `{"ok":true,"state":null}` when
  there is no owner snapshot yet. Guest sessions, vault entries and tool results
  are never sent to it. See [`CLOUD-VM-SETUP.md`](CLOUD-VM-SETUP.md).

## Open items

1. **Physical iPhone confirmation** of build `2026-11-26a`. Use the canonical
   site — it sends COOP/COEP, which the compat WASM's shared memory needs. Build
   `j` upgraded wllama to 4.0.0 (abort-reason extraction, iOS shared-memory
   retry, OPFS handle retry) and loads phone compat models with
   `n_gpu_layers:0`, `n_threads:1`. Builds `k`–`m` fixed the later "generic
   answer" lookup report: browsers cannot call GDELT directly (no CORS), so a
   same-origin Pages Function now supplies dated news links, with Bing News RSS
   first, Google/GDELT behind it and Wikipedia as the final fallback. Live
   canonical lookup of "Please look up Whats going on this week in idaho falls"
   returned four local links in 0.47 s. Ask the user to retest that exact prompt
   on the Home Screen app and confirm links appear under the answer. On build
   `2026-11-26a`, also create a Socials Bot and confirm the Name/Title/Description
   fields fit the screen and the opener asks about platforms, audience and
   posting goals without fetching anything.
   Every model still gets public web context whenever the device is online —
   owner, guest and host. Ask a current/local question and confirm source links appear under the
   answer. Going offline, or switching Web search off in Profile, still gives a
   fully local answer with zero fetches. Build `2026-11-21e`
   revealed that the on-device model hang was not about model size: both 0.6B
   and 350M stayed at "Loading saved … from this device…". This was traced to
   upstream wllama issue #297 — iOS Safari 27 accepts a 64-bit `WebAssembly.Memory`
   object but cannot compile a memory64 module, so wllama picked the wrong WASM
   build. Build `2026-11-21f` validates a real memory64 module and forces
   wllama's compat/Asyncify build when that probe fails. The physical phone then
   produced `Model error:(ABORT)` during load: the compat WASM imports a **shared**
   memory (flags `0x3`), which WebKit only allows in a cross-origin-isolated
   document. Build `2026-11-21i` adds COOP/COEP on Cloudflare Pages, so the
   canonical site is isolated and the compat module instantiates. The GitHub
   Pages backup cannot send those headers and now shows a clear "use canonical"
   message instead of an abort. Build `2026-11-21j` then adopted wllama 4.0.0
   because the iPhone still hit a bare `(ABORT)` on lookup prompts even with COI;
   4.0.0 includes upstream PR #333 (real abort reason, memory64 validation,
   iOS shared-memory retry, OPFS handle retry) and the phone load now uses CPU
   only with one thread. If an abort still appears, its message now starts with
   `[wllama load]` or `[wllama chat]` and includes COI/compat/phone state.
   On the phone now:
   select Smart 0.6B (or Balanced 350M), confirm the model finishes loading and
   answers a real question; confirm reopening loads the saved model silently
   and works offline. Then tap the sparkle button and confirm the "Images
   aren't available on iPhone" message appears with no white flash; confirm
   chat and voice still work. In Profile → Web search, turn search on and set
   your city, then ask what is happening tomorrow and confirm source links.
2. **Intermittent iPhone `Model error:`** — still open. The load abort was first
   addressed by cross-origin isolation, then by wllama 4.0.0 and phone CPU/single
   thread options in build `2026-11-21j`. The later lookup-only symptom was not
   another model abort: it was the CORS-blocked GDELT fetch, fixed by the proxy
   in builds `k`–`m`. If any `Model error:` remains, capture the full text: it
   now starts with `[wllama load]` or `[wllama chat]` and includes COI/compat/
   phone state, plus a stack when one exists. Do not guess from bare `(ABORT)`.
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
| `CLOUD-VM-SETUP.md` | One-time free D1 `ORACLE_DB` binding and verification |
| `IMAGE-GENERATION-HISTORY.md` | Every image build, what failed, and why we stopped |
| `TRACKING/` | Snapshots of the changelog, both regression checklists, active SHA index and rollback script |
| `WORKSPACE/` | Git-backed snapshot of the wider Mac workspace: source, bridge, harness, baselines, knowledge and dev assets; runtime logs, sessions, caches and virtualenv excluded |

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
| `oracle-pages/functions/api/cloud-state.js` | Owner-only, non-secret D1 cloud-state Function. |
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
