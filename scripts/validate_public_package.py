#!/usr/bin/env python3
"""Validate the public package using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import ipaddress
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from validate_submission import validate as validate_submission


ROOT = Path(__file__).resolve().parents[1]
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:password|passwd|token|api[_-]?key)\s*[:=]\s*[^\s,;]+"),
]
PRIVATE_PATTERNS = [
    re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
]
ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9.:])/Users/[^/\s]+/"),
    re.compile(r"(?<![A-Za-z0-9.:])/home/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\"),
]
ROLE_DISPLAY_VERSION = "agent-hiring-map-role-display/1.0"
TITLE_AUTHENTICITY_VERSION = "agent-hiring-map-title-authenticity/1.0"
VERIFIED_TITLE_STATUSES = {
    "verified_official_title",
    "verified_official_listing",
}
CURRENT_TITLE_GRANULARITIES = {
    "direct_role_detail",
    "stable_official_listing_locator",
}
LOCATION_STATUSES = {
    "normalized_or_descriptive",
    "official_role_title_location_reviewed",
    "company_or_context_only",
    "pending_review",
}
WORK_ARRANGEMENTS = {"onsite", "remote_or_hybrid"}
WORK_ARRANGEMENT_BASES = {
    "explicit_remote_or_hybrid",
    "explicit_onsite",
    "default_onsite_no_remote_signal",
}
PUBLIC_CONFIDENCE_TIERS = {"verified", "probable"}
TRACKING_KEYS = {"fbclid", "gclid", "ref", "source"}
NONCANONICAL_NUMERIC_HOST_RE = re.compile(
    r"^(?:0[xX][0-9a-fA-F]+|[0-9]+)(?:\.(?:0[xX][0-9a-fA-F]+|[0-9]+))*$"
)
LOCATION_RESIDUE_ZH = re.compile(
    r"(?i)(?:"
    r"\b(?:current|roles?|job|remote|hybrid|onsite|on-site|full-time|"
    r"social|campus|preferred|candidates?|work|office|team|exact|"
    r"location|listing|context|requirement|headquarters)\b|"
    r"岗位|职位|角色|当前|招聘|截止|招满|公告|长期|实习|全日制|全职|"
    r"兼职|现场|驻场|偏僻的|动力|优先|候选人|工作授权|营业时间|"
    r"每季度|办公室|总部|通知|未解决"
    r")"
)
LOCATION_RESIDUE_EN = re.compile(
    r"(?i)(?:"
    r"\b(?:current|roles?|job|remote|hybrid|onsite|on-site|full-time|"
    r"part-time|social|campus|preferred|candidates?|work|"
    r"office|team|exact|listing|context|requirement|headquarters|"
    r"recruitment|recruited|hiring|opening|internship|expired|deadline|"
    r"valid until|until filled|notice|unresolved)\b|"
    r"[\u4e00-\u9fff]"
    r")"
)
DATASET_SPECS = {
    "data/evidence/evidence-ledger-safe": None,
    "data/map/organizations": None,
    "data/map/teams": None,
    "data/map/products": None,
    "data/map/roles": None,
    "data/map/relations": None,
    "data/current/current-opportunities": None,
    "data/review/review-queue": None,
}
REQUIRED_FILES = [
    ".nojekyll",
    "index.html",
    "assets/app.js",
    "assets/styles.css",
    "assets/icons/chevron-down.svg",
    "README.md",
    "LICENSE-CODE",
    "LICENSE-DATA",
    "NOTICE",
    "SECURITY.md",
    "docs/AUTHORITY.md",
    "docs/DATA_SCALE_AND_SCOPE.md",
    "docs/DATA_DICTIONARY.md",
    "docs/CONTRIBUTING.md",
    "docs/MAINTENANCE.md",
    "docs/METHODOLOGY.md",
    "docs/OBSERVATION.md",
    "docs/CHANGELOG.md",
    "docs/TEAM_ROLE_OVERVIEW.md",
    "docs/PROBABLE_ROLE_UPGRADE.md",
    "schemas/evidence-safe.schema.json",
    "schemas/current-opportunity.schema.json",
    "schemas/submission.schema.json",
    "schemas/review-queue-item.schema.json",
    "scripts/build_review_queue.py",
    "scripts/build_team_role_overview.py",
    "scripts/build_manifest.py",
    "scripts/validate_submission.py",
    ".github/workflows/validate.yml",
    ".github/workflows/weekly-review.yml",
    "data/metadata/release-metadata.json",
    "data/metadata/global-recovery-summary.json",
    "data/metadata/release-delta.json",
    "data/review/source-batches.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_value(raw: str, reference: Any) -> Any:
    if isinstance(reference, (list, dict)) or reference is None:
        return json.loads(raw)
    if isinstance(reference, bool):
        return raw == "true"
    if isinstance(reference, int):
        return int(raw)
    if isinstance(reference, float):
        return float(raw)
    return raw


def parity_errors(stem: str) -> list[str]:
    csv_rows = load_csv(ROOT / f"{stem}.csv")
    json_rows = load_jsonl(ROOT / f"{stem}.jsonl")
    errors: list[str] = []
    if len(csv_rows) != len(json_rows):
        return [f"{stem}:csv_jsonl_row_count_mismatch"]
    for index, (csv_row, json_row) in enumerate(zip(csv_rows, json_rows), start=1):
        if list(csv_row) != list(json_row):
            errors.append(f"{stem}:field_order_mismatch:{index}")
            break
        converted = {key: csv_value(csv_row[key], json_row[key]) for key in csv_row}
        if converted != json_row:
            errors.append(f"{stem}:csv_jsonl_value_mismatch:{index}")
            break
    return errors


def valid_public_url(value: str) -> bool:
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError:
        return False
    host = (parts.hostname or "").casefold().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is None and NONCANONICAL_NUMERIC_HOST_RE.fullmatch(host):
        return False
    return (
        parts.scheme in {"http", "https"}
        and bool(parts.netloc)
        and parts.username is None
        and parts.password is None
        and (address is None or address.is_global)
    )


def normalize_url_for_projection(value: object) -> str:
    """Mirror the release builder's public URL canonicalization."""

    try:
        parsed = urlsplit(str(value or "").strip())
        if not valid_public_url(str(value or "")):
            return ""
        host = parsed.hostname.casefold().rstrip(".")
        query = [
            (key, val)
            for key, val in parse_qsl(parsed.query, keep_blank_values=True)
            if key.casefold() not in TRACKING_KEYS
            and not key.casefold().startswith("utm_")
        ]
        fragment = parsed.fragment.strip()
        moka_job = re.fullmatch(r"/?job/[A-Za-z0-9._:-]{8,240}", fragment)
        trip_job = (
            parsed.scheme == "https"
            and parsed.hostname.casefold() == "careers.ctrip.com"
            and parsed.port is None
            and (parsed.path or "/") == "/index.html"
            and not parsed.query
            and re.fullmatch(r"/?experienced/job-detail/MJ[0-9]+", fragment)
        )
        if not (moka_job or trip_job):
            fragment = ""
        elif not fragment.startswith("/"):
            fragment = "/" + fragment
        path = re.sub(r"/+", "/", parsed.path)
        path = (path or "/") if fragment else (path.rstrip("/") or "/")
        port = f":{parsed.port}" if parsed.port else ""
        return urlunsplit(
            ("https", f"{host}{port}", path, urlencode(sorted(query)), fragment)
        )
    except (TypeError, ValueError):
        return ""


def filesystem_structure_errors() -> list[str]:
    errors: list[str] = []
    if ROOT.is_symlink():
        errors.append("public_root_symlink_forbidden")
        return errors
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"symlink_forbidden:{relative}")
        if relative == "metrics-private" or relative.startswith("metrics-private/"):
            errors.append(f"private_metrics_forbidden:{relative}")
    return errors


def scan_text_safety() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in {".md", ".json", ".jsonl", ".csv", ".py", ".yml", ".yaml", ""}:
            continue
        text = path.read_text(encoding="utf-8")
        detector_sources = {
            "scripts/validate_public_package.py",
            "scripts/validate_submission.py",
        }
        if relative not in detector_sources and any(
            pattern.search(text) for pattern in SECRET_PATTERNS
        ):
            errors.append(f"secret_pattern:{relative}")
        if relative.startswith("data/") and any(pattern.search(text) for pattern in PRIVATE_PATTERNS):
            errors.append(f"private_contact_pattern:{relative}")
        if relative not in detector_sources and any(
            pattern.search(text) for pattern in ABSOLUTE_PATH_PATTERNS
        ):
            errors.append(f"absolute_path:{relative}")
        lower = text.lower()
        if relative not in detector_sources and any(
            token in lower
            for token in (
                "google-analytics.com",
                "googletagmanager.com",
                "api.segment.io",
                "posthog.capture",
                "mixpanel.track",
            )
        ):
            errors.append(f"telemetry_detected:{relative}")
    return errors


