# Oracle Chat — what it is

Oracle Chat is a private, local-first AI chat app built for this Mac (8 GB MacBook Air). It looks like Grokbot and answers with a REAL model, never canned text.

## Files
- `Oracle-Chat-Offline.html` — FROZEN visual mockup / rollback baseline. Never edit before re-freezing. SHA-256 at freeze: 320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191
- `Oracle-Chat-Live.html` — the live UI served by the bridge. All new work happens here.
- `oracle_bridge.py` — Python stdlib server on 127.0.0.1:8765 (LAN 0.0.0.0 for share links). Chat, vault, tools, skills, sharing.
- `Regression Check/` — frozen baseline, restore.command, README checklist, CHANGELOG.
- `Desktop/Oracle Chat/` — Launch and Stop .command scripts.

## Models
- Local: Ollama `qwen2.5:3b` (~1.9 GB) at 127.0.0.1:11434. Runs offline, fits the 8 GB Mac.
- Cloud: bundled OpenCode CLI, free model `big-pickle`. Free quota was exhausted on 2026-11-19 (~5 PM MT reset). Default backend is `local` until cloud is confirmed working again. `auto` tries cloud then falls back to local on 429.

## Auto-start
- Ollama: Homebrew login service `sh.brew.ollama`.
- Bridge: LaunchAgent `com.oracle.chat.bridge` in ~/Library/LaunchAgents. RunAtLoad + KeepAlive. Logs at /opt/homebrew/var/log/oracle-chat.log (NOT in Documents — TCC blocks launchd writing there).

## Secrets
- Vault backed by macOS Keychain, prefix `oracle-vault-`. The model only ever sees credential NAMES. USE markers (double square brackets with a credential name and URL) are resolved bridge-side and results are redacted. Guest/share sessions have no vault access.
