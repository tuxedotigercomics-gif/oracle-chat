# Neutral share URL — done

Live site: **https://oracle-chat.pages.dev/**

No business name in the address. GitHub Pages is still live at the old URL as a
backup; nothing was removed.

## What was set up

- Free Cloudflare account, Pages project `oracle-chat`, connected to the GitHub
  repo `tuxedotigercomics-gif/oracle-chat`.
- Cloudflare GitHub app access was limited to that single repository.
- Build: no build command, output directory `/`, production branch `master`.
- Every push to that repo's `master` branch auto-deploys to Pages.

## Share links

- On either hosted site, share links are built from the page's own URL. A link
  created on Cloudflare uses `oracle-chat.pages.dev`.
- The Mac app uses `PUBLIC_SHARE_BASE` in `Oracle-Chat-Live.html`, now set to
  `https://oracle-chat.pages.dev/`, so shared links from the app are neutral too.

## How to publish future app changes

1. Update `Oracle-Chat-Live.html` (and `sw.js` if the offline cache changes).
2. Copy both to `oracle-pages/` (`index.html` and `sw.js`).
3. Commit and push the `oracle-pages` repo.
4. Both Cloudflare Pages and GitHub Pages update automatically.
5. Re-freeze the baseline and update the regression docs after tests pass.

## Offline use on a phone

- The hosted build registers `sw.js`, which saves the page itself and the model
  files the first time they load. After that the app opens and answers with no
  connection.
- Two private on-device models are offered: Tiny 135M (~182 MB download, the
  default) and 0.5B (~786 MB, better answers). Tap the model pill → "Prepare
  private model now" to download it before you need it.
- Voice replies use the phone's own installed voices and speech features.

## Verified

- Both sites serve the same SHA-256 build and the same `sw.js`.
- Real-click browser check: model dropdown, voice picker, Try preview, zero console errors.
- A share link opened as an isolated guest: one blank chat, one folder, device models only.
- Phone layout checked at 320–430 px: full-width Chats / Folders home list,
  tap a chat to open it, ← back to return; send button visible; no overflow.
- A full offline reload rendered the app from the service worker cache.