def scan_csv_formula() -> list[str]:
    errors: list[str] = []
    for path in sorted((ROOT / "data").rglob("*.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for line_number, row in enumerate(csv.reader(handle), start=1):
                if line_number == 1:
                    continue
                for value in row:
                    if value.startswith(FORMULA_PREFIXES):
                        errors.append(
                            f"formula_injection:{path.relative_to(ROOT).as_posix()}:{line_number}"
                        )
                        return errors
    return errors


def evidence_errors(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(rows) < 7217:
        errors.append("evidence_below_sealed_historical_baseline")
    expected_ids = [f"AMC-{index:04d}" for index in range(1, len(rows) + 1)]
    actual_ids = [row.get("evidence_id") for row in rows]
    if actual_ids != expected_ids:
        errors.append("evidence_ids_not_unique_continuous")
    forbidden = {"batch", "c0_status", "c1_status", "c2_status", "c3_status", "c4_status", "next_action", "notes", "dedupe_key"}
    for row in rows:
        if forbidden.intersection(row):
            errors.append("evidence_internal_field_leak")
            break
        geography = row.get("geography_bucket")
        scope = row.get("coverage_scope")
        expected_scope = (
            "canonical_map_scope"
            if geography in {"China", "United States"}
            else "evidence_index_only"
        )
        if scope != expected_scope:
            errors.append(f"evidence_scope_error:{row.get('evidence_id')}")
        urls = row.get("source_urls")
        if not isinstance(urls, list) or any(not valid_public_url(url) for url in urls):
            errors.append(f"evidence_url_error:{row.get('evidence_id')}")
        if not row.get("access_requirement"):
            errors.append(f"evidence_missing_access:{row.get('evidence_id')}")
        excerpt = row.get("public_excerpt", "")
        if excerpt and (not urls or len(excerpt) > 300):
            errors.append(f"evidence_excerpt_error:{row.get('evidence_id')}")
    return errors


def current_errors(
    rows: list[dict[str, Any]], metadata: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    as_of = date.fromisoformat(metadata["release_as_of"])
    for row in rows:
        role_id = row.get("role_id", "missing")
        geography = row.get("geography")
        if (
            not isinstance(geography, str)
            or not geography.strip()
            or len(geography) > 80
        ):
            errors.append(f"current_invalid_geography:{role_id}")
        if row.get("currentness_status") not in {"current_verified", "current_probable"}:
            errors.append(f"current_invalid_status:{role_id}")
        if row.get("access_requirement") != "public_no_login":
            errors.append(f"current_restricted_access:{role_id}")
        if row.get("title_support_status") not in VERIFIED_TITLE_STATUSES:
            errors.append(f"current_unverified_title:{role_id}")
        if row.get("title_source_granularity") not in CURRENT_TITLE_GRANULARITIES:
            errors.append(f"current_weak_title_source:{role_id}")
        if row.get("citation_supports_title") is not True:
            errors.append(f"current_unsupported_title:{role_id}")
        if not row.get("title") or not row.get("display_title_zh") or not row.get(
            "display_title_en"
        ):
            errors.append(f"current_missing_title:{role_id}")
        if not valid_public_url(str(row.get("title_source_url") or "")):
            errors.append(f"current_invalid_title_source:{role_id}")
        try:
            verified = date.fromisoformat(row["last_verified_at"])
            age = (as_of - verified).days
            if age < 0:
                errors.append(f"current_future_verified:{role_id}")
            if age > 14:
                errors.append(f"current_ttl_expired:{role_id}")
        except (KeyError, TypeError, ValueError):
            errors.append(f"current_invalid_verified_at:{role_id}")
        if not row.get("source_urls") or any(
            not valid_public_url(url) for url in row.get("source_urls", [])
        ):
            errors.append(f"current_source_error:{role_id}")
        if not row.get("agent_specific_excerpt") or len(row["agent_specific_excerpt"]) > 300:
            errors.append(f"current_excerpt_error:{role_id}")
        if row.get("evidence_grade") not in {"A", "B", "C"}:
            errors.append(f"current_grade_error:{role_id}")
        if not row.get("evidence_ids"):
            errors.append(f"current_missing_evidence:{role_id}")
    declared = metadata["current_opportunities"]["rows"]
    if len(rows) != declared:
        errors.append("current_metadata_count_mismatch")
    return errors


def map_errors(datasets: dict[str, list[dict[str, Any]]], evidence_ids: set[str]) -> list[str]:
    errors: list[str] = []
    ids: dict[str, set[str]] = {
        "organizations": {row["organization_id"] for row in datasets["organizations"]},
        "teams": {row["team_id"] for row in datasets["teams"]},
        "products": {row["product_id"] for row in datasets["products"]},
        "roles": {row["role_id"] for row in datasets["roles"]},
    }
    all_object_ids = set().union(*ids.values())
    for name in ("organizations", "teams", "products", "roles", "relations"):
        for row in datasets[name]:
            refs = row.get("evidence_ids")
            if not refs or any(ref not in evidence_ids for ref in refs):
                errors.append(f"map_provenance_error:{name}")
                break
    for row in datasets["teams"]:
        if row["organization_id"] not in ids["organizations"]:
            errors.append(f"team_organization_missing:{row['team_id']}")
    for row in datasets["products"]:
        if row["organization_id"] not in ids["organizations"]:
            errors.append(f"product_organization_missing:{row['product_id']}")
    for row in datasets["roles"]:
        if row["organization_id"] not in ids["organizations"]:
            errors.append(f"role_organization_missing:{row['role_id']}")
        if row.get("team_id") and row["team_id"] not in ids["teams"]:
            errors.append(f"role_team_missing:{row['role_id']}")
        if row.get("product_id") and row["product_id"] not in ids["products"]:
            errors.append(f"role_product_missing:{row['role_id']}")
    for row in datasets["relations"]:
        if row["subject_id"] not in all_object_ids or row["object_id"] not in all_object_ids:
            errors.append(f"relation_endpoint_missing:{row['relation_id']}")
            if len(errors) > 100:
                break
    return errors


def role_display_errors(
    roles: list[dict[str, Any]], metadata: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    arrangement_counts: dict[str, int] = {}
    basis_counts: dict[str, int] = {}
    location_counts: dict[str, int] = {}
    title_status_counts: dict[str, int] = {}
    confidence_counts: dict[str, int] = {}
    origin_counts: dict[str, int] = {}
    required_text = (
        "display_title_zh",
        "display_title_en",
        "display_location_zh",
        "display_location_en",
    )
    for role in roles:
        role_id = role.get("role_id", "missing")
        if role.get("role_display_version") != ROLE_DISPLAY_VERSION:
            errors.append(f"role_display_version:{role_id}")
        if role.get("title_authenticity_version") != TITLE_AUTHENTICITY_VERSION:
            errors.append(f"role_title_authenticity_version:{role_id}")
        title_status = role.get("title_support_status")
        title_status_counts[title_status] = title_status_counts.get(
            title_status, 0
        ) + 1
        confidence_tier = role.get("public_confidence_tier")
        if confidence_tier not in PUBLIC_CONFIDENCE_TIERS:
            errors.append(f"role_confidence_tier:{role_id}")
        else:
            confidence_counts[confidence_tier] = (
                confidence_counts.get(confidence_tier, 0) + 1
            )
        origin = role.get("recovery_origin")
        if origin not in {
            "existing_role_revalidated",
            "unlinked_evidence_recovered",
            "global_deferred_evidence_recovered",
            "continuous_new_role_discovery",
        }:
            errors.append(f"role_recovery_origin:{role_id}")
        else:
            origin_counts[origin] = origin_counts.get(origin, 0) + 1
        if role.get("public_disposition") == "publish_current":
            try:
                verified = date.fromisoformat(str(role["last_verified_at"]))
                next_check = datetime.fromisoformat(
                    str(role["currentness_next_check_at"]).replace("Z", "+00:00")
                )
                if next_check.tzinfo is None:
                    raise ValueError("timezone required")
                next_check = next_check.astimezone(timezone.utc)
                ttl_days = (next_check.date() - verified).days
                if ttl_days < 1 or ttl_days > 14:
                    errors.append(f"role_currentness_ttl_out_of_bounds:{role_id}")
            except (KeyError, TypeError, ValueError):
                errors.append(f"role_currentness_next_check_invalid:{role_id}")
        if confidence_tier == "probable" and (
            role.get("eligible_for_strict_current") is not False
            or role.get("title_current_eligible_after_gate") is not False
        ):
            errors.append(f"probable_role_current_pollution:{role_id}")
        if role.get("title_provenance") == "role_family":
            errors.append(f"role_family_used_as_title:{role_id}")
        if title_status in VERIFIED_TITLE_STATUSES:
            if (
                not role.get("official_title_raw")
                or role.get("title") != role.get("official_title_raw")
                or role.get("citation_supports_title") is not True
                or not valid_public_url(str(role.get("title_source_url") or ""))
                or not role.get("title_source_observed_at")
            ):
                errors.append(f"role_verified_title_incomplete:{role_id}")
        else:
            if role.get("official_title_raw") is not None or role.get("title") is not None:
                errors.append(f"role_unverified_title_published:{role_id}")
            if role_id not in role.get("display_title_zh", ""):
                errors.append(f"role_pending_title_not_traceable:{role_id}")
        if any(
            not isinstance(role.get(field), str) or not role.get(field).strip()
            for field in required_text
        ):
            errors.append(f"role_display_missing_bilingual_text:{role_id}")
        if (
            re.search(r"[\u4e00-\u9fff]", role.get("display_title_en", ""))
            or "官方中文原名" in role.get("display_title_en", "")
            or "官方英文原名" in role.get("display_title_zh", "")
            or role.get("display_title_en", "").startswith("Agent-related role")
        ):
            errors.append(f"role_title_language_fallback:{role_id}")
        arrangement = role.get("work_arrangement")
        basis = role.get("work_arrangement_basis")
        location_status = role.get("location_data_status")
        if arrangement not in WORK_ARRANGEMENTS:
            errors.append(f"role_work_arrangement:{role_id}")
        else:
            arrangement_counts[arrangement] = arrangement_counts.get(arrangement, 0) + 1
        if basis not in WORK_ARRANGEMENT_BASES:
            errors.append(f"role_work_arrangement_basis:{role_id}")
        else:
            basis_counts[basis] = basis_counts.get(basis, 0) + 1
        if (
            arrangement == "remote_or_hybrid"
            and basis != "explicit_remote_or_hybrid"
        ):
            errors.append(f"role_remote_basis_mismatch:{role_id}")
        if (
            arrangement == "onsite"
            and basis not in {"explicit_onsite", "default_onsite_no_remote_signal"}
        ):
            errors.append(f"role_onsite_basis_mismatch:{role_id}")
        if location_status not in LOCATION_STATUSES:
            errors.append(f"role_location_status:{role_id}")
            continue
        location_counts[location_status] = location_counts.get(location_status, 0) + 1
        locations = role.get("job_locations")
        if not isinstance(locations, list):
            errors.append(f"role_job_locations_not_list:{role_id}")
        elif location_status in {
            "normalized_or_descriptive",
            "official_role_title_location_reviewed",
        }:
            if locations != [role.get("display_location_en")]:
                errors.append(f"role_job_location_display_mismatch:{role_id}")
            if (
                LOCATION_RESIDUE_ZH.search(role.get("display_location_zh", ""))
                or LOCATION_RESIDUE_EN.search(role.get("display_location_en", ""))
                or "，，" in role.get("display_location_zh", "")
                or re.search(r"[A-Za-z]{3,}", role.get("display_location_zh", ""))
            ):
                errors.append(f"role_location_residue:{role_id}")
        elif locations:
            errors.append(f"role_unverified_location_published:{role_id}")
        if location_status == "pending_review" and (
            role.get("display_location_zh") != "地点待复核"
            or role.get("display_location_en") != "Location pending review"
        ):
            errors.append(f"role_pending_location_label:{role_id}")
        if location_status == "company_or_context_only" and (
            role.get("display_location_zh")
            != "岗位地点待复核（来源仅列出公司或团队地点）"
            or role.get("display_location_en")
            != "Role location pending review (source only lists company or team locations)"
        ):
            errors.append(f"role_context_location_label:{role_id}")

    display_metadata = metadata.get("role_display", {})
    if display_metadata.get("version") != ROLE_DISPLAY_VERSION:
        errors.append("role_display_metadata_version")
    if display_metadata.get("languages") != ["zh", "en"]:
        errors.append("role_display_metadata_languages")
    if display_metadata.get("work_arrangement") != dict(sorted(arrangement_counts.items())):
        errors.append("role_display_metadata_arrangement_counts")
    if display_metadata.get("work_arrangement_basis") != dict(sorted(basis_counts.items())):
        errors.append("role_display_metadata_basis_counts")
    if display_metadata.get("location_data_status") != dict(sorted(location_counts.items())):
        errors.append("role_display_metadata_location_counts")
    if (
        display_metadata.get("default_rule")
        != "roles without explicit remote or hybrid signals are classified as onsite"
    ):
        errors.append("role_display_metadata_default_rule")
    title_metadata = metadata.get("title_authenticity", {})
    if title_metadata.get("version") != TITLE_AUTHENTICITY_VERSION:
        errors.append("title_authenticity_metadata_version")
    if title_metadata.get("roles_audited") != len(roles):
        errors.append("title_authenticity_metadata_role_count")
    if title_metadata.get("status") != dict(sorted(title_status_counts.items())):
        errors.append("title_authenticity_metadata_status_counts")
    if title_metadata.get("role_family_used_as_title_fallback") != 0:
        errors.append("title_authenticity_role_family_fallback")
    recovery_metadata = metadata.get("recovery", {})
    if recovery_metadata.get("version") != "agent-hiring-map-global-evidence-recovery/1.0":
        errors.append("recovery_metadata_version")
    if recovery_metadata.get("existing_roles_audited") != 1148:
        errors.append("recovery_existing_audit_count")
    if recovery_metadata.get("existing_roles_accepted_before_public_dedupe") != 703:
        errors.append("recovery_existing_pre_dedupe_count")
    if recovery_metadata.get("existing_roles_retained") != 701:
        errors.append("recovery_existing_retained_count")
    if recovery_metadata.get("existing_records_demoted_to_leads") != 445:
        errors.append("recovery_demoted_lead_count")
    if recovery_metadata.get("new_probable_roles") != 172:
        errors.append("recovery_new_role_count")
    if recovery_metadata.get("duplicate_role_records_suppressed") != 2:
        errors.append("recovery_duplicate_suppression_count")
    if recovery_metadata.get("public_role_records") != len(roles):
        errors.append("recovery_public_role_count")
    if recovery_metadata.get("public_confidence_tier") != dict(
        sorted(confidence_counts.items())
    ):
        errors.append("recovery_confidence_counts")
    historical_origin_counts = {
        key: origin_counts.get(key, 0)
        for key in (
            "existing_role_revalidated",
            "global_deferred_evidence_recovered",
            "unlinked_evidence_recovered",
        )
    }
    if historical_origin_counts != {
        "existing_role_revalidated": 701,
        "global_deferred_evidence_recovered": 347,
        "unlinked_evidence_recovered": 265,
    }:
        errors.append("recovery_origin_counts")
    incremental_count = origin_counts.get("continuous_new_role_discovery", 0)
    if recovery_metadata.get("continuous_new_role_discovery_roles", 0) != incremental_count:
        errors.append("recovery_incremental_role_count")
    if recovery_metadata.get("historical_public_role_records", 1313) != 1313:
        errors.append("recovery_historical_role_count")
    if recovery_metadata.get("new_roles_admitted_to_strict_current") != 91:
        errors.append("recovery_new_role_current_pollution")
    if recovery_metadata.get("global_new_current_opportunities") != 345:
        errors.append("recovery_global_current_count")
    upgrade_metadata = metadata.get("probable_role_upgrade", {})
    if upgrade_metadata != {
        "version": "agent-hiring-map-probable-role-upgrade/1.0",
        "frozen_roles": 95,
        "verified_and_current": 91,
        "retained_probable": 1,
        "source_changed_or_closed": 1,
        "agent_relevance_insufficient_removed": 2,
        "title_or_url_mismatches": 0,
        "wrong_cross_group_merges": 0,
        "full_descriptions_persisted": 0,
    }:
        errors.append("probable_role_upgrade_metadata")

    beisen = [
        role
        for role in roles
        if "ed135f65-0e42-47ac-8c1d-abc76940cfb3"
        in str(role.get("official_role_url") or "")
    ]
    if len(beisen) != 1:
        errors.append("beisen_j14460_missing_or_duplicate")
    else:
        role = beisen[0]
        if (
            role.get("display_title_zh")
            != "高级产品经理（AI人才发展方向）（PBG / 北京）（J14460）"
            or role.get("display_title_en")
            != "Senior Product Manager, AI Talent Development (PBG / Beijing) (J14460)"
            or role.get("display_location_zh") != "北京"
            or role.get("display_location_en") != "Beijing"
            or role.get("work_arrangement") != "onsite"
            or role.get("work_arrangement_basis")
            != "default_onsite_no_remote_signal"
        ):
            errors.append("beisen_j14460_display_regression")
    smart_drug = [
        role
        for role in roles
        if role.get("role_id") == "ROLE-B0A80F962CFE85AD"
    ]
    if len(smart_drug) != 1:
        errors.append("smart_drug_role_missing")
    else:
        role = smart_drug[0]
        if (
            role.get("official_title_raw") != "智慧药物平台实验技术岗位"
            or role.get("display_title_en")
            != "Smart Drug Platform Laboratory Technical Role"
            or "rsc.bjmu.edu.cn/rczp/jfxz/"
            not in str(role.get("official_role_url") or "")
        ):
            errors.append("smart_drug_role_regression")
    serialized_titles = "\n".join(
        str(role.get("official_title_raw") or "") for role in roles
    )
    for forbidden_title in (
        "工业智能体技术项目",
        "经营规划、记忆评估",
        "科学平台智能体系统工程师",
    ):
        if forbidden_title in serialized_titles:
            errors.append(f"known_false_title_reintroduced:{forbidden_title}")
    return errors


def incremental_tree_manifest(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative_path = path.relative_to(root)
        relative = relative_path.as_posix()
        if any(part in {".git", "__pycache__", ".pytest_cache", ".DS_Store"} for part in relative_path.parts):
            continue
        if path.suffix == ".pyc" or relative in {
            "manifest.json",
            "data/metadata/incremental-build-seal.json",
        }:
            continue
        files[relative] = sha256(path)
    return files


def stable_manifest_sha256(files: dict[str, str]) -> str:
    encoded = json.dumps(
        files, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def incremental_release_errors(
    datasets: dict[str, list[dict[str, Any]]],
    metadata: dict[str, Any],
    root: Path | None = None,
) -> list[str]:
    """Tie incremental rows, metadata, delta, and build seal into one closure."""
    errors: list[str] = []
    root = ROOT if root is None else root
    roles = datasets.get("roles", [])
    evidence = datasets.get("evidence-ledger-safe", [])
    current = datasets.get("current-opportunities", [])
    review = datasets.get("review-queue", [])
    incremental_roles = [
        row for row in roles if row.get("recovery_origin") == "continuous_new_role_discovery"
    ]
    incremental_evidence = [
        row
        for row in evidence
        if "continuous_new_role_discovery" in (row.get("limitations") or [])
    ]
    declaration = metadata.get("incremental_release")
    if not incremental_roles:
        if declaration:
            if not isinstance(declaration, dict):
                errors.append("incremental_declaration_without_roles")
            else:
                if (
                    declaration.get("cumulative_roles") not in {0, None}
                    or declaration.get("batch_roles_added") not in {0, None}
                    or declaration.get("batch_evidence_added") not in {0, None}
                    or declaration.get("role_ids_added") not in (None, (), [])
                ):
                    errors.append("incremental_declaration_without_roles")
                if declaration.get("raw_html_or_full_jd_stored") is not False:
                    errors.append("incremental_raw_html_or_full_jd")
        return errors
    if not isinstance(declaration, dict):
        return ["incremental_release_metadata_missing"]
    if declaration.get("version") != "agent-hiring-map-continuous-new-role-discovery/1.0":
        errors.append("incremental_release_version")
    if declaration.get("cumulative_roles") != len(incremental_roles):
        errors.append("incremental_cumulative_role_count")
    if len(incremental_evidence) != len(incremental_roles):
        errors.append("incremental_role_evidence_bijection")
    if declaration.get("raw_html_or_full_jd_stored") is not False:
        errors.append("incremental_raw_html_or_full_jd")
    evidence_id_list = [str(row.get("evidence_id") or "") for row in incremental_evidence]
    evidence_ids = set(evidence_id_list)
    if not all(evidence_id_list) or len(evidence_ids) != len(evidence_id_list):
        errors.append("incremental_evidence_ids_not_unique")
    role_to_evidence: dict[str, str] = {}
    for role in incremental_roles:
        linked = list(role.get("evidence_ids") or [])
        matched = set(linked) & evidence_ids
        if (
            role.get("public_confidence_tier") != "verified"
            or role.get("public_disposition") != "publish_current"
            or role.get("currentness_terminal") != "open_verified"
            or len(linked) != 1
            or len(matched) != 1
        ):
            errors.append(f"incremental_role_hard_gate:{role.get('role_id')}")
        elif role.get("role_id"):
            role_to_evidence[str(role["role_id"])] = next(iter(matched))
    usage = Counter(role_to_evidence.values())
    if set(usage) != evidence_ids or any(count != 1 for count in usage.values()):
        errors.append("incremental_role_evidence_bijection")
    for role in roles:
        if role.get("recovery_origin") != "continuous_new_role_discovery" and set(
            role.get("evidence_ids") or []
        ) & evidence_ids:
            errors.append(f"incremental_evidence_linked_from_historical_role:{role.get('role_id')}")

    actual_counts = {
        "evidence": len(evidence),
        "organizations": len(datasets.get("organizations", [])),
        "teams": len(datasets.get("teams", [])),
        "products": len(datasets.get("products", [])),
        "roles": len(roles),
        "relations": len(datasets.get("relations", [])),
        "current": len(current),
        "review": len(review),
    }
    canonical = metadata.get("canonical_counts")
    if not isinstance(canonical, dict):
        errors.append("incremental_metadata_canonical_counts_missing")
    else:
        for key in ("organizations", "teams", "products", "roles", "relations"):
            if canonical.get(key) != actual_counts[key]:
                errors.append(f"incremental_metadata_count:{key}")
    if metadata.get("evidence_rows") != actual_counts["evidence"]:
        errors.append("incremental_metadata_count:evidence")
    if metadata.get("review_queue_rows") != actual_counts["review"]:
        errors.append("incremental_metadata_count:review")
    current_metadata = metadata.get("current_opportunities")
    if not isinstance(current_metadata, dict) or current_metadata.get("rows") != actual_counts["current"]:
        errors.append("incremental_metadata_count:current")
    actual_current_geography = dict(
        sorted(Counter(str(row.get("geography") or "") for row in current).items())
    )
    if (
        not isinstance(current_metadata, dict)
        or current_metadata.get("geography") != actual_current_geography
    ):
        errors.append("incremental_metadata_current_geography")
    actual_confidence = dict(
        sorted(
            Counter(str(row.get("public_confidence_tier") or "") for row in roles).items()
        )
    )
    recovery = metadata.get("recovery")
    if not isinstance(recovery, dict) or recovery.get("public_confidence_tier") != actual_confidence:
        errors.append("incremental_metadata_confidence_partition")

    delta_path = root / "data/metadata/release-delta.json"
    seal_path = root / "data/metadata/incremental-build-seal.json"
    try:
        delta = json.loads(delta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append("incremental_release_delta_missing_or_invalid")
        delta = None
    try:
        seal = json.loads(seal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append("incremental_build_seal_missing_or_invalid")
        seal = None
    if not isinstance(delta, dict) or not isinstance(seal, dict):
        return errors

    if delta.get("schema_version") != "agent-hiring-map-public-delta/2.0":
        errors.append("incremental_delta_schema_version")
    if delta.get("reason") != "continuous_new_role_discovery_release":
        errors.append("incremental_delta_reason")
    if delta.get("raw_html_or_full_jd_stored") is not False:
        errors.append("incremental_delta_raw_html_or_full_jd")
    if seal.get("schema_version") != "agent-hiring-map-incremental-build-seal/1.0":
        errors.append("incremental_build_seal_schema_version")

    release_dates = [
        metadata.get("release_as_of"),
        declaration.get("release_date"),
        delta.get("release_as_of"),
        seal.get("release_date"),
    ]
    if not all(isinstance(value, str) for value in release_dates) or len(set(release_dates)) != 1:
        errors.append("incremental_release_date_mismatch")
    else:
        try:
            date.fromisoformat(release_dates[0])
        except ValueError:
            errors.append("incremental_release_date_invalid")

    input_sha256 = declaration.get("input_sha256")
    if not isinstance(input_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", input_sha256):
        errors.append("incremental_input_sha256_invalid")
    if seal.get("admissions_sha256") != input_sha256:
        errors.append("incremental_input_sha256_seal_mismatch")
    if not isinstance(seal.get("source_manifest_sha256"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", seal.get("source_manifest_sha256", "")
    ):
        errors.append("incremental_source_manifest_sha256_invalid")

    before = delta.get("before")
    after = delta.get("after")
    changed = delta.get("changed")
    count_keys = {
        "evidence",
        "organizations",
        "teams",
        "products",
        "roles",
        "relations",
        "current",
        "review",
    }
    changed_keys = {
        "role_ids_added",
        "roles_added",
        "current_added",
        "evidence_added",
        "organizations_added",
        "teams_added",
        "products_added",
        "relations_added",
        "review_delta",
    }
    if not isinstance(before, dict) or set(before) != count_keys:
        errors.append("incremental_delta_before_contract")
    if not isinstance(after, dict) or set(after) != count_keys:
        errors.append("incremental_delta_after_contract")
    if not isinstance(changed, dict) or set(changed) != changed_keys:
        errors.append("incremental_delta_changed_contract")
    if not isinstance(before, dict) or not isinstance(after, dict) or not isinstance(changed, dict):
        return errors

    for key in count_keys:
        if (
            not isinstance(before.get(key), int)
            or isinstance(before.get(key), bool)
            or before.get(key, -1) < 0
            or not isinstance(after.get(key), int)
            or isinstance(after.get(key), bool)
            or after.get(key, -1) < 0
        ):
            errors.append(f"incremental_delta_count_type:{key}")
        if after.get(key) != actual_counts[key]:
            errors.append(f"incremental_delta_after_actual:{key}")

    delta_fields = {
        "evidence": "evidence_added",
        "organizations": "organizations_added",
        "teams": "teams_added",
        "products": "products_added",
        "roles": "roles_added",
        "relations": "relations_added",
        "current": "current_added",
        "review": "review_delta",
    }
    for count_key, change_key in delta_fields.items():
        change_value = changed.get(change_key)
        if not isinstance(change_value, int) or isinstance(change_value, bool):
            errors.append(f"incremental_delta_change_type:{change_key}")
            continue
        if change_key != "review_delta" and change_value < 0:
            errors.append(f"incremental_delta_negative_addition:{change_key}")
        before_value = before.get(count_key)
        after_value = after.get(count_key)
        if (
            isinstance(before_value, int)
            and not isinstance(before_value, bool)
            and isinstance(after_value, int)
            and not isinstance(after_value, bool)
            and before_value + change_value != after_value
        ):
            errors.append(f"incremental_delta_not_closed:{count_key}")

    role_ids_added = changed.get("role_ids_added")
    declaration_role_ids = declaration.get("role_ids_added")
    seal_role_ids = seal.get("role_ids_added")
    if (
        not isinstance(role_ids_added, list)
        or not all(isinstance(value, str) and value for value in role_ids_added)
        or role_ids_added != sorted(set(role_ids_added))
    ):
        errors.append("incremental_delta_role_ids_invalid")
        role_ids_added = []
    if declaration_role_ids != role_ids_added or seal_role_ids != role_ids_added:
        errors.append("incremental_role_ids_three_way_mismatch")
    if declaration.get("batch_roles_added") != len(role_ids_added):
        errors.append("incremental_batch_role_count")
    if changed.get("roles_added") != len(role_ids_added):
        errors.append("incremental_delta_role_count")
    if changed.get("current_added") != len(role_ids_added):
        errors.append("incremental_delta_current_count")
    incremental_role_ids = {str(row.get("role_id") or "") for row in incremental_roles}
    current_role_ids = {str(row.get("role_id") or "") for row in current}
    if not set(role_ids_added) <= incremental_role_ids:
        errors.append("incremental_delta_role_ids_not_incremental")
    if not set(role_ids_added) <= current_role_ids:
        errors.append("incremental_delta_role_ids_not_current")
    batch_evidence_ids = {
        evidence_id
        for row in incremental_roles
        if row.get("role_id") in set(role_ids_added)
        for evidence_id in (row.get("evidence_ids") or [])
    }
    if declaration.get("batch_evidence_added") != len(batch_evidence_ids):
        errors.append("incremental_batch_evidence_count")
    if changed.get("evidence_added") != len(batch_evidence_ids):
        errors.append("incremental_delta_evidence_count")

    metadata_hash = sha256(root / "data/metadata/release-metadata.json")
    delta_hash = sha256(delta_path)
    if seal.get("release_metadata_sha256") != metadata_hash:
        errors.append("incremental_build_seal_metadata_hash")
    if seal.get("release_delta_sha256") != delta_hash:
        errors.append("incremental_build_seal_delta_hash")
    sealed_files = seal.get("output_files")
    if not isinstance(sealed_files, dict) or any(
        not isinstance(path, str)
        or not path
        or path.startswith("/")
        or ".." in Path(path).parts
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        for path, digest in (sealed_files.items() if isinstance(sealed_files, dict) else [])
    ):
        errors.append("incremental_build_seal_files_contract")
        sealed_files = {}
    actual_files = incremental_tree_manifest(root)
    if sealed_files != actual_files:
        errors.append("incremental_build_seal_output_drift")
    if seal.get("output_files_sha256") != stable_manifest_sha256(actual_files):
        errors.append("incremental_build_seal_output_manifest_hash")
    return errors


def workflow_errors() -> list[str]:
    errors: list[str] = []
    for name in ("validate.yml", "weekly-review.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        if "permissions:\n  contents: read" not in text:
            errors.append(f"workflow_not_read_only:{name}")
        if re.search(r"(?m)^\s*(?:contents|issues|pull-requests):\s*write\s*$", text):
            errors.append(f"workflow_write_permission:{name}")
        if any(token in text for token in ("secrets.", "curl ", "wget ", "gh api")):
            errors.append(f"workflow_network_or_secret:{name}")
    return errors


def honest_state_errors() -> list[str]:
    errors: list[str] = []
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "README.md",
            ROOT / "index.html",
            ROOT / "docs" / "OBSERVATION.md",
        ]
    ).lower()
    false_claims = (
        "7,217 个当前岗位",
        "7217 个当前岗位",
        "p4_passed=true",
        "demand_proven=true",
        "scale_proven=true",
        "candidate_ready=true",
    )
    for claim in false_claims:
        if claim.lower() in combined:
            errors.append(f"false_state_claim:{claim}")
    return errors


def site_errors() -> list[str]:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    styles = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
    errors: list[str] = []

    required_html_tokens = (
        'http-equiv="Content-Security-Policy"',
        'id="explorer"',
        'id="filter-query"',
        'id="filter-scope"',
        'id="filter-geography"',
        'id="filter-category"',
        'id="filter-remote"',
        'id="filter-grade"',
        'id="filter-confidence"',
        'id="filter-team-state"',
        'id="lang-zh"',
        'id="lang-en"',
        'data-i18n="heroLead"',
        'id="results"',
        'src="./assets/app.js"',
        'href="./assets/styles.css"',
    )
    for token in required_html_tokens:
        if token not in html:
            errors.append(f"site_missing_html_token:{token}")

    required_data_paths = (
        "./data/metadata/release-metadata.json",
        "./data/map/organizations.jsonl",
        "./data/map/teams.jsonl",
        "./data/map/products.jsonl",
        "./data/map/roles.jsonl",
        "./data/current/current-opportunities.jsonl",
    )
    for path in required_data_paths:
        if path not in app:
            errors.append(f"site_missing_dynamic_data_path:{path}")
        if app.count(path) != 1:
            errors.append(f"site_duplicate_dynamic_data_path:{path}")

    if re.search(r"<script(?![^>]*\bsrc=)[^>]*>", html, flags=re.IGNORECASE):
        errors.append("site_inline_script")
    if re.search(r"<style(?:\s|>)", html, flags=re.IGNORECASE):
        errors.append("site_inline_style")
    if re.search(r"<form(?:\s|>)", html, flags=re.IGNORECASE):
        errors.append("site_business_form")
    if re.search(
        r"<script[^>]+\bsrc=[\"']https?://",
        html,
        flags=re.IGNORECASE,
    ):
        errors.append("site_external_script")
    if re.search(
        r"<link[^>]+\brel=[\"']stylesheet[\"'][^>]+\bhref=[\"']https?://",
        html,
        flags=re.IGNORECASE,
    ):
        errors.append("site_external_stylesheet")

    forbidden_app_tokens = (
        ".innerHTML",
        ".outerHTML",
        "document.write",
        "new Function",
        "eval(",
        "localStorage",
        "sessionStorage",
        "sendBeacon",
        "WebSocket(",
    )
    for token in forbidden_app_tokens:
        if token in app:
            errors.append(f"site_forbidden_runtime:{token}")
    if "textContent" not in app or "document.createElement" not in app:
        errors.append("site_external_text_not_dom_safe")
    if 'credentials: "same-origin"' not in app:
        errors.append("site_fetch_not_same_origin")
    if 'document.addEventListener("DOMContentLoaded", load)' not in app:
        errors.append("site_missing_load_entrypoint")
    for token in (
        "display_title_zh",
        "display_title_en",
        "display_location_zh",
        "display_location_en",
        "work_arrangement",
        "work_arrangement_basis",
        "public_confidence_tier",
        '"filter-confidence"',
        'params.set("lang", state.lang)',
        "document.documentElement.lang",
        "const I18N",
        "zh:",
        "en:",
    ):
        if token not in app:
            errors.append(f"site_missing_localization_contract:{token}")
    if any(
        token in app.lower()
        for token in (
            "translate.googleapis.com",
            "api.deepl.com",
            "api.cognitive.microsofttranslator.com",
        )
    ):
        errors.append("site_runtime_translation_service")
    if "@media (max-width:" not in styles:
        errors.append("site_missing_responsive_layout")
    if "@media (prefers-reduced-motion: reduce)" not in styles:
        errors.append("site_missing_reduced_motion")
    for token in (
        'background-image: url("./icons/chevron-down.svg")',
        "appearance: none",
        "padding-right: 44px",
        "background-position: right 15px center",
    ):
        if token not in styles:
            errors.append(f"site_select_spacing_contract:{token}")
    return errors


def overview_errors() -> list[str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_team_role_overview.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    detail = (result.stderr or result.stdout).strip().replace("\n", " ")
    return [f"team_role_overview:{detail or 'check_failed'}"]


def scale_doc_errors(
    datasets: dict[str, list[dict[str, Any]]], metadata: dict[str, Any]
) -> list[str]:
    summary = json.loads(
        (ROOT / "data" / "metadata" / "global-recovery-summary.json").read_text(
            encoding="utf-8"
        )
    )
    document = (ROOT / "docs" / "DATA_SCALE_AND_SCOPE.md").read_text(
        encoding="utf-8"
    )
    dictionary = (ROOT / "docs" / "DATA_DICTIONARY.md").read_text(encoding="utf-8")
    methodology = (ROOT / "docs" / "METHODOLOGY.md").read_text(encoding="utf-8")
    errors: list[str] = []
    evidence = summary.get("evidence", {})
    terminal = summary.get("terminal_status", {})
    network = summary.get("network", {})
    projection = summary.get("projection", {})
    exploration = summary.get("exploration", {})
    recovery = metadata.get("recovery", {})
    canonical = metadata.get("canonical_counts", {})

    incremental_roles = [
        row
        for row in datasets.get("roles", [])
        if row.get("recovery_origin") == "continuous_new_role_discovery"
    ]
    incremental_evidence = [
        row
        for row in datasets.get("evidence-ledger-safe", [])
        if "continuous_new_role_discovery" in (row.get("limitations") or [])
    ]
    try:
        summary_date = date.fromisoformat(str(summary.get("as_of_date") or ""))
        release_date = date.fromisoformat(str(metadata.get("release_as_of") or ""))
    except ValueError:
        errors.append("scale_summary_release_date")
    else:
        if (
            (not incremental_roles and summary_date != release_date)
            or (incremental_roles and summary_date > release_date)
        ):
            errors.append("scale_summary_release_date")
    expected_ledger_rows = metadata.get("evidence_rows")
    if not isinstance(expected_ledger_rows, int) or isinstance(expected_ledger_rows, bool):
        errors.append("scale_summary_evidence_rows")
    else:
        if incremental_roles:
            expected_ledger_rows -= len(incremental_evidence)
        if evidence.get("ledger_rows") != expected_ledger_rows:
            errors.append("scale_summary_evidence_rows")
    if evidence.get("global_frozen_rows") != recovery.get(
        "global_frozen_evidence_terminalized"
    ):
        errors.append("scale_summary_global_frozen_rows")
    if sum(terminal.values()) != evidence.get("global_frozen_rows"):
        errors.append("scale_summary_terminal_partition")
    if sum(network.get("adapter_triggers", {}).values()) != network.get("triggers"):
        errors.append("scale_summary_network_partition")
    for summary_key, recovery_key in (
        ("new_unique_roles", "global_new_roles"),
        ("new_strict_current", "global_new_current_opportunities"),
        ("new_organizations", "global_new_organizations"),
    ):
        if projection.get(summary_key) != recovery.get(recovery_key):
            errors.append(f"scale_summary_projection:{summary_key}")
    if sum(exploration.get("high_signal_recheck_definition", {}).values()) != exploration.get(
        "high_signal_recheck_rows"
    ):
        errors.append("scale_summary_high_signal_partition")

    current_teams = len(
        {
            row.get("team_id")
            for row in datasets.get("current-opportunities", [])
            if row.get("team_id")
        }
    )
    expected_doc_tokens = {
        f"数据快照：{metadata['release_as_of']}": "release_date",
        f"{metadata['evidence_rows']:,} 条证据": "evidence_rows",
        f"{evidence['global_frozen_rows']:,} 条": "global_frozen_rows",
        f"{canonical['roles']:,} 个岗位": "role_rows",
        f"{recovery['public_confidence_tier']['verified']:,} 个已核实岗位": "verified_roles",
        f"{recovery['public_confidence_tier']['probable']:,} 个高概率岗位": "probable_roles",
        f"{metadata['current_opportunities']['rows']:,} 个确认当前开放": "current_rows",
        f"{metadata['review_queue_rows']:,} | 复核队列事件": "review_queue_rows",
        f"{current_teams:,} 个有当前岗位的团队": "current_teams",
        f"{canonical['organizations']:,} | 组织": "organizations",
        f"{canonical['teams']:,} | 团队": "teams",
        f"{canonical['products']:,} | 产品": "products",
        f"{canonical['relations']:,} | 关系": "relations",
    }
    for token, code in expected_doc_tokens.items():
        if token not in document:
            errors.append(f"scale_doc_stale:{code}")
    current_rows = metadata["current_opportunities"]["rows"]
    role_rows = canonical["roles"]
    evidence_rows = metadata["evidence_rows"]
    if f"默认 Current 只由 `{current_rows:,}` 条 `publish_current` 组成" not in dictionary:
        errors.append("data_dictionary_current_count_stale")
    if (
        f"因此 {evidence_rows:,} 条 Evidence、{role_rows:,} 条岗位记录和 "
        f"{current_rows:,} 条 {metadata['release_as_of']} 严格 Current"
        not in methodology
        or f"Current 由全部 {role_rows:,} 条唯一公开处置直接投影" not in methodology
    ):
        errors.append("methodology_current_snapshot_stale")
    return errors


def manifest_errors() -> list[str]:
    path = ROOT / "manifest.json"
    if not path.exists():
        return ["manifest_missing"]
    manifest = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    files = manifest.get("files")
    if (
        manifest.get("schema_version") != "agent-hiring-map-public-manifest/1.0"
        or manifest.get("hash_algorithm") != "sha256"
        or manifest.get("self_excluded") is not True
        or not isinstance(files, dict)
    ):
        errors.append("manifest_contract_invalid")
        files = files if isinstance(files, dict) else {}
    if "manifest.json" in files:
        errors.append("manifest_not_self_excluded")
    for relative, digest in files.items():
        if (
            not isinstance(relative, str)
            or not relative
            or relative.startswith("/")
            or ".." in Path(relative).parts
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            errors.append("manifest_file_entry_invalid")
            break
    actual = {}
    for item in sorted(ROOT.rglob("*")):
        if not item.is_file() or ".git" in item.parts:
            continue
        relative = item.relative_to(ROOT).as_posix()
        if (
            ".pytest_cache" in item.parts
            or "__pycache__" in item.parts
            or item.suffix == ".pyc"
            or item.name == ".DS_Store"
            or relative == "review-queue.jsonl"
            or relative.startswith("metrics-private/")
        ):
            continue
        if relative == "manifest.json":
            continue
        actual[relative] = sha256(item)
    if actual != files:
        errors.append("manifest_hash_drift")
    return errors


def project_current(role: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """Rebuild the deterministic Current fields from canonical Role."""

    return {
        "access_requirement": role.get("access_requirement"),
        "agent_specific_excerpt": str(
            role.get("agent_specific_quote") or role.get("agent_relevance_summary") or ""
        ).strip()[:300],
        "citation_supports_title": role.get("citation_supports_title"),
        "currentness_status": role.get("currentness_status"),
        "display_title_en": role.get("display_title_en"),
        "display_title_zh": role.get("display_title_zh"),
        "evidence_grade": "A",
        "evidence_ids": role.get("evidence_ids"),
        "geography": role.get("geography") or current.get("geography"),
        "last_verified_at": role.get("last_verified_at"),
        "limitations": current.get("limitations"),
        "organization_id": role.get("organization_id"),
        "product_id": role.get("product_id"),
        "role_id": role.get("role_id"),
        "schema_version": role.get("schema_version"),
        "source_urls": [normalize_url_for_projection(role.get("official_role_url"))],
        "team_id": role.get("team_id"),
        "title": role.get("official_title_raw"),
        "title_source_granularity": role.get("title_source_granularity"),
        "title_source_url": role.get("title_source_url"),
        "title_support_status": role.get("title_support_status"),
        "title_translation_status": role.get("title_translation_status"),
    }


def run_default() -> dict[str, Any]:
    errors = filesystem_structure_errors()
    if errors:
        return {
            "validator": "agent-hiring-map-public-package/1.0",
            "mode": "default",
            "counts": {},
            "errors": sorted(set(errors)),
            "status": "fail",
        }
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"missing_required_file:{name}")
    datasets: dict[str, list[dict[str, Any]]] = {}
    for stem, expected in DATASET_SPECS.items():
        csv_path = ROOT / f"{stem}.csv"
        jsonl_path = ROOT / f"{stem}.jsonl"
        if not csv_path.exists() or not jsonl_path.exists():
            errors.append(f"missing_dataset:{stem}")
            continue
        errors.extend(parity_errors(stem))
        rows = load_jsonl(jsonl_path)
        datasets[stem.split("/")[-1]] = rows
        if expected is not None and len(rows) != expected:
            errors.append(f"row_count:{stem}:{len(rows)}")
    id_keys = {
        "evidence-ledger-safe": "evidence_id",
        "organizations": "organization_id",
        "teams": "team_id",
        "products": "product_id",
        "roles": "role_id",
        "relations": "relation_id",
        "current-opportunities": "role_id",
    }
    for name, key in id_keys.items():
        if name not in datasets:
            continue
        values = [row.get(key) for row in datasets[name]]
        if any(not value for value in values) or len(values) != len(set(values)):
            errors.append(f"duplicate_or_missing_id:{name}:{key}")
    metadata = json.loads(
        (ROOT / "data" / "metadata" / "release-metadata.json").read_text(encoding="utf-8")
    )
    declared_counts = metadata.get("canonical_counts", {})
    for dataset_name, metadata_name in (
        ("organizations", "organizations"),
        ("teams", "teams"),
        ("products", "products"),
        ("roles", "roles"),
        ("relations", "relations"),
    ):
        if dataset_name in datasets and len(datasets[dataset_name]) != declared_counts.get(
            metadata_name
        ):
            errors.append(f"metadata_row_count:{dataset_name}")
    if "evidence-ledger-safe" in datasets:
        errors.extend(evidence_errors(datasets["evidence-ledger-safe"]))
    if "current-opportunities" in datasets:
        errors.extend(current_errors(datasets["current-opportunities"], metadata))
    if "roles" in datasets:
        errors.extend(role_display_errors(datasets["roles"], metadata))
    errors.extend(incremental_release_errors(datasets, metadata))
    if "review-queue" in datasets:
        if len(datasets["review-queue"]) != metadata.get("review_queue_rows"):
            errors.append("metadata_row_count:review-queue")
    if "roles" in datasets and "review-queue" in datasets:
        probable_ids = {
            row["role_id"]
            for row in datasets["roles"]
            if row.get("public_confidence_tier") == "probable"
        }
        queued_probable_ids = {
            row["role_id"]
            for row in datasets["review-queue"]
            if row.get("review_reason") == "probable_role_followup"
        }
        if probable_ids != queued_probable_ids:
            errors.append("review_queue_probable_role_set_mismatch")
        reason_counts = Counter(
            str(row.get("review_reason")) for row in datasets["review-queue"]
        )
        if sum(reason_counts.values()) != metadata.get("review_queue_rows"):
            errors.append("review_queue_reason_partition")
    required_map = {"organizations", "teams", "products", "roles", "relations"}
    if required_map.issubset(datasets) and "evidence-ledger-safe" in datasets:
        errors.extend(
            map_errors(
                datasets,
                {row["evidence_id"] for row in datasets["evidence-ledger-safe"]},
            )
        )
    if "current-opportunities" in datasets and "roles" in datasets:
        role_by_id = {row["role_id"]: row for row in datasets["roles"]}
        current_ids = {row["role_id"] for row in datasets["current-opportunities"]}
        publish_ids = {
            row["role_id"]
            for row in datasets["roles"]
            if row.get("public_disposition") == "publish_current"
        }
        if current_ids != publish_ids:
            errors.append("current_publish_disposition_set_mismatch")
        for role in datasets["roles"]:
            is_current = role["role_id"] in current_ids
            if role.get("public_is_current") is not is_current:
                errors.append(f"role_public_is_current_mismatch:{role['role_id']}")
            if not is_current and role.get("currentness_status") in {
                "current_verified",
                "current_probable",
            }:
                errors.append(f"noncurrent_role_implies_current:{role['role_id']}")
        for row in datasets["current-opportunities"]:
            role = role_by_id.get(row["role_id"])
            if role is None:
                errors.append(f"current_role_missing:{row['role_id']}")
                continue
            if row != project_current(role, row):
                errors.append(f"current_not_exact_role_projection:{row['role_id']}")
            if (
                row.get("title") != role.get("official_title_raw")
                or row.get("title_source_url") != role.get("title_source_url")
                or row.get("title_support_status")
                != role.get("title_support_status")
                or row.get("citation_supports_title") is not True
            ):
                errors.append(f"current_role_title_mismatch:{row['role_id']}")
            if (
                role.get("public_confidence_tier") != "verified"
                or role.get("eligible_for_strict_current") is not True
                or role.get("public_disposition") != "publish_current"
                or role.get("currentness_terminal") != "open_verified"
            ):
                errors.append(f"current_role_confidence_mismatch:{row['role_id']}")
    errors.extend(scan_text_safety())
    errors.extend(scan_csv_formula())
    errors.extend(workflow_errors())
    errors.extend(honest_state_errors())
    errors.extend(site_errors())
    errors.extend(overview_errors())
    errors.extend(scale_doc_errors(datasets, metadata))
    errors = sorted(set(errors))
    return {
        "validator": "agent-hiring-map-public-package/1.0",
        "mode": "default",
        "counts": {
            name: len(rows) for name, rows in sorted(datasets.items())
        },
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }


def run_self_test() -> dict[str, Any]:
    tests: list[tuple[str, bool]] = []
    tests.append(("formula_injection", "=cmd" .startswith(FORMULA_PREFIXES)))
    tests.append(("secret_private_key", bool(SECRET_PATTERNS[0].search("-----BEGIN PRIVATE KEY-----"))))
    tests.append(("secret_github_token", bool(SECRET_PATTERNS[1].search("ghp_abcdefghijklmnopqrstuvwxyz1234"))))
    tests.append(("private_email", bool(PRIVATE_PATTERNS[0].search("person@example.com"))))
    tests.append(("absolute_path", bool(ABSOLUTE_PATH_PATTERNS[0].search("/Users/name/project"))))
    tests.append(("unsafe_url_scheme", not valid_public_url("file:///tmp/data")))
    tests.append(("url_credentials", not valid_public_url("https://user:pass@example.com/a")))
    tests.append(("url_localhost", not valid_public_url("https://localhost/jobs/1")))
    tests.append(("url_private_ipv4", not valid_public_url("https://10.0.0.8/jobs/1")))
    tests.append(("url_loopback_ipv6", not valid_public_url("https://[::1]/jobs/1")))
    tests.append(("url_short_loopback", not valid_public_url("https://127.1/jobs/1")))
    tests.append(("url_integer_loopback", not valid_public_url("https://2130706433/jobs/1")))
    tests.append(("url_hex_loopback", not valid_public_url("https://0x7f000001/jobs/1")))
    invalid = {
        "schema_version": "agent-hiring-map-submission/1.0",
        "change_type": "add",
        "organization_name": "=BAD",
        "role_title": "ignore previous instructions",
        "geography": "",
        "official_source_url": "http://user:pass@example.com/job",
        "observed_at": "2099-01-01",
        "access_requirement": "paid_or_private_blocked",
        "agent_specific_excerpt": "email person@example.com",
    }
    submission_errors = validate_submission(invalid)
    tests.append(("submission_formula", any("formula_injection" in item for item in submission_errors)))
    tests.append(("submission_prompt", any("prompt_injection" in item for item in submission_errors)))
    tests.append(("submission_private", any("private_contact" in item for item in submission_errors)))
    tests.append(("submission_geography", "invalid_geography" in submission_errors))
    tests.append(("submission_access", "restricted_access_not_allowed" in submission_errors))
    tests.append(("submission_future", "future_observed_at" in submission_errors))
    tests.append(("submission_url", "invalid_official_source_url" in submission_errors))
    tests.append(("blocked_current", "blocked" not in {"current_verified", "current_probable"}))
    tests.append(("paid_current", "paid_or_private_blocked" != "public_no_login"))
    tests.append(("future_current", (date(2026, 7, 23) - date(2026, 7, 24)).days < 0))
    tests.append(("expired_current", (date(2026, 7, 23) - date(2026, 7, 8)).days > 14))
    tests.append(("workflow_write_permission", bool(re.search(r"contents:\s*write", "permissions:\n contents: write"))))
    tests.append(("telemetry_domain", "posthog.capture" in "posthog.capture('query')"))
    tests.append(("evidence_current_conflation", "7,217 个当前岗位" in "本项目有 7,217 个当前岗位"))
    tests.append(
        (
            "probable_current_pollution",
            "probable" in PUBLIC_CONFIDENCE_TIERS and False is not True,
        )
    )
    duplicate_incremental_evidence = incremental_release_errors(
        {
            "roles": [
                {
                    "role_id": f"ROLE-DUP-{index}",
                    "recovery_origin": "continuous_new_role_discovery",
                    "public_confidence_tier": "verified",
                    "public_disposition": "publish_current",
                    "currentness_terminal": "open_verified",
                    "evidence_ids": ["AMC-7218"],
                }
                for index in range(2)
            ],
            "evidence-ledger-safe": [
                {
                    "evidence_id": "AMC-7218",
                    "limitations": ["continuous_new_role_discovery"],
                },
                {
                    "evidence_id": "AMC-7219",
                    "limitations": ["continuous_new_role_discovery"],
                },
            ],
        },
        {
            "incremental_release": {
                "version": "agent-hiring-map-continuous-new-role-discovery/1.0",
                "cumulative_roles": 2,
                "raw_html_or_full_jd_stored": False,
            }
        },
    )
    tests.append(
        (
            "incremental_duplicate_evidence_negative_control",
            "incremental_role_evidence_bijection" in duplicate_incremental_evidence,
        )
    )
    negative_incremental = incremental_release_errors(
        {
            "roles": [
                {
                    "role_id": "ROLE-NEGATIVE",
                    "recovery_origin": "continuous_new_role_discovery",
                    "public_confidence_tier": "verified",
                    "public_disposition": "publish_current",
                    "currentness_terminal": "open_verified",
                    "evidence_ids": ["AMC-7218"],
                }
            ],
            "evidence-ledger-safe": [],
        },
        {
            "incremental_release": {
                "version": "agent-hiring-map-continuous-new-role-discovery/1.0",
                "cumulative_roles": 1,
                "raw_html_or_full_jd_stored": False,
            }
        },
    )
    tests.append(
        (
            "incremental_missing_evidence_negative_control",
            "incremental_role_evidence_bijection" in negative_incremental,
        )
    )
    raw_incremental = incremental_release_errors(
        {"roles": [], "evidence-ledger-safe": []},
        {
            "incremental_release": {
                "cumulative_roles": 1,
                "raw_html_or_full_jd_stored": True,
            }
        },
    )
    tests.append(
        (
            "incremental_declaration_without_roles_negative_control",
            "incremental_declaration_without_roles" in raw_incremental,
        )
    )
    tests.append(
        (
            "known_false_title_fixture",
            "工业智能体技术项目"
            in "清华大学工业智能体技术项目（错误合成标题）",
        )
    )
    tests.append(
        (
            "location_residue_chinese",
            bool(LOCATION_RESIDUE_ZH.search("北京市；长期招聘")),
        )
    )
    tests.append(
        (
            "location_residue_english",
            bool(LOCATION_RESIDUE_EN.search("Beijing; full-time social recruitment")),
        )
    )
    tests.append(
        (
            "default_onsite_contract",
            "default_onsite_no_remote_signal"
            in WORK_ARRANGEMENT_BASES
            and "onsite" in WORK_ARRANGEMENTS,
        )
    )
    tests.append(
        (
            "site_inline_script",
            bool(
                re.search(
                    r"<script(?![^>]*\bsrc=)[^>]*>",
                    "<script>alert(1)</script>",
                )
            ),
        )
    )
    tests.append(
        (
            "site_external_script",
            bool(
                re.search(
                    r"<script[^>]+\bsrc=[\"']https?://",
                    '<script src="https://example.com/a.js">',
                )
            ),
        )
    )
    tests.append(
        (
            "site_business_form",
            bool(re.search(r"<form(?:\s|>)", "<form action='/apply'>")),
        )
    )
    site_app = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    tests.append(
        (
            "site_dynamic_data_binding",
            all(
                path in site_app
                for path in (
                    "./data/metadata/release-metadata.json",
                    "./data/map/organizations.jsonl",
                    "./data/map/teams.jsonl",
                    "./data/map/products.jsonl",
                    "./data/map/roles.jsonl",
                    "./data/current/current-opportunities.jsonl",
                )
            ),
        )
    )
    tests.append(
        (
            "site_safe_text_rendering",
            ".innerHTML" not in site_app and "textContent" in site_app,
        )
    )
    tests.append(
        (
            "site_bilingual_contract",
            all(
                token in site_app
                for token in (
                    "const I18N",
                    "display_title_zh",
                    "display_title_en",
                    'params.set("lang", state.lang)',
                )
            ),
        )
    )
    with tempfile.TemporaryDirectory() as tmp:
        test_file = Path(tmp) / "x"
        test_file.write_text("a", encoding="utf-8")
        first = sha256(test_file)
        test_file.write_text("b", encoding="utf-8")
        tests.append(("manifest_hash_drift", first != sha256(test_file)))
    tests.append(("manifest_runtime_cache_excluded", "__pycache__" in Path("scripts/__pycache__/x.pyc").parts))
    failed = [name for name, passed in tests if not passed]
    return {
        "validator": "agent-hiring-map-public-package/1.0",
        "mode": "self-test",
        "tests": len(tests),
        "passed": len(tests) - len(failed),
        "failed": failed,
        "status": "pass" if not failed else "fail",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--final", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = run_self_test()
    else:
        result = run_default()
        result["mode"] = "final" if args.final else "default"
        if args.final:
            result["errors"].extend(manifest_errors())
            result["errors"] = sorted(set(result["errors"]))
            result["status"] = "pass" if not result["errors"] else "fail"
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
