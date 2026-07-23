# Agent Hiring Map：中美 Agent 岗位地图

这是一个基于公开来源、可追溯、可下载的中国与美国 Agent 岗位地图。

当前公开版本包含：

- 7,217 条**安全证据索引**；
- 中国和美国的组织、团队、产品、岗位及其关系；
- 经过日期与来源门筛选的当前岗位视图；
- 新岗位建议、纠错、定期复核、降级、替代和回滚的维护工具。

> 重要：7,217 是历史证据行数，不是当前岗位数、招聘人数或市场规模。本项目也不承诺实时或绝对完整。

## 快速使用

只看当前岗位：

- `data/current/current-opportunities.csv`
- `data/current/current-opportunities.jsonl`

查看标准化地图：

- `data/map/organizations.*`
- `data/map/teams.*`
- `data/map/products.*`
- `data/map/roles.*`
- `data/map/relations.*`

用中文查看全部团队、每团队岗位数和整体分类分布：

- [团队与岗位全景总览](docs/TEAM_ROLE_OVERVIEW.md)

查看全部证据的安全索引：

- `data/evidence/evidence-ledger-safe.*`

CSV 适合表格软件；JSONL 是“一行一个结构化对象”的文本格式，适合程序和 Agent。

## 当前数据边界

- 标准化地图和当前岗位只覆盖中国与美国；
- Other/Global/Unknown 只保留既有证据索引，不做标准化扩张；
- 当前岗位必须有官方公开来源、Agent 相关最短必要引文、最后复核日期和访问要求；
- unknown、stale、blocked、disputed、duplicate、superseded、closed、付费或私人来源不会进入当前岗位；
- 完整招聘正文不在本仓库再发布。

发布时从 P0–P3 的 920 条当前岗位候选中移除了日期异常或超过期限的记录。实际公开数量和差异原因见：

- `data/metadata/release-metadata.json`
- `data/metadata/release-delta.json`

## 新岗位怎么加入

新岗位不能直接写入正式数据。请使用 GitHub 的“岗位新增或纠错”模板，或按 `schemas/submission.schema.json` 提交结构化建议。

流程是：

```text
建议
→ 安全与格式检查
→ 官方来源检查
→ 组织归属检查
→ 重复/替代检查
→ currentness 检查
→ 人工审核
→ 全量重建和验证
→ 合并进入新版本
```

详细规则见 [贡献指南](docs/CONTRIBUTING.md)。

## 如何定期复核

- 当前岗位复核期限是 14 天；
- 每周只读工作流生成到期复核队列；
- 临时 404、429、5xx 或挑战页不能自动关闭岗位；
- 只有足够的一手证据才能确认关闭；
- 所有降级、替代和回滚保留历史。

详细操作见 [维护手册](docs/MAINTENANCE.md)。

## 本地验证

只依赖 Python 3 标准库：

```bash
python3 scripts/validate_public_package.py
python3 scripts/validate_public_package.py --self-test
python3 scripts/validate_public_package.py --final
```

生成指定日期的离线复核队列：

```bash
python3 scripts/build_review_queue.py --as-of 2026-08-01 --output review-queue.jsonl
```

记录不含个人信息的每周 GitHub 汇总数字：

```bash
python3 scripts/record_aggregate_metrics.py \
  --date 2026-08-01 \
  --views 0 --unique-views 0 \
  --clones 0 --unique-clones 0 \
  --stars 0 --forks 0 \
  --output metrics/week-01.json
```

汇总数字不计作独立或重复使用证据。

验证一条岗位建议：

```bash
python3 scripts/validate_submission.py examples/submissions/valid-china-role.json
```

## 项目状态

- P0–P3：中国与美国公开来源有界验证已通过；
- P4：公开仓库已于 2026-07-23 进入至少四周的只读观察；
- 外部 Claim 写入接口：未开放；
- 网站、API、MCP、岗位申请和消息功能：未开放；
- 需求、规模化、PMF 和候选人就绪：均未证明。

观察状态与通过门见 [P4 观察记录](docs/OBSERVATION.md)。

## 文档入口

- [规则权威](docs/AUTHORITY.md)
- [字段和状态](docs/DATA_DICTIONARY.md)
- [团队与岗位全景总览](docs/TEAM_ROLE_OVERVIEW.md)
- [贡献指南](docs/CONTRIBUTING.md)
- [维护手册](docs/MAINTENANCE.md)
- [方法和限制](docs/METHODOLOGY.md)
- [安全政策](SECURITY.md)
- [版本记录](docs/CHANGELOG.md)

## 许可证

- 代码：Apache License 2.0，见 `LICENSE-CODE`；
- 本项目原创整理的数据和文档：CC BY 4.0，见 `LICENSE-DATA`；
- 第三方内容不被本项目重新授权，见 `NOTICE`。
