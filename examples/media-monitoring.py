# Hourly media monitoring: new Google News headlines for brand terms,
# deduplicated across terms and markets. Keeps seen keys in seen.json.
import json, os, pathlib, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
TERMS = ['"Acme Corp"', '"Jane Doe" CEO', "acme.com"]
MARKETS = [("en", "us"), ("en", "gb")]
STATE = pathlib.Path("seen.json")
seen = set(json.loads(STATE.read_text())) if STATE.exists() else set()

def headlines(q, language, country):
    # A busy term fills more than one page in an hour; follow next_cursor.
    page = 1
    while page:
        r = requests.get(f"{API}/v1/google-news", headers=HEADERS, timeout=60, params={
            "q": q, "when": "1h", "page": page,
            "language": language, "country": country})
        r.raise_for_status()
        body = r.json()
        yield from body["results"]
        page = body["next_cursor"]

def story_key(item):
    # Outlets syndicate and markets overlap, so key on outlet and headline
    # rather than the URL.
    return f"{item['source']['name'].lower()}|{item['title'].lower()}"

for term in TERMS:
    for language, country in MARKETS:
        for item in headlines(term, language, country):
            key = story_key(item)
            if key in seen:
                continue
            seen.add(key)
            print(f"[{item['source']['name']}] {item['title']}\n  {item['url']}")

STATE.write_text(json.dumps(sorted(seen)))
