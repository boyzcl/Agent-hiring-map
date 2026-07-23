#!/usr/bin/env python3
"""Write a privacy-minimal weekly aggregate snapshot from explicit counts."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def nonnegative(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("count must be nonnegative")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--views", type=nonnegative, required=True)
    parser.add_argument("--unique-views", type=nonnegative, required=True)
    parser.add_argument("--clones", type=nonnegative, required=True)
    parser.add_argument("--unique-clones", type=nonnegative, required=True)
    parser.add_argument("--stars", type=nonnegative, required=True)
    parser.add_argument("--forks", type=nonnegative, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    snapshot_date = date.fromisoformat(args.date)
    if args.unique_views > args.views or args.unique_clones > args.clones:
        raise SystemExit("unique counts cannot exceed total counts")
    payload = {
        "schema_version": "agent-hiring-map-p4-aggregate-metrics/1.0",
        "snapshot_date": snapshot_date.isoformat(),
        "github_aggregate": {
            "views": args.views,
            "unique_views": args.unique_views,
            "clones": args.clones,
            "unique_clones": args.unique_clones,
            "stars": args.stars,
            "forks": args.forks,
        },
        "contains_personal_data": False,
        "contains_query_content": False,
        "counts_as_independent_usage_evidence": False,
        "network_requests": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "pass", "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

