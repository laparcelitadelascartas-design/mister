import urllib.request, urllib.error, http.cookiejar, json, os
os.makedirs("probe", exist_ok=True)
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36"
page = "https://www.fcf.cat/ca/competicio/2026-2027/tercera-catalana/grup-7/calendari"
log = []
r = op.open(urllib.request.Request(page, headers={"User-Agent": UA}), timeout=40)
log.append({"page_status": r.status, "set_cookie": r.headers.get_all("Set-Cookie"), "cookies": [c.name for c in cj]})
html = r.read().decode("utf-8", "replace")
def api(path, extra, tag):
    h = {"User-Agent": UA, "Referer": page, "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty"}
    h.update(extra)
    try:
        rr = op.open(urllib.request.Request("https://www.fcf.cat" + path, headers=h), timeout=40)
        b = rr.read().decode("utf-8", "replace")
        log.append({"tag": tag, "path": path, "status": rr.status, "len": len(b), "body": b[:600]})
        return b
    except urllib.error.HTTPError as e:
        log.append({"tag": tag, "path": path, "status": e.code, "headers": dict(e.headers.items()), "body": e.read().decode("utf-8", "replace")[:800]})
api("/api/competition/temporadas", {}, "cookies")
api("/api/competition/temporadas", {"X-Requested-With": "XMLHttpRequest"}, "xhr")
api("/api/competition/partidos?grupId=58161878", {}, "partidos t3g7")
# search for tokens in html
import re
toks = re.findall(r'(api[_-]?key|token|x-api|authorization)[^,]{0,120}', html, re.I)
log.append({"tokens_in_html": toks[:20]})
json.dump(log, open("probe/api_log.json", "w"), indent=1, ensure_ascii=False)
