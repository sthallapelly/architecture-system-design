# Architecture & System Design

A practical, continuously evolving knowledge base for system design, distributed systems, software architecture, and cloud architecture.

The goal is to build architecture reasoning skills—not just memorize technologies or interview answers.

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
- `docs/problems/` — system-design problems
- `docs/deep-dives/` — selected long-form architecture articles

## Learning method

Each topic follows a repeatable model:

1. Problem
2. Concept
3. Why it matters
4. How it works
5. When to use it
6. When not to use it
7. Architecture
8. Failure scenarios
9. Scale considerations
10. Trade-offs
11. AWS/cloud mapping
12. Interview questions
13. Design problem
14. Key takeaways
15. References

The repository is intentionally technology-independent first. Cloud services are mapped after the architectural reasoning is established.

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open the local URL shown by MkDocs.

## GitHub Pages

The repository includes a GitHub Actions workflow in `.github/workflows/deploy.yml`.

After pushing the repository to GitHub:

1. Open **Settings → Pages**.
2. Set the source to **GitHub Actions**.
3. Push changes to `main`.
4. The workflow builds and deploys the documentation.

## Status

This is the starter structure. Content will be added progressively as the learning program advances.
