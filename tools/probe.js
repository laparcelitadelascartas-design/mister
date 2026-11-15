const { chromium } = require('playwright-core');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ userAgent: 'Mozilla/5.0 (Linux; Android 14; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.0.0 Mobile Safari/537.36' })).newPage();
  const out = {};
  await p.goto('https://www.fcf.cat/ca/competicio', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(3000);
  out.cookies = (await p.context().cookies()).map(c => c.name);
  for (const path of ['/api/competition/temporadas', '/api/competition/disciplines']) {
    out[path] = await p.evaluate(async (u) => { try { const r = await fetch(u); const t = await r.text(); return { status: r.status, body: t.slice(0, 1500) }; } catch (e) { return { err: String(e) }; } }, path);
  }
  // network log of the page's own API calls
  fs.writeFileSync('probe/browser.json', JSON.stringify(out, null, 1));
  await b.close();
})();
