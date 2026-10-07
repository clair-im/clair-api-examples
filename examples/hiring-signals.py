# Daily diff of open roles on Greenhouse boards: which companies opened
# roles that signal a buying need. Keeps yesterday's job ids in seen.json.
import json, os, pathlib, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}
BOARDS = ["stripe", "airbnb", "figma"]
SIGNALS = ["data engineer", "revenue operations", "security engineer"]
STATE = pathlib.Path("seen.json")
seen = json.loads(STATE.read_text()) if STATE.exists() else {}

def jobs(board, q):
    r = requests.get(f"{API}/v1/greenhouse/jobs", headers=HEADERS, timeout=60,
                     params={"board": board, "q": q})
    r.raise_for_status()
    return r.json()["results"]

for board in BOARDS:
    before = set(seen.get(board, []))
    now = {}
    for q in SIGNALS:  # q matches the job title
        for job in jobs(board, q):
            now[job["id"]] = job
    for job_id in now.keys() - before:
        job = now[job_id]
        print(f"{job['company']}: {job['title']} ({job['location']}) {job['url']}")
    seen[board] = sorted(now)

STATE.write_text(json.dumps(seen, indent=2))
