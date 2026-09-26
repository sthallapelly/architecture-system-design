# Architecture & System Design

A public architecture knowledge base covering system design, distributed systems, software architecture, cloud architecture, security, reliability, data platforms, and AI-enabled applications.

The repository focuses on architectural reasoning: understanding the problem, constraints, scale, failure modes, operational characteristics, and trade-offs behind a design rather than treating technologies as isolated building blocks.

## Structure

- `docs/fundamentals/` — system design fundamentals
- `docs/distributed-systems/` — distributed systems
- `docs/microservices/` — microservices architecture
- `docs/event-driven/` — event-driven architecture
- `docs/messaging/` — messaging systems
- `docs/databases/` — data and database architecture
- `docs/streaming/` — streaming systems
- `docs/caching/` — caching
- `docs/reliability/` — reliability and resilience
- `docs/security/` — security architecture
- `docs/multi-tenancy/` — multi-tenant architecture
- `docs/genai/` — GenAI architecture
- `docs/patterns/` — reusable architecture patterns
- `docs/problems/` — system-design scenarios
- `docs/deep-dives/` — long-form architecture discussions
- `docs/reference/` — architecture checklists, glossary, and reference material

## Content model

Topics generally examine the architectural problem, core concepts, design mechanics, appropriate use cases, failure scenarios, scale considerations, security and operational implications, alternatives, and trade-offs. Cloud services are mapped to these concepts where useful, while keeping the architectural reasoning technology-independent first.

Template files remain in the repository as authoring aids, but they are intentionally excluded from the public site navigation.

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open the local URL shown by MkDocs.

## GitHub Pages

The repository includes a GitHub Actions workflow in `.github/workflows/deploy.yml` that builds the MkDocs site and deploys it to GitHub Pages on pushes to `main`.

Public site: `https://sthallapelly.github.io/architecture-system-design/`
