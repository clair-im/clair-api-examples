# Clair API examples

Runnable Python scripts for the [Clair](https://clair.im) data APIs: live Google Search, Maps and News, Reuters, Bloomberg and AP, Glassdoor, Indeed, Greenhouse, Amazon, Crunchbase, Trustpilot, Product Hunt and website contacts, as JSON, with one API key.

Each script solves one real task and is walked through, with recorded responses and monthly cost estimates, on the matching [use case page](https://clair.im/use-cases).

## Quickstart

```bash
git clone https://github.com/clair-im/clair-api-examples && cd clair-api-examples
pip install -r requirements.txt
export CLAIR_API_KEY=your_key   # free key: https://clair.im/dashboard/api-keys
python examples/serp-search.py
```

Every API has a free tier of 200 requests a month, no card. Docs: <https://clair.im/docs>. Base URL: `https://api.clair.im`, auth: `Authorization: Bearer <key>`.

## Examples

| Task | APIs | Script |
| --- | --- | --- |
| [Amazon price monitoring](https://clair.im/use-cases/amazon-price-monitoring) | Amazon | [`amazon-price-monitoring.py`](examples/amazon-price-monitoring.py) |
| [Google rank tracking](https://clair.im/use-cases/serp-search) | Google Search | [`serp-search.py`](examples/serp-search.py) |
| [Lead enrichment from company websites](https://clair.im/use-cases/website-contacts) | Website Contacts | [`website-contacts.py`](examples/website-contacts.py) |
| [Trustpilot review monitoring](https://clair.im/use-cases/review-intelligence) | Trustpilot | [`review-intelligence.py`](examples/review-intelligence.py) |
| [Product Hunt launch tracking](https://clair.im/use-cases/product-launches) | Product Hunt, Website Contacts | [`product-launches.py`](examples/product-launches.py) |
| [Local lead generation](https://clair.im/use-cases/local-lead-generation) | Google Maps, Website Contacts | [`local-lead-generation.py`](examples/local-lead-generation.py) |
| [Local SEO competitor audit](https://clair.im/use-cases/local-seo-audit) | Google Maps | [`local-seo-audit.py`](examples/local-seo-audit.py) |
| [Grounding LLM answers in search results](https://clair.im/use-cases/llm-grounding) | Google Search | [`llm-grounding.py`](examples/llm-grounding.py) |
| [Content research from People also ask](https://clair.im/use-cases/content-research) | Google Search | [`content-research.py`](examples/content-research.py) |
| [MAP enforcement on Amazon](https://clair.im/use-cases/map-enforcement) | Amazon | [`map-enforcement.py`](examples/map-enforcement.py) |
| [Amazon rating monitoring](https://clair.im/use-cases/amazon-rating-monitoring) | Amazon | [`amazon-rating-monitoring.py`](examples/amazon-rating-monitoring.py) |
| [Amazon category research](https://clair.im/use-cases/amazon-category-research) | Amazon | [`amazon-category-research.py`](examples/amazon-category-research.py) |
| [Trustpilot competitor benchmarking](https://clair.im/use-cases/trustpilot-benchmarking) | Trustpilot | [`trustpilot-benchmarking.py`](examples/trustpilot-benchmarking.py) |
| [Startup deal sourcing](https://clair.im/use-cases/deal-sourcing) | Product Hunt, Website Contacts, Crunchbase | [`deal-sourcing.py`](examples/deal-sourcing.py) |
| [Account research briefs](https://clair.im/use-cases/account-research) | Website Contacts, Crunchbase, Trustpilot, Glassdoor | [`account-research.py`](examples/account-research.py) |
| [Salary benchmarking](https://clair.im/use-cases/salary-benchmarking) | Glassdoor | [`salary-benchmarking.py`](examples/salary-benchmarking.py) |
| [Job market analytics](https://clair.im/use-cases/job-market-analytics) | Indeed | [`job-market-analytics.py`](examples/job-market-analytics.py) |
| [Hiring signals for sales](https://clair.im/use-cases/hiring-signals) | Greenhouse | [`hiring-signals.py`](examples/hiring-signals.py) |
| [Employer reputation tracking](https://clair.im/use-cases/employer-reputation) | Glassdoor | [`employer-reputation.py`](examples/employer-reputation.py) |
| [Media monitoring](https://clair.im/use-cases/media-monitoring) | Google News | [`media-monitoring.py`](examples/media-monitoring.py) |
| [Financial news tracking](https://clair.im/use-cases/financial-news-alerts) | Reuters, Associated Press, Bloomberg | [`financial-news-alerts.py`](examples/financial-news-alerts.py) |
| [News corpus for research and RAG](https://clair.im/use-cases/news-corpus) | Associated Press | [`news-corpus.py`](examples/news-corpus.py) |

## Notes

- Scripts read the key from `CLAIR_API_KEY`. Some take parameters (domains, keywords, ASINs) in constants at the top: edit them before running.
- Failed requests (5xx) are not charged. Check each use case page for cost and limits.
- OpenAPI 3.1 specs, one per API: <https://clair.im/openapi/google-search.json> (and the other APIs). Import them into Postman, Insomnia or a code generator.
- [Pricing](https://clair.im/pricing) · [Comparisons](https://clair.im/vs) · [Glossary](https://clair.im/glossary)

## License

MIT. The scripts are examples; the Clair API itself is covered by the [terms of service](https://clair.im/legal/terms).
