# Monthly employer rating snapshot for you and your hiring competitors.
# Appends to employer_ratings.csv and prints the newest public reviews.
import csv, datetime, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
EMPLOYERS = ["Google", "Microsoft", "Meta"]

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90, params=params)
    r.raise_for_status()
    return r.json()

today = datetime.date.today().isoformat()
with open("employer_ratings.csv", "a", newline="") as f:
    out = csv.writer(f)
    for name in EMPLOYERS:
        hit = get("/v1/glassdoor/companies", q=name)["results"][0]
        c = get("/v1/glassdoor/company", employer_id=hit["employer_id"], slug=hit["slug"])["company"]
        r = c["ratings"]
        out.writerow([today, c["name"], r["overall"], r["work_life_balance"],
                      r["compensation_and_benefits"], r["senior_management"],
                      r["ceo_approval_pct"], r["recommend_to_friend_pct"],
                      c["counts"]["reviews"]])
        for review in c["latest_reviews"]:
            print(f"{c['name']} {review['rating']}/5 {review['job_title']}: {review['title']}")
