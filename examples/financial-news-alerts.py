# Every 15 minutes: new Reuters, AP, and Bloomberg business headlines that
# name a company on the watchlist, with the article text for each match.
import json, os, pathlib, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
WATCHLIST = ["Nvidia", "Apollo", "Stripe", "OpenAI"]
LISTINGS = [("reuters", {"section": "business"}),
            ("ap", {"section": "business"}),
            ("bloomberg", {"section": "markets"})]
STATE = pathlib.Path("seen.json")
seen = set(json.loads(STATE.read_text())) if STATE.exists() else set()

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=60, params=params)
    r.raise_for_status()
    return r.json()

for source, params in LISTINGS:
    for item in get(f"/v1/{source}/search", **params)["results"]:
        names = [n for n in WATCHLIST if n.lower() in item["title"].lower()]
        if not names or item["url"] in seen:
            continue
        seen.add(item["url"])
        article = get(f"/v1/{source}/article", url=item["url"])["article"]
        lead = " ".join(article["paragraphs"][:2])
        cut = " (truncated)" if article["body_truncated"] else ""
        print(f"{', '.join(names)} | {source}: {article['title']}{cut}\n  {lead[:300]}")

STATE.write_text(json.dumps(sorted(seen)))
