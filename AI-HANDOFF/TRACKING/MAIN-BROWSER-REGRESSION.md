# Regression checklist — main browser (desktop / host Mac)

Run this on **Chrome, Edge or Safari on the Mac**, against the bridge-served app
(`Oracle-Chat-Live.html` via `oracle_bridge.py`) and against
`https://oracle-chat.pages.dev/`.

Baseline SHA (live UI): `2c769b7485deac2147ef3e6af5f519ed962b1bfc22b71096343ae84a284f7d38`
Rollback: `restore-live.command`

> The phone-only checklist lives in `PHONE-BROWSER-REGRESSION.md`.
> Voice-call fixes are marked **VOICE FIX 2026-11-19** below.

## Full feature + UI audit — 2026-11-19 (host)
- [x] Bridge healthy: local qwen2.5:3b ok, deep qwen3:4b ok, vault ok, tool scope includes email/webhook/browser
- [x] File integrity: local, Pages copy, baseline, restore script, Cloudflare live and GitHub live all match the active SHA
- [x] Zero console errors on the host app and on both published sites
- [x] Layout: sidebar, main, composer, send, mic, plus, model pill, voice, call, more, share all present
- [x] Model menu: local / deep / cloud→local / cloud / add-model all present
- [x] Plus menu: Attach a file, Use a saved login, Teach a Skill all present
- [x] More menu: new chat, new folder, tool mode, voice, voice picker, rename, move, delete, smart actions, share all present
- [x] Profile menu: vault, memory, web routines, edit name all present
- [x] Real send: local model answered a test room ("READY") — test room deleted, original 2 chats intact
- [x] Hero states in code: `walking` (waiting) and `asking` (raise-hand) both present
- [x] Modals open cleanly: Share/export, Voice picker (device voices), Teach a Skill, Web Routines, Memory
- [x] Vault add/delete works; value field is `password`; only names ever shown
- [x] Skill save works; tool-mode toggle auto↔ask works and was restored to `auto`
- [x] Valid guest token: routines/vault/memory/tool-execution return 403; skills empty; mode `guest`; chat credentials ignored
- [x] All audit artifacts removed (test cred, test skill, guest sessions, tool mode restored)

## Hero personality presets — 2026-11-19
- [x] Personality picker opens from the chat More menu and applies immediately
- [x] Bridge chat follows the selected tone (Concise vs Tutor visibly differ)
- [x] Bot roster create/edit shows and saves the per-chat personality
- [x] Default personality leaves existing chat behaviour unchanged
- [x] System instruction stays out of visible history; zero console errors

## Automatic Home Screen app updates — 2026-11-19
- [x] Host app still loads and chats through the bridge with zero console errors
- [x] Update check code stays in the static/phone build only (no host/local effect)
- [x] Both published sites serve the updated app and SW with matching SHAs

## wllama 4.0.0 + phone CPU load — 2026-11-23 (harness + live verified; device pass open)
- [x] wllama 4.0.0 ESM/default WASM paths load a tiny GGUF with forced compat (harness)
- [x] Saved OPFS cache key stays `${hashSHA1(fullURL)}_${fileName}` (harness)
- [x] Phone compat load uses `n_gpu_layers:0`, `n_threads:1`; desktop defaults unchanged (harness)
- [x] Model errors carry stage/COI/compat/phone-option context (harness)
- [x] Web context for all users, guest/host scope and bridge unchanged; build 2026-11-21j (harness + live)

## Cross-origin isolation for compat WASM — 2026-11-23 (harness + live verified; device pass open)
- [x] `_headers` sends COOP/COEP on canonical; `crossOriginIsolated` true (live)
- [x] jsDelivr/ORT/transformers and CORS fetches still load with zero console errors (harness + live)
- [x] Non-isolated phone builds fail early with a clear message, not `(ABORT)` (harness)
- [x] Abort errors keep their decoded stack for diagnosis; bridge/vault/scope unchanged; build 2026-11-21i (harness + live)

