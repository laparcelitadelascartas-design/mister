import urllib.request, re, os, json, ssl
URLS = [
 "https://www.fcf.cat/en/competicio/2026-2027/tercera-catalana/grup-7/resultats",
 "https://www.fcf.cat/ca/competicio/2026-2027/tercera-catalana/grup-7/calendari",
 "https://www.fcf.cat/ca/competicio/2026-2027/tercera-catalana/grup-7/classificacio",
 "https://www.fcf.cat/calendari/2627/futbol-11/tercera-catalana/grup-7",
 "https://www.fcf.cat/ca/clubs",
 "https://www.fcf.cat/ca/noticies-fcf/1036839",
 "https://www.fcf.cat/ca/competicions",
 "https://www.fcf.cat/",
]
os.makedirs("probe", exist_ok=True)
idx = []
for i, u in enumerate(URLS):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36", "Accept-Language": "ca,es;q=0.9"})
        r = urllib.request.urlopen(req, timeout=40)
        body = r.read().decode("utf-8", "replace")
        open(f"probe/{i:02d}.html", "w").write(body)
        hrefs = sorted(set(re.findall(r'href="([^"]+)"', body)))
        keep = [h for h in hrefs if re.search(r"competicio|equip|club|calendari|partit|acta|api", h)]
        scripts = re.findall(r'<script[^>]+src="([^"]+)"', body)
        apis = sorted(set(re.findall(r'["\'](/api/[^"\']+|https://[^"\']*api[^"\']*)["\']', body)))
        idx.append({"i": i, "url": u, "final": r.geturl(), "status": r.status, "len": len(body), "hrefs": keep[:300], "scripts": scripts[:40], "apis": apis[:80]})
    except Exception as e:
        idx.append({"i": i, "url": u, "error": repr(e)})
json.dump(idx, open("probe/index.json", "w"), indent=1, ensure_ascii=False)
