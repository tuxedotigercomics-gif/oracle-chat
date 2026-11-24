// Same-origin bridge for public news lookups.
//
// Browsers cannot call api.gdeltproject.org directly: GDELT sends no
// Access-Control-Allow-Origin header, so that fetch dies before the app sees any
// articles. Cloudflare Pages can fetch news server-side, so the phone app posts
// its query here and receives plain JSON. Google News RSS is the primary source
// (fast, no key, real dated local articles); GDELT remains as a fallback. GitHub
// Pages has no Functions runtime, so that host skips this endpoint and falls
// straight back to Wikipedia.
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

function decodeXml(value) {
  return String(value || '')
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, dec) => String.fromCharCode(Number(dec)))
    .replace(/&apos;|&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
}

function tag(block, name) {
  const match = block.match(new RegExp('<' + name + '(?:\\s[^>]*)?>([\\s\\S]*?)<\\/' + name + '>', 'i'));
  return match ? decodeXml(match[1]) : '';
}

function seendate(pubDate) {
  const d = new Date(pubDate);
  return isNaN(d.getTime()) ? '' : d.toISOString().slice(0, 10).replace(/-/g, '');
}

async function fetchGoogleNews(query) {
  const url = 'https://news.google.com/rss/search?' + new URLSearchParams({
    q: query + ' when:7d',
    hl: 'en-US',
    gl: 'US',
    ceid: 'US:en'
  });
  const res = await fetch(url);
  if (!res.ok) throw new Error('Google News status ' + res.status);
  const xml = await res.text();
  const articles = [];
  for (const item of (xml.match(/<item>[\s\S]*?<\/item>/gi) || [])) {
    const title = tag(item, 'title');
    const link = tag(item, 'link');
    if (!title || !link) continue;
    const source = item.match(/<source[^>]*url="([^"]+)"[^>]*>([\s\S]*?)<\/source>/i);
    articles.push({
      title: title.slice(0, 140),
      url: link,
      domain: (source ? decodeXml(source[2]) : 'Google News').slice(0, 80),
      seendate: seendate(tag(item, 'pubDate'))
    });
    if (articles.length >= 4) break;
  }
  return articles;
}

async function fetchGdelt(query) {
  const url = 'https://api.gdeltproject.org/api/v2/doc/doc?' + new URLSearchParams({
    query: query + ' sourcelang:english',
    mode: 'artlist',
    format: 'json',
    sort: 'datedesc',
    timespan: '1month',
    maxrecords: '4'
  });

  // GDELT asks for at most one request every five seconds. One retry is enough
  // for the common 429 burst when a Home Screen app is reopened.
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(url);
      if (res.status === 429) {
        if (attempt === 0) {
          await new Promise(resolve => setTimeout(resolve, 5200));
          continue;
        }
        return [];
      }
      if (!res.ok) return [];
      const text = await res.text();
      try {
        const data = JSON.parse(text);
        return Array.isArray(data && data.articles) ? data.articles : [];
      } catch (e) {
        return [];
      }
    } catch (e) {
      if (attempt === 0) continue;
      return [];
    }
  }
  return [];
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

  try {
    const articles = await fetchGoogleNews(query);
    if (articles.length) return json({ articles });
  } catch (e) {
    // GDELT and then the app's Wikipedia fallback still get a chance.
  }
  return json({ articles: await fetchGdelt(query) });
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
