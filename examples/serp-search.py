# Daily Google rank check: where does your domain rank for each keyword?
# Reads up to MAX_PAGES result pages per keyword and stops at the first hit.
import csv, datetime, os, requests
from urllib.parse import urlparse

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
DOMAIN = "example.com"
KEYWORDS = ["payment api", "accept payments online", "invoice software"]
COUNTRY, LANGUAGE, MAX_PAGES = "us", "en", 3  # each page is one request
FEATURES = ("knowledge_graph", "people_also_ask", "local_results", "videos")

def serp(q, page):
    r = requests.get(f"{API}/v1/google-search", headers=HEADERS, timeout=60, params={
        "q": q, "country": COUNTRY,
        "language": LANGUAGE, "page": page})
    r.raise_for_status()
    return r.json()

def ours(url):
    host = (urlparse(url).hostname or "").removeprefix("www.")
    return host == DOMAIN or host.endswith("." + DOMAIN)

today = datetime.date.today().isoformat()
with open("ranks.csv", "a", newline="") as f:
    out = csv.writer(f)
    for q in KEYWORDS:
        rank, url, features = None, None, []
        for page in range(1, MAX_PAGES + 1):
            body = serp(q, page)
            if page == 1:  # SERP blocks sit on the first page
                features = [k for k in FEATURES if body.get(k)]
            hit = next((r for r in body["results"] if ours(r["url"])), None)
            if hit:
                rank, url = hit["position"], hit["url"]
                break
            if len(body["results"]) < 10:
                break  # Google has no further pages for this query
        out.writerow([today, q, COUNTRY, rank, url, "|".join(features)])
