# OliveSoft — n8n Workflow Orchestration

**CSTAM 3.0 Challenge:** CSTAM-OliveSoft — Automated RFP Intelligence & Commercial Proposal Generation System
**Phase 1 component — 10 / 100 points** (plus Phase 2 "Generative Presentation & Proposal Output" — 15 pts)

## Scope

Seamless orchestration using n8n to connect detection, research, RAG retrieval, and initial document generation.

### Responsibilities
- Wire together the 3 sibling services end-to-end via n8n workflows:
  1. `olivesoft-tender-detection` — new RFP detected → structured requirements
  2. `olivesoft-rag-retrieval` — structured requirements → matched OliveSoft assets (CVs/projects/tech)
  3. `olivesoft-prospect-research` — client name → client insights
  4. Merge outputs → generate initial commercial proposal/presentation draft (Phase 2 deliverable)
- Handle edge cases: incomplete tender specs, noisy research data, missing internal references (Phase 2, 5 pts)
- Export workflows as versioned JSON in `workflows/`

## Suggested stack
n8n (self-hosted via Docker), REST/webhook calls into the other 3 services.

## Status
🚧 Scaffolding — Phase 1 MVP in progress. Deadline: Oct 1, 2026.

## Related repos
- Hub: [olivesoft-rfp-intelligence](https://github.com/bilelkhlif/olivesoft-rfp-intelligence)
- [olivesoft-tender-detection](https://github.com/bilelkhlif/olivesoft-tender-detection)
- [olivesoft-rag-retrieval](https://github.com/bilelkhlif/olivesoft-rag-retrieval)
- [olivesoft-prospect-research](https://github.com/bilelkhlif/olivesoft-prospect-research)
