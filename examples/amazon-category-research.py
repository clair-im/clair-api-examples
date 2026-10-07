# Map an Amazon category: the top 60 best sellers in each subcategory,
# with price and ratings. Out: category.csv.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
CATEGORY = "electronics"

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90, params=params)
    r.raise_for_status()
    return r.json()

top = get("/v1/amazon/bestsellers", category=CATEGORY)
with open("category.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["subcategory", "rank", "asin", "title", "price", "rating", "ratings"])
    for sub in top["subcategories"]:
        for page in (1, 2):  # 30 products a page, two pages per list
            body = get("/v1/amazon/bestsellers", category=CATEGORY,
                       node_id=sub["node_id"], page=page)
            for p in body["results"]:
                out.writerow([sub["name"], p["rank"], p["asin"], p["title"],
                              p["price"], p["rating"], p["ratings_count"]])
