# Rules and settled decisions

These are constraints from the owner, not suggestions. Preserve them across
every change. When in doubt, choose the more private/local option.

## Hard rules

- `Oracle-Chat-Offline.html` stays frozen. All live work is in
  `Oracle-Chat-Live.html` (and `oracle_bridge.py` for host behaviour).
- **Superseded 2026-11-21h:** the owner asked for every model to have internet
  access when connected. Public web search context is now used by owner, guest
  and host models whenever the device is online. The old "phone/guest users
  stay offline" and "guests make zero network requests" rules no longer apply
  while online; offline mode and an explicit Web search "off" still mean zero
  fetches. The host bridge itself remains owner-only.
- Guests cannot use host tools, vault, memory, skills, routines or approval
  rules. No host credentials, routines or tools are exposed; the model sees
  credential **names only**.
- Phone/static routines are device-local, per-session, owner-approved and
  whitelist-based. Mac web routines are owner-only and hidden on static/phone.
- Office remains read-only/frozen unless explicitly approved after review.
- The local/private chat model stays saved on the device with no repeat
  download, and the download progress bar stays.
- On-device models on iPhone require cross-origin isolation because the wllama
  compat WASM imports shared memory. Keep `oracle-pages/_headers` sending
  `Cross-Origin-Opener-Policy: same-origin` and
  `Cross-Origin-Embedder-Policy: require-corp` on the canonical Cloudflare Pages
  site. GitHub Pages cannot send headers, so the backup remains web/chat-only
  and must show the clear "use canonical" message rather than an abort. Do not
  remove COOP/COEP to fix an unrelated issue.
- Installed Home Screen apps pick up updates automatically.
- About/Update status stays local, guest-safe and free of host credentials/tools.
- No continuous iPhone live video. Host camera is phased: still-image answer
  first, phone photo Q&A later.

## Preserve existing behaviour

Do not regress: voice input and spoken replies, folder sidebar, hero sprites and
colour coding, send/call visibility, back navigation, offline caching, and the
seven offline hero personality presets.

## Settled design decisions

### Static vs guest vs host

- Static detection: `location.hostname` not in `127.0.0.1`, `localhost`, `[::1]`.
- Guest detection: a `share` token is present (`?share=...`).
- Owner/static sees private on-device models and the image command.
- Guest sees on-device chat models only; no image command, diagnostics, host
  tools or bridge capabilities.
- Host (localhost via the bridge) sees Mac models and bridge features; no
  static-only update code and no image command.

### Chat model loading

- Uses `w.loadModelFromUrl({url})` with a direct Hugging Face resolve URL.
- OPFS cache is the source of truth for the chat GGUF.
- No HF/GGUF files are cached in the service worker (app shell only).
- Context overflow: treat `length out of range buffer` as overflow;
  `DEVICE_CTX=2048`, `DEVICE_INPUT_CHARS=4800`, with tight retries and a retry
  button.

### Theme

System-aware light/dark with a manual override stored under `oracle.theme`.

### Home Screen auto-update

`oracle-build` meta drives checks on load and foreground/pageshow/focus;
`reg.update()`, `SKIP_WAITING`, a guarded single reload on `controllerchange`,
draft preservation via `oracle.pendingDraft`, and a reload cap of 2 in
`oracle.reload.count`. Busy image work defers reload via `updateBusy()`.

### Personality

Seven local per-chat tones are injected as a system instruction; the picker is
in the chat More menu. Works for guests, survives reload, stays out of visible
history.

### Host vision / status

- Host vision uses `qwen2.5vl:3b`; `/api/vision` is owner-only, hidden on
  static/guest, and returns 403 to guests.
- `/api/status` is bridge-only and hardened: owner keeps full mode/scope; guest
  receives only `{"mode":"guest — chat only"}`.

### Smarter model options (added in `2026-11-21c`, resized in `2026-11-21e`)

- Exactly one larger private GGUF is offered: `qwen3-0.6b-smart`
  (`bartowski/Qwen_Qwen3-0.6B-GGUF`, `Qwen_Qwen3-0.6B-Q4_K_M.gguf`, ~462 MiB).
  It is owner/static only. Guests still see 2 device models; host sees 0. Do not
  add a second similar GGUF without a measured reason.
