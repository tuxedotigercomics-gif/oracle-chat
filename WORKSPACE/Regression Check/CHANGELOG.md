# Changelog — Oracle Chat UI

Record every change here before you make it, so there is always a clear trail
between the frozen baseline and whatever is currently in the working file.

## 2026-12-02 — Profile menu becomes a scrollable, searchable sheet (published and verified)

Status: **published and verified**. The owner reported that the long profile
list on iPhone ran off the top of the screen and iOS rubber-banding snapped it
back, leaving “My Connectors” hard to reach. The fix touched only the live app;
the offline mockup stayed frozen.

Intended change:

1. Keep the desktop dropdown, but cap its height and let it scroll with
   `overscroll-behavior:contain` so it never runs off the screen.
2. On phones, turn the profile list into a fixed, edge-to-edge sheet with a
   clear Menu title, a Close button, and a local-only “Search this menu” field.
3. Give each row a larger touch target and keep every entry, including
   “My Connectors”, reachable by scrolling the menu body instead of dragging
   the chat list behind it.
4. Keep every existing action, owner/guest gate, approval rule, connector token
   boundary, and no-zoom input rule unchanged.
5. Bump the marker to `2026-12-02`, extend the harness, and re-freeze only after
   local/live checks pass. The physical iPhone pass stays open.

Shipped in build `2026-12-02`: local harness PASS and live harness PASS on both
sites. App SHA `9e9b97365df05dc678af1c1c927c34a1f06d62e5b4cc5553d19cf42abfa92bf5`
was verified byte-for-byte on the live source, published copy, canonical site and
backup site. Published in Pages commit `ee9eb4a`. Emulated 320/360/390/430 px
checks on owner, guest, backup and bridge-host pages confirmed the menu sits
inside the viewport, its body scrolls independently, search narrows entries to
“My Connectors”, Close and Esc dismiss it, the search field stays at 16px, and
there is no horizontal overflow. Owner, guest and backup pages had zero console
errors; the bridge host only showed its known missing manifest asset. Baseline,
rollback, README, workspace snapshot and manifest were re-frozen only after those
checks passed. Physical iPhone confirmation for this new build remains open.

## 2026-12-01 — Smart chips, chat search, approval coach, Library 2.0 and voice-first composer (published and verified)

Status: **published and verified** (planned before edits). The owner approved all five next improvements.
They stay device-local, plain-language and approval-first; no background work,
always-allow, hidden token, borrowed account, paid worker or browser control is
added.

Intended change:

1. Add context-aware quick chips that suggest summarize, simpler, checklist,
   save-to-Library and approval actions from the current chat. They use natural
   phrases only and never create hidden connector syntax.
2. Add local chat search that finds chat names and message text, then jumps to
   the exact message. It stays inside the device vault and cloud state excludes
   the search index.
3. Add an approval coach that says in plain words what one Allow will and will
   not do before the decision. It never adds always-allow or exposes a token.
4. Upgrade the Library with search, tags, favorites and a preview before insert.
   Items stay device-local, guest-isolated and are never injected into prompts
   unless the person chooses them.
5. Add a voice-first composer: dictate, preview the exact words, edit if needed,
   then tap Send. Nothing sends from voice alone and no background listening is
   claimed.
6. Bump the marker to `2026-12-01`, extend the harness, run local/live smoke and
   SHA checks, then re-freeze only after verification. Physical iPhone
   confirmation stays open.

Shipped in build `2026-12-01`: local harness PASS and live harness PASS on both
sites. App SHA `62148db7142ddb5f61495507041d72e2522425d9ed9b3d6e49e2535aef8c0c22`
was verified byte-for-byte on the live source, published copy, canonical site and
backup site. The bridge stayed unchanged at
`eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`, the worker at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`, the
config-gated callback at
`2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`, and the
frozen mockup at
`320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`. Published in
Pages commit `f07663b`. Emulated 320/360/390/430 px checks on owner, guest,
backup and bridge-host pages confirmed 16px fields, `enterkeyhint="send"`, context
chips, working local search/coach/Library controls, voice preview with no
auto-send, no focus zoom, no post-send refocus and no horizontal overflow. Owner,
guest and backup pages had zero console errors; the bridge host only showed its
known missing manifest asset. Baseline, rollback, README, workspace snapshot and
manifest were re-frozen only after those checks passed. Physical iPhone
confirmation for this new build remains open.

## 2026-11-30 — Physical iPhone Safari pass confirmed (documentation closeout)

Status: **verified**. The owner opened the canonical build on a physical iPhone
in Safari and confirmed the fix: tapping the message field no longer zooms the
page, and sending closes the keyboard without the check/pinch cleanup. No app
file changed; the app SHA stays
`7f610c0fd4d76befb9f23ed93b3ee71c7d3b3f0a2f55a726dc29a5442ce5d17b`. This closes
the physical box for build `2026-11-30` only. Older physical-device boxes remain
open until each flow is separately confirmed.

## 2026-11-30 — Stop iPhone composer zoom and keyboard reset (published and verified)

Status: **published and verified** (planned before edits). The owner reported that tapping the message
field zooms the page in, and after sending they must tap the keyboard’s check key
and pinch back out. This is iOS Safari auto-zoom for text under 16px plus an
unconditional refocus after send.

Intended change:

1. Set every text input, textarea and select to at least 16px on phone widths so
   Safari does not zoom when the field is focused.
2. Add `enterkeyhint="send"` to the chat field so the keyboard’s main key sends.
3. Blur the composer before rerendering after send, and stop refocusing it so the
   keyboard closes and the page stays fitted.
4. One click/tap reopens the field if needed. Keep approvals, guests, connectors,
   routines and every existing SHA boundary unchanged except the live app. Bump
   the marker to `2026-11-30`, extend the harness, run local/live smoke and SHA
   checks, then re-freeze only after verification. Physical iPhone confirmation
   stays open.

Shipped in build `2026-11-30`: local harness PASS and live harness PASS on both
sites. App SHA `7f610c0fd4d76befb9f23ed93b3ee71c7d3b3f0a2f55a726dc29a5442ce5d17b`
was verified byte-for-byte on the live source, published copy, canonical site and
backup site. The bridge stayed unchanged at
`eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`, the worker at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`, the config-gated
callback at `2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`,
and the frozen mockup at
`320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`. Published in
Pages commit `98df621`. Emulated 320/360/390/430 px checks on owner, guest,
backup and bridge-host pages confirmed 16px fields, `enterkeyhint="send"`, no
focus zoom, no post-send refocus and no horizontal overflow. Owner and guest
pages had zero console errors; the backup host only showed its known static-host
`/api/cloud-state` 404/405 and the bridge host only showed its known missing
manifest asset, with no app error. Baseline, rollback, README, workspace snapshot
and manifest were re-frozen only after those checks passed. The physical iPhone
confirmation was later reported fixed and closed separately.

## 2026-11-29 — Physical iPhone Safari pass confirmed (documentation closeout)

Status: **verified**. The owner opened the canonical build on a physical iPhone
in Safari and reported that everything looked good. The pass covered the owner
view, guest share, backup host, approval inbox, starter bot gallery, Library,
bot template import and copied routine steps. No app file changed; the app SHA
stays `2e3fd5470804d6f1427de0959d05dc1ec36b193edf01c94002792f85b952f985`. This
closes the physical box for build `2026-11-29` only. Older physical-device boxes
remain open until each flow is separately confirmed.

## 2026-11-29 — Approval inbox, bot gallery, local Library, template share and more routines (published and verified)

Status: **published and verified** (planned before edits). After re-reading the
Grok Bot video, the owner said to do whatever is best for the app and then
approved all five safe ideas. This build keeps every useful idea device-local,
plain-language and approval-first.

Intended change:

1. Add a **local Approval inbox** that gathers pending chat approvals from every
   conversation: own-connector actions, host tool actions and draft cards. Each
   row shows the bot name, plain action and a short preview — never a token,
   endpoint secret, cloud state or borrowed account.
2. Keep the exact existing decisions: connector and host tool rows offer only
   **Allow once / Deny** in the inbox (no Always allow, no auto-approve); draft
   rows offer Edit / Copy / Publish / Cancel. Publish still creates a normal
   connector approval card and does not post until Allow once.
3. Add a small **pending count** in Profile and the command palette, plus a plain
   “Approvals” quick action. Opening a row switches to that chat, keeps the card
   visible in its original place, and focuses the same approval controls. Guests
   see only their own pending items; nothing goes to cloud, console or bridge.
4. Add a **starter bot gallery** with one-tap local bots modelled on the video's
   useful jobs (community moderator, newsletter, SEO/AEO, Slack reply drafter,
   YouTube engagement). Each bot gets a name, job, persona and opener, but no
   connector is attached until that person adds their own account.
5. Add a **device-local Library** for saving useful drafts, briefs, source cards
   and images from any chat, then reusing them in any bot. It remains
   guest-isolated, excluded from cloud state and never injected into prompts
   unless the user explicitly chooses an item.
6. Add **share a bot template** as a link or file containing only the bot's name,
   job, description, persona and hero. The recipient imports a fresh local copy;
   no login, token, shared account, chat history or cloud state travels with it.
7. Extend **routine templates** with a weekly digest and a foreground-only
   interval reminder. They copy honest iOS Shortcut/webhook steps and keep the
   existing “runs only while your phone is awake” wording.
8. Bump the marker to `2026-11-29`, extend the harness for all five paths, run
   local/live harnesses and browser smoke, verify SHAs, then re-freeze only after
   verification. Physical iPhone confirmation stays a separate open checklist.
   No Orgo cloud computer, Composio token broker, xAI key, browser control,
   hidden token, always-allow action or background claim is added.

Shipped in build `2026-11-29`: local harness PASS and live harness PASS on both
sites. App SHA `2e3fd5470804d6f1427de0959d05dc1ec36b193edf01c94002792f85b952f985`
was verified byte-for-byte on the live source, published copy, canonical site and
backup site. The bridge stayed unchanged at
`eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`, the worker at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`, the config-gated
callback at `2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`,
and the frozen mockup at
`320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.
Published in Pages commit `2b11d59`; zero console errors on owner, guest, backup
and bridge-host pages. Emulated 320/360/390/430 px checks confirmed no horizontal
overflow and reachable approval inbox, starter gallery, Library, template
share/import and routine controls on owner and guest sessions. The physical
iPhone Safari pass was later confirmed by the owner and closed separately;
older physical-device boxes remain open. Baseline, rollback, README, workspace
snapshot and manifest were re-frozen only after those checks passed.

## 2026-11-28 — Chief-of-staff routing, connector catalog/bot desks and routine templates (published and verified)

Status: **published and verified** (planned before edits). The owner watched the
Grok Bot reverse-engineering video and approved all three recommended upgrades.
This build borrows the useful ideas — one routing bot, one desk per specialist,
and ready-made routine handoffs — without copying the paid/always-on parts of that
stack.

Intended change:

1. Add **chief-of-staff routing**: plain requests in one chat are handed to the
   right specialist bot with a short, readable handoff card. No extra login, no
   context switching, and no change to custom chat names or user messages.
2. Add a plain-English **connector catalog** and local **bot desk** cards. Each
   desk shows the bot's assigned connector, memory/project state, routine count
   and last approval. Tokens stay encrypted device-local; the model still sees
   only connector names, and approval remains Allow once / Deny only.
3. Add **routine template handoff** cards for daily briefs, mention checks and
   draft posts. They produce copyable iOS Shortcut/webhook steps and plainly say
   they need the app open in the foreground; no background claim.
4. Keep every existing connector, guest/owner gate, deep search, source card,
   team, voice, image, approval and bridge rule unchanged. Bump the marker to
   `2026-11-28`, extend the harness for the new paths, run local/live harnesses
   and browser smoke, verify both app SHAs and the unchanged worker, then
   re-freeze only after verification. Physical iPhone confirmation stays a
   separate open checklist. No Orgo computer, Composio token broker, xAI key,
   browser control or hidden token is added.

Shipped in build `2026-11-28`: local harness PASS and live harness PASS on both
sites. App SHA `6cde3091390818902b0383f411f1d8566914f4f6cb9afe769708ea206844acb8`
was verified byte-for-byte on the live source, Pages copy, canonical site and
backup site. The bridge stayed unchanged at
`eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`, the worker at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`, the config-gated
callback at `2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`,
and the frozen mockup at `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.
Published in Pages commit `2429f93`; zero console errors on owner, guest, backup
and bridge-host pages. Emulated 320/360/390/430 px checks confirmed no horizontal
overflow and reachable routing, catalog, desk and routine-template controls;
the physical iPhone Safari pass remains a separate open checklist. Baseline,
rollback, README, workspace snapshot and manifest were re-frozen only after those
checks passed.

## 2026-11-27c — OAuth-ready setup, draft cards, automation handoff, first-run actions and Memory/Projects (published and verified)

Status: **published and verified** (planned before edits on 2026-11-26). The owner
said “let’s do all of it” after being offered the next improvements. This build
keeps the same free-tier, device-local, approval-first rules and does not use a
VM, paid plan, browser control or borrowed login.

Intended change:

1. Add an **OAuth-ready Connect with Instagram** path. The app can be configured
   with a public Meta App ID and HTTPS callback on the existing free Pages host;
   until configured it honestly falls back to the current own-token setup. No
   client secret is ever placed in the HTML, chat, cloud state, bridge or prompt.
2. Turn “Draft a post” into a real **draft card** with Edit, Copy, Publish and
   Cancel actions. Publishing still goes through the existing own-connector
   approval card; Cancel only discards the local draft card.
3. Replace the raw connector form with a plain-English **setup wizard**:
   choose own Instagram or own webhook, explain that it is their account, add
   the credential, run a one-time Test connection, then finish. Tokens stay
   encrypted device-local and are never shown again.
4. Add an **automation handoff card** for “monitor/schedule”. It explains the
   foreground limit and gives copyable iOS Shortcuts/webhook steps for the
   person’s own automation, without claiming background control.
5. Add **first-run quick actions** on empty/new chats so guests and phone users
   can discover Check Instagram, Draft a post, Connect Instagram and Set up
   automation without knowing hidden syntax.
6. Add **Memory and Projects** on-device: a Projects panel for grouping work and
   a small user-controlled memory list that can be included in prompts only when
   enabled. Guests get their own device-local copy; nothing syncs to cloud state.
7. Keep every existing command, approval, privacy gate and guest/owner boundary
   working. Bump the marker to `2026-11-27c`, extend the harness for the new
   paths, run local/live harnesses and browser smoke, verify both SHAs and the
   unchanged worker, then re-freeze only after verification. Physical iPhone
   confirmation stays a separate open checklist.

Shipped in build `2026-11-27c`: local and live harness PASS; app SHA
`800f07cdc3bd76f2dbbc7b99fe92ce626f7e8de83879be4236515c1c5f5698f1` verified byte-for-byte
on the source, published copy, canonical and backup sites; service worker unchanged
at `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`; bridge
unchanged at `eb86840cf681ef57881244d87bc2f0bad57c593fb0673118c356429600661e20`.
Published in Pages commit `0d6a506`. Zero console errors on owner, guest,
backup and bridge-host pages; owner/guest/host command matrix and 320/360/390/430 px
layout emulation passed. The free Pages callback is deployed at
`/api/instagram-oauth/callback` with SHA
`2adb97b605d9ffe749d3b5d83934a8ebe6ff61ad34ae5eaff1aa6f345e271eda`; it returns
a controlled, secret-free “Not configured” page until the owner supplies the
Meta App ID, server-side app secret, redirect URI and scopes as Pages secrets.
Private Development-mode tester access can then be enabled; public/guest access
still needs Meta App Review / Advanced Access. OAuth remains config-gated: no
client secret exists in the HTML, chat, console, cloud state, bridge or prompts.
Draft cards, the guided connector wizard with
Test connection, first-run quick actions, automation handoff, opt-in Memory and
Projects were verified in the browser. Physical iPhone confirmation remains a
separate open checklist.

## 2026-11-27b — Plain-language connector automation (published and verified)

