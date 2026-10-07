# Collect new Trustpilot reviews for a list of companies since the last run
# and flag the negative ones. Keeps the newest seen review id per company.
import json, os, pathlib, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
COMPANIES = ["stripe.com", "adyen.com", "wise.com"]
STATE = pathlib.Path("seen.json")
seen = json.loads(STATE.read_text()) if STATE.exists() else {}

def listing(domain, page):
    r = requests.get(f"{API}/v1/trustpilot/reviews", headers=HEADERS, timeout=60, params={
        "domain": domain, "sort": "recency", "language": "all", "page": page})
    r.raise_for_status()
    return r.json()

for domain in COMPANIES:
    new, page = [], 1
    while page:  # next_page is null after page 10, the anonymous limit
        body = listing(domain, page)
        if page == 1:
            b = body["business"]
            print(f"{domain}: TrustScore {b['trust_score']}, {b['review_count']} reviews")
        fresh = []
        for review in body["results"]:
            if review["id"] == seen.get(domain):
                break
            fresh.append(review)
        new += fresh
        # Stop at last run's newest review; on a first run, keep page 1 only.
        if len(fresh) < len(body["results"]) or domain not in seen:
            break
        page = body["pagination"]["next_page"]
    for review in new:
        if review["rating"] <= 2:
            print(f"  {review['rating']} stars: {review['title']!r} {review['url']}")
    if new:
        seen[domain] = new[0]["id"]

STATE.write_text(json.dumps(seen, indent=2))
