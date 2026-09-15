"""Reference orchestration logic for the OliveSoft RFP pipeline.

This script is Phase 1 scaffolding: it reads the JSON outputs already
produced by the 3 sibling services (tender-detection, rag-retrieval,
prospect-research) and merges them into a rough commercial proposal draft.

Upgrade path for n8n (10 pts) + Generative Presentation & Proposal Output
(15 pts, Phase 2): port each step below into an n8n workflow --
  1. Webhook/Cron trigger -> HTTP Request to tender-detection's API
  2. HTTP Request to rag-retrieval's API with the structured tender
  3. HTTP Request to prospect-research's API with the structured tender
  4. Merge node -> HTTP Request to an LLM (or Code node running this same
     merge logic) -> export as PPTX/PDF matching OliveSoft branding
Keep this script as the "ground truth" logic while workflows/*.json grows.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def render_proposal_markdown(tender: dict, matched: dict, insights: dict) -> str:
    lines = []
    lines.append(f"# Commercial Proposal Draft — {tender['title']}")
    lines.append("")
    lines.append(f"**Buyer:** {tender['buyer_name']} ({tender.get('buyer_country', 'N/A')})")
    lines.append(f"**Source:** {tender['source']} — [{tender['tender_id']}]({tender.get('source_url', '')})")
    lines.append(f"**Deadline:** {tender['deadline']}")
    lines.append(f"**Category:** {', '.join(tender.get('cpv_labels', [])) or 'N/A'}")
    lines.append("")
    lines.append("## Opportunity Summary")
    lines.append(tender.get("raw_description", "_No description available._"))
    lines.append("")
    lines.append(f"**Detected technical needs:** {', '.join(tender.get('required_tech', [])) or 'none detected'}")
    lines.append("")
    lines.append("## Client Insights")
    lines.append(f"**Sector:** {insights['industry_guess']}")
    lines.append("")
    for n in insights.get("notes", []):
        lines.append(f"- {n}")
    lines.append("")
    lines.append("## Why OliveSoft")
    for w in insights.get("why_olivesoft_can_help", []):
        lines.append(f"- {w}")
    lines.append("")
    lines.append("## Matched OliveSoft Capabilities")
    matches = matched.get("matches", [])
    if not matches:
        lines.append("_No strong internal matches found — needs manual sourcing._")
    for m in matches:
        lines.append(f"### {m['title']}  _(score: {m['score']}, type: {m['asset_type']})_")
        lines.append(m["snippet"])
        lines.append(f"Matched on: {', '.join(m['matched_terms'])}")
        lines.append("")
    lines.append("---")
    lines.append(f"_Generated {datetime.now(timezone.utc).isoformat()} — Phase 1 MVP draft, not reviewed by a human yet._")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge tender + matched assets + client insights into a proposal draft.")
    parser.add_argument("--tender", required=True)
    parser.add_argument("--matches", required=True)
    parser.add_argument("--insights", required=True)
    parser.add_argument("--out", required=True, help="Path to write the proposal Markdown.")
    args = parser.parse_args()

    tender = json.loads(Path(args.tender).read_text(encoding="utf-8"))
    matched = json.loads(Path(args.matches).read_text(encoding="utf-8"))
    insights = json.loads(Path(args.insights).read_text(encoding="utf-8"))

    proposal_md = render_proposal_markdown(tender, matched, insights)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(proposal_md, encoding="utf-8")

    print(f"Wrote proposal draft to {out_path}")


if __name__ == "__main__":
    main()
