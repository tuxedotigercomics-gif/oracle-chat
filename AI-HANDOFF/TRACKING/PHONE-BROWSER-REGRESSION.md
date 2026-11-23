# Regression checklist — phone browser (iPhone Safari first)

Run this at **320 / 360 / 390 / 430 px** on the real iPhone in Safari, and in
an emulated iPhone viewport against `https://oracle-chat.pages.dev/`.
The backup host is `https://tuxedotigercomics-gif.github.io/oracle-chat/`.

Baseline SHA (live UI): `87a4c7e05ca267e55e24c43ec9a476abfa89acfa5ba36152b4d83083bf165ac1`
Service-worker SHA: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`
Rollback: `restore-live.command`

> The desktop/host checklist lives in `MAIN-BROWSER-REGRESSION.md`.
> Voice-call fixes are marked **VOICE FIX 2026-11-19** below.

## Full feature + UI audit — 2026-11-19 (phone/static)
- [x] Static mode detected on `oracle-chat.pages.dev`; zero console errors
- [x] Model menu shows only private on-device models (135M / 350M) — no Mac models
- [x] Web Routines hidden from profile; guest vault ("encrypted on this device") shown instead
- [x] Emulated 390×844 viewport: no horizontal overflow on home or in-chat
- [x] Chats / Folders home then tap into chat; back button returns home
- [x] In-chat: composer, send, mic and call buttons all visible; header at top; no overlap
- [x] Real on-device send: model downloaded, loaded, produced a real local reply; zero errors
- [x] Offline cache confirmed: app shell, `index.js`, `wllama.wasm` and the GGUF model cached under `oracle-chat-v3`
- [x] Note: the 135M model is weak/off-topic on first reply — genuine local inference, not a scripted answer; pick the 350M "Balanced" model for better quality

## Hero personality presets — 2026-11-19
- [x] Personality picker is reachable and usable at phone width (390×844 pass; real-device pass still open)
- [x] Selected tone is passed to the on-device model as a system message
- [x] Personality survives reload and is per-chat, including for guests
- [x] Device context fitting keeps the system instruction instead of dropping it
- [x] No host tools or credentials exposed; zero console errors

## Automatic Home Screen app updates — 2026-11-19
- [x] New service worker is checked for on load and on foreground/pageshow/focus
- [x] New worker takes over and the page reloads once when a build changes
- [x] No reload loop; typed draft survives the reload and the guard caps reloads
- [ ] First-install no-reload guard and offline shell/model with the network blocked — needs the physical phone
- [ ] Zero console errors across update, reload, send and offline reuse — offline pass still open

## Phone-sized Smart model — 2026-11-23 (harness verified; device pass open)
- [ ] Smart 0.6B downloads and the progress text changes to "Downloaded — preparing…" at 462/462 MB (harness done; physical iPhone pending)
- [ ] Smart 0.6B finishes initializing and answers a real question on the iPhone (physical iPhone pending)
- [ ] Reopening the app loads the saved 0.6B from OPFS silently and works offline (physical iPhone pending)
- [x] Tiny / Balanced / Unfiltered models are unchanged (harness)
- [x] No new network path for guests; zero console errors (harness + live)

## Parallel Smart-model download — 2026-11-23 (harness verified; device pass open)
- [ ] Smart 1.7B downloads as 3 parallel shards and the progress bar advances to 100% (harness confirms 3 URLs + 3-way config; physical iPhone pending)
- [ ] A completed shard download is recognised after refresh / new room / offline — no repeat prompt or download (harness confirms saved detection; physical iPhone pending)
- [x] Wi-Fi/size warning still appears for the ~1.1 GB download (harness + live — spec size and menu text updated)
- [x] Tiny / Balanced / Unfiltered models still download and load as a single file (harness)
- [ ] Chat and voice still work and offline reuse still works with no network (physical iPhone pending)

## Smarter model options — 2026-11-23 (harness verified; device pass open)
- [x] Smart 1.7B GGUF is owner/static only; guest and host model lists unchanged (harness)
- [x] Download confirmation warns about the ~1.28 GB size and Wi-Fi (harness)
- [x] Provider presets fill the existing Add a model fields and keys still use the encrypted device vault (harness)
- [ ] Owner-only web search injects sources into custom cloud answers and shows links (harness done; physical iPhone pending)
- [x] No new network path for guests; offline default still makes zero fetches (harness)

## Web search for current info — 2026-11-21 (harness verified; device pass open)
- [x] Web search is off by default and the app still works fully offline (harness — 0 fetches with search off)
- [x] Owner-only setting and city field are visible on static/phone, hidden from guests and host (harness)
- [ ] Enabling search injects current sources into the on-device prompt and shows links (harness done; physical iPhone pending)
- [x] No host credentials/tools/bridge endpoints are exposed by the phone path (harness + live)

## Graceful iOS image message — 2026-11-21 (published; device pass open)
- [x] iPhone image window shows a clear unsupported message with no Generate control (harness)
- [x] No image-model download or U-Net run is started on iOS (harness)
- [x] Message is guest-safe and contains no host credentials/tools (harness + live)
- [ ] Confirm on the physical iPhone that the white flash is gone (physical iPhone)
- [ ] Chat, voice and all other phone features still work (physical iPhone)

## Hybrid image engine — 2026-11-20 (published; device pass open)
- [x] Provider chosen per role: hybrid = WebGPU encoder + CPU U-Net/decoder (harness)
- [x] iPhone defaults to hybrid, desktop to WebGPU; phones on all-CPU migrate to hybrid (harness)
- [x] Engine row shows Phone hybrid / WebGPU / CPU and remembers the choice (harness)
- [x] Full pipeline produces a PNG under hybrid; diagnostics record the engine (harness + live)
- [ ] iPhone image generation completes without white flash using hybrid engine (physical iPhone)
- [ ] Generated image attaches, downloads and copies (physical iPhone)

## CPU image engine — 2026-11-20 (published; device pass open)
- [x] iPhone/iPad default to CPU, desktop to WebGPU (harness)
- [x] Engine toggle persists and is visible at phone width (harness)
- [x] Full pipeline produces a PNG under the CPU engine (harness)
- [ ] iPhone generates an image without a white flash (physical iPhone)
- [ ] Generated image still downloads/copies and attaches to chat (physical iPhone)

## Image crash checkpoint — 2026-11-20 (published; device pass open)
- [x] Checkpoint written before every image stage and cache read (harness)
- [x] Diagnostics copy the last checkpoint (harness)
- [x] No change to image output; zero console errors (harness + live)
- [ ] Diagnostics show the exact stage that killed the iPhone tab (physical iPhone)
- [ ] Paste the last checkpoint back after reproducing the flash (physical iPhone)

## Streamed image model files — 2026-11-20 (published; device pass open)
- [x] Only one model pair is in memory at a time during generation (harness)
- [x] Missing/damaged cached file reports a labelled error (harness)
- [x] Full pipeline still produces a PNG with the streamed reads (harness)
- [ ] Image generation no longer flashes white / kills the iPhone tab (physical iPhone)
- [ ] Model still downloads once and works offline afterwards (physical iPhone)

## Image failure stage diagnostics — 2026-11-20 (published; device pass open)
- [x] Image failure shows which step failed (e.g. unet run, decoder load) (harness)
- [x] Diagnostics command copies saved errors (harness)
- [ ] Physical iPhone pass: paste the labelled error back for targeted fix

## Stop mid-generation reloads and model memory pile-up — 2026-11-20 (published; device pass open)
- [x] Auto-update reload is deferred during image generation (harness)
- [x] Only one chat model stays resident; others are exited on switch (harness)
- [x] Image result still saves and shows before the blob write (harness)
- [ ] No white flash when an update arrives during generation (physical iPhone)
- [ ] No Model error after switching models (physical iPhone)
- [ ] Physical iPhone pass on the installed Home Screen app

## Unfiltered on-device model — 2026-11-20 (published; device pass open)
- [x] Unfiltered model appears in the selector on the static/owner app (harness + live)
- [x] Resolves to the abliterated GGUF and answers through the same wllama path (harness)
- [x] Guest sessions cannot see or load it; no host tools or credentials involved (harness + live)
- [ ] Physical iPhone pass on the installed Home Screen app

## Free chat model before image generation — 2026-11-20 (published; device pass open)
- [x] Image generation releases the chat model before WebGPU starts (harness)
- [x] A blank/black result shows a clear retry message, never a black screen (harness)
- [x] Chat model reloads silently from OPFS on the next message after an image (harness)
- [ ] Physical iPhone pass on the installed Home Screen app

## Generated image survives a phone reload — 2026-11-20 (published; device pass open)
- [x] After generation, a reload returns to the chat with the image message visible (harness)
- [x] Image download/copy still work after the reload (harness)
- [ ] Physical iPhone reload after generation lands on the chat, not the list

## Phone-side image generation — 2026-11-20 (published; physical device pass open)
- [x] NanoDiffuser saves to Cache Storage, loads and reuses offline without redownload (harness; real Mac WebGPU pass)
- [x] All four social sizes (1:1, 4:5, 9:16, 16:9) are available; CLIP picks from the prompt (harness + real WebGPU pass)
- [x] Download/copy controls work and the image attaches to the chat message (harness; PNG crop verified)
- [x] Guest sessions cannot access image generation or any host tools (harness)
- [x] Existing chat-model download, progress bar and offline cache are unchanged (harness)
- [ ] Real iPhone generation pass on the installed Home Screen app

## Retry control for long-chat model errors — 2026-11-20
- [x] Retry button is visible and tappable at phone width on model-error replies (harness)
- [x] Retry with short history answers from the same chat without a new chat
- [x] No host tools, credentials or chat history leak into the retry prompt
- [ ] Real iPhone retry pass on the installed Home Screen app — not triggered: automatic short-history retries handled the long chat, so the button correctly stayed hidden

## Phone long-chat model error — 2026-11-20
- [x] Long chat with the Balanced · 350M model no longer shows `length out of range buffer` (harness)
- [x] Overflow retry shortens history and still answers with the newest question
- [x] Saved model, progress bar and offline reuse remain unchanged in the harness
- [x] Real iPhone long-chat pass on the installed Home Screen app — confirmed by user: 15–25 turn chat and a very large prompt both answered normally, no raw buffer error, no manual retry needed

## About + update status — 2026-11-20
- [x] About screen opens from Profile at phone width without overflow (harness; real-device pass still open)
- [x] Shows build marker, backend, saved-model state and service-worker state
- [x] Check for updates runs on demand and reports the result clearly
- [x] No host tools, credentials, routines or chat content are exposed

## Host camera vision — 2026-11-20
- [x] See this button and camera permission request never appear on static/phone
- [x] Command palette has no host vision command on static/phone

## Model download progress bar — 2026-11-19
- [x] First save shows a visible animated progress bar with real percentage
- [x] Bar fills to the callback percentage and hides when loading completes
- [x] Reusing a saved model shows no download bar
- [x] Bar remains visible across renders while the model saves
- [x] Zero console errors through save → reload → saved-model send in the static harness

## Light + dark visual refresh — 2026-11-19
- [x] Theme system detection and manual override persist across reload (installed-app pass remains on the real-device list)
- [x] Refreshed sidebar, chat, composer, menus and modals fit a phone viewport
- [x] 20px heroes, hero colours, folder sidebar, send/call and back navigation intact
- [x] Model status/download dialogs remain clear in both themes
- [x] Offline caching and static/guest isolation unaffected
- [x] Zero console errors through theme toggle, reload, model reuse and send

## Persistent on-device model storage — 2026-11-19
- [x] Saved model is loaded via `loadModelFromUrl` with the direct HF resolve URL
- [x] Cache check uses wllama's `cacheManager.list()`, not just the Cache API
- [x] Second load shows "Loading saved model from this device" and no download
- [x] First save shows real progress percentage from `progressCallback`
- [x] Private model menu shows "Saved on this device" after a successful load
- [x] Service worker no longer caches HF/GGUF responses; cache bumped to v5
- [x] Download/install dialogs explain iOS Safari vs Home Screen storage split
- [x] Saved-model reuse verified from a populated wllama OPFS cache list (blocked-network real-device pass remains open)
- [x] Zero console errors through save → reload → saved-model send in the static harness

## Grokbot control layer — 2026-11-19
- [x] Bot roster shows a job label and primary badge; new rooms can set them
- [x] Profile → Command palette opens, and `Ctrl/Cmd+K` works where a keyboard exists
- [x] My Routines shows Test and a redacted run history
- [x] Test prints a dry-run preview and executes no steps
- [x] No host approval rules, host Web Routines or bridge APIs appear
- [x] Profile → Install this web app shows Add to Home Screen guidance on iOS
- [x] Manifest and icons load offline from the service worker cache
- [x] Zero console errors through roster → palette → routines
- [ ] Installed web app opens standalone with the Oracle icon and theme color — needs the physical phone (see below)

## On-device context overflow fix — 2026-11-19
- [x] Model loads with a 2048-token context window, not 1024
- [x] Long chat history is trimmed before generation; the newest message is always kept
- [x] A 1051-token request no longer fails with a context-size error
- [x] A remaining overflow retries with a shorter history, then a clear error
- [x] Routine authoring still works with a long endpoint allowlist
- [x] No re-download prompt and zero console errors after the fix

## Model re-prompt fix — 2026-11-19
- [x] Refreshing the page does **not** ask to re-download the model when its GGUF is cached
- [x] Opening a new chat does **not** ask to re-download the model when its GGUF is cached
- [x] The confirmation appears only before a genuine first download
- [x] The acknowledgement persists (`oracle.device.ok`), while the cached bytes load silently

## Device-local routines — 2026-11-19
- [x] Profile → **My Routines** opens on the static/phone build; host **Web Routines** stays hidden
- [x] Router/allowlist accepts only approved https hostnames; other fetch URLs are rejected
- [x] The private model can draft a routine, but it appears in a reviewable JSON editor
- [x] A new or edited routine is untrusted until the owner approves it
- [x] Manual **Run** works; `fetch`, `model`, `say`, `notify`, `share`, `wait` and `log` use the whitelist
- [x] `{{cred:NAME}}` is filled from the device vault at run time and redacted from logs
- [x] `{{var:NAME}}` carries a saved step result to a later step
- [x] Hourly and daily triggers run only while the page is open; daily fires once per day
- [x] A shared chat/folder link gets its own blank routines — no host or other guest routines
- [x] Zero console errors through open → draft → approve → run

## Layout and navigation
- [x] Home screen is the full-width Chats / Folders list (no cramped side-by-side)
- [x] Tapping a folder expands it in place; tapping a chat opens it full-screen
- [x] ← back button returns from chat / vault / memory to the home list
- [x] Send button is visible and inside the viewport; composer does not overflow
- [x] Header fits at 320–430 px: back, model, call, ⋯ and Share all reachable
- [x] Top spacing fits; nothing hidden behind the notch / status bar
- [x] Header three-dot menu and Share open and work on phone
- [x] Desktop still shows sidebar and chat side-by-side; phone back button hidden there

## Model, offline and isolation
- [x] Host-only Mac models are removed; only private on-device models are offered
- [x] Phone runtime is **wllama** (llama.cpp/WASM) — survives iOS where
      Transformers.js kills the tab (research: `PHONE-MODEL-RESEARCH.md`)
- [x] Models are GGUF: **SmolLM2-135M (~105 MB)** default,
      **LFM2.5-350M (~229 MB)** "Balanced" option
- [x] Consent dialog names the exact model and size before the first download
- [x] Model files come from Hugging Face and are cached on the device afterwards
- [x] No host Mac needed: airplane-mode reload still loads the cached app and answers
- [x] Service worker registers on hosted builds (`oracle-chat-v3`)
- [x] Service worker skips HTTP Range requests so a partial 206 cannot corrupt a GGUF load
- [x] A full offline reload renders the app; zero console errors afterwards
- [x] Sending a phone message does not navigate/reload the page; progress stays visible
- [x] Message is saved before generation; a tab reload offers "Try again", not data loss
- [x] Input stays focused after send so the keyboard does not appear to reset
- [x] On-device generation has a 120 s timeout with a clear retry message
- [x] Answers use the model's chat template (coherent, no repetition)
- [x] Guest gets own blank session/copy; no host folders, chats, vault, tools or skills
- [x] Guest vault is device-local and encrypted; values never reach the model

## Web routines — not available on phone (by design)
- [x] Web Routines menu item is hidden on the static/phone build
- [x] Guests cannot call `/api/routines`, vault, tools or memory (403)
- [x] No host credentials, webhook URLs or browser actions are exposed to the phone build
- [x] Documented limitation: iOS Safari gives websites no background browser automation

## Voice and live call — VOICE FIX 2026-11-19
- [x] Call button visible in the phone header; start / end works
- [x] **VOICE FIX:** spoken replies actually play on iPhone — the speech engine is
      primed on the call-button tap (a user gesture), voices load asynchronously,
      and the engine is resumed before speaking
- [x] **VOICE FIX:** microphone releases when the call ends — every recognition is
      aborted, the tracking Set is cleared, and no mic indicator remains
- [x] **VOICE FIX:** the call keeps working after the first reply even when iOS never
      fires speech `onend` (bounded fallback resumes the listener)
- [x] **VOICE FIX:** ending the call mid-speech cancels the fallback timer; no late
      listener can switch the mic back on
- [x] **VOICE FIX:** stale callbacks cannot restart the call (generation token guard)
- [x] **VOICE FIX:** backgrounding / locking the phone releases the mic (`pagehide`)
- [x] Ending a call restores the previous spoken-replies setting; speaker goes silent
- [x] Voice presets: Jarvis (male), Assistant (female), Auto; picker persists
- [x] Voice picker waits for late-loading device voices
- [x] Voice "Try" preview plays without being cut off by a delayed cancel
- [x] Zero console errors through start → speak → reply → speak → end

## How these fixes were verified
Automated in the in-app browser with a mocked `SpeechRecognition` and
`speechSynthesis`: two simultaneous recognizers were both aborted on end;
with speech `onend` deliberately never firing, the fallback still resumed the
listener; ending mid-speech left no recognizer after 8.5 s. No console errors
apart from the expected `/api/status` 404 on a static file server.

## Still needs a real-device pass (cannot be proven by emulation)
- [ ] Actual iPhone Safari microphone permission prompt and release indicator
- [ ] Real iOS system voices speaking through the speaker
- [ ] Hands-free loop across several turns on the user's physical phone
- [ ] Offline reload after the model cache is cold-cleared
- [ ] Add to Home Screen from Safari, then confirm it opens standalone with the Oracle icon and theme colour
