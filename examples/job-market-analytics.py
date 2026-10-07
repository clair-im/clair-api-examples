# Weekly count of new openings and posted pay for a set of roles and cities.
# Appends to market.csv; chart it to see demand and pay move.
import csv, datetime, os, statistics, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
ROLES = ["data engineer", "machine learning engineer"]
CITIES = ["New York, NY", "Austin, TX", "Seattle, WA"]

def search(q, location):
    r = requests.get(f"{API}/v1/indeed/jobs", headers=HEADERS, timeout=90, params={
        "q": q, "location": location, "posted": "7d"})
    r.raise_for_status()
    return r.json()["results"]

week = datetime.date.today().isocalendar()
with open("market.csv", "a", newline="") as f:
    out = csv.writer(f)
    for role in ROLES:
        for city in CITIES:
            jobs = search(role, city)
            # Annual pay only; hourly and monthly postings are kept out of the median.
            mids = [(j["salary"]["min"] + j["salary"]["max"]) / 2 for j in jobs
                    if j["salary"] and j["salary"]["period"] == "year"
                    and j["salary"]["min"] and j["salary"]["max"]]
            remote = sum(1 for j in jobs if j["remote"])
            out.writerow([f"{week.year}-W{week.week:02d}", role, city, len(jobs),
                          len(mids), statistics.median(mids) if mids else None, remote])
