// Owner cloud-state backup for Oracle Chat.
//
// This stores ONLY non-secret bot workspace state (chat titles, messages,
// folders, the active room) so a fresh device can restore its own roster even
// when the owner's Mac is off. It never receives vault keys, API keys, host
// tool results or guest sessions. Guests keep their state on their own device.
//
// Requires a free Cloudflare D1 database bound to this Pages project as
// ORACLE_DB. See AI-HANDOFF/CLOUD-VM-SETUP.md. If the binding is missing the
// endpoint degrades with a clear code instead of throwing.

const KEY_RE = /^[A-Za-z0-9_-]{8,64}$/;
const MAX_STATE_CHARS = 250000;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store'
    }
  });
}

function missingBinding() {
  // Return 200 with a controlled code: a 503 appears in the browser console as
  // a failed resource even though the app handles it cleanly.
  return json({
    ok: false,
    code: 'binding-missing',
    message: 'Cloud state needs the free D1 binding named ORACLE_DB. See AI-HANDOFF/CLOUD-VM-SETUP.md.'
  }, 200);
}

async function ensureTable(db) {
  await db.prepare(
    'CREATE TABLE IF NOT EXISTS oracle_state (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated INTEGER NOT NULL)'
  ).run();
}

export async function onRequestGet(context) {
  const db = context.env && context.env.ORACLE_DB;
  if (!db) return missingBinding();
  const key = new URL(context.request.url).searchParams.get('key') || '';
  if (!KEY_RE.test(key)) return json({ ok: false, code: 'bad-key' }, 400);
  try {
    await ensureTable(db);
    const row = await db.prepare('SELECT value, updated FROM oracle_state WHERE key = ?').bind(key).first();
    if (!row) return json({ ok: true, state: null });
    return json({ ok: true, state: JSON.parse(row.value), updated: row.updated });
  } catch (err) {
    return json({ ok: false, code: 'read-failed', message: String(err && err.message || err) }, 500);
  }
}

export async function onRequestPost(context) {
  const db = context.env && context.env.ORACLE_DB;
  if (!db) return missingBinding();
  let d;
  try {
    d = await context.request.json();
  } catch (err) {
    return json({ ok: false, code: 'bad-json' }, 400);
  }
  const key = String(d && d.key || '');
  if (!KEY_RE.test(key)) return json({ ok: false, code: 'bad-key' }, 400);
  const state = d && d.state;
  if (!state || typeof state !== 'object' || !Array.isArray(state.convs) || !Array.isArray(state.folders)) {
    return json({ ok: false, code: 'bad-state' }, 400);
  }
  const value = JSON.stringify(state);
  if (value.length > MAX_STATE_CHARS) return json({ ok: false, code: 'too-large' }, 413);
  try {
    await ensureTable(db);
    const updated = Date.now();
    await db.prepare(
      'INSERT INTO oracle_state (key, value, updated) VALUES (?, ?, ?) ' +
      'ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated = excluded.updated'
    ).bind(key, value, updated).run();
    return json({ ok: true, updated });
  } catch (err) {
    return json({ ok: false, code: 'write-failed', message: String(err && err.message || err) }, 500);
  }
}
