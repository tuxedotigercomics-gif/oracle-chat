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

## Active live baseline (re-frozen 2026-11-26, build 2026-11-27a)

The live UI is now the working app (served by `oracle_bridge.py`). It has its
own known-good snapshot:

- **File:** `baseline/Oracle-Chat-Live.html`
- **SHA-256:** `a640db6d59a509542d299986ea328fe4115bf50994d7a7a8fc93dc808039a4b0`
- Roll back with `restore-live.command` (keeps a `.broken` backup).

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