Status: **published and verified**. The owner said the exact connector wording was
hard to remember and not user friendly, and wants Oracle to feel very user
friendly and automated, like Grok. This build keeps the same device-local,
approval-first safety but moves the complexity behind the scenes.

Intended change:

1. Add a local intent parser so normal phrases such as “connect my Instagram”,
   “check my Instagram”, “post this to Instagram” and “monitor my DMs” are
   understood without special syntax. No secret, token or account value is read
   from the phrase; only the intent and optional public image URL are used.
2. Auto-select the matching own-account connector on the device. A check or
   publish intent creates the same approval card the model used to request, with
   plain wording and Allow once / Deny only.
3. If no matching connector exists, “connect my Instagram” opens My Connectors
   with Instagram preselected; “check my Instagram” opens setup and explains
   that Oracle uses the person's own account, never the owner's.
4. Add compact quick buttons under the composer for Socials Bot and connector
   chats: Check Instagram, Draft a post, Connect Instagram, and Set up
   automation. They fill or run the same normal-language path.
5. “Monitor my DMs / emails / Instagram” does not pretend to run in the
   background. It answers plainly that one check is available now and offers a
   Shortcuts/webhook handoff as the free, user-owned automation path.
6. Keep the explicit `CONNECTOR {…}` line working for models as a fallback.
   Guests, phone users and owner all get the same plain-language path; tokens
   still remain encrypted on that person's device and never enter cloud state,
   prompts, bridge logs or console.
7. Extend the harness for the intent parser, auto connector selection, quick
   buttons, honest monitoring answer and unchanged privacy gates. Bump the
   marker to `2026-11-27b`, run local/live harnesses and browser smoke, verify
   both SHAs and the unchanged worker, then re-freeze only after verification.
   Physical iPhone confirmation stays a separate open checklist.

Shipped in build `2026-11-27b`: local and live harness PASS; app SHA
`1ee397885f4eee930cd77deef400feb362ce6b8559e95f74c2bfcfd765f032c5` verified byte-for-byte
on the source, canonical and backup copies; service worker unchanged at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`; zero console
errors on owner, guest, backup and bridge-host pages. Published in Pages commit
`36f733a`. Plain phrases, quick buttons, guided setup, check/publish approval
cards and the honest monitoring answer were verified in the browser. Physical
iPhone confirmation remains a separate open checklist.

## 2026-11-27a — Deep Search, source cards, own-account connectors and truthful wording (published and verified)

Status: **published and verified**. The owner asked for another Grok deep dive, then
said "do whatever you suggest"; the top-ranked free-tier gap was Deep Search with
better source cards. The owner also reported that Socials Bot said it could not
log into Instagram while its guide implied it could create and manage posts, and
then clarified that **everyone** using the app should be able to connect their
own accounts. That overpromise is corrected here, and own-account connectors are
built in this same build rather than deferred. "Own-accounts-only" means each
person connects their own Instagram/email/webhook with their own token on their
own device — guest and phone users included. It does **not** mean owner-only;
host tools/vault/memory/routines stay owner-only. Nobody borrows the owner's
accounts, and the assistant never receives, creates or displays a token.

Intended change:

1. Add a per-chat **Deep Search** toggle to the chat More menu for owner, guest
   and host. It is off by default, stored only in non-secret chat state, and
   changes one-query link lists into multi-query, dated source cards.
2. Fan out up to three public queries (the existing normalized query, a
   recency variant, and a city variant when a city is saved) through the existing
   `/api/gdelt` news proxy, dedupe by URL, cap at 12 dated sources, and keep the
   existing Wikipedia fallback for hosts without the Pages Function.
3. Add an optional owner/static **domain filter** to Web search settings, applied
   as `site:` clauses to Deep Search queries only. No API key, cloud key, token
   or account is added, and guest sessions never read this owner setting.
4. Render each source as a compact card with title, publisher domain, date,
   snippet and a "Why this source?" disclosure that says it is a public page
   found by the named query. Keep the 320–430 px layout readable.
5. Put numbered, query-labelled source text into the system prompt so every
   backend (on-device, custom cloud, Mac bridge) can cite the same sources, and
   label bot notes with "Deep Search" when the mode is on.
6. Fix bot wording: Socials Bot plans and drafts posts but cannot log into or
   manage an Instagram account yet; Oracle Bot's guide says the same. State
   plainly that the app cannot drive the device browser like a person or keep
   monitoring/posting in the background on a phone, and that actions run only in
   the foreground after approval. Add explicit no-external-account and
   no-background-control rules to both the browser identity prompt and the
   bridge system prompt until a future approved own-account connector exists.
   Saved workspaces also get a targeted migration: only the exact old seeded
   Socials Bot description/preview and Oracle Bot guide are replaced, leaving
   custom chat names, notes, preferences and user messages alone.
7. Extend the parity harness for the build marker, Deep Search query fan-out,
   domain clauses, source dedupe, source-card rendering, guest/owner visibility,
   offline and explicit-off zero-fetch behaviour, and unchanged service worker.
   Bump the build marker to `2026-11-27a` only after local checks pass.
8. Add **My Connectors** to Profile for owner, guest and phone. Two free,
   own-account connector types are supported: an Instagram connector using the
   person's own Meta Graph API token/account ID, and a generic webhook using the
   person's own URL and optional token. Connector metadata stays in device-local
   storage; tokens are encrypted in the existing device vault. Nothing is sent
   to the bridge, cloud state or the model, which sees connector **names only**.
9. Add an approval card for connector actions. The model may request a
   `CONNECTOR` line (check account or publish/draft), the app shows the exact
   target and payload, and nothing runs until the person taps Allow once. Deny
   is always available; no always-allow rule can be saved for a connector.
   Instagram publishing still depends on the person's own Meta app/token and a
   public image URL, so the UI says that plainly instead of pretending to log in.
10. Publish to both sites, verify byte-identical app SHAs and the unchanged
    worker, smoke-test owner/guest/host pages with zero console errors, then
    refresh the rollback baseline and restore script only after those checks
    pass. Start a separate physical-device checklist section for the phone
    confirmation.

Shipped in build `2026-11-27a`: local and live harness PASS; app SHA
`a640db6d59a509542d299986ea328fe4115bf50994d7a7a8fc93dc808039a4b0` verified byte-for-byte
on the source, canonical and backup copies; service worker unchanged at
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`; zero console
errors on owner, guest and backup pages. Published in Pages commits `a03bf20`
and `9141795`. The saved-wording migration was added after the first live smoke
showed older cached chats, then re-published and re-verified. Physical iPhone
confirmation remains a separate open checklist.

## 2026-11-26b — Team + trigger manager and automatic free cloud model (published and verified)

Status: **published and verified** — this entry was recorded before any code edits. The owner chose
to build the team/trigger manager first, to keep any future guest connectors
**own-accounts-only** with tokens on the guest device, and to stay on the free
tier with no always-on cloud VM. For the later personal-assistant connectors,
the owner wants every person to own and connect their own Instagram/email pages
using the best free method, with approval first and the ability to give a bot
chat consent that upgrades only that bot's privileges.

Intended change:

1. Add an owner-only **Teams & Triggers** manager for named bot teams with roles,
   an ordered handoff chain, and active/paused state.
2. Add trigger rules: **manual**, **keyword**, and **daily schedule**. Every
   rule is owner-approved, pausable, and stored with non-secret owner state.
3. Keep guests isolated: no team UI, no chain execution, and no cloud-state
   writes. Static/phone owner sessions use device-local, per-session rules with
   approval; host tool actions still use the existing owner approval path.
4. Add safe runtime hooks that enqueue chain steps. On the free tier, scheduled
   rules run while the app or owner bridge is active; there is no app-closed
   cloud VM.
5. Extend the harness for owner/guest gates, paused-rule enforcement, chain
   order, and cloud-state exclusion of guest/vault data; verify both live sites
   and the unchanged service worker.
6. Publish a git-backed `WORKSPACE/` snapshot so another model or a new PC can
   resume from the repo. Include source, frozen/offline files, baselines,
   bridge/browser/routine scripts, harnesses, regression docs, icons and
   runtime scripts. Exclude `.oracle-venv`, caches, OS files, local logs,
   `.oracle-backups`, and live `oracle-shared/sessions.json` because those are
   machine-local runtime/session data, not source. Record a SHA manifest.
7. Add an automatic free-cloud-model pull on the owner bridge. Read OpenCode's
   `/api/model` catalog, cache the newest active free chat model, use it for
   cloud chat, and on `free-limit` force a refresh and retry the next free model.
   Show the selected model in status/Computer panel; never expose provider keys.
8. Record the personal-assistant connector policy: each person connects and owns
   their own Instagram/email pages; use the best free webhook/API method; sending
   and replying start approval-first; chat consent may widen only that bot's
   privileges and never another guest's or the owner's vault. Connectors are a
   later build, not silently added to this one.
9. Seed an **Oracle Bot** room for every person: owner and guest workspaces each
   get one non-duplicating room with a pre-made “how to use Oracle” guide. It can
   explain the app, draft UI/bug-fix instructions and use host tools only for the
   owner with an approval card; guests and phone users get guidance, not host
   file/vault access.
10. Bump the build marker to `2026-11-26b` only after local and live tests pass.

