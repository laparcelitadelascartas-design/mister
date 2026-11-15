import urllib.request, re, os, json
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36", "Accept-Language": "ca,es;q=0.9"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "replace")
os.makedirs("probe", exist_ok=True)
base = "https://www.fcf.cat"
page = get(base + "/ca/competicio/2026-2027/tercera-catalana/grup-7/calendari")
chunks = sorted(set(re.findall(r'(/_next/static/chunks/[A-Za-z0-9_\-./]+\.js)', page)))
out = []
for c in chunks:
    try:
        js = get(base + c)
    except Exception as e:
        out.append(f"### {c} ERROR {e}"); continue
    hits = []
    for m in re.finditer(r'https?://[A-Za-z0-9.\-]+(?:/[A-Za-z0-9_\-./{}$]*)?', js):
        s = m.group(0)
        if any(x in s for x in ["fcf", "api", "cluber"]): hits.append(("URL", s))
    for kw in ["/api/", "jornad", "calendari", "partits", "grupId", "grup_id", "fetch(", "classificacio", "equip"]:
        for m in re.finditer(re.escape(kw), js):
            a = max(0, m.start() - 160); b = min(len(js), m.end() + 220)
            hits.append((kw, js[a:b].replace("\n", " ")))
            if len([h for h in hits if h[0] == kw]) > 6: break
    out.append(f"### {c} len={len(js)}")
    seen = set()
    for k, s in hits:
        if s in seen: continue
        seen.add(s); out.append(f"[{k}] {s}")
open("probe/js.txt", "w").write("\n".join(out))
