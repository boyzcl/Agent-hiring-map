#!/usr/bin/env python3
"""Generate the offline deterministic TTL and data-quality review queue.

The script performs no network access and makes no formal data changes.  It
queues only triggers; a reviewer must later inspect the frozen, deduplicated
public sources.
"""

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
        dest="current_input",
        type=Path,
        default=ROOT / "data" / "current" / "current-opportunities.jsonl",
        help="backward-compatible alias for --current-input",
    )
    parser.add_argument(
        "--roles-input",
        type=Path,
        default=ROOT / "data" / "map" / "roles.jsonl",
    )
    parser.add_argument(
        "--teams-input",
        type=Path,
        default=ROOT / "data" / "map" / "teams.jsonl",
    )
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-batches", type=Path)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def queue_item(
    role_id: str,
    geography: str,
    last_verified_at: str | None,
    as_of: date,
    reason: str,
    priority: str,
    source_urls: list[str],
    access_requirement: str,
) -> dict:
    key = f"{role_id}|{reason}|{as_of.isoformat()}"
    return {
        "schema_version": "agent-hiring-map-public/1.0",
        "queue_id": "REV-" + hashlib.sha256(key.encode()).hexdigest()[:16].upper(),
        "role_id": role_id,
        "geography": geography,
        "last_verified_at": last_verified_at,
        "as_of_date": as_of.isoformat(),
        "review_reason": reason,
        "priority": priority,
        "source_urls": sorted(set(source_urls)),
        "access_requirement": access_requirement,
        "trigger_recorded": True,
        "network_recheck_performed": False,
        "queue_status": "queued_offline",
    }


def build(
    current_rows: list[dict],
    role_rows: list[dict],
    team_rows: list[dict],
    as_of: date,
) -> tuple[list[dict], dict]:
    queue = []
    urls: set[str] = set()
    domains: dict[str, set[str]] = {}
    current_by_id = {row["role_id"]: row for row in current_rows}
    team_geographies = {
        row["team_id"]: row.get("team_geography") or [] for row in team_rows
    }
    for row in current_rows:
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
            domains.setdefault(domain, set()).add(row["role_id"])
        queue.append(
            queue_item(
                row["role_id"],
                row["geography"],
                raw,
                as_of,
                reason,
                priority,
                source_urls,
                row["access_requirement"],
            )
        )
    for role in role_rows:
        current = current_by_id.get(role["role_id"])
        team_values = team_geographies.get(role.get("team_id"), [])
        geography = current["geography"] if current else (
            team_values[0] if len(team_values) == 1 else "United States"
        )
        triggers: list[tuple[str, str]] = []
        if role.get("public_confidence_tier") == "probable":
            triggers.append(("probable_role_followup", "high"))
        if role.get("location_data_status") == "pending_review":
            triggers.append(("location_data_pending_review", "normal"))
        elif role.get("location_data_status") == "company_or_context_only":
            triggers.append(("location_company_or_context_only", "normal"))
        if role.get("currentness_status") in {
            "stale_unverified",
            "unknown",
            "historical_closed_or_offline",
        }:
            triggers.append(("currentness_revalidation_needed", "normal"))
        source_urls = [role["official_role_url"]] if role.get("official_role_url") else []
        for reason, priority in triggers:
            queue.append(
                queue_item(
                    role["role_id"],
                    geography,
                    role.get("last_verified_at"),
                    as_of,
                    reason,
                    priority,
                    source_urls,
                    role.get("access_requirement") or "public_no_login",
                )
            )
    unique = {row["queue_id"]: row for row in queue}
    queue = list(unique.values())
    urls.clear()
    domains.clear()
    for row in queue:
        for url in row["source_urls"]:
            urls.add(url)
            domain = urlsplit(url).netloc.lower()
            domains.setdefault(domain, set()).add(row["role_id"])
    queue.sort(
        key=lambda item: (
            item["priority"] != "high",
            item["role_id"],
            item["review_reason"],
        )
    )
    batches = {
        "schema_version": "agent-hiring-map-public/1.0",
        "as_of_date": as_of.isoformat(),
        "network_recheck_performed": False,
        "unique_url_count": len(urls),
        "unique_domain_count": len(domains),
        "urls": sorted(urls),
        "domains": [
            {"domain": domain, "queued_role_references": len(domains[domain])}
            for domain in sorted(domains)
        ],
    }
    return queue, batches


def main() -> None:
    args = parse_args()
    as_of = date.fromisoformat(args.as_of)
    queue, batches = build(
        load_jsonl(args.current_input),
        load_jsonl(args.roles_input),
        load_jsonl(args.teams_input),
        as_of,
    )
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
