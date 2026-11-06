"""Scarica foto candidate da Pixabay (gira su GitHub Actions, chiave nel secret PIXABAY_KEY)."""
import json, os, pathlib, urllib.parse, urllib.request, time
# ROOT = radice del repo (due livelli sopra _src/tools/)
ROOT = pathlib.Path(__file__).resolve().parents[2]
KEY = os.environ["PIXABAY_KEY"]
req = json.loads((ROOT / "foto-richieste.json").read_text())
out = ROOT / "_src" / "foto-candidati"
UA = {"User-Agent": "NaturCampGuide-foto/1.0"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
for nome, queries in req["ricerche"].items():
    d = out / nome; d.mkdir(parents=True, exist_ok=True)
    meta = {}
    for q in queries:
        p = dict(key=KEY, q=q, image_type="photo", orientation="horizontal", min_width=1600,
                 safesearch="true", per_page=8, order="popular")
        data = json.loads(get("https://pixabay.com/api/?" + urllib.parse.urlencode(p)))
        for h in data.get("hits", [])[:5]:
            fn = f"{h['id']}.jpg"
            if fn in meta: continue
            (d / fn).write_bytes(get(h["largeImageURL"]))
            meta[fn] = {"id": h["id"], "query": q, "page": h["pageURL"], "user": h["user"], "tags": h["tags"],
                        "w": h["imageWidth"], "h": h["imageHeight"]}
            time.sleep(1)
    (d / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(nome, len(meta))