## Internet context for every model — 2026-11-23 (harness + live verified; device pass open)
- [x] Host backends receive web sources in the system message (harness — local, local-deep, auto, cloud)
- [x] Guest/host no longer blocked from webSources; offline and explicit off return no sources (harness)
- [x] Bridge file unchanged; build marker 2026-11-21h; both live sites verified (harness + live)

## Owner phone Web search default — 2026-11-23 (harness + live verified; device pass open)
- [x] Missing flag defaults on only for owner static; guest and host stay off (harness)
- [x] Explicit off still disables search with zero fetches (harness)
- [x] Bridge/vault/model scope unchanged; build marker 2026-11-21g (harness + live)
- [x] Both published sites serve the new app SHA and unchanged worker SHA (live)

## iOS wllama compat fix — 2026-11-23 (harness + live verified; device pass open)
- [x] Memory64 validation probe passes on desktop; WebAssembly globals untouched (harness)
- [x] Valid probe makes no compat calls and requests no extra assets (harness)
- [x] Host model visibility and guest isolation unchanged; build marker 2026-11-21f (harness + live)
- [x] Both published sites serve the new app SHA and unchanged worker SHA; zero console errors (live)

## Phone-sized Smart model — 2026-11-23 (harness + live verified; device pass open)
- [x] Smart resolves to `Qwen_Qwen3-0.6B-Q4_K_M` (~462 MiB) with the single-file URL list (harness)
- [x] Progress text shows "Downloaded — preparing…" at byte completion instead of a frozen 99% (harness)
- [x] Guest keeps 2 models and host keeps 0 device models; no new network path (harness + live)
- [x] Build marker bumps to 2026-11-21e; service worker unchanged; zero console errors (harness + live)

## Parallel Smart-model download — 2026-11-23 (harness + live verified; device pass open)
- [x] Smart 1.7B resolves to the 3-shard repo and wllama issues 3 concurrent shard fetches (harness — real wllama parse + config verified)
- [x] Saved-model detection still recognises a completed shard download after refresh and offline (harness)
- [x] Guest keeps 2 models and host keeps 0 device models; no new network path for guests (harness + live)
- [x] Build marker bumps to 2026-11-21d; service worker unchanged; zero console errors (harness + live)

## Smarter model options — 2026-11-23 (harness verified; live smoke pending)
- [x] Owner Big Pickle cloud chat gets current source context for current-event questions (harness — stubbed CLI)
- [x] Guest cloud path gets no search and no new capabilities (harness)
- [x] No new host local model downloaded; bridge syntax and owner/guest scope unchanged (harness)
- [x] Zero console errors on host, guest and live pages (harness; host static-harness 404 expected)

## Web search for current info — 2026-11-21 (harness verified; live smoke pending)
- [x] Owner `search` tool returns current article titles/dates/URLs via GDELT/Wikipedia (harness — real results verified)
- [x] Model prompt directs current/local/recent questions to the search tool (harness)
- [x] Guest tool scope still chat-only; host status still owner-only (harness + live)
- [x] Zero console errors on host, guest and live pages (harness; host static-harness 404 on `/api/status` expected)

## Graceful iOS image message — 2026-11-21 (published)
- [x] Desktop image generation is unchanged; full WebGPU path still works (harness)
- [x] iOS detection shows an unsupported message with no U-Net run or crash (harness)
- [x] Guest/host visibility unchanged; no bridge/key/cloud exposure; zero console errors (harness + live)

## Hybrid image engine — 2026-11-20 (published)
- [x] Provider is chosen per model role; hybrid = WebGPU encoder + CPU U-Net/decoder (harness)
- [x] iPhone defaults to hybrid; desktop defaults to WebGPU; all three choices work (harness)
- [x] Checkpoints and diagnostics include engine/provider; zero console errors (harness + live)

## CPU image engine — 2026-11-20 (published)
- [x] Engine selector offers WebGPU and CPU, stored per device (harness)
- [x] CPU sessions use the wasm execution provider and skip the WebGPU check (harness)
- [x] Both engines still produce a PNG; diagnostics include the engine (harness)
- [x] Host build and guest sessions unchanged; zero console errors (harness + live)