Verified after publication: local harness PASS, live harness PASS on both
canonical and backup, app SHA `230ae9cad770e595506da9b694ac73d81f96bd6ffb6341917784145d1d5f7953`
served byte-identically by both sites, unchanged service worker SHA
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`, bridge
SHA `4bf1df9fdbee35fc39dae6dc374d84f900447d2e2581a57eae2554be134ed922`
with `/api/status` showing the active free model `seaglass-alpha-free`, and zero
browser console errors on owner and guest pages. Pages commits: `e736d02`
(feature), `ee16af2` (modal bindings), `fce6b8c` (rule-form validator fix).
The live rollback baseline and restore script were refreshed only after those
checks. One UI bug was caught in live browser testing — the rule form wrapped a
single raw rule in `teamValidate()` incorrectly — and fixed with a dedicated
`teamRule()` helper before final publication. The owner then confirmed on a
physical iPhone that Home Screen auto-update, the exact Idaho Falls lookup
prompt, Socials Bot fields/template, the single seeded Oracle Bot guide room,
guest-hidden Teams & Triggers, and pause/approval behaviour all work at
320–430 px; the phone checklist is now fully complete.

## 2026-11-26 — Grok Bot parity (published and verified)

Status: **published and verified** — build `2026-11-21m` → `2026-11-26a`.
App SHA: `5b804997b2c63475a4314c36ffe2806bbf5e246e01017f490fe66d0cfabb7db4`.
Pages commits: `5c06979` (app + cloud function), `9546db5` (console-clean
missing-binding response). Service worker unchanged:
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge SHA: `1e7dbcabd5af7637e06b0db51924c2fac2d58d716e4388188d10e5a7e4e59d95`.
Bridge gains one owner-only `/api/computer` status/control endpoint; all
existing guest denials stay intact. Cloud state is a free Cloudflare Pages
Function backed by D1 and needs a one-time `ORACLE_DB` binding in the Cloudflare
dashboard. Re-frozen the live rollback baseline only after the local and live
harnesses passed, both sites served matching app bytes with zero console errors,
and the restarted owner bridge passed owner/guest `/api/computer` checks.

Completed after publication: the owner created the free D1 database
`oracle-chat-cloud` in the signed-in Cloudflare dashboard, bound it as
`ORACLE_DB` to both Production and Preview on the `oracle-chat` Pages project,
and retriggered the latest deployment. The canonical
`/api/cloud-state?key=cs-harness-check-123` then returned `{"ok":true,"state":null}`
with HTTP 200. No app or service-worker bytes changed; only Cloudflare config and
handoff docs did.

The user asked for research into Grok Bot and then chose **full parity**. The
official sources reviewed were `x.ai/grok`, `x.ai/bot/guides/grok-bot-101`,
`docs.x.ai/grok-bot/get-started`, `docs.x.ai/grok-bot/overview`, and the
`Introducing Grok Bot 1.0` announcement.

Grok Bot's headline features are: one-job bots defined by Name/Title/Description,
chat-driven setup, voice note and voice chat, per-bot memory/preferences, skills,
routines and triggers, approval cards with allow/deny rules, a vault with secure
forms and human handoff, connectors/MCP/plugins, multi-bot teams and chains, a
bot marketplace, a persistent cloud computer with remote takeover, and mobile
control of that computer.

GitHub/git cannot be a live VM: Pages is static and the repo is only source
and deploy history. The user then chose the best free runtime, so **Cloudflare
D1 + Pages Functions is the cloud brain**. It keeps non-secret owner workspace
state alive when the Mac is off. The owner Mac bridge remains a local tool
path, not a dependency for anyone else's session. Guest sessions stay isolated
on each guest device. No cloud API key ever leaves the existing encrypted
device vault. iOS image/video generation remains deliberately unavailable.

Intended change:

1. Add a local opener generator that reads the bot's name, title/job and
   description, then asks two or three questions specific to that role. A bot
   named "Socials Bot" asks about platforms, audience and posting goals. No
   model call or network fetch happens when a room is created.
2. Add Name/Title/Description to new-room and bot-edit flows, with a small local
   template gallery for common one-job bots.
3. Include the bot identity and durable per-bot preferences in the system
   instruction sent to both on-device and bridge models.
4. Add a "teach this task" flow that turns a repeated instruction into an
   owner-approved skill or routine draft. The device path stays whitelist-based;
   the host path stays owner-only.
5. Add bot-to-bot handoff/team chat for owner sessions, with a visible chain and
   no guest access.
6. Add `/api/cloud-state` as a free D1-backed Pages Function with a clear
   `binding-missing` degradation until the owner binds `ORACLE_DB`. No secrets,
   vault entries, tool results or guest data are sent to it.
7. Add an owner-only `/api/computer` panel: status, connector names, vault
   credential names, secure-form names, and routine pause/resume. Guest tokens
   are denied; the model never receives secret values.
8. Keep host-only tools, connectors, approval rules and routines on the owner
   Mac bridge; phone/static routines stay device-local, per-session,
   whitelist-based, and gain a paused state. Multi-bot handoff is owner-only and
   visible in chat.
9. Add `site:x.com` style public lookup through the existing news proxy while
   keeping explicit-off and offline paths at zero fetches.
10. Bump the build marker to `2026-11-26a`. Existing chats are untouched.

Out of scope because they would break settled rules or require new
infrastructure: a real cloud VM with shell/browser compute while the owner Mac
is off, automatic guest SaaS connectors, cloud-stored API keys, and iPhone
image/video generation. Cloudflare D1 supplies always-on non-secret state only;
the owner must bind `ORACLE_DB` once in the dashboard.

## 2026-11-23 — Bing-first news proxy for Cloudflare workers (published and verified)

Status: **published and verified** — build `2026-11-21l` → `2026-11-21m`.
App SHA: `7e83fe68bcef9e7b2b409639d177365bb8d5f864845a1957f75ce370325bb78b`.
Pages commit: `866b5a5`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge unchanged: `4166484c20c2d19b9a21d8f02b0b7f57445abeaf291ddb078307be51d82973db`.

Build `l` published the same-origin proxy, but Google News RSS is blocked or
fails from Cloudflare's worker network. The live function then fell through to
GDELT, which returned a real article after 44 seconds — too slow for a phone
lookup. Bing News RSS returns dated local articles in under a second from the
same public feed, so the function should try Bing first, then Google News, then
GDELT. The app-side normalization, source block, off/offline rules and fallback
to Wikipedia are unchanged.

Intended change:

1. Add a Bing News RSS parser to `/api/gdelt`, ahead of Google News and GDELT.
2. Keep the GDELT rate-limit-aware retry and the app's Wikipedia fallback.
3. Update the About text and bump the build marker to `2026-11-21m`.

Shipped in `2026-11-21m`: `/api/gdelt` parses Bing News RSS first, then Google
News RSS, then GDELT (one 5.2-second rate-limit-aware retry). Bing links are
cleaned from their `url=` redirect parameter into the publisher URL, with the
publisher hostname as the source label. The app still normalizes lookup phrasing,
posts the query to the same-origin function, and falls back to Wikipedia whenever
the proxy returns zero items.

Harness verified: the exact user phrase normalizes to `Idaho Falls`; mocked Bing
RSS produced a cleaned publisher URL/date; mocked Bing+Google failures still
reached GDELT; the app made one POST to `/api/gdelt` and injected the source
block; empty proxy results fell through to Wikipedia; explicit off made zero
fetches; forced-phone compat still loaded a real GGUF with `n_ctx:2048`,
`n_gpu_layers:0`, `n_threads:1`; non-isolated phones still got the clear
canonical-site message; guest/host model scope stayed 2 device / 4 host.
Live: both sites serve the new app SHA and unchanged worker; canonical returns
COOP/COEP; a real `Idaho Falls` lookup returned four dated local links in 0.47 s;
backup skipped the proxy and got Wikipedia; owner/guest/backup smoke had zero
console errors. Physical iPhone retest remains open.

## 2026-11-23 — Real news lookup through same-origin proxy (published; superseded by m)

Status: **published and verified (app)** — build `2026-11-21j` → `2026-11-21l`.
App SHA: `5b33215964103f8f92ff890475f4e507578a226b3b75d33f25d705b547c628fa`.
Pages commit: `4eee091`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge unchanged: `4166484c20c2d19b9a21d8f02b0b7f57445abeaf291ddb078307be51d82973db`.
The app-side lookup and fallback paths passed harness and live checks, but the
Google News fetch fails from Cloudflare workers; build `m` replaces it as the
first source with Bing News RSS.

Status: **planned before edits** — build `2026-11-21j` → `2026-11-21l`.
Service worker expected unchanged (the proxy is POST, which the SW ignores).
Bridge unchanged.

The user asked "Please look up Whats going on this week in idaho falls" on build
`j` and got a generic answer. Live browser check found the real cause: GDELT's
API sends **no `Access-Control-Allow-Origin` header**, so `webSources()`'s fetch
is blocked by CORS before any result exists. The old code then skipped its
Wikipedia fallback entirely because the GDELT failure escaped to the outer
catch, so the model received no source block and answered from memory.

Intended change:

1. Add a Cloudflare Pages Function at `/api/gdelt` that accepts POST JSON
   `{query}`. It fetches Google News RSS server-side first (fast, no key, real
   dated local articles), then GDELT with one rate-limit-aware retry, and returns
   normalized articles. POST avoids the service worker's GET-only cache. GitHub
   Pages has no function, so that host skips the proxy and goes straight to
   Wikipedia.
2. Normalize lookup questions before querying news: strip "please look up",
   "what's going on", "this week", etc., so "Please look up Whats going on this
   week in idaho falls" becomes the phrase `Idaho Falls`.
3. Make `webSources()` always try Wikipedia when the proxy yields no usable
   items, including when the proxy fails. Keep online/offline and explicit-off
   rules unchanged.
4. Bump the build marker to `2026-11-21l`.

## 2026-11-23 — wllama 4.0.0 abort fix + phone CPU load (published and verified)

Status: **published and verified** — build `2026-11-21i` → `2026-11-21j`.
App SHA: `2c769b7485deac2147ef3e6af5f519ed962b1bfc22b71096343ae84a284f7d38`.
Pages commit: `ddf8fea`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge unchanged: `4166484c20c2d19b9a21d8f02b0b7f57445abeaf291ddb078307be51d82973db`.

Physical iPhone retest of build `2026-11-21i` still shows `Model error:(ABORT)`
on lookup prompts, even though the canonical site is now cross-origin isolated.
The user confirms: Web search off + casual question gives an answer; Web search
on + simple "hi" gives an answer; only internet/lookup prompts abort. The error
still has no stack, so wllama 3.6.1 is swallowing the real abort reason.

Upstream wllama `4.0.0` (released 22 Nov) contains PR #333: it extracts the real
abort reason (`reason?.message ?? String(reason)`), validates memory64 modules,
retries iOS shared-memory allocation in 128 MB steps, and retries OPFS handles
that WebKit closes mid-write. The OPFS cache key format is unchanged
(`${hashSHA1(fullURL)}_${fileName}`), so saved GGUF weights are reused.

Intended change:

1. Move `WLLAMA_JS` to `@wllama/wllama@4.0.0/esm/index.js` and the default WASM
   to `@wllama/wllama@4.0.0/esm/wasm/wllama.wasm` (the 3.x `src/wasm` path is
   gone in 4.0.0). Keep `setCompat('default')` so the 4.0.0 compat WASM is used.
2. Keep the memory64 probe, forced compat selection and COOP/COEP guard.
3. On phones using compat, load with `n_gpu_layers:0` and `n_threads:1` so iOS
   does not try GPU offload or extra pthreads. Desktop options stay unchanged.
4. Tag model errors with stage (`load`/`chat`), COI, compat and phone-option
   state so a future bare abort is diagnosable without another guess.
5. Bump the build marker to `2026-11-21j`.

Shipped in build `2026-11-21j`: the app loads wllama 4.0.0 from
`@wllama/wllama@4.0.0/esm/index.js` with its default module at
`.../esm/wasm/wllama.wasm`. The earlier memory64 probe, forced compat selection
and COOP/COEP guard are unchanged. On a phone using compat, GGUF loading now
passes `n_ctx:2048, n_gpu_layers:0, n_threads:1`; desktop keeps wllama defaults.
Model errors now read `[wllama load] … (coi=…, compat=…, phone=…)` or
`[wllama chat] …`, keeping any decoded abort stack. No bridge, vault, guest/host
scope or web-context change.

Harness verified: a forced-phone page under COOP/COEP with the broken-probe
simulation hid JSPI, selected compat, loaded a tiny GGUF through the app's own
`loadDeviceModel()` and produced a completion with zero console errors; a
prototype spy confirmed the load options were `n_ctx:2048, n_gpu_layers:0,
n_threads:1`; the non-isolated page threw the clear canonical-site message;
empty-stack aborts gained the context tag; online search made 1 source fetch,
explicit off and offline made 0, and a stubbed send injected the source block.
Owner/guest/host model lists stayed 4 device / 2 device / 4 host backends.
Live: both sites serve the new app SHA and unchanged worker; canonical returns
both isolation headers; owner, guest and backup smoke tests had zero console
errors. Physical iPhone retest remains open.

## 2026-11-23 — Cross-origin isolation for wllama compat on iPhone (published and verified)

Status: **published and verified** — build `2026-11-21h` → `2026-11-21i`.
App SHA: `95bb49c83bebf4a8f4fc13fbb1ba3f1a44c7a54a0f529756324a927fdfe1bed8`.
Pages commit: `c708893`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge unchanged: `4166484c20c2d19b9a21d8f02b0b7f57445abeaf291ddb078307be51d82973db`.

On the physical iPhone, build `2026-11-21h` moved past the silent hang but the
Smart 0.6B load now ends in `Model error:(ABORT)`. The compat WASM that the
earlier fix selects imports a **shared** WebAssembly memory (import flags `0x3`,
initial 2048 / max 65536 pages). WebKit only allows shared memory in a
cross-origin-isolated document, and headers check shows neither live host sends
`Cross-Origin-Opener-Policy` or `Cross-Origin-Embedder-Policy`. So the compat
module cannot instantiate and Emscripten aborts before the GGUF is read.

Intended change:

1. Add `oracle-pages/_headers` with `Cross-Origin-Opener-Policy: same-origin`
   and `Cross-Origin-Embedder-Policy: require-corp` for all paths. Cloudflare
   Pages honours this; GitHub Pages ignores `_headers`, so the canonical site is
   the iPhone-capable host.
2. Keep the memory64 probe / forced compat selection from `2026-11-21f`.
   Before loading on a phone where compat was forced, require
   `self.crossOriginIsolated`; otherwise fail early with a clear message that
   points to the canonical site instead of showing `(ABORT)`.
3. Keep the existing CDN assets: jsDelivr sends `cross-origin-resource-policy:
   cross-origin` and CORS headers, so module imports/WASM still work under
   `require-corp`. HF, GDELT and Wikipedia are fetched with CORS.
4. Bump the build marker to `2026-11-21i`.

Shipped in build `2026-11-21i`: Cloudflare Pages now sends COOP `same-origin`
and COEP `require-corp` for every path, so `self.crossOriginIsolated` is true
and the compat WASM's shared memory import can instantiate on iPhone. The
existing memory64 probe / compat selection is unchanged. On a phone-like build
that is **not** isolated (the GitHub Pages backup), model loading now fails
immediately with "On-device models need the main Oracle Chat site on iPhone…"
instead of wllama's bare `(ABORT)`. Wllama abort errors now keep the decoded
stack (first 360 chars) so future failures are diagnosable. No model, vault,
bridge or guest/host scope changes.

Harness verified: forced-phone build under COOP/COEP reported
`crossOriginIsolated:true`; the broken-probe simulation still hid JSPI and
called `setCompat('default','firefox_safari')`; a real 260K GGUF loaded through
the compat WASM and produced a completion with zero console errors. On the
non-isolated harness, the same path threw the clear canonical-site message with
no download. Owner/guest/host model lists stayed at 4 device / 2 device /
4 host backends with zero console errors. Live: both sites serve the new app SHA and unchanged
worker; canonical returns both isolation headers and reports COI true; backup
reports COI false as expected; zero console errors on owner, guest and backup.
Physical iPhone pass remains open.

## 2026-11-23 — Internet context for every model and user (published and verified)

Status: **published and verified** — build `2026-11-21g` → `2026-11-21h`.
App SHA: `04198568b1cdc6b47c5a062a87ad6cfa3799a0146cab654072322c7697420776`.
Pages commit: `df46582`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.
Bridge unchanged: `4166484c20c2d19b9a21d8f02b0b7f57445abeaf291ddb078307be51d82973db`.

The owner asked for every model to have internet access whenever the device is
online. This deliberately supersedes the old "guests never make network
requests" and owner-only phone search rules. Intended change:

1. `webSearchOn()` is true whenever `navigator.onLine` is not false, for owner,
   guest and host alike. An explicit `oracle.websearch=0` still turns it off.
2. `webSources()` no longer rejects guest or host builds. The browser fetches
   GDELT/Wikipedia directly for every chat, and the source block is added to
   the system message for **all** backends (device models, custom cloud, host
   local/deep/auto/cloud). The bridge already forwards system text to both
   Ollama and the cloud tool, so no host bridge change is needed.
3. Update the setting copy and the handoff rules to record the reversal:
   guests and host now make public search requests when online. Offline still
   works — failed fetches return no sources and chat continues locally.
4. Bump the build marker to `2026-11-21h`.

Shipped in build `2026-11-21h`: every chat model — Tiny, Balanced, Smart,
Unfiltered, custom cloud, and the host's local/deep/auto/cloud backends — gets
public GDELT/Wikipedia source context whenever the device is online, for owner,
guest and host sessions alike. Offline or an explicit Web search "off" still
means zero fetches and a fully local answer. No bridge, vault or key change was
needed: the browser adds the source block to the system message, which the
bridge already forwards to Ollama and the cloud tool.

**Rule change recorded deliberately:** this supersedes the earlier guarantees
that guests make no network requests and that phone search is owner-only.
Guest and host questions now reach public search services when online.

Harness verified: owner, guest and host each produced one stubbed search fetch
and one source; offline and explicit-off produced zero fetches and null sources;
all nine backends (4 device ids, custom cloud, local, local-deep, auto, cloud)
received the source block in their system message; zero console errors on owner
and guest, with only the expected static-harness `/api/status` 404 on host.
Both live sites serve the new app SHA and unchanged worker SHA. The backup site
needed one reload to clear browser cache; after reload all three smoke pages
reported build `2026-11-21h` with owner/guest search on and zero console errors.
Physical-device pass remains open.

## 2026-11-23 — Owner phone Web search on by default (published and verified)

Status: **published and verified** — build `2026-11-21f` → `2026-11-21g`.
App SHA: `9cc5d5cd5d3eb02d1378d3b51f8f7b219c069a593db505117acb991453fdefa3`.
Pages commit: `5f86cd4`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

The owner asked for the phone app to have internet access for current
information. The owner-only Web search setting already exists but defaults to
off, so a fresh install makes zero network requests until the owner finds the
switch. Intended change:

1. `webSearchOn()` treats a missing `oracle.websearch` flag as **on** only for
   a non-guest static/phone build. An explicit `0` still means off, so anyone
   who switched it off stays off. Guest and host builds always return false and
   keep making zero network requests.
2. Update the setting's copy from "Off by default" to reflect the new owner
   default, while keeping the guest/offline warning.
3. Bump the build marker to `2026-11-21g`. No bridge, key vault or model change.

Shipped in build `2026-11-21g`: owner phone/static builds now start with Web
search enabled, so current-event questions reach GDELT (then Wikipedia as a
fallback) and the source links are shown under the answer. Guests and the host
still return false from `webSearchOn()` and make zero network requests; anyone
who explicitly switched search off keeps that choice. No API key, cloud key or
bridge path was added — the setting still uses the existing public CORS APIs.

Harness verified: missing flag → owner on with one stubbed fetch and a source;
explicit `0` → off with zero fetches; guest and host → off with zero fetches;
setting copy updated; model visibility unchanged (owner 4 / guest 2 / host 0).
Both live sites serve the new app SHA and unchanged worker SHA with zero console
errors. Physical iPhone pass remains open.

## 2026-11-23 — Force wllama compat build on iOS Safari 27 (published and verified)

Status: **published and verified** — build `2026-11-21e` → `2026-11-21f`.
App SHA: `f8727fd41386698bb039ef41cbecd9dcf3493ff24bbbf85d7d353b6da3ce4fc4`.
Pages commit: `10bacba`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Observed on the physical iPhone with `2026-11-21e`: both `Smart · 0.6B` and
`Balanced · 350M` reach "Loading saved … from this device…" and never settle.
The byte counter reaches 100% and the saved model is recognised, so the
download and OPFS cache are fine. The failure is in wllama's WASM build
selection, not the model size — swapping 1.7B → 0.6B → 350M could not fix it.

Root cause (upstream wllama issue #297): iOS Safari 27 accepts
`new WebAssembly.Memory({address:'i64'})`, so wllama's `isSupportMem64()` probe
returns true, but Safari refuses to compile a module that actually declares
memory64 (`parse at byte 4680: Memory64 is not enabled`). JSPI is also present,
so `needCompat()` returns false and wllama picks the memory64 build. Model
initialisation then hangs forever with no error. The reporter confirmed that
forcing compat mode on the same iPhone loads and runs the model fine.

Intended fix:
1. Add a real memory64 module validation probe
   (`WebAssembly.validate(new Uint8Array([0,97,115,109,1,0,0,0,5,3,1,4,1]))`).
   When it fails on a phone, hide `WebAssembly.Suspending` so wllama's
   `needCompat()` selects its Asyncify/compat WASM build, which Safari can compile.
2. Call `setCompat('default','firefox_safari')` on that path as well, matching
   the confirmed workaround. Desktop behaviour is untouched: the probe passes
   there, so no global is changed and no extra CDN asset is requested.
3. Bump the build marker to `2026-11-21f`. Service worker unchanged (its
   jsdelivr rule already caches the compat WASM/JS after the first online load).

Shipped in build `2026-11-21f`: on-device chat on iOS Safari 27 now validates a
real memory64 module before loading GGUF weights. If Safari reports memory64 but
cannot compile it, the app hides JSPI so wllama selects its Asyncify/compat WASM
build and calls `setCompat('default','firefox_safari')`, matching the workaround
confirmed against upstream issue #297. Desktop browsers pass the probe and keep
the faster default build with no extra requests. This addresses the "Loading
saved … from this device…" hang seen with both 350M and 0.6B; no model files,
vault, guest isolation or host behaviour changed. Service worker is unchanged.

Harness verified: with the broken probe simulated and `PHONE` forced true,
`forceWllamaCompat()` hid JSPI, set `wllamaCompatForced`, and called
`setCompat('default','firefox_safari')`; with a valid probe it changed nothing
and made no compat calls. Owner static shows 4 device models, guest 2, host 0;
build marker and both published SHAs verified on canonical and backup sites;
zero console errors on owner, guest, backup and iOS-simulation tabs. The compat
WASM/JS URLs return HTTP 200 and match the existing jsdelivr cache rule.
Physical iPhone pass remains open.

## 2026-11-23 — Phone-sized Smart model and honest progress text (published and verified)

Status: **published and verified** — build `2026-11-21d` → `2026-11-21e`.
App SHA: `87a4c7e05ca267e55e24c43ec9a476abfa89acfa5ba36152b4d83083bf165ac1`.
Pages commit: `861af4b`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Observed on the physical iPhone with `2026-11-21d`: all three shards downloaded
(`1056 / 1056 MB`) but wllama never finished initializing the 1.7B model. The
page stayed responsive, the shards were recognised as saved on reopen, and
"Loading saved Smart…" still did not settle. The 1.1 GB of weights plus ~235 MB
of KV cache is over this phone's practical budget. The 99% display was also
misleading: the app hard-caps the percentage at 99, so a finished download at
`1056 / 1056 MB` still read "Saving … 99%".

Ship:
1. Replace `qwen3-1.7b-smart` with `Qwen3-0.6B-Q4_K_M` from
   `bartowski/Qwen_Qwen3-0.6B-GGUF` (~462 MiB, single file, same Qwen3
   architecture and wllama runtime). Keep the `device-smart` id and owner/static
   only scope; guests keep 2 device models and host keeps 0. Verified the file
   returns HTTP 206 with GGUF v3 magic.
2. Show "Downloaded — preparing <model> on this device…" when the byte counter
   reaches the total, instead of a frozen 99%. Extract the text into a small
   helper so the harness can assert both states.
3. Leave the shard-aware saved-model code in place — it is harmless for a
   single-file spec and keeps the option open for a future sharded model.
4. Bump the build marker to `2026-11-21e`. Service worker unchanged.

Shipped in build `2026-11-21e`: Smart on-device is now Qwen3 0.6B Q4 (462 MiB)
instead of Qwen3 1.7B. It keeps the `device-smart` id and owner/static-only scope
and uses the same wllama runtime, but fits an iPhone's memory budget. The first
download is a single stream again, so slower per MB than the three-shard 1.7B,
but there is 2.3x less data and the model actually finishes loading. The byte
counter now switches to "Downloaded — preparing … on this device…" at completion
instead of freezing on 99%. The shard-aware cache code remains for future models.

Harness verified: the new spec, single URL and 462 MB menu text; `device-smart`
resolves `qwen3-0.6b-smart`; both progress strings (including the completion
message); shard-aware saved detection still returns true only with every shard;
owner 4 models / guest 2 / host 0; `webSources()` null with zero fetches; the new
model URL returns HTTP 206 with GGUF v3 magic and CORS from the page origin;
zero console errors on all harness tabs (host `/api/status` 404 on the static
harness server is expected). Both live sites and all three smoke-test pages
served the new SHA and build marker with zero console errors. Physical iPhone
pass remains open.

## 2026-11-23 — Parallel shard download for the Smart model (published and verified)

Status: **published and verified** — build `2026-11-21c` → `2026-11-21d`.
App SHA: `e905eed6c99c47e58930258bbce53c54e8544a9f6d578e5809f3d97f1365820a`.
Pages commit: `c50ded8`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Problem: the owner reported the 1.7B Smart model downloading at about 1 MB/s on
gigabit Wi-Fi. The Mac-side CDN measured ~16 MB/s on the same file, so the host
is fast; wllama fetches a single-file GGUF over one stream, and the phone's
single TLS/OPFS write path is the likely bottleneck.

Ship:
1. Point `qwen3-1.7b-smart` at the pre-sharded
   `fukayatti0/Qwen3-1.7B-GGUF-split` Q4_K_M repo (3 GGUF shards: 487 + 485 +
   85 MiB, ~1.1 GB total). Verified the same Qwen3 1.7B architecture and Q4_K_M
   quantization, valid GGUF v3 headers, and `access-control-allow-origin: *`.
   wllama expands the `-00001-of-00003.gguf` filename pattern and fetches all
   three shards concurrently (default `parallelDownloads: 3`), so the same smart
   model downloads in parallel instead of one stream. No quality change.
2. Teach the saved-model / cache check about shards, so a completed download is
   still recognised after refresh, in a new room and offline — no repeat prompt,
   no repeat download. Keep the Wi-Fi/size warning.
3. Bump the build marker to `2026-11-21d`. Service worker unchanged: the existing
   build-marker check detects an HTML-only change.

Shipped in build `2026-11-21d`: the Smart 1.7B option now downloads three GGUF
shards in parallel through wllama instead of one slow 1.28 GB stream. The saved
check now treats a split model as saved only when all three shards are present,
so reuse after refresh / new room / offline stays silent and free. The model
menu and Wi-Fi warning show the new ~1.1 GB size. Everything else is unchanged.

Harness verified: all three shard URLs return HTTP 206 with GGUF v3 magic and
CORS `*` from the page origin; the real wllama 3.6.1 library expands the first
URL into exactly those three shards with `parallelDownloads: 3`; a fake OPFS
listing with all shards is recognised as saved and one missing shard is not;
single-file models still resolve as before; `backend='device-smart'` still
resolves `qwen3-1.7b-smart`; owner keeps 4 device models, guest keeps 2, host
keeps 0; `webSources()` is `null` with zero fetches by default; zero console
errors on all harness tabs (host `/api/status` 404 on the static harness server
is expected). Both live sites and all three smoke-test pages served the new SHA
and build marker with zero console errors. Physical iPhone pass stays open.

## 2026-11-23 — Smarter model options, reusing the existing search path (published and verified)

Status: **published and verified** — build `2026-11-21b` → `2026-11-21c`.
App SHA: `039d48c90ef3f4a1e52d29ce1bd9947da8399eaa9ae42c35c70abeba86316554`.
Pages commit: `5bba1aa`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Audit first confirmed the app already has: an OpenAI-compatible custom cloud
model form with AES-GCM device-vault key storage; a host OpenCode Big Pickle
cloud backend; three small GGUFs; and the GDELT/Wikipedia search added in
`2026-11-21b`. Nothing below duplicates those systems.

Shipped:
1. Add exactly one new owner/static-only GGUF: `Qwen3-1.7B-Q4_K_M`
   (~1.28 GB) as "Smart on-device · 1.7B". Guests and host stay unchanged.
   Keep the existing download-confirmation and progress UI; add a Wi-Fi/size
   warning for this larger file.
2. Extend the existing "Add a model" dialog with provider presets for OpenAI,
   OpenRouter and Anthropic via OpenRouter (direct Anthropic blocks browser
   CORS — verified). No new vault, no new key handling: keys still go straight
   into the existing encrypted device vault.
3. Reuse `webSources()` for custom cloud models as well as device models, so
   the same owner-only, off-by-default search setting supplies current sources
   to every private/static chat. Show the source links under cloud answers.
4. Bridge: pass compact GDELT/Wikipedia source context into the existing
   Big Pickle cloud prompt for owner current-event questions. Guests get no
   search. No new host local model: this Mac has 8 GB RAM and ~5.5 GB free.

Harness verified: owner/static model list contains `device-smart` and resolves
`qwen3-1.7b-smart`; guest keeps 2 models and host keeps 0 device models; the
large-download warning appears; all three provider presets fill the existing
cloud fields (OpenRouter `openai/gpt-6.2-astra`, Anthropic via OpenRouter
`anthropic/claude-sonnet-5.5`); the saved key round-trips through the encrypted
device vault and is sent as `Authorization: Bearer …`; web sources inject into
custom cloud answers with links; Big Pickle cloud prompts receive the same
source context via a stubbed bridge CLI; guests get no search; offline default
still makes zero fetches; zero console errors apart from the expected static
harness `/api/status` 404 on the host tab. Physical iPhone pass remains open.

## 2026-11-21 — Give the models real web search (published and verified)

Status: **published and verified** — build `2026-11-21a` → `2026-11-21b`.
App SHA: `82a1ab7ddb26a3671f7b3f6cef96b023aa47ad039af88391b8af79a7a0839aaa`.
Pages commit: `701cc86`.
Service worker unchanged: `6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Shipped in build `2026-11-21b`: the Mac host now has an owner-only `search`
tool backed by GDELT news and Wikipedia, with the system prompt directing
current/local/recent questions to it before answering. The static/phone app
gains an owner-only, off-by-default "Web search" setting (Profile → Web search,
also in the command palette) with an optional city field. When enabled, public
CORS-safe results are injected as source context before the local model answers,
and links are shown below the reply. Guests and the host build never see it;
with search off, the phone makes no network request and stays fully offline.

