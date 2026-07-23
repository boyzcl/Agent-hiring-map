#!/usr/bin/env python3
"""Deterministically build the Chinese team and role overview document."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "TEAM_ROLE_OVERVIEW.md"

CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "安全、治理与合规",
        (
            "security",
            "safety",
            "governance",
            "compliance",
            "risk",
            "trust",
            "identity",
            "policy",
            "secure",
            "安全",
            "治理",
            "合规",
        ),
    ),
    (
        "评测、测试与质量",
        (
            "evaluation",
            "eval",
            "test",
            "quality",
            "observability",
            "benchmark",
            "red_team",
            "red team",
            "评测",
            "测试",
            "质量",
        ),
    ),
    (
        "产品与设计",
        (
            "product",
            "design",
            "designer",
            "ux",
            "ui",
            "产品",
            "设计",
        ),
    ),
    (
        "商务、市场与合作",
        (
            "gtm",
            "sales",
            "marketing",
            "commercial",
            "partnership",
            "partner",
            "business_development",
            "business development",
            "growth",
            "account executive",
            "销售",
            "市场",
            "商务",
            "合作",
        ),
    ),
    (
        "客户解决方案与交付",
        (
            "solution",
            "solutions",
            "forward_deployed",
            "forward deployed",
            "fde",
            "delivery",
            "implementation",
            "customer",
            "adoption",
            "consult",
            "architect",
            "support",
            "解决方案",
            "交付",
            "客户",
            "架构",
        ),
    ),
    (
        "运营、项目与职能",
        (
            "operations",
            "operation",
            "program",
            "project",
            "recruit",
            "talent",
            "strategy",
            "human_resources",
            "human resources",
            "finance",
            "legal",
            "chief_of_staff",
            "chief of staff",
            "运营",
            "项目",
            "招聘",
            "战略",
        ),
    ),
    (
        "算法、研究与模型",
        (
            "research",
            "scientist",
            "algorithm",
            "training",
            "post_training",
            "post-training",
            "model",
            "machine_learning",
            "machine learning",
            "reinforcement",
            "reasoning",
            "alignment",
            "算法",
            "研究",
            "训练",
            "模型",
        ),
    ),
    (
        "平台、基础设施与数据",
        (
            "platform",
            "infra",
            "infrastructure",
            "orchestration",
            "data",
            "backend",
            "cloud",
            "devops",
            "sre",
            "database",
            "distributed",
            "systems",
            "rag",
            "retrieval",
            "context",
            "平台",
            "基础设施",
            "数据",
            "后端",
        ),
    ),
    (
        "工程与应用开发",
        (
            "engineer",
            "engineering",
            "developer",
            "application",
            "full_stack",
            "full stack",
            "frontend",
            "software",
            "coding",
            "开发",
            "工程",
        ),
    ),
)

CATEGORY_ORDER = tuple(name for name, _ in CATEGORY_RULES) + ("其他或边界岗位",)
GEOGRAPHY_LABELS = {
    ("China",): "中国",
    ("United States",): "美国",
    ("China", "United States"): "中国、美国",
}
CURRENTNESS_LABELS = {
    "current_verified": "已确认当前有效",
    "current_probable": "很可能当前有效",
    "stale_unverified": "已过期、未重新确认",
    "closed_verified": "已确认关闭",
    "disputed": "存在争议",
}
ACCESS_LABELS = {
    "public_no_login": "公开网页、无需登录",
    "official_free_account": "官方免费账号后可查看",
    "user_assisted_auth": "需要用户协助认证",
    "paid_or_private_blocked": "付费或私人来源、禁止进入当前岗位",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def unique_index(rows: Iterable[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row[key]
        if value in result:
            raise ValueError(f"duplicate {key}: {value}")
        result[value] = row
    return result


def role_category(role: dict[str, Any]) -> str:
    # role_family is the existing normalized label and therefore takes precedence.
    # The title is only a fallback for a future record without that field.
    text = str(role.get("role_family") or role.get("title") or "").lower()
    for category, keywords in CATEGORY_RULES:
        if any(keyword in text for keyword in keywords):
            return category
    return "其他或边界岗位"


def percent(count: int, total: int) -> str:
    return "0.0%" if total == 0 else f"{count / total * 100:.1f}%"


def escape_cell(value: Any) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def summarize_categories(counter: Counter[str]) -> str:
    if not counter:
        return "—"
    ordered = sorted(
        counter.items(),
        key=lambda item: (-item[1], CATEGORY_ORDER.index(item[0])),
    )
    return "；".join(f"{name} {count}" for name, count in ordered)


def size_band(count: int) -> str:
    if count == 0:
        return "0"
    if count == 1:
        return "1"
    if count <= 4:
        return "2–4"
    if count <= 9:
        return "5–9"
    return "10 及以上"


def geography_label(values: list[str]) -> str:
    key = tuple(sorted(values, key=("China", "United States").index))
    if key not in GEOGRAPHY_LABELS:
        raise ValueError(f"unsupported team geography: {values}")
    return GEOGRAPHY_LABELS[key]


def category_table(
    all_counts: Counter[str],
    current_counts: Counter[str],
    all_total: int,
    current_total: int,
) -> list[str]:
    lines = [
        "| 阅读用岗位类别 | 地图岗位记录 | 占地图岗位 | 当前岗位 | 占当前岗位 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for category in CATEGORY_ORDER:
        all_count = all_counts[category]
        current_count = current_counts[category]
        lines.append(
            f"| {category} | {all_count} | {percent(all_count, all_total)} | "
            f"{current_count} | {percent(current_count, current_total)} |"
        )
    lines.append(
        f"| **合计** | **{all_total}** | **100.0%** | "
        f"**{current_total}** | **100.0%** |"
    )
    return lines


def distribution_table(
    heading: str,
    counts: Counter[str],
    labels: dict[str, str],
    total: int,
) -> list[str]:
    lines = [
        f"### {heading}",
        "",
        "| 类型 | 数量 | 占比 |",
        "| --- | ---: | ---: |",
    ]
    for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {labels.get(key, key)} | {count} | {percent(count, total)} |")
    return lines


def build_document() -> str:
    metadata = load_json(ROOT / "data" / "metadata" / "release-metadata.json")
    organizations = load_jsonl(ROOT / "data" / "map" / "organizations.jsonl")
    teams = load_jsonl(ROOT / "data" / "map" / "teams.jsonl")
    roles = load_jsonl(ROOT / "data" / "map" / "roles.jsonl")
    current = load_jsonl(ROOT / "data" / "current" / "current-opportunities.jsonl")

    organization_by_id = unique_index(organizations, "organization_id")
    team_by_id = unique_index(teams, "team_id")
    role_by_id = unique_index(roles, "role_id")
    current_by_id = unique_index(current, "role_id")

    expected = metadata["canonical_counts"]
    if len(organizations) != expected["organizations"]:
        raise ValueError("organization count does not match release metadata")
    if len(teams) != expected["teams"]:
        raise ValueError("team count does not match release metadata")
    if len(roles) != expected["roles"]:
        raise ValueError("role count does not match release metadata")
    if len(current) != metadata["current_opportunities"]["rows"]:
        raise ValueError("current opportunity count does not match release metadata")

    roles_by_team: dict[str, list[dict[str, Any]]] = defaultdict(list)
    current_by_team: dict[str, list[dict[str, Any]]] = defaultdict(list)
    role_categories: dict[str, str] = {}

    for role in roles:
        team_id = role.get("team_id")
        if not team_id or team_id not in team_by_id:
            raise ValueError(f"role has no resolvable team: {role['role_id']}")
        roles_by_team[team_id].append(role)
        role_categories[role["role_id"]] = role_category(role)

    for opportunity in current:
        role_id = opportunity["role_id"]
        role = role_by_id.get(role_id)
        if role is None:
            raise ValueError(f"current opportunity has no role: {role_id}")
        if opportunity.get("team_id") != role.get("team_id"):
            raise ValueError(f"current opportunity team mismatch: {role_id}")
        current_by_team[role["team_id"]].append(opportunity)

    all_category_counts = Counter(role_categories.values())
    current_category_counts = Counter(
        role_categories[role_id] for role_id in current_by_id
    )
    if sum(all_category_counts.values()) != len(roles):
        raise ValueError("map category totals do not add up")
    if sum(current_category_counts.values()) != len(current):
        raise ValueError("current category totals do not add up")

    teams_with_current = sum(bool(current_by_team[team["team_id"]]) for team in teams)
    teams_without_current = len(teams) - teams_with_current
    teams_with_map_roles = sum(bool(roles_by_team[team["team_id"]]) for team in teams)
    teams_without_map_roles = len(teams) - teams_with_map_roles
    current_size_bands = Counter(
        size_band(len(current_by_team[team["team_id"]])) for team in teams
    )
    currentness_counts = Counter(role.get("currentness_status") or "（未记录）" for role in roles)
    access_counts = Counter(
        opportunity.get("access_requirement") or "（未记录）" for opportunity in current
    )
    evidence_counts = Counter(
        opportunity.get("evidence_grade") or "（未记录）" for opportunity in current
    )
    remote_counts = Counter(
        "明确标注远程或混合办公"
        if role_by_id[opportunity["role_id"]].get("remote_scope")
        else "未记录远程或混合办公范围"
        for opportunity in current
    )
    geography_counts = Counter(opportunity["geography"] for opportunity in current)

    top_families = Counter(
        (role.get("role_family") or "（未记录）") for role in roles
    ).most_common(25)

    lines = [
        "# 团队与岗位全景总览",
        "",
        f"> 数据快照日期：{metadata['release_as_of']}。本页由 "
        "`scripts/build_team_role_overview.py` 从公开 JSONL 数据确定性生成；"
        "底层数据仍是唯一权威来源。",
        "",
        "## 先看结论",
        "",
        "| 指标 | 数量 | 说明 |",
        "| --- | ---: | --- |",
        f"| 团队总数 | {len(teams)} | 中国、美国及 3 个同时标注中美地域的团队 |",
        f"| 有地图岗位记录的团队 | {teams_with_map_roles} | 至少关联 1 条标准化 Role 记录 |",
        f"| 没有地图岗位记录的团队 | {teams_without_map_roles} | 仍保留团队及其证据关系 |",
        f"| 有当前岗位的团队 | {teams_with_current} | 至少有 1 条记录进入当前岗位视图 |",
        f"| 当前岗位为 0 的团队 | {teams_without_current} | 不等于该团队永久不招聘 |",
        f"| 地图岗位记录 | {len(roles)} | 标准化 Role 对象，包含当前、过期、关闭或争议记录 |",
        f"| 当前岗位 | {len(current)} | 通过本次公开快照的日期、来源和访问门 |",
        f"| 安全证据索引 | {metadata['evidence_rows']} | **不是岗位数，也不是招聘人数** |",
        "",
        "## 统计口径",
        "",
        "- **地图岗位记录**：`data/map/roles.jsonl` 中的标准化 Role 对象。它是岗位记录，不代表仍在招聘，也不代表招聘人数。",
        "- **当前岗位**：`data/current/current-opportunities.jsonl` 中通过当前性、官方来源、日期、证据和访问要求门的岗位。",
        "- **每团队岗位数**：岗位通过唯一 `team_id` 计入一个团队，因此不会因产品关系或证据行重复计数。",
        "- **当前岗位为 0**：只表示当前快照中没有岗位通过当前视图门；不能推断团队不存在、停止运营或永久不招聘。",
        "- **岗位类别**：为方便阅读，根据已有 `role_family` 和岗位名称按下文固定优先顺序生成的单一派生类别；它不是新增的正式数据字段，不会修改底层岗位判断。",
        "- **岗位类型**：现有数据可以可靠展示地域、当前状态、证据等级、访问方式以及是否明确标注远程/混合办公；没有可靠的全职、兼职、实习或合同工字段，因此本页不猜测这些雇佣类型。",
        "",
        "## 岗位类别分布",
        "",
        "派生分类按以下优先顺序匹配：安全治理 → 评测质量 → 产品设计 → 商务市场 → "
        "客户交付 → 运营职能 → 算法研究 → 平台数据 → 工程开发 → 其他。"
        "一条岗位只计入一个类别；规则公开在生成脚本中。",
        "",
        *category_table(
            all_category_counts,
            current_category_counts,
            len(roles),
            len(current),
        ),
        "",
        "### 原始岗位族标签（前 25 项）",
        "",
        f"共有 {len(set(role.get('role_family') for role in roles))} 个不同的原始 `role_family` "
        "标签。它们粒度不统一，因此不直接当作高层分类；下表保留最常见标签，完整值仍在岗位数据中。",
        "",
        "| 原始岗位族标签 | 地图岗位记录 |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {escape_cell(name)} | {count} |" for name, count in top_families)

    lines.extend(
        [
            "",
            "## 岗位类型与状态分布",
            "",
            *distribution_table(
                "当前岗位地域",
                geography_counts,
                {"China": "中国", "United States": "美国"},
                len(current),
            ),
            "",
            *distribution_table(
                "地图岗位记录的当前状态",
                currentness_counts,
                CURRENTNESS_LABELS,
                len(roles),
            ),
            "",
            "> 注意：地图 Role 中标为“很可能当前有效”的记录，仍可能因为公开发布时的期限、访问或结构门"
            "而没有进入 911 条当前岗位；求职检索应以当前岗位视图为准。",
            "",
            *distribution_table(
                "当前岗位证据等级",
                evidence_counts,
                {},
                len(current),
            ),
            "",
            *distribution_table(
                "当前岗位访问方式",
                access_counts,
                ACCESS_LABELS,
                len(current),
            ),
            "",
            *distribution_table(
                "当前岗位远程/混合办公字段",
                remote_counts,
                {},
                len(current),
            ),
            "",
            "> “未记录远程或混合办公范围”不等于必须到岗办公，只表示现有结构化字段没有可靠记录。",
            "",
            "## 团队的当前岗位规模分布",
            "",
            "| 每团队当前岗位数 | 团队数 | 占全部团队 |",
            "| --- | ---: | ---: |",
        ]
    )
    for band in ("0", "1", "2–4", "5–9", "10 及以上"):
        count = current_size_bands[band]
        lines.append(f"| {band} | {count} | {percent(count, len(teams))} |")

    lines.extend(
        [
            "",
            "## 全部团队完整列表",
            "",
            "以下列表覆盖全部团队，包括地图岗位记录为 0 或当前岗位为 0 的团队。"
            "“类别摘要”后的数字是该团队该类岗位记录数。",
            "",
            "| 序号 | 团队 | 所属组织 | 地域 | 地图岗位记录 | 当前岗位 | 当前岗位类别摘要 | 全部岗位类别摘要 | 团队编号 |",
            "| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )

    sorted_teams = sorted(
        teams,
        key=lambda team: (
            0 if team["team_geography"] == ["China"] else
            1 if team["team_geography"] == ["United States"] else 2,
            organization_by_id[team["organization_id"]]["canonical_name"].casefold(),
            team["team_name"].casefold(),
            team["team_id"],
        ),
    )
    for index, team in enumerate(sorted_teams, start=1):
        team_id = team["team_id"]
        organization = organization_by_id.get(team["organization_id"])
        if organization is None:
            raise ValueError(f"team has no organization: {team_id}")
        all_team_categories = Counter(
            role_categories[role["role_id"]] for role in roles_by_team[team_id]
        )
        current_team_categories = Counter(
            role_categories[opportunity["role_id"]]
            for opportunity in current_by_team[team_id]
        )
        lines.append(
            "| "
            + " | ".join(
                (
                    str(index),
                    escape_cell(team["team_name"]),
                    escape_cell(organization["canonical_name"]),
                    geography_label(team["team_geography"]),
                    str(len(roles_by_team[team_id])),
                    str(len(current_by_team[team_id])),
                    escape_cell(summarize_categories(current_team_categories)),
                    escape_cell(summarize_categories(all_team_categories)),
                    f"`{team_id}`",
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 如何更新本页",
            "",
            "正式数据经过审核、全量重建和验证后，运行：",
            "",
            "```bash",
            "python3 scripts/build_team_role_overview.py",
            "python3 scripts/build_team_role_overview.py --check",
            "python3 scripts/validate_public_package.py --final",
            "```",
            "",
            "`--check` 只比较生成结果，不写文件。公开验证器也会执行同一检查，防止数据已更新而总览仍停留在旧版本。",
            "",
            "## 限制",
            "",
            "- 这是中国和美国公开来源的有界快照，不是绝对市场完整清单。",
            "- 一条 Role 是一个标准化岗位记录，不是招聘名额或人数。",
            "- 7,217 条安全证据索引可能包含产品页、招聘入口、过期记录或定位线索，不能用于推算当前岗位数。",
            "- 派生岗位类别适合总览和导航，不替代岗位原始标题、原始岗位族标签或人工判断。",
            "- 求职前应打开官方链接重新确认岗位状态、地点、资格和申请要求。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed overview differs from the generated content",
    )
    args = parser.parse_args()
    content = build_document()
    if args.check:
        if not OUTPUT.exists():
            print(f"missing generated overview: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            raise SystemExit(1)
        if OUTPUT.read_text(encoding="utf-8") != content:
            print(
                f"stale generated overview: {OUTPUT.relative_to(ROOT)}",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(
            json.dumps(
                {
                    "document": OUTPUT.relative_to(ROOT).as_posix(),
                    "status": "pass",
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return
    OUTPUT.write_text(content, encoding="utf-8")
    print(
        json.dumps(
            {
                "document": OUTPUT.relative_to(ROOT).as_posix(),
                "status": "written",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