- **Do not put Qwen3 1.7B back on the phone.** In `2026-11-21d` it was tried as
  three parallel shards (~1.1 GB): the download finished but llama.cpp never
  finished initializing on the owner's iPhone, even when reloading the saved
  shards. The page stayed responsive. 1.1 GB of weights plus ~235 MB of KV cache
  is over a phone's practical budget. The earlier single-file 1.28 GB version
  also downloaded at about 1 MB/s while the CDN did 16 MB/s.
- The shard-aware saved-model code remains (all shards required before a split
  model counts as saved), but every current model is a single file.
- The download-confirmation UI adds a Wi-Fi/size warning for GB files. At byte
  completion the text changes to "Downloaded — preparing … on this device…"
  instead of freezing at 99%. The one-time flag, OPFS caching and progress bar
  are unchanged.
- Cloud provider presets only fill the **existing** Add a model fields. Keys
  still go directly into the AES-GCM device vault; no new key system.
- Direct Anthropic API blocks browser CORS, so Claude is offered via OpenRouter
  (`anthropic/claude-sonnet-5.5`). Presets: OpenAI, OpenRouter, Anthropic via
  OpenRouter.
- The older owner-only/off-by-default `webSources()` note is superseded by
  `2026-11-21h`: all online users now get public source context (see Web search
  below). Host bridge search remains owner-only as a tool.
- No new host local model: the Mac has 8 GB RAM and ~5.5 GB free disk.

### iOS wllama build selection (added in `2026-11-21f`)

- On phones only, validate a real memory64 module before loading GGUF weights:
  `WebAssembly.validate(new Uint8Array([0,97,115,109,1,0,0,0,5,3,1,4,1]))`.