Harness verified: owner/guest/host visibility, zero console errors (apart from
the expected static-harness `/api/status` 404 on the host tab), off-by-default
behaviour with zero fetches, source injection into the local model prompt,
rendered source links, the settings modal, and a real host search returning
current dated articles with URLs. Physical iPhone pass remains open.

The owner reports generic answers to questions about current local events in
both the phone app and the Mac host app. The 135M/350M on-device models have no
internet and cannot know current events; the host 3B/4B models have a `fetch`
tool but no general search. Prompt changes cannot supply missing information.

Verified CORS-capable sources: GDELT DOC 2.0 (`api.gdeltproject.org/api/v2/doc/doc`,
`Access-Control-Allow-Origin: *`, recent article titles/dates/URLs, ~1 request
per 5 seconds) and Wikipedia's API with `origin=*`. DuckDuckGo's Instant Answer
API has CORS but returns nothing for news/current-event queries.

Work completed (all three planned items shipped):
1. Host bridge: owner-only `search` tool backed by GDELT and Wikipedia, with a
   compact sources result and a system prompt that directs current questions to
   it. Guests still have no tools.
2. Phone/static: owner-only, off-by-default "Web search" setting with city field,
   source-context injection and source links. Guests and host never see it.
3. Host and phone regression entries added, harness-tested, published, verified
   on both live sites and re-frozen after the harness passed.

## 2026-11-21 — Add an AI handoff folder to the published repo (documentation only)

Status: **documentation only** — no app or bridge code changed, so there is no
new build marker and the live/baseline SHAs stay at build `2026-11-21a`
(`1aa44729b87ba0123ce49b96e05eb2f02fab3b3612b51406f21e2618f6d975f0`).

Add `oracle-pages/AI-HANDOFF/` so a future AI can resume without access to this
local workspace: start-here README, rules/decisions, change workflow, the full
image-generation investigation history, and snapshots of the changelog and both
regression checklists. Add a short pointer from the repo README.

## 2026-11-21 — Stop image generation crashing on iPhones (published and verified)

Status: **published and verified** — final live SHA
`1aa44729b87ba0123ce49b96e05eb2f02fab3b3612b51406f21e2618f6d975f0`;
Pages commit `49d1b5e`.

The physical iPhone diagnosis is now conclusive. The checkpoint reaches
`unet run` under every engine: WebGPU U-Net kills the tab, CPU/WASM U-Net kills
the tab, and hybrid (WebGPU encoder + CPU U-Net) also kills the tab. The encoder
and decoder are fine; the U-Net compute itself exceeds this device's limits.
There is no smaller ready-to-run ONNX model: `sdxs-micro` ships only Python and
safetensors (no browser export), and the other int8 U-Net is larger than the
one already used. Further engine tweaks cannot fix this.

Per owner decision, planned:
1. Detect iOS devices and replace the image-generation flow with a clear
   "not available on this iPhone" message. No U-Net run, no white flash, no
   unnecessary 382 MB image-model download on those devices.
2. Keep desktop WebGPU image generation unchanged. Keep the iOS path guest-safe
   and host-free: no bridge endpoint, key, or cloud call; no credentials shown.
3. Add unchecked host and phone regression entries, harness-test the iOS message
   and unchanged desktop path, publish, verify both live SHAs and re-freeze only
   after the harness passes.

Shipped in build `2026-11-21a`: `imageUnsupported()` detects iOS; the image
window then shows "Images aren't available on iPhone" with a Close button and
no prompt, size, engine or Generate controls. `startImageGeneration()` and
`loadImageRuntime()` both guard before any generation or model download, and
the model menu and command palette show the unsupported status. Desktop WebGPU
generation is untouched. Harness confirmed the iOS message, guards, no download,
command text, unchanged desktop PNG pipeline, and unchanged owner/guest/host
visibility with zero console errors; all three live pages are clean. Physical
iPhone pass is open.

## 2026-11-20 — Hybrid image engine for iPhones (published and verified)

Status: **published and verified** — final live SHA
`cd016f2a4496582c310709594b7f20806326fa7888c7cbfd73be3381f519edb1`;
Pages commit `ba3331d`.

The physical iPhone screenshot showed the CPU build failing at `text encoder
load`: ORT WASM has no implementation for the encoder's `GatherBlockQuantized`
op. Together with the earlier `unet run` checkpoint, the two engines fail at
opposite ends:
- WebGPU on iPhone: encoder loads and embeds successfully; U-Net kills the tab.
- CPU/WASM: U-Net and decoder run correctly; encoder cannot be created.

Local tests with the real pinned model confirmed WASM runs the U-Net (~10 s)
and the FP16 decoder (~5 s) with the same float16 tensors. Planned:
1. Add a `hybrid` engine that uses WebGPU for the text encoder and CPU/WASM for
   the U-Net and decoder. Make it the default on iPhone/iPad; keep WebGPU as the
   desktop default. Keep the existing all-WebGPU and all-CPU choices.
2. Select the provider per model role, include role/provider in checkpoints and
   diagnostics, and update the engine buttons in the image window.
3. Add unchecked host and phone regression entries, harness-test all three
   engines, publish, verify both live SHAs and re-freeze only after the harness
   passes.

Shipped in build `2026-11-20m`: `imageProvider(role)` selects the ORT provider
per model role. The `hybrid` engine (default on iPhone/iPad, and the migration
target for phones left on all-CPU) uses WebGPU only for the text encoder and
CPU/WASM for the U-Net and decoder. All-WebGPU and all-CPU choices remain
available. Engine buttons in the image window now read Phone · hybrid /
WebGPU · fast / CPU · slow; checkpoints and diagnostics record the engine, and
`imageSession()` logs the role/provider. A build that previously stored `wasm`
on a phone is migrated to `hybrid` so the broken encoder path is not reused.
Harness confirmed all three engine/provider maps, defaults, migration, the
full PNG pipeline under hybrid (`webgpu`/`wasm`/`wasm`), UI toggle, diagnostics,
and owner/guest/host plus all three live pages with zero console errors.
Physical iPhone pass is open.

## 2026-11-20 — Add a CPU engine for image generation on iPhones (published and verified)

Status: **published and verified** — final live SHA
`cadf55b14ad0984626dbdb9ad6c176c4341ddc6028c2b59a6ab992696c5210eb`;
Pages commit `a8f5242`.

The checkpoint from the physical iPhone names the failing stage: `unet run`.
That is the WebGPU U-Net inference; the session loads, then iOS kills the tab
on the first compute dispatch. This is a device WebGPU limitation, not memory
in the app's own maps — the earlier memory refactor could not change it.

A local test downloaded the real pinned model and ran the same U-Net through
ONNX Runtime's `wasm` execution provider with the same float16 tensors: it
completed successfully (about 10 s on the Mac, output `noise_pred`). Planned:
1. Add an engine choice in the image modal — WebGPU (fast) or CPU (slower,
   wider support), stored per device. Default to CPU on iPhone/iPad and WebGPU
   elsewhere, so the crashing path is not attempted by default on phones.
2. Skip the WebGPU capability check when CPU is selected; use the CPU provider
   for all three sessions; include the engine in checkpoints and diagnostics.
3. Add unchecked host and phone regression entries, harness-test both engines,
   publish, verify both live SHAs and re-freeze only after the harness passes.

