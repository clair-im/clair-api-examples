# Daily deal flow: yesterday's top Product Hunt launches in chosen topics,
# each with its makers, website contacts, and Crunchbase profile if one exists.
import datetime, os, re, requests
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
TOPICS = {"artificial-intelligence", "developer-tools", "fintech"}

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90, params=params)
    r.raise_for_status()
    return r.json()

day = (datetime.datetime.now(ZoneInfo("America/Los_Angeles")) - datetime.timedelta(days=1)).date()
board = get("/v1/producthunt/launches", date=day.isoformat(), period="daily")
for launch in board["results"][:20]:
    if not TOPICS & {t["slug"] for t in launch["topics"]}:
        continue
    product = get("/v1/producthunt/product", slug=launch["url"])["product"]
    makers = ", ".join(m["name"] for m in product["makers"])
    print(f"#{launch['daily_rank']} {launch['name']}: {launch['tagline']} ({launch['votes']} votes)")
    print(f"   makers: {makers or 'not listed'}")
    if product["website"]:
        site = get("/v1/contacts", domain=urlparse(product["website"]).hostname, pages=3)
        linkedin = next((s["url"] for s in site["social"] if s["network"] == "linkedin"), None)
        print(f"   {product['website']} {[e['value'] for e in site['emails']][:2]} {linkedin or ''}")
    # Crunchbase has no search: try the product name as the permalink.
    permalink = re.sub(r"[^a-z0-9]+", "-", launch["name"].lower()).strip("-")
    try:
        org = get("/v1/crunchbase/organization", permalink=permalink)["organization"]
        if org["website"] and urlparse(org["website"]).hostname == urlparse(product["website"] or "").hostname:
            print(f"   Crunchbase: {org['employee_range']} employees, {org['funding']['num_rounds']} rounds")
    except requests.HTTPError:
        pass  # no profile under that name
