#!/usr/bin/env python3
"""Generate an offline, deterministic TTL review queue. Performs no network access."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
TTL_DAYS = 14


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "current" / "current-opportunities.jsonl",
    )
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-batches", type=Path)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build(rows: list[dict], as_of: date) -> tuple[list[dict], dict]:
    queue = []
    urls: set[str] = set()
    domains: dict[str, int] = {}
    for row in rows:
        raw = row.get("last_verified_at")
        try:
            verified = date.fromisoformat(raw)
            age = (as_of - verified).days
        except (TypeError, ValueError):
            age = TTL_DAYS + 1
        if age < 0:
            reason, priority = "time_anomaly", "high"
        elif age > TTL_DAYS:
            reason, priority = "ttl_expired", "high"
        elif age == TTL_DAYS:
            reason, priority = "ttl_due_now", "high"
        elif age >= TTL_DAYS - 7:
            reason, priority = "ttl_due_within_7_days", "normal"
        else:
            continue
        source_urls = sorted(set(row.get("source_urls", [])))
        for url in source_urls:
            urls.add(url)
            domain = urlsplit(url).netloc.lower()
            domains[domain] = domains.get(domain, 0) + 1
        key = f"{row['role_id']}|{reason}|{as_of.isoformat()}"
        queue.append(
            {
                "schema_version": "agent-hiring-map-public/1.0",
                "queue_id": "REV-" + hashlib.sha256(key.encode()).hexdigest()[:16].upper(),
                "role_id": row["role_id"],
                "geography": row["geography"],
                "last_verified_at": raw,
                "as_of_date": as_of.isoformat(),
                "review_reason": reason,
                "priority": priority,
                "source_urls": source_urls,
                "access_requirement": row["access_requirement"],
                "trigger_recorded": True,
                "network_recheck_performed": False,
                "queue_status": "queued_offline",
            }
        )
    queue.sort(key=lambda item: (item["priority"] != "high", item["role_id"]))
    batches = {
        "schema_version": "agent-hiring-map-public/1.0",
        "as_of_date": as_of.isoformat(),
        "network_recheck_performed": False,
        "unique_url_count": len(urls),
        "unique_domain_count": len(domains),
        "urls": sorted(urls),
        "domains": [
            {"domain": domain, "queued_role_references": domains[domain]}
            for domain in sorted(domains)
        ],
    }
    return queue, batches


def main() -> None:
    args = parse_args()
    as_of = date.fromisoformat(args.as_of)
    queue, batches = build(load_jsonl(args.input), as_of)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for row in queue:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    if args.source_batches:
        args.source_batches.parent.mkdir(parents=True, exist_ok=True)
        args.source_batches.write_text(
            json.dumps(batches, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "status": "pass",
                "as_of_date": as_of.isoformat(),
                "queue_rows": len(queue),
                "unique_urls": batches["unique_url_count"],
                "unique_domains": batches["unique_domain_count"],
                "network_requests": 0,
                "formal_data_writes": 0,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

