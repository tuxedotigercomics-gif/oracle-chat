# Oracle Chat

A private, local-first AI chat app. This site runs entirely in your browser —
there is no backend, no account, and no server that stores your chats.

## How it works

- Answers come from a small AI model that **runs on your own device** using
  WebGPU/WASM (downloaded the first time you chat, then cached by your browser).
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