- iOS Safari 27 accepts `new WebAssembly.Memory({address:'i64'})` but refuses to
  compile memory64 modules. wllama's own probe therefore picks a build Safari
  cannot run and model initialization hangs silently (upstream issue #297).
- When the validation fails, hide `WebAssembly.Suspending` so wllama's
  `needCompat()` selects its Asyncify/compat WASM build, and call
  `setCompat('default','firefox_safari')`. Desktop passes the probe and keeps
  the faster default build — no globals changed, no extra requests.
- The compat WASM imports a shared memory (import flags `0x3`, initial 2048 /
  max 65536 pages). WebKit permits shared memory only in a cross-origin-isolated
  document. Build `2026-11-21i` keeps COOP/COEP on the canonical Pages site and
  fails early with a "use canonical" message where isolation is unavailable.
- Build `2026-11-21j` uses wllama `4.0.0` (ESM at
  `@wllama/wllama@4.0.0/esm/index.js`, default WASM at
  `.../esm/wasm/wllama.wasm`). Keep it: 4.0.0 extracts the real abort reason,
  validates memory64 modules, retries iOS shared-memory allocation in smaller
  steps, and retries OPFS handles WebKit closes mid-write. Do not return to
  3.6.1. The OPFS cache key is unchanged, so saved GGUF weights are reused.
- On phones using compat, load with `n_ctx:2048, n_gpu_layers:0, n_threads:1`.
  Desktop keeps wllama's defaults. iOS GPU offload or extra pthreads can abort
  the compat WASM under memory pressure.
- Any remaining model error is tagged `[wllama load]` or `[wllama chat]` with
  COI/compat/phone state. A bare `(ABORT)` is no longer enough information to
  diagnose; capture the full tagged message instead of guessing.
- Do not go back to swapping model sizes to fix a load hang. 1.7B, 0.6B and
  350M all hung identically; the build selection was the cause. The service
  worker's existing jsdelivr rule caches the compat assets after first load.

### Web search (added in `2026-11-21b`)

The 135M/350M phone models cannot know current events. A 3B/4B host model needs
a search tool. Do not try to fix this with prompts alone.

- Host: owner-only `search` tool in `oracle_bridge.py`, backed by GDELT DOC 2.0
  news and Wikipedia. Read-only (no approval prompt); guests have no tools and
  cannot call it. The system prompt directs current/local/recent questions to
  search first.
- As of `2026-11-21h`, **all models and all users** get web context whenever
  `navigator.onLine` is not false. `webSearchOn()` is only false when the device
  is offline or the stored `oracle.websearch` flag is explicitly `0`. The
  `webSources()` guard no longer checks `staticMode` or `guestMode`, and
  `sendMessage()` adds the source block to the system message for every backend
  (device ids, custom cloud, local, local-deep, auto, cloud).
- Public news is fetched through the site's same-origin Cloudflare Pages Function
  `functions/api/gdelt.js`. It tries Bing News RSS first, then Google News RSS,
  then GDELT with one 5.2-second rate-limit-aware retry. This is required because
  GDELT sends no `Access-Control-Allow-Origin` header and direct browser fetches
  silently produced no sources (hence generic answers). GitHub Pages has no
  Functions runtime, so the backup host skips the proxy and uses Wikipedia.
  Sources appear as dated links under the reply. The bridge needs no change: it
  already forwards system text to Ollama and the cloud tool. Guests now make
  these public requests too — this deliberately supersedes the older
  owner-only/guest-offline rule.
- `newsSearchPhrase()` strips lookup scaffolding before querying: "Please look up
  Whats going on this week in idaho falls" becomes `Idaho Falls`. `webSources()`
  isolates each source so a failed proxy cannot stop Wikipedia or escape as a
  model abort. An empty proxy result must still produce a source block when
  Wikipedia answers.
- The Profile → Web search setting (with optional `oracle.city`) remains an
  explicit kill switch. Offline or `0` means zero fetches and a fully local
  answer.

### Grok Bot parity (added in `2026-11-26a`)

- One-job bots are defined by Name / Title-job / Description. New rooms use a
  local opener generator keyed to that identity, so a "Socials Bot" asks about
  platforms, audience and posting goals with no model call or network fetch.
  Bot identity and durable per-bot preferences are injected into both device and
  bridge system text.
- "Teach this task" creates a skill on the owner Mac or an **unapproved** device
  routine draft on static/phone. It never auto-runs. Device routines remain
  whitelist-based, per-session and owner-approved; paused routines cannot run.
- Bot-to-bot handoff is owner-only and visible in chat. Guests see no handoff,
  team UI, host tools, connectors or secure forms.
- `functions/api/cloud-state.js` is a free Cloudflare D1 convenience backup for
  **non-secret owner workspace state only**: bot metadata, preferences, messages,
  folders and active room id. Guests, vault entries, API keys and tool results
  are never sent to it. It needs one owner dashboard binding named `ORACLE_DB`
  (see `CLOUD-VM-SETUP.md`); until then it returns a controlled
  `binding-missing` code with HTTP 200 and the app stays device-local.
- `oracle_bridge.py` exposes a single owner-only `/api/computer` status/control
  endpoint. It shows vault credential **names only**, connector names/hostnames,
  secure-form names/field names and routine pause state. Guest tokens get 403.
  No secret value, routine body or tool result is exposed to the model.
- Real cloud shell/browser compute while the owner Mac is off, automatic guest
  SaaS connectors, cloud-stored API keys and iPhone image/video generation are
  deliberately out of scope.

### Image generation (read the history file too)

- Model: `utkucoban/NanoDiffuser`, pinned revision
  `14cff72356365c3586ee38a2237332525889b69c`, ~382 MB, WebGPU + float16.
- No bridge endpoint, cloud key or API call. Generated PNGs live in IndexedDB
  `oracle-images`; model files in Cache Storage `oracle-image-v1` (streamed one
  model pair at a time via `imageFile()` / `imageSession()`).
- Sizes 1:1, 4:5, 9:16, 16:9 plus model choice; copy/download controls attach
  the result to the chat.
- `halfToFloat()` applies only to `Uint16Array`; decoder uses
  `tensorFloatGetter(out.type, d)`.
- Chat pipes are released before image generation.
- **iOS:** image generation is deliberately unavailable.
  `imageUnsupported()` detects iPhone/iPad, shows a clear message, and guards
  both `startImageGeneration()` and `loadImageRuntime()` so no download or
  U-Net run occurs. Desktop WebGPU generation is unchanged.

### Unfiltered local model

`mradermacher/LFM2.5-350M-abliterated-GGUF`, file
`LFM2.5-350M-abliterated.Q4_K_M.gguf`, ~219 MiB. Owner/static only, id
`device-free` → `lfm2-350m-free`. Guests do not see it; hosts have zero device
models.
