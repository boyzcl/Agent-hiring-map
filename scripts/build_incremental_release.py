#!/usr/bin/env python3
"""Deterministically promote sealed admissions into an isolated public tree.

The source tree is never modified.  An empty admission file is a byte-for-byte
tree copy.  Non-empty runs rebuild every affected JSONL/CSV projection from the
source JSONL plus a sealed, independently reviewed admission set.
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import ipaddress
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from build_review_queue import build as build_review_queue


PUBLIC_SCHEMA = "agent-hiring-map-public/1.0"
INCREMENTAL_VERSION = "agent-hiring-map-continuous-new-role-discovery/1.0"
PUBLICATION_VERSION = "agent-hiring-map-existing-role-public-disposition/1.0"
ROLE_DISPLAY_VERSION = "agent-hiring-map-role-display/1.0"
TITLE_VERSION = "agent-hiring-map-title-authenticity/1.0"
TRACKING_KEYS = {"fbclid", "gclid", "ref", "source"}
ATS_HOSTS = {
    "jobs.ashbyhq.com",
    "jobs.lever.co",
    "job-boards.greenhouse.io",
    "boards.greenhouse.io",
    "careers.smartrecruiters.com",
}
FORBIDDEN_PAYLOAD_KEYS = {
    "raw_html",
    "html",
    "full_jd",
    "full_job_description",
    "job_description",
    "description_html",
    "description",
    "responsibilities",
    "requirements",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
NONCANONICAL_NUMERIC_HOST_RE = re.compile(
    r"^(?:0[xX][0-9a-fA-F]+|[0-9]+)(?:\.(?:0[xX][0-9a-fA-F]+|[0-9]+))*$"
)
HTML_OR_ENTITY_RE = re.compile(
    r"<\s*[A-Za-z!/]|&(?:#[0-9]+|#x[0-9a-f]+|[A-Za-z][A-Za-z0-9]+);",
    re.I,
)
RELEASE_COHORTS = {
    "historical_local_overlay_revalidation",
    "china_main1_restricted_new_admission",
}
ANTI_JOIN_KEY_FIELDS = (
    "canonical_url",
    "organization_stable_job_id",
    "ats_tenant_locator",
    "organization_title",
)
COPY_IGNORED_NAMES = {".git", "__pycache__", ".pytest_cache", ".DS_Store"}


class ReleaseError(ValueError):
    """Fail-closed admission or source-tree error."""


def stable_json(value: Any, *, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    material = "\0".join(normalize_text(part) for part in parts)
    return f"{prefix}-{hashlib.sha256(material.encode()).hexdigest()[:16].upper()}"


def normalize_text(value: object) -> str:
    return " ".join(str(value or "").casefold().strip().split())


def normalize_url(value: object) -> str:
    try:
        parsed = urlsplit(str(value or "").strip())
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return ""
        if parsed.username or getattr(parsed, "password"):
            return ""
        host = parsed.hostname.casefold().rstrip(".")
        if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
            return ""
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = None
        if address is None and NONCANONICAL_NUMERIC_HOST_RE.fullmatch(host):
            return ""
        if address is not None and not address.is_global:
            return ""
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
            and not parsed.username
            and not parsed.password
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
            (
                "https",
                f"{host}{port}",
                path,
                urlencode(sorted(query)),
                fragment,
            )
        )
    except (ValueError, TypeError):
        return ""


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_jsonl_bytes(content: bytes) -> list[dict[str, Any]]:
    try:
        text = content.decode("utf-8")
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseError("admissions must be valid UTF-8 JSONL") from exc


def write_jsonl(
    path: Path, rows: Iterable[dict[str, Any]], *, sort_keys: bool = False
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            # Existing public JSONL files intentionally use schema-oriented key
            # order rather than a single repository-wide alphabetical order.
            # ``json.loads`` preserves that order, so retaining insertion order
            # keeps unchanged source rows byte-stable while newly constructed
            # rows remain deterministic from their builders.
            handle.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=sort_keys,
                )
                + "\n"
            )


def csv_cell(value: Any) -> Any:
    if value is None or isinstance(value, (list, dict, bool)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def csv_serialization_contract(
    path: Path, rows: list[dict[str, Any]]
) -> tuple[list[str], str]:
    available = set().union(*(set(row) for row in rows)) if rows else set()
    existing_fields: list[str] = []
    line_terminator = "\n"
    if path.exists():
        raw = path.read_bytes()
        if b"\r\n" in raw:
            line_terminator = "\r\n"
        try:
            header = raw.splitlines()[0].decode("utf-8") if raw.splitlines() else ""
            existing_fields = next(csv.reader([header])) if header else []
        except (UnicodeDecodeError, csv.Error) as exc:
            raise ReleaseError(f"invalid existing CSV serialization contract: {path}") from exc
        if len(existing_fields) != len(set(existing_fields)):
            raise ReleaseError(f"duplicate existing CSV field: {path}")
    return existing_fields + sorted(available - set(existing_fields)), line_terminator


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
    *,
    line_terminator: str = "\n",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, lineterminator=line_terminator
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({name: csv_cell(row.get(name)) for name in fieldnames})


def tree_file_manifest(root: Path, *, exclude_release_seal: bool = False) -> dict[str, str]:
    root = root.absolute()
    if root.is_symlink():
        raise ReleaseError("source tree must not be a symlink")
    root = root.resolve()
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative_path = path.relative_to(root)
        relative = relative_path.as_posix()
        if path.is_symlink():
            raise ReleaseError(f"source tree contains symlink: {relative}")
        if relative_path.parts and relative_path.parts[0] == "metrics-private":
            raise ReleaseError("source tree contains forbidden metrics-private content")
        if any(part in COPY_IGNORED_NAMES for part in relative_path.parts):
            continue
        if path.suffix == ".pyc" or not path.is_file():
            continue
        if exclude_release_seal and relative in {
            "manifest.json",
            "data/metadata/incremental-build-seal.json",
        }:
            continue
        files[relative] = sha256_bytes(path.read_bytes())
    return files


def manifest_sha256(manifest: dict[str, str]) -> str:
    return sha256_bytes(stable_json(manifest).encode())


def lexical_absolute_output_path(output: Path, label: str) -> Path:
    """Make an output path absolute without following any filesystem links."""
    output = Path(output)
    if ".." in output.parts:
        raise ReleaseError(f"{label} path must not contain '..'")
    if not output.is_absolute():
        output = Path.cwd() / output
    return output


def reject_output_path_symlinks(output: Path, label: str) -> None:
    for component in (output, *output.parents):
        if component.is_symlink():
            raise ReleaseError(f"{label} path must not be or traverse a symlink")


def prepare_secure_output_path(output: Path, label: str) -> Path:
    """Return a lexical absolute output path after fail-closed symlink checks."""

    output = lexical_absolute_output_path(output, label)

    # Do not resolve before this check: resolve() follows both existing and
    # dangling final links and would erase the evidence that must fail closed.
    reject_output_path_symlinks(output, label)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Recheck after mkdir so a newly materialized parent cannot bypass the gate.
    reject_output_path_symlinks(output, label)
    return output


def open_nofollow_lock(lock_path: Path, label: str):
    """Open a regular lock file without following a hostile final symlink."""

    if not hasattr(os, "O_NOFOLLOW"):
        raise ReleaseError(f"{label} requires O_NOFOLLOW support")
    flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise ReleaseError(f"{label} must be a regular non-symlink file") from exc
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ReleaseError(f"{label} must be a regular non-symlink file")
    return os.fdopen(descriptor, "a+b")


def open_nofollow_directory(path: Path, label: str) -> int:
    """Open a directory itself, never a final symlink, for durable fsync."""

    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise ReleaseError(f"{label} requires O_NOFOLLOW and O_DIRECTORY support")
    try:
        return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ReleaseError(f"{label} must be a non-symlink directory") from exc


def copy_source(
    source: Path, output: Path, expected_manifest: dict[str, str] | None = None
) -> None:
    source = source.absolute()
    if source.is_symlink():
        raise ReleaseError("source tree must not be a symlink")
    source = source.resolve()
    output = lexical_absolute_output_path(output, "staging output")
    reject_output_path_symlinks(output, "staging output")
    if source == output or source in output.parents:
        raise ReleaseError("output tree must be outside the source tree")
    precreated = output.exists()
    if precreated and (not output.is_dir() or any(output.iterdir())):
        raise ReleaseError(f"precreated output tree must be an empty directory: {output}")
    if expected_manifest is None:
        expected_manifest = tree_file_manifest(source)
    shutil.copytree(
        source,
        output,
        dirs_exist_ok=precreated,
        ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache", "*.pyc", ".DS_Store"
        ),
    )
    if tree_file_manifest(output) != expected_manifest:
        raise ReleaseError("source tree changed while the frozen release copy was created")


def nested_values(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from nested_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_values(child)


def pick(row: dict[str, Any], *names: str, default: Any = None) -> Any:
    role = row.get("role") if isinstance(row.get("role"), dict) else {}
    for name in names:
        if row.get(name) not in (None, ""):
            return row[name]
        if role.get(name) not in (None, ""):
            return role[name]
    return default


def parse_observed_at(value: object, field: str) -> datetime:
    raw = str(value or "").strip()
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReleaseError(f"{field} must be a valid timezone-aware timestamp") from exc
    if parsed.tzinfo is None:
        raise ReleaseError(f"{field} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def read_sealed_bytes(spec: object, label: str) -> tuple[Path, bytes]:
    if not isinstance(spec, dict):
        raise ReleaseError(f"missing sealed artifact specification: {label}")
    path = Path(str(spec.get("path") or ""))
    expected = str(spec.get("sha256") or "")
    if not path.is_absolute() or not SHA256_RE.fullmatch(expected):
        raise ReleaseError(f"invalid sealed artifact specification: {label}")
    if path.is_symlink() or not path.is_file():
        raise ReleaseError(f"sealed artifact must be a regular non-symlink file: {label}")
    content = path.read_bytes()
    if sha256_bytes(content) != expected:
        raise ReleaseError(f"sealed artifact hash mismatch: {label}")
    return path, content


def read_sealed_json(spec: object, label: str) -> dict[str, Any]:
    _, content = read_sealed_bytes(spec, label)
    try:
        value = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"sealed artifact is not valid JSON: {label}") from exc
    if not isinstance(value, dict):
        raise ReleaseError(f"sealed JSON artifact must be an object: {label}")
    return value


def read_sealed_jsonl_row(
    spec: object, label: str, candidate_id: str
) -> tuple[dict[str, Any], str]:
    _, content = read_sealed_bytes(spec, label)
    expected_row_hash = str(spec.get("row_sha256") or "") if isinstance(spec, dict) else ""
    if not SHA256_RE.fullmatch(expected_row_hash):
        raise ReleaseError(f"sealed artifact row hash is invalid: {label}")
    matches: list[tuple[dict[str, Any], str]] = []
    for line in content.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReleaseError(f"sealed artifact is not valid JSONL: {label}") from exc
        if isinstance(row, dict) and str(row.get("candidate_id") or "") == candidate_id:
            matches.append((row, sha256_bytes(line)))
    if len(matches) != 1:
        raise ReleaseError(f"sealed artifact must contain candidate exactly once: {label}")
    row, actual_row_hash = matches[0]
    if actual_row_hash != expected_row_hash:
        raise ReleaseError(f"sealed artifact row hash mismatch: {label}")
    return row, actual_row_hash


def read_sealed_jsonl_rows(spec: object, label: str) -> list[dict[str, Any]]:
    _, content = read_sealed_bytes(spec, label)
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReleaseError(f"sealed artifact is not valid JSONL: {label}:{number}") from exc
        if not isinstance(row, dict):
            raise ReleaseError(f"sealed JSONL row must be an object: {label}:{number}")
        rows.append(row)
    return rows


def publication_identity_keys(row: dict[str, Any]) -> dict[str, str]:
    explicit = row.get("identity_keys")
    if isinstance(explicit, dict):
        return {
            "canonical_url": normalize_url(explicit.get("canonical_url")),
            "organization_stable_job_id": normalize_text(
                explicit.get("organization_stable_job_id")
            ),
            "ats_tenant_locator": normalize_text(explicit.get("ats_tenant_locator")),
            "organization_title": normalize_text(explicit.get("organization_title")),
        }
    organization = normalize_text(pick(row, "organization_name", "organization"))
    stable_id = normalize_text(pick(row, "stable_job_id", "stable_role_locator"))
    title = normalize_text(pick(row, "title", "official_title_raw"))
    return {
        "canonical_url": normalize_url(
            pick(row, "official_role_url", "title_source_url")
        ),
        "organization_stable_job_id": (
            f"{organization}|{stable_id}" if organization and stable_id else ""
        ),
        "ats_tenant_locator": normalize_text(row.get("ats_tenant_locator")),
        "organization_title": (
            f"{organization}|{title}" if organization and title else ""
        ),
    }


def sealed_antijoin_semantic_audit(
    *,
    candidate_id: str,
    candidate: dict[str, Any],
    manifest: dict[str, Any],
    required_layers: set[str],
) -> dict[str, str]:
    if manifest.get("schema_version") != "agent-hiring-map-publication-antijoin-inputs/1.0":
        raise ReleaseError("sealed four-layer anti-join manifest schema is invalid")
    layers = manifest.get("layers")
    if not isinstance(layers, dict) or set(layers) != required_layers:
        raise ReleaseError("sealed four-layer anti-join manifest is incomplete")
    candidate_keys = publication_identity_keys(candidate)
    if set(candidate_keys) != set(ANTI_JOIN_KEY_FIELDS) or any(
        not candidate_keys[field] for field in ANTI_JOIN_KEY_FIELDS
    ):
        raise ReleaseError("publication candidate lacks complete four-key anti-join identity")

    hashes: dict[str, str] = {}
    conflicts: list[str] = []
    self_layers = {"current_run_candidates_zero_conflict", "batch_zero_conflict"}
    for layer in sorted(required_layers):
        spec = layers[layer]
        _, content = read_sealed_bytes(spec, f"antijoin:{layer}")
        hashes[layer] = sha256_bytes(content)
        rows = read_sealed_jsonl_rows(spec, f"antijoin:{layer}")
        if not isinstance(spec, dict) or spec.get("row_count") != len(rows):
            raise ReleaseError(f"sealed anti-join row count mismatch: {layer}")
        references: list[str] = []
        self_count = 0
        for row in rows:
            reference = str(
                row.get("candidate_id")
                or row.get("role_id")
                or row.get("admission_id")
                or row.get("reference_id")
                or ""
            )
            if not reference:
                raise ReleaseError(f"sealed anti-join row lacks stable reference: {layer}")
            references.append(reference)
            keys = publication_identity_keys(row)
            if set(keys) != set(ANTI_JOIN_KEY_FIELDS) or any(
                not keys[field] for field in ANTI_JOIN_KEY_FIELDS
            ):
                raise ReleaseError(f"sealed anti-join row lacks complete identity keys: {layer}")
            if reference == candidate_id:
                self_count += 1
                if layer not in self_layers or keys != candidate_keys:
                    raise ReleaseError(f"sealed anti-join candidate membership mismatch: {layer}")
                continue
            for field in ANTI_JOIN_KEY_FIELDS:
                if keys[field] == candidate_keys[field]:
                    conflicts.append(f"{layer}:{field}:{reference}")
        if len(references) != len(set(references)):
            raise ReleaseError(f"sealed anti-join layer contains duplicate references: {layer}")
        if layer in self_layers and self_count != 1:
            raise ReleaseError(f"sealed anti-join layer must contain candidate exactly once: {layer}")
        if layer not in self_layers and self_count:
            raise ReleaseError(f"sealed anti-join historical layer contains current candidate: {layer}")
    if conflicts:
        raise ReleaseError(f"sealed four-layer anti-join semantic conflict: {sorted(conflicts)}")
    return hashes


def bind_sealed_evidence(raw: dict[str, Any]) -> dict[str, Any]:
    """Recompute every publication hard-gate seal from referenced artifacts."""

    candidate_id = str(raw.get("candidate_id") or "")
    sealed = raw.get("sealed_evidence")
    if not candidate_id or not isinstance(sealed, dict):
        raise ReleaseError("sealed publication evidence is required")

    sidecar, _ = read_sealed_jsonl_row(
        sealed.get("source_sidecar"), "source_sidecar", candidate_id
    )
    for field, names in {
        "stable_job_id": ("stable_job_id", "stable_role_locator"),
        "official_role_url": ("official_role_url", "title_source_url"),
        "organization": ("organization_name", "organization"),
        "title": ("title",),
        "ats_tenant_locator": ("ats_tenant_locator",),
    }.items():
        expected = pick(raw, *names)
        actual = sidecar.get(field)
        if field == "official_role_url":
            matches = normalize_url(expected) == normalize_url(actual)
        else:
            matches = normalize_text(expected) == normalize_text(actual)
        if not matches:
            raise ReleaseError(f"source sidecar identity mismatch: {field}")
    if sidecar.get("raw_html_or_full_jd_stored") is not False:
        raise ReleaseError("source sidecar raw HTML/full JD gate failed")

    pack_row, pack_row_hash = read_sealed_jsonl_row(
        sealed.get("reviewer_pack"), "reviewer_pack", candidate_id
    )
    if pack_row.get("raw_html_or_full_jd_stored") is not False:
        raise ReleaseError("reviewer pack raw HTML/full JD gate failed")
    pack_identity = {
        "stable_job_id": pick(raw, "stable_job_id", "stable_role_locator"),
        "official_role_url": pick(raw, "official_role_url", "title_source_url"),
        "organization": pick(raw, "organization_name", "organization"),
        "title": pick(raw, "title"),
        "ats_tenant_locator": pick(raw, "ats_tenant_locator"),
        "agent_specific_excerpt": raw.get("agent_specific_excerpt")
        or raw.get("agent_relevance_summary"),
    }
    for field, expected in pack_identity.items():
        actual = pack_row.get(field)
        if field == "official_role_url":
            matches = normalize_url(actual) == normalize_url(expected)
        else:
            matches = normalize_text(actual) == normalize_text(expected)
        if not matches:
            raise ReleaseError(f"reviewer pack identity mismatch: {field}")
    roster = read_sealed_json(sealed.get("reviewer_roster"), "reviewer_roster")
    candidate_ids = roster.get("candidate_ids")
    contexts = roster.get("reviewer_context_ids")
    if (
        not isinstance(candidate_ids, list)
        or candidate_id not in candidate_ids
        or not isinstance(contexts, dict)
    ):
        raise ReleaseError("reviewer roster does not seal candidate and contexts")
    roster_sealed_at = roster.get("sealed_at")

    reviewer_rows: list[dict[str, Any]] = []
    reviewer_hashes: list[str] = []
    derived_review_authority = True
    for reviewer_label in ("reviewer_a", "reviewer_b"):
        row, row_hash = read_sealed_jsonl_row(
            sealed.get(reviewer_label), reviewer_label, candidate_id
        )
        reviewer_id = str(row.get("reviewer_id") or "")
        context_id = str(row.get("execution_context_id") or "")
        is_safe_projection = (
            row.get("projection_of_sealed_prior_review") is True
            and row.get("reviewed_at_status") == "not_recorded_in_source_authority"
            and row.get("authority_predates_publication_revalidation") is True
            and SHA256_RE.fullmatch(str(row.get("source_provenance_sha256") or ""))
        )
        derived_review_authority = derived_review_authority and is_safe_projection
        if (
            row.get("verdict", row.get("decision")) != "positive"
            or row.get("independent_review") is not True
            or str(row.get("input_row_sha256") or "") != pack_row_hash
            or not reviewer_id
            or (
                not is_safe_projection
                and (contexts.get(reviewer_id) != context_id or not context_id)
            )
        ):
            raise ReleaseError(f"sealed Reviewer decision linkage failed: {reviewer_label}")
        reviewer_rows.append(row)
        reviewer_hashes.append(row_hash)
    sealed_duty_quotes = pack_row.get("reviewer_duty_quotes")
    if not isinstance(sealed_duty_quotes, list):
        sealed_duty_quotes = [pack_row.get("agent_specific_excerpt")]
    if (
        not sealed_duty_quotes
        or any(
            not isinstance(quote, str)
            or not quote.strip()
            or len(quote) > 300
            or HTML_OR_ENTITY_RE.search(quote)
            for quote in sealed_duty_quotes
        )
    ):
        raise ReleaseError("sealed reviewer duty evidence is unsafe")
    for reviewer_label, reviewer_row in zip(("reviewer_a", "reviewer_b"), reviewer_rows):
        quote = str(reviewer_row.get("evidence_quote") or "").strip()
        if not quote or len(quote) > 300 or HTML_OR_ENTITY_RE.search(quote):
            raise ReleaseError("reviewer evidence quote is unsafe or exceeds public minimum")
        if quote not in sealed_duty_quotes:
            raise ReleaseError(
                f"sealed Reviewer quote is not linked to official duty evidence: {reviewer_label}"
            )
    if derived_review_authority:
        if not (
            roster_sealed_at is None
            and roster.get("sealed_at_status") == "not_recorded_in_source_authority"
            and roster.get("projection_of_sealed_prior_review") is True
        ):
            raise ReleaseError("sealed prior Reviewer roster timing projection is incomplete")
    else:
        parse_observed_at(roster_sealed_at, "roster_sealed_at")

    live, _ = read_sealed_jsonl_row(sealed.get("live_check"), "live_check", candidate_id)
    if (
        live.get("status") != "open"
        or live.get("official_source") is not True
        or live.get("official_specific_job") is not True
        or live.get("public_readable") is not True
        or live.get("actionable_apply") is not True
        or live.get("raw_html_or_full_jd_stored") is not False
    ):
        raise ReleaseError("sealed live check hard gates failed")
    for field, expected in {
        "title_observed": pick(raw, "title"),
        "stable_job_id_observed": pick(raw, "stable_job_id", "stable_role_locator"),
        "organization_observed": pick(raw, "organization_name", "organization"),
    }.items():
        actual = live.get(field)
        if not isinstance(actual, str) or not actual.strip():
            raise ReleaseError(f"sealed live check observed identity missing: {field}")
        if normalize_text(actual) != normalize_text(expected):
            raise ReleaseError(f"sealed live check observed identity mismatch: {field}")

    antijoin, _ = read_sealed_jsonl_row(
        sealed.get("antijoin_decision"), "antijoin_decision", candidate_id
    )
    if (
        antijoin.get("zero_duplicate") is not True
        or antijoin.get("anti_join_conflicts") not in ([], None)
        or antijoin.get("final_pre_sidecar_disposition") != "eligible"
    ):
        raise ReleaseError("sealed anti-join decision failed")
    for field, expected in {
        "stable_job_id": pick(raw, "stable_job_id", "stable_role_locator"),
        "official_role_url": pick(raw, "official_role_url", "title_source_url"),
        "organization": pick(raw, "organization_name", "organization"),
        "title": pick(raw, "title"),
        "ats_tenant_locator": pick(raw, "ats_tenant_locator"),
    }.items():
        actual = antijoin.get(field)
        if field == "official_role_url":
            matches = normalize_url(actual) == normalize_url(expected)
        else:
            matches = normalize_text(actual) == normalize_text(expected)
        if not matches:
            raise ReleaseError(f"sealed anti-join identity mismatch: {field}")
    manifest = read_sealed_json(
        sealed.get("antijoin_input_manifest"), "antijoin_input_manifest"
    )
    required_layers = {
        "canonical_roles_zero_conflict",
        "prior_sidecars_zero_conflict",
        "current_run_candidates_zero_conflict",
        "batch_zero_conflict",
    }
    antijoin_hashes = sealed_antijoin_semantic_audit(
        candidate_id=candidate_id,
        candidate=raw,
        manifest=manifest,
        required_layers=required_layers,
    )
    if antijoin.get("input_sha256") != antijoin_hashes:
        raise ReleaseError("sealed anti-join decision input hashes do not match artifacts")

    def reviewer_projection(row: dict[str, Any], row_hash: str) -> dict[str, Any]:
        return {
            "reviewer_id": row["reviewer_id"],
            "execution_context_id": row.get("execution_context_id"),
            "verdict": "positive",
            "lane": row.get("lane") or row.get("role_lane"),
            "evidence_quote": row.get("evidence_quote"),
            "reviewed_at": row.get("reviewed_at"),
            "input_sha256": pack_row_hash,
            "decision_sha256": row_hash,
            "reviewed_at_status": row.get("reviewed_at_status"),
            "authority_predates_publication_revalidation": row.get(
                "authority_predates_publication_revalidation"
            ),
        }

    return {
        "source_sidecar": sidecar,
        "verification": live,
        "reviewers": {
            "independent": True,
            "roster_sealed_before_review": True,
            "roster_sealed_at": roster_sealed_at,
            "timing_mode": (
                "sealed_prior_review_without_exact_timestamp"
                if derived_review_authority
                else "exact_recorded_timestamps"
            ),
            "a": reviewer_projection(reviewer_rows[0], reviewer_hashes[0]),
            "b": reviewer_projection(reviewer_rows[1], reviewer_hashes[1]),
        },
        "strict_four_layer_antijoin": {
            **{layer: True for layer in required_layers},
            "input_sha256": antijoin_hashes,
        },
    }


def normalize_admission(raw: dict[str, Any], release_date: date) -> dict[str, Any]:
    for key, value in nested_values(raw):
        if key.casefold() in FORBIDDEN_PAYLOAD_KEYS and value not in (None, "", [], {}):
            raise ReleaseError(f"forbidden full-description field: {key}")
    if raw.get("raw_html_or_full_jd_stored") is not False:
        raise ReleaseError("raw_html_or_full_jd_stored must be false")

    sealed = bind_sealed_evidence(raw)

    verification = sealed["verification"]
    if not isinstance(verification, dict):
        raise ReleaseError("missing verification object")
    if (
        verification.get("status") != "open"
        or verification.get("official_source") is not True
        or verification.get("official_specific_job") is not True
        or verification.get("public_readable") is not True
        or verification.get("actionable_apply") is not True
        or verification.get("raw_html_or_full_jd_stored") is not False
    ):
        raise ReleaseError("official open hard gates failed")
    checked_at = parse_observed_at(verification.get("checked_at"), "checked_at")
    if checked_at.date() != release_date:
        raise ReleaseError("open verification is not from the release date")

    reviewers = sealed["reviewers"]
    if (
        not isinstance(reviewers, dict)
        or reviewers.get("independent") is not True
        or reviewers.get("roster_sealed_before_review") is not True
    ):
        raise ReleaseError("Reviewer A/B independence and pre-review roster seal required")
    reviewer_a = reviewers.get("a") or reviewers.get("reviewer_a") or {}
    reviewer_b = reviewers.get("b") or reviewers.get("reviewer_b") or {}
    if reviewer_a.get("verdict") != "positive" or reviewer_b.get("verdict") != "positive":
        raise ReleaseError("dual positive Reviewer A/B decisions required")
    if not reviewer_a.get("evidence_quote") or not reviewer_b.get("evidence_quote"):
        raise ReleaseError("both reviewers require exact evidence quotes")
    reviewer_ids = [str(reviewer_a.get("reviewer_id") or ""), str(reviewer_b.get("reviewer_id") or "")]
    reviewer_context_ids = [
        str(reviewer_a.get("execution_context_id") or ""),
        str(reviewer_b.get("execution_context_id") or ""),
    ]
    decision_hashes = [
        str(reviewer_a.get("decision_sha256") or ""),
        str(reviewer_b.get("decision_sha256") or ""),
    ]
    input_hashes = [
        str(reviewer_a.get("input_sha256") or ""),
        str(reviewer_b.get("input_sha256") or ""),
    ]
    if (
        not all(reviewer_ids)
        or reviewer_ids[0] == reviewer_ids[1]
        or (
            reviewers.get("timing_mode") == "exact_recorded_timestamps"
            and (not all(reviewer_context_ids) or reviewer_context_ids[0] == reviewer_context_ids[1])
        )
        or not all(SHA256_RE.fullmatch(value) for value in decision_hashes + input_hashes)
        or decision_hashes[0] == decision_hashes[1]
        or input_hashes[0] != input_hashes[1]
    ):
        raise ReleaseError("Reviewer A/B identities, contexts, or cryptographic seals are not independent")
    lanes = [str(reviewer_a.get("lane") or ""), str(reviewer_b.get("lane") or "")]
    if lanes[0] not in {"A", "B", "C"} or lanes[0] != lanes[1]:
        raise ReleaseError("Reviewer A/B must independently agree on the same A/B/C role lane")
    release_end = datetime.combine(release_date, time.max, timezone.utc)
    if reviewers.get("timing_mode") == "exact_recorded_timestamps":
        roster_sealed_at = parse_observed_at(
            reviewers.get("roster_sealed_at") or raw.get("roster_sealed_at"),
            "roster_sealed_at",
        )
        reviewed_times = [
            parse_observed_at(reviewer.get("reviewed_at"), "reviewed_at")
            for reviewer in (reviewer_a, reviewer_b)
        ]
        if roster_sealed_at > min(reviewed_times) or max(reviewed_times) > checked_at:
            raise ReleaseError(
                "timestamp chain must satisfy roster_sealed_at <= reviewed_at(A/B) <= checked_at"
            )
    elif reviewers.get("timing_mode") == "sealed_prior_review_without_exact_timestamp":
        if not all(
            reviewer.get("reviewed_at_status") == "not_recorded_in_source_authority"
            and reviewer.get("authority_predates_publication_revalidation") is True
            for reviewer in (reviewer_a, reviewer_b)
        ):
            raise ReleaseError("sealed prior Reviewer timing projection is incomplete")
    else:
        raise ReleaseError("Reviewer timing authority is invalid")
    if checked_at > release_end:
        raise ReleaseError("open verification occurs after release_end")

    ttl_value = raw.get("ttl_days")
    if ttl_value is None:
        ttl_value = verification.get("ttl_days")
    if isinstance(ttl_value, bool) or not isinstance(ttl_value, int) or not 1 <= ttl_value <= 14:
        raise ReleaseError("ttl_days must be an integer from 1 through 14")
    next_check_value = (
        raw.get("currentness_next_check_at")
        or raw.get("next_check_at")
        or verification.get("next_check_at")
    )
    declared_next_check_at = parse_observed_at(next_check_value, "next_check_at")
    if declared_next_check_at <= checked_at:
        raise ReleaseError("next_check_at must be later than checked_at")
    ttl_deadline = checked_at + timedelta(days=ttl_value)
    effective_next_check_at = min(declared_next_check_at, ttl_deadline)

    title = str(pick(raw, "title") or "").strip()
    stable_locator = str(pick(raw, "stable_job_id", "stable_role_locator") or "").strip()
    official_url = normalize_url(pick(raw, "official_role_url", "title_source_url"))
    organization_name = str(
        pick(raw, "organization_name", "organization") or ""
    ).strip()
    candidate_id = str(raw.get("candidate_id") or "").strip()
    ats_tenant_locator = str(raw.get("ats_tenant_locator") or "").strip()
    excerpt = str(
        raw.get("agent_specific_excerpt") or raw.get("agent_relevance_summary") or ""
    ).strip()
    if not all(
        (
            candidate_id,
            title,
            stable_locator,
            official_url,
            organization_name,
            ats_tenant_locator,
            excerpt,
        )
    ):
        raise ReleaseError("admission identity or Agent-duty evidence is incomplete")
    if len(excerpt) > 300 or HTML_OR_ENTITY_RE.search(excerpt):
        raise ReleaseError("Agent excerpt is too long or contains HTML")
    reviewer_quotes = [str(reviewer_a["evidence_quote"]), str(reviewer_b["evidence_quote"])]
    if any(not quote.strip() or len(quote) > 300 or HTML_OR_ENTITY_RE.search(quote) for quote in reviewer_quotes):
        raise ReleaseError("reviewer evidence quote is unsafe or exceeds public minimum")
    # Both independent Reviewer quotes remain sealed and individually checked.
    # The public excerpt is intentionally a <=300-character minimum, so it
    # needs verbatim continuity with at least one Reviewer quote; requiring it
    # to concatenate two distinct valid quotes would force excess JD text into
    # the public package.
    if not any(quote.strip() in excerpt for quote in reviewer_quotes):
        raise ReleaseError("public Agent-duty excerpt is not linked to either sealed reviewer quote")
    if normalize_url(verification.get("official_role_url") or verification.get("final_url")) != official_url:
        raise ReleaseError("verification URL does not match admission identity")
    observed_title = str(verification.get("title_observed") or "")
    if not observed_title.strip():
        raise ReleaseError("verification observed title is required")
    if normalize_text(observed_title) != normalize_text(title):
        raise ReleaseError("verification title does not match admission identity")
    observed_stable = str(verification.get("stable_job_id_observed") or "")
    if not observed_stable.strip():
        raise ReleaseError("verification observed stable ID is required")
    if normalize_text(observed_stable) != normalize_text(stable_locator):
        raise ReleaseError("verification stable ID does not match admission identity")
    observed_organization = str(verification.get("organization_observed") or "")
    if not observed_organization.strip():
        raise ReleaseError("verification observed organization is required")
    if normalize_text(observed_organization) != normalize_text(organization_name):
        raise ReleaseError("verification organization does not match admission identity")

    antijoin = sealed["strict_four_layer_antijoin"]
    required_antijoin_layers = {
        "canonical_roles_zero_conflict",
        "prior_sidecars_zero_conflict",
        "current_run_candidates_zero_conflict",
        "batch_zero_conflict",
    }
    if not isinstance(antijoin, dict) or any(
        antijoin.get(field) is not True for field in required_antijoin_layers
    ):
        raise ReleaseError("strict canonical/sidecar/current-run/batch anti-join proof required")
    antijoin_hashes = antijoin.get("input_sha256")
    if not isinstance(antijoin_hashes, dict) or set(antijoin_hashes) != required_antijoin_layers:
        raise ReleaseError("strict four-layer anti-join input hashes are incomplete")
    if not all(SHA256_RE.fullmatch(str(value or "")) for value in antijoin_hashes.values()):
        raise ReleaseError("strict four-layer anti-join input hashes are invalid")

    display_title_zh = str(pick(raw, "display_title_zh") or "").strip()
    display_title_en = str(pick(raw, "display_title_en") or "").strip()
    if not display_title_zh or not display_title_en or re.search(r"[\u4e00-\u9fff]", display_title_en):
        raise ReleaseError("honest non-empty Chinese/English display titles required")
    geography = str(pick(raw, "geography", default=(raw.get("provenance") or {}).get("region")) or "").strip()
    if not geography:
        raise ReleaseError("geography is required")
    release_cohort = str(raw.get("release_cohort") or "")
    if release_cohort not in RELEASE_COHORTS:
        raise ReleaseError("release_cohort is required and must be recognized")
    if release_cohort == "china_main1_restricted_new_admission" and geography != "China":
        raise ReleaseError("new main-1 restricted admissions must be China-only")
    if release_cohort == "historical_local_overlay_revalidation" and geography not in {"China", "United States"}:
        raise ReleaseError("historical overlay cohort escaped its frozen geography set")

    location_status = str(pick(raw, "location_data_status", default="pending_review"))
    job_locations = list(pick(raw, "job_locations", default=[]) or [])
    location_zh = str(pick(raw, "display_location_zh", default="地点待复核"))
    location_en = str(pick(raw, "display_location_en", default="Location pending review"))
    if location_status == "pending_review":
        job_locations, location_zh, location_en = [], "地点待复核", "Location pending review"
    elif location_status == "company_or_context_only":
        job_locations = []
        location_zh = "岗位地点待复核（来源仅列出公司或团队地点）"
        location_en = "Role location pending review (source only lists company or team locations)"
    elif location_status in {"normalized_or_descriptive", "official_role_title_location_reviewed"}:
        if not location_zh or not location_en:
            raise ReleaseError("verified location requires bilingual display")
        job_locations = [location_en]
    else:
        raise ReleaseError("invalid location_data_status")

    arrangement = str(pick(raw, "work_arrangement", default="onsite"))
    basis = str(
        pick(raw, "work_arrangement_basis", default="default_onsite_no_remote_signal")
    )
    allowed_arrangements = {
        ("onsite", "explicit_onsite"),
        ("onsite", "default_onsite_no_remote_signal"),
        ("remote_or_hybrid", "explicit_remote_or_hybrid"),
    }
    if (arrangement, basis) not in allowed_arrangements:
        raise ReleaseError("invalid work arrangement/basis pair")

    domains = raw.get("organization_official_domains") or []
    if isinstance(domains, str):
        domains = [domains]
    domains = sorted({str(item).casefold().strip() for item in domains if str(item).strip()})
    for domain in domains:
        if "://" in domain or "/" in domain or normalize_url(f"https://{domain}") != f"https://{domain}/":
            raise ReleaseError("organization_official_domains must contain hostnames only")

    team_name = str(pick(raw, "team_name") or "").strip()
    product_name = str(pick(raw, "product_name") or "").strip()
    if not team_name or not product_name:
        raise ReleaseError("canonical team_name and product_name are required")

    return {
        "candidate_id": candidate_id,
        "stable_locator": stable_locator,
        "ats_tenant_locator": ats_tenant_locator,
        "official_url": official_url,
        "organization_name": organization_name,
        "canonical_organization_id": raw.get("canonical_organization_id"),
        "organization_domains": domains,
        "team_name": team_name,
        "canonical_team_id": raw.get("canonical_team_id"),
        "product_name": product_name,
        "canonical_product_id": raw.get("canonical_product_id"),
        "product_official_url": normalize_url(raw.get("product_official_url")) or None,
        "title": title,
        "display_title_zh": display_title_zh,
        "display_title_en": display_title_en,
        "title_source_language": str(raw.get("title_source_language") or ("zh" if re.search(r"[\u4e00-\u9fff]", title) else "en")),
        "title_translation_status": str(raw.get("title_translation_status") or "verified_translation"),
        "geography": geography,
        "job_locations": job_locations,
        "display_location_zh": location_zh,
        "display_location_en": location_en,
        "location_data_status": location_status,
        "work_arrangement": arrangement,
        "work_arrangement_basis": basis,
        "role_family": str(pick(raw, "role_family") or "agent_role_continuous_new_discovery"),
        "agent_excerpt": excerpt,
        "first_seen_at": str(raw.get("first_seen_at") or release_date.isoformat())[:10],
        "release_date": release_date.isoformat(),
        "release_cohort": release_cohort,
        "checked_at": checked_at.isoformat().replace("+00:00", "Z"),
        "ttl_days": ttl_value,
        "currentness_next_check_at": effective_next_check_at.isoformat().replace(
            "+00:00", "Z"
        ),
    }


def unique_match(rows: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    matches = [row for row in rows if normalize_text(row.get(key)) == normalize_text(value)]
    if len(matches) > 1:
        raise ReleaseError(f"ambiguous {key}: {value}")
    return matches[0] if matches else None


def resolve_organization(
    admission: dict[str, Any], organizations: list[dict[str, Any]], evidence_id: str
) -> tuple[dict[str, Any], bool]:
    wanted = normalize_text(admission["organization_name"])
    matches = []
    for row in organizations:
        names = [row.get("canonical_name"), *(row.get("aliases") or [])]
        if wanted in {normalize_text(name) for name in names}:
            matches.append(row)
    if len(matches) > 1:
        raise ReleaseError(f"ambiguous organization alias: {admission['organization_name']}")
    if matches:
        row = matches[0]
        claimed = admission.get("canonical_organization_id")
        if claimed and claimed != row["organization_id"]:
            raise ReleaseError("claimed canonical organization ID disagrees with alias audit")
        supplied = set(admission["organization_domains"])
        existing = {str(item).casefold() for item in row.get("official_domains") or []}
        owners = {
            other["organization_id"]
            for other in organizations
            if other["organization_id"] != row["organization_id"]
            and supplied.intersection(
                {str(item).casefold() for item in other.get("official_domains") or []}
            )
        }
        if owners:
            raise ReleaseError("official domain is already owned by another organization")
        if supplied and existing and supplied.isdisjoint(existing):
            raise ReleaseError("organization domain disagrees with canonical entity")
        if not claimed and (not supplied or not existing or supplied.isdisjoint(existing)):
            raise ReleaseError(
                "existing organization requires an exact canonical ID or matching official domain"
            )
        return row, False
    if admission.get("canonical_organization_id"):
        raise ReleaseError("claimed canonical organization ID was not found")
    if not admission["organization_domains"]:
        raise ReleaseError("new organization requires an audited official domain")
    supplied = set(admission["organization_domains"])
    if any(
        supplied.intersection(
            {str(item).casefold() for item in row.get("official_domains") or []}
        )
        for row in organizations
    ):
        raise ReleaseError("official domain is already owned by another organization")
    org_id = stable_id("ORG", admission["organization_name"])
    if any(row["organization_id"] == org_id for row in organizations):
        raise ReleaseError("new organization stable ID collision")
    return {
        "schema_version": PUBLIC_SCHEMA,
        "organization_id": org_id,
        "canonical_name": admission["organization_name"],
        "group_id": None,
        "official_domains": admission["organization_domains"],
        "geography": [admission["geography"]],
        "aliases": [admission["organization_name"]],
        "status": "active",
        "confidence": 1.0,
        "evidence_ids": [evidence_id],
        "version": 1,
    }, True


def resolve_child(
    kind: str,
    admission: dict[str, Any],
    rows: list[dict[str, Any]],
    organization_id: str,
    evidence_id: str,
) -> tuple[dict[str, Any], bool]:
    id_key = f"{kind}_id"
    name_key = "team_name" if kind == "team" else "name"
    admission_name = admission["team_name" if kind == "team" else "product_name"]
    matches = [
        row
        for row in rows
        if row.get("organization_id") == organization_id
        and normalize_text(row.get(name_key)) == normalize_text(admission_name)
    ]
    if len(matches) > 1:
        raise ReleaseError(f"ambiguous canonical {kind}")
    claimed = admission.get(f"canonical_{kind}_id")
    if matches:
        if claimed and claimed != matches[0][id_key]:
            raise ReleaseError(f"claimed canonical {kind} ID disagrees with name audit")
        return matches[0], False
    if claimed:
        raise ReleaseError(f"claimed canonical {kind} ID was not found")
    prefix = "TEAM" if kind == "team" else "PROD"
    object_id = stable_id(prefix, organization_id, admission_name)
    if any(row[id_key] == object_id for row in rows):
        raise ReleaseError(f"new {kind} stable ID collision")
    if kind == "team":
        return {
            "schema_version": PUBLIC_SCHEMA,
            "team_id": object_id,
            "organization_id": organization_id,
            "team_name": admission_name,
            "product_ids": [],
            "team_geography": [admission["geography"]],
            "status": "active",
            "confidence": 1.0,
            "evidence_ids": [evidence_id],
            "version": 1,
        }, True
    return {
        "schema_version": PUBLIC_SCHEMA,
        "product_id": object_id,
        "organization_id": organization_id,
        "name": admission_name,
        "agent_category": "agent_product_or_work_surface",
        "official_url": admission["product_official_url"],
        "status": "active",
        "confidence": 1.0,
        "evidence_ids": [evidence_id],
        "version": 1,
    }, True


def evidence_row(admission: dict[str, Any], evidence_id: str) -> dict[str, Any]:
    return {
        "schema_version": PUBLIC_SCHEMA,
        "evidence_id": evidence_id,
        "geography_bucket": admission["geography"] if admission["geography"] in {"China", "United States", "Other/Global", "Unknown"} else "Unknown",
        "coverage_scope": "canonical_map_scope",
        "organization_observed": admission["organization_name"],
        "parent_organization_inferred": "",
        "product_or_work_surface": admission["product_name"],
        "source_class": "official_or_first_party",
        "source_urls": [admission["official_url"]],
        "attribution": admission["organization_name"],
        "access_requirement": "public_no_login",
        "observed_at": admission["release_date"],
        "evidence_grade": "A",
        "evidence_kind": "role_signal",
        "public_excerpt": admission["agent_excerpt"],
        "quote_publication_status": "minimal_attributed_excerpt",
        "limitations": ["continuous_new_role_discovery", "minimal_role_duty_excerpt_only"],
    }


def role_row(
    admission: dict[str, Any], evidence_id: str, org_id: str, team_id: str, product_id: str
) -> dict[str, Any]:
    role_id = stable_id("ROLE", org_id, admission["stable_locator"], admission["official_url"])
    decision = {
        "candidate_id": admission["candidate_id"],
        "role_id": role_id,
        "official_url": admission["official_url"],
        "release_date": admission["release_date"],
        "evidence_id": evidence_id,
        "disposition": "publish_current",
        "release_cohort": admission["release_cohort"],
    }
    return {
        "access_requirement": "public_no_login",
        "agent_relevance_evidence_type": "continuous_new_role_exact_official_duty",
        "agent_relevance_summary": admission["agent_excerpt"],
        "agent_specific_quote": admission["agent_excerpt"],
        "citation_supports_title": True,
        "currentness_next_check_at": admission["currentness_next_check_at"],
        "currentness_status": "current_verified",
        "currentness_terminal": "open_verified",
        "decision_sha256": sha256_bytes(stable_json(decision).encode()),
        "display_location_en": admission["display_location_en"],
        "display_location_zh": admission["display_location_zh"],
        "display_title_en": admission["display_title_en"],
        "display_title_zh": admission["display_title_zh"],
        "eligible_for_job_list": True,
        "eligible_for_strict_current": True,
        "evidence_exhausted": False,
        "evidence_grade": "A",
        "evidence_ids": [evidence_id],
        "first_seen_at": admission["first_seen_at"],
        "geography": admission["geography"],
        "job_locations": admission["job_locations"],
        "last_seen_at": admission["release_date"],
        "last_verified_at": admission["release_date"],
        "location_data_status": admission["location_data_status"],
        "official_role_url": admission["official_url"],
        "official_title_raw": admission["title"],
        "organization_id": org_id,
        "product_id": product_id,
        "public_confidence_tier": "verified",
        "public_disposition": "publish_current",
        "public_disposition_reason_code": "continuous_new_role_all_hard_gates_pass",
        "public_is_current": True,
        "publication_state_version": PUBLICATION_VERSION,
        "recovery_origin": "continuous_new_role_discovery",
        "remote_scope": None,
        "role_display_version": ROLE_DISPLAY_VERSION,
        "role_family": admission["role_family"],
        "role_id": role_id,
        "role_recovery_confidence": 1.0,
        "role_recovery_status": "verified_job",
        "schema_version": PUBLIC_SCHEMA,
        "source_role_descriptor": None,
        "stable_role_locator": admission["stable_locator"],
        "supersedes_role_id": None,
        "team_id": team_id,
        "title": admission["title"],
        "title_authenticity_version": TITLE_VERSION,
        "title_current_eligible_after_gate": True,
        "title_provenance": "official_current_role_detail",
        "title_source_granularity": "direct_role_detail",
        "title_source_language": admission["title_source_language"],
        "title_source_observation_status": "fetched_success",
        "title_source_observed_at": admission["release_date"],
        "title_source_recheck_attempted_at": admission["release_date"],
        "title_source_recheck_performed": True,
        "title_source_url": admission["official_url"],
        "title_support_status": "verified_official_title",
        "title_translation_status": admission["title_translation_status"],
        "version": 1,
        "work_arrangement": admission["work_arrangement"],
        "work_arrangement_basis": admission["work_arrangement_basis"],
    }


def project_current(
    role: dict[str, Any], previous: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Project one publishable canonical Role into the sole Current shape."""

    previous = previous or {}
    geography = role.get("geography") or previous.get("geography")
    excerpt = str(
        role.get("agent_specific_quote") or role.get("agent_relevance_summary") or ""
    ).strip()[:300]
    if not isinstance(geography, str) or not geography.strip() or not excerpt:
        raise ReleaseError(f"Role cannot be projected to Current: {role.get('role_id')}")
    if role.get("recovery_origin") == "continuous_new_role_discovery":
        limitations = [
            "bounded_public_source_validation_not_market_complete",
            "continuous_new_role_discovery_release",
        ]
    else:
        limitations = previous.get("limitations")
        if not isinstance(limitations, list):
            raise ReleaseError(
                f"historical Role lacks sealed Current limitations: {role.get('role_id')}"
            )
    return {
        "access_requirement": role["access_requirement"],
        "agent_specific_excerpt": excerpt,
        "citation_supports_title": role["citation_supports_title"],
        "currentness_status": role["currentness_status"],
        "display_title_en": role["display_title_en"],
        "display_title_zh": role["display_title_zh"],
        "evidence_grade": "A",
        "evidence_ids": role["evidence_ids"],
        "geography": geography,
        "last_verified_at": role["last_verified_at"],
        "limitations": limitations,
        "organization_id": role["organization_id"],
        "product_id": role["product_id"],
        "role_id": role["role_id"],
        "schema_version": PUBLIC_SCHEMA,
        "source_urls": [normalize_url(role["official_role_url"])],
        "team_id": role["team_id"],
        "title": role["official_title_raw"],
        "title_source_granularity": role["title_source_granularity"],
        "title_source_url": role["title_source_url"],
        "title_support_status": role["title_support_status"],
        "title_translation_status": role["title_translation_status"],
    }


