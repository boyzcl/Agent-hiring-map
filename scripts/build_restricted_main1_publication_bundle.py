#!/usr/bin/env python3
"""Build the real ten-row, fail-closed restricted main-1 publication bundle."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import build_incremental_release as release
import build_publication_admission_pack as adapter


SCHEMA = "agent-hiring-map-restricted-main1-publication-bundle/1.0"
DISPLAY_TITLES = {
    "CAND-019AD4896989F98D1A29A665": ("递归自我改进 Agent 架构研发工程师", "Recursive Self-Improvement Agent R&D Engineer"),
    "CAND-424979A20B17D87DC7958FED": ("企业级 Agent 工程师", "Enterprise Agent Engineer"),
    "CAND-439118A231AE2B6D3DDC6BF6": ("智能体开发工程师", "Agent Development Engineer"),
    "CAND-6DEA73120DE5B09888CA12F7": ("AI GTM 架构师（营收运营）", "AI GTM Architect (Revenue Operations)"),
    "CAND-B23BBCC24471894CAFA25D18": ("高级后端软件工程师（AI Agent）", "Senior Software Engineer, Backend (AI Agent)"),
    "CAND-B3EBD4D0622DED17F367B018": ("大模型 Agent 算法工程师", "LLM Agent Algorithm Engineer"),
    "CAND-B4BABDF7C67F3C1E6FAD13FC": ("AI/ML 工程师", "AI/ML Engineer"),
    "CAND-B9B695401E16E362F97EF0D6": ("AI Agent 开发工程师", "AI Agent Development Engineer"),
    "CAND-F036FB46C1924CD87DF029BC": ("高级软件工程师——应用 AI", "Senior Software Engineer -- Applied AI"),
    "CAND-FD210912522B0D48A3AB212F": ("产品工程师—技术成员", "Product Engineer - Member of Technical Staff"),
}
NEW_ORGANIZATION_DOMAINS = {
    "Contemporary Amperex Technology": ["catl.com"],
    "Zoomlion": ["zoomlion.com"],
    "Lenovo / 联想": ["lenovo.com"],
}


def stable_json(value: Any, *, pretty: bool = False) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        sort_keys=True,
    ) + "\n"


def rows(path: Path) -> list[dict[str, Any]]:
    return release.read_sealed_jsonl_rows(
        {"path": str(path.resolve()), "sha256": release.sha256_bytes(path.read_bytes())},
        path.name,
    )


def row_hash(row: dict[str, Any]) -> str:
    return release.sha256_bytes(stable_json(row).encode("utf-8").rstrip(b"\n"))


def physical_row_hash(row: dict[str, Any]) -> str:
    return release.sha256_bytes(stable_json(row).encode("utf-8"))


def spec(path: Path, *, selected: dict[str, Any] | None = None, row_count: int | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "path": str(path.resolve()),
        "sha256": release.sha256_bytes(path.read_bytes()),
    }
    if selected is not None:
        value["row_sha256"] = row_hash(selected)
    if row_count is not None:
        value["row_count"] = row_count
    return value


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.write_text("".join(stable_json(value) for value in values), encoding="utf-8")


def identity_projection(row: dict[str, Any], reference: str, organization: str | None = None) -> dict[str, Any]:
    organization = organization or str(row.get("organization") or row.get("organization_name") or "")
    stable = str(row.get("stable_job_id") or row.get("stable_role_locator") or reference)
    title = str(row.get("title") or row.get("official_title_raw") or "")
    url = str(row.get("official_role_url") or row.get("title_source_url") or "")
    ats = str(row.get("ats_tenant_locator") or f"canonical|{reference}")
    projected = {
        "reference_id": reference,
        "identity_keys": {
            "canonical_url": release.normalize_url(url),
            "organization_stable_job_id": f"{release.normalize_text(organization)}|{release.normalize_text(stable)}",
            "ats_tenant_locator": release.normalize_text(ats),
            "organization_title": f"{release.normalize_text(organization)}|{release.normalize_text(title)}",
        },
    }
    if any(not value for value in projected["identity_keys"].values()):
        raise release.ReleaseError(f"incomplete anti-join identity: {reference}")
    return projected


def build(run_root: Path, source_root: Path, output: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    source_root = source_root.resolve()
    output = release.prepare_secure_output_path(output, "restricted publication bundle output")
    if output.exists():
        raise release.ReleaseError("restricted publication bundle output already exists")
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        merged = run_root / "publication-revalidation-01/merged-fail-closed-01"
        formal = run_root / "formal-main1-inputs-03"
        pass_rows = rows(merged / "pass.jsonl")
        if len(pass_rows) != 10 or {row["candidate_id"] for row in pass_rows} != set(DISPLAY_TITLES):
            raise release.ReleaseError("real pass cohort is not the frozen ten-row set")
        sidecar_values = rows(formal / "all-sidecars-93.jsonl")
        sidecars = {row["candidate_id"]: row for row in sidecar_values}
        cohort_values = rows(formal / "cohort-membership-93.jsonl")
        cohorts = {row["candidate_id"]: row["cohort"] for row in cohort_values}
        if len(sidecars) != 93 or len(cohorts) != 93:
            raise release.ReleaseError("formal main-1 93-row authority is incomplete")

        pack_files = {
            shard: run_root / f"publication-revalidation-packs-02/{shard}/pack.jsonl"
            for shard in ("moka41", "other26", "trip26")
        }
        pack_rows = {
            row["candidate_id"]: row
            for path in pack_files.values()
            for row in rows(path)
        }
        organizations = rows(source_root / "data/map/organizations.jsonl")
        org_by_name: dict[str, dict[str, Any]] = {}
        for organization in organizations:
            for name in [organization.get("canonical_name"), *(organization.get("aliases") or [])]:
                if name:
                    org_by_name.setdefault(release.normalize_text(name), organization)

        canonical_orgs = {row["organization_id"]: row["canonical_name"] for row in organizations}
        canonical_roles = rows(source_root / "data/map/roles.jsonl")
        canonical_projection = [
            identity_projection(row, row["role_id"], canonical_orgs[row["organization_id"]])
            for row in canonical_roles
        ]
        if len(canonical_projection) != 1313:
            raise release.ReleaseError("canonical anti-join layer is not 1,313 rows")
        canonical_path = staging / "canonical-roles-1313.identity.jsonl"
        write_jsonl(canonical_path, canonical_projection)
        current_projection = [
            identity_projection(row, row["candidate_id"])
            for row in sidecar_values
        ]
        current_path = staging / "current-run-93.identity.jsonl"
        write_jsonl(current_path, current_projection)

        pass_ids = {row["candidate_id"] for row in pass_rows}
        batch_projection = [row for row in current_projection if row["reference_id"] in pass_ids]
        batch_path = staging / "publication-batch-10.identity.jsonl"
        write_jsonl(batch_path, batch_projection)

        live_values: list[dict[str, Any]] = []
        reviewer_pack_values: list[dict[str, Any]] = []
        reviewer_values = {"reviewer_a": [], "reviewer_b": []}
        pass_by_id = {row["candidate_id"]: row for row in pass_rows}
        for candidate_id in sorted(pass_ids):
            passed = pass_by_id[candidate_id]
            sidecar = sidecars[candidate_id]
            source_pack = pack_rows[candidate_id]
            if physical_row_hash(source_pack) != passed["pack_row_sha256"]:
                raise release.ReleaseError("pass row does not bind source revalidation pack")
            observed = passed["observed"]
            live_values.append({
                "candidate_id": candidate_id,
                "checked_at": passed["checked_at"],
                "status": "open",
                "official_source": True,
                "official_specific_job": True,
                "public_readable": True,
                "actionable_apply": True,
                "raw_html_or_full_jd_stored": False,
                "official_role_url": observed["final_url"],
                "organization_observed": observed["organization"],
                "title_observed": observed["title"],
                "stable_job_id_observed": observed["stable_job_id"],
            })
            prior = source_pack["prior_reviewer_duty_evidence"]
            reviewer_pack_values.append({
                "candidate_id": candidate_id,
                "stable_job_id": sidecar["stable_job_id"],
                "ats_tenant_locator": sidecar["ats_tenant_locator"],
                "official_role_url": sidecar["official_role_url"],
                "organization": sidecar["organization"],
                "title": sidecar["title"],
                "agent_specific_excerpt": observed["minimal_duty_quote"],
                "reviewer_duty_quotes": [item["duty_quote"] for item in prior],
                "source_revalidation_pack_row_sha256": passed["pack_row_sha256"],
                "raw_html_or_full_jd_stored": False,
            })
        live_path = staging / "live-checks.aug6-pass-10.jsonl"
        reviewer_pack_path = staging / "reviewer-authority.safe-pack-10.jsonl"
        write_jsonl(live_path, live_values)
        write_jsonl(reviewer_pack_path, reviewer_pack_values)
        reviewer_pack_by_id = {row["candidate_id"]: row for row in reviewer_pack_values}
        for candidate_id in sorted(pass_ids):
            prior = pack_rows[candidate_id]["prior_reviewer_duty_evidence"]
            for item in prior:
                slot = item["reviewer_slot"]
                reviewer_values[slot].append({
                    "candidate_id": candidate_id,
                    "source_reviewer_id": item["reviewer_id"],
                    "reviewer_id": f"{item['reviewer_id']}::{candidate_id}",
                    "independent_review": True,
                    "verdict": "positive",
                    "lane": item.get("role_lane") or sidecars[candidate_id].get("role_lane") or "A",
                    "evidence_quote": item["duty_quote"],
                    "input_row_sha256": row_hash(reviewer_pack_by_id[candidate_id]),
                    "source_provenance_sha256": release.sha256_bytes(
                        stable_json(item.get("provenance_sha256") or {}).encode("utf-8").rstrip(b"\n")
                    ),
                    "projection_of_sealed_prior_review": True,
                    "reviewed_at": None,
                    "reviewed_at_status": "not_recorded_in_source_authority",
                    "authority_predates_publication_revalidation": True,
                })
        reviewer_paths = {}
        for slot, values in reviewer_values.items():
            path = staging / f"{slot}.safe-projection-10.jsonl"
            write_jsonl(path, values)
            reviewer_paths[slot] = path
        roster_path = staging / "reviewer-authority.safe-roster.json"
        roster_path.write_text(stable_json({
            "sealed_at": None,
            "sealed_at_status": "not_recorded_in_source_authority",
            "projection_of_sealed_prior_review": True,
            "candidate_ids": sorted(pass_ids),
            "reviewer_context_ids": {},
            "timing_note": "exact historical reviewed_at was not recorded; source authority predates Aug-6 publication revalidation",
        }, pretty=True), encoding="utf-8")

        antijoin_dir = staging / "antijoin"
        antijoin_dir.mkdir()
        decision_values = []
        manifest_paths: dict[str, Path] = {}
        for candidate_id in sorted(pass_ids):
            prior_values = [row for row in current_projection if row["reference_id"] != candidate_id]
            if len(prior_values) != 92:
                raise release.ReleaseError("per-candidate prior sidecar layer is not 92 rows")
            prior_path = antijoin_dir / f"{candidate_id}.prior-sidecars-92.jsonl"
            write_jsonl(prior_path, prior_values)
            layers = {
                "canonical_roles_zero_conflict": spec(canonical_path, row_count=1313),
                "prior_sidecars_zero_conflict": spec(prior_path, row_count=92),
                "current_run_candidates_zero_conflict": spec(current_path, row_count=93),
                "batch_zero_conflict": spec(batch_path, row_count=10),
            }
            manifest_path = antijoin_dir / f"{candidate_id}.manifest.json"
            manifest_path.write_text(stable_json({
                "schema_version": "agent-hiring-map-publication-antijoin-inputs/1.0",
                "candidate_id": candidate_id,
                "layers": layers,
            }, pretty=True), encoding="utf-8")
            manifest_paths[candidate_id] = manifest_path
            sidecar = sidecars[candidate_id]
            decision_values.append({
                "candidate_id": candidate_id,
                "stable_job_id": sidecar["stable_job_id"],
                "ats_tenant_locator": sidecar["ats_tenant_locator"],
                "official_role_url": sidecar["official_role_url"],
                "organization": sidecar["organization"],
                "title": sidecar["title"],
                "zero_duplicate": True,
                "anti_join_conflicts": [],
                "final_pre_sidecar_disposition": "eligible",
                "input_sha256": {key: value["sha256"] for key, value in layers.items()},
            })
        decisions_path = staging / "antijoin-decisions-10.jsonl"
        write_jsonl(decisions_path, decision_values)

        decision_by_id = {row["candidate_id"]: row for row in decision_values}
        live_by_id = {row["candidate_id"]: row for row in live_values}
        reviewer_by_slot = {
            slot: {row["candidate_id"]: row for row in values}
            for slot, values in reviewer_values.items()
        }
        authority_names = {
            "terminal": "terminal-seal.json",
            "manifest": "artifact-manifest.json",
            "decisions": "decisions-93.jsonl",
            "pass": "pass.jsonl",
            "exclude": "exclude.jsonl",
            "unresolved": "unresolved.jsonl",
            "dispositions": "publication-dispositions-93.jsonl",
        }
        authority = {key: spec(merged / name) for key, name in authority_names.items()}
        contract_rows = []
        for candidate_id in sorted(pass_ids):
            sidecar = sidecars[candidate_id]
            passed = pass_by_id[candidate_id]
            source_pack = pack_rows[candidate_id]
            shard = passed["shard_id"]
            organization = org_by_name.get(release.normalize_text(sidecar["organization"]))
            domains = [] if organization else NEW_ORGANIZATION_DOMAINS.get(sidecar["organization"])
            if not organization and not domains:
                raise release.ReleaseError(f"organization ownership domain unavailable: {sidecar['organization']}")
            zh, en = DISPLAY_TITLES[candidate_id]
            publication_fields = {
                "canonical_organization_id": organization.get("organization_id") if organization else None,
                "organization_official_domains": domains,
                "team_name": "Restricted admission / 受限准入",
                "product_name": "Agent role work surface / 智能体岗位工作面",
                "product_official_url": None,
                "display_title_zh": zh,
                "display_title_en": en,
                "title_source_language": "zh" if any("\u4e00" <= c <= "\u9fff" for c in sidecar["title"]) else "en",
                "title_translation_status": "deterministic_bilingual_translation_v1",
                "location_data_status": "company_or_context_only",
                "display_location_zh": "岗位地点待复核（来源仅列出公司或团队地点）",
                "display_location_en": "Role location pending review (source only lists company or team locations)",
                "job_locations": [],
                "work_arrangement": "onsite",
                "work_arrangement_basis": "default_onsite_no_remote_signal",
                "role_family": "agent_engineering",
                "agent_specific_excerpt": passed["observed"]["minimal_duty_quote"],
                "release_cohort": (
                    "historical_local_overlay_revalidation"
                    if cohorts[candidate_id] == "historical"
                    else "china_main1_restricted_new_admission"
                ),
                "first_seen_at": str(sidecar.get("admitted_at") or "2026-08-06")[:10],
            }
            contract_rows.append({
                "candidate_id": candidate_id,
                "publication_fields": publication_fields,
                "revalidation_linkage": {
                    "pass_row_sha256": physical_row_hash(passed),
                    "pack_row_sha256": passed["pack_row_sha256"],
                    "shard_result_sha256": json.loads((merged / "artifact-manifest.json").read_text())["result_inputs"][shard]["sha256"],
                },
                "sealed_evidence": {
                    "source_sidecar": spec(formal / "all-sidecars-93.jsonl", selected=sidecar),
                    "revalidation_pack": spec(pack_files[shard], selected=source_pack),
                    "reviewer_pack": spec(reviewer_pack_path, selected=reviewer_pack_by_id[candidate_id]),
                    "reviewer_roster": spec(roster_path),
                    "reviewer_a": spec(reviewer_paths["reviewer_a"], selected=reviewer_by_slot["reviewer_a"][candidate_id]),
                    "reviewer_b": spec(reviewer_paths["reviewer_b"], selected=reviewer_by_slot["reviewer_b"][candidate_id]),
                    "live_check": spec(live_path, selected=live_by_id[candidate_id]),
                    "antijoin_decision": spec(decisions_path, selected=decision_by_id[candidate_id]),
                    "antijoin_input_manifest": spec(manifest_paths[candidate_id]),
                },
            })
        contract = {
            "schema_version": adapter.SCHEMA,
            "revalidation_authority": authority,
            "rows": contract_rows,
        }
        contract_path = staging / "publication-admission-contract.json"
        contract_path.write_text(stable_json(contract, pretty=True), encoding="utf-8")
        admissions = adapter.build(contract_path.read_bytes())
        admissions_path = staging / "publication-admissions-10.jsonl"
        admissions_path.write_bytes(admissions)

        artifacts = {}
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                relative = path.relative_to(staging).as_posix()
                artifacts[relative] = {
                    "bytes": path.stat().st_size,
                    "sha256": release.sha256_bytes(path.read_bytes()),
                }
                if path.suffix == ".jsonl":
                    artifacts[relative]["row_count"] = len(rows(path))
        manifest = {
            "schema_version": SCHEMA,
            "status": "completed_restricted_main1_publication_bundle",
            "candidate_count": 10,
            "partition": {"historical": 6, "known_source_china": 3, "main_1_china": 1},
            "anti_join_counts": {"canonical": 1313, "other_sidecars_per_candidate": 92, "current_run": 93, "batch": 10},
            "scope": "user-directed single completed main-1 release",
            "saturation_not_claimed": True,
            "network_requests": 0,
            "raw_html_or_full_jd_stored": False,
            "artifacts": artifacts,
        }
        manifest_path = staging / "artifact-manifest.json"
        manifest_path.write_text(stable_json(manifest, pretty=True), encoding="utf-8")
        terminal_path = staging / "terminal-seal.json"
        terminal_path.write_text(stable_json({
            "schema_version": f"{SCHEMA}-terminal",
            "status": "completed_restricted_main1_publication_bundle",
            "candidate_count": 10,
            "admissions_sha256": release.sha256_bytes(admissions),
            "artifact_manifest_sha256": release.sha256_bytes(manifest_path.read_bytes()),
            "scope": "user-directed single completed main-1 release",
            "saturation_not_claimed": True,
            "network_requests": 0,
        }, pretty=True), encoding="utf-8")
        staging_prefix = str(staging.resolve())
        output_prefix = str(output.resolve())
        os.replace(staging, output)

        def rebase(value: Any) -> Any:
            if isinstance(value, dict):
                return {key: rebase(child) for key, child in value.items()}
            if isinstance(value, list):
                return [rebase(child) for child in value]
            if isinstance(value, str) and value.startswith(staging_prefix + os.sep):
                return output_prefix + value[len(staging_prefix):]
            return value

        for candidate_id in sorted(pass_ids):
            final_antijoin_manifest = output / "antijoin" / f"{candidate_id}.manifest.json"
            value = rebase(json.loads(final_antijoin_manifest.read_text(encoding="utf-8")))
            final_antijoin_manifest.write_text(stable_json(value, pretty=True), encoding="utf-8")

        final_contract_path = output / "publication-admission-contract.json"
        final_contract = rebase(json.loads(final_contract_path.read_text(encoding="utf-8")))
        for entry in final_contract["rows"]:
            candidate_id = entry["candidate_id"]
            final_antijoin_manifest = output / "antijoin" / f"{candidate_id}.manifest.json"
            entry["sealed_evidence"]["antijoin_input_manifest"]["sha256"] = (
                release.sha256_bytes(final_antijoin_manifest.read_bytes())
            )
        final_contract_path.write_text(stable_json(final_contract, pretty=True), encoding="utf-8")
        final_admissions = adapter.build(final_contract_path.read_bytes())
        final_admissions_path = output / "publication-admissions-10.jsonl"
        final_admissions_path.write_bytes(final_admissions)

        final_artifacts = {}
        for path in sorted(output.rglob("*")):
            if path.is_file() and path.name not in {"artifact-manifest.json", "terminal-seal.json"}:
                relative = path.relative_to(output).as_posix()
                final_artifacts[relative] = {
                    "bytes": path.stat().st_size,
                    "sha256": release.sha256_bytes(path.read_bytes()),
                }
                if path.suffix == ".jsonl":
                    final_artifacts[relative]["row_count"] = len(rows(path))
        manifest["artifacts"] = final_artifacts
        final_manifest_path = output / "artifact-manifest.json"
        final_manifest_path.write_text(stable_json(manifest, pretty=True), encoding="utf-8")
        final_terminal_path = output / "terminal-seal.json"
        final_terminal_path.write_text(stable_json({
            "schema_version": f"{SCHEMA}-terminal",
            "status": "completed_restricted_main1_publication_bundle",
            "candidate_count": 10,
            "admissions_sha256": release.sha256_bytes(final_admissions),
            "artifact_manifest_sha256": release.sha256_bytes(final_manifest_path.read_bytes()),
            "scope": "user-directed single completed main-1 release",
            "saturation_not_claimed": True,
            "network_requests": 0,
        }, pretty=True), encoding="utf-8")
        return {
            "status": "completed_restricted_main1_publication_bundle",
            "candidate_count": 10,
            "admissions_sha256": release.sha256_bytes(final_admissions),
            "output": str(output),
            "network_requests": 0,
        }
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    print(stable_json(build(args.run_root, args.source_root, args.output_root), pretty=True), end="")


if __name__ == "__main__":
    main()