## Image crash checkpoint — 2026-11-20 (published)
- [x] A checkpoint is written before every image stage and cache file read (harness)
- [x] Diagnostics show the last checkpoint reached after a simulated kill (harness)
- [x] Host build and guest sessions unchanged; zero console errors (harness + live)

## Streamed image model files — 2026-11-20 (published)
- [x] Image model files are read from Cache Storage on demand, not all held at once (harness)
- [x] Only small support files stay resident; each session loads one model pair (harness)
- [x] Full text-encoder → U-Net → decoder pipeline still produces a PNG (harness)
- [x] Host build and guest sessions unchanged; zero console errors (harness + live)

## Image failure stage diagnostics — 2026-11-20 (published)
- [x] Every image step reports a labelled stage plus the raw error (harness)
- [x] Last image errors persist and copy via a diagnostics command (harness)
- [x] Host build and guest sessions unchanged; zero console errors (harness + live)

## Stop mid-generation reloads and model memory pile-up — 2026-11-20 (published)
- [x] Auto-update reload is deferred while an image or chat reply is in flight (harness)
- [x] Loading one device model exits every other resident pipe (harness)
- [x] Host bridge build and guest sessions unchanged; zero console errors (harness + live)

## Unfiltered on-device model — 2026-11-20 (published)
- [x] Third model appears only on static/owner builds, hidden for guests and host (harness + live)
- [x] Selecting it uses the abliterated LFM2.5 GGUF through the same on-device path (harness)
- [x] Host bridge replies and zero console errors are unchanged (harness + live)

## Free chat model before image generation — 2026-11-20 (published)
- [x] wllama pipes are released before WebGPU image generation (harness)
- [x] Blank/black output is detected and reported instead of attached (harness)
- [x] Host build and guest sessions are unchanged; zero console errors (harness + live)

## Generated image survives a phone reload — 2026-11-20 (published)
- [x] Mobile screen choice is remembered across a reload (harness)
- [x] Image chat message is saved before the IndexedDB blob write (harness)
- [x] Host build and guest sessions are unchanged; zero console errors (harness + live)

## Phone-side image generation — 2026-11-20 (published; physical phone open)
- [x] NanoDiffuser is wired as a static/owner-only, device-local, offline-first model with no host or cloud call (harness)
- [x] Host build shows no image-generation UI; guest tokens get no image endpoint (harness + live)
- [x] New image download/cache does not change the existing chat-model progress bar (harness)
- [x] Host chat, bridge replies and zero console errors are unchanged after publishing
- [x] Both live sites serve the final app/SW SHAs with the image build marker

## Retry control for long-chat model errors — 2026-11-20
- [x] Retry button appears on model-error replies, including the "too long" message
- [x] Retry re-sends the preceding question with short history and keeps the chat
- [x] Host bridge errors and normal replies are unchanged; zero console errors

## Phone long-chat model error — 2026-11-20
- [x] Context-overflow detection also recognizes the phone's `length out of range buffer` error
- [x] A tighter final retry with only the newest question is exercised in the harness
- [x] Host chat, bridge replies and zero console errors are unchanged

## About + update status — 2026-11-20
- [x] About screen opens from Profile and the command palette
- [x] Shows build marker, backend and service-worker state without console errors
- [x] Static-only Check for updates button is absent on the host build

## Host camera vision — 2026-11-20
- [x] See this button is host-only and hidden on static/phone builds
- [x] Synthetic webcam preview and still capture work in the host app
- [ ] Real Mac webcam permission prompt works with the physical camera
- [x] Image and question go only to the local bridge vision endpoint
- [x] Guest tokens are denied by /api/vision; no image or credential in history
- [x] Guest /api/status hides the host tool-scope list; owner status is unchanged
- [x] Result appears as a normal bot reply with zero console errors

