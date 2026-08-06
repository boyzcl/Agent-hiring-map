from __future__ import annotations

import hashlib
import json
import fcntl
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_incremental_release as B  # noqa: E402
import build_publication_admission_pack as A  # noqa: E402
import build_manifest as M  # noqa: E402
import validate_public_package as V  # noqa: E402


def jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class IncrementalReleaseBuilderTests(unittest.TestCase):
    release_date = date(2026, 8, 6)

    def setUp(self) -> None:
        # macOS exposes /var as a symlink. Use its physical path so the test
        # root remains outside the source tree without weakening parent checks.
        self.temp = tempfile.TemporaryDirectory(
            prefix="incremental-release-tests-",
            dir=Path(tempfile.gettempdir()).resolve(),
        )
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self._fixture_source(self.source)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _fixture_source(self, root: Path) -> None:
        evidence = {
            "schema_version": B.PUBLIC_SCHEMA,
            "evidence_id": "AMC-0001",
            "geography_bucket": "China",
            "coverage_scope": "canonical_map_scope",
            "source_class": "official_or_first_party",
            "source_urls": ["https://example.cn/jobs/base"],
            "access_requirement": "public_no_login",
            "evidence_grade": "A",
            "evidence_kind": "role_signal",
            "public_excerpt": "构建 Agent 工具调用模块。",
            "quote_publication_status": "minimal_attributed_excerpt",
            "limitations": [],
        }
        organization = {
            "schema_version": B.PUBLIC_SCHEMA,
            "organization_id": "ORG-BASE",
            "canonical_name": "Baseline",
            "official_domains": ["example.cn"],
            "geography": ["China"],
            "aliases": ["Baseline"],
            "evidence_ids": ["AMC-0001"],
        }
        team = {
            "schema_version": B.PUBLIC_SCHEMA,
            "team_id": "TEAM-BASE",
            "organization_id": "ORG-BASE",
            "team_name": "Agent Team",
            "product_ids": ["PROD-BASE"],
            "team_geography": ["China"],
            "evidence_ids": ["AMC-0001"],
        }
        product = {
            "schema_version": B.PUBLIC_SCHEMA,
            "product_id": "PROD-BASE",
            "organization_id": "ORG-BASE",
            "name": "Agent Platform",
            "evidence_ids": ["AMC-0001"],
        }
        role = {
            "schema_version": B.PUBLIC_SCHEMA,
            "role_id": "ROLE-BASE",
            "organization_id": "ORG-BASE",
            "team_id": "TEAM-BASE",
            "product_id": "PROD-BASE",
            "title": "Agent Engineer",
            "official_title_raw": "Agent Engineer",
            "display_title_zh": "Agent 工程师",
            "display_title_en": "Agent Engineer",
            "official_role_url": "https://example.cn/jobs/base",
            "stable_role_locator": "base-1",
            "public_disposition": "publish_current",
            "public_confidence_tier": "verified",
            "recovery_origin": "existing_role_revalidated",
            "work_arrangement": "onsite",
            "work_arrangement_basis": "default_onsite_no_remote_signal",
            "location_data_status": "pending_review",
            "title_support_status": "verified_official_title",
            "title_source_granularity": "direct_role_detail",
            "title_source_url": "https://example.cn/jobs/base",
            "title_translation_status": "verified_translation",
            "citation_supports_title": True,
            "currentness_status": "current_verified",
            "currentness_next_check_at": "2026-08-19T00:00:00Z",
            "last_verified_at": "2026-08-05",
            "access_requirement": "public_no_login",
            "evidence_grade": "A",
            "agent_specific_quote": "构建 Agent 工具调用模块。",
            "agent_relevance_summary": "构建 Agent 工具调用模块。",
            "geography": "China",
            "evidence_ids": ["AMC-0001"],
        }
        current = {
            "schema_version": B.PUBLIC_SCHEMA,
            "role_id": "ROLE-BASE",
            "organization_id": "ORG-BASE",
            "team_id": "TEAM-BASE",
            "product_id": "PROD-BASE",
            "title": "Agent Engineer",
            "display_title_zh": "Agent 工程师",
            "display_title_en": "Agent Engineer",
            "title_source_granularity": "direct_role_detail",
            "title_source_url": "https://example.cn/jobs/base",
            "title_support_status": "verified_official_title",
            "title_translation_status": "verified_translation",
            "citation_supports_title": True,
            "currentness_status": "current_verified",
            "last_verified_at": "2026-08-05",
            "source_urls": ["https://example.cn/jobs/base"],
            "agent_specific_excerpt": "构建 Agent 工具调用模块。",
            "evidence_grade": "A",
            "evidence_ids": ["AMC-0001"],
            "geography": "China",
            "access_requirement": "public_no_login",
            "limitations": [],
        }
        relation = {
            "schema_version": B.PUBLIC_SCHEMA,
            "relation_id": "REL-BASE",
            "subject_id": "ROLE-BASE",
            "predicate": "BELONGS_TO",
            "object_id": "TEAM-BASE",
            "evidence_ids": ["AMC-0001"],
        }
        for stem, rows in (
            ("evidence/evidence-ledger-safe", [evidence]),
            ("map/organizations", [organization]),
            ("map/teams", [team]),
            ("map/products", [product]),
            ("map/roles", [role]),
            ("map/relations", [relation]),
            ("current/current-opportunities", [current]),
        ):
            jsonl(root / "data" / f"{stem}.jsonl", rows)
        metadata = {
            "release_as_of": "2026-08-05",
            "evidence_rows": 1,
            "review_queue_rows": 0,
            "canonical_counts": {
                "organizations": 1,
                "teams": 1,
                "products": 1,
                "roles": 1,
                "relations": 1,
            },
            "current_opportunities": {"rows": 1, "geography": {"China": 1}},
            "recovery": {"public_role_records": 1, "public_confidence_tier": {"verified": 1}},
            "role_display": {},
            "title_authenticity": {},
        }
        path = root / "data/metadata/release-metadata.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(metadata), encoding="utf-8")
        (root / "marker.txt").write_text("unchanged\n", encoding="utf-8")
        for relative in (
            "scripts/build_team_role_overview.py",
            "docs/TEAM_ROLE_OVERVIEW.md",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)

    def admission(self, **changes: object) -> dict:
        row = {
            "candidate_id": "CAND-NEW-1",
            "stable_job_id": "job-2026-1",
            "ats_tenant_locator": "self_hosted|newco.cn|job-2026-1",
            "official_role_url": "https://newco.cn/careers/job-2026-1",
            "organization_name": "NewCo / 新公司",
            "organization_official_domains": ["newco.cn"],
            "team_name": "智能体平台团队",
            "product_name": "企业智能体平台",
            "product_official_url": "https://newco.cn/agent",
            "title": "智能体平台工程师",
            "display_title_zh": "智能体平台工程师",
            "display_title_en": "Agent Platform Engineer",
            "title_source_language": "zh",
            "geography": "China",
            "location_data_status": "official_role_title_location_reviewed",
            "display_location_zh": "上海",
            "display_location_en": "Shanghai",
            "job_locations": ["Shanghai"],
            "work_arrangement": "onsite",
            "work_arrangement_basis": "explicit_onsite",
            "role_family": "agent_platform_engineering",
            "agent_specific_excerpt": "负责设计智能体任务规划、工具调用和评测模块。",
            "release_cohort": "china_main1_restricted_new_admission",
            "raw_html_or_full_jd_stored": False,
            "reviewers": {
                "independent": True,
                "roster_sealed_before_review": True,
                "roster_sealed_at": "2026-08-06T00:30:00Z",
                "a": {
                    "reviewer_id": "reviewer-a",
                    "execution_context_id": "context-a",
                    "verdict": "positive",
                    "lane": "A",
                    "evidence_quote": "负责设计智能体任务规划、工具调用和评测模块。",
                    "reviewed_at": "2026-08-06T01:00:00Z",
                    "input_sha256": "1" * 64,
                    "decision_sha256": "2" * 64,
                },
                "b": {
                    "reviewer_id": "reviewer-b",
                    "execution_context_id": "context-b",
                    "verdict": "positive",
                    "lane": "A",
                    "evidence_quote": "负责设计智能体任务规划、工具调用和评测模块。",
                    "reviewed_at": "2026-08-06T01:10:00Z",
                    "input_sha256": "1" * 64,
                    "decision_sha256": "3" * 64,
                },
            },
            "verification": {
                "status": "open",
                "official_source": True,
                "official_specific_job": True,
                "public_readable": True,
                "actionable_apply": True,
                "raw_html_or_full_jd_stored": False,
                "checked_at": "2026-08-06T02:00:00Z",
                "official_role_url": "https://newco.cn/careers/job-2026-1",
                "title_observed": "智能体平台工程师",
                "stable_job_id_observed": "job-2026-1",
                "organization_observed": "NewCo / 新公司",
            },
            "ttl_days": 7,
            "next_check_at": "2026-08-13T02:00:00Z",
            "strict_four_layer_antijoin": {
                "canonical_roles_zero_conflict": True,
                "prior_sidecars_zero_conflict": True,
                "current_run_candidates_zero_conflict": True,
                "batch_zero_conflict": True,
                "input_sha256": {
                    "canonical_roles_zero_conflict": "4" * 64,
                    "prior_sidecars_zero_conflict": "5" * 64,
                    "current_run_candidates_zero_conflict": "6" * 64,
                    "batch_zero_conflict": "7" * 64,
                },
            },
        }
        row.update(changes)
        return row

    def write_admissions(self, name: str, rows: list[dict]) -> Path:
        path = self.base / name
        for index, row in enumerate(rows):
            self._seal_admission(path.stem, index, row)
        jsonl(path, rows)
        return path

    def _seal_admission(self, name: str, index: int, row: dict) -> None:
        root = self.base / "sealed" / name / str(index)
        root.mkdir(parents=True, exist_ok=True)
        candidate_id = row["candidate_id"]
        semantic_conflict_layer = row.pop("_sealed_test_conflict_layer", None)
        sealed_duty_quotes = row.pop(
            "_sealed_duty_quotes", [row["agent_specific_excerpt"]]
        )

        def write_rows(filename: str, items: list[dict]) -> tuple[Path, str]:
            target = root / filename
            jsonl(target, items)
            physical = target.read_bytes().splitlines()[0]
            return target, hashlib.sha256(physical).hexdigest()

        def spec(target: Path, row_hash: str | None = None) -> dict:
            value = {
                "path": str(target.resolve()),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
            if row_hash is not None:
                value["row_sha256"] = row_hash
            return value

        source_sidecar = {
            "candidate_id": candidate_id,
            "stable_job_id": row["stable_job_id"],
            "ats_tenant_locator": row["ats_tenant_locator"],
            "official_role_url": row["official_role_url"],
            "organization": row["organization_name"],
            "title": row["title"],
            "raw_html_or_full_jd_stored": False,
            "provenance": {
                "region": row.get("geography"),
                "ttl": {
                    "days": row.get("ttl_days"),
                    "next_check_at": row.get("next_check_at"),
                },
            },
        }
        source_path, source_row_hash = write_rows("source-sidecar.jsonl", [source_sidecar])
        pack_row = {
            "candidate_id": candidate_id,
            "stable_job_id": row["stable_job_id"],
            "ats_tenant_locator": row["ats_tenant_locator"],
            "official_role_url": row["official_role_url"],
            "organization": row["organization_name"],
            "title": row["title"],
            "agent_specific_excerpt": row["agent_specific_excerpt"],
            "reviewer_duty_quotes": sealed_duty_quotes,
            "raw_html_or_full_jd_stored": False,
        }
        pack_path, pack_row_hash = write_rows("reviewer-pack.jsonl", [pack_row])

        reviewers = row["reviewers"]
        reviewer_specs = {}
        for key in ("a", "b"):
            reviewer = reviewers[key]
            decision = {
                "candidate_id": candidate_id,
                "reviewer_id": reviewer["reviewer_id"],
                "execution_context_id": reviewer["execution_context_id"],
                "independent_review": True,
                "verdict": reviewer["verdict"],
                "lane": reviewer["lane"],
                "evidence_quote": reviewer["evidence_quote"],
                "reviewed_at": reviewer["reviewed_at"],
                "input_row_sha256": pack_row_hash,
            }
            decision_path, decision_row_hash = write_rows(
                f"reviewer-{key}.jsonl", [decision]
            )
            reviewer_specs[key] = spec(decision_path, decision_row_hash)

        roster = {
            "sealed_at": reviewers["roster_sealed_at"],
            "candidate_ids": [candidate_id],
            "reviewer_context_ids": {
                reviewers[key]["reviewer_id"]: reviewers[key]["execution_context_id"]
                for key in ("a", "b")
            },
        }
        roster_path = root / "reviewer-roster.json"
        roster_path.write_text(json.dumps(roster), encoding="utf-8")

        live = dict(row["verification"])
        live["candidate_id"] = candidate_id
        live_path, live_row_hash = write_rows("live-check.jsonl", [live])
        candidate_identity = {
            "canonical_url": B.normalize_url(row["official_role_url"]),
            "organization_stable_job_id": (
                f"{B.normalize_text(row['organization_name'])}|"
                f"{B.normalize_text(row['stable_job_id'])}"
            ),
            "ats_tenant_locator": B.normalize_text(row["ats_tenant_locator"]),
            "organization_title": (
                f"{B.normalize_text(row['organization_name'])}|"
                f"{B.normalize_text(row['title'])}"
            ),
        }
        baseline_identity = {
            "canonical_url": "https://example.cn/jobs/base",
            "organization_stable_job_id": "baseline|base-1",
            "ats_tenant_locator": "self_hosted|example.cn|base-1",
            "organization_title": "baseline|agent engineer",
        }
        layer_specs = {}
        layer_hashes = {}
        for layer in (
            "canonical_roles_zero_conflict",
            "prior_sidecars_zero_conflict",
            "current_run_candidates_zero_conflict",
            "batch_zero_conflict",
        ):
            layer_path = root / f"{layer}.jsonl"
            if layer == "canonical_roles_zero_conflict":
                layer_rows = [
                    {"reference_id": "ROLE-BASE", "identity_keys": baseline_identity}
                ]
            elif layer == "prior_sidecars_zero_conflict":
                layer_rows = []
            else:
                layer_rows = [
                    {"candidate_id": candidate_id, "identity_keys": candidate_identity}
                ]
            if semantic_conflict_layer == layer:
                layer_rows.append(
                    {
                        "reference_id": "CONFLICT-OTHER",
                        "identity_keys": candidate_identity,
                    }
                )
            jsonl(layer_path, layer_rows)
            layer_specs[layer] = {**spec(layer_path), "row_count": len(layer_rows)}
            layer_hashes[layer] = layer_specs[layer]["sha256"]
        antijoin_manifest_path = root / "antijoin-input-manifest.json"
        antijoin_manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": "agent-hiring-map-publication-antijoin-inputs/1.0",
                    "layers": layer_specs,
                }
            ),
            encoding="utf-8",
        )
        antijoin_decision = {
            "candidate_id": candidate_id,
            "stable_job_id": row["stable_job_id"],
            "ats_tenant_locator": row["ats_tenant_locator"],
            "official_role_url": row["official_role_url"],
            "organization": row["organization_name"],
            "title": row["title"],
            "zero_duplicate": True,
            "anti_join_conflicts": [],
            "final_pre_sidecar_disposition": "eligible",
            "input_sha256": layer_hashes,
        }
        antijoin_path, antijoin_row_hash = write_rows(
            "antijoin-decision.jsonl", [antijoin_decision]
        )
        row["sealed_evidence"] = {
            "source_sidecar": spec(source_path, source_row_hash),
            "reviewer_pack": spec(pack_path, pack_row_hash),
            "reviewer_roster": spec(roster_path),
            "reviewer_a": reviewer_specs["a"],
            "reviewer_b": reviewer_specs["b"],
            "live_check": spec(live_path, live_row_hash),
            "antijoin_decision": spec(antijoin_path, antijoin_row_hash),
            "antijoin_input_manifest": spec(antijoin_manifest_path),
        }

    def write_revalidation_authority(
        self,
        pass_ids: list[str],
        pack_row_sha256_by_id: dict[str, str] | None = None,
    ) -> tuple[dict[str, dict[str, str]], dict[str, dict]]:
        self.assertEqual(len(pass_ids), 10)
        root = self.base / "sealed-revalidation-authority"
        root.mkdir(parents=True, exist_ok=True)
        pass_rows = [
            {
                "candidate_id": candidate_id,
                "outcome": "pass",
                "shard_id": "moka41",
                "pack_row_sha256": (
                    pack_row_sha256_by_id[candidate_id]
                    if pack_row_sha256_by_id is not None
                    else f"{index + 1:064x}"
                ),
                "checked_at": "2026-08-06T02:00:00Z",
                "hard_gates": {"all_required_gates": True, "ttl_valid": True},
                "observed": {
                    "final_url": f"https://newco.cn/careers/job-2026-{index}",
                    "organization": "NewCo / 新公司",
                    "title": f"智能体平台工程师 {index}",
                    "stable_job_id": f"job-2026-{index}",
                },
                "reason_codes": ["ALL_HARD_GATES_PASS"],
            }
            for index, candidate_id in enumerate(pass_ids)
        ]
        exclude_rows = [
            {
                "candidate_id": f"CAND-EXCLUDE-{index:02d}",
                "outcome": "exclude",
                "shard_id": "other26",
                "pack_row_sha256": f"{100 + index:064x}",
                "reason_codes": ["HARD_GATE_FAILED"],
            }
            for index in range(55)
        ]
        unresolved_rows = [
            {
                "candidate_id": f"CAND-UNRESOLVED-{index:02d}",
                "outcome": "unresolved",
                "shard_id": "trip26",
                "pack_row_sha256": f"{200 + index:064x}",
                "reason_codes": ["PARSER_FAILURE"],
            }
            for index in range(28)
        ]
        decisions = pass_rows + exclude_rows + unresolved_rows
        dispositions = [
            {
                "candidate_id": row["candidate_id"],
                "evidence_outcome": row["outcome"],
                "publication_disposition": (
                    "publish" if row["outcome"] == "pass" else "exclude_fail_closed"
                ),
                "reason_codes": row["reason_codes"],
            }
            for row in decisions
        ]

        def write_jsonl(name: str, rows: list[dict]) -> tuple[Path, bytes]:
            path = root / name
            payload = b"".join(
                (json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
                for row in rows
            )
            path.write_bytes(payload)
            return path, payload

        payloads = {}
        paths = {}
        for key, name, rows in (
            ("decisions", "decisions-93.jsonl", decisions),
            ("pass", "pass.jsonl", pass_rows),
            ("exclude", "exclude.jsonl", exclude_rows),
            ("unresolved", "unresolved.jsonl", unresolved_rows),
            ("dispositions", "publication-dispositions-93.jsonl", dispositions),
        ):
            paths[key], payloads[name] = write_jsonl(name, rows)
        artifacts = {
            name: {"sha256": hashlib.sha256(payload).hexdigest()}
            for name, payload in payloads.items()
        }
        manifest = {
            "schema_version": "china-publication-revalidation-merge-manifest/1.1",
            "candidate_count": 93,
            "request_count": 93,
            "outcome_counts": {"pass": 10, "exclude": 55, "unresolved": 28},
            "publication_authorized": True,
            "publication_eligible_count": 10,
            "publication_excluded_count": 83,
            "unresolved_evidence_count": 28,
            "scope": "user-directed single completed main-1 release",
            "saturation_not_claimed": True,
            "result_inputs": {
                "moka41": {"sha256": "a" * 64},
                "trip26": {"sha256": "b" * 64},
                "other26": {"sha256": "c" * 64},
            },
            "artifacts": artifacts,
        }
        manifest_path = root / "artifact-manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        terminal = {
            "schema_version": "china-publication-revalidation-merge-terminal/1.1",
            "status": "completed_publication_revalidation_fail_closed",
            "candidate_count": 93,
            "request_count": 93,
            "outcome_counts": {"pass": 10, "exclude": 55, "unresolved": 28},
            "publication_authorized": True,
            "publication_eligible_count": 10,
            "publication_excluded_count": 83,
            "unresolved_evidence_count": 28,
            "unresolved_publication_disposition": "exclude_fail_closed_without_replacement",
            "scope": "user-directed single completed main-1 release",
            "saturation_not_claimed": True,
            "artifact_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        }
        terminal_path = root / "terminal-seal.json"
        terminal_path.write_text(
            json.dumps(terminal, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )

        def spec(path: Path) -> dict[str, str]:
            return {
                "path": str(path.resolve()),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }

        authority = {
            "terminal": spec(terminal_path),
            "manifest": spec(manifest_path),
            **{key: spec(path) for key, path in paths.items()},
        }
        return authority, {row["candidate_id"]: row for row in pass_rows}

    def test_zero_admissions_is_byte_exact_noop(self) -> None:
        admissions = self.write_admissions("empty.jsonl", [])
        output = self.base / "noop"
        result = B.build_release(self.source, admissions, self.release_date, output)
        self.assertEqual(result["status"], "completed_no_admissions")
        self.assertEqual(tree_hashes(self.source), tree_hashes(output))

    def test_dataset_serialization_preserves_existing_key_header_and_newline_contract(self) -> None:
        rows = [{"schema_version": "v1", "evidence_id": "E-1", "new_field": "x"}]
        jsonl_path = self.base / "ordered.jsonl"
        B.write_jsonl(jsonl_path, rows)
        self.assertEqual(
            jsonl_path.read_bytes(),
            b'{"schema_version":"v1","evidence_id":"E-1","new_field":"x"}\n',
        )

        csv_path = self.base / "ordered.csv"
        csv_path.write_bytes(b"evidence_id,schema_version\r\nE-0,v1\r\n")
        fields, line_terminator = B.csv_serialization_contract(csv_path, rows)
        self.assertEqual(fields, ["evidence_id", "schema_version", "new_field"])
        self.assertEqual(line_terminator, "\r\n")
        B.write_csv(
            csv_path,
            rows,
            fields,
            line_terminator=line_terminator,
        )
        self.assertEqual(
            csv_path.read_bytes(),
            b"evidence_id,schema_version,new_field\r\nE-1,v1,x\r\n",
        )

    def test_verified_hash_job_locators_remain_distinct_and_other_fragments_drop(self) -> None:
        moka_a = (
            "https://talent.catl.com/social-recruitment/catlhr/98098/"
            "#/job/c4f4b436-debc-4d26-a608-a92f5789d519"
        )
        moka_b = (
            "https://talent.catl.com/social-recruitment/catlhr/98098/"
            "#/job/753d65f9-e613-43df-9deb-ec0d3a65beed"
        )
        trip = (
            "https://careers.ctrip.com/index.html"
            "#/experienced/job-detail/MJ036295"
        )
        self.assertNotEqual(B.normalize_url(moka_a), B.normalize_url(moka_b))
        self.assertTrue(B.normalize_url(moka_a).endswith("#/job/c4f4b436-debc-4d26-a608-a92f5789d519"))
        self.assertTrue(B.normalize_url(trip).endswith("#/experienced/job-detail/MJ036295"))
        self.assertEqual(
            B.normalize_url("https://example.cn/jobs/one#tracking"),
            "https://example.cn/jobs/one",
        )
        self.assertEqual(
            B.normalize_url(
                "https://careers.ctrip.com/index.html#/experienced/job-detail/not-MJ"
            ),
            "https://careers.ctrip.com/index.html",
        )

    def test_one_china_admission_builds_complete_deterministic_projection(self) -> None:
        admissions = self.write_admissions("one.jsonl", [self.admission()])
        output_a, output_b = self.base / "a", self.base / "b"
        first = B.build_release(self.source, admissions, self.release_date, output_a)
        second = B.build_release(self.source, admissions, self.release_date, output_b)
        self.assertEqual(first["admitted"], 1)
        self.assertEqual(first["role_ids"], second["role_ids"])
        self.assertEqual(tree_hashes(output_a), tree_hashes(output_b))
        roles = B.load_jsonl(output_a / "data/map/roles.jsonl")
        current = B.load_jsonl(output_a / "data/current/current-opportunities.jsonl")
        evidence = B.load_jsonl(output_a / "data/evidence/evidence-ledger-safe.jsonl")
        self.assertEqual(len(roles), 2)
        self.assertEqual({row["role_id"] for row in current}, {row["role_id"] for row in roles if row["public_disposition"] == "publish_current"})
        promoted = [row for row in roles if row["recovery_origin"] == "continuous_new_role_discovery"]
        self.assertEqual(len(promoted), 1)
        self.assertEqual(promoted[0]["currentness_terminal"], "open_verified")
        self.assertEqual(evidence[-1]["public_excerpt"], self.admission()["agent_specific_excerpt"])
        self.assertLessEqual(len(evidence[-1]["public_excerpt"]), 300)
        self.assertEqual(len(B.load_jsonl(output_a / "data/map/organizations.jsonl")), 2)
        self.assertEqual(len(B.load_jsonl(output_a / "data/map/teams.jsonl")), 2)
        self.assertEqual(len(B.load_jsonl(output_a / "data/map/products.jsonl")), 2)
        overview = (output_a / "docs/TEAM_ROLE_OVERVIEW.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("| 地图岗位记录 | 2 |", overview)
        self.assertIn("| 当前岗位 | 2 |", overview)
        self.assertIn("| 安全证据索引 | 2 |", overview)

    def test_duplicate_official_url_fails_closed(self) -> None:
        row = self.admission(official_role_url="https://example.cn/jobs/base")
        row["verification"]["official_role_url"] = "https://example.cn/jobs/base"
        admissions = self.write_admissions("duplicate.jsonl", [row])
        with self.assertRaisesRegex(
            B.ReleaseError, "semantic conflict|duplicates canonical official URL"
        ):
            B.build_release(self.source, admissions, self.release_date, self.base / "duplicate-output")

    def test_excerpt_length_and_html_fail_closed(self) -> None:
        for index, excerpt in enumerate(("x" * 301, "<div>完整岗位正文</div>")):
            row = self.admission(agent_specific_excerpt=excerpt)
            admissions = self.write_admissions(f"unsafe-{index}.jsonl", [row])
            with self.subTest(excerpt=excerpt[:10]):
                with self.assertRaisesRegex(B.ReleaseError, "too long|contains HTML|unsafe"):
                    B.build_release(self.source, admissions, self.release_date, self.base / f"unsafe-output-{index}")

    def test_full_description_field_fails_closed(self) -> None:
        row = self.admission(full_jd="forbidden")
        admissions = self.write_admissions("full-jd.jsonl", [row])
        with self.assertRaisesRegex(B.ReleaseError, "forbidden full-description"):
                B.build_release(self.source, admissions, self.release_date, self.base / "full-jd-output")

    def test_new_admission_must_be_china(self) -> None:
        admissions = self.write_admissions("non-china.jsonl", [self.admission(geography="United States")])
        with self.assertRaisesRegex(B.ReleaseError, "China-only"):
            B.build_release(self.source, admissions, self.release_date, self.base / "non-china-output")

    def test_retired_saturation_cohort_name_fails_closed(self) -> None:
        admissions = self.write_admissions(
            "retired-saturation-cohort.jsonl",
            [self.admission(release_cohort="china_source_saturation_new_admission")],
        )
        with self.assertRaisesRegex(B.ReleaseError, "release_cohort"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                self.base / "retired-saturation-cohort-output",
            )

    def test_private_local_and_nonstandard_port_urls_fail_closed(self) -> None:
        unsafe_urls = (
            "https://localhost/jobs/1",
            "https://127.0.0.1/jobs/1",
            "https://10.0.0.8/jobs/1",
            "https://127.1/jobs/1",
            "https://2130706433/jobs/1",
            "https://0x7f000001/jobs/1",
        )
        for index, unsafe in enumerate(unsafe_urls):
            row = self.admission(official_role_url=unsafe)
            row["verification"]["official_role_url"] = unsafe
            admissions = self.write_admissions(f"unsafe-url-{index}.jsonl", [row])
            with self.subTest(url=unsafe):
                with self.assertRaisesRegex(
                    B.ReleaseError,
                    "identity or Agent-duty evidence|complete four-key anti-join identity",
                ):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"unsafe-url-output-{index}",
                    )

    def test_private_or_path_like_organization_domain_fails_closed(self) -> None:
        for index, domain in enumerate(("localhost", "10.0.0.8", "example.cn/path")):
            row = self.admission(organization_official_domains=[domain])
            admissions = self.write_admissions(f"unsafe-domain-{index}.jsonl", [row])
            with self.subTest(domain=domain):
                with self.assertRaisesRegex(B.ReleaseError, "hostnames only"):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"unsafe-domain-output-{index}",
                    )

    def test_historical_overlay_cohort_allows_frozen_us_record(self) -> None:
        row = self.admission(
            geography="United States",
            release_cohort="historical_local_overlay_revalidation",
        )
        admissions = self.write_admissions("historical-us.jsonl", [row])
        result = B.build_release(self.source, admissions, self.release_date, self.base / "historical-us-output")
        self.assertEqual(result["admitted"], 1)

    def test_reviewer_independence_and_quote_safety_fail_closed(self) -> None:
        same_reviewer = self.admission()
        same_reviewer["reviewers"]["b"]["reviewer_id"] = "reviewer-a"
        admissions = self.write_admissions("same-reviewer.jsonl", [same_reviewer])
        with self.assertRaisesRegex(B.ReleaseError, "sealed Reviewer|not independent"):
            B.build_release(self.source, admissions, self.release_date, self.base / "same-reviewer-output")
        unsafe_quote = self.admission()
        unsafe_quote["reviewers"]["a"]["evidence_quote"] = "<div>完整岗位正文</div>"
        admissions = self.write_admissions("unsafe-reviewer-quote.jsonl", [unsafe_quote])
        with self.assertRaisesRegex(B.ReleaseError, "quote is unsafe"):
            B.build_release(self.source, admissions, self.release_date, self.base / "unsafe-reviewer-output")

    def test_reviewer_context_lane_and_quote_linkage_fail_closed(self) -> None:
        same_context = self.admission()
        same_context["reviewers"]["b"]["execution_context_id"] = "context-a"
        admissions = self.write_admissions("same-context.jsonl", [same_context])
        with self.assertRaisesRegex(B.ReleaseError, "contexts"):
            B.build_release(self.source, admissions, self.release_date, self.base / "same-context-output")

        lane_disagreement = self.admission()
        lane_disagreement["reviewers"]["b"]["lane"] = "C"
        admissions = self.write_admissions("lane-disagreement.jsonl", [lane_disagreement])
        with self.assertRaisesRegex(B.ReleaseError, "same A/B/C role lane"):
            B.build_release(self.source, admissions, self.release_date, self.base / "lane-disagreement-output")

        unlinked_quote = self.admission()
        unlinked_quote["reviewers"]["a"]["evidence_quote"] = "没有出现在岗位职责摘录中的句子"
        admissions = self.write_admissions("unlinked-quote.jsonl", [unlinked_quote])
        with self.assertRaisesRegex(B.ReleaseError, "not linked"):
            B.build_release(self.source, admissions, self.release_date, self.base / "unlinked-quote-output")

    def test_public_minimum_may_bind_one_of_two_distinct_sealed_quotes(self) -> None:
        row = self.admission()
        row["reviewers"]["b"]["evidence_quote"] = (
            "另一位独立 Reviewer 引用同一岗位中的智能体评测与可靠性职责。"
        )
        row["_sealed_duty_quotes"] = [
            row["agent_specific_excerpt"],
            row["reviewers"]["b"]["evidence_quote"],
        ]
        admissions = self.write_admissions("one-of-two-linked-quotes.jsonl", [row])
        result = B.build_release(
            self.source,
            admissions,
            self.release_date,
            self.base / "one-of-two-linked-quotes-output",
        )
        self.assertEqual(result["admitted"], 1)

    def test_four_layer_antijoin_proof_is_mandatory(self) -> None:
        missing_layer = self.admission()
        admissions = self.write_admissions("missing-antijoin.jsonl", [missing_layer])
        manifest_path = Path(
            missing_layer["sealed_evidence"]["antijoin_input_manifest"]["path"]
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["layers"].pop("batch_zero_conflict")
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(B.ReleaseError, "hash mismatch"):
            B.build_release(self.source, admissions, self.release_date, self.base / "missing-antijoin-output")

    def test_four_layer_antijoin_is_recomputed_from_semantic_rows(self) -> None:
        for layer in (
            "canonical_roles_zero_conflict",
            "prior_sidecars_zero_conflict",
            "current_run_candidates_zero_conflict",
            "batch_zero_conflict",
        ):
            row = self.admission(_sealed_test_conflict_layer=layer)
            admissions = self.write_admissions(f"semantic-conflict-{layer}.jsonl", [row])
            with self.subTest(layer=layer):
                with self.assertRaisesRegex(B.ReleaseError, "semantic conflict"):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"semantic-conflict-{layer}-output",
                    )

    def test_timestamp_chain_and_strict_checked_at_fail_closed(self) -> None:
        cases = []
        malformed = self.admission()
        malformed["verification"]["checked_at"] = "2026-08-06garbage"
        cases.append(("malformed", malformed))
        wrong_utc_day = self.admission()
        wrong_utc_day["verification"]["checked_at"] = "2026-08-06T02:00:00+08:00"
        cases.append(("wrong-utc-day", wrong_utc_day))
        late_review = self.admission()
        late_review["reviewers"]["b"]["reviewed_at"] = "2026-08-06T03:00:00Z"
        cases.append(("late-review", late_review))
        late_roster = self.admission()
        late_roster["reviewers"]["roster_sealed_at"] = "2026-08-06T01:05:00Z"
        cases.append(("late-roster", late_roster))
        stale_review = self.admission()
        stale_review["reviewers"]["a"]["reviewed_at"] = "2020-01-01T00:00:00Z"
        cases.append(("stale-review", stale_review))
        for name, row in cases:
            admissions = self.write_admissions(f"time-{name}.jsonl", [row])
            with self.subTest(name=name):
                with self.assertRaises(B.ReleaseError):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"time-{name}-output",
                    )

    def test_actual_ttl_uses_stricter_deadline_and_rejects_invalid_values(self) -> None:
        row = self.admission(
            ttl_days=7,
            next_check_at="2026-08-20T02:00:00Z",
        )
        admissions = self.write_admissions("ttl-stricter.jsonl", [row])
        output = self.base / "ttl-stricter-output"
        B.build_release(self.source, admissions, self.release_date, output)
        promoted = [
            item
            for item in B.load_jsonl(output / "data/map/roles.jsonl")
            if item.get("recovery_origin") == "continuous_new_role_discovery"
        ][0]
        self.assertEqual(promoted["currentness_next_check_at"], "2026-08-13T02:00:00Z")

        for name, changes in (
            ("too-long", {"ttl_days": 15}),
            ("boolean", {"ttl_days": True}),
            ("expired", {"next_check_at": "2026-08-06T01:59:59Z"}),
        ):
            admissions = self.write_admissions(
                f"ttl-{name}.jsonl", [self.admission(**changes)]
            )
            with self.subTest(name=name):
                with self.assertRaises(B.ReleaseError):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"ttl-{name}-output",
                    )

    def test_symlink_and_private_metrics_source_content_fail_closed(self) -> None:
        admissions = self.write_admissions("empty-special.jsonl", [])
        outside = self.base / "outside-secret.txt"
        outside.write_text("SECRET_SENTINEL\n", encoding="utf-8")
        (self.source / "linked-secret.txt").symlink_to(outside)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            B.build_release(
                self.source, admissions, self.release_date, self.base / "symlink-output"
            )
        (self.source / "linked-secret.txt").unlink()
        private = self.source / "metrics-private"
        private.mkdir()
        (private / "ledger.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(B.ReleaseError, "metrics-private"):
            B.build_release(
                self.source, admissions, self.release_date, self.base / "private-output"
            )

        source_link = self.base / "source-link"
        source_link.symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(B.ReleaseError, "source tree must not be a symlink"):
            B.build_release(
                source_link,
                admissions,
                self.release_date,
                self.base / "source-link-output",
            )

    def test_incremental_release_output_symlinks_fail_closed(self) -> None:
        admissions = self.write_admissions("empty-output-symlinks.jsonl", [])
        existing_target = self.base / "existing-release-target"
        existing_target.mkdir()
        existing_link = self.base / "existing-release-link"
        existing_link.symlink_to(existing_target, target_is_directory=True)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            B.build_release(self.source, admissions, self.release_date, existing_link)

        dangling_link = self.base / "dangling-release-link"
        dangling_link.symlink_to(self.base / "missing-release-target", target_is_directory=True)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            B.build_release(self.source, admissions, self.release_date, dangling_link)

        real_parent = self.base / "real-release-parent"
        real_parent.mkdir()
        linked_parent = self.base / "linked-release-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                linked_parent / "release-output",
            )

    def test_incremental_release_hostile_lock_dotdot_and_staging_fail_closed(self) -> None:
        admissions = self.write_admissions("empty-hostile-output.jsonl", [])
        victim = self.base / "release-lock-victim.txt"
        victim.write_text("DO NOT TOUCH\n", encoding="utf-8")
        lock_path = self.base / ".incremental-release.lock"
        lock_path.symlink_to(victim)
        with self.assertRaisesRegex(B.ReleaseError, "lock.*symlink"):
            B.build_release(
                self.source, admissions, self.release_date, self.base / "locked-output"
            )
        self.assertEqual(victim.read_text(encoding="utf-8"), "DO NOT TOUCH\n")
        lock_path.unlink()

        with self.assertRaisesRegex(B.ReleaseError, "must not contain"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                self.base / "lexical-parent" / ".." / "escaped-release",
            )

        outside = self.base / "hostile-staging-target"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_text("DO NOT TOUCH\n", encoding="utf-8")
        staging_link = self.base / "hostile-staging-link"
        staging_link.symlink_to(outside, target_is_directory=True)
        original_mkdtemp = B.tempfile.mkdtemp
        B.tempfile.mkdtemp = lambda **_kwargs: str(staging_link)
        try:
            with self.assertRaisesRegex(B.ReleaseError, "staging output.*symlink"):
                B.build_release(
                    self.source,
                    admissions,
                    self.release_date,
                    self.base / "hostile-staging-output",
                )
        finally:
            B.tempfile.mkdtemp = original_mkdtemp
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "DO NOT TOUCH\n")

    def test_admissions_are_read_once_and_hashed_from_same_bytes(self) -> None:
        admissions = self.write_admissions("single-read.jsonl", [self.admission()])
        original_bytes = admissions.read_bytes()
        original_normalize = B.normalize_admission

        def mutate_after_capture(row: dict, release: date) -> dict:
            admissions.write_text("", encoding="utf-8")
            return original_normalize(row, release)

        B.normalize_admission = mutate_after_capture
        output = self.base / "single-read-output"
        try:
            B.build_release(self.source, admissions, self.release_date, output)
        finally:
            B.normalize_admission = original_normalize
        metadata = json.loads(
            (output / "data/metadata/release-metadata.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            metadata["incremental_release"]["input_sha256"],
            hashlib.sha256(original_bytes).hexdigest(),
        )

    def test_duplicate_canonical_and_current_ids_fail_closed(self) -> None:
        admissions = self.write_admissions("duplicate-ids.jsonl", [self.admission()])
        for index, (stem, key) in enumerate(
            (("map/roles", "role_id"), ("current/current-opportunities", "role_id"))
        ):
            source = self.base / f"duplicate-source-{index}"
            self._fixture_source(source)
            path = source / "data" / f"{stem}.jsonl"
            rows = B.load_jsonl(path)
            rows.append(dict(rows[0]))
            jsonl(path, rows)
            with self.subTest(dataset=stem):
                with self.assertRaisesRegex(B.ReleaseError, f"duplicate {key}"):
                    B.build_release(
                        source,
                        admissions,
                        self.release_date,
                        self.base / f"duplicate-id-output-{index}",
                    )

    def test_current_is_rebuilt_from_single_role_projection(self) -> None:
        current_path = self.source / "data/current/current-opportunities.jsonl"
        tampered = B.load_jsonl(current_path)
        tampered[0]["organization_id"] = "ORG-TAMPERED"
        tampered[0]["title"] = "Tampered title"
        jsonl(current_path, tampered)
        admissions = self.write_admissions("projection.jsonl", [self.admission()])
        output = self.base / "projection-output"
        B.build_release(self.source, admissions, self.release_date, output)
        current = {
            row["role_id"]: row
            for row in B.load_jsonl(output / "data/current/current-opportunities.jsonl")
        }
        self.assertEqual(current["ROLE-BASE"]["organization_id"], "ORG-BASE")
        self.assertEqual(current["ROLE-BASE"]["title"], "Agent Engineer")

    def test_source_projection_and_metadata_counts_are_audited_before_build(self) -> None:
        admissions = self.write_admissions("source-audit.jsonl", [self.admission()])
        missing_current = self.base / "missing-current-source"
        self._fixture_source(missing_current)
        jsonl(
            missing_current / "data/current/current-opportunities.jsonl",
            [],
        )
        with self.assertRaisesRegex(B.ReleaseError, "exact public_disposition projection"):
            B.build_release(
                missing_current,
                admissions,
                self.release_date,
                self.base / "missing-current-output",
            )

        stale_metadata = self.base / "stale-metadata-source"
        self._fixture_source(stale_metadata)
        metadata_path = stale_metadata / "data/metadata/release-metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["evidence_rows"] = 99
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaisesRegex(B.ReleaseError, "metadata count drift"):
            B.build_release(
                stale_metadata,
                admissions,
                self.release_date,
                self.base / "stale-metadata-output",
            )

    def test_source_manifest_detects_copy_time_mutation(self) -> None:
        admissions = self.write_admissions("source-toctou.jsonl", [self.admission()])
        original_copy = B.copy_source

        def mutate_then_copy(
            source: Path, output: Path, expected_manifest: dict[str, str] | None = None
        ) -> None:
            (source / "marker.txt").write_text("changed\n", encoding="utf-8")
            original_copy(source, output, expected_manifest)

        B.copy_source = mutate_then_copy
        try:
            with self.assertRaisesRegex(B.ReleaseError, "source tree changed"):
                B.build_release(
                    self.source,
                    admissions,
                    self.release_date,
                    self.base / "source-toctou-output",
                )
        finally:
            B.copy_source = original_copy

    def test_same_output_is_idempotent_and_drift_fails_closed(self) -> None:
        admissions = self.write_admissions("idempotent.jsonl", [self.admission()])
        output = self.base / "idempotent-output"
        first = B.build_release(self.source, admissions, self.release_date, output)
        before = tree_hashes(output)
        second = B.build_release(self.source, admissions, self.release_date, output)
        self.assertEqual(first["admitted"], second["admitted"])
        self.assertEqual(second["status"], "completed_idempotent")
        self.assertEqual(before, tree_hashes(output))
        (output / "marker.txt").write_text("drifted\n", encoding="utf-8")
        with self.assertRaisesRegex(B.ReleaseError, "different inputs or drift"):
            B.build_release(self.source, admissions, self.release_date, output)

    def test_official_domain_cannot_create_second_organization(self) -> None:
        row = self.admission(
            organization_name="Lookalike Organization",
            organization_official_domains=["example.cn"],
        )
        row["verification"]["organization_observed"] = "Lookalike Organization"
        admissions = self.write_admissions("duplicate-domain.jsonl", [row])
        with self.assertRaisesRegex(B.ReleaseError, "already owned"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                self.base / "duplicate-domain-output",
            )

    def test_existing_organization_requires_id_or_matching_domain(self) -> None:
        row = self.admission(
            organization_name="Baseline",
            organization_official_domains=[],
        )
        row["verification"]["organization_observed"] = "Baseline"
        admissions = self.write_admissions("same-name-no-proof.jsonl", [row])
        with self.assertRaisesRegex(B.ReleaseError, "canonical ID or matching official domain"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                self.base / "same-name-no-proof-output",
            )

        proven = self.admission(
            organization_name="Baseline",
            organization_official_domains=[],
            canonical_organization_id="ORG-BASE",
        )
        proven["verification"]["organization_observed"] = "Baseline"
        proven_admissions = self.write_admissions("same-name-id-proof.jsonl", [proven])
        result = B.build_release(
            self.source,
            proven_admissions,
            self.release_date,
            self.base / "same-name-id-proof-output",
        )
        self.assertEqual(result["admitted"], 1)

    def test_actual_sidecar_adapter_builds_sealed_admission_pack(self) -> None:
        rows = [
            self.admission(
                candidate_id=f"CAND-NEW-{index}",
                stable_job_id=f"job-2026-{index}",
                ats_tenant_locator=f"self_hosted|newco.cn|job-2026-{index}",
                official_role_url=f"https://newco.cn/careers/job-2026-{index}",
                title=f"智能体平台工程师 {index}",
                display_title_zh=f"智能体平台工程师 {index}",
                display_title_en=f"Agent Platform Engineer {index}",
            )
            for index in range(10)
        ]
        for row in rows:
            row["verification"]["official_role_url"] = row["official_role_url"]
            row["verification"]["title_observed"] = row["title"]
            row["verification"]["stable_job_id_observed"] = row["stable_job_id"]
        self.write_admissions("adapter-seal-source.jsonl", rows)
        pack_hashes = {}
        for row in rows:
            candidate_id = row["candidate_id"]
            root = self.base / "sealed" / "adapter-projection" / candidate_id
            root.mkdir(parents=True, exist_ok=True)

            def write_projected(name: str, value: object, *, jsonl_file: bool) -> tuple[Path, dict]:
                path = root / name
                if jsonl_file:
                    jsonl(path, [value])
                    line = path.read_bytes().splitlines()[0]
                    sealed = {
                        "path": str(path.resolve()),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "row_sha256": hashlib.sha256(line).hexdigest(),
                    }
                else:
                    path.write_text(json.dumps(value), encoding="utf-8")
                    sealed = {
                        "path": str(path.resolve()),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                return path, sealed

            source_spec = row["sealed_evidence"]["source_sidecar"]
            source_line = next(
                line
                for line in Path(source_spec["path"]).read_bytes().splitlines()
                if json.loads(line).get("candidate_id") == candidate_id
            )
            reviewers = row["reviewers"]
            prior = []
            for key, slot in (("a", "reviewer_a"), ("b", "reviewer_b")):
                reviewer = reviewers[key]
                provenance = {"decision_sha256": reviewer["decision_sha256"]}
                prior.append(
                    {
                        "reviewer_slot": slot,
                        "reviewer_id": reviewer["reviewer_id"],
                        "duty_quote": reviewer["evidence_quote"],
                        "provenance_sha256": provenance,
                    }
                )
            source_pack = {
                "candidate_id": candidate_id,
                "stable_job_id": row["stable_job_id"],
                "ats_tenant_locator": row["ats_tenant_locator"],
                "official_role_url": row["official_role_url"],
                "organization": row["organization_name"],
                "title": row["title"],
                "cohort": "main_1",
                "prior_reviewer_duty_evidence": prior,
                "source_row_sha256": {
                    "sidecar": A.physical_row_sha(json.loads(source_line))
                },
                "ttl_basis": "sidecar.ttl.next_check_at",
                "ttl_deadline": row["next_check_at"],
            }
            _, source_pack_spec = write_projected(
                "source-revalidation-pack.jsonl", source_pack, jsonl_file=True
            )
            pack_hash = hashlib.sha256(
                (json.dumps(source_pack, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            ).hexdigest()
            pack_hashes[candidate_id] = pack_hash
            safe_pack = {
                "candidate_id": candidate_id,
                "stable_job_id": row["stable_job_id"],
                "ats_tenant_locator": row["ats_tenant_locator"],
                "official_role_url": row["official_role_url"],
                "organization": row["organization_name"],
                "title": row["title"],
                "agent_specific_excerpt": row["agent_specific_excerpt"],
                "reviewer_duty_quotes": [item["duty_quote"] for item in prior],
                "source_revalidation_pack_row_sha256": pack_hash,
                "raw_html_or_full_jd_stored": False,
            }
            safe_pack_path, safe_pack_spec = write_projected(
                "reviewer-pack.jsonl", safe_pack, jsonl_file=True
            )
            safe_pack_row_hash = hashlib.sha256(
                safe_pack_path.read_bytes().splitlines()[0]
            ).hexdigest()
            decision_specs = {}
            for key, source_reviewer in zip(("a", "b"), prior):
                provenance_hash = hashlib.sha256(
                    json.dumps(
                        source_reviewer["provenance_sha256"],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest()
                decision = {
                    "candidate_id": candidate_id,
                    "reviewer_id": f"{source_reviewer['reviewer_id']}::{candidate_id}",
                    "source_reviewer_id": source_reviewer["reviewer_id"],
                    "execution_context_id": None,
                    "independent_review": True,
                    "projection_of_sealed_prior_review": True,
                    "reviewed_at_status": "not_recorded_in_source_authority",
                    "authority_predates_publication_revalidation": True,
                    "verdict": "positive",
                    "lane": reviewers[key]["lane"],
                    "evidence_quote": source_reviewer["duty_quote"],
                    "reviewed_at": None,
                    "input_row_sha256": safe_pack_row_hash,
                    "source_provenance_sha256": provenance_hash,
                }
                _, decision_specs[key] = write_projected(
                    f"reviewer-{key}.jsonl", decision, jsonl_file=True
                )
            roster = {
                "sealed_at": None,
                "sealed_at_status": "not_recorded_in_source_authority",
                "projection_of_sealed_prior_review": True,
                "candidate_ids": [candidate_id],
                "reviewer_context_ids": {},
            }
            _, roster_spec = write_projected(
                "reviewer-roster.json", roster, jsonl_file=False
            )
            row["sealed_evidence"].update(
                {
                    "revalidation_pack": source_pack_spec,
                    "reviewer_pack": safe_pack_spec,
                    "reviewer_a": decision_specs["a"],
                    "reviewer_b": decision_specs["b"],
                    "reviewer_roster": roster_spec,
                }
            )
        authority, pass_rows = self.write_revalidation_authority(
            [row["candidate_id"] for row in rows], pack_hashes
        )
        entries = []
        for row in rows:
            publication_fields = {
                key: value
                for key, value in row.items()
                if key
                not in {
                    "candidate_id",
                    "stable_job_id",
                    "official_role_url",
                    "organization_name",
                    "title",
                    "geography",
                    "raw_html_or_full_jd_stored",
                    "ttl_days",
                    "next_check_at",
                    "sealed_evidence",
                    "reviewers",
                    "verification",
                    "strict_four_layer_antijoin",
                }
            }
            pass_row = pass_rows[row["candidate_id"]]
            entries.append(
                {
                    "candidate_id": row["candidate_id"],
                    "sealed_evidence": row["sealed_evidence"],
                    "publication_fields": publication_fields,
                    "revalidation_linkage": {
                        "pass_row_sha256": hashlib.sha256(
                            (json.dumps(pass_row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
                        ).hexdigest(),
                        "pack_row_sha256": pass_row["pack_row_sha256"],
                        "shard_result_sha256": "a" * 64,
                    },
                }
            )
        contract = {
            "schema_version": A.SCHEMA,
            "revalidation_authority": authority,
            "rows": entries,
        }
        content = A.build(json.dumps(contract).encode("utf-8"))
        admissions = self.base / "adapted-admissions.jsonl"
        admissions.write_bytes(content)
        output = self.base / "adapted-output"
        result = B.build_release(self.source, admissions, self.release_date, output)
        self.assertEqual(result["admitted"], 10)
        adapted = json.loads(content.splitlines()[0])
        self.assertEqual(adapted["candidate_id"], rows[0]["candidate_id"])
        self.assertEqual(adapted["ttl_days"], 7)

        pack_output = self.base / "sealed-publication-pack.jsonl"
        self.assertEqual(
            A.write_atomic_idempotent(pack_output, content),
            "completed_publication_admission_pack",
        )
        self.assertEqual(A.write_atomic_idempotent(pack_output, content), "completed_idempotent")
        lock_path = pack_output.parent / f".{pack_output.name}.lock"
        with lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(B.ReleaseError, "pack lock already held"):
                A.write_atomic_idempotent(pack_output, content)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def test_publication_adapter_requires_exact_pass_set_and_row_linkage(self) -> None:
        pass_ids = [f"CAND-PASS-{index:02d}" for index in range(10)]
        authority, pass_rows = self.write_revalidation_authority(pass_ids)
        missing = {
            "schema_version": A.SCHEMA,
            "revalidation_authority": authority,
            "rows": [
                {
                    "candidate_id": candidate_id,
                    "sealed_evidence": {},
                    "publication_fields": {},
                }
                for candidate_id in pass_ids[:-1]
            ],
        }
        with self.assertRaisesRegex(B.ReleaseError, "candidate set"):
            A.build(json.dumps(missing).encode("utf-8"))

        tampered = {
            "schema_version": A.SCHEMA,
            "revalidation_authority": authority,
            "rows": [
                {
                    "candidate_id": candidate_id,
                    "sealed_evidence": {},
                    "publication_fields": {},
                    "revalidation_linkage": {
                        "pass_row_sha256": "0" * 64,
                        "pack_row_sha256": pass_rows[candidate_id]["pack_row_sha256"],
                        "shard_result_sha256": "a" * 64,
                    },
                }
                for candidate_id in pass_ids
            ],
        }
        with self.assertRaisesRegex(B.ReleaseError, "pass linkage"):
            A.build(json.dumps(tampered).encode("utf-8"))

    def test_publication_pack_output_symlinks_fail_closed(self) -> None:
        content = b'{"candidate_id":"candidate-1"}\n'
        existing_target = self.base / "existing-pack-target.jsonl"
        existing_target.write_bytes(content)
        existing_link = self.base / "existing-pack-link.jsonl"
        existing_link.symlink_to(existing_target)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            A.write_atomic_idempotent(existing_link, content)

        dangling_link = self.base / "dangling-pack-link.jsonl"
        dangling_link.symlink_to(self.base / "missing-pack-target.jsonl")
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            A.write_atomic_idempotent(dangling_link, content)

        real_parent = self.base / "real-pack-parent"
        real_parent.mkdir()
        linked_parent = self.base / "linked-pack-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(B.ReleaseError, "symlink"):
            A.write_atomic_idempotent(linked_parent / "pack.jsonl", content)

    def test_publication_pack_hostile_lock_and_dotdot_fail_closed(self) -> None:
        content = b'{"candidate_id":"candidate-1"}\n'
        output = self.base / "hostile-pack.jsonl"
        victim = self.base / "pack-lock-victim.txt"
        victim.write_text("DO NOT TOUCH\n", encoding="utf-8")
        lock_path = output.parent / f".{output.name}.lock"
        lock_path.symlink_to(victim)
        with self.assertRaisesRegex(B.ReleaseError, "lock.*symlink"):
            A.write_atomic_idempotent(output, content)
        self.assertEqual(victim.read_text(encoding="utf-8"), "DO NOT TOUCH\n")
        lock_path.unlink()

        with self.assertRaisesRegex(B.ReleaseError, "must not contain"):
            A.write_atomic_idempotent(
                self.base / "lexical-parent" / ".." / "escaped-pack.jsonl",
                content,
            )

    def test_reviewer_and_antijoin_artifact_hash_tampering_fails_closed(self) -> None:
        for name, artifact in (
            ("reviewer", "reviewer_a"),
            ("antijoin", "canonical_roles_zero_conflict"),
        ):
            row = self.admission()
            admissions = self.write_admissions(f"tamper-{name}.jsonl", [row])
            if artifact == "reviewer_a":
                target = Path(row["sealed_evidence"][artifact]["path"])
            else:
                manifest = json.loads(
                    Path(
                        row["sealed_evidence"]["antijoin_input_manifest"]["path"]
                    ).read_text(encoding="utf-8")
                )
                target = Path(manifest["layers"][artifact]["path"])
            target.write_bytes(target.read_bytes() + b"tamper\n")
            with self.subTest(artifact=artifact):
                with self.assertRaisesRegex(B.ReleaseError, "hash mismatch"):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"tamper-{name}-output",
                    )

    def test_resealed_prior_review_projection_flag_deletion_fails_closed(self) -> None:
        row = self.admission()
        admissions = self.write_admissions("projection-mutation.jsonl", [row])

        def reseal_jsonl(spec: dict, value: dict) -> None:
            target = Path(spec["path"])
            jsonl(target, [value])
            physical = target.read_bytes().splitlines()[0]
            spec["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            spec["row_sha256"] = hashlib.sha256(physical).hexdigest()

        for key in ("reviewer_a", "reviewer_b"):
            reviewer_spec = row["sealed_evidence"][key]
            reviewer = json.loads(Path(reviewer_spec["path"]).read_text(encoding="utf-8"))
            reviewer.update(
                {
                    "execution_context_id": None,
                    "reviewed_at": None,
                    "projection_of_sealed_prior_review": True,
                    "reviewed_at_status": "not_recorded_in_source_authority",
                    "authority_predates_publication_revalidation": True,
                    "source_provenance_sha256": "a" * 64,
                }
            )
            reseal_jsonl(reviewer_spec, reviewer)

        roster_spec = row["sealed_evidence"]["reviewer_roster"]
        roster_path = Path(roster_spec["path"])
        roster = json.loads(roster_path.read_text(encoding="utf-8"))
        roster.update(
            {
                "sealed_at": None,
                "sealed_at_status": "not_recorded_in_source_authority",
                "projection_of_sealed_prior_review": True,
            }
        )
        roster_path.write_text(json.dumps(roster, separators=(",", ":")), encoding="utf-8")
        roster_spec["sha256"] = hashlib.sha256(roster_path.read_bytes()).hexdigest()
        jsonl(admissions, [row])

        result = B.build_release(
            self.source,
            admissions,
            self.release_date,
            self.base / "projection-control-output",
        )
        self.assertEqual(result["admitted"], 1)

        reviewer_spec = row["sealed_evidence"]["reviewer_a"]
        reviewer = json.loads(Path(reviewer_spec["path"]).read_text(encoding="utf-8"))
        del reviewer["projection_of_sealed_prior_review"]
        reseal_jsonl(reviewer_spec, reviewer)
        jsonl(admissions, [row])

        with self.assertRaisesRegex(B.ReleaseError, "Reviewer decision linkage"):
            B.build_release(
                self.source,
                admissions,
                self.release_date,
                self.base / "projection-mutated-output",
            )

    def test_manifest_and_validator_reject_symlink_and_private_metrics(self) -> None:
        root = self.base / "public-structure"
        root.mkdir()
        outside = self.base / "outside.txt"
        outside.write_text("secret\n", encoding="utf-8")
        (root / "linked.txt").symlink_to(outside)
        old_validator_root, old_manifest_root = V.ROOT, M.ROOT
        try:
            V.ROOT = root
            M.ROOT = root
            self.assertTrue(
                any("symlink_forbidden" in item for item in V.filesystem_structure_errors())
            )
            with self.assertRaisesRegex(ValueError, "symlink forbidden"):
                M.build()
            (root / "linked.txt").unlink()
            (root / "metrics-private").mkdir()
            self.assertTrue(
                any(
                    "private_metrics_forbidden" in item
                    for item in V.filesystem_structure_errors()
                )
            )
            with self.assertRaisesRegex(ValueError, "private metrics forbidden"):
                M.build()
        finally:
            V.ROOT, M.ROOT = old_validator_root, old_manifest_root

    def test_verification_organization_must_match(self) -> None:
        row = self.admission()
        row["verification"]["organization_observed"] = "Different Company"
        admissions = self.write_admissions("wrong-org.jsonl", [row])
        with self.assertRaisesRegex(B.ReleaseError, "observed identity mismatch"):
            B.build_release(self.source, admissions, self.release_date, self.base / "wrong-org-output")

    def test_live_check_requires_public_readable_actionable_and_explicit_identity(self) -> None:
        required_fields = (
            ("public_readable", "hard gates failed"),
            ("actionable_apply", "hard gates failed"),
            ("title_observed", "observed identity missing"),
            ("stable_job_id_observed", "observed identity missing"),
            ("organization_observed", "observed identity missing"),
        )
        for field, error in required_fields:
            with self.subTest(field=field):
                row = self.admission()
                row["verification"].pop(field)
                admissions = self.write_admissions(f"missing-{field}.jsonl", [row])
                with self.assertRaisesRegex(B.ReleaseError, error):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"missing-{field}-output",
                    )

    def test_live_check_observed_title_and_stable_id_must_match(self) -> None:
        for field, value in (
            ("title_observed", "Different role"),
            ("stable_job_id_observed", "different-stable-id"),
        ):
            with self.subTest(field=field):
                row = self.admission()
                row["verification"][field] = value
                admissions = self.write_admissions(f"mismatch-{field}.jsonl", [row])
                with self.assertRaisesRegex(B.ReleaseError, "observed identity mismatch"):
                    B.build_release(
                        self.source,
                        admissions,
                        self.release_date,
                        self.base / f"mismatch-{field}-output",
                    )

    def test_failure_after_copy_is_atomic_and_lock_is_exclusive(self) -> None:
        admissions = self.write_admissions("atomic.jsonl", [self.admission()])
        output = self.base / "atomic-output"
        original = B.replace_snapshot_tokens
        try:
            B.replace_snapshot_tokens = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("injected"))
            with self.assertRaisesRegex(RuntimeError, "injected"):
                B.build_release(self.source, admissions, self.release_date, output)
        finally:
            B.replace_snapshot_tokens = original
        self.assertFalse(output.exists())

        lock_path = self.base / ".incremental-release.lock"
        with lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(B.ReleaseError, "lock already held"):
                B.build_release(self.source, admissions, self.release_date, output)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _copy_public_docs(self, root: Path) -> None:
        (root / "docs").mkdir(parents=True, exist_ok=True)
        for relative in (
            "README.md",
            "docs/DATA_SCALE_AND_SCOPE.md",
            "docs/MAINTENANCE.md",
            "docs/DATA_DICTIONARY.md",
            "docs/METHODOLOGY.md",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)

    def _synthetic_snapshot(self) -> tuple[dict, dict, dict]:
        before = {
            "evidence": 1,
            "organizations": 1,
            "teams": 1,
            "products": 1,
            "roles": 1,
            "relations": 1,
            "current": 1,
            "review": 1,
        }
        after = {
            "evidence": 10_001,
            "organizations": 1_111,
            "teams": 2_222,
            "products": 3_333,
            "roles": 2_002,
            "relations": 4_444,
            "current": 1_800,
            "review": 4_004,
        }
        snapshot = {
            **after,
            "verified": 1_900,
            "probable": 102,
            "noncurrent": 202,
            "verified_noncurrent": 100,
            "current_teams": 1_500,
            "teams_without_current": 722,
            "incremental_roles": 689,
            "baseline_roles": 1_313,
            "location": {
                "normalized_or_descriptive": 1_700,
                "pending_review": 200,
                "company_or_context_only": 100,
                "official_role_title_location_reviewed": 2,
            },
            "arrangement": {"onsite": 1_500, "remote_or_hybrid": 502},
            "arrangement_basis": {
                "default_onsite_no_remote_signal": 1_400,
                "explicit_onsite": 100,
                "explicit_remote_or_hybrid": 502,
            },
            "current_geography": {"China": 1_000, "United States": 800},
        }
        return before, after, snapshot

    def test_snapshot_projection_is_semantic_and_preserves_historical_numbers(self) -> None:
        root = self.base / "snapshot-docs"
        self._copy_public_docs(root)
        before, after, snapshot = self._synthetic_snapshot()
        B.replace_snapshot_tokens(root, before, after, "2026-08-06", snapshot)
        readme = (root / "README.md").read_text(encoding="utf-8")
        scale = (root / "docs/DATA_SCALE_AND_SCOPE.md").read_text(encoding="utf-8")
        maintenance = (root / "docs/MAINTENANCE.md").read_text(encoding="utf-8")
        dictionary = (root / "docs/DATA_DICTIONARY.md").read_text(encoding="utf-8")
        methodology = (root / "docs/METHODOLOGY.md").read_text(encoding="utf-8")
        self.assertIn("10,001 条**安全证据索引**", readme)
        self.assertIn("2,002 条岗位记录：1,900 条已核实岗位、102 条高概率岗位", readme)
        self.assertIn("1,800 条经 2026-08-06 正式复核", readme)
        self.assertIn("| 5,358 | 其他证据 | `10,001 - 4,643`", scale)
        self.assertIn("| 202 | 不在 Current 的岗位 | `2,002 - 1,800`", scale)
        self.assertIn("4,643 条冻结线索", scale)
        self.assertIn("严格 Current=1,800；它由 2,002 条", maintenance)
        self.assertIn("默认 Current 只由 `1,800` 条", dictionary)
        self.assertIn(
            "因此 10,001 条 Evidence、2,002 条岗位记录和 1,800 条 2026-08-06 严格 Current",
            methodology,
        )
        self.assertIn("Current 由全部 2,002 条唯一公开处置直接投影", methodology)
        self.assertNotIn("严格 Current=4,004", maintenance)
        B.replace_snapshot_tokens(root, before, after, "2026-08-07", snapshot)
        self.assertIn(
            "1,800 条经 2026-08-07 正式复核",
            (root / "README.md").read_text(encoding="utf-8"),
        )

    def test_snapshot_projection_missing_or_repeated_label_fails_closed(self) -> None:
        before, after, snapshot = self._synthetic_snapshot()
        for name, mutate, expected in (
            (
                "duplicate",
                lambda root: (root / "README.md").write_text(
                    (root / "README.md").read_text(encoding="utf-8")
                    + "\n- 7,217 条**安全证据索引**；\n",
                    encoding="utf-8",
                ),
                "found 2",
            ),
            (
                "missing",
                lambda root: (root / "docs/MAINTENANCE.md").write_text(
                    "# 维护手册\n", encoding="utf-8"
                ),
                "found 0",
            ),
        ):
            root = self.base / f"snapshot-{name}"
            self._copy_public_docs(root)
            mutate(root)
            with self.subTest(name=name):
                with self.assertRaisesRegex(B.ReleaseError, expected):
                    B.replace_snapshot_tokens(
                        root, before, after, "2026-08-06", snapshot
                    )

    def _incremental_validation_fixture(self, name: str) -> tuple[Path, dict, dict]:
        admissions = self.write_admissions(f"{name}.jsonl", [self.admission()])
        output = self.base / f"{name}-output"
        B.build_release(self.source, admissions, self.release_date, output)
        datasets = {
            "evidence-ledger-safe": B.load_jsonl(
                output / "data/evidence/evidence-ledger-safe.jsonl"
            ),
            "organizations": B.load_jsonl(output / "data/map/organizations.jsonl"),
            "teams": B.load_jsonl(output / "data/map/teams.jsonl"),
            "products": B.load_jsonl(output / "data/map/products.jsonl"),
            "roles": B.load_jsonl(output / "data/map/roles.jsonl"),
            "relations": B.load_jsonl(output / "data/map/relations.jsonl"),
            "current-opportunities": B.load_jsonl(
                output / "data/current/current-opportunities.jsonl"
            ),
            "review-queue": B.load_jsonl(output / "data/review/review-queue.jsonl"),
        }
        metadata = json.loads(
            (output / "data/metadata/release-metadata.json").read_text(
                encoding="utf-8"
            )
        )
        return output, datasets, metadata

    def test_incremental_metadata_delta_and_seal_form_exact_closure(self) -> None:
        output, datasets, metadata = self._incremental_validation_fixture("closure")
        self.assertEqual(V.incremental_release_errors(datasets, metadata, output), [])

    def test_real_public_tree_incremental_build_passes_default_validator(self) -> None:
        source_role_count = len(B.load_jsonl(ROOT / "data/map/roles.jsonl"))
        source_current_count = len(
            B.load_jsonl(ROOT / "data/current/current-opportunities.jsonl")
        )
        admissions = self.write_admissions("real-tree.jsonl", [self.admission()])
        output = self.base / "real-tree-output"
        B.build_release(ROOT, admissions, self.release_date, output)
        old_validator_root = V.ROOT
        try:
            V.ROOT = output
            result = V.run_default()
        finally:
            V.ROOT = old_validator_root
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["counts"]["roles"], source_role_count + 1)
        self.assertEqual(
            result["counts"]["current-opportunities"], source_current_count + 1
        )

    def test_incremental_metadata_delta_and_seal_negative_controls(self) -> None:
        output, datasets, metadata = self._incremental_validation_fixture("negative")
        stale_batch = json.loads(json.dumps(metadata))
        stale_batch["incremental_release"]["batch_roles_added"] = 99
        self.assertIn(
            "incremental_batch_role_count",
            V.incremental_release_errors(datasets, stale_batch, output),
        )

        fake_input = json.loads(json.dumps(metadata))
        fake_input["incremental_release"]["input_sha256"] = "f" * 64
        self.assertIn(
            "incremental_input_sha256_seal_mismatch",
            V.incremental_release_errors(datasets, fake_input, output),
        )

        wrong_evidence = json.loads(json.dumps(metadata))
        wrong_evidence["incremental_release"]["batch_evidence_added"] = 99
        self.assertIn(
            "incremental_batch_evidence_count",
            V.incremental_release_errors(datasets, wrong_evidence, output),
        )

        delta_path = output / "data/metadata/release-delta.json"
        delta = json.loads(delta_path.read_text(encoding="utf-8"))
        delta["release_as_of"] = "2026-08-07"
        delta["before"]["roles"] += 1
        delta["changed"]["role_ids_added"].append(delta["changed"]["role_ids_added"][0])
        delta_path.write_text(B.stable_json(delta, pretty=True), encoding="utf-8")
        errors = V.incremental_release_errors(datasets, metadata, output)
        self.assertIn("incremental_release_date_mismatch", errors)
        self.assertIn("incremental_delta_not_closed:roles", errors)
        self.assertIn("incremental_delta_role_ids_invalid", errors)

        delta = json.loads(delta_path.read_text(encoding="utf-8"))
        delta["changed"]["role_ids_added"] = ["ROLE-EXTRA-NOT-IN-DATASET"]
        delta_path.write_text(B.stable_json(delta, pretty=True), encoding="utf-8")
        self.assertIn(
            "incremental_delta_role_ids_not_incremental",
            V.incremental_release_errors(datasets, metadata, output),
        )

        seal_path = output / "data/metadata/incremental-build-seal.json"
        seal = json.loads(seal_path.read_text(encoding="utf-8"))
        seal["release_metadata_sha256"] = "0" * 64
        seal_path.write_text(B.stable_json(seal, pretty=True), encoding="utf-8")
        self.assertIn(
            "incremental_build_seal_metadata_hash",
            V.incremental_release_errors(datasets, metadata, output),
        )


if __name__ == "__main__":
    unittest.main()
