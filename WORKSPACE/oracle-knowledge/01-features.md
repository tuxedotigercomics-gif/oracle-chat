# Features built into Oracle Chat

## Chat & UI
- Real answers from local qwen2.5:3b and free cloud Big Pickle; model selector (Local / Cloud→Local / Big Pickle).
- `+` menu: Attach a file, Use a saved login (vault), Teach a Skill.
- Editable profile name (click it), persisted in localStorage `oracle.displayName`. No `87` badge.
- Folders organization: CHATS / FOLDERS view toggle, multiple folders, click to open, drag a chat onto a folder, create/rename/delete folders, inline new folder when creating a chat room.
- 20 selectable pixel-art Marvel-style hero agents (CSS sprites, not images). Pick one when creating/naming a room. Hero shows beside room title and in the chat list. Hero has a color that color-codes the chat (sidebar stripe, avatar border, bot bubbles). Hero animates: raise-hand when help/approval needed, walking while working.
- Header three-dot menu by Share: New chat room, New folder, Tools mode toggle, Voice replies, Smart name/folder/summary, Share/export.
- Share button: copy transcript or download .txt.
- Smart actions (local model): name this room, suggest folder, summarize chat — in both header and per-chat menus.

## Tools (local model, all four scopes)
- read files/folders, write/edit files, shell commands, fetch web pages.
- Sandboxed to the project folder, path traversal blocked.
- Modes: `auto` (default — tools run immediately inside sandbox, no approval prompts) and `ask` (read-only + ask-first for write/shell/fetch). Toggle in the header three-dot menu.
- Blocked shell: sudo, rm -rf, mkfs, dd, shutdown, restart, killall, security, keychain, vault, printenv, env, secrets, credentials, tokens, /etc/, /var/, chmod 777, curl|wget pipes.
- Tool results are redacted before display.

## Voice
- Mic button: voice-to-text (Web Speech API).
- Volume button: spoken replies, Jarvis-style voice picked when the device provides one (Daniel/Oliver/George/Google UK English Male).
- Phone button: LIVE voice call — hands-free loop of listen → auto-send → speak reply → listen again. Uses the local model so it is fast. Works in Chrome/Android Chrome; iPhone Safari supports speech output but has limited speech recognition.

## Sharing (family)
- Tokenized links. Guests get their OWN blank workspace — no copy of your folders, other chats, or vault.
- Share a single chat (optional), or Share folder from a folder's three-dot menu (a copy of just that folder's chats).
- Works on the same Wi‑Fi as this Mac. For family elsewhere needs a secure tunnel (not set up yet).
- Guest sessions cannot create links, use the vault, change tools, or run tools.