Shipped in build `2026-11-20l`: the image window has an Engine row with WebGPU
and CPU buttons, stored per device in `oracle.image.engine`. iPhones/iPads
default to CPU, desktop stays on WebGPU. `imageSession()` selects the matching
ORT execution provider, the WebGPU capability check is skipped on CPU, and
checkpoints and diagnostics include the engine. A standalone test with the real
pinned U-Net confirmed ORT's CPU provider runs the float16 model correctly
(about 10 s on the Mac). Harness confirmed defaults, toggle persistence, EP
selection for all three sessions, a full PNG result on CPU, engine in
diagnostics, and owner/guest/host plus all three live pages with zero console
errors. Physical iPhone pass is open.

## 2026-11-20 — Survive an iOS tab kill with a checkpoint log (published and verified)

Status: **published and verified** — final live SHA
`14a238e77fa52a79482e1d31331649124f19de224b3f50a0711db8e22083d6f4`;
Pages commit `8f2225f`.

Build `2026-11-20j` reduced peak image memory from ~695 MB to ~313 MB, but the
physical iPhone still shows only a white flash and returns to chat. No error is
recorded and the reload counter stays at zero, so JavaScript never gets to run
an error handler: iOS is terminating the tab. Four builds of speculative fixes
have not helped, so the next step is to find the exact operation that kills it
rather than guess again.

Because a killed tab cannot run a `catch` block, the plan is to write a small
synchronous `localStorage` checkpoint *before* each image stage (including each
cache file read). After the tab is killed and the app reopens, "Copy image
diagnostics" will show the last stage entered, identifying the culprit. This is
a diagnostic-only change: it does not alter image generation.

Add unchecked host and phone regression entries, test, publish, verify both
live SHAs and re-freeze only after the harness passes.

Shipped in build `2026-11-20k`: `imageCheckpoint()` writes a small synchronous
localStorage record before every `imageStage()` call, every `imageFile()` cache
read, and at generate start / model release / image generated / image saved /
failure. "Copy image diagnostics" now includes "Last checkpoint: timestamp
[build] stage". Harness confirmed the checkpoint is written before a failing
stage and before each cache read, survives into the copied diagnostics, and
owner/guest/host plus all three live pages have zero console errors. Image
generation output is unchanged. Physical iPhone pass is open: reproduce the
flash, reopen the app, copy diagnostics and paste the last checkpoint.

## 2026-11-20 — Stream image model files instead of holding all 382 MB (published and verified)

Status: **published and verified** — final live SHA
`f4be9dee0fdcf5d228d9e0529abe42e36ad45468744e0a301a9801f1c7cc90f2`;
Pages commit `c804d7c`.

The stage diagnostics came back empty and the iPhone shows only a white flash
then returns to chat: no error handler runs, so iOS WebKit is terminating the
tab on memory pressure. The cause is `getImageFiles()`: it downloads all nine
model files (~382 MB) into a `Map` of `File` objects and keeps that map alive in
`imageRuntime` forever. Combined with the ~313 MB the U-Net session materialises
during `InferenceSession.create()` and the WebGPU buffers, a phone tab exceeds
its budget and is killed before any JavaScript error can be caught.

Planned changes:
1. Keep only the small support files (manifest + tokenizer, ~4 MB) in memory.
2. Read each model's `.onnx` and `.onnx.data` from Cache Storage on demand in
   `imageSession()`, so only the model currently in use is resident; release it
   as soon as the session is created. Each session is already released after
   its run, so peak memory drops from ~695 MB to roughly the U-Net's ~313 MB.
3. Add unchecked host and phone regression entries, harness-test the download,
   on-demand read and session lifecycle, publish, verify both live SHAs and
   re-freeze only after the harness passes.

Shipped in build `2026-11-20j`: `ensureImageFiles()` still downloads and verifies
every file into Cache Storage once, but keeps only the manifest and tokenizer
(~4 MB) in memory. `imageFile()` reads a single file from the device cache on
demand with a size check, and `imageSession()` now takes only the model name and
loads that model's graph/data pair. Each session is still released after its
run, so peak model memory falls from roughly 695 MB to the U-Net's ~313 MB.
Harness confirmed only the three small support files remain resident, the
correct model pair is loaded per session, a missing file reports a labelled
error, the full text-encoder → U-Net → decoder pipeline still produces a PNG,
and owner/guest/host visibility plus all three live pages have zero console
errors. Physical iPhone pass remains open in the phone checklist: this reduces
memory but cannot raise the device's hard ceiling if the U-Net alone is still
too large.

## 2026-11-20 — Label image failures by stage and keep them (published and verified)

Status: **published and verified** — final live SHA
`d40a643392fd18ce2768c6b6c623938d5fdc794fcf40f60751ce8336b3fad4e5`;
Pages commit `51b2ad1`.

The iPhone now reports `Image failed: I/O image generation failed`. That string
does not exist in the app, the demo bundle, onnxruntime-web JS/WASM or
transformers.js, so it is an opaque error from the browser's WebGPU/storage
layer. Without knowing which step throws, further fixes would be guesswork.
Planned changes:
1. Wrap each image step (runtime load, WebGPU check, each ONNX session load and
   run, PNG encode) with a stage label and the raw error name/message.
2. Save the last eight labelled image errors in localStorage and add a
   "Copy image diagnostics" command so a failure can be pasted even after the
   toast disappears.
3. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs and re-freeze only after the harness passes.

Shipped in build `2026-11-20i`: every image step runs through `imageStage()`,
which prefixes a failure with the stage name and the browser's raw error
name/message (for example `unet run: OperationError: I/O failure`). The last
eight labelled errors are saved in localStorage and a "Copy image diagnostics"
command (owner/static only) copies them with the build and update status. The
happy path is unchanged. Harness confirmed stage labelling, persistence, a
successful generation with the error log intact, owner/guest/host visibility and
zero console errors on all three live pages. The physical iPhone pass is open:
the user needs to paste the labelled error so the failing step can be fixed
directly.

## 2026-11-20 — Stop mid-generation reloads and model memory pile-up (published and verified)

Status: **published and verified** — final live SHA
`e52b1b96709471fe52255dcca65dd96495eee88bc5ff73a7be776ee2a112871d`;
Pages commit `684f6b0`.

User reports from the iPhone: chat replies sometimes show `Model error:` after a
few conversations, and image generation flashes a white screen then errors out.
No bridge or server errors exist (both bridge logs are empty). Two client-side
causes were found in the code:

1. The auto-update watcher calls `location.reload()` on `load`, `pageshow`,
   `focus` and `visibilitychange`. On a phone those events fire constantly
   (screen unlock, app switch, keyboard). If a build change or a waiting service
   worker is detected while an image is generating or a chat reply is pending,
   the page reloads mid-flight — a white flash and the lost result. Planned:
   defer the reload while `imageBusy` or `waiting` is true, retry when idle.
2. `devicePipes` keeps every loaded model resident. With Tiny (105 MB), Balanced
   (229 MB) and the new Unfiltered (219 MB) all selectable, switching models in
   one session can hold about 553 MB in a phone tab with a ~400 MB ceiling.
   Planned: when loading a model, exit and drop every *other* pipe first, so only
   one chat model is ever resident. The weights stay in OPFS and reload silently.

3. Add unchecked host and phone regression entries, harness-test, publish,
   verify both live SHAs and re-freeze only after tests pass.

Shipped in build `2026-11-20h`: `reloadOnce()` now checks `imageBusy`/`waiting`
and defers any build or service-worker reload by five seconds while work is in
flight, instead of reloading immediately. `releaseOtherDevicePipes(keepId)`
exits every other wllama pipe before a new model loads, so only one chat model
is resident; `releaseDevicePipes()` now reuses it. Harness confirmed the reload
is suppressed for the whole busy window and fires once idle, the correct pipe
is kept while the others are exited, the image harness still produces a result
and saves it before the blob write, and owner/guest/host visibility plus all
three live pages report zero console errors. Physical iPhone pass remains open
in the phone checklist. The exact `Model error:` text was not supplied, so a
targeted follow-up may still be needed if a different cause (timeout or context
overflow) is behind the chat errors.

## 2026-11-20 — Add an unfiltered on-device model (published and verified)

Status: **published and verified** — final live SHA
`38964394205008c49d4d49559669aa53990c3e5c6280697f3efd8b3ef60d8ff8`;
Pages commit `9181984`.

Requested after finding no preferred uncensored model on a phone-friendly
budget. Researched Hugging Face for low-refusal GGUFs small enough for the phone
tab. Chosen: **LFM2.5-350M-abliterated** in GGUF
(`mradermacher/LFM2.5-350M-abliterated-GGUF`,
`LFM2.5-350M-abliterated.Q4_K_M.gguf`, 229,312,736 bytes / about 219 MiB). This
is an abliterated finetune of the **same** LiquidAI 350M already offered, so it
uses the same `lfm2` architecture, chat template and wllama runtime, and the same
phone memory budget. Direct resolve URL returns HTTP 200 with CORS `*`.
Planned changes:
1. Add it as a third static/owner-only model option "Unfiltered on-device · 350M".
2. Keep guest sessions and the Mac host build unchanged; no bridge call.
3. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs and re-freeze only after the harness passes.

Shipped in build `2026-11-20g`: the static/owner selector gains a third option
"Unfiltered on-device · 350M" (`device-free` → `lfm2-350m-free`). It is gated to
`staticMode && !guestMode`, so guests still see only Tiny and Balanced and the
Mac host build is untouched. `activeDeviceModel()` now resolves every on-device
backend (including custom models) through `ggufSpec`, and the send path uses it,
so selecting the new model loads the abliterated GGUF from Hugging Face once and
caches it in OPFS exactly like the existing 350M. Harness confirmed: owner sees
three models, guest sees two, host sees none; `device-free` resolves to the
correct repo/file and the model id reaching `deviceChat` is `lfm2-350m-free`;
zero console errors on owner/guest and all three live pages. Physical iPhone
pass remains open in the phone checklist.

## 2026-11-20 — Free the chat model before image generation (published and verified)

Status: **published and verified** — final live SHA
`ac235e94e7788ce8e1e47769d6e4a5ca83bf1f43c4bef78f73b4a806bb819fa2`;
Pages commit `9c044db`.

On the phone, selecting an on-device chat model keeps its wllama/WASM weights
(up to 229 MB) resident. Generating an image then also loads 382 MB into WebGPU.
On iOS that combined footprint can kill the tab, which shows as a jump back to
the chat list or a black screen when the progress bar finishes. Planned changes:
1. Release every loaded wllama pipe before image generation starts. The GGUF
   weights stay in OPFS, so the chat model reloads silently on the next message.
2. Detect an all-black generated image and report a clear retry message instead
   of attaching a blank picture.
3. Make the result modal and chat message robust to an IndexedDB failure so the
   generated image is never hidden by a storage error.
4. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs and re-freeze only after the harness passes.

Shipped in build `2026-11-20f`: `releaseDevicePipes()` exits every loaded wllama
worker before WebGPU starts, so the chat model no longer competes with the 382 MB
image model for the phone's memory. The GGUF weights stay in OPFS and reload
silently on the next chat message. The decoder now computes mean/standard
deviation of the decoded pixels; a flat black result raises a clear retry
message instead of attaching a blank image. The harness confirmed the release
runs before generation, a blank result shows the error with no chat message and
no console errors, and host/guest visibility is unchanged. Both live sites serve
the final app SHA with build `2026-11-20f`. Physical iPhone pass remains open in
the phone checklist.

## 2026-11-20 — Keep the generated image in view after a phone reload (published and verified)

Status: **published and verified** — final live SHA
`5a4a836b800a944e34abb170a92fdb42aac03f1bcd59c8b3d2e573139676a663`;
Pages commit `889415d`.

On a physical phone the tab can reload after image generation (WebGPU memory or
a normal app foreground restart). The image is already saved, but the app starts
on the chat list because the mobile screen is not persisted. Planned changes:
1. Remember the last mobile screen (`chat` vs list) in localStorage.
2. Add the image chat message and save the transcript before the slower
   IndexedDB blob write, so a reload cannot lose the result entirely.
3. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs and re-freeze only after the harness passes.

Shipped: the mobile screen is now stored in localStorage, so a reload returns to
the chat with the generated image instead of the chat list. The image message is
also saved to the transcript before the slower IndexedDB blob write. The harness
verified the save-before-store order, reload back into the chat, hydrated image,
working download/copy controls, unchanged host/guest hiding and zero console
errors. Both live sites serve build `2026-11-20e` with the final SHA. The physical
iPhone reload pass remains open in the phone checklist.

## 2026-11-20 — Retry control for long-chat model errors (planned before edits)

Status: **published and verified** — final live SHA
`1755f6963f5f3ccd20eeb0fd5a38e2a03ab1f182c7fe3802152808ee1d03ea3e`;
Pages commit `56a3481`.

After the buffer-length fix, a genuinely over-long chat still ends with
"This chat is too long for the private model… then tap retry", but no retry
control exists — the only escape is a new chat. Planned changes:
1. Mark model-error bot replies as retryable and show a **Retry with short
   history** button on them.
2. Make the retry re-send the preceding question with only that question and a
   short tone instruction, without deleting the chat.
3. Keep the same rule for the "device took too long" message, which also says
   "tap retry".
4. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs, then re-freeze the baseline.

Shipped: model-error replies now carry a **Retry with short history** button on
the last message only. Tapping it removes the error reply, restores the previous
question and re-sends it through the tightest device path (short tone + newest
question), keeping the chat intact. Host/bridge errors are not marked retryable.
The phone harness reproduced four buffer-length failures, showed the button,
then answered on the retry using only the short prompt; normal replies and
non-overflow errors are unchanged. Host, Cloudflare Pages and GitHub Pages all
load build `2026-11-20c` with zero console errors; SW and manifest SHAs are
unchanged. On the physical iPhone the retry control was not needed: automatic
short-history retries handled the long chat, so the button correctly stayed
hidden. That specific manual-button path therefore remains unverified on device
and is noted as such in the phone checklist.

## 2026-11-20 — Phone-side image generation (published and verified)

Status: **published and verified** — final live SHA
`5a4a836b800a944e34abb170a92fdb42aac03f1bcd59c8b3d2e573139676a663`;
Pages commit `889415d` (includes the phone-reload fix above). Service worker SHA
`6a84bda96dbf89e0c87de494a536e64e8aa7b711c95bc3517254caeebdde0c35`.

Requested for social-media posts. Requirements captured from the user:
1. Generate on the **phone later** (not the Mac host, no cloud API key).
2. Offer all common social sizes (1:1, 4:5, 9:16, 16:9) as inputs and let the
   model choose the right one for the job.
3. Show **download/copy** controls and also attach the image to the chat message
   so it can be exported with the transcript.
4. Keep it device-local, guest-safe and offline-first, with separate host/phone
   regression entries before any implementation.
5. Pick a model that genuinely runs inside iOS Safari / Home Screen (no cloud,
   no host bridge), then test, publish, verify live SHAs and re-freeze only after
   the harness passes.

Model: **NanoDiffuser** (`utkucoban/NanoDiffuser`, one-step SDXS, pinned revision
`14cff72356365c3586ee38a2237332525889b69c`). It is 382 MiB of ONNX assets,
CLIP + one U-Net step + a tiny decoder, WebGPU with float16, and no cloud call.
The files are downloaded once from Hugging Face into the app's own
`oracle-image-v1` Cache Storage, reused offline, and deliberately preserved by
the service worker across shell updates. Generated PNGs are kept in IndexedDB,
not localStorage, so a long chat stays small.

Shipped in the working file:
- Static/owner-only image button, command-palette entry and model-menu status.
  Hidden on the Mac host and in every guest session; no bridge endpoint, key or
  credential is involved.
- One-time phone download confirmation, live progress bar, WebGPU/float16
  check, and offline reuse without a second download.
