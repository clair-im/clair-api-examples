# Enrich a list of company domains with the contacts they publish.
# In: domains.txt, one domain per line. Out: contacts.csv, one row per domain.
import csv, os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}

def lookup(domain):
    r = requests.get(f"{API}/v1/contacts", headers=HEADERS, timeout=90,
                     params={"domain": domain, "pages": 5})
    r.raise_for_status()
    return r.json()

def best_email(emails):
    # An address on the company's own domain first, role inboxes before people.
    ranked = sorted(emails, key=lambda e: (not e["domain_match"], e["type"] != "generic"))
    return ranked[0]["value"] if ranked else None

with open("domains.txt") as f:
    domains = [line.strip() for line in f if line.strip()]

with open("contacts.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["domain", "company", "email", "email_source", "phone",
                  "linkedin", "country"])
    for domain in domains:
        try:
            c = lookup(domain)
        except requests.HTTPError as e:
            print(domain, e.response.status_code, e.response.text[:200])
            continue
        email = best_email(c["emails"])
        source = next((e["sources"][0] for e in c["emails"] if e["value"] == email), None)
        linkedin = next((s["url"] for s in c["social"] if s["network"] == "linkedin"), None)
        company = c["company"] or {}
        out.writerow([domain, company.get("name"), email, source,
                      c["phones"][0]["e164"] if c["phones"] else None,
                      linkedin, company.get("country")])
