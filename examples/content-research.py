# Map what searchers ask around a topic: People also ask and related
# searches for seed queries, expanded one level. Out: questions.csv.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
SEEDS = ["web scraping api", "serp api", "amazon price tracker"]

def serp(q):
    r = requests.get(f"{API}/v1/google-search", headers=HEADERS, timeout=60, params={
        "q": q, "country": "us", "language": "en"})
    r.raise_for_status()
    return r.json()

rows, done = [], set()
for seed in SEEDS:
    body = serp(seed)
    done.add(seed)
    rows += [(seed, "question", q) for q in body["people_also_ask"]]
    rows += [(seed, "related", q) for q in body["related_searches"]]
    # One level deeper: related searches are queries people type next.
    for q in body["related_searches"][:5]:
        if q in done:
            continue
        done.add(q)
        rows += [(q, "question", x) for x in serp(q)["people_also_ask"]]

with open("questions.csv", "w", newline="") as f:
    csv.writer(f).writerows([("from_query", "kind", "text"), *dict.fromkeys(rows)])