- Smart size picks by CLIP (1:1, 4:5, 9:16, 16:9), plus manual size buttons.
- Download/copy controls in the result modal and on the attached chat image.
  The transcript shows an image reference, never image bytes.
- Service worker caches the ONNX Runtime / tokenizer helpers while excluding the
  large model files, and preserves `oracle-image-v1` during activation.

Harness results: static owner showed the image controls; host and guest showed
none. A fake-runtime pass covered download progress, CLIP size choice (`9:16`),
512×512 generation, crop to 288×512, PNG attachment, IndexedDB reuse after
reload, download/copy handlers, zero console errors, and unchanged chat state.
A real WebGPU pass on the Mac loaded the pinned model, produced a non-black
512×512 PNG, and chose `9:16` for a story prompt and `16:9` for a banner prompt.
A cache test confirmed the service worker keeps the image model cache. Physical
iPhone/Home Screen verification remains unchecked in the phone checklist.

Published and verified build `2026-11-20d`: Cloudflare Pages and GitHub Pages
both serve the final app and SW SHAs with zero console errors, active service
workers, image controls for the static owner and no image controls for guests.
The Mac host/bridge build stays hidden and answered a live smoke-test message
with `OK.` and no console errors. Baseline and rollback script were re-frozen
to the final SHA.

## 2026-11-20 — Phone long-chat model error (planned before edits)

Status: **published and verified** — final live SHA
`82611435769be2e280cb0b45c7efc6d52b86c11486082f4c770e31bf991c9419`;
Pages commit `a1e8d44`.

On the phone, after a chat grows, the Balanced · 350M on-device model can reply
`Model error: length out of range buffer`. The existing context-overflow retry
only matches wording like "context size" / "too many tokens", so this buffer-
length error skips the short-history fallbacks and reaches the user raw.
Planned changes:
1. Recognize the buffer/length error as a context overflow in `deviceChat`.
2. Add a tighter final retry (short system tone + newest question only) so a
   long chat can still answer instead of failing.
3. Leave host, guest, saved-model, progress-bar and update behaviour unchanged.
4. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs, then re-freeze the baseline.

Shipped: overflow detection now also treats iOS wllama's "length out of range
buffer" as a context overflow, and `fitDeviceMessages` accepts a smaller budget
and system limit. `deviceChat` adds a fourth, tightest retry (short tone plus
newest question only). The phone harness reproduced three buffer-length
failures followed by a successful fourth attempt through the real send flow;
normal one-shot answers and non-overflow errors are unchanged. Host app, static
site and published build marker verified with zero console errors. Cloudflare
Pages and GitHub Pages both served the final app SHA; SW and manifest SHAs are
unchanged. Physical iPhone confirmation: the user ran a 15–25 turn chat and a
very large prompt on the installed Home Screen app; both answered normally with
no raw buffer error and no manual retry needed, so this pass is now closed in the
phone checklist.

## 2026-11-20 — About + update status screen

Status: **published and verified** — final live SHA
`df0f54ba4a769e90b407aed17870efe76625640bf263b13ab595cee8345fe736`;
Pages commit `693eae6`.

Installed Home Screen apps have no visible version or update state, which makes
verification and support needlessly hard. Planned changes:
1. Add an **About / Update status** item to Profile and the command palette.
2. Show the build marker, service-worker state/cache version, saved-model state,
   and the current backend. On static builds also expose a **Check for updates**
   button tied to the existing update routine.
3. Keep all of it device-local: no host credentials, tools, routines or chat
   content are shown, and the manual check is static-only.
4. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs, then re-freeze the baseline.

Shipped: Profile and command-palette entry, local-only rows for build/mode/
model/private-model/SW/cache/update state, static-only manual check, and update
result reporting to the About screen. Harness tests covered host, static,
guest, light/dark, and the reload cap with a preserved draft; zero console
errors. Cloudflare Pages and GitHub Pages both served the final app SHA with
the unchanged SW/manifest SHAs. Real iPhone storage/theme/network checks are
still listed as open in the phone checklist.

## 2026-11-20 — Camera vision (planned, phased — building host phase now)

Status: **host phase published and verified** — final live SHA
`df0f54ba4a769e90b407aed17870efe76625640bf263b13ab595cee8345fe736`;
Pages commit `693eae6`. Phone photo-Q&A remains planned.

Following Grok's camera-in-voice feature, the chosen roadmap is:
1. Host-only "See this" first: webcam/still frame → local Ollama vision model
   through the Mac bridge. Private, reliable, owner-only; needs a one-time model
   pull and small bridge changes.
2. Then an opt-in phone photo-Q&A prototype using SmolVLM2 via WebGPU. True
   offline vision, but a large download and real iPhone testing before stable.
3. No continuous live video in the iOS Home Screen app: WebKit permission
   resets and tab kills make it a poor experience.
4. Host phase must deny guest tokens at the bridge, hide the button entirely on
   static/phone builds, and never echo images or credentials into chat history.

Shipped (host phase): pulled `qwen2.5vl:3b` once on the Mac, added
`/api/vision` with guest-token denial, added the owner-only "See this" button
and command, and used a one-frame capture with no image data in chat history.
Verified with a synthetic webcam stream and a real local vision answer; the
physical webcam permission prompt is still a real-Mac check. The button,
command and permission request are absent on static/phone and for guests.

## 2026-11-20 — Guest status hardening (bridge-only)

Status: **verified locally** — no app SHA change; `oracle_bridge.py` only.

The guest response from `/api/status` still included the owner's host tool-scope
list even though guests cannot use those tools. Guest responses now expose only
`"mode": "guest — chat only"`; owner responses keep the full mode and scope.
Verified with owner and valid guest-token requests after a bridge restart.

## 2026-11-19 — Hero personality presets

Status: **published and verified** — final live SHA
`00fb27e17790a9e2ed0cec72a8e1acb9ad6a25739fe66b6a56cae983c3abb886`;
Pages commit `01e1c99`.

Grok's chat personalities and voice personas are one of its most visible wins.
Planned changes:
1. Add local, per-chat personality presets (Oracle, Concise, Tutor, Formal,
   Playful, Kids, Coach) as short system instructions — no cloud, no new model.
2. Pick a personality from a new "Personality" item in the chat More menu, or
   while creating/editing a bot in the Bot roster.
3. Send the selected instruction as a `system` message to device, custom-cloud
   and bridge backends; teach the bridge to fold it into its system prompt
   without exposing it as chat history.
4. Keep it per-chat and device-local, including for guests; never send a
   credential value with it.
5. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs, then re-freeze the baseline.

## 2026-11-19 — Automatic updates for Home Screen apps

Status: **published and verified** — final live SHA
`00fb27e17790a9e2ed0cec72a8e1acb9ad6a25739fe66b6a56cae983c3abb886`;
Pages commit `01e1c99`.

An installed (Add to Home Screen) app resumes instead of navigating, so it keeps
running the old shell after a publish until iOS happens to relaunch it. Planned
changes:
1. Keep the one-time registration, but also actively check for a new service
   worker on load and whenever the app returns to the foreground
   (`pageshow` / `focus` / `visibilitychange`), with a short throttle.
2. When a new worker finishes installing, tell it to take over and reload the
   page exactly once so the fresh HTML/JS is used. Guard against first-install
   and repeat reloads so it can never loop.
3. Preserve an in-progress typed message across that one reload.
4. Add a `SKIP_WAITING` message handler in the SW and bump the cache to v6.
5. Add unchecked host and phone regression entries, test, publish, verify both
   live SHAs, then re-freeze the baseline.

### Release verification for auto-update + personality presets

- Final live app SHA: `00fb27e17790a9e2ed0cec72a8e1acb9ad6a25739fe66b6a56cae983c3abb886`
- Service worker SHA: `5a29f860200a736610c8e002cc49778a74be12f7a02bfd0a61326303b1d15b91` (`oracle-chat-v6`)
- Manifest SHA: `9750fc8b3135ade31891825be44c4f8e9e51166c1c9b5ebd9c8f420bbf0e66a3`
- Pages commit: `01e1c99`
- Verified on both `https://oracle-chat.pages.dev/` and the GitHub Pages backup:
  app, SW and manifest SHAs match the local publish copies.
- Host: bridge chat followed Concise vs Tutor, roster create/edit saved the
  per-chat tone, default tone unchanged, system text absent from visible
  history, light/dark and zero console errors.
- Static/phone: picker works at 390 px, tone reaches device and custom-cloud
  backends as a system message, context fitting keeps it on every overflow
  retry, per-chat/guest persistence works, host tools stay hidden, update reload
  preserves a typed draft and stops at the guard, zero harness console errors.
- Blocked-network cold reload, real installed Home Screen auto-update, real
  iPhone camera/mic and hands-free multi-turn remain on the real-device list.

## 2026-11-19 — Model download progress bar

Status: **published and verified** — final live SHA
`0c92d8d4e034fc72a75b2f6c1159a835f7d0140ce6fb556bc05017b9bddece3b`;
Pages commit `3c1f74b`.

The first-save status already receives a real percentage from wllama's
`progressCallback`; it was only shown as text. Changes made:
1. Added a slim progress track under the model status bar in the composer.
2. Fed the callback percentage into its width and ARIA value.
3. Kept the bar hidden for "Loading saved model from this device" and during
   normal chat, so it only appears while bytes are being saved.
4. Added host and phone regression entries, tested, published, verified both
   live SHAs, then re-froze the baseline.

### Release verification for this three-part update

- Final live app SHA: `0c92d8d4e034fc72a75b2f6c1159a835f7d0140ce6fb556bc05017b9bddece3b`
- Service worker SHA: `db4118faaf4f27b8485415b5371a34354675ffb969ce1b3889051083bfe77e30` (`oracle-chat-v5`)
- Manifest SHA: `9750fc8b3135ade31891825be44c4f8e9e51166c1c9b5ebd9c8f420bbf0e66a3`
- Pages commits: `711ca6f` (theme + device-save fix), `3c1f74b` (progress bar)
- Verified on both `https://oracle-chat.pages.dev/` and the GitHub Pages backup:
  app, SW and manifest SHAs match the local publish copies.
- Host: bridge chat, theme toggle persistence, dark/light rendering, zero console errors.
- Static/phone: first-save progress 0% → 22% with matching bar width/ARIA,
  bar survives a mid-load render, hidden on completion and on saved-model reuse,
  saved-model send replies correctly, host tools hidden for guests, zero console
  errors. Real-device blocked-network and installed-app checks remain open on
  the phone checklist.
