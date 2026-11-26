# Regression & troubleshooting

## Rule
Freeze the visual baseline BEFORE changes. Re-freeze only AFTER all regression tests pass.

## Checklist (Regression Check/README.md)
1. Baseline SHA-256 of Regression Check/baseline/Oracle-Chat-Offline.html must be 320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191 until re-freeze.
2. Open the frozen mockup and the live UI side by side; compare layout.
3. Verify model selector, + menu, attach chip, skills, vault panel (hidden behind profile name).
4. Verify folders toggle, drag-to-folder, inline new folder, room creation with hero, share/export.
5. Verify local answer (BRIDGE_LOCAL_OK) and auto fallback (BRIDGE_AUTO_OK).
6. Verify tool read/deny/approve and redaction.
7. Check browser console: zero errors.
8. Update CHANGELOG, then re-freeze baseline.

## Rollback
Double-click `Regression Check/restore.command` to restore the frozen mockup over the live file. Only do this with approval if office work is involved.

## Common failures
- Bridge down: double-click Desktop/Oracle Chat/Launch Oracle Chat.command. Check /opt/homebrew/var/log/oracle-chat.log.
- Cloud 429 `provider.free-limit`: expected until quota resets; default backend is local.
- Console errors after edits: reload with cache-busting URL.
- launchd EX_CONFIG: log paths in ~/Documents are blocked by TCC; keep logs in /opt/homebrew/var/log.
