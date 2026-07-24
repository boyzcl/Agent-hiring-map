# 规则权威

发生冲突时按以下顺序处理：

1. 当前版本的数据 schema 和发布 manifest；
2. 本仓库的 `docs/MAINTENANCE.md` 与 `docs/CONTRIBUTING.md`；
3. `docs/DATA_DICTIONARY.md`；
4. `docs/METHODOLOGY.md`；
5. 历史版本和变更记录。

数据层级必须保持分开：

- `data/evidence/` 是证据安全索引，不代表当前岗位；
- `data/map/` 是标准化对象和关系；
- `data/current/` 是通过 currentness 门的当前岗位快照；
- `data/review/` 是待复核队列，不是正式岗位；
- GitHub issue、合并请求和建议文件都是待审核输入，不能直接覆盖正式数据。

`docs/TEAM_ROLE_OVERVIEW.md` 是从上述正式数据确定性生成的中文展示页，方便查看团队、数量和分布；它不是新的权威数据层。展示页与底层 JSONL 冲突时，以 schema、manifest 和底层 JSONL 为准。

`docs/DATA_SCALE_AND_SCOPE.md` 是当前发布快照的派生数据背景参考，用于解释证据、岗位、Current、团队和恢复终态的不同分母，以及剩余探索空间；它不取代发布元数据、正式 JSONL 或验证报告。冲突时仍以 schema、manifest、正式 JSONL 和 validator 结果为准。

公开筛选网页也是只读展示层。它在浏览器中直接读取 `data/map/`、`data/current/` 和发布元数据，不保存或提升外部输入，不构成新的岗位、当前性或组织归属判断。网页显示与底层数据冲突时，仍以 schema、manifest 和底层 JSONL 为准。

任何自动化都不能绕过人工审核把外部文本写入正式地图。
