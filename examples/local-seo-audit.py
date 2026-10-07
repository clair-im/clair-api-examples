# Local competitor audit: how a business compares with the others Google
# Maps shows for the searches its customers make.
import os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
MY_PLACE_ID = "ChIJszGcvzV0bIcR3_6j5Gru8sM"
SEARCHES = ["plumber denver", "water heater repair denver", "emergency plumber denver"]

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=120, params=params)
    r.raise_for_status()
    return r.json()

for q in SEARCHES:
    results = [p for p in get("/v1/google-maps/search", q=q)["results"] if not p["sponsored"]]
    mine = next((p for p in results if p["place_id"] == MY_PLACE_ID), None)
    print(f"\n{q}: position {mine['position'] if mine else 'not listed'} of {len(results)}")
    for p in results[:5]:
        print(f"  #{p['position']} {p['title']}: {p['rating']} stars, {p['reviews_count']} reviews")

# What customers mention most, for you and the top competitor of the last search.
for place_id in [MY_PLACE_ID, results[0]["place_id"]]:
    place = get("/v1/google-maps/place", place_id=place_id)["place"]
    topics = ", ".join(f"{t['topic']} ({t['mentions']})" for t in place["review_topics"])
    print(f"\n{place['title']} [{place['view']} view]: {topics}")
