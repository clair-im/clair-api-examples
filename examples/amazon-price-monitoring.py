# Daily price and Buy Box snapshot for a list of ASINs.
# Appends one row per ASIN to prices.csv; diff consecutive days to alert.
import csv, datetime, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
ASINS = ["B0CF3VGQFL", "B004YAVF8I", "B015NBTAOW"]
ZIP = "10001"  # prices and the Buy Box follow the delivery location

def product(asin):
    r = requests.get(f"{API}/v1/amazon/product", headers=HEADERS, timeout=60,
                     params={"asin": asin, "zip_code": ZIP})
    r.raise_for_status()
    return r.json()["product"]

today = datetime.date.today().isoformat()
with open("prices.csv", "a", newline="") as f:
    out = csv.writer(f)
    for asin in ASINS:
        try:
            p = product(asin)
        except requests.HTTPError as e:
            print(asin, e.response.status_code, e.response.text[:200])
            continue
        seller = p["sold_by"] or {}
        out.writerow([today, asin, p["price"], p["currency"],
                      p["original_price"], p["availability"],
                      seller.get("id"), seller.get("name"),
                      p["rating"], p["ratings_count"]])
