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

任何自动化都不能绕过人工审核把外部文本写入正式地图。

