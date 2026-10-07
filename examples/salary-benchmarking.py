# Salary bands for chosen job titles at the employers you hire against.
# Out: salaries.csv, one row per employer and title, base and total pay.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
EMPLOYERS = ["Stripe", "Datadog", "Cloudflare"]
TITLES = {"software engineer", "senior software engineer", "product manager"}
MAX_PAGES = 5  # 10 titles per page, most-reported first

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90, params=params)
    r.raise_for_status()
    return r.json()

with open("salaries.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["employer", "title", "reports", "base_p25", "base_p50",
                  "base_p75", "total_p50", "last_reported_at"])
    for name in EMPLOYERS:
        employer = get("/v1/glassdoor/companies", q=name)["results"][0]
        for page in range(1, MAX_PAGES + 1):
            body = get("/v1/glassdoor/salaries", employer_id=employer["employer_id"],
                       slug=employer["slug"], page=page)
            for row in body["results"]:
                if row["job_title"].lower() in TITLES:
                    b, t = row["base_pay"], row["total_pay"]
                    out.writerow([employer["name"], row["job_title"], row["salaries_count"],
                                  b["p25"], b["p50"], b["p75"], t["p50"],
                                  row["last_reported_at"]])
            if not body["next_cursor"]:
                break
