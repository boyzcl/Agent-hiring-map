#!/usr/bin/env python3
"""Validate an external suggestion into quarantine; never promotes canonical data."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


ALLOWED_FIELDS = {
    "schema_version",
    "change_type",
    "organization_name",
    "team_name",
    "product_name",
    "role_title",
    "geography",
    "official_source_url",
    "observed_at",
    "access_requirement",
    "agent_specific_excerpt",
    "replaces_role_id",
    "notes",
}
REQUIRED_FIELDS = {
    "schema_version",
    "change_type",
    "organization_name",
    "role_title",
    "geography",
    "official_source_url",
    "observed_at",
    "access_requirement",
    "agent_specific_excerpt",
}
CHANGE_TYPES = {"add", "correct", "close", "supersede", "duplicate", "ownership_dispute"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:password|passwd|token|api[_-]?key)\s*[:=]\s*\S+"),
]
PRIVATE_PATTERNS = [
    re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{8,}\d)(?!\d)"),
]
PROMPT_PATTERNS = [
    re.compile(r"(?i)ignore (?:all |the )?previous instructions"),
    re.compile(r"(?i)system prompt"),
    re.compile(r"(?i)执行(?:以下|这个)指令"),
    re.compile(r"(?i)忽略(?:之前|以上)"),
]


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    unknown = sorted(set(payload) - ALLOWED_FIELDS)
    missing = sorted(REQUIRED_FIELDS - set(payload))
    if unknown:
        errors.append("unknown_fields:" + ",".join(unknown))
    if missing:
        errors.append("missing_fields:" + ",".join(missing))
    if payload.get("schema_version") != "agent-hiring-map-submission/1.0":
        errors.append("invalid_schema_version")
    if payload.get("change_type") not in CHANGE_TYPES:
        errors.append("invalid_change_type")
    if payload.get("geography") not in {"China", "United States"}:
        errors.append("out_of_scope_geography")
    if payload.get("access_requirement") != "public_no_login":
        errors.append("restricted_access_not_allowed")
    try:
        observed = date.fromisoformat(str(payload.get("observed_at", "")))
        if observed > date.today():
            errors.append("future_observed_at")
    except ValueError:
        errors.append("invalid_observed_at")
    try:
        parts = urlsplit(str(payload.get("official_source_url", "")))
        if parts.scheme != "https" or not parts.netloc or parts.username or parts.password:
            errors.append("invalid_official_source_url")
    except ValueError:
        errors.append("invalid_official_source_url")
    for field in (
        "organization_name",
        "team_name",
        "product_name",
        "role_title",
        "agent_specific_excerpt",
        "notes",
    ):
        value = payload.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            errors.append(f"non_string:{field}")
            continue
        if value.startswith(("=", "+", "-", "@", "\t", "\r")):
            errors.append(f"formula_injection:{field}")
        if any(pattern.search(value) for pattern in SECRET_PATTERNS):
            errors.append(f"secret_detected:{field}")
        if any(pattern.search(value) for pattern in PRIVATE_PATTERNS):
            errors.append(f"private_contact_detected:{field}")
        if any(pattern.search(value) for pattern in PROMPT_PATTERNS):
            errors.append(f"prompt_injection_quarantine:{field}")
    excerpt = payload.get("agent_specific_excerpt", "")
    if not isinstance(excerpt, str) or not excerpt.strip() or len(excerpt) > 300:
        errors.append("invalid_excerpt_length")
    for field, limit in {
        "organization_name": 200,
        "team_name": 200,
        "product_name": 200,
        "role_title": 240,
        "notes": 300,
    }.items():
        value = payload.get(field)
        if isinstance(value, str) and len(value) > limit:
            errors.append(f"field_too_long:{field}")
    return sorted(set(errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.submission.read_text(encoding="utf-8"))
    errors = validate(payload)
    result = {
        "status": "accepted_to_quarantine" if not errors else "rejected_or_manual_hold",
        "errors": errors,
        "canonical_modified": False,
        "current_view_modified": False,
        "network_requests": 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()

