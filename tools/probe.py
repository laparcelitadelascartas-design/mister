import urllib.request, re, os
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "replace")
os.makedirs("probe", exist_ok=True)
B = "https://www.fcf.cat"
page = get(B + "/ca/competicio/2026-2027/tercera-catalana/grup-7/calendari")
for c in sorted(set(re.findall(r'(/_next/static/chunks/[A-Za-z0-9_\-./]+\.js)', page))):
    js = get(B + c)
    if "competition/partidos" in js or "grupos?competicioId" in js or "classificacio?grupId" in js:
        open("probe/chunk_" + c.split("/")[-1], "w").write(js)