## Model download progress bar — 2026-11-19
- [x] Progress track appears only while a model is first being saved
- [x] Bar width and ARIA value follow wllama's progress percentage
- [x] Saved-model loading and normal chat show no progress bar
- [x] Host chat and zero console errors unchanged

## Light + dark visual refresh — 2026-11-19
- [x] System theme is detected and manual light/dark toggle persists
- [x] Refreshed surfaces, composer, menus and modals remain readable in both themes
- [x] 20px hero sprites and colour coding are unchanged
- [x] Folder sidebar, send/call buttons and back navigation still work
- [x] Host bridge chat and guest isolation still work after the restyle
- [x] Zero console errors on host and both published sites

## Persistent on-device model storage — 2026-11-19
- [x] Saved model is loaded via `loadModelFromUrl` with no HF API round-trip
- [x] wllama OPFS cache is the source of truth; per-model saved flag is set after load
- [x] First-save progress and saved-model status messages are correct
- [x] Service worker caches only runtime assets; GGUF duplication removed in v5
- [x] Host website still loads and chats normally with the bridge
- [x] Zero console errors on host and both published sites

## Grokbot control layer — 2026-11-19
- [x] Bot roster shows job labels and a primary badge; new rooms can set them
- [x] Approval cards show risk chips and Allow once / Always allow / Deny
- [x] Always allow matches the exact action only; rules are removable in More
- [x] Auto-approved actions reuse the rule without a new prompt; Deny still works
- [x] Command palette opens with `Ctrl/Cmd+K` and searches chats/folders/commands
- [x] Guest sessions never see or use always-allow rules; bridge unchanged
- [x] Routines show Test and a redacted run history on the static build
- [x] PWA manifest, icons and standalone meta tags are linked and cached
- [x] Install UI: Chrome prompt branch, Chrome manual steps, and iOS Add to Home Screen steps all verified
- [x] Service worker cache bumps to v4 and old caches are removed

## On-device context overflow fix — 2026-11-19
- [x] Phone/static model loads with a 2048-token context window
- [x] Large chat histories are bounded before being sent to the model
- [x] Routine authoring prompt remains within the context budget
- [x] Context-overflow errors are retried with shorter history, then explained
- [x] Host bridge behavior and host models are unchanged

## Device-local routines + model re-prompt — 2026-11-19
- [x] Refreshing a chat or opening a new chat does not ask to re-download a cached model
- [x] `oracle.device.ok` persists the download acknowledgement across reloads
- [x] Static build profile shows **My Routines** but not host-only **Web Routines**
- [x] Routines are stored per share token; a shared link opens with a blank routine set
- [x] Allowed endpoints are hostnames only; an unapproved fetch step is blocked
- [x] AI-authored routines land in a JSON editor and cannot run before approval
- [x] `{{cred:NAME}}` resolves from the device vault and is redacted from output
- [x] Schedules run only while the page is open; a daily trigger fires once per day
- [x] No host credentials, host routines or bridge API calls are used

## Startup and backend
- [x] Bridge auto-starts at login and restarts if killed (LaunchAgent KeepAlive)
- [x] `/api/status`: local ok, cloud configured, vault ok, tools auto
- [x] Real local answer from `qwen2.5:3b`; no fake/reply placeholder text
- [x] Deeper local model (`qwen3:4b`, `local-deep`) selectable on host; default stays fast 3B
- [x] Local model tuned: trick wording, step-by-step checking, honest uncertainty
- [x] Trivial prompts do not trigger tools (verified "READY", no tool call)
- [x] Tool calls execute with no `TOOL:` text leaked into the answer

## UI and layout
- [x] Grokbot layout: sidebar and chat side-by-side; phone back button hidden here
- [x] Sidebar shows the conversations with last-message previews
- [x] CHATS / FOLDERS toggle, folders listed, drag-to-folder works
- [x] Clicking a conversation switches the chat
- [x] `+` menu: Attach a file, Use a saved login, Teach a Skill
- [x] Attaching a file shows an attachment chip and is included in the prompt
- [x] Teach a Skill opens a modal, saves, and updates the count badge
- [x] Model selector: Local / Cloud → Local / Big Pickle (host build)
- [x] Model pill opens the dropdown with all host models
- [x] Header three-dot menu: room/folder, tools, voice, smart, share
- [x] Profile menu: vault, memory, editable name
- [x] Share modal: copy, download, family link
- [x] Voice/model dropdown items respond to **real mouse clicks** (not just scripted ones)

