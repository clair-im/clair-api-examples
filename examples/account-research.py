# One-page account brief from a company's domain and name: what it
# publishes, how employees and customers rate it, and its Crunchbase facts.
import os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}

def get(path, **params):
    r = requests.get(f"{API}{path}", headers=HEADERS, timeout=90, params=params)
    r.raise_for_status()
    return r.json()

def brief(domain, name, permalink):
    site = get("/v1/contacts", domain=domain, pages=5)
    org = get("/v1/crunchbase/organization", permalink=permalink)["organization"]
    tp = get("/v1/trustpilot/reviews", domain=domain)["business"]
    gd_hit = get("/v1/glassdoor/companies", q=name)["results"][0]
    gd = get("/v1/glassdoor/company", employer_id=gd_hit["employer_id"],
             slug=gd_hit["slug"])["company"]
    hq = org["headquarters"] or {}
    return {
        "company": org["name"], "hq": f"{hq.get('city')}, {hq.get('country')}",
        "employees": org["employee_range"], "status": org["ipo_status"],
        "founders": [f["name"] for f in org["founders"]],
        "funding_rounds": org["funding"]["num_rounds"],
        "emails": [e["value"] for e in site["emails"] if e["domain_match"]],
        "phones": [p["e164"] for p in site["phones"]],
        "trustpilot": f"{tp['trust_score']} from {tp['review_count']} reviews",
        "glassdoor": f"{gd['ratings']['overall']}, CEO approval {gd['ratings']['ceo_approval_pct']}%",
    }

print(brief("stripe.com", "Stripe", "stripe"))
