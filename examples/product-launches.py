# Morning digest of yesterday's Product Hunt launches in chosen topics,
# with each product's makers and website.
import datetime, os, requests
from zoneinfo import ZoneInfo

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
TOPICS = {"artificial-intelligence", "developer-tools"}
TOP = 10

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=60, params=params)
    r.raise_for_status()
    return r.json()

# Product Hunt days run on Pacific time. Yesterday's board has final ranks;
# today's is still moving.
now = datetime.datetime.now(ZoneInfo("America/Los_Angeles"))
yesterday = (now - datetime.timedelta(days=1)).date().isoformat()
board = get("/v1/producthunt/launches", date=yesterday, period="daily")

picked = [launch for launch in board["results"]
          if TOPICS & {t["slug"] for t in launch["topics"]}][:TOP]
for launch in picked:
    # The /posts/ URL opens that launch, with its hunter, makers, and comments.
    product = get("/v1/producthunt/product", slug=launch["url"])["product"]
    makers = ", ".join(m["name"] for m in product["makers"]) or "not listed"
    print(f"#{launch['daily_rank']} {launch['name']}: {launch['tagline']}")
    print(f"    {launch['votes']} votes, {product['website']}, makers: {makers}")