- Frozen offline mockup unchanged: `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Light + dark visual refresh

Status: **published and verified** — shipped with the same final release
(`0c92d8d4…`, Pages commits `711ca6f` + `3c1f74b`).

The user reported the installed app looked old school and chose the light +
dark theme direction. Planned changes:
1. Add system-aware light/dark themes with a manual override stored locally.
2. Modernize typography, spacing, rounded surfaces, shadows, composer, pills,
   menus, and modals using theme tokens.
3. Preserve the required 20px hero sprites and hero colour coding, folder
   sidebar, mic/call buttons, back navigation, and guest isolation.
4. Keep status-bar/meta theme colour in sync with the active theme.
5. Add unchecked host and phone regression entries, then test host/static/guest
   before publishing.

## 2026-11-19 — Persistent on-device model storage

Status: **published and verified** — app and SW SHAs re-frozen after tests
passed; see the release verification block above.

The user asked for the private/local model to be saved on the device instead of
being downloaded again each time. Diagnosis: wllama 3.6.1 already persists GGUF
weights in OPFS, but our app checked the wrong store (Cache API), showed a
"first time only" message on every load, and called `loadModelFromHF()`, which
hits the Hugging Face repo API before it can use the saved copy. The service
worker also cached the full GGUF a second time, and iOS Home Screen apps keep a
separate storage container from Safari.

Planned changes:
1. Load via `w.loadModelFromUrl({url})` with the direct resolve URL so a saved
   model opens from OPFS with no HF API call and works offline. Fall back to
   `loadModelFromHF()` only if that API is unavailable.
2. Check wllama's own `cacheManager.list()` for the exact saved URL, set a
   per-model saved flag after a successful load, and only ask for the first
   download when the weights are genuinely absent.
3. Show real `progressCallback` percentages while saving, and "Loading saved
   model from this device" when reusing it.
4. Stop the service worker from caching Hugging Face/GGUF responses (wllama
   owns those files); bump the cache to v5 so the duplicate v4 copy is removed.
5. Explain the iOS Safari vs installed-app storage split in the download and
   install dialogs.
6. Regression entries on both lists, host + static tests, publish, verify both
   live app/SW SHAs, then re-freeze the baseline.

## 2026-11-19 — Grokbot-style control layer

Status: **published and verified** — new live SHA
`77a4a8f8180d15a7eda015d94d98adee52b3c4a899835ace74642d9f89f697bf`;
Pages commit `6005abc`. Previous live SHA was `057400bf…`.

Delivery note: this release covers both targets in one build — the same
`Oracle-Chat-Live.html` is served locally by the bridge (host website) and
copied to Pages (phone/static web app), with host-only features hidden when
`staticMode` or `guestMode` is true.

After the Grokbot research, the user chose the local “control layer” first. It
copies the useful UI pattern (named bots, visible approvals, routine controls,
fast search) without trying to copy Grokbot’s paid cloud computer.

Planned changes to `Oracle-Chat-Live.html`:
1. Bot roster: each chat gets a job label and a primary badge; Profile → **Bot
   roster** and the new-room modal can set them. No shared/cloud state.
2. Approval cards: risk chips plus **Allow once / Always allow / Deny**.
   “Always allow” stores an exact-action rule on the host only and is removable;
   guests and the static build never see it. The bridge is not changed.
3. My Routines: add **Test** (dry-run preview that executes nothing) and a
   redacted run history for each routine.
4. Command palette: `Ctrl/Cmd+K` (and a menu item for phones) searches chats,
   folders, routines and commands.
5. Installable web-app shell: link a manifest with real icons, add standalone
   meta tags, cache the shell assets in the service worker, and add Profile →
   **Install this web app** with Add-to-Home-Screen guidance where Chrome's
   install prompt is unavailable (notably iOS Safari).
6. Regression entries on both lists, host + static tests, publish, verify both
   live SHAs, then re-freeze the baseline.

Verification completed before publishing:
- Static/phone harness (`staticMode`, `PHONE`, stub wllama): roster with job +
  PRIMARY badge, `Ctrl/Cmd+K` palette, Test dry-run (no history write, no steps
  executed), real run recording redacted history, Manifest + icons + theme
  colour, SW v4 cache list, zero console errors.
- Guest share link: isolated routine key `oracle.routines.guestC`, zero routines,
  no host rule menu, no host Web Routines, zero console errors.
- Host website on `127.0.0.1:8765`: risk chips, Allow once / Always allow /
  Deny, exact-match rule auto-approval, changed target requires new approval,
  rule removal, command palette, roster with job/primary, zero console errors.
- Both live sites verified: app SHA, service-worker SHA, manifest SHA and all
  three icon assets match the local publish copies. The frozen
  `Oracle-Chat-Offline.html` mockup was not touched (SHA `320603d7…`).

## 2026-11-19 — On-device context overflow fix

Status: **published and verified** — new live SHA
`057400bf2d890c5e009ebea7da66d20fe2dee7f2f32a7001217eba7683248846`;
Pages commit `6ec577f`. Previous live SHA was `cadd95ed…`.

User hit: `request 1051 tokens exceeds the available context size 1024 try
increasing it`. This comes from the phone's wllama runtime: the model is loaded
with `n_ctx: 1024`, and `deviceChat()` passes every stored chat message plus the
long routine-authoring prompt with no token budgeting.

Planned changes to `Oracle-Chat-Live.html`:
1. Raise the on-device context window from 1024 to 2048 tokens.
2. Add a conservative message-history fit function (recent messages first,
   bounded character budget) so long chats cannot overflow the window.
3. On a context-overflow error, retry once with only the last exchange and then
   once with only the last message; give a clear retry/new-chat message if it
   still fails.
4. Cap the routine-authoring allowlist included in the prompt.
5. Add regression entries, test with a stub runtime that reproduces the error,
   publish, verify both live SHAs, then re-freeze the baseline.

Verified with a local static harness whose stub runtime throws the exact
`request 1051 tokens exceeds the available context size 1024` error above a
4200-character prompt. The model now loads with `n_ctx: 2048`; a 20-turn history
first sent 4483 characters, triggered the stub overflow, then automatically
retried with the last exchange (649 characters) and succeeded; a single
6000-character message produced the clear "too long" error after three bounded
attempts; AI routine authoring kept 15 configured endpoints down to the first 10
in the prompt. Hosted Cloudflare and GitHub builds match the new SHA, and the
live static build reports zero console errors. The bridge was not changed.

## 2026-11-19 — Device-local routines + model re-prompt fix

Status: **published and verified** — new live SHA
`cadd95edd11c2b5d2d8dbd8d5a08df32a3ea016f793a8c814fc9f381d8df5524`;
Pages commit `fc0eee8`. Original offline mockup SHA unchanged.

User chose "device-local first" for self-authoring routines on the phone/web
build, and reported a bug: the app asks to re-download the model on every
refresh / new chat. Investigation showed the cached GGUF is served locally
(`transferSize: 0`, ~0.5 s load) — the bytes are NOT re-downloaded. The real
cause is `deviceOk` being an in-memory flag reset on every page load, so the
first-download confirmation modal reappears.

Planned changes to `Oracle-Chat-Live.html`:
1. Fix: persist the download acknowledgement in localStorage and check the
   actual Cache API for cached GGUF bytes before showing the confirmation, so
   the prompt only appears on a genuine first download.
2. Add a device-local routine engine to the static/phone build only:
   - "My Routines" in the profile menu, stored per-session on the device
   - strict whitelist of steps (fetch to owner-approved hosts, model, say,
     notify, share, wait, log); model output is never eval'd
   - `{{cred:NAME}}` resolved from the device-local encrypted vault at run time
     and redacted; `{{var:NAME}}` carries step outputs
   - AI authoring: the on-device model writes routine JSON from a plain-language
     description, then the owner reviews and approves before it can run
   - manual / hourly / daily-at-08:00 triggers selected in the UI; they run only
     while the page is open, and a daily trigger fires once per calendar day
   - guests and shared chats get their own blank routine set; no host access
3. Regression entries on both lists; publish, verify both live SHAs, then
   re-freeze the baseline.

Verified in a local static harness with a stub wllama module: cached GGUF bytes
load with no prompt; a genuine first download still prompts; the acknowledgement
survives reload; AI drafting → review → approve → run works; unapproved fetch
hosts are rejected; vault secrets are redacted; `{{var:NAME}}` carries a fetched
result; daily trigger does not re-fire; a second share token gets blank routines.
Hosted smoke test on Cloudflare Pages showed zero console errors, My Routines
opening, and no host Web Routines menu. Bridge `/api/status` remains healthy and
unchanged (local 3B ok, deep 4B ok, Keychain vault ok, tool mode `auto`).

## 2026-11-19 — Full feature + UI audit (no app code changed)

Status: **audit only — app SHA unchanged** (`a0215899…`)

User asked whether everything was fixed and requested a full pass over all
features and UI. Ran end-to-end checks on the host build, the bridge APIs, and
the phone/static build. No application code was changed; the only edits were
to the two regression checklists (added audit sections, corrected a stale
baseline SHA that still read `6a0e7e0f…`) and this changelog.

Key results: bridge healthy; all six SHAs match; zero console errors; real local
send works; all menus/modals present; vault/skill/tool-mode flows work; valid
guest tokens are isolated (403 on routines/vault/memory/tool execution); phone
build shows only device models, hides Web Routines, has no layout overflow at
390px, and produced a real on-device reply via wllama with the model cached for
offline. Audit artifacts (test chat/credential/skill/guest session) removed and
state restored (9 skills, tool mode `auto`).

Not fixable here / still open: Big Pickle free cloud quota; real email/social
account setup needs the user's credentials; the 135M phone model is weak (use
the 350M "Balanced" model); phone background browser automation needs a native
app/Shortcuts; frozen office state untouched pending approval.

## 2026-11-19 — Baseline (frozen)

**File:** `baseline/Oracle-Chat-Offline.html`
**SHA-256:** `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`

Initial layout matched to Grokbot screenshot. Features:
- Two-column layout: sidebar (conversations) + chat area
- 13 demo conversations, clickable
- Message send with fake bot reply
- `+` menu: Attach a file (file picker + chips), Teach a Skill (modal + storage)
- Model selector dropdown (label only — not a real model)
- Fully offline single file

Known limitation: replies are fake; model selector changes only a label. This
is the state before connecting a real backend.

---

## 2026-11-19 — Real answers: local model + OpenCode cloud bridge + vault

Status: **implemented, verified; baseline NOT re-frozen yet**

What changed:
- Added `oracle_bridge.py`: local-only Python bridge (127.0.0.1:8765, stdlib
  only) that serves the UI and proxies chat messages to:
  - **local**: Ollama `qwen2.5:3b` (1.9 GB, fits 8 GB MacBook Air, works offline)
  - **cloud**: OpenCode free models via the bundled desktop CLI (`opencode-cli`,
    `opencode/big-pickle`), with automatic fallback to local on 429 free-limit.
- Added `Oracle-Chat-Live.html`: same Grokbot layout, now with real replies,
  working model selector (Local / Cloud→Local / Big Pickle), vault panel,
  `+` menu (Attach a file, Use a saved login, Teach a Skill).
- Credential vault uses **macOS Keychain** (`oracle-vault:*` service names).
  Only credential *names* go to the model; `[[USE:key|url]]` markers are
  resolved server-side by the bridge. Values are never returned in chat.
- Desktop relaunch folder: `~/Desktop/Oracle Chat/` with Launch/Stop `.command`
  scripts and README, so the window can be reopened after a restart.
- Default model switched to **local** while the free OpenCode quota is
  exhausted (HTTP 429, ~3 hour reset); cloud options remain selectable.

Files touched (baseline untouched):
- New: `oracle_bridge.py`, `Oracle-Chat-Live.html`
- New: `~/Desktop/Oracle Chat/*`
- Not changed: `Oracle-Chat-Offline.html`, `Regression Check/baseline/*`

Test result:
- `curl /api/status`: local ok, cloud configured, vault ok — PASS
- `/api/chat` backend=local → `BRIDGE_LOCAL_OK` — PASS
- `/api/chat` backend=auto → `BRIDGE_AUTO_OK`, note "Cloud free quota is
  exhausted; used local model." — PASS
- Browser: UI rendered, model pill shows "Qwen 2.5 3B (local)", sent a real
  message, got a real local answer, zero console errors — PASS
- Keychain set/read/delete probe — PASS
- Free cloud models (Big Pickle, tidepool-alpha-free): HTTP 429 free usage
  limit — external/account issue, not a code failure.

Still to do before re-freezing: full README regression checklist after cloud
quota resets and a cloud answer is verified.

## 2026-11-19 — Sidebar cleanup: vault behind profile, editable name

Status: **implemented, verified; baseline NOT re-frozen yet**

- Removed the top-level "Credential Vault" nav item; it is now in the menu
  opened by clicking the profile row at the bottom of the sidebar.
- Profile row is clickable; menu offers **Credential Vault** and
  **Change display name**. Name is saved in browser localStorage
  (`oracle.displayName`) and the avatar initials update with it.
- Removed the unexplained `87` badge from the profile row.
- File touched: `Oracle-Chat-Live.html` only (baseline untouched).
- Browser test: profile menu opens, vault entry opens vault, name change
  persists, no `87` badge, zero console errors — PASS.

## 2026-11-19 — Organization, agents, sharing, voice, auto-start, memory

Status: **implemented; baseline NOT re-frozen yet — full checklist in progress**

### Folders & agents
- Sidebar: CHATS / FOLDERS toggle, multiple folders, click to open, drag a chat
  onto a folder, folder rename/delete, new folder inline when creating a room.
- 20 selectable CSS pixel-sprite Marvel heroes when creating/naming a room,
  shown beside the room title and in the chat list. Each hero has a color that
  color-codes the chat (sidebar stripe, avatar border, bot bubbles). Raise-hand
  when help/approval is needed, walking while working.
- Header three-dot menu by Share now works: New chat room, New folder, Tools
  mode, Voice replies, Smart name/folder/summary, Share/export. Same smart
  actions also in the per-chat menu.
- Share button copies transcript or downloads .txt.

### Local tool permissions
- Tools now default to **auto**: the local model runs sandboxed read/write/shell/
  fetch without an approval prompt. Toggle to **ask** in the header menu keeps
  read-only + ask-first. Guests never get tools.
- Hardened blocked-shell list (secrets, keychain, traversal, destructive cmds).
- Fixed a bug where the model's `TOOL:` call was shown as chat text: the parser
  now finds multi-line JSON, inline calls and code fences, and strips them.

### Voice
- Mic button: voice-to-text (Web Speech API).
- Volume button: spoken replies with a Jarvis-style voice when the device has
  one (Daniel/Oliver/George/Google UK English Male).
- Phone button: hands-free **live call** loop — listen → auto-send → speak reply
  → listen again, using the fast local model. Chrome/Android Chrome fully
  supported; iPhone Safari speaks replies but has limited recognition.

### Sharing (family)
- Tokenized links; guests get their OWN blank workspace — never your folders,
  other chats, or vault. Share one chat, or Share folder from the folder menu.
  Guest sessions cannot create links, use the vault, change tools, or run tools.
- Same Wi‑Fi only; a secure tunnel is still needed for family off-network.
- Android/phone guests keep secrets in their own browser storage; the host
  Keychain is never exposed to guests.

### Auto-start
- Ollama starts via its Homebrew login service.
- Bridge managed by LaunchAgent `com.oracle.chat.bridge` (RunAtLoad + KeepAlive),
  logs at `/opt/homebrew/var/log/oracle-chat.log` (TCC blocks ~/Documents for
  launchd). Verified: kill the process → launchd restarts it automatically.
- Desktop Launch/Stop scripts updated to cooperate with the LaunchAgent.

### Memory & knowledge
- New `oracle-knowledge/` folder with notes on the app, features, decisions,
  office constraints and regression rules. `oracle-skills.json` seeds skills.
- The bridge recalls relevant notes into the model prompt per question; verified
  the model returned the exact frozen baseline SHA-256 from recall.
- Memory tool lets the model save/recall facts; Memory panel in profile menu;
  `/api/memory` GET/POST endpoints. Guest sessions have no memory access.

Files touched: `Oracle-Chat-Live.html`, `oracle_bridge.py`, new `oracle-knowledge/*`,
new `oracle-skills.json`, new LaunchAgent, Desktop launcher scripts.
Baseline and frozen mockup untouched.

Tests so far: parser unit test (3 formats) PASS; memory endpoints + recall PASS;
model recalled exact baseline hash PASS; browser memory panel PASS; browser tool
call with no leaked `TOOL:` text PASS; zero console errors PASS; launchd
KeepAlive restart PASS; verified voice call loop with simulated mic PASS.

### Device-local inference + guest vault (added before final re-freeze)
- Shared links now offer **This device (private)** backend (default for guests):
  loads Qwen2.5-0.5B via transformers.js from CDN, runs on the guest's own
  WebGPU/WASM. Verified: guest browser downloaded the model and answered
  "Say hello in one word." entirely on-device, no bridge call for inference.
- Guests get an **encrypted device-local vault** (AES-GCM, key kept in their
  browser). Only credential names reach the model; values never leave the
  device. Verified: value encrypted at rest, zero console errors.
- Guest sessions hide host-only vault/memory/tool items; no 403 calls.
- Guest token 403 on vault list fixed.

### Re-frozen after all tests passed
- New active live baseline: `baseline/Oracle-Chat-Live.html`
- SHA-256: `f0783f4dee937a165b4c860ede0d4121f864699a3637c5b9c4a1dac5dd0f8460`
- Roll back with `restore-live.command`.
- Original offline mockup baseline unchanged at
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — GitHub Pages, custom models, call audio & voice presets

Status: **implemented, browser-verified; baseline re-frozen; site published**

### Published site (no dependency on the Mac)
- Repo: `tuxedotigercomics-gif/oracle-chat` (public).
- GitHub Pages: `https://tuxedotigercomics-gif.github.io/oracle-chat/`
  (verified HTTP 200). Static single-file build in `oracle-pages/index.html`.
- Static-host detection: on a non-loopback host only the device backend is
  shown; bridge-only menus (tools, smart actions, host vault/memory, skills)
  are hidden. Zero console errors.
- Share links are now self-contained: the shared chat/folder JSON is
  base64url-encoded in the URL fragment (`#s=…`). The fragment is never sent to
  GitHub, and the recipient needs no Mac, bridge, or server. Verified: a shared
  chat opened on a pure static server with messages intact.
- Important: Big Pickle is **not** available to guests — it only exists behind
  the local bridge and uses the host's OpenCode quota. Each link instead runs
  the on-device model with the recipient's own device resources.

### Add a model (dropdown)
- New "Add a model…" item in the model menu. Two kinds:
  1. **On-device** — any Hugging Face ONNX text-generation model id; loaded via
     transformers.js WebGPU/WASM, no key.
  2. **Cloud (bring your own)** — OpenAI-compatible endpoint, model id, API key.
     Key is AES-GCM encrypted in the device vault; only the name/marker ever
     reaches a model. Endpoint must allow browser CORS.
- Custom models persist in `localStorage.oracle.customModels`, can be removed
  from the dropdown, and are remembered across reloads. Fixed a render crash
  where the model pill looked up only the built-in list.

### Voice fixes
- Ending a live call now restores the previous spoken-replies setting instead of
  leaving every later chat reply talking. Verified off → on during call → off.
- Speech cancellation hardened (generation guard + delayed cancel).
- Added built-in voice presets: **Jarvis (male)**, **Assistant (female)**, and
  **Auto**, plus a full picker of every system voice on the device with Try
  buttons. Verified female → Samantha, male → Daniel, auto → Daniel; persisted
  across reload; zero console errors.
- Note: browsers cannot install voice models. No actor/character voice clone was
  downloaded — only device-installed voices are used.

Files touched: `Oracle-Chat-Live.html`, `oracle-pages/index.html`,
`oracle-pages/README.md`, regression docs, new GitHub repo + Pages config.

Tests: static site HTTP 200 PASS; self-contained share PASS; add/remove model
PASS; call audio restoration PASS; voice presets PASS; zero console errors PASS.

### Re-frozen after all tests passed
- New active live baseline SHA-256 recorded in README.md and restore-live.command.

## 2026-11-19 — Dropdown click fix and local-model tuning

Status: **implemented, browser-verified; baseline re-frozen; site republished**

### Bug fix: header menus appeared dead
- The full-screen `.backdrop` (z-index 40) covered the header dropdowns because
  `.chat-header` created a stacking context at z-index 30. The dropdown's own
  z-index 50 could not escape its parent, so real mouse clicks landed on the
  backdrop and just closed the menu. **Choose speaking voice**, the model
  dropdown, and the three-dot menu all looked like they did nothing.
- Fix: `.chat-header` raised to z-index 45 (still below the modal at 60).
- Found by testing with real mouse clicks; earlier scripted `.click()` calls
  bypassed hit-testing and missed it. Verified on both the local build and the
  published page: menu opens, voice changes (e.g. Albert), presets work, model
  dropdown opens. Zero console errors.

### Local model tuning
- System prompt now requires honest uncertainty, step-by-step checking, and
  attention to trick wording; added `oracle-knowledge/04-everyday-reasoning.md`.
- Benchmarked `qwen2.5:3b` vs pulled `qwen3:4b` on 8 everyday / pop-culture /
  reasoning questions. `qwen3:4b` got 8/8 (caught "all but 9") but took
  12–66 s per answer; `qwen2.5:3b` took 0.3–8.6 s and missed one trick
  question. With the new tuned prompt, `qwen2.5:3b` now answers that question
  correctly ("9 are left"). Kept `qwen2.5:3b` as default for voice-call speed;
  `qwen3:4b` is available on the Mac if you want the slower, deeper model.

### Re-frozen after tests passed
- New active live baseline: `5163205eab5fd24a0ddec3fc8e265a74211e542a02e4f8f95fc12c803e1594c7`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Deeper local model, tool restraint, late voice loading

Status: **implemented, browser-verified; baseline re-frozen; site republished**

- Added host-only **Qwen 3 4B (deeper)** to the model dropdown (`local-deep`).
  Bridge gained `DEEP_MODEL` and passes the chosen model to Ollama; status now
  reports `deepOk`. Guests and the static site do not see it. Default remains
  Qwen 2.5 3B so live voice calls stay fast.
  Verified: selecting it, asking the "17 sheep" trick question, got
  "9 are left" in ~40 s with `backend: local-deep`.
- System prompt now forbids tool calls for greetings, simple conversation, and
  one-word requests, and forbids reading the model's own knowledge/skill files
  to answer them. Verified "Reply with the word READY only." returned `READY`
  with no tool call in ~7 s.
- Voice picker now waits for asynchronously loaded voices (Safari) with a
  "Loading…" dialog instead of doing nothing. Verified: with `getVoices()`
  temporarily empty, the loading dialog appeared; on restore, all 199 voices
  and the presets appeared.
- Zero browser console errors; all checks used real mouse clicks.

### Re-frozen after tests passed
- New active live baseline: `e9729cf8b99dde1909aff6d1d38130d5e6576bbd559db0d4bfe2bcfea7fa9175`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Voice Try fix, safe code-change tool, Cloudflare-ready sharing

Status: **implemented, browser-verified; baseline re-frozen; site republished**

- **Voice "Try" preview fixed.** The preview called `cancelSpeech()`, which fires a
  second `cancel()` ~80 ms later and cut the sample off immediately. It now does a
  single cancel and starts the sample on the next tick. Verified with instrumented
  speech calls: `cancel → speak`, no second cancel, two previews in a row both work,
  zero console errors.
- **New `patch` tool for in-chat code edits.** It requires an exact match that occurs
  exactly once, saves a timestamped backup under `.oracle-backups/`, applies the
  change, and re-reads the file to verify it. Added to the tool list/prompt and a
  `code-change` skill that tells the model to read first, patch one focused change,
  report what changed, and ask the user to reload. Verified end-to-end in chat: the
  model emitted the tool call, the bridge patched the file, and the chat reported
  the backup path and `verified=True`. Failure cases (missing text, duplicate text)
  make no change.
- **Share links are now host-aware.** On any hosted build the share base is derived
  from the current page URL, so a Cloudflare Pages build (`oracle-chat.pages.dev`)
  generates clean links automatically. The Mac app keeps a stable public base until
  Cloudflare is live (one constant to flip in `Oracle-Chat-Live.html`).

### Re-frozen after tests passed
- New active live baseline: `3aa8c6252b6624529bc6388b50e552ae9fc5736d8d74e81adbc40e7143b758ed`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Neutral Cloudflare Pages URL

Status: **live and browser-verified; baseline re-frozen**

- Created the free Cloudflare Pages project `oracle-chat` from the `oracle-chat`
  GitHub repo (no build command, output `/`). GitHub app access was limited to
  that one repository. Site: `https://oracle-chat.pages.dev/`.
- Flipped `PUBLIC_SHARE_BASE` to the new URL so links generated in the Mac app
  are neutral too. Hosted builds still derive their base from the serving host.
- Both sites serve the identical build:
  `72e600ca13cc2b195adc20ca76cb56ff55907990f7268d06ad2a6aed0becbcdb`.
  GitHub Pages remains live as a backup.
- Verified on Cloudflare with real clicks: model dropdown (device only), 199
  device voices, "Try" preview speaks, zero console errors. A generated share
  link opened as an isolated guest with one blank chat ("My Oracle"), one folder
  ("My Chats") and only the device model — no host data.

### Re-frozen after tests passed
- New active live baseline: `72e600ca13cc2b195adc20ca76cb56ff55907990f7268d06ad2a6aed0becbcdb`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Phone layout and offline models

Status: **live and browser-verified; baseline re-frozen**

- The phone no longer hides the left panel. The sidebar (Chats / Folders /
  chats / profile) stays visible beside the chat at 320–430 px, using the same
  styling as the desktop version. The chat title ellipsizes so Share, model
  and the ⋯ menu always fit and are reachable.
- The header call icon is hidden on phones; the same live call is available
  from the ⋯ menu ("Live voice call"), so hands-free voice still works.
- Hosted model picker now offers two real private models: Tiny on-device 135M
  (`SmolLM2-135M-Instruct-ONNX-MHA`, ~182 MB q4) as the new default, and the
  previous 0.5B Qwen (~786 MB q4) for better answers. Both load through
  transformers.js and never use the host Mac.
- Added "Prepare private model now" in the model menu so the chosen model can
  be downloaded ahead of time, with a note explaining why Mac models are absent.
- Added `sw.js`, registered only on hosted builds. It caches the app shell and
  the jsdelivr / Hugging Face model files, so the site and its downloaded model
  work offline after the first load.
- Files touched: `Oracle-Chat-Live.html`, new `sw.js`, `oracle-pages/index.html`,
  `oracle-pages/sw.js`, Desktop publish script, regression docs.
- Test result: real-click phone checks passed at 320/360/390/430 px; hosted
  static mode, two models, ⋯ call item, sidebar folder/chat switching, and an
  offline reload all passed with zero console errors. Both sites serve the same
  build; `sw.js` matches on both.

### Re-frozen after tests passed
- New active live baseline: `c12bec4b1554e0a3e13e6b2eff231082ceaba87dca0cea745516572b2ccf876c`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Phone home-screen navigation, send button, call fixes

Status: **live and browser-verified; baseline re-frozen**

- The cramped always-visible side-by-side phone layout was replaced with a
  proper master/detail flow. On phones the **home screen is the full-width
  Chats / Folders list**. Tapping a folder expands it in place; tapping a chat
  opens that conversation full-screen. A **← back button** in the header
  returns to the home list from a chat, vault or memory screen. Desktop is
  unchanged — sidebar and chat still sit side-by-side.
- The **send button** was already in the markup but the narrow side-by-side
  composer overflowed (`scrollWidth 284` vs `clientWidth 226`), pushing it to
  x=404 on a 390 px phone — off-screen. With the full-width chat and
  `min-width:0` on the input, the send button now fits and is visible.
- The "New chat" pencil in the sidebar header was changed to a **plus sign**
  (matches its "New chat" action).
- The **live call button** was restored to the phone header (it had been moved
  into the ⋯ menu). The call loop now stops cleanly on mic permission/service
  errors and after four no-speech retries, so a blocked microphone can no
  longer wedge the page. Ending a call stops the speaker as before.
- Files touched: `Oracle-Chat-Live.html`, `oracle-pages/index.html`, regression
  docs, restore script.
- Test result: real-click checks passed at 320/360/390/430 px — home list,
  folder expand, chat open, back, visible send button with no composer
  overflow, reachable header controls, ⋯ menu (12 items), model dropdown,
  call start/end. Desktop unaffected. Hosted build verified in static mode
  with two device models and a working offline reload; zero console errors.

### Re-frozen after tests passed
- New active live baseline: `632270f6e06c12f72b84b54f78f9a738fbea267a8a89445abf1c2e8a1cf873a2`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Phone send no longer appears to reset

Status: **live and browser-verified; baseline re-frozen**

- Reported: asking anything on a phone looked like it reset the page and did
  nothing. The page was not actually navigating, but the first message triggers
  a ~182 MB private-model download; the old code called a full `render()` for
  each progress change (destroying the input and closing the keyboard) and only
  showed a bare "Thinking…" line, so it looked frozen. A phone tab killed during
  the load also lost the question, because state was only saved after the reply.
- Added `setDeviceStatus()` to update progress text in place instead of
  rebuilding the whole app. The message area now shows a clear, persistent
  "First time: downloading your private model — keep this page open" (and a
  device-CPU fallback message) rather than a silent spinner.
- `sendMessage()` now calls `saveState()` immediately after adding the user
  message, and an interrupted turn (saved chat ending on a user message) shows
  a "Try again" button. The input is refocused after send so the phone keyboard
  stays open. On-device generation has a 120 s timeout with a retry message.
- Reduced `max_new_tokens` from 200 to 160 for faster phone answers.
- Files touched: `Oracle-Chat-Live.html`, `oracle-pages/index.html`, regression
  docs, restore script.
- Test result: hosted phone check confirmed no navigation on send (window marker
  and unload counter unchanged), progress bar visible immediately, input still
  focused, answer arrives and progress clears. A simulated mid-generation reload
  preserved the question and showed the retry banner; retry re-sent it. Both
  sites serve the identical build.

### Re-frozen after tests passed
- New active live baseline: `b68c10321b0223bae8ade6563af5f21d465d9e21b47751a85a4a1750f0649c44`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — iPhone send crash fix (confirmed root cause)

Status: **live and browser-verified; baseline re-frozen**

- Reported: on iPhone Safari, sending "Hey" showed "preparing device", then
  returned to the Chats/Folders home (tab reload), and a second attempt left a
  blank page. The 182 MB q4 model + WebGPU→WASM fallback was too heavy for the
  phone tab and Safari killed it.
- Added a consent dialog on phones before the first model download, with clear
  wording about the size and the saved-question recovery.
- Phones now try WebGPU + q4f16 (118 MB — the smallest single download) and fall
  back to WASM int8 with a single thread. No duplicate WebGPU→WASM weight fetch.
- Fixed the prompt: role-tagged messages now use the model's own chat template.
  The previous `User:/Assistant:` string made the small model repeat itself and
  produce unusable answers.
- Service worker cache bumped to v2 so stale model files are cleared.
- Files touched: `Oracle-Chat-Live.html`, `oracle-pages/index.html`, `sw.js`,
  regression docs, restore script.
- Test result: hosted iPhone-UA check confirmed the consent dialog appears,
  the model loads, a coherent answer is returned, and there are no console
  errors. Both sites serve identical builds.

### Re-frozen after tests passed
- New active live baseline: `16af482f75974a6bf39d791f20aace5683a6b9bcfdad9623e7363d221f40e30f`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Phone models refreshed after runtime research

Status: **live and browser-verified; baseline re-frozen**

- Research (see `Regression Check/PHONE-MODEL-RESEARCH.md`) found the runtime,
  not just model size, caused the iPhone tab deaths: Transformers.js v3 is a
  known iOS memory problem (issue #1242), and an Oct 2026 five-runtime study
  found WebLLM and wllama ran on iPhone while Transformers.js answered then
  killed the tab.
- Swapped the phone path to **wllama** (llama.cpp/WASM) with GGUF models:
  - `SmolLM2-135M-Instruct-Q4_K_M` (~105 MB) — new default, fits any phone.
  - `LFM2.5-350M-Q4_K_M` (~229 MB) — "Balanced" option, better answers.
- Removed the old ONNX model IDs; model menu and consent dialog now show the
  correct model name and size. Custom on-device models accept `repo|file.gguf`.
- `sw.js`: cache bumped to v3; HTTP Range requests pass through uncached so a
  partial 206 cannot corrupt later GGUF loads.
- Files touched: `Oracle-Chat-Live.html`, `oracle-pages/index.html`, `sw.js`,
  regression docs, restore script. New research note added.
- Test result: hosted iPhone-UA check confirmed the consent dialog names
  Tiny 135M / 105 MB, the model loads, two consecutive sends answered with no
  console errors, and both phone models appear in the selector. Both sites
  serve identical builds.
- Caveat: small models trade depth for fit — 135M is chosen for reliability;
  use the Mac bridge build for demanding questions.

### Re-frozen after tests passed
- New active live baseline: `6a0e7e0fa2f01270babbc1626a8e3ada3b12c89ca19796a4042dd86738223c62`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Voice call: mic release, one-reply stall, iPhone speech

Status: **verified in emulated browser; baseline re-frozen**

User reports: (1) after speaking once the microphone stayed on after ending
the call, (2) the call stopped working after one reply, (3) spoken replies were
not audible on the phone.

Cause: the hands-free loop was driven only by `speechSynthesis.onend`. iOS
Safari frequently never fires that event (and speech needs a user gesture to
unlock), so the loop never restarted and the call bar stayed in "speaking".
A single shared `recognition` variable also meant an instance could outlive
the call and keep the mic active.

Fixes in `Oracle-Chat-Live.html`:
- Added a call generation token (`callGen`) so stale `onend`/`onerror`
  callbacks and restart timers cannot run after the call has ended.
- Track every recognition instance in `liveRecognitions`; `stopAllRecognition()`
  nulls handlers then aborts/stops all of them. `endCall()` is now the single
  teardown path used by the end button, header button, fatal errors, no-speech
  give-up and `listenLoop()` startup failure.
- `speak()` has a bounded fallback timer that calls `onDone` even if iOS never
  fires `onend`, so the call resumes listening after the first reply.
- `primeSpeech()` runs on the call-button tap (a real gesture): loads voices,
  resumes the engine, and unlocks speech with a silent utterance.
- `pagehide` releases recognition, speech and timers on back/tab-switch/sleep.
- `callState` resets to idle on end; `callGen` invalidates late loops.

Regression documentation:
- Split the single combined checklist into `MAIN-BROWSER-REGRESSION.md` and
  `PHONE-BROWSER-REGRESSION.md`, with all voice fixes listed in both and a
  real-device-only section in the phone list. `README.md` now links to them.

Verification: in-app browser with mocked `SpeechRecognition`/`speechSynthesis`.
Two simultaneous recognizers were both aborted on end; with `onend` never
firing, the fallback resumed the listener and created a new recognizer; ending
mid-speech left no recognizer after 8.5 s; no console errors (apart from the
expected `/api/status` 404 on a static server).

### Re-frozen after tests passed
- New active live baseline: `ac33c29a3b0936fabf33e963baebb4c16aba5274ea98eaf177efa541b0aa036d`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

## 2026-11-19 — Web routines (email, webhook, browser agent)

Status: **host-side tools verified; baseline re-frozen**

User asked for the model to use its own computer to handle accounts (post to
Instagram/Facebook, schedule posts, read and summarize email). Built as
explicit, credential-safe routines on the Mac bridge. The phone/static build
does not expose any of it: iOS Safari has no background browser automation for
websites, and guests must not hold owner credentials.

Added:
- `oracle_routines.py` — non-secret config in `oracle-routines.json`; IMAP
  email (`summary`/`check`/`read`/`search`) and JSON webhook posting. Secrets
  are resolved from the Keychain by name and never returned.
- `oracle_browser.py` — Playwright headless browser routine runner. Recorded
  steps (`goto`, `fill`, `click`, `press`, `wait`, `text`, `sleep`, `screenshot`)
  support `{{cred:NAME}}` and `{{param:name}}` placeholders.
- `.oracle-venv/` with Playwright + Chromium (project-local, not published).
- Bridge: `email`, `webhook`, `browser` tools in `system_prompt`, `tool_summary`,
  `run_tool`, `/api/status`; new owner-only `GET/POST /api/routines`.
- UI: **Profile → Web Routines** modal with config editor and status summary.
- Docs: `WEB-ROUTINES.md`; both browser regression lists updated.

Verified: all three tools through `/api/tool/execute`; the model invoked a
browser routine end-to-end through `/api/chat` and returned page text; webhook
POST returned 200 from a local test server; Routines modal opened with zero
console errors. Test credentials and configs were removed afterwards.

### Re-frozen after tests passed
- New active live baseline: `a02158996f8a80ac5c50240c40dc6ab405f0e64a9f7b2117c991655e28c02c13`.
- Original mockup baseline unchanged:
  `320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191`.

<!--
Template for a new entry:

## YYYY-MM-DD — short title

- What changed:
- Files touched:
- Why:
- Test result (checklist pass/fail):
- New baseline SHA-256 (if re-frozen):
-->
