import urllib.request, json, os, re
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36", "Accept-Language": "ca,es;q=0.9",
      "Origin": "https://laparcelitadelascartas-design.github.io", "Accept": "application/json"}
B = "https://www.fcf.cat"
os.makedirs("probe", exist_ok=True)
log = []
def get(path, name):
    try:
        r = urllib.request.urlopen(urllib.request.Request(B + path, headers=UA), timeout=40)
        body = r.read().decode("utf-8", "replace")
        hdr = {k: v for k, v in r.headers.items() if k.lower().startswith(("access-control", "content-type", "cache", "x-", "cf-", "server", "vary"))}
        log.append({"path": path, "status": r.status, "headers": hdr, "len": len(body)})
        open(f"probe/{name}.json", "w").write(body)
        return json.loads(body)
    except Exception as e:
        log.append({"path": path, "error": repr(e)}); return None
temps = get("/api/competition/temporadas", "temporadas")
disc = get("/api/competition/disciplines", "disciplines")
get("/api/search?q=sant%20ildefons&locale=ca", "search")
f7 = None
for d in (disc or []):
    if "7" in str(d.get("label", "")) and "SALA" not in str(d.get("label", "")).upper(): f7 = d
log.append({"f7": f7})
if f7:
    comps = get(f"/api/competition/competicions?disciplinaId={f7['value']}&temporada=22", "competicions_f7")
    pre = [c for c in (comps or []) if "PREBENJ" in c.get("label", "").upper()]
    log.append({"prebenjami": pre})
    for c in pre[:6]:
        gr = get(f"/api/competition/grupos?competicioId={c['value']}&temporada=22", f"grupos_{c['value']}")
        g20 = [g for g in (gr or []) if re.search(r"\b20\b", g.get("label", ""))]
        if g20:
            gid = g20[0]["value"]; log.append({"comp": c, "grup": g20[0]})
            get(f"/api/competition/partidos?grupId={gid}", "partidos_g20")
            get(f"/api/competition/classificacio?grupId={gid}", "classificacio_g20")
            get(f"/api/competition/equipos?grupId={gid}&temporada=22", "equipos_g20")
            break
json.dump(log, open("probe/api_log.json", "w"), indent=1, ensure_ascii=False)