def assert_unique_ids(rows: list[dict[str, Any]], key: str, dataset: str) -> None:
    values = [row.get(key) for row in rows]
    if any(not value for value in values) or len(values) != len(set(values)):
        raise ReleaseError(f"{dataset} contains missing or duplicate {key}")


def relation(subject: str, predicate: str, obj: str, evidence_id: str) -> dict[str, Any]:
    return {
        "schema_version": PUBLIC_SCHEMA,
        "relation_id": stable_id("REL", subject, predicate, obj),
        "subject_id": subject,
        "predicate": predicate,
        "object_id": obj,
        "status": "active",
        "confidence": 1.0,
        "evidence_ids": [evidence_id],
        "version": 1,
    }


def append_relation(
    rows: list[dict[str, Any]], subject: str, predicate: str, obj: str, evidence_id: str
) -> bool:
    key = (subject, predicate, obj)
    if any((row["subject_id"], row["predicate"], row["object_id"]) == key for row in rows):
        return False
    candidate = relation(subject, predicate, obj, evidence_id)
    if any(row["relation_id"] == candidate["relation_id"] for row in rows):
        raise ReleaseError("relation stable ID collision")
    rows.append(candidate)
    return True


def replace_unique(
    text: str,
    pattern: str,
    replacement: str,
    label: str,
    *,
    flags: int = 0,
) -> str:
    """Replace one semantically labelled projection and fail on drift/ambiguity."""

    projected, count = re.subn(pattern, replacement, text, flags=flags)
    if count != 1:
        raise ReleaseError(f"snapshot projection {label} expected one match, found {count}")
    return projected