## Memory, vault, sharing
- [x] Memory recall returns the exact frozen baseline hash
- [x] Vault: credential names only; values filled silently bridge-side, never shown to model
- [x] Guest vault encrypts values at rest (AES-GCM)
- [x] Guest link defaults to "This device" and hides host-only menu items
- [x] Guest on-device models answer without the host Mac
- [x] Self-contained `#s=` share link opens a chat with messages on a pure static host
- [x] Share links use the hosting domain; Mac app shares `https://oracle-chat.pages.dev/`
- [x] Share URLs do not expose the business name; no domain purchase
- [x] Add / remove custom on-device and cloud models; selection persists

## Publishing
- [x] Cloudflare Pages live at `oracle-chat.pages.dev` (guest isolation verified)
- [x] GitHub Pages kept live as backup at the original URL
- [x] Local source, baseline, Pages copy, restore script and both live sites share one SHA
- [x] `patch` tool: backup + exact-match + verification for in-chat code edits

## Web routines — 2026-11-19 (host only)
- [x] Profile menu has **Web Routines**; modal opens with zero console errors
- [x] Routines config loads/saves through `/api/routines`; guests get 403
- [x] Config holds names/settings only — no secret values; secrets stay in Keychain
- [x] `email` tool: summary/check/read/search via IMAP, credential resolved bridge-side
- [x] `webhook` tool: POSTs JSON to a vault-held webhook URL, redacts response
- [x] `browser` tool: Playwright routine runner with `{{cred:NAME}}` / `{{param:name}}`
- [x] Credential values never appear in tool results, errors or chat
- [x] Model can invoke a routine end-to-end through `/api/chat` (verified: browser routine returned page text)
- [x] Bridge `/api/status` advertises email, webhook and browser tool scope
- [x] Playwright + Chromium installed in project-local `.oracle-venv`
- [x] Documentation: `WEB-ROUTINES.md`
- [ ] Real email account connected and daily summary verified by user
- [ ] Real Make/Zapier webhook connected and a real post verified by user
- [ ] Real site browser routine recorded and verified by user

## Voice and live call — VOICE FIX 2026-11-19
- [x] Voice: mic, spoken replies, live call loop (simulated mic on this browser)
- [x] Ending a live call restores the previous spoken-replies setting
- [x] Voice presets: Jarvis (male), Assistant (female), Auto; picker persists
- [x] Voice picker waits for late-loading device voices
- [x] Voice "Try" preview plays without being cut off by a delayed cancel
- [x] **VOICE FIX:** ending a call aborts *every* recognition instance, clears the
      tracking Set, and releases the mic — no stuck microphone indicator
- [x] **VOICE FIX:** after one reply the call keeps working even if speech `onend`
      never fires (bounded speech fallback calls the loop callback)
- [x] **VOICE FIX:** ending a call during speech cancels the fallback timer, so no
      late listener can restart the mic
- [x] **VOICE FIX:** a call generation token invalidates stale `onend`/`onerror`
      callbacks; `listenLoop()` cannot run after the call has ended
- [x] **VOICE FIX:** leaving the page (`pagehide`) stops all recognition, speech and
      timers so the mic is released on back/tab-switch
- [x] **VOICE FIX:** call state resets to idle on end; call bar disappears
- [x] Zero browser console errors after start → reply → end call

## How these fixes were verified
Automated in the in-app browser with a mocked `SpeechRecognition` and
`speechSynthesis`: two simultaneous recognizers were both aborted on end;
with speech `onend` deliberately never firing, the fallback still resumed the
listener; ending mid-speech left no recognizer after 8.5 s. No console errors
apart from the expected `/api/status` 404 on a static file server.
