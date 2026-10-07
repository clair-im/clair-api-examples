# Build a news corpus for a topic from AP: search, then read each article,
# and write one JSON line per story for analysis or a retrieval index.
import json, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
QUERY = "hurricane"
PAGES = 5

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=60, params=params)
    r.raise_for_status()
    return r.json()

urls = []
for page in range(1, PAGES + 1):
    body = get("/v1/ap/search", q=QUERY, sort="newest", page=page)
    urls += [r["url"] for r in body["results"] if r["content_type"] == "article"]
    if not body["next_page"]:
        break

with open("corpus.jsonl", "w") as f:
    for url in dict.fromkeys(urls):  # keep order, drop repeats
        a = get("/v1/ap/article", url=url)["article"]
        f.write(json.dumps({
            "url": a["url"], "title": a["title"], "section": a["section"],
            "authors": [x["name"] for x in a["authors"]],
            "text": "\n\n".join(a["paragraphs"]),
        }) + "\n")
