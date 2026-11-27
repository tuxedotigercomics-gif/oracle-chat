# Regression Check — Oracle Chat

This folder holds a **known-good snapshot** of the chat UI before we add the
"real answers / real model" feature. Use it to test new changes and to roll
back instantly if something breaks.

## What's here

```
Regression Check/
├── baseline/
│   └── Oracle-Chat-Offline.html   <-- frozen known-good copy (features below)
├── restore.command                <-- double-click to roll back to baseline
├── CHANGELOG.md                   <-- record of what changed and when
└── README.md                      <-- this file
```

The working file lives one folder up:
`../Oracle-Chat-Offline.html`

## Snapshot details

- **File:** `baseline/Oracle-Chat-Offline.html`
- **SHA-256:** `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`
- **Frozen:** 2026-11-19

### Features included in this baseline
- Two-column Grokbot-style layout (sidebar + chat)
- 13 clickable conversations with last-message previews
- Michael Lynch / 87 profile footer
- Message sending with fake bot reply and auto-scroll
- `+` menu with **Attach a file** (file picker, attachment chips) and
  **Teach a Skill** (modal, saved to browser storage)
- **Model selector** dropdown in the header (Qwen Coder 30B, Qwen3.6 27B,
  Qwen3.8 27B, Qwen3.8 Flash Next, Qwen3.6 35B-A3B) — label only, not real
- Fully offline: single file, no server, no Node, no internet

> Note: in this baseline the bot replies are **fake** and the model selector
> only changes a label. That is expected — it is the last state before wiring
> in a real backend.

## How to use it

### Test before adding something new
1. Copy `../Oracle-Chat-Offline.html` to a temp name, e.g.
   `Oracle-Chat-Offline-NEW.html`, and make your changes there.
2. Open both files in a browser and compare side by side.
3. Run the checklist below on the NEW file.
4. Only when it passes, replace the working file and update the baseline.

### Roll back if you break something
- **Option A (easy):** double-click `restore.command`. It copies the baseline
  over `../Oracle-Chat-Offline.html` and keeps a `.broken` backup of whatever
  was there.
- **Option B (manual):** copy `baseline/Oracle-Chat-Offline.html` over
  `../Oracle-Chat-Offline.html`.

## Regression checklist (run on any new version)

- [ ] Opens by double-click, no internet, no server
- [ ] Sidebar shows all 13 conversations
- [ ] Clicking a conversation switches the chat
- [ ] Type + Send adds your message and a bot reply appears
- [ ] `+` opens a menu with "Attach a file" and "Teach a Skill"
- [ ] "Attach a file" opens a file picker and shows an attachment chip
- [ ] "Teach a Skill" opens a modal and saves a skill (shown by the count badge)
- [ ] Model pill opens a dropdown with all 5 models
- [ ] Selecting a model updates the pill and shows a toast
- [ ] No errors in the browser console
- [ ] Layout still looks like Grokbot (sidebar + chat columns)

## Verify the baseline is intact

```sh
shasum -a 256 baseline/Oracle-Chat-Offline.html   # original mockup
shasum -a 256 baseline/Oracle-Chat-Live.html      # active live UI
```

If a hash differs from the one above, the baseline was modified — restore
from your own backup before trusting it.

## Active live baseline (re-frozen 2026-11-27, build 2026-12-02)

The live UI is now the working app (served by `oracle_bridge.py`). It has its
own known-good snapshot:

- **File:** `baseline/Oracle-Chat-Live.html`
- **SHA-256:** `9e9b97365df05dc678af1c1c927c34a1f06d62e5b4cc5553d19cf42abfa92bf5`
- Roll back with `restore-live.command` (keeps a `.broken` backup).

Build `2026-12-02` turns the long profile list into a scrollable, searchable
menu sheet on phones: a fixed in-viewport panel with a Close button, a 16px local
search field, larger rows, and independent scrolling so “My Connectors” and the
last item stay reachable without rubber-banding the chat list behind it. The
desktop dropdown is now height-capped and scrollable too. It keeps all of
`2026-12-01` (smart chips, local chat search, one-time approval coach, Library
2.0 and voice-first preview/send) plus the earlier no-zoom composer, approval
inbox, starter bots, device-local Library, template share/import, routines,
chief-of-staff routing, connector catalog and bot desks. The config-gated free Pages
callback at `oracle-pages/functions/api/instagram-oauth/callback.js` from
`2026-11-27c` is unchanged and stays honestly “Not configured” until the owner
supplies the Meta App ID, server-side app secret, redirect URI and scopes as Pages
secrets. No client secret exists in the app, chat, console, cloud state or prompts.

Build `2026-12-01` adds smart context chips, local chat search with a jump to the
exact message, a plain-language one-time approval coach, Library 2.0 with search,
tags, favorites and preview-before-insert, and a voice-first composer that
previews dictated words and sends only on an explicit tap. It keeps the
`2026-11-30` no-zoom/no-refocus composer, the `2026-11-29` approval inbox,
starter bot gallery, device-local Library, safe bot template share/import and
weekly/interval routine templates, plus the `2026-11-28` chief-of-staff routing,
plain connector catalog and device-local bot desks.

The physical iPhone Safari passes for builds `2026-11-29` and `2026-11-30` are
confirmed; the physical passes for `2026-12-01` and `2026-12-02` remain open, as do
older device-only boxes.

The original offline mockup baseline and its SHA-256 are preserved unchanged
for layout comparison and historical rollback via `restore.command`.

### Live UI regression checklists — split by browser

There are now **two separate lists**, because the phone has different failure
modes (WebKit memory cap, real microphone, offline cache) from the host browser:

- **`MAIN-BROWSER-REGRESSION.md`** — desktop / host Mac: bridge, tools, vault,
  sharing, publishing, mouse interactions and voice-call fixes.
- **`PHONE-BROWSER-REGRESSION.md`** — iPhone Safari first: 320–430 px layout,
  navigation, wllama GGUF models, offline cache, guest isolation and
  voice-call fixes. Includes a real-device section that emulation cannot prove.

Research behind the phone runtime: `PHONE-MODEL-RESEARCH.md`.

The original single combined checklist above was retired on 2026-11-19; its
items were carried into the two files (and the outdated ONNX/WebGPU model
notes were corrected to the current wllama GGUF models).
