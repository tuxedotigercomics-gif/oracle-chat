# Change workflow

Follow this order every time. The owner asked for a visible trail between the
frozen baseline and the working file, and for tests before any re-freeze.

## 1. Record before editing

In `Regression Check/CHANGELOG.md` add an entry marked **planned before edits**
describing the intended change. In `MAIN-BROWSER-REGRESSION.md` and
`PHONE-BROWSER-REGRESSION.md` add **unchecked** entries for the change. Keep the
host and phone checklists separate.

## 2. Edit only the allowed files

`Oracle-Chat-Live.html` for UI/app changes, `oracle_bridge.py` for host changes.
Never touch `Oracle-Chat-Offline.html` or the baseline. Bump the
`<meta name="oracle-build" content="...">` marker to a new value.

## 3. Harness test locally

Serve the workspace with `python3 -m http.server <port> --bind 0.0.0.0` and
drive it with browser automation. In OpenCode this is Code Mode: `execute` with
`tools.browser.tabs.open`, `reload`, `evaluate`, `console`, `wait`,
`tabs.close`. Start console capture before reload; assert zero console errors.

Useful patterns that were used successfully:

- Owner static: `http://oracle.localhost:<port>/Oracle-Chat-Live.html`
- Guest static: the same with `?share=gtest`
- Host: `http://127.0.0.1:<port>/Oracle-Chat-Live.html` (bridge expected; a
  static harness server produces a harmless `/api/status` 404)
- Simulate iOS: redefine `navigator.userAgent` and `navigator.platform` with
  `Object.defineProperty`, then restore the original descriptors.
- Simulate the image pipeline without downloading 382 MB: replace `IMG_FILES`
  with tiny fake sizes, stub `CacheStorage.prototype.open`, and inject a fake
  `imageRuntime` with `ort.Tensor` / `InferenceSession.create`. Assert a PNG
  blob, `blank:false`, expected providers and checkpoint stage.
- Capture diagnostics by stubbing `navigator.clipboard.writeText`.

There is no `setTimeout` in the Code Mode runtime itself; use
`new Promise(r=>setTimeout(r,10))` **inside** `page.evaluate` when a microtask
delay is needed.

## 4. Publish

```sh
cd '/Users/macbookair/Documents/Default Project'
shasum -a 256 Oracle-Chat-Live.html
cp Oracle-Chat-Live.html oracle-pages/index.html
cd oracle-pages
git add index.html
git commit -m "<describe the change>"
git push origin master
```

Documentation-only commits can add other files under `AI-HANDOFF/` the same
way; they must not change `index.html` or `sw.js`.

## 5. Verify live

Loop until both sites serve the new SHA, then check the worker and marker:

```sh
for u in 'https://oracle-chat.pages.dev/' \
         'https://tuxedotigercomics-gif.github.io/oracle-chat/'; do
  curl -sSfL "$u" | shasum -a 256
  curl -sSfL "${u%/}/sw.js" | shasum -a 256
  curl -sSfL "$u" | grep -o 'content="<build>"'
done
```

Then smoke-test all three pages (canonical owner, canonical guest, backup) in
the browser: correct build, expected models, expected command visibility, zero
console errors. Expected matrix:

| Page | Device models | Image cmd | Diagnostics |
|---|---|---|---|
| Owner static | 4 (`device-small`, `device`, `device-smart`, `device-free`) | yes | yes |
| Guest static | 2 (no `device-free`) | no | no |
| Host via bridge | 0 | no | no |

Web search visibility must match the same owner/static-only pattern: Profile →
Web search exists only for owner static; guest and host do not see it. With the
setting off, `webSources()` must return `null` with zero fetches.

## 6. Finish bookkeeping

- Change the changelog entry to **published and verified** with final SHA and
  Pages commit; add a short "Shipped in build ..." paragraph.
- Tick the harness/live regression items; leave physical-device items unchecked.
- Replace the old SHA with the new one in `README.md`, both regression
  checklists and `restore-live.command` (all under `Regression Check/`).
- `cp Oracle-Chat-Live.html 'Regression Check/baseline/Oracle-Chat-Live.html'`
  and confirm all three SHAs (source, published copy, baseline) match.
- Close harness tabs and stop the local HTTP server.

Only re-freeze after the harness and live checks pass. If a physical device pass
is still open, say so plainly rather than marking it done.

## Rollback

`Regression Check/restore-live.command` restores the recorded SHA. The frozen
baseline is `Regression Check/baseline/Oracle-Chat-Live.html`.
