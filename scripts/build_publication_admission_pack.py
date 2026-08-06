#!/usr/bin/env python3
"""Adapt actual restricted-production sidecars into sealed publication admissions."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_incremental_release as release


SCHEMA = "agent-hiring-map-publication-admission-adapter/1.1"
REVALIDATION_FILES = {
    "terminal",
    "manifest",
    "decisions",
    "pass",
    "exclude",
    "unresolved",
    "dispositions",
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def physical_row_sha(row: dict[str, Any]) -> str:
    return release.sha256_bytes((stable_json(row) + "\n").encode("utf-8"))


def parse_utc(value: object, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise release.ReleaseError(f"{label} is not an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise release.ReleaseError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_revalidation_authority(specs: object) -> dict[str, Any]:
    if not isinstance(specs, dict) or set(specs) != REVALIDATION_FILES:
        raise release.ReleaseError("revalidation authority file closure is invalid")
    terminal = release.read_sealed_json(specs["terminal"], "revalidation terminal")
    manifest = release.read_sealed_json(specs["manifest"], "revalidation manifest")
    if not (
        terminal.get("schema_version") == "china-publication-revalidation-merge-terminal/1.1"
        and terminal.get("status") == "completed_publication_revalidation_fail_closed"
        and terminal.get("candidate_count") == 93
        and terminal.get("request_count") == 93
        and terminal.get("outcome_counts") == {"pass": 10, "exclude": 55, "unresolved": 28}
        and terminal.get("publication_authorized") is True
        and terminal.get("publication_eligible_count") == 10
        and terminal.get("publication_excluded_count") == 83
        and terminal.get("unresolved_evidence_count") == 28
        and terminal.get("unresolved_publication_disposition")
        == "exclude_fail_closed_without_replacement"
        and terminal.get("scope") == "user-directed single completed main-1 release"
        and terminal.get("saturation_not_claimed") is True
    ):
        raise release.ReleaseError("revalidation terminal is not the sealed restricted 10/83 authority")
    _, manifest_bytes = release.read_sealed_bytes(specs["manifest"], "revalidation manifest")
    if terminal.get("artifact_manifest_sha256") != release.sha256_bytes(manifest_bytes):
        raise release.ReleaseError("revalidation terminal does not bind manifest")
    if not (
        manifest.get("schema_version") == "china-publication-revalidation-merge-manifest/1.1"
        and manifest.get("candidate_count") == 93
        and manifest.get("request_count") == 93
        and manifest.get("outcome_counts") == terminal.get("outcome_counts")
        and manifest.get("publication_authorized") is True
        and manifest.get("publication_eligible_count") == 10
        and manifest.get("publication_excluded_count") == 83
        and manifest.get("unresolved_evidence_count") == 28
        and manifest.get("scope") == terminal.get("scope")
        and manifest.get("saturation_not_claimed") is True
    ):
        raise release.ReleaseError("revalidation manifest is not the restricted 10/83 authority")

    names = {
        "decisions": "decisions-93.jsonl",
        "pass": "pass.jsonl",
        "exclude": "exclude.jsonl",
        "unresolved": "unresolved.jsonl",
        "dispositions": "publication-dispositions-93.jsonl",
    }
    rows: dict[str, list[dict[str, Any]]] = {}
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise release.ReleaseError("revalidation manifest artifacts are missing")
    for key, artifact_name in names.items():
        _, payload = release.read_sealed_bytes(specs[key], f"revalidation {key}")
        if (artifacts.get(artifact_name) or {}).get("sha256") != release.sha256_bytes(payload):
            raise release.ReleaseError(f"revalidation manifest does not bind {key}")
        rows[key] = release.read_sealed_jsonl_rows(specs[key], f"revalidation {key}")
    if not (
        len(rows["decisions"]) == 93
        and len(rows["pass"]) == 10
        and len(rows["exclude"]) == 55
        and len(rows["unresolved"]) == 28
        and len(rows["dispositions"]) == 93
    ):
        raise release.ReleaseError("revalidation row partition is not 93=10+55+28")
    decision_by_id = {str(row.get("candidate_id") or ""): row for row in rows["decisions"]}
    if len(decision_by_id) != 93 or "" in decision_by_id:
        raise release.ReleaseError("revalidation decisions are not unique")
    partition_sets = {
        key: {str(row.get("candidate_id") or "") for row in rows[key]}
        for key in ("pass", "exclude", "unresolved")
    }
    if (
        any("" in values for values in partition_sets.values())
        or set.union(*partition_sets.values()) != set(decision_by_id)
        or any(partition_sets[a] & partition_sets[b] for a, b in (("pass", "exclude"), ("pass", "unresolved"), ("exclude", "unresolved")))
    ):
        raise release.ReleaseError("revalidation partitions overlap or do not close")
    disposition_by_id = {
        str(row.get("candidate_id") or ""): row for row in rows["dispositions"]
    }
    if len(disposition_by_id) != 93:
        raise release.ReleaseError("revalidation dispositions are not unique")
    for candidate_id, decision in decision_by_id.items():
        disposition = disposition_by_id.get(candidate_id) or {}
        expected = "publish" if decision.get("outcome") == "pass" else "exclude_fail_closed"
        if (
            disposition.get("evidence_outcome") != decision.get("outcome")
            or disposition.get("publication_disposition") != expected
        ):
            raise release.ReleaseError("revalidation disposition disagrees with evidence outcome")
    result_inputs = manifest.get("result_inputs")
    if not isinstance(result_inputs, dict) or set(result_inputs) != {"moka41", "trip26", "other26"}:
        raise release.ReleaseError("revalidation shard result closure is invalid")
    return {
        "terminal_sha256": specs["terminal"]["sha256"],
        "manifest_sha256": specs["manifest"]["sha256"],
        "pass_by_id": {str(row["candidate_id"]): row for row in rows["pass"]},
        "excluded_ids": partition_sets["exclude"] | partition_sets["unresolved"],
        "result_inputs": result_inputs,
    }


def adapt_entry(entry: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    candidate_id = str(entry.get("candidate_id") or "")
    sealed = entry.get("sealed_evidence")
    publication = entry.get("publication_fields")
    if not candidate_id or not isinstance(sealed, dict) or not isinstance(publication, dict):
        raise release.ReleaseError("adapter entry requires candidate_id, sealed_evidence, and publication_fields")
    pass_row = authority["pass_by_id"].get(candidate_id)
    linkage = entry.get("revalidation_linkage")
    if pass_row is None or candidate_id in authority["excluded_ids"] or not isinstance(linkage, dict):
        raise release.ReleaseError("adapter entry is not a uniquely sealed revalidation pass")
    shard_id = str(pass_row.get("shard_id") or "")
    result_input = authority["result_inputs"].get(shard_id) or {}
    if not (
        linkage.get("pass_row_sha256") == physical_row_sha(pass_row)
        and linkage.get("pack_row_sha256") == pass_row.get("pack_row_sha256")
        and linkage.get("shard_result_sha256") == result_input.get("sha256")
    ):
        raise release.ReleaseError("adapter revalidation pass linkage is invalid")
    sidecar, _ = release.read_sealed_jsonl_row(
        sealed.get("source_sidecar"), "source_sidecar", candidate_id
    )
    source_pack, _ = release.read_sealed_jsonl_row(
        sealed.get("revalidation_pack"), "revalidation_pack", candidate_id
    )
    if not (
        physical_row_sha(source_pack) == pass_row.get("pack_row_sha256")
        and (source_pack.get("source_row_sha256") or {}).get("sidecar")
        == physical_row_sha(sidecar)
    ):
        raise release.ReleaseError("source revalidation pack does not bind source sidecar")
    live, _ = release.read_sealed_jsonl_row(
        sealed.get("live_check"), "live_check", candidate_id
    )
    observed = pass_row.get("observed")
    hard_gates = pass_row.get("hard_gates")
    if not isinstance(observed, dict) or not isinstance(hard_gates, dict) or not all(
        value is True for value in hard_gates.values()
    ):
        raise release.ReleaseError("sealed revalidation pass hard gates are incomplete")
    if not (
        live.get("checked_at") == pass_row.get("checked_at")
        and live.get("status") == "open"
        and live.get("official_source") is True
        and live.get("official_specific_job") is True
        and live.get("public_readable") is True
        and live.get("actionable_apply") is True
        and live.get("raw_html_or_full_jd_stored") is False
        and release.normalize_url(live.get("official_role_url"))
        == release.normalize_url(observed.get("final_url"))
        and release.normalize_text(live.get("organization_observed"))
        == release.normalize_text(observed.get("organization"))
        and release.normalize_text(live.get("title_observed"))
        == release.normalize_text(observed.get("title"))
        and release.normalize_text(live.get("stable_job_id_observed"))
        == release.normalize_text(observed.get("stable_job_id"))
    ):
        raise release.ReleaseError("sealed live check is not the latest revalidation pass")
    checked_at = parse_utc(pass_row.get("checked_at"), "revalidation checked_at")
    ttl_deadline = parse_utc(source_pack.get("ttl_deadline"), "revalidation ttl_deadline")
    if ttl_deadline <= checked_at or hard_gates.get("ttl_valid") is not True:
        raise release.ReleaseError("revalidation TTL is not valid at the publication check")
    ttl_candidates = [sidecar.get("ttl"), (sidecar.get("provenance") or {}).get("ttl")]
    ttl = next((value for value in ttl_candidates if isinstance(value, dict)), None)
    if ttl is not None:
        ttl_days = ttl.get("days")
    elif str(source_pack.get("ttl_basis") or "").endswith("_plus_7d"):
        ttl_days = 7
    else:
        raise release.ReleaseError("source sidecar/revalidation pack lacks auditable TTL policy")
    if isinstance(ttl_days, bool) or not isinstance(ttl_days, int) or not 1 <= ttl_days <= 14:
        raise release.ReleaseError("source TTL days are outside the publication policy")

    normalized_pack, _ = release.read_sealed_jsonl_row(
        sealed.get("reviewer_pack"), "reviewer_pack", candidate_id
    )
    if normalized_pack.get("source_revalidation_pack_row_sha256") != pass_row.get("pack_row_sha256"):
        raise release.ReleaseError("normalized Reviewer pack is not bound to revalidation pack")
    expected_reviewers = source_pack.get("prior_reviewer_duty_evidence")
    if not isinstance(expected_reviewers, list) or len(expected_reviewers) != 2:
        raise release.ReleaseError("source revalidation pack lacks exactly two Reviewer proofs")
    reviewer_by_slot = {str(item.get("reviewer_slot") or ""): item for item in expected_reviewers}
    if set(reviewer_by_slot) != {"reviewer_a", "reviewer_b"}:
        raise release.ReleaseError("source revalidation Reviewer slots are incomplete")
    for reviewer_label in ("reviewer_a", "reviewer_b"):
        normalized_reviewer, _ = release.read_sealed_jsonl_row(
            sealed.get(reviewer_label), reviewer_label, candidate_id
        )
        source_reviewer = reviewer_by_slot[reviewer_label]
        provenance_hash = release.sha256_bytes(
            stable_json(source_reviewer.get("provenance_sha256") or {}).encode("utf-8")
        )
        if not (
            normalized_reviewer.get("source_reviewer_id") == source_reviewer.get("reviewer_id")
            and normalized_reviewer.get("reviewer_id")
            == f"{source_reviewer.get('reviewer_id')}::{candidate_id}"
            and normalized_reviewer.get("evidence_quote") == source_reviewer.get("duty_quote")
            and normalized_reviewer.get("source_provenance_sha256") == provenance_hash
            and normalized_reviewer.get("projection_of_sealed_prior_review") is True
            and normalized_reviewer.get("reviewed_at_status")
            == "not_recorded_in_source_authority"
            and normalized_reviewer.get("authority_predates_publication_revalidation") is True
            and normalized_reviewer.get("reviewed_at") is None
        ):
            raise release.ReleaseError(
                f"normalized Reviewer projection disagrees with source authority: "
                f"{candidate_id}:{reviewer_label}:"
                f"source_id={normalized_reviewer.get('source_reviewer_id') == source_reviewer.get('reviewer_id')}:"
                f"quote={normalized_reviewer.get('evidence_quote') == source_reviewer.get('duty_quote')}:"
                f"provenance={normalized_reviewer.get('source_provenance_sha256') == provenance_hash}:"
                f"projection={normalized_reviewer.get('projection_of_sealed_prior_review') is True}:"
                f"status={normalized_reviewer.get('reviewed_at_status') == 'not_recorded_in_source_authority'}:"
                f"predates={normalized_reviewer.get('authority_predates_publication_revalidation') is True}:"
                f"reviewed_at={normalized_reviewer.get('reviewed_at') is None}"
            )
    row = dict(publication)
    row.update(
        {
            "candidate_id": candidate_id,
            "stable_job_id": sidecar.get("stable_job_id"),
            "ats_tenant_locator": sidecar.get("ats_tenant_locator"),
            "official_role_url": sidecar.get("official_role_url"),
            "organization_name": sidecar.get("organization"),
            "title": sidecar.get("title"),
            "geography": (sidecar.get("provenance") or {}).get("region"),
            "raw_html_or_full_jd_stored": False,
            "ttl_days": ttl_days,
            "next_check_at": source_pack.get("ttl_deadline"),
            "sealed_evidence": sealed,
            "publication_revalidation": {
                "terminal_sha256": authority["terminal_sha256"],
                "manifest_sha256": authority["manifest_sha256"],
                "pass_row_sha256": linkage["pass_row_sha256"],
                "pack_row_sha256": linkage["pack_row_sha256"],
                "shard_result_sha256": linkage["shard_result_sha256"],
                "shard_id": shard_id,
                "outcome": "pass",
            },
        }
    )
    if publication.get("organization_name") not in (None, sidecar.get("organization")):
        raise release.ReleaseError("publication organization disagrees with source sidecar")
    if publication.get("title") not in (None, sidecar.get("title")):
        raise release.ReleaseError("publication title disagrees with source sidecar")
    release.bind_sealed_evidence(row)
    return row


def build(contract_bytes: bytes) -> bytes:
    try:
        contract = json.loads(contract_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise release.ReleaseError("adapter contract must be valid UTF-8 JSON") from exc
    if not isinstance(contract, dict) or contract.get("schema_version") != SCHEMA:
        raise release.ReleaseError("adapter contract schema is invalid")
    entries = contract.get("rows")
    if not isinstance(entries, list):
        raise release.ReleaseError("adapter contract rows must be a list")
    authority = load_revalidation_authority(contract.get("revalidation_authority"))
    entry_ids = {str(entry.get("candidate_id") or "") for entry in entries if isinstance(entry, dict)}
    if entry_ids != set(authority["pass_by_id"]) or len(entries) != len(entry_ids):
        raise release.ReleaseError("adapter contract candidate set must equal sealed revalidation pass set")
    rows = [adapt_entry(entry, authority) for entry in entries]
    candidate_ids = [row["candidate_id"] for row in rows]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise release.ReleaseError("adapter contract contains duplicate candidate IDs")
    rows.sort(key=lambda row: row["candidate_id"])
    return "".join(stable_json(row) + "\n" for row in rows).encode("utf-8")


def write_atomic_idempotent(output: Path, content: bytes) -> str:
    output = release.prepare_secure_output_path(output, "publication admission pack output")
    lock_path = output.parent / f".{output.name}.lock"
    with release.open_nofollow_lock(lock_path, "publication admission pack lock") as lock_handle:
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise release.ReleaseError("publication admission pack lock already held") from exc
        try:
            release.reject_output_path_symlinks(output, "publication admission pack output")
            if output.exists():
                if output.is_symlink() or output.read_bytes() != content:
                    raise release.ReleaseError("adapter output exists with different content")
                return "completed_idempotent"
            fd, temporary_name = tempfile.mkstemp(
                prefix=f".{output.name}.", dir=output.parent
            )
            temporary = Path(temporary_name)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())
                release.reject_output_path_symlinks(output, "publication admission pack output")
                os.replace(temporary, output)
                directory_fd = release.open_nofollow_directory(
                    output.parent, "publication admission pack output parent"
                )
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except Exception:
                temporary.unlink(missing_ok=True)
                raise
            return "completed_publication_admission_pack"
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.contract.is_symlink() or not args.contract.is_file():
        raise release.ReleaseError("adapter contract must be a regular non-symlink file")
    content = build(args.contract.read_bytes())
    status = write_atomic_idempotent(args.output, content)
    print(
        json.dumps(
            {
                "status": status,
                "rows": len([line for line in content.splitlines() if line.strip()]),
                "sha256": release.sha256_bytes(content),
                "output": str(args.output.resolve()),
                "network_used": False,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
