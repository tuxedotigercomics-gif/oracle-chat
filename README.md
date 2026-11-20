# Oracle Chat

Canonical site: **https://oracle-chat.pages.dev/**

A private, local-first AI chat app. This site runs entirely in your browser —
there is no backend, no account, and no server that stores your chats.

## How it works

- Answers come from a small AI model that **runs on your own device** using
  WebGPU/WASM. Two sizes are offered: Tiny 135M (~182 MB, the default) and 0.5B
  (~786 MB, better answers). Use "Prepare private model now" in the model menu
  to download one ahead of time.
- A service worker caches the page and the model files, so after the first load
  the app keeps working with no internet connection.
- Your chats, folders, and settings stay in this browser's local storage.
- Voice input and spoken replies use your browser's built-in speech features.
- The "Use a saved login" vault encrypts values with a key that never leaves
  this browser. Only credential *names* are ever shown to the model.

## Share links

The "Share" button can create a family link. The chat you share is carried
**inside the link itself** (in the URL fragment, which is not sent to GitHub).
Anyone with the link can read what is in it, so only share with people you
trust. Opening a link gives you your own separate workspace — the sender's
other chats, folders, and vault are never included.

Because everything runs in the browser, a link keeps working even if the person
who created it is offline.

## Models & voice
- The model menu has an **Add a model…** option. Add another on-device model by
  Hugging Face ID, or a cloud model using your own endpoint and API key. Keys
  are encrypted in this browser and never shown to a model. The cloud endpoint
  must allow browser requests (CORS).
- Voice replies use a voice installed on your device. Use the three-dot menu →
  **Choose speaking voice** for one-click **Jarvis (male)**, **Assistant
  (female)**, or **Auto** presets, plus a full voice list with Try buttons.
  Browsers cannot install voice models, so no character/actor voice clone is
  included.

## Local development
The full local app (bridge, tools, vault, memory, auto-start) lives beside the
desktop source files; this repository is only the browser-only published build.

## For future maintainers and AI assistants
[`AI-HANDOFF/README.md`](AI-HANDOFF/README.md) records the current build, open
items, privacy rules, the change/verification workflow, the full image-generation
investigation, and snapshots of the regression checklists. Start there.
