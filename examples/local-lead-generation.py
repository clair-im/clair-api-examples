# Local lead list: every business Google Maps lists for a category in each
# city, enriched with the email the business publishes on its website.
import csv, os, requests
from urllib.parse import urlparse

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
CATEGORY = "plumbers"
CITIES = ["Denver, CO", "Aurora, CO", "Boulder, CO"]

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=120, params=params)
    r.raise_for_status()
    return r.json()

seen = set()
with open("leads.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["name", "category", "phone", "website", "email", "address",
                  "rating", "reviews", "place_id"])
    for city in CITIES:
        body = get("/v1/google-maps/search", q=f"{CATEGORY} in {city}")
        for p in body["results"]:
            if p["place_id"] in seen or p["sponsored"]:
                continue  # neighbouring cities overlap; ads repeat organic listings
            seen.add(p["place_id"])
            email = None
            if p["website"]:
                try:
                    site = get("/v1/contacts", domain=urlparse(p["website"]).hostname, pages=3)
                    email = next((e["value"] for e in site["emails"] if e["domain_match"]), None)
                except requests.HTTPError:
                    pass  # site down or blocking; keep the Maps data
            out.writerow([p["title"], p["category"], p["phone"], p["website"], email,
                          p["address"], p["rating"], p["reviews_count"], p["place_id"]])