def replace_section(text: str, heading: str, next_heading: str, body: str) -> str:
    pattern = rf"(?ms)^{re.escape(heading)}\n.*?(?=^{re.escape(next_heading)}\n)"
    replacement = f"{heading}\n\n{body.rstrip()}\n\n"
    return replace_unique(text, pattern, replacement, heading, flags=re.M | re.S)


def geography_label(value: str) -> str:
    return {
        "China": "中国",
        "United States": "美国",
        "Unknown": "地域待复核",
    }.get(value, value)


def snapshot_projection(rows: dict[str, list[dict[str, Any]]], metadata: dict[str, Any]) -> dict[str, Any]:
    roles = rows["roles"]
    current = rows["current"]
    confidence = Counter(row["public_confidence_tier"] for row in roles)
    origin = Counter(row["recovery_origin"] for row in roles)
    location = Counter(row["location_data_status"] for row in roles)
    arrangement = Counter(row["work_arrangement"] for row in roles)
    arrangement_basis = Counter(row["work_arrangement_basis"] for row in roles)
    geography = Counter(row["geography"] for row in current)
    current_teams = len({row["team_id"] for row in current})
    verified = confidence.get("verified", 0)
    probable = confidence.get("probable", 0)
    return {
        "evidence": len(rows["evidence"]),
        "organizations": len(rows["organizations"]),
        "teams": len(rows["teams"]),
        "products": len(rows["products"]),
        "roles": len(roles),
        "relations": len(rows["relations"]),
        "current": len(current),
        "review": int(metadata["review_queue_rows"]),
        "verified": verified,
        "probable": probable,
        "noncurrent": len(roles) - len(current),
        "verified_noncurrent": verified - len(current),
        "current_teams": current_teams,
        "teams_without_current": len(rows["teams"]) - current_teams,
        "incremental_roles": origin.get("continuous_new_role_discovery", 0),
        "baseline_roles": len(roles) - origin.get("continuous_new_role_discovery", 0),
        "location": location,
        "arrangement": arrangement,
        "arrangement_basis": arrangement_basis,
        "current_geography": geography,
    }


