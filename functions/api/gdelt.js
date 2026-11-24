// Same-origin bridge for GDELT's public news API.
//
// Browsers cannot call api.gdeltproject.org directly: GDELT sends no
// Access-Control-Allow-Origin header, so the fetch dies before the app sees any
// articles. Cloudflare Pages can fetch it server-side, so the phone app posts
// the query here and receives plain JSON. GitHub Pages has no Functions runtime;
// that host skips this endpoint and falls straight back to Wikipedia.
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...CORS,
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store'
    }
  });
}

function empty(status = 200) {
  return json({ articles: [] }, status);
}

export async function onRequestPost({ request }) {
  let query = '';
  try {
    const input = await request.json();
    query = String((input && input.query) || '').replace(/\s+/g, ' ').trim().slice(0, 200);
  } catch (e) {
    return json({ error: 'Invalid JSON body' }, 400);
  }
  if (!query) return empty();

  const url = 'https://api.gdeltproject.org/api/v2/doc/doc?' + new URLSearchParams({
    query: query + ' sourcelang:english',
    mode: 'artlist',
    format: 'json',
    sort: 'datedesc',
    timespan: '1month',
    maxrecords: '4'
  });

  // One retry is enough for the common 429 burst when a Home Screen app is
  // reopened. If GDELT still refuses, return no articles: the app's Wikipedia
  // fallback will provide dated source links instead of a generic answer.
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(url);
      if (res.status === 429) {
        if (attempt === 0) {
          await new Promise(resolve => setTimeout(resolve, 400));
          continue;
        }
        return empty();
      }
      if (!res.ok) return empty(502);
      const text = await res.text();
      try {
        const data = JSON.parse(text);
        return json({ articles: Array.isArray(data && data.articles) ? data.articles : [] });
      } catch (e) {
        return empty();
      }
    } catch (e) {
      if (attempt === 0) continue;
      return empty(502);
    }
  }
  return empty();
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
