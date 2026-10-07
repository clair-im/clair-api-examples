# Ground a model's answer in current Google results: search, keep the top
# results with their snippets, and pass them as numbered sources.
import os, requests

API = "https://api.clair.im"
HEADERS = {"Authorization": f"Bearer {os.environ['CLAIR_API_KEY']}"}

def google(q, country="us", language="en"):
    r = requests.get(f"{API}/v1/google-search", headers=HEADERS, timeout=60, params={
        "q": q, "country": country, "language": language})
    r.raise_for_status()
    return r.json()

def sources_for(question, k=6):
    body = google(question)
    lines = []
    if body.get("knowledge_graph"):
        kg = body["knowledge_graph"]
        lines.append(f"[0] {kg['title']} ({kg['type']}): {kg['description']}")
    for r in body["results"][:k]:
        date = f" ({r['date']})" if r["date"] else ""
        lines.append(f"[{r['position']}] {r['title']}{date}\n{r['url']}\n{r['snippet']}")
    return "\n\n".join(lines)

question = "What changed in the EU AI Act this year?"
prompt = (
    "Answer using only the sources below, and cite them by number. "
    "Say so if they do not answer the question.\n\n"
    f"Sources:\n{sources_for(question)}\n\nQuestion: {question}"
)
print(prompt)  # send to the model of your choice
