"""
Ingest seed_data.py events into a Hindsight memory bank, then run
test queries to check retrieval/synthesis quality.

Usage (PowerShell):
    $env:HINDSIGHT_BASE_URL="https://api.hindsight.vectorize.io"
    $env:HINDSIGHT_API_KEY="your-api-key"
    python ingest_and_test.py

NOTE: retain/recall/reflect call signatures come from the official docs
(hindsight.vectorize.io/sdks/python) as of 2026-06-13, but haven't been
run end-to-end - treat first run as a debugging step, not guaranteed-working.
"""

import os
from datetime import datetime

from hindsight_client import Hindsight
from seed_data import events

from dotenv import load_dotenv
load_dotenv()

BANK_ID = "buildtrack-demo"

BASE_URL = os.environ.get("HINDSIGHT_BASE_URL", "http://localhost:8888")
API_KEY = os.environ.get("HINDSIGHT_API_KEY")


def get_client():
    kwargs = {"base_url": BASE_URL}
    if API_KEY:
        kwargs["api_key"] = API_KEY
    return Hindsight(**kwargs)


def ensure_bank(client):
    """Create the demo memory bank (mission shapes `reflect`, not `recall`)."""
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="BuildTrack Decision Memory",
            mission=(
                "I am the institutional memory for BuildTrack, a construction "
                "project management SaaS company. I track customer feedback, "
                "engineering estimates, roadmap decisions, and investor input "
                "so the team can understand why past decisions were made and "
                "who held which positions."
            ),
            disposition={
                "skepticism": 2,
                "literalism": 2,
                "empathy": 3,
            },
        )
        print(f"Created bank '{BANK_ID}'")
    except Exception as e:
        print(f"create_bank skipped (may already exist): {e}")


def ingest(client):
    """Retain all seed events as separate memories with metadata + timestamps."""
    items = []
    for i, e in enumerate(events):
        items.append({
            "content": e["content"],
            "context": e["context"],
            "timestamp": datetime.fromisoformat(e["date"]),
            "metadata": {**e["metadata"], "thread": e["thread"]},
            "document_id": f"buildtrack_seed_{i:03d}",
        })

    print(f"Retaining {len(items)} memories into bank '{BANK_ID}'...")
    client.retain_batch(
        bank_id=BANK_ID,
        items=items,
        retain_async=False,
    )
    print("Retain batch complete.")


def run_recall_test(client, query):
    print(f"\n--- RECALL: {query!r} ---")
    results = client.recall(bank_id=BANK_ID, query=query)
    if not results.results:
        print("  (no results)")
        return
    for r in results.results:
        print(f"  [{r.type}] {r.text}")


def run_reflect_test(client, query, context=None):
    print(f"\n--- REFLECT: {query!r} ---")
    answer = client.reflect(
        bank_id=BANK_ID,
        query=query,
        budget="mid",
        context=context,
    )
    print(answer.text)


def main():
    client = get_client()

    ensure_bank(client)
    ingest(client)

    test_queries = [
        "Why was dark mode postponed?",
        "What competing priorities existed when deciding on dark mode?",
        "Who might oppose prioritizing dark mode today, and why?",
        "Who would likely support revisiting dark mode today, and why?",
        "How have Sarah's opinions about dark mode vs. dashboard performance changed over time?",
    ]

    for q in test_queries:
        run_recall_test(client, q)
        run_reflect_test(client, q)

    client.close()


if __name__ == "__main__":
    main()