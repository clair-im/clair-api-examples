# Benchmark companies in a Trustpilot category: TrustScore, share of
# 1-star reviews, and how often each replies to negative reviews.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
CATEGORY, COUNTRY, PAGES = "bank", "GB", 2

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=60, params=params)
    r.raise_for_status()
    return r.json()

companies = []
for page in range(1, PAGES + 1):
    body = get("/v1/trustpilot/categories", category=CATEGORY, country=COUNTRY,
               sort="reviews_count", page=page)
    companies += body["results"]

with open("benchmark.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["company", "trust_score", "reviews", "reviews_12m",
                  "one_star_pct", "negative_reply_rate", "days_to_reply"])
    for c in companies:
        b = get("/v1/trustpilot/reviews", domain=c["domain"])["business"]
        one = next((d["percent"] for d in b["rating_distribution"] if d["stars"] == 1), None)
        reply = b["reply_behavior"] or {}
        out.writerow([b["name"], b["trust_score"], b["review_count"],
                      b["review_count_last_12_months"], one,
                      reply.get("negative_reply_rate"), reply.get("average_days_to_reply")])