def replace_snapshot_tokens(
    output: Path,
    before: dict[str, int],
    after: dict[str, int],
    release: str,
    snapshot: dict[str, Any],
) -> None:
    """Project current machine facts into bounded documentation regions.

    ``before``/``after`` remain explicit inputs so callers cannot accidentally
    invoke this outside an incremental build.  Numeric values are never used as
    search keys: historical paragraphs can legitimately contain the same
    numbers as the current snapshot.
    """

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
    if any(after.get(key) != snapshot.get(key) for key in count_keys):
        raise ReleaseError("snapshot projection does not match release delta")
    paths = {
        "readme": output / "README.md",
        "scale": output / "docs" / "DATA_SCALE_AND_SCOPE.md",
        "maintenance": output / "docs" / "MAINTENANCE.md",
        "dictionary": output / "docs" / "DATA_DICTIONARY.md",
        "methodology": output / "docs" / "METHODOLOGY.md",
    }
    existing = {name: path.exists() for name, path in paths.items()}
    if not any(existing.values()):
        # Minimal unit fixtures do not carry the public documentation surface.
        return
    if not all(existing.values()):
        missing = sorted(name for name, present in existing.items() if not present)
        raise ReleaseError(f"snapshot projection document set incomplete: {missing}")

    evidence = snapshot["evidence"]
    roles = snapshot["roles"]
    verified = snapshot["verified"]
    probable = snapshot["probable"]
    current = snapshot["current"]

    readme_path = paths["readme"]
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_unique(
        readme,
        r"(?m)^- [0-9,]+ 条\*\*安全证据索引\*\*；$",
        f"- {evidence:,} 条**安全证据索引**；",
        "README evidence bullet",
    )
    readme = replace_unique(
        readme,
        r"(?m)^- 全球公开来源有界恢复(?:和本轮|、)存量公开完整性终审(?:后的|和持续发现准入后的) .*高概率岗位；$",
        f"- 全球公开来源有界恢复、存量公开完整性终审和持续发现准入后的 {roles:,} 条岗位记录：{verified:,} 条已核实岗位、{probable:,} 条高概率岗位；",
        "README role tier bullet",
    )
    readme = replace_unique(
        readme,
        r"(?m)^- [0-9,]+ 条经 \d{4}-\d{2}-\d{2} .*严格当前岗位；$",
        f"- {current:,} 条经 {release} 正式复核、从全部 {roles:,} 条唯一处置直接投影并通过十项 Current 硬门的严格当前岗位；",
        "README Current bullet",
    )
    readme = replace_unique(
        readme,
        r"(?m)^> 重要：[0-9,]+ 是历史证据行数，不是当前岗位数、招聘人数或市场规模。",
        f"> 重要：{evidence:,} 是历史证据行数，不是当前岗位数、招聘人数或市场规模。",
        "README evidence disclaimer",
    )
    readme_path.write_text(readme, encoding="utf-8")

    scale_path = paths["scale"]
    scale = scale_path.read_text(encoding="utf-8")
    scale = replace_unique(
        scale,
        r"(?m)^数据快照：\d{4}-\d{2}-\d{2}$",
        f"数据快照：{release}",
        "scale release date",
    )
    overview = "\n".join(
        (
            "```text",
            f"{evidence:,} 条证据",
            "→ 其中 4,643 条 Other/Global/Unknown 线索完成历史恢复裁决",
            f"→ 全站共有 {roles:,} 个岗位",
            f"→ 其中 {verified:,} 个已核实",
            f"→ 其中 {current:,} 个确认当前开放",
            f"→ 分布在 {snapshot['current_teams']:,} 个有当前岗位的团队",
            "```",
            "",
            "证据、岗位、组织、团队、产品和关系是不同类型的对象，不能放进同一个漏斗直接相减。",
        )
    )
    scale = replace_section(scale, "## 一句话总览", "## 1. 总体规模", overview)

    section_one_matches = list(
        re.finditer(r"(?ms)^## 1\. 总体规模\n.*?(?=^## 2\.)", scale)
    )
    if len(section_one_matches) != 1:
        raise ReleaseError(
            "snapshot projection scale section 1 expected one match, "
            f"found {len(section_one_matches)}"
        )
    section_one_match = section_one_matches[0]
    section_one = section_one_match.group(0)
    for pattern, replacement, label in (
        (r"(?m)^\| [0-9,]+ \| 关系 \|", f"| {snapshot['relations']:,} | 关系 |", "scale relations row"),
        (r"(?m)^\| [0-9,]+ \| Evidence Ledger \|", f"| {evidence:,} | Evidence Ledger |", "scale evidence row"),
        (
            r"(?m)^\| [0-9,]+ \| 其他证据 \| `[^`]+`，",
            f"| {evidence - 4_643:,} | 其他证据 | `{evidence:,} - 4,643`，",
            "scale other evidence row",
        ),
    ):
        section_one = replace_unique(section_one, pattern, replacement, label)
    scale = scale[: section_one_match.start()] + section_one + scale[section_one_match.end() :]

    role_body = "\n".join(
        (
            "```text",
            f"{roles:,} 个岗位",
            f"├── {verified:,} 个已核实岗位",
            f"│   ├── {current:,} 个严格当前岗位",
            f"│   └── {snapshot['verified_noncurrent']:,} 个已核实但不在当前视图",
            f"└── {probable:,} 个高概率岗位",
            "    └── 0 个进入严格当前视图",
            "```",
            "",
            "| 数字 | 对象 | 定义 |",
            "| ---: | --- | --- |",
            f"| {roles:,} | 全部岗位记录 | 去重后的正式 Role；其中 {snapshot['baseline_roles']:,} 条来自历史/恢复基线，{snapshot['incremental_roles']:,} 条来自持续新岗位发现。 |",
            f"| {verified:,} | 已核实岗位 | 官方具体岗位标题、同岗位 Agent 证据和引用可以核实。 |",
            f"| {probable:,} | 高概率岗位 | 可以用于岗位发现，但不能直接进入严格 Current。 |",
            f"| {current:,} | 严格当前岗位 | 从 {roles:,} 条唯一公开处置直接投影，全部通过身份、标题、岗位级 Agent 证据、官方开放、公开访问、TTL、schema 与去重硬门。 |",
            f"| {snapshot['noncurrent']:,} | 不在 Current 的岗位 | `{roles:,} - {current:,}`；包括证据穷尽仍不明、临时阻塞、身份争议、明确关闭与相关性/标题失败。 |",
            "",
            f"{current:,} 个严格 Current 来自全部 {roles:,} 条 `public_disposition` 的直接投影；非 Current 继续保留真实历史状态，不暗示仍在招聘。",
        )
    )
    scale = replace_section(scale, "## 4. 全站岗位层级", "## 5. 严格当前岗位的地域分布", role_body)

    geography_rows = sorted(
        snapshot["current_geography"].items(), key=lambda item: (-item[1], item[0])
    )
    geography_table = ["| 地域 | 当前岗位 |", "| --- | ---: |"]
    geography_table.extend(
        f"| {geography_label(name)} | {count:,} |" for name, count in geography_rows
    )
    geography_table.append(f"| **合计** | **{current:,}** |")
    china_us = snapshot["current_geography"].get("China", 0) + snapshot[
        "current_geography"
    ].get("United States", 0)
    geography_body = "\n".join(
        geography_table
        + [
            "",
            f"中国和美国共有 {china_us:,} 个严格当前岗位；其他地区、全球范围或地域待复核共有 {current - china_us:,} 个。",
        ]
    )
    scale = replace_section(scale, "## 5. 严格当前岗位的地域分布", "## 6. 地图实体", geography_body)

    entity_body = "\n".join(
        (
            "| 数字 | 对象 | 定义 |",
            "| ---: | --- | --- |",
            f"| {snapshot['organizations']:,} | 组织 | 按集团或明确公司主体聚合。共享 ATS 或名称相似不会自动合并。 |",
            f"| {snapshot['teams']:,} | 团队 | 组织下的团队、部门或工作方向。 |",
            f"| {snapshot['products']:,} | 产品 | 团队构建、运营或支持的产品和能力方向。 |",
            f"| {roles:,} | 岗位 | 去重后的岗位记录。 |",
            f"| {snapshot['relations']:,} | 关系 | 上述对象之间的图谱关系。 |",
            f"| {snapshot['current_teams']:,} | 有当前岗位的团队 | 至少包含一个严格当前岗位。 |",
            f"| {snapshot['teams_without_current']:,} | 当前岗位为 0 的团队 | `{snapshot['teams']:,} - {snapshot['current_teams']:,}`，仍保留在完整团队地图中。 |",
        )
    )
    scale = replace_section(scale, "## 6. 地图实体", "## 7. 地点与办公方式", entity_body)

    location = snapshot["location"]
    arrangement = snapshot["arrangement"]
    basis = snapshot["arrangement_basis"]
    display_body = "\n".join(
        (
            "| 数字 | 地点状态 | 定义 |",
            "| ---: | --- | --- |",
            f"| {location.get('normalized_or_descriptive', 0):,} | 已规范化或有可靠描述 | 有可公开展示的城市、国家或地域范围。 |",
            f"| {location.get('pending_review', 0):,} | 地点待复核 | 来源没有足够的岗位地点信息。 |",
            f"| {location.get('company_or_context_only', 0):,} | 只有公司或上下文地点 | 不能直接当成岗位地点。 |",
            f"| {location.get('official_role_title_location_reviewed', 0):,} | 从官方岗位标题复核 | 地点由官方岗位标题中的明确字段支持。 |",
            f"| **{roles:,}** | **合计** | 覆盖全部岗位。 |",
            "",
            "| 数字 | 办公方式 | 定义 |",
            "| ---: | --- | --- |",
            f"| {arrangement.get('onsite', 0):,} | 现场办公 | 其中 {basis.get('default_onsite_no_remote_signal', 0):,} 个按“未标远程或混合则默认现场”分类，{basis.get('explicit_onsite', 0):,} 个来源明确写明现场。 |",
            f"| {arrangement.get('remote_or_hybrid', 0):,} | 远程或混合 | 来源明确出现远程或混合信号。 |",
            f"| **{roles:,}** | **合计** | 覆盖全部岗位。 |",
            "",
            "默认现场是本项目的产品分类规则，不表示招聘方逐条明确承诺现场办公。",
        )
    )
    scale = replace_section(scale, "## 7. 地点与办公方式", "## 8. 复核队列", display_body)

    review_body = "\n".join(
        (
            "| 数字 | 对象 | 定义 |",
            "| ---: | --- | --- |",
            f"| {snapshot['review']:,} | 复核队列事件 | 高概率、地点、TTL 或当前性复核事件；不是 {snapshot['review']:,} 个唯一岗位。 |",
            f"| {probable:,} | 高概率岗位 | 后续可能通过新的一手证据升级或继续保持高概率。 |",
            f"| {location.get('pending_review', 0):,} | 地点待复核岗位 | 后续可以在官方岗位页出现新地点字段时补全。 |",
            "",
            "一个岗位可能同时产生多种复核事件，因此事件数不能与岗位数直接相减。",
        )
    )
    scale = replace_section(scale, "## 8. 复核队列", "## 9. 本轮网络复核规模", review_body)
    scale_path.write_text(scale, encoding="utf-8")

    maintenance_path = paths["maintenance"]
    maintenance = maintenance_path.read_text(encoding="utf-8")
    maintenance = replace_unique(
        maintenance,
        r"(?m)^> 当前发布基线：\d{4}-\d{2}-\d{2}，严格 Current=[0-9,]+；它由 [0-9,]+ 条唯一 `public_disposition` 直接投影。",
        f"> 当前发布基线：{release}，严格 Current={current:,}；它由 {roles:,} 条唯一 `public_disposition` 直接投影。",
        "maintenance release baseline",
    )
    maintenance_path.write_text(maintenance, encoding="utf-8")

    dictionary_path = paths["dictionary"]
    dictionary = dictionary_path.read_text(encoding="utf-8")
    dictionary = replace_unique(
        dictionary,
        r"默认 Current 只由 `[0-9,]+` 条 `publish_current` 组成；",
        f"默认 Current 只由 `{current:,}` 条 `publish_current` 组成；",
        "data dictionary Current count",
    )
    dictionary_path.write_text(dictionary, encoding="utf-8")

    methodology_path = paths["methodology"]
    methodology = methodology_path.read_text(encoding="utf-8")
    methodology = replace_unique(
        methodology,
        (
            r"因此 [0-9,]+ 条 Evidence、[0-9,]+ 条岗位记录和 [0-9,]+ 条 "
            r"\d{4}-\d{2}-\d{2} 严格 Current 是三个不同分母；Current 由全部 "
            r"[0-9,]+ 条唯一公开处置直接投影，"
        ),
        (
            f"因此 {evidence:,} 条 Evidence、{roles:,} 条岗位记录和 {current:,} 条 "
            f"{release} 严格 Current 是三个不同分母；Current 由全部 "
            f"{roles:,} 条唯一公开处置直接投影，"
        ),
        "methodology current snapshot",
    )
    methodology_path.write_text(methodology, encoding="utf-8")


