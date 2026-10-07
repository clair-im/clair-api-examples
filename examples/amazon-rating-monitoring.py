# Weekly rating snapshot for your products and competitors on Amazon,
# with the share of 1- and 2-star ratings and any new critical reviews.
import csv, datetime, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
ASINS = ["B0CF3VGQFL", "B004YAVF8I"]

def reviews(asin):
    r = requests.get(f"{API}/v1/amazon/reviews", headers=HEADERS, timeout=90,
                     params={"asin": asin})
    r.raise_for_status()
    return r.json()

today = datetime.date.today().isoformat()
with open("ratings.csv", "a", newline="") as f:
    out = csv.writer(f)
    for asin in ASINS:
        body = reviews(asin)
        p, dist = body["product"], body["product"]["rating_distribution"]
        low = dist.get("1", 0) + dist.get("2", 0)  # percent of ratings
        out.writerow([today, asin, p["rating"], p["ratings_count"], low])
        for review in body["reviews"]:
            if review["rating"] <= 2:
                print(f"{asin} {review['rating']} stars {review['date']}: {review['title']}")
