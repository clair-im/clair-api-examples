# MAP check: find listings of a brand's products priced below the minimum
# advertised price, and name the sellers behind each.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
BRAND = "Logitech"
MAP = {"B004YAVF8I": 14.99, "B015NBTAOW": 49.99}  # ASIN -> minimum advertised price
ZIP = "10001"

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90,
                     params={"zip_code": ZIP, **params})
    r.raise_for_status()
    return r.json()

with open("map_violations.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["asin", "map", "seller_id", "seller", "condition", "price"])
    for page in range(1, 4):  # the brand's first three result pages
        body = get("/v1/amazon/search", q=BRAND, brand=BRAND, page=page)
        for item in body["results"]:
            floor = MAP.get(item["asin"])
            prices = [item["price"], (item["other_offers"] or {}).get("min_price")]
            lowest = min((p for p in prices if p), default=None)
            if floor is None or lowest is None or lowest >= floor:
                continue  # not a watched ASIN, or nobody is below MAP
            for offer in get("/v1/amazon/offers", asin=item["asin"])["offers"]:
                if offer["condition"] == "New" and offer["price"] < floor:
                    out.writerow([item["asin"], floor, offer["seller"]["id"],
                                  offer["seller"]["name"], offer["condition"], offer["price"]])
        if not body["next_cursor"]:
            break