def rebuild_team_overview(output: Path) -> None:
    script = output / "scripts/build_team_role_overview.py"
    document = output / "docs/TEAM_ROLE_OVERVIEW.md"
    if not script.exists() and not document.exists():
        return
    if not script.is_file() or script.is_symlink() or not document.is_file():
        raise ReleaseError("team overview projection surface is incomplete")
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=output,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        raise ReleaseError(f"team overview projection failed: {detail or 'unknown error'}")


def rebuild_public_manifest(output: Path) -> None:
    """Rebuild the public self-excluded manifest after all release files exist."""

    files: dict[str, str] = {}
    for path in sorted(output.rglob("*")):
        relative_path = path.relative_to(output)
        relative = relative_path.as_posix()
        if path.is_symlink():
            raise ReleaseError(f"public package symlink forbidden: {relative}")
        if relative_path.parts and relative_path.parts[0] == "metrics-private":
            raise ReleaseError(f"private metrics forbidden in public package: {relative}")
        if not path.is_file() or ".git" in relative_path.parts:
            continue
        if (
            any(part in COPY_IGNORED_NAMES for part in relative_path.parts)
            or path.suffix == ".pyc"
            or relative == "review-queue.jsonl"
            or relative == "manifest.json"
        ):
            continue
        files[relative] = sha256_bytes(path.read_bytes())
    manifest = {
        "schema_version": "agent-hiring-map-public-manifest/1.0",
        "hash_algorithm": "sha256",
        "self_excluded": True,
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _build_release_tree(
    source: Path,
    admissions_bytes: bytes,
    source_manifest: dict[str, str],
    release_date: date,
    output: Path,
) -> dict[str, Any]:
    source = source.absolute()
    admissions_raw = load_jsonl_bytes(admissions_bytes)
    admissions = [normalize_admission(row, release_date) for row in admissions_raw]
    admissions.sort(key=lambda row: (row["official_url"], row["candidate_id"]))
    copy_source(source, output, source_manifest)
    if not admissions:
        return {"status": "completed_no_admissions", "admitted": 0, "output": str(output.resolve())}

    data = output / "data"
    specs = {
        "evidence": ("evidence/evidence-ledger-safe", "evidence_id"),
        "organizations": ("map/organizations", "organization_id"),
        "teams": ("map/teams", "team_id"),
        "products": ("map/products", "product_id"),
        "roles": ("map/roles", "role_id"),
        "relations": ("map/relations", "relation_id"),
        "current": ("current/current-opportunities", "role_id"),
    }
    rows = {name: load_jsonl(data / f"{stem}.jsonl") for name, (stem, _) in specs.items()}
    for name, (_, id_key) in specs.items():
        assert_unique_ids(rows[name], id_key, name)
    metadata_path = data / "metadata/release-metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    original_current = {row["role_id"]: row for row in rows["current"]}
    source_publish_ids = {
        row["role_id"]
        for row in rows["roles"]
        if row.get("public_disposition") == "publish_current"
    }
    if set(original_current) != source_publish_ids:
        raise ReleaseError("source Current is not an exact public_disposition projection")
    source_review_path = data / "review/review-queue.jsonl"
    source_review = load_jsonl(source_review_path) if source_review_path.exists() else []
    before = {
        "evidence": len(rows["evidence"]),
        "organizations": len(rows["organizations"]),
        "teams": len(rows["teams"]),
        "products": len(rows["products"]),
        "roles": len(rows["roles"]),
        "relations": len(rows["relations"]),
        "current": len(rows["current"]),
        "review": len(source_review),
    }
    declared_canonical = metadata.get("canonical_counts")
    source_count_contract = {
        "evidence_rows": before["evidence"],
        "review_queue_rows": before["review"],
    }
    if any(metadata.get(key) != value for key, value in source_count_contract.items()):
        raise ReleaseError("source release metadata count drift")
    if not isinstance(declared_canonical, dict) or any(
        declared_canonical.get(key) != before[key]
        for key in ("organizations", "teams", "products", "roles", "relations")
    ):
        raise ReleaseError("source canonical metadata count drift")
    if (
        not isinstance(metadata.get("current_opportunities"), dict)
        or metadata["current_opportunities"].get("rows") != before["current"]
    ):
        raise ReleaseError("source Current metadata count drift")

    existing_urls = {normalize_url(row.get("official_role_url")) for row in rows["roles"]}
    existing_org_title = {
        (row["organization_id"], normalize_text(row.get("title"))) for row in rows["roles"]
    }
    existing_org_locator = {
        (row["organization_id"], normalize_text(row.get("stable_role_locator"))) for row in rows["roles"]
    }
    batch_candidates: set[str] = set()
    batch_urls: set[str] = set()
    batch_tenant_locators: set[str] = set()
    new_roles: list[dict[str, Any]] = []
    next_evidence = max(int(row["evidence_id"].split("-")[1]) for row in rows["evidence"]) + 1

    for admission in admissions:
        if admission["candidate_id"] in batch_candidates or admission["official_url"] in batch_urls:
            raise ReleaseError("duplicate candidate or URL inside sealed batch")
        if normalize_text(admission["ats_tenant_locator"]) in batch_tenant_locators:
            raise ReleaseError("duplicate ATS tenant locator inside sealed batch")
        batch_candidates.add(admission["candidate_id"])
        batch_urls.add(admission["official_url"])
        batch_tenant_locators.add(normalize_text(admission["ats_tenant_locator"]))
        if admission["official_url"] in existing_urls:
            raise ReleaseError("admission duplicates canonical official URL")
        evidence_id = f"AMC-{next_evidence:04d}"
        next_evidence += 1
        evidence = evidence_row(admission, evidence_id)

        org, new_org = resolve_organization(admission, rows["organizations"], evidence_id)
        if new_org:
            rows["organizations"].append(org)
        team, new_team = resolve_child("team", admission, rows["teams"], org["organization_id"], evidence_id)
        if new_team:
            rows["teams"].append(team)
        product, new_product = resolve_child("product", admission, rows["products"], org["organization_id"], evidence_id)
        if new_product:
            rows["products"].append(product)
        if product["product_id"] not in team.get("product_ids", []):
            team["product_ids"] = sorted({*(team.get("product_ids") or []), product["product_id"]})

        org_id = org["organization_id"]
        if (org_id, normalize_text(admission["title"])) in existing_org_title:
            raise ReleaseError("admission duplicates canonical organization + title")
        if (org_id, normalize_text(admission["stable_locator"])) in existing_org_locator:
            raise ReleaseError("admission duplicates canonical stable locator")
        role = role_row(admission, evidence_id, org_id, team["team_id"], product["product_id"])
        if any(item["role_id"] == role["role_id"] for item in rows["roles"]):
            raise ReleaseError("new Role stable ID collision")
        rows["evidence"].append(evidence)
        rows["roles"].append(role)
        new_roles.append(role)
        existing_urls.add(admission["official_url"])
        existing_org_title.add((org_id, normalize_text(admission["title"])))
        existing_org_locator.add((org_id, normalize_text(admission["stable_locator"])))
        append_relation(rows["relations"], team["team_id"], "PART_OF", org_id, evidence_id)
        append_relation(rows["relations"], product["product_id"], "PART_OF", org_id, evidence_id)
        append_relation(rows["relations"], team["team_id"], "BUILDS", product["product_id"], evidence_id)
        append_relation(rows["relations"], role["role_id"], "BELONGS_TO", team["team_id"], evidence_id)
        append_relation(rows["relations"], role["role_id"], "SUPPORTS", product["product_id"], evidence_id)

    assert_unique_ids(rows["roles"], "role_id", "roles")
    role_by_id = {row["role_id"]: row for row in rows["roles"]}
    publish_ids = {
        role_id for role_id, role in role_by_id.items() if role.get("public_disposition") == "publish_current"
    }
    if set(original_current) - publish_ids:
        raise ReleaseError("source Current was not an exact public_disposition projection")
    rows["current"] = [
        project_current(role_by_id[role_id], original_current.get(role_id))
        for role_id in sorted(publish_ids)
    ]

    for name, (stem, id_key) in specs.items():
        rows[name].sort(key=lambda row: row[id_key])
        csv_path = data / f"{stem}.csv"
        fields, line_terminator = csv_serialization_contract(csv_path, rows[name])
        write_jsonl(data / f"{stem}.jsonl", rows[name])
        write_csv(
            csv_path,
            rows[name],
            fields,
            line_terminator=line_terminator,
        )

    queue, batches = build_review_queue(rows["current"], rows["roles"], rows["teams"], release_date)
    # The review queue is a fully regenerated derivative whose established
    # JSONL/CSV contract uses the same alphabetical field order.
    write_jsonl(data / "review/review-queue.jsonl", queue, sort_keys=True)
    review_fields = sorted(set().union(*(set(row) for row in queue))) if queue else sorted([
        "schema_version", "queue_id", "role_id", "geography", "last_verified_at", "as_of_date",
        "review_reason", "priority", "source_urls", "access_requirement", "trigger_recorded",
        "network_recheck_performed", "queue_status",
    ])
    review_csv_path = data / "review/review-queue.csv"
    existing_review_fields, review_line_terminator = csv_serialization_contract(
        review_csv_path, queue
    )
    if existing_review_fields:
        review_fields = existing_review_fields
    write_csv(
        review_csv_path,
        queue,
        review_fields,
        line_terminator=review_line_terminator,
    )
    (data / "review/source-batches.json").write_text(stable_json(batches, pretty=True), encoding="utf-8")

    metadata["release_as_of"] = release_date.isoformat()
    metadata["evidence_rows"] = len(rows["evidence"])
    metadata["review_queue_rows"] = len(queue)
    metadata["canonical_counts"] = {
        "organizations": len(rows["organizations"]),
        "products": len(rows["products"]),
        "relations": len(rows["relations"]),
        "roles": len(rows["roles"]),
        "teams": len(rows["teams"]),
    }
    metadata["current_opportunities"]["rows"] = len(rows["current"])
    metadata["current_opportunities"]["geography"] = dict(sorted(Counter(row["geography"] for row in rows["current"]).items()))
    confidence = Counter(row["public_confidence_tier"] for row in rows["roles"])
    origins = Counter(row["recovery_origin"] for row in rows["roles"])
    metadata["recovery"]["public_role_records"] = len(rows["roles"])
    metadata["recovery"]["public_confidence_tier"] = dict(sorted(confidence.items()))
    metadata["recovery"]["continuous_new_role_discovery_roles"] = origins.get("continuous_new_role_discovery", 0)
    metadata["recovery"]["historical_public_role_records"] = len(rows["roles"]) - origins.get("continuous_new_role_discovery", 0)
    arrangement = Counter(row["work_arrangement"] for row in rows["roles"])
    basis = Counter(row["work_arrangement_basis"] for row in rows["roles"])
    locations = Counter(row["location_data_status"] for row in rows["roles"])
    title_status = Counter(row["title_support_status"] for row in rows["roles"])
    metadata["role_display"]["work_arrangement"] = dict(sorted(arrangement.items()))
    metadata["role_display"]["work_arrangement_basis"] = dict(sorted(basis.items()))
    metadata["role_display"]["location_data_status"] = dict(sorted(locations.items()))
    metadata["title_authenticity"]["roles_audited"] = len(rows["roles"])
    metadata["title_authenticity"]["status"] = dict(sorted(title_status.items()))
    role_ids_added = sorted(role["role_id"] for role in new_roles)
    metadata["incremental_release"] = {
        "version": INCREMENTAL_VERSION,
        "release_date": release_date.isoformat(),
        "batch_roles_added": len(new_roles),
        "role_ids_added": role_ids_added,
        "cumulative_roles": origins.get("continuous_new_role_discovery", 0),
        "batch_evidence_added": len(new_roles),
        "input_sha256": sha256_bytes(admissions_bytes),
        "raw_html_or_full_jd_stored": False,
    }
    metadata_path.write_text(stable_json(metadata, pretty=True), encoding="utf-8")

    after = {
        "evidence": len(rows["evidence"]),
        "organizations": len(rows["organizations"]),
        "teams": len(rows["teams"]),
        "products": len(rows["products"]),
        "roles": len(rows["roles"]),
        "relations": len(rows["relations"]),
        "current": len(rows["current"]),
        "review": len(queue),
    }
    delta = {
        "schema_version": "agent-hiring-map-public-delta/2.0",
        "release_as_of": release_date.isoformat(),
        "reason": "continuous_new_role_discovery_release",
        "before": before,
        "after": after,
        "changed": {
            "role_ids_added": role_ids_added,
            "roles_added": len(new_roles),
            "current_added": len(new_roles),
            "evidence_added": after["evidence"] - before["evidence"],
            "organizations_added": after["organizations"] - before["organizations"],
            "teams_added": after["teams"] - before["teams"],
            "products_added": after["products"] - before["products"],
            "relations_added": after["relations"] - before["relations"],
            "review_delta": after["review"] - before["review"],
        },
        "raw_html_or_full_jd_stored": False,
    }
    (data / "metadata/release-delta.json").write_text(stable_json(delta, pretty=True), encoding="utf-8")
    replace_snapshot_tokens(
        output,
        before,
        after,
        release_date.isoformat(),
        snapshot_projection(rows, metadata),
    )
    rebuild_team_overview(output)
    output_files = tree_file_manifest(output, exclude_release_seal=True)
    build_seal = {
        "schema_version": "agent-hiring-map-incremental-build-seal/1.0",
        "release_date": release_date.isoformat(),
        "admissions_sha256": sha256_bytes(admissions_bytes),
        "role_ids_added": role_ids_added,
        "release_metadata_sha256": sha256_bytes(metadata_path.read_bytes()),
        "release_delta_sha256": sha256_bytes(
            (data / "metadata/release-delta.json").read_bytes()
        ),
        "source_manifest_sha256": manifest_sha256(source_manifest),
        "output_files": output_files,
        "output_files_sha256": manifest_sha256(output_files),
    }
    (data / "metadata/incremental-build-seal.json").write_text(
        stable_json(build_seal, pretty=True), encoding="utf-8"
    )
    rebuild_public_manifest(output)
    return {
        "status": "completed_incremental_release_build",
        "admitted": len(new_roles),
        "role_ids": sorted(role["role_id"] for role in new_roles),
        "before": before,
        "after": after,
        "output": str(output.resolve()),
    }


def build_release(source: Path, admissions_path: Path, release_date: date, output: Path) -> dict[str, Any]:
    """Build in a sibling temporary tree, then atomically publish once complete."""

    output = prepare_secure_output_path(output, "incremental release output")
    lock_path = output.parent / ".incremental-release.lock"
    with open_nofollow_lock(lock_path, "incremental release lock") as lock_handle:
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ReleaseError("incremental release lock already held") from exc
        reject_output_path_symlinks(output, "incremental release output")
        if admissions_path.is_symlink() or not admissions_path.is_file():
            raise ReleaseError("admissions input must be a regular non-symlink file")
        admissions_bytes = admissions_path.read_bytes()
        source_manifest = tree_file_manifest(source)
        if output.exists():
            admissions = load_jsonl_bytes(admissions_bytes)
            if not admissions and tree_file_manifest(output) == source_manifest:
                return {
                    "status": "completed_idempotent",
                    "admitted": 0,
                    "output": str(output),
                }
            seal_path = output / "data/metadata/incremental-build-seal.json"
            release_metadata_path = output / "data/metadata/release-metadata.json"
            release_delta_path = output / "data/metadata/release-delta.json"
            try:
                seal = json.loads(seal_path.read_text(encoding="utf-8"))
                release_metadata = json.loads(
                    release_metadata_path.read_text(encoding="utf-8")
                )
                release_delta = json.loads(release_delta_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                seal = {}
                release_metadata = {}
                release_delta = {}
            actual_output_files = tree_file_manifest(output, exclude_release_seal=True)
            declared_role_ids = (
                release_metadata.get("incremental_release", {}).get("role_ids_added")
                if isinstance(release_metadata.get("incremental_release"), dict)
                else None
            )
            delta_role_ids = (
                release_delta.get("changed", {}).get("role_ids_added")
                if isinstance(release_delta.get("changed"), dict)
                else None
            )
            if (
                seal.get("schema_version")
                == "agent-hiring-map-incremental-build-seal/1.0"
                and seal.get("release_date") == release_date.isoformat()
                and seal.get("admissions_sha256") == sha256_bytes(admissions_bytes)
                and seal.get("source_manifest_sha256") == manifest_sha256(source_manifest)
                and seal.get("role_ids_added") == declared_role_ids == delta_role_ids
                and seal.get("release_metadata_sha256")
                == sha256_bytes(release_metadata_path.read_bytes())
                and seal.get("release_delta_sha256")
                == sha256_bytes(release_delta_path.read_bytes())
                and seal.get("output_files") == actual_output_files
                and seal.get("output_files_sha256")
                == manifest_sha256(actual_output_files)
            ):
                return {
                    "status": "completed_idempotent",
                    "admitted": int(
                        json.loads(
                            (output / "data/metadata/release-metadata.json").read_text(
                                encoding="utf-8"
                            )
                        )["incremental_release"]["batch_roles_added"]
                    ),
                    "output": str(output),
                }
            raise ReleaseError(f"output tree already exists with different inputs or drift: {output}")
        # Keep mkdtemp's mode-0700 directory in place while building. Removing
        # it would create a name-substitution window for a hostile symlink.
        staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
        try:
            result = _build_release_tree(
                source, admissions_bytes, source_manifest, release_date, staging
            )
            reject_output_path_symlinks(output, "incremental release output")
            os.replace(staging, output)
            directory_fd = open_nofollow_directory(
                output.parent, "incremental release output parent"
            )
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            result["output"] = str(output)
            return result
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--admissions", type=Path, required=True)
    parser.add_argument("--release-date", type=date.fromisoformat, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    result = build_release(args.source_root, args.admissions, args.release_date, args.output_root)
    print(stable_json(result, pretty=True), end="")


if __name__ == "__main__":
    main()
