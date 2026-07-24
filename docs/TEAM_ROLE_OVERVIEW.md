# 团队与岗位全景总览

> 数据快照日期：2026-07-24。本页由 `scripts/build_team_role_overview.py` 从公开 JSONL 数据确定性生成；底层数据仍是唯一权威来源。

## 先看结论

| 指标 | 数量 | 说明 |
| --- | ---: | --- |
| 团队总数 | 1424 | 中国、美国及 3 个同时标注中美地域的团队 |
| 有地图岗位记录的团队 | 473 | 至少关联 1 条标准化 Role 记录 |
| 没有地图岗位记录的团队 | 951 | 仍保留团队及其证据关系 |
| 有当前岗位的团队 | 181 | 至少有 1 条记录进入当前岗位视图 |
| 当前岗位为 0 的团队 | 1243 | 不等于该团队永久不招聘 |
| 地图岗位记录 | 966 | 仅含已核实或高概率的标准化 Role 对象 |
| 当前岗位 | 491 | 通过本次公开快照的日期、来源和访问门 |
| 安全证据索引 | 7217 | **不是岗位数，也不是招聘人数** |

## 统计口径

- **地图岗位记录**：`data/map/roles.jsonl` 中的标准化 Role 对象。它是岗位记录，不代表仍在招聘，也不代表招聘人数。
- **已核实岗位 / 高概率岗位**：前者通过完整岗位真实性门；后者有官方标题和稳定定位，但仍缺少一项非核心事实。高概率岗位不会进入严格当前岗位视图。
- **当前岗位**：`data/current/current-opportunities.jsonl` 中通过当前性、官方来源、日期、证据和访问要求门的岗位。
- **每团队岗位数**：岗位通过唯一 `team_id` 计入一个团队，因此不会因产品关系或证据行重复计数。
- **当前岗位为 0**：只表示当前快照中没有岗位通过当前视图门；不能推断团队不存在、停止运营或永久不招聘。
- **岗位类别**：为方便阅读，根据已有 `role_family` 和岗位名称按下文固定优先顺序生成的单一派生类别；它不是新增的正式数据字段，不会修改底层岗位判断。
- **岗位类型**：现有数据可以可靠展示地域、当前状态、证据等级、访问方式以及是否明确标注远程/混合办公；没有可靠的全职、兼职、实习或合同工字段，因此本页不猜测这些雇佣类型。

## 岗位类别分布

派生分类按以下优先顺序匹配：安全治理 → 评测质量 → 产品设计 → 商务市场 → 客户交付 → 运营职能 → 算法研究 → 平台数据 → 工程开发 → 其他。一条岗位只计入一个类别；规则公开在生成脚本中。

| 阅读用岗位类别 | 地图岗位记录 | 占地图岗位 | 当前岗位 | 占当前岗位 |
| --- | ---: | ---: | ---: | ---: |
| 安全、治理与合规 | 50 | 5.2% | 32 | 6.5% |
| 评测、测试与质量 | 75 | 7.8% | 49 | 10.0% |
| 产品与设计 | 122 | 12.6% | 81 | 16.5% |
| 商务、市场与合作 | 18 | 1.9% | 14 | 2.9% |
| 客户解决方案与交付 | 63 | 6.5% | 43 | 8.8% |
| 运营、项目与职能 | 13 | 1.3% | 13 | 2.6% |
| 算法、研究与模型 | 132 | 13.7% | 94 | 19.1% |
| 平台、基础设施与数据 | 73 | 7.6% | 63 | 12.8% |
| 工程与应用开发 | 131 | 13.6% | 93 | 18.9% |
| 其他或边界岗位 | 289 | 29.9% | 9 | 1.8% |
| **合计** | **966** | **100.0%** | **491** | **100.0%** |

### 原始岗位族标签（前 25 项）

共有 286 个不同的原始 `role_family` 标签。它们粒度不统一，因此不直接当作高层分类；下表保留最常见标签，完整值仍在岗位数据中。

| 原始岗位族标签 | 地图岗位记录 |
| --- | ---: |
| agent_role_recovered_from_official_title | 265 |
| agent_algorithm_or_research_role | 55 |
| agent_engineering_or_application_role | 43 |
| agent_engineer_platform_or_infrastructure | 25 |
| agent_engineer_or_applied_ai_engineer | 25 |
| agent_or_ai_product_management_role | 24 |
| agent_product_manager | 20 |
| agent_operations_delivery_or_management_role | 14 |
| agent_research_training_or_evaluation_role | 14 |
| agent_security_evaluation_governance_or_response_role | 14 |
| agent_engineer | 14 |
| coding_agent_or_developer_product_role | 13 |
| agent_platform_or_application_architect_role | 13 |
| agent_eval_test_or_quality_role | 11 |
| agent_adjacent_qualification_or_ai_workflow_boundary | 10 |
| agent_engineering_operations_or_adjacent_role | 9 |
| agent_research_scientist_or_algorithm_engineer | 9 |
| agent_infrastructure_or_orchestration_role | 8 |
| agent_security_or_ai_safety_role | 8 |
| agent_product_team_adjacent_or_boundary_role | 7 |
| agent_research_training_or_model_engineering | 7 |
| forward_deployed_solutions_or_customer_delivery | 7 |
| embodied_physical_ai_product_or_infrastructure_role | 7 |
| agent_algorithm_research | 6 |
| agent_gtm_sales_or_customer_adoption | 5 |

## 岗位类型与状态分布

### 当前岗位地域

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| 中国 | 277 | 56.4% |
| 美国 | 214 | 43.6% |

### 地图岗位可信度

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| 已核实岗位 | 634 | 65.6% |
| 高概率岗位 | 332 | 34.4% |

### 地图岗位记录的当前状态

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| 很可能当前有效 | 935 | 96.8% |
| historical_closed_or_offline | 10 | 1.0% |
| 已确认关闭 | 9 | 0.9% |
| 已过期、未重新确认 | 8 | 0.8% |
| unknown | 3 | 0.3% |
| 存在争议 | 1 | 0.1% |

> 注意：地图 Role 中标为“很可能当前有效”的记录，仍可能因为公开发布时的期限、访问或结构门而没有进入 491 条当前岗位；求职检索应以当前岗位视图为准。

### 当前岗位证据等级

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| A | 482 | 98.2% |
| B | 9 | 1.8% |

### 当前岗位访问方式

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| 公开网页、无需登录 | 491 | 100.0% |

### 当前岗位远程/混合办公字段

| 类型 | 数量 | 占比 |
| --- | ---: | ---: |
| 现场办公（来源未标远程或混合时按规则默认） | 451 | 91.9% |
| 明确标注远程或混合办公 | 40 | 8.1% |

> 未明确写远程或混合办公的岗位，按本项目已确认规则归为现场办公；卡片会披露这一判断依据。

## 团队的当前岗位规模分布

| 每团队当前岗位数 | 团队数 | 占全部团队 |
| --- | ---: | ---: |
| 0 | 1243 | 87.3% |
| 1 | 148 | 10.4% |
| 2–4 | 16 | 1.1% |
| 5–9 | 9 | 0.6% |
| 10 及以上 | 8 | 0.6% |

## 全部团队完整列表

以下列表覆盖全部团队，包括地图岗位记录为 0 或当前岗位为 0 的团队。“类别摘要”后的数字是该团队该类岗位记录数。

| 序号 | 团队 | 所属组织 | 地域 | 地图岗位记录 | 当前岗位 | 当前岗位类别摘要 | 全部岗位类别摘要 | 团队编号 |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | 零一万物 01.AI | 01.AI / 零一万物 | 中国 | 15 | 12 | 客户解决方案与交付 3；工程与应用开发 3；平台、基础设施与数据 2；评测、测试与质量 1；产品与设计 1；商务、市场与合作 1；算法、研究与模型 1 | 产品与设计 3；客户解决方案与交付 3；工程与应用开发 3；评测、测试与质量 2；平台、基础设施与数据 2；商务、市场与合作 1；算法、研究与模型 1 | `TEAM-10C405784F542C45` |
| 2 | 360 Group / 360集团 | 360 Group / 360集团 | 中国 | 0 | 0 | — | — | `TEAM-A7AA49B633396CD0` |
| 3 | 360 纳米 AI 搜索 | 360 纳米 AI 搜索 | 中国 | 0 | 0 | — | — | `TEAM-5772D8F24BF41F24` |
| 4 | Agentica | Agentica | 中国 | 0 | 0 | — | — | `TEAM-9640633244925380` |
| 5 | AgentsChain / AppChain AI | AgentsChain / AppChain AI | 中国 | 0 | 0 | — | — | `TEAM-6CC639BAA998C799` |
| 6 | AgiBot / 智元机器人 | AgiBot / 智元机器人 | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-0D08DC9570146B68` |
| 7 | AgileX Robotics / 松灵机器人 / 深圳库犸科技有限公司 | AgileX Robotics / 松灵机器人 / 深圳库犸科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6D6BCD83D76997E5` |
| 8 | AHIVE / 星未来软件工作室 | AHIVE / 星未来软件工作室 | 中国 | 0 | 0 | — | — | `TEAM-EE01668275B7DA23` |
| 9 | AI for Education | AI for Education | 中国 | 0 | 0 | — | — | `TEAM-9F7C4FC4FCD8E2F0` |
| 10 | ai-flowx | ai-flowx | 中国 | 0 | 0 | — | — | `TEAM-24411D5E7661359F` |
| 11 | Ai-Thinker / 安信可科技 | Ai-Thinker / 安信可科技 | 中国 | 0 | 0 | — | — | `TEAM-EAB1006A03E46A91` |
| 12 | AI2 Robotics | AI2 Robotics | 中国 | 0 | 0 | — | — | `TEAM-56F9D90D66ECE70A` |
| 13 | Aix-DB | Aix-DB | 中国 | 0 | 0 | — | — | `TEAM-41DE945A19711321` |
| 14 | Alibaba / Qwen | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-191C6BA4851C0F80` |
| 15 | Alibaba Cloud | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-E93396C29114E0C1` |
| 16 | Alibaba Cloud / 阿里云 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-7EACDF71A5FB0EF1` |
| 17 | Alibaba Cloud Bailian Memory | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-4F3D62E4B08C19EA` |
| 18 | Alibaba Cloud Data Agent | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-05FC474D88D0048A` |
| 19 | Alibaba DAMO | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-2F587405E1CCE99E` |
| 20 | Alibaba DAMO / Healthcare AI | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-E2D79180E8F8E22E` |
| 21 | Alibaba Group | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-9B39C2D354110033` |
| 22 | Alibaba Group / 阿里巴巴集团 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-D451DFA1EE470739` |
| 23 | Alibaba International / Taobao | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-796B22C2D17CC606` |
| 24 | Alibaba Security | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-BFEBFE01C4C08D95` |
| 25 | DingTalk / 钉钉 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-1970815962963262` |
| 26 | Nacos / Alibaba | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-F166A36943FD76C6` |
| 27 | PolarDB for AI DB Agent | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-DE701396CBAAC08A` |
| 28 | Qoder CN / 通义灵码 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-5115B2D1287C72C5` |
| 29 | WuYing AgentBay / Alibaba Cloud | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-A9A2C2C0E73B8F8B` |
| 30 | 夸克 AI | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-DD5C461BEDFFAA61` |
| 31 | 夸克扫描王开放平台 / Quark Scan | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-F76CAB9E19C3D3AD` |
| 32 | 通义千问 / Qwen Chat | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-B945F3B5CE913F4B` |
| 33 | 钉钉 AI 助理 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-E9F6F5475E694BBD` |
| 34 | 钉钉智能招聘 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-4048048F6FDC7E97` |
| 35 | 阿里云 QoderWork CN | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-C8BF886A7DC266E3` |
| 36 | 阿里云函数计算 MCP/Agent | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-902A1EA3A4319F72` |
| 37 | 阿里云百炼 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-CA817346EC8588A0` |
| 38 | 阿里巴巴达摩院 | Alibaba Group / 阿里巴巴 | 中国 | 0 | 0 | — | — | `TEAM-9B106EA6E56D919F` |
| 39 | alinesno-infrastructure | alinesno-infrastructure | 中国 | 0 | 0 | — | — | `TEAM-0B792ACBE83E00D2` |
| 40 | Anker Innovations / 安克创新科技股份有限公司 | Anker Innovations / 安克创新科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3F1A3714FC833596` |
| 41 | Anspire | Anspire | 中国 | 0 | 0 | — | — | `TEAM-3C0C4F90451D0CC4` |
| 42 | agentUniverse | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-D07D0DBD405A2C1A` |
| 43 | Alipay AI Agent Payments | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-2E3029BF92B55974` |
| 44 | Ant Group / 蚂蚁集团 | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-4EB90FAA9CA3D00B` |
| 45 | AntV AI Visualization Team | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-66A49BA3F33C06E6` |
| 46 | InclusionAI / Ant Group | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-4E410FE4A196DA1C` |
| 47 | 蚂蚁数字科技 / Ant Digital | Ant Group / 蚂蚁集团 | 中国 | 0 | 0 | — | — | `TEAM-1CF0136C7EA345A0` |
| 48 | AnyEnv / Anycodes 在线编程 | AnyEnv / Anycodes 在线编程 | 中国 | 0 | 0 | — | — | `TEAM-016347B934A548A9` |
| 49 | AtomCode | AtomCode | 中国 | 0 | 0 | — | — | `TEAM-F6179FB3CFE501B5` |
| 50 | Baichuan Intelligence / 百川智能 | Baichuan Intelligence / 百川智能 | 中国 | 7 | 7 | 算法、研究与模型 2；工程与应用开发 2；安全、治理与合规 1；平台、基础设施与数据 1；其他或边界岗位 1 | 算法、研究与模型 2；工程与应用开发 2；安全、治理与合规 1；平台、基础设施与数据 1；其他或边界岗位 1 | `TEAM-9A82995FED33C9F6` |
| 51 | 百川智能 | Baichuan Intelligence / 百川智能 | 中国 | 0 | 0 | — | — | `TEAM-9A976AD93BA42646` |
| 52 | Baidu ACG Agent Product GTM | Baidu / 百度 | 中国 | 1 | 1 | 商务、市场与合作 1 | 商务、市场与合作 1 | `TEAM-8BDA57274A79792F` |
| 53 | Baidu ACG AI Coding Adoption | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-2C25CF2963AC1862` |
| 54 | Baidu Agent Data Security Platform | Baidu / 百度 | 中国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-15BF12C8BF2FB6DF` |
| 55 | Baidu AI-Native Monitoring Agent / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-F269807922697440` |
| 56 | Baidu Application Model R&D | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-11C07887C6CEBAF5` |
| 57 | Baidu Brand Advertising Agent Strategy / MEG | Baidu / 百度 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-E754EA4690AC9C55` |
| 58 | Baidu Cloud Agent Infra / ACG | Baidu / 百度 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-6A0E00EAAAE75C03` |
| 59 | Baidu Cloud GPU Agent Sandbox / ACG | Baidu / 百度 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-C9F20D62C0697CBA` |
| 60 | Baidu Commercial Agent Algorithms / MEG | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-2DE9913810F12289` |
| 61 | Baidu Commercial Agent Infrastructure / MEG | Baidu / 百度 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-054F4BEDCF023305` |
| 62 | Baidu Customer-Service QA Agent Adoption / PSIG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-BBD4396F87DDFB5D` |
| 63 | Baidu Data Intelligence Agent Platform / ACG | Baidu / 百度 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-8225105C76267E0B` |
| 64 | Baidu DuMate Agent Ecosystem / ACG | Baidu / 百度 | 中国 | 1 | 1 | 运营、项目与职能 1 | 运营、项目与职能 1 | `TEAM-524DF651E26D40C0` |
| 65 | Baidu DuMate Agent Evaluation / ACG | Baidu / 百度 | 中国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-3240F4EC74CE1776` |
| 66 | Baidu DuMate Agent Platform / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-5619B2FCC094E8EC` |
| 67 | Baidu DuMate Agent Runtime / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-2D0F6E9599DCFDF1` |
| 68 | Baidu DuMate Product Management / ACG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-2E62B4592CE8C811` |
| 69 | Baidu DuMate User And Growth Operations / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-67F2FB6DFB914EA5` |
| 70 | Baidu Ecommerce Agent Product / MEG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-7982881A9CB9AC8B` |
| 71 | Baidu Famou / ACG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-FBF5FCBD04B1E2E2` |
| 72 | Baidu Famou Agent Growth Operations / ACG | Baidu / 百度 | 中国 | 1 | 1 | 商务、市场与合作 1 | 商务、市场与合作 1 | `TEAM-E6A4A31E67C03679` |
| 73 | Baidu Foundation Model Agent Training | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-75AC184FEC976421` |
| 74 | Baidu Foundation Model Code Agent | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-4DE686E58481773D` |
| 75 | Baidu Health / MEG | Baidu / 百度 | 中国 | 4 | 4 | 产品与设计 4 | 产品与设计 4 | `TEAM-B795F5DA51F4B07B` |
| 76 | Baidu Health Agent Evaluation / MEG | Baidu / 百度 | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-EFF5143E64F1EEDA` |
| 77 | Baidu IDG Voice and Vehicle Agent | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-59E1B3A16A9B95E4` |
| 78 | Baidu Intelligent Operations LLM System / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-CF4918E4A9BD8B68` |
| 79 | Baidu Large-Model Application Platform / ACG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-F40C9A807DDCBDEB` |
| 80 | Baidu Maps Agent Adoption / IDG | Baidu / 百度 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-DCA0815D9A8F9DCD` |
| 81 | Baidu MeDo Global Agent Builder / ACG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-FF324995FE392D8A` |
| 82 | Baidu MEG Agent R&D | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-1A2CB9A86893FDB6` |
| 83 | Baidu MEG AI Engineering Effectiveness | Baidu / 百度 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-B2CA7E98FAD76BE3` |
| 84 | Baidu MEG Multimodal Agent Strategy | Baidu / 百度 | 中国 | 1 | 1 | 运营、项目与职能 1 | 运营、项目与职能 1 | `TEAM-0475B0D7709AB020` |
| 85 | Baidu Merchant Ecommerce Agent / MEG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-40369FCC158A1624` |
| 86 | Baidu Miaoda | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-D0978F617E5D6392` |
| 87 | Baidu Network Automation Agent / ACG | Baidu / 百度 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-38651D908AC7C254` |
| 88 | Baidu PSIG Agent Evaluation Platform | Baidu / 百度 | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-8BC21DDACE814C32` |
| 89 | Baidu PSIG Code Agent | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-4EE541AB0F3C016B` |
| 90 | Baidu PSIG Multi-Agent Architecture | Baidu / 百度 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-DCC51275C3E9AD90` |
| 91 | Baidu PSIG Office Agent | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-8DC1D0091D6FE69F` |
| 92 | Baidu Qianfan Agent And Tools Platform / ACG | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-98E028F340F44F34` |
| 93 | Baidu Qianfan AppBuilder | Baidu / 百度 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-18F4FF7B7EB405FB` |
| 94 | Baidu Qianfan Financial AI Solutions / ACG | Baidu / 百度 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-F7C26F3598F459E8` |
| 95 | Baidu Qianfan Next-Generation Agent Backend / ACG | Baidu / 百度 | 中国 | 1 | 0 | — | 平台、基础设施与数据 1 | `TEAM-DBA2F4C0774A2C76` |
| 96 | Baidu Sales Data Analysis Agent / MEG | Baidu / 百度 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-A68E972CCC6A1B37` |
| 97 | Baidu Search DuMate / ACG | Baidu / 百度 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-D2AFA6826EB5080B` |
| 98 | Baidu Security & Enterprise Efficiency Platform | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-13E09E0C7F2A9CF5` |
| 99 | Baidu Wenku and Netdisk AI Product / PSIG | Baidu / 百度 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-D3639010DB184751` |
| 100 | Baidu Wenxin Agent Strategy / MEG | Baidu / 百度 | 中国 | 1 | 1 | 运营、项目与职能 1 | 运营、项目与职能 1 | `TEAM-A29F39BB204AB49D` |
| 101 | Baidu Wenxin Assistant / Wenxin App | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-FD29AA594F2E8733` |
| 102 | Baidu Xiaodu Multimodal Agent Orchestration / Xiaodu | Baidu / 百度 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-1AAC2348EB72BB19` |
| 103 | 百度 AIDU | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-DBE946C652808DAE` |
| 104 | 百度千帆企业招聘智能助手 | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-90240373D892BBAD` |
| 105 | 百度文库 AI | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-96E85A5B99CCAAD9` |
| 106 | 百度文心快码 Comate | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-F83095E35FF6A918` |
| 107 | 百度智能云客悦 | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-28EB631E4BE09686` |
| 108 | 百度智能云曦灵数字人 | Baidu / 百度 | 中国 | 0 | 0 | — | — | `TEAM-574C7BBF02D1DD76` |
| 109 | Beike / 贝壳 | Beike / 贝壳 | 中国 | 0 | 0 | — | — | `TEAM-5D1A631E81D07B62` |
| 110 | BlueFocus Group / 蓝色光标集团 | BlueFocus Group / 蓝色光标集团 | 中国 | 2 | 1 | 工程与应用开发 1 | 工程与应用开发 1；其他或边界岗位 1 | `TEAM-A5F79437673A2BD4` |
| 111 | Bocha AI Search | Bocha | 中国 | 0 | 0 | — | — | `TEAM-87A1A9849239B358` |
| 112 | ArkClaw / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-A53BD0E7DFCC42B9` |
| 113 | ArkClaw / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-C832622E65D70B72` |
| 114 | ByteDance / 字节跳动 | ByteDance / 字节跳动 | 中国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-9AA5CB6DF0FA1643` |
| 115 | ByteDance China Transaction and Ads | ByteDance / 字节跳动 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-7564E9444C0F1857` |
| 116 | ByteDance Commercial AI | ByteDance / 字节跳动 | 中国 | 2 | 2 | 评测、测试与质量 1；算法、研究与模型 1 | 评测、测试与质量 1；算法、研究与模型 1 | `TEAM-CB53F4244D51BF58` |
| 117 | ByteDance Commercial Trust and Safety | ByteDance / 字节跳动 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-983D3899F2A96F84` |
| 118 | ByteDance Data Platform | ByteDance / 字节跳动 | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-D1D3AC9D30BD7879` |
| 119 | ByteDance Global Monetization Product and Technology | ByteDance / 字节跳动 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-243466EE951FC1BC` |
| 120 | ByteDance intelligent security | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-9A6BBE0C729BF47E` |
| 121 | ByteDance international e-commerce | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-B646A5D905A4F8F7` |
| 122 | ByteDance International E-commerce | ByteDance / 字节跳动 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-E0668FA0A346F26E` |
| 123 | ByteDance PDI Search / 字节跳动搜索 | ByteDance / 字节跳动 | 中国 | 2 | 2 | 工程与应用开发 2 | 工程与应用开发 2 | `TEAM-AE7A05A1E83E25FE` |
| 124 | ByteDance safety/risk-control | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-078D350AC1E55D2B` |
| 125 | ByteDance Security Engineering / Volcano Engine | ByteDance / 字节跳动 | 中国 | 1 | 1 | 安全、治理与合规 1 | 安全、治理与合规 1 | `TEAM-2DE1AED7007642C8` |
| 126 | ByteDance Seed | ByteDance / 字节跳动 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-E5A965BD23B008B3` |
| 127 | CloudWeGo / ByteDance | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-52A1D1C25E833577` |
| 128 | Coze / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-40BCA87BD0F0F82E` |
| 129 | Coze Studio | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-50F8255A5460C543` |
| 130 | Douyin Intelligent Creation / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-E4FA03F4862DABC5` |
| 131 | Douyin Open Platform / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-1A402FF2E79C3A32` |
| 132 | Feilian / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-623579AC45184FDA` |
| 133 | Feishu AI / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-58AB49A5EB551528` |
| 134 | OpenViking / Volcengine | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-88279BD90EC15F49` |
| 135 | SandboxFusion / ByteDance | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-2B3CB040FB8C15C9` |
| 136 | TikTok Privacy Safety / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-518315F1A2382017` |
| 137 | TikTok Short Video Recommendation / ByteDance | ByteDance / 字节跳动 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-0352035CA5889F6D` |
| 138 | TRAE | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-129E2CB6E1925C7B` |
| 139 | TRAE / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-A1322C05FE767DB7` |
| 140 | Volcengine Coze / HiAgent / TRAE | ByteDance / 字节跳动 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-E0997F09635690EA` |
| 141 | Volcengine Coze / TRAE | ByteDance / 字节跳动 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-3B326CB321144207` |
| 142 | 国际电商 / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-F3C7B1F5BBEF04B3` |
| 143 | 字节跳动 Data | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-CF56CBF2327EC9DE` |
| 144 | 字节跳动 Seed | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-60054AA9F7E08A77` |
| 145 | 字节跳动 安全与风控 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-CA95A661F4D60003` |
| 146 | 扣子 Coze | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-C38D02EA351D741C` |
| 147 | 扣子编程 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-C23D44E684BFDD2F` |
| 148 | 抖音 / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-F40DEF1499E775AD` |
| 149 | 火山引擎 / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-3E5C13A18A592EED` |
| 150 | 火山引擎 HiAgent | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-CAC22D01A38A0272` |
| 151 | 火山方舟 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-02DCFC7FE5ED320C` |
| 152 | 飞书 AI / 字节跳动 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-876CF740DEDE88B0` |
| 153 | 飞书 aily | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-DB2151F0338299B7` |
| 154 | 飞书 Aily 工作助手 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-1E3CB03E4E63B937` |
| 155 | 飞书 OpenClaw | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-28BC619C44F8261D` |
| 156 | 飞书招聘 AI 模板 | ByteDance / 字节跳动 | 中国 | 0 | 0 | — | — | `TEAM-633140B272D446AB` |
| 157 | Chengdu Aircraft Design and Research Institute / 成都飞机设计研究所 | Chengdu Aircraft Design and Research Institute / 成都飞机设计研究所 | 中国 | 0 | 0 | — | — | `TEAM-E2C0A021F5D540FD` |
| 158 | Chengdu RockBase Technology Co., Ltd. | Chengdu RockBase Technology Co., Ltd. | 中国 | 0 | 0 | — | — | `TEAM-0570EFB16C89960D` |
| 159 | China Aerospace Science and Industry Corporation / 中国航天科工集团 | China Aerospace Science and Industry Corporation / 中国航天科工集团 | 中国 | 0 | 0 | — | — | `TEAM-6E745D050E756DEE` |
| 160 | Shanghai Zhenhua Heavy Industries / 上海振华重工 | China Communications Construction Company / 中国交建 | 中国 | 0 | 0 | — | — | `TEAM-A3A15106B4F1D066` |
| 161 | 中金资本 | China International Capital Corporation / 中金公司 | 中国 | 0 | 0 | — | — | `TEAM-E9D14ED755DF5C13` |
| 162 | China Guangfa Bank / 广发银行 | China Life Insurance (Group) Company / 中国人寿保险（集团）公司 | 中国 | 0 | 0 | — | — | `TEAM-81C1CEE23B575988` |
| 163 | China Literature / 阅文集团 | China Literature / 阅文集团 | 中国 | 0 | 0 | — | — | `TEAM-10701887A10D0295` |
| 164 | China Merchants Fintech / 招商金科 | China Merchants Group / 招商局集团 | 中国 | 0 | 0 | — | — | `TEAM-1124AE101524F67B` |
| 165 | China Merchants Group / 招商局集团 | China Merchants Group / 招商局集团 | 中国 | 0 | 0 | — | — | `TEAM-4C1227E332C30402` |
| 166 | Lion Rock Laboratory / 狮子山实验室 | China Merchants Group / 招商局集团 | 中国 | 0 | 0 | — | — | `TEAM-461321604EE29F3C` |
| 167 | 招商交科 | China Merchants Group / 招商局集团 | 中国 | 0 | 0 | — | — | `TEAM-915C0BA216431001` |
| 168 | 中国电信人工智能研究院（TeleAI） | China Telecom | 中国 | 0 | 0 | — | — | `TEAM-111290911E5FFA1F` |
| 169 | China Unicom AI / 中国联通人工智能创新中心 | China Unicom | 中国 | 0 | 0 | — | — | `TEAM-09762ED30A6CD9C7` |
| 170 | 中国联通软件研究院 | China Unicom | 中国 | 0 | 0 | — | — | `TEAM-178FB0B19A6C0F11` |
| 171 | China Unicom Data Intelligence / 联通数据智能有限公司 | China Unicom Data Intelligence / 联通数据智能有限公司 | 中国 | 0 | 0 | — | — | `TEAM-7C813ECA7D98B383` |
| 172 | CAS-SIAT XinHai / 中国科学院深圳先进技术研究院心海团队 | Chinese Academy of Sciences | 中国 | 0 | 0 | — | — | `TEAM-2DF841E6C7F769A0` |
| 173 | Chinese Academy of Sciences Institute of Industrial AI / 中国科学院工业人工智能研究所 | Chinese Academy of Sciences | 中国 | 0 | 0 | — | — | `TEAM-EF3961CEC6861694` |
| 174 | Computer Network Information Center, Chinese Academy of Sciences / 中国科学院计算机网络信息中心 | Chinese Academy of Sciences | 中国 | 0 | 0 | — | — | `TEAM-91734E3B5EF88E75` |
| 175 | 中国科学院上海微系统与信息技术研究所仿生视觉系统实验室 | Chinese Academy of Sciences | 中国 | 1 | 0 | — | 平台、基础设施与数据 1 | `TEAM-D6F27F3B5244CE17` |
| 176 | CicadaRelay / Deconstruction Lab | CicadaRelay / Deconstruction Lab | 中国 | 0 | 0 | — | — | `TEAM-14D2CAF2F6CACB8D` |
| 177 | Claude Code Stock Deep Research Agent / liangdabiao | Claude Code Stock Deep Research Agent / liangdabiao | 中国 | 0 | 0 | — | — | `TEAM-8B304FCA5A9A0FF7` |
| 178 | CodeFuse | CodeFuse | 中国 | 0 | 0 | — | — | `TEAM-F1949EB0527B2B2E` |
| 179 | CodeGeeX | CodeGeeX | 中国 | 0 | 0 | — | — | `TEAM-E6B6B2849D32A912` |
| 180 | CrewBeeLab | CrewBeeLab | 中国 | 0 | 0 | — | — | `TEAM-159A9D8D1D67D5B6` |
| 181 | Ctrip Group / 携程集团 | Ctrip Group / 携程集团 | 中国 | 0 | 0 | — | — | `TEAM-D3FB2E395F2D9536` |
| 182 | CubeStudio / data-infra | CubeStudio / data-infra | 中国 | 0 | 0 | — | — | `TEAM-2AE137E6E7FEB241` |
| 183 | Customize Agent / Pan-jijian | Customize Agent / Pan-jijian | 中国 | 0 | 0 | — | — | `TEAM-370E181D98305D35` |
| 184 | CXMT / 长鑫存储技术有限公司 | CXMT / 长鑫存储技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A749E3AC9687ABB1` |
| 185 | DataFocus | DataFocus | 中国 | 0 | 0 | — | — | `TEAM-30E4338E242E2F2E` |
| 186 | Datawhale | Datawhale | 中国 | 0 | 0 | — | — | `TEAM-AD6B0AA331426EE8` |
| 187 | DeepArchi / deeparchi-ai | DeepArchi / deeparchi-ai | 中国 | 0 | 0 | — | — | `TEAM-6CD4703DA28985DD` |
| 188 | DeepSeek | DeepSeek / 深度求索 | 中国 | 0 | 0 | — | — | `TEAM-F85C895051A39D83` |
| 189 | DeepSeek / 杭州深度求索 | DeepSeek / 深度求索 | 中国 | 0 | 0 | — | — | `TEAM-3A8DB7932D55A6AB` |
| 190 | MetaGPT / DeepWisdom / FoundationAgents | DeepWisdom / FoundationAgents | 中国 | 0 | 0 | — | — | `TEAM-E0DFA34077B30B25` |
| 191 | Desay SV / 惠州市德赛西威汽车电子股份有限公司 | Desay SV / 惠州市德赛西威汽车电子股份有限公司 | 中国 | 5 | 4 | 平台、基础设施与数据 2；客户解决方案与交付 1；算法、研究与模型 1 | 平台、基础设施与数据 2；客户解决方案与交付 1；算法、研究与模型 1；其他或边界岗位 1 | `TEAM-7850261E00ECC2F3` |
| 192 | DIDA-AI / Dida Hotel MCP | Didatravel International Limited | 中国 | 0 | 0 | — | — | `TEAM-78B52D288FEB35B2` |
| 193 | EasyClaw | DOCUAGILE PTE. LTD. | 中国 | 0 | 0 | — | — | `TEAM-DC0F77B8396DA1BA` |
| 194 | Dongchedi / 懂车帝 | Dongchedi / 懂车帝 | 中国 | 1 | 1 | 其他或边界岗位 1 | 其他或边界岗位 1 | `TEAM-3ADD1B84A0009420` |
| 195 | Du Xiaoman / 度小满 | Du Xiaoman / 度小满 | 中国 | 1 | 1 | 其他或边界岗位 1 | 其他或边界岗位 1 | `TEAM-0498D7679F649898` |
| 196 | 翼鸥集团 / EEO Group | EEO Group | 中国 | 0 | 0 | — | — | `TEAM-210D3E9FFC8FF07F` |
| 197 | EvoFlow / EvoVex AI | Evovex AI | 中国 | 0 | 0 | — | — | `TEAM-629A4F46F1B27A91` |
| 198 | e签宝 AI 合同 | e签宝 AI 合同 | 中国 | 0 | 0 | — | — | `TEAM-AD77B114181B65D0` |
| 199 | Fanruan / 帆软 | Fanruan / 帆软 | 中国 | 0 | 0 | — | — | `TEAM-621A3D417822CADF` |
| 200 | 帆软 FineChatBI | Fanruan / 帆软 | 中国 | 0 | 0 | — | — | `TEAM-CD2B2B7E8D1DACD3` |
| 201 | FastGPT | FastGPT | 中国 | 0 | 0 | — | — | `TEAM-D38FA220CBBC0894` |
| 202 | Fastlane | Fastlane | 中国 | 0 | 0 | — | — | `TEAM-99818182A816A9E1` |
| 203 | Fellou | Fellou | 中国 | 0 | 0 | — | — | `TEAM-E1080118709F5BFD` |
| 204 | fisher-admin / FisherQuant | fisher-admin / FisherQuant | 中国 | 0 | 0 | — | — | `TEAM-2C552D9E7E7C79A9` |
| 205 | MaxKB | FIT2CLOUD 飞致云 | 中国 | 0 | 0 | — | — | `TEAM-B9A50F8996603726` |
| 206 | Fitten Code | Fitten Code | 中国 | 0 | 0 | — | — | `TEAM-A83272728AA0978B` |
| 207 | Flowith | Flowith | 中国 | 0 | 0 | — | — | `TEAM-0018D46E3A1C45D0` |
| 208 | Fosun Pharma / 复星医药 | Fosun Pharma | 中国 | 2 | 0 | — | 评测、测试与质量 1；产品与设计 1 | `TEAM-DF858E57CF922BC2` |
| 209 | FOTILE / 方太集团 | FOTILE / 方太集团 | 中国 | 0 | 0 | — | — | `TEAM-4C3691E77F787BCD` |
| 210 | OpenManus / FoundationAgents | FoundationAgents / MetaGPT contributor team | 中国 | 0 | 0 | — | — | `TEAM-4BA1122E78A5E701` |
| 211 | Galaxea AI | Galaxea AI | 中国 | 0 | 0 | — | — | `TEAM-3A266173EBAE2B01` |
| 212 | GeminiLight / MindOS | GeminiLight / MindOS | 中国 | 0 | 0 | — | — | `TEAM-E48AF22B87F5DD2E` |
| 213 | GienTech / 中电金信 | GienTech / 中电金信 | 中国 | 0 | 0 | — | — | `TEAM-D4125845A7A4E50A` |
| 214 | GraphFlow / Roarpeng | GraphFlow / Roarpeng | 中国 | 0 | 0 | — | — | `TEAM-FEACA6372AC55E46` |
| 215 | Hisense | Hisense | 中国 | 0 | 0 | — | — | `TEAM-B5EA6FB7C97707CE` |
| 216 | Home Assistant China (unofficial) | Home Assistant China (unofficial) | 中国 | 0 | 0 | — | — | `TEAM-D43F9F98C20C1896` |
| 217 | Huawei | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-B0D2AD7D55FEA28A` |
| 218 | 仓颉编程语言 / Cangjie Team | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-66249E445BCC8582` |
| 219 | 华为云 | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-D077810FC68F0C28` |
| 220 | 华为云 Agent 开发平台 | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-FE2A0FD55B772469` |
| 221 | 华为云 AgentArts | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-1F1B888CA8028E8F` |
| 222 | 华为云工业智能体 | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-B196D40752A0A4C6` |
| 223 | 华为云码道 CodeArts | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-9AB374B5E2E6E402` |
| 224 | 星网信通 / 华为央国企AI智能体联合方案 | Huawei / 华为 | 中国 | 0 | 0 | — | — | `TEAM-9EEBB6E6DD324D53` |
| 225 | iCourt Alpha | iCourt Alpha | 中国 | 0 | 0 | — | — | `TEAM-9CAEB7F6601FEC69` |
| 226 | IDEA Digital Economy Institute / IDEA数字经济研究院 | IDEA Digital Economy Institute / IDEA数字经济研究院 | 中国 | 0 | 0 | — | — | `TEAM-BF575E05DA9490C2` |
| 227 | IdeaSeek | IdeaSeek | 中国 | 0 | 0 | — | — | `TEAM-340E58CA55E8B36F` |
| 228 | iFlyCode | iFlyCode | 中国 | 0 | 0 | — | — | `TEAM-D872FBA37029D858` |
| 229 | 科大讯飞 / iFlytek | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-889A367F8936B71F` |
| 230 | 讯飞 AstronClaw | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-0312DCA1B4A62D88` |
| 231 | 讯飞听见 AI | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-09DF1BD40239D62A` |
| 232 | 讯飞星火 | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-FF0F8ACEB1E9FA95` |
| 233 | 讯飞星辰 Agent 平台 | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-D9895EA81560B58A` |
| 234 | 讯飞星辰智能 RPA | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-BCCCBE66994EB6EA` |
| 235 | 讯飞晓医 | iFlytek / 科大讯飞 | 中国 | 0 | 0 | — | — | `TEAM-7D9E58EDA2C454C8` |
| 236 | iMaoKe / i贸客 | iMaoKe / i贸客 | 中国 | 0 | 0 | — | — | `TEAM-67DA03E0C9DE4861` |
| 237 | imcp / imcp.pro | imcp / imcp.pro | 中国 | 0 | 0 | — | — | `TEAM-FC286DBF02C5C96E` |
| 238 | Inspire Group / 英湃数字科技 | Inspire Group / 英湃数字科技 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-D2C49B2C1B824800` |
| 239 | itongban ChatBI | itongban | 中国 | 0 | 0 | — | — | `TEAM-5CA9969A518DA06B` |
| 240 | iWhaleCloud / 浩鲸科技 | iWhaleCloud / 浩鲸科技 | 中国 | 1 | 0 | — | 客户解决方案与交付 1 | `TEAM-0266AED0EA91186B` |
| 241 | BOE / 京东方 | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-6F48E6D594A605A0` |
| 242 | JD Group | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-86AE0137DCDBEECD` |
| 243 | JD Health | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-A6FDC52687472CD4` |
| 244 | JD Technology | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-D436BE460C446641` |
| 245 | JD.com | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-7A3F4165A4757DF3` |
| 246 | 京东言犀 | JD.com / 京东 | 中国 | 0 | 0 | — | — | `TEAM-5D2FCBFA82A92F7A` |
| 247 | K2 Lab / Moras | K2 Lab / Moras | 中国 | 0 | 0 | — | — | `TEAM-9B74B0575C36621A` |
| 248 | KAON / FlowGPT | KAON / FlowGPT | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-3B252E3A7BFEE6EC` |
| 249 | WPS AI / WPS 灵犀 | Kingsoft Office / 金山办公 | 中国 | 0 | 0 | — | — | `TEAM-7A58272A7BB0DA2E` |
| 250 | 金山办公 AI 简历助手 | Kingsoft Office / 金山办公 | 中国 | 0 | 0 | — | — | `TEAM-1FF95733B8D6027F` |
| 251 | KittLabs / KittLabsAI | KittLabs / KittLabsAI | 中国 | 0 | 0 | — | — | `TEAM-0C02C7F2DE47823C` |
| 252 | Kuaishou | Kuaishou / 快手 | 中国 | 0 | 0 | — | — | `TEAM-7CBEFC2F5E1FCB9A` |
| 253 | Kuehne+Nagel / 德迅 | Kuehne+Nagel / 德迅 | 中国 | 0 | 0 | — | — | `TEAM-FC7881FCC95461D7` |
| 254 | Kyligence Zen | Kyligence Zen | 中国 | 0 | 0 | — | — | `TEAM-C975E37C673A64A7` |
| 255 | Laiye / 来也科技 | Laiye / 来也科技 | 中国 | 0 | 0 | — | — | `TEAM-E89F3F39C8602535` |
| 256 | Dify / LangGenius | LangGenius | 中国 | 0 | 0 | — | — | `TEAM-168FBE3E61DABA2A` |
| 257 | Leapmotor / 浙江零跑科技股份有限公司 | Leapmotor / 浙江零跑科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-0EB69C82191FFC33` |
| 258 | Li Auto / 理想汽车 | Li Auto / 理想汽车 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-E7EA10B1C04ACE7D` |
| 259 | Lulula | Lulula | 中国 | 0 | 0 | — | — | `TEAM-B4698E64FF2A4B6B` |
| 260 | Maimai / 脉脉 | Maimai / 脉脉 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-DCA46671BE51CE1A` |
| 261 | MAREF / maref-org | MAREF / maref-org | 中国 | 0 | 0 | — | — | `TEAM-07A1D6FC12E20F1F` |
| 262 | Mashang Consumer Finance / 马上消费 | Mashang Consumer Finance / 马上消费 | 中国 | 3 | 3 | 算法、研究与模型 3 | 算法、研究与模型 3 | `TEAM-0DBF640EC0E0A597` |
| 263 | McDonald's China / 麦当劳中国 | McDonald's | 中国 | 0 | 0 | — | — | `TEAM-B2B3D6614004FD85` |
| 264 | MEACHEAL Research Center / MEACHEAL 米茜尔 | MEACHEAL Research Center / MEACHEAL 米茜尔 | 中国 | 0 | 0 | — | — | `TEAM-45951396164911FC` |
| 265 | MEACHEAL Research Center / MRC Data | MEACHEAL Research Center / MRC Data | 中国 | 0 | 0 | — | — | `TEAM-633C727B2BFA1D36` |
| 266 | Meitu / 美图 | Meitu / 美图 | 中国 | 0 | 0 | — | — | `TEAM-26CA945764BFA751` |
| 267 | Meituan / 美团 | Meituan / 美团 | 中国 | 0 | 0 | — | — | `TEAM-72B0D4802A76E095` |
| 268 | Meituan Core Local Commerce | Meituan / 美团 | 中国 | 0 | 0 | — | — | `TEAM-65C206EB78C72700` |
| 269 | Meituan Platform | Meituan / 美团 | 中国 | 0 | 0 | — | — | `TEAM-810E49C2F995B9E7` |
| 270 | Meituan Restaurant SaaS Platform | Meituan / 美团 | 中国 | 0 | 0 | — | — | `TEAM-4AD3673324FD655C` |
| 271 | MemOS / OpenMem (MemTensor org) | MemTensor | 中国 | 0 | 0 | — | — | `TEAM-8C38CA2C127A52FA` |
| 272 | MetaGO Lightyear / metago-ai | MetaGO Lightyear / metago-ai | 中国 | 0 | 0 | — | — | `TEAM-6DF5132589A31793` |
| 273 | MetaHub / 元枢科技 | MetaHub / 元枢科技 | 中国 | 0 | 0 | — | — | `TEAM-DDF996F84EBF5E8C` |
| 274 | Mindverse | Mindverse | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-BBC84DF3FB5A2EBB` |
| 275 | MiniMax | MiniMax | 中国 | 28 | 26 | 平台、基础设施与数据 7；工程与应用开发 7；评测、测试与质量 4；产品与设计 3；客户解决方案与交付 2；安全、治理与合规 1；算法、研究与模型 1；其他或边界岗位 1 | 平台、基础设施与数据 7；工程与应用开发 7；评测、测试与质量 4；产品与设计 4；客户解决方案与交付 3；安全、治理与合规 1；算法、研究与模型 1；其他或边界岗位 1 | `TEAM-CA43507C9674341D` |
| 276 | MiniMax Agent | MiniMax | 中国 | 0 | 0 | — | — | `TEAM-9B5332F90EC1D267` |
| 277 | MiniMax Code | MiniMax | 中国 | 0 | 0 | — | — | `TEAM-D7F9250FE721EE0E` |
| 278 | Mininglamp Technology / 明略科技 | Mininglamp Technology / 明略科技 | 中国 | 0 | 0 | — | — | `TEAM-37BCBC1B0B905942` |
| 279 | ModelBest / 面壁智能 | ModelBest / 面壁智能 | 中国 | 1 | 1 | 其他或边界岗位 1 | 其他或边界岗位 1 | `TEAM-CCF3F15BB0083947` |
| 280 | ModelScope / 魔搭 | ModelScope / 魔搭 | 中国 | 0 | 0 | — | — | `TEAM-9A9B9F80FDC3D972` |
| 281 | ModelScope AgentScope | ModelScope AgentScope | 中国 | 0 | 0 | — | — | `TEAM-BCCDC5B2CAE95059` |
| 282 | Moka / 北京希瑞亚斯科技有限公司 | Moka / 北京希瑞亚斯科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-D786573431C98A46` |
| 283 | Moka AI | Moka AI | 中国 | 0 | 0 | — | — | `TEAM-B286549211894671` |
| 284 | Momenta | Momenta | 中国 | 1 | 1 | 其他或边界岗位 1 | 其他或边界岗位 1 | `TEAM-6DAFFA2656E93E53` |
| 285 | Kimi / Moonshot AI | Moonshot AI / 月之暗面 | 中国 | 0 | 0 | — | — | `TEAM-61987EE17F2DAC44` |
| 286 | Kimi Code | Moonshot AI / 月之暗面 | 中国 | 0 | 0 | — | — | `TEAM-4F76BC3A43227B02` |
| 287 | Moonshot AI / Kimi | Moonshot AI / 月之暗面 | 中国 | 0 | 0 | — | — | `TEAM-CC6AC36EAB07A189` |
| 288 | MorphixAI / Morphicai | MorphixAI / Morphicai | 中国 | 0 | 0 | — | — | `TEAM-F523096B29FBF0F8` |
| 289 | Naoli / 脑利 | Naoli / 脑利 | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-69CBFDD7714FF326` |
| 290 | Nebutra Intelligence / 无锡 Nebutra Intelligence | Nebutra Intelligence / 无锡 Nebutra Intelligence | 中国 | 0 | 0 | — | — | `TEAM-0DE709FC4D1BDB56` |
| 291 | 网易严选 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-25AEFA73B96ED7B5` |
| 292 | 网易云音乐 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-CEFC0248E1AE2590` |
| 293 | 网易伏羲 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-45A5F8E063367E82` |
| 294 | 网易元气 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-0BBB7BC4116E2868` |
| 295 | 网易智企 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-9BA15AB61E1CC39D` |
| 296 | 网易有道 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-1A89CAC1C76B2604` |
| 297 | 网易有道 子曰/AI 助手 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-7A99751BEADDA0F7` |
| 298 | 网易游戏（互娱） | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-8C20383F53C1995E` |
| 299 | 网易游戏（雷火） | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-44BFAC78E2D4A990` |
| 300 | 网易职能 | NetEase / 网易 | 中国 | 0 | 0 | — | — | `TEAM-1C19D795AC11481E` |
| 301 | Zhi Ao Tong / 新紫光前沿院 / 智遨通（天津）信息技术有限公司 | New Unigroup / 新紫光 | 中国 | 3 | 2 | 评测、测试与质量 1；平台、基础设施与数据 1 | 评测、测试与质量 1；算法、研究与模型 1；平台、基础设施与数据 1 | `TEAM-3BF3BD3EB8450A34` |
| 302 | NIO / 蔚来 | NIO / 蔚来 | 中国 | 82 | 54 | 算法、研究与模型 15；产品与设计 14；工程与应用开发 12；客户解决方案与交付 7；安全、治理与合规 4；平台、基础设施与数据 1；其他或边界岗位 1 | 算法、研究与模型 23；产品与设计 19；工程与应用开发 19；客户解决方案与交付 9；安全、治理与合规 8；评测、测试与质量 2；平台、基础设施与数据 1；其他或边界岗位 1 | `TEAM-C4A36E8C44F675DF` |
| 303 | NIO GeniTech / Shenji | NIO / 蔚来 | 中国 | 0 | 0 | — | — | `TEAM-32ABF1B2861BC2D7` |
| 304 | Nuwax AI Agent Platform | Nuwax AI Agent Platform | 中国 | 0 | 0 | — | — | `TEAM-12CCEB8AABCC218A` |
| 305 | PowerMem / OceanBase | OceanBase, Inc. | 中国 | 0 | 0 | — | — | `TEAM-E8ED8B113AE8A6EE` |
| 306 | Oinone（数式） | Oinone（数式） | 中国 | 0 | 0 | — | — | `TEAM-1CDAAD4DBD466281` |
| 307 | openEuler / SIG-Intelligence | OpenAtom Foundation / 开放原子开源基金会 | 中国 | 0 | 0 | — | — | `TEAM-974B50AEDBFBD27C` |
| 308 | OpenCSG / 北京开放传神科技有限公司 | OpenCSG / 北京开放传神科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-98104ED059611AEE` |
| 309 | JiuwenSwarm / openJiuwen | openJiuwen community | 中国 | 0 | 0 | — | — | `TEAM-C4E876DE57987A92` |
| 310 | OPPO | OPPO | 中国 | 0 | 0 | — | — | `TEAM-79B064F0669BC157` |
| 311 | OrcaKIT AI / OrcaAgent-AI | OrcaKIT AI / OrcaAgent-AI | 中国 | 0 | 0 | — | — | `TEAM-D1D079EB373B98AA` |
| 312 | PartMe AI | PartMe AI | 中国 | 0 | 0 | — | — | `TEAM-39FC57014C491C6B` |
| 313 | PATEO | PATEO | 中国 | 0 | 0 | — | — | `TEAM-19DC42A80EC63948` |
| 314 | PaXini | PaXini | 中国 | 0 | 0 | — | — | `TEAM-0C8E27D2FE006073` |
| 315 | PDD / 拼多多集团 | PDD / 拼多多集团 | 中国 | 0 | 0 | — | — | `TEAM-38F8A66808D13BDF` |
| 316 | Peking University Health Science Center / 北京大学医学部 | Peking University | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-651FF195CC75E748` |
| 317 | Peking University Institute of Artificial Intelligence / 北京大学人工智能研究院 | Peking University | 中国 | 0 | 0 | — | — | `TEAM-F6ECBD35F7D7B825` |
| 318 | Petnest AI / 宠巢智能 | Petnest AI / 宠巢智能 | 中国 | 0 | 0 | — | — | `TEAM-CFEC81FB7E4787E4` |
| 319 | PieTeams | PieTeams | 中国 | 0 | 0 | — | — | `TEAM-BCBF8B15B9751FEE` |
| 320 | PlatonAI | PlatonAI | 中国 | 0 | 0 | — | — | `TEAM-4BE5B07C28C8C38F` |
| 321 | POIZON / 得物App | POIZON / 得物App | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-FD58D9C534FD9049` |
| 322 | ProcessOn AI | ProcessOn AI | 中国 | 0 | 0 | — | — | `TEAM-E84AAE594B1B4F51` |
| 323 | Proscenic / 普森斯 | Proscenic / 普森斯 | 中国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-7BE2D3EFBFF43119` |
| 324 | QCraft / 轻舟智航 | QCraft / 轻舟智航 | 中国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3450E800065CFFF6` |
| 325 | Qianzhi Tech / 千帜科技 (UNICUS) | Qianzhi Tech / 千帜科技 (UNICUS) | 中国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-2B36DD27E3DB585E` |
| 326 | Qihe Agent / 启合涌现 | Qihe Agent / 启合涌现 | 中国 | 0 | 0 | — | — | `TEAM-75839F3297A2092B` |
| 327 | Ragent AI / 拿个offer | Ragent AI / 拿个offer | 中国 | 0 | 0 | — | — | `TEAM-E095E995A1495A62` |
| 328 | RAGFlow / InfiniFlow | RAGFlow / InfiniFlow | 中国 | 0 | 0 | — | — | `TEAM-E3C75721B603EB62` |
| 329 | RayNeo / 雷鸟创新 | RayNeo / 雷鸟创新 | 中国 | 1 | 0 | — | 平台、基础设施与数据 1 | `TEAM-7B6FCEC8DE70DFC9` |
| 330 | Raytone.AI / Raytone AI Labs | Raytone.AI / Raytone AI Labs | 中国 | 0 | 0 | — | — | `TEAM-DB1D6740752136D1` |
| 331 | ReachAI / EnterpriseAgentFramework | ReachAI / EnterpriseAgentFramework | 中国 | 0 | 0 | — | — | `TEAM-F3140568D0AE1511` |
| 332 | Rokid | Rokid | 中国 | 0 | 0 | — | — | `TEAM-41A0D32543E782E5` |
| 333 | Ronbay Group / 容百集团 | Ronbay Group / 容百集团 | 中国 | 0 | 0 | — | — | `TEAM-7E5ACDA3494D02E7` |
| 334 | RubikSQL | RubikSQL | 中国 | 0 | 0 | — | — | `TEAM-0556AF919CD35FB6` |
| 335 | RuoYi AI | RuoYi AI | 中国 | 0 | 0 | — | — | `TEAM-5DEA320E52BB70DD` |
| 336 | 商汤商量 | SenseTime / 商汤 | 中国 | 0 | 0 | — | — | `TEAM-126EEAC6919E85DB` |
| 337 | 商汤日日新 / SenseNova | SenseTime / 商汤 | 中国 | 0 | 0 | — | — | `TEAM-DFF2952D6CCD5D7B` |
| 338 | 商汤科技 / SenseTime | SenseTime / 商汤 | 中国 | 9 | 8 | 算法、研究与模型 3；平台、基础设施与数据 2；评测、测试与质量 1；客户解决方案与交付 1；工程与应用开发 1 | 算法、研究与模型 3；客户解决方案与交付 2；平台、基础设施与数据 2；评测、测试与质量 1；工程与应用开发 1 | `TEAM-BBB7B8A75E61B65F` |
| 339 | Sevoniva | Sevoniva | 中国 | 0 | 0 | — | — | `TEAM-65450838C880196A` |
| 340 | Shanghai HiQ Smart Data Technology Co., Ltd. / 上海海科智慧数据科技有限公司 | Shanghai HiQ Smart Data Technology Co., Ltd. / 上海海科智慧数据科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E276779E83505972` |
| 341 | OMNILab / 上海交通大学大数据智能实验室 | Shanghai Jiao Tong University | 中国 | 0 | 0 | — | — | `TEAM-F012199CDFDEF59B` |
| 342 | Shanghai Sudu Technology / 上海苏度科技有限公司 | Shanghai Sudu Technology / 上海苏度科技有限公司 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-B1DD3CF89771A2BE` |
| 343 | ShellWard / jnMetaCode | ShellWard / jnMetaCode | 中国 | 0 | 0 | — | — | `TEAM-01F3AE483E07BE5C` |
| 344 | ShengShu Technology / 生数科技 | ShengShu Technology / 生数科技 | 中国 | 1 | 0 | — | 产品与设计 1 | `TEAM-1BFC0DEA147F89D2` |
| 345 | Shenzhen Institute of Artificial Intelligence and Robotics for Society / AIRS | Shenzhen Institute of Artificial Intelligence and Robotics for Society / AIRS | 中国 | 0 | 0 | — | — | `TEAM-14993C2985B76E5D` |
| 346 | SigmaZ | SigmaZ | 中国 | 0 | 0 | — | — | `TEAM-9BF0BFFE22DF36FE` |
| 347 | SIMIAIOS / 龙虾手机 | SIMIAIOS / 龙虾手机 | 中国 | 0 | 0 | — | — | `TEAM-0678B1CFC492202E` |
| 348 | SingTown | SingTown | 中国 | 0 | 0 | — | — | `TEAM-423AD7842CECB7F1` |
| 349 | Snow CLI | Snow CLI | 中国 | 0 | 0 | — | — | `TEAM-6CD3543FDD33C9DE` |
| 350 | Spirit AI | Spirit AI | 中国 | 0 | 0 | — | — | `TEAM-77350E818752C405` |
| 351 | sre-agents | sre-agents | 中国 | 0 | 0 | — | — | `TEAM-84A243856FE4450E` |
| 352 | StellarLink / 重庆星纬智联科技 | StellarLink / 重庆星纬智联科技 | 中国 | 0 | 0 | — | — | `TEAM-A9FAEBA09C17CCAC` |
| 353 | StepFun / 阶跃星辰 | StepFun / 阶跃星辰 | 中国 | 0 | 0 | — | — | `TEAM-A5869B4A43BCBE75` |
| 354 | 阶跃星辰 / StepFun | StepFun / 阶跃星辰 | 中国 | 0 | 0 | — | — | `TEAM-D7991F7B1A510C76` |
| 355 | 阶跃星辰开放平台 | StepFun / 阶跃星辰 | 中国 | 0 | 0 | — | — | `TEAM-6DDDB97F9B609D9C` |
| 356 | superun (知擎信息) | superun (知擎信息) | 中国 | 0 | 0 | — | — | `TEAM-598F0D64CF58CAB8` |
| 357 | SuperX | SuperX | 中国 | 0 | 0 | — | — | `TEAM-A5AB6D5F7AB588DD` |
| 358 | Talkdesk / 拓德（武汉）软件有限公司 | Talkdesk / 拓德（武汉）软件有限公司 | 中国 | 0 | 0 | — | — | `TEAM-98310F88B6CB1A7B` |
| 359 | CubeSandbox / Tencent Cloud | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-6371A11D6FC6C4C8` |
| 360 | Tencent | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-2678CDD785533E86` |
| 361 | Tencent ClawPet | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-055002F8FDC27AE7` |
| 362 | Tencent Cloud | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-4462DBD28E518F15` |
| 363 | Tencent RTC Conversational AI | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-9856E741B89A5F71` |
| 364 | Tencent tRPC | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-12B9E5B0826E555F` |
| 365 | Tencent Yuanbao / 腾讯元宝 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-EAEF736C020A8045` |
| 366 | 企业微信 / WeCom | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-899D678B44617C61` |
| 367 | 企业微信 AI | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-970515F10808644A` |
| 368 | 腾讯 TEG | Tencent / 腾讯 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-6F09D0ED97DA3DF0` |
| 369 | 腾讯 智能助手 | Tencent / 腾讯 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-7B152602A45A8F6F` |
| 370 | 腾讯ima.copilot | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-78351D1E41A3DBCF` |
| 371 | 腾讯云 CodeBuddy | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-325D9C4B84369245` |
| 372 | 腾讯云开发 CloudBase | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-C5962C1E55FD3E86` |
| 373 | 腾讯云智能体平台 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-2F1D4F8BBA50C3EE` |
| 374 | 腾讯元器 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-A8619FB08AA15814` |
| 375 | 腾讯元器公众号智能体 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-1B15B86FD4755A90` |
| 376 | 腾讯文档 AI | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-36D926BADEDA50AC` |
| 377 | 腾讯混元助手 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-10661C43950F0E75` |
| 378 | 腾讯觅影 | Tencent / 腾讯 | 中国 | 0 | 0 | — | — | `TEAM-F1DD7AB2B7FE32D2` |
| 379 | Teshi.org / teshi-org | Teshi.org / teshi-org | 中国 | 0 | 0 | — | — | `TEAM-294C307AD434017E` |
| 380 | THU-MAIC / OpenMAIC | THU-MAIC / OpenMAIC | 中国 | 0 | 0 | — | — | `TEAM-934C088ED0410D82` |
| 381 | ThunderSoft | ThunderSoft | 中国 | 0 | 0 | — | — | `TEAM-2D372FB897CDB5B3` |
| 382 | Tongji EDA Lab and CUHK | Tongji EDA Lab and CUHK | 中国 | 0 | 0 | — | — | `TEAM-33CC9FBECAF85509` |
| 383 | TradingAgents-AShare / KylinMountain | TradingAgents-AShare / KylinMountain | 中国 | 0 | 0 | — | — | `TEAM-76025FDE6E2DAD6A` |
| 384 | TradingAgents-CN | TradingAgents-CN | 中国 | 0 | 0 | — | — | `TEAM-744180B19458A1E8` |
| 385 | Udesk / 沃丰科技 | Udesk / 沃丰科技 | 中国 | 0 | 0 | — | — | `TEAM-A91AF878F621FEAE` |
| 386 | VCPToolBox / VCP-OS | VCPToolBox / VCP-OS | 中国 | 0 | 0 | — | — | `TEAM-B3C0BA9991084746` |
| 387 | VTJ.PRO | VTJ.PRO | 中国 | 0 | 0 | — | — | `TEAM-6A501A615F1DA95D` |
| 388 | WePie / 微派网络 | WePie / 微派网络 | 中国 | 0 | 0 | — | — | `TEAM-52B6ADB2FA81C10C` |
| 389 | WindClaw | WindClaw | 中国 | 0 | 0 | — | — | `TEAM-BE0A7D480C30B552` |
| 390 | Wuhan SharkOrb Tech Co., Ltd. | Wuhan SharkOrb Tech Co., Ltd. | 中国 | 0 | 0 | — | — | `TEAM-1391423990044995` |
| 391 | X Square Robot / 自变量机器人科技（深圳）有限公司 | X Square Robot / 自变量机器人科技（深圳）有限公司 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-161BFB34D375D284` |
| 392 | XD Inc. | XD Inc. | 中国 | 0 | 0 | — | — | `TEAM-64B81F5332CC2E78` |
| 393 | Xiaohongshu | Xiaohongshu / 小红书 | 中国 | 0 | 0 | — | — | `TEAM-B8A776987CFE3B07` |
| 394 | Xiaohongshu / RedNote | Xiaohongshu / 小红书 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-5F1327605A1E5535` |
| 395 | 小红书 | Xiaohongshu / 小红书 | 中国 | 0 | 0 | — | — | `TEAM-76D29010587E10E4` |
| 396 | Xiaomi / MiMo | Xiaomi / 小米 | 中国 | 0 | 0 | — | — | `TEAM-9B7E64A2898EAACB` |
| 397 | Xiaomi / 小米 | Xiaomi / 小米 | 中国 | 2 | 0 | — | 评测、测试与质量 2 | `TEAM-098C48CA29B7C627` |
| 398 | Xiaomi Auto / 小米汽车 | Xiaomi / 小米 | 中国 | 0 | 0 | — | — | `TEAM-0836C08769F5BFE8` |
| 399 | XPeng / 小鹏汽车 | XPeng / 小鹏汽车 | 中国 | 106 | 39 | 工程与应用开发 13；算法、研究与模型 11；客户解决方案与交付 9；产品与设计 5；评测、测试与质量 1 | 算法、研究与模型 34；工程与应用开发 25；客户解决方案与交付 18；产品与设计 15；评测、测试与质量 11；安全、治理与合规 3 | `TEAM-729BC98A1D8C89EA` |
| 400 | Yidian Intelligent Computing / 仪电智算 | Yidian Intelligent Computing / 仪电智算 | 中国 | 0 | 0 | — | — | `TEAM-107AEB3CC67BD0A8` |
| 401 | 用友 / BIP企业AI | Yonyou / 用友 | 中国 | 0 | 0 | — | — | `TEAM-58938B0966B271B0` |
| 402 | 用友 / Yonyou | Yonyou / 用友 | 中国 | 0 | 0 | — | — | `TEAM-8813467FBE5FEC90` |
| 403 | 用友 YonYou | Yonyou / 用友 | 中国 | 0 | 0 | — | — | `TEAM-C2DC136E3CBF9CDB` |
| 404 | 用友YonSuite / 智能体市场 | Yonyou / 用友 | 中国 | 0 | 0 | — | — | `TEAM-B07846946D0B38C7` |
| 405 | Z.ai | Z.ai | 中国 | 0 | 0 | — | — | `TEAM-C7A729DC0F6E31CD` |
| 406 | Zeroclave | Zeroclave | 中国 | 0 | 0 | — | — | `TEAM-C02F9BF97303D805` |
| 407 | ZetaZeroHub / ζ0Hub | ZetaZeroHub / ζ0Hub | 中国 | 0 | 0 | — | — | `TEAM-A894FAB41C875DE0` |
| 408 | ZJUNLP Knowledge Engine Lab | Zhejiang University | 中国 | 0 | 0 | — | — | `TEAM-A27AAE0E0AAD864A` |
| 409 | Zhipu AI / 智谱 | Zhipu AI / 智谱 | 中国 | 0 | 0 | — | — | `TEAM-9423D4B1B5315FD6` |
| 410 | 智谱 AutoGLM | Zhipu AI / 智谱 | 中国 | 0 | 0 | — | — | `TEAM-AF2B7813EEF54BB9` |
| 411 | 一湾生命科技 / BayOne Life Sciences | 一湾生命科技 / BayOne Life Sciences | 中国 | 0 | 0 | — | — | `TEAM-20258AFC52C5B37F` |
| 412 | 七牛云 / Qiniu Cloud | 七牛云 / Qiniu Cloud | 中国 | 0 | 0 | — | — | `TEAM-8B6EDC7E33F9683F` |
| 413 | 上汽大众汽车有限公司 | 上汽大众汽车有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E4492C6A907C8962` |
| 414 | 上海二三四五网络科技有限公司 | 上海二三四五网络科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-CCC72D540E9C09EF` |
| 415 | 上海交通大学机械与动力工程学院邵雷来团队 | 上海交通大学 | 中国 | 0 | 0 | — | — | `TEAM-180D02701DD1B4F9` |
| 416 | AI45Research / 上海人工智能实验室安全可信AI中心 | 上海人工智能实验室 | 中国 | 0 | 0 | — | — | `TEAM-1AC0064DC1D885AD` |
| 417 | InternScience / 上海人工智能实验室 AI For Science中心 | 上海人工智能实验室 | 中国 | 0 | 0 | — | — | `TEAM-FFF369DC296446D7` |
| 418 | Shanghai Artificial Intelligence Laboratory / 上海人工智能实验室 | 上海人工智能实验室 | 中国 | 17 | 17 | 算法、研究与模型 10；工程与应用开发 3；安全、治理与合规 2；评测、测试与质量 2 | 算法、研究与模型 10；工程与应用开发 3；安全、治理与合规 2；评测、测试与质量 2 | `TEAM-9628695203F5AF8B` |
| 419 | 上海六信合投资 | 上海六信合投资 | 中国 | 0 | 0 | — | — | `TEAM-B185196ECA89C31F` |
| 420 | 上海农村商业银行股份有限公司 | 上海农村商业银行股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-DC49FC30DAF8CABC` |
| 421 | 上海创智学院 | 上海创智学院 | 中国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-70048D1AA164851D` |
| 422 | 上海埃迪希科技服务有限公司 / 仪电智算云 | 上海埃迪希科技服务有限公司 / 仪电智算云 | 中国 | 0 | 0 | — | — | `TEAM-D7AB16936F915A3D` |
| 423 | 上海外服广东 / 佳才聘 | 上海外服广东 / 佳才聘 | 中国 | 0 | 0 | — | — | `TEAM-1A4036233ABCF9EE` |
| 424 | 同济大学附属东方医院医学人工智能创新中心 | 上海市东方医院 | 中国 | 0 | 0 | — | — | `TEAM-FE4C5B12386022B6` |
| 425 | 上海帆一尚行科技有限公司 / SAIL-Cloud | 上海帆一尚行科技有限公司 / SAIL-Cloud | 中国 | 0 | 0 | — | — | `TEAM-491C268321FC620D` |
| 426 | 上海数绎智能科技有限公司 / biMetaverse | 上海数绎智能科技有限公司 / biMetaverse | 中国 | 0 | 0 | — | — | `TEAM-84BC93339BBA32BE` |
| 427 | 上海科技大学信息科学与技术学院视觉与数据智能中心 / VDI | 上海科技大学 | 中国 | 0 | 0 | — | — | `TEAM-A2E52A014FB1E02F` |
| 428 | 上海科技大学信息科学与技术学院智能网络中心（NICE） / ShanghaiTech SIST Network Intelligence Center | 上海科技大学 / ShanghaiTech University | 中国 | 0 | 0 | — | — | `TEAM-7D986C5E0632CE65` |
| 429 | 上海紫羚数字科技有限公司 / 紫羚数智 / Gazellio | 上海紫羚数字科技有限公司 / 紫羚数智 / Gazellio | 中国 | 0 | 0 | — | — | `TEAM-B10AF5AFBA3FC20D` |
| 430 | 上海纽酷信息科技有限公司 / Newker | 上海纽酷信息科技有限公司 / Newker | 中国 | 0 | 0 | — | — | `TEAM-576A77C3CC3ECB15` |
| 431 | 胜算云 / SSYCloud | 上海胜算速惠云科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-59A2778D0AE83076` |
| 432 | 上海艺赛旗软件股份有限公司 | 上海艺赛旗软件股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-1E12F8913F5E0497` |
| 433 | 上海英方软件股份有限公司 / Info2Soft | 上海英方软件股份有限公司 / Info2Soft | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-0804BBE9293B487E` |
| 434 | 上海非凸智能科技有限公司 / FTShare | 上海非凸智能科技有限公司 / FTShare | 中国 | 0 | 0 | — | — | `TEAM-05543D62979F53C6` |
| 435 | 世窗信息股份有限公司 / Saitron | 世窗信息股份有限公司 / Saitron | 中国 | 0 | 0 | — | — | `TEAM-C6DF0785D4112A24` |
| 436 | 世纪恒通科技股份有限公司 | 世纪恒通科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-4D94C3A182C13044` |
| 437 | 东莞市大湾区高等研究院智能计算研究中心 / Greater Bay Area Institute of Advanced Research Intelligent Computing Research Center | 东莞市大湾区高等研究院智能计算研究中心 / Greater Bay Area Institute of Advanced Research Intelligent Computing Research Center | 中国 | 0 | 0 | — | — | `TEAM-9DA571008E67A74F` |
| 438 | 中关村科金 / ZKJ Technology | 中关村科金 / ZKJ Technology | 中国 | 0 | 0 | — | — | `TEAM-56FA03CC1333BCC8` |
| 439 | 中南大学姜守勇团队 | 中南大学 | 中国 | 0 | 0 | — | — | `TEAM-C9D42BCEF552501E` |
| 440 | 上海振华重工（集团）股份有限公司 / ZPMC | 中国交通建设股份有限公司 / CCCC | 中国 | 0 | 0 | — | — | `TEAM-07E0FD9DE8704B5B` |
| 441 | 中国北方车辆研究所（中国兵器第一研究院） | 中国兵器工业集团 | 中国 | 0 | 0 | — | — | `TEAM-A2FE13086539A3BA` |
| 442 | 中国星网数字科技有限公司 | 中国卫星网络集团有限公司 | 中国 | 1 | 0 | — | 算法、研究与模型 1 | `TEAM-5BF74A62E30FB70A` |
| 443 | 中国标准化研究院高新技术标准化研究所 | 中国标准化研究院 | 中国 | 1 | 0 | — | 算法、研究与模型 1 | `TEAM-781E42936511A142` |
| 444 | 中国科学院大连化学物理研究所人工智能应用中心 | 中国科学院 | 中国 | 0 | 0 | — | — | `TEAM-25D69A2FA86035A2` |
| 445 | 中国科学院自动化研究所 / CASIA | 中国科学院 | 中国 | 0 | 0 | — | — | `TEAM-5DD17803119F1ADE` |
| 446 | 国家生物信息中心数据资源部 | 中国科学院北京基因组研究所 | 中国 | 0 | 0 | — | — | `TEAM-9FE8678813DEE594` |
| 447 | 生物设计中心 | 中国科学院天津工业生物技术研究所 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-983C33E209C22216` |
| 448 | 数据智能与可视化课题组 / 人类细胞谱系大科学研究设施 | 中国科学院广州生物医药与健康研究院 | 中国 | 0 | 0 | — | — | `TEAM-080ABC34F0B3E9A8` |
| 449 | 中国科学院西安光机所大数据与人工智能中心 | 中国科学院西安光学精密机械研究所 | 中国 | 0 | 0 | — | — | `TEAM-0E9504BF8715B6D5` |
| 450 | 天府宇宙线研究中心数字化团队 | 中国科学院高能物理研究所 | 中国 | 0 | 0 | — | — | `TEAM-15C6440CF578C7DB` |
| 451 | 中移（杭州）信息技术有限公司 | 中国移动 | 中国 | 0 | 0 | — | — | `TEAM-6C870AE750A8A49D` |
| 452 | 中国能建电力规划总院 / 中能智新公司 | 中国能源建设集团（股份）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-9D56782C78363E9F` |
| 453 | 中航集团（国航股份） | 中国航空集团有限公司 | 中国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-AB1CDAEFD78917FC` |
| 454 | 中国银联 / China UnionPay | 中国银联 / China UnionPay | 中国 | 0 | 0 | — | — | `TEAM-ED98D115D78F6331` |
| 455 | 中安云科科技发展(山东)有限公司 | 中安云科科技发展(山东)有限公司 | 中国 | 0 | 0 | — | — | `TEAM-F0912DC92FC58AAB` |
| 456 | 中富通集团 / ZFTII | 中富通集团股份有限公司 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-1B20E993AD0E4F45` |
| 457 | 中山大学先进制造学院先进智造实验室 | 中山大学 | 中国 | 0 | 0 | — | — | `TEAM-D8D56BE4719A4957` |
| 458 | 中山大学计算机学院刘咏梅研究组 | 中山大学 | 中国 | 0 | 0 | — | — | `TEAM-35D3A8E20B319344` |
| 459 | 中硅星云科技（广州）有限公司 | 中硅星云科技（广州）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-122085B3090D1002` |
| 460 | 中科星图股份有限公司 | 中科星图股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6BDDBD421E40636C` |
| 461 | 中科智源 / Zhongke Zhiyuan | 中科智源 / Zhongke Zhiyuan | 中国 | 0 | 0 | — | — | `TEAM-624A0F831C482A6B` |
| 462 | 中科紫东太初 | 中科紫东太初 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-B19E23F877034D2D` |
| 463 | 中软国际有限公司 | 中软国际有限公司 | 中国 | 0 | 0 | — | — | `TEAM-C92C085817526D51` |
| 464 | 中通天鸿（北京）通信科技股份有限公司 | 中通天鸿（北京）通信科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-030AA2E1C4B541F8` |
| 465 | 临床科学家 / 风锐智能体 | 临床科学家 / 风锐智能体 | 中国 | 0 | 0 | — | — | `TEAM-942F45D2D46C75CB` |
| 466 | 乐有家 / Leyoujia | 乐有家 / Leyoujia | 中国 | 0 | 0 | — | — | `TEAM-A4FB5F53A79A937C` |
| 467 | 云扩科技 | 云扩科技 | 中国 | 0 | 0 | — | — | `TEAM-8C5297102B5548A1` |
| 468 | 云舟智维（武汉）科技有限责任公司 | 云舟智维（武汉）科技有限责任公司 | 中国 | 0 | 0 | — | — | `TEAM-A351E7C7E681856B` |
| 469 | 云起技术 | 云起技术 | 中国 | 0 | 0 | — | — | `TEAM-998DE777AC3D3E1C` |
| 470 | AsiaInfo Technologies / 亚信科技 | 亚信科技（中国）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3A7C3788A9E5144B` |
| 471 | 仟寻 MoSeeker | 仟寻 MoSeeker | 中国 | 0 | 0 | — | — | `TEAM-7CC83D66C31FD874` |
| 472 | 仟寻 MoSeeker 招聘智能体 | 仟寻 MoSeeker 招聘智能体 | 中国 | 0 | 0 | — | — | `TEAM-750FFBA609F51453` |
| 473 | 企查查智能体数据平台 / qcc-agent-cli | 企查查科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-00FAEC4F32A00A79` |
| 474 | 众数信科 / CrowdDigital | 众数（厦门）信息科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-9B012F1A96C4F09F` |
| 475 | 众阳健康集团 | 众阳健康集团 | 中国 | 0 | 0 | — | — | `TEAM-E26EACE700E3B883` |
| 476 | 优匠时代智能科技（东莞）有限公司 / Youjiang Era Intelligent Technology (Dongguan) | 优匠时代智能科技（东莞）有限公司 / Youjiang Era Intelligent Technology (Dongguan) | 中国 | 0 | 0 | — | — | `TEAM-E06F7468021085A2` |
| 477 | 佛山市斜杠无界信息科技有限公司 / 斜杠无界 | 佛山市斜杠无界信息科技有限公司 / 斜杠无界 | 中国 | 0 | 0 | — | — | `TEAM-333D63DD76D57D0E` |
| 478 | 佳昊创想（深圳）科技有限公司 | 佳昊创想（深圳）科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-2718ED1F69C28E25` |
| 479 | 依图科技 / YITU | 依图科技 / YITU | 中国 | 0 | 0 | — | — | `TEAM-E3B611A1771AEA06` |
| 480 | 信息高铁研究院 / 算力网原生龙虾智能体 | 信息高铁研究院 / 算力网原生龙虾智能体 | 中国 | 0 | 0 | — | — | `TEAM-9F1CE9B94EE92874` |
| 481 | 健康萧山 / 区一医院伦理审查智能体 | 健康萧山 / 区一医院伦理审查智能体 | 中国 | 0 | 0 | — | — | `TEAM-42308C44812A41EC` |
| 482 | Bazhuayu / Octoparse | 八爪鱼 MCP service team (legal entity unresolved) | 中国 | 0 | 0 | — | — | `TEAM-7FEAB948ED41C15C` |
| 483 | 养虾社 / 智能体经济网络 | 养虾社 / 智能体经济网络 | 中国 | 0 | 0 | — | — | `TEAM-A5B3C2624635B0AA` |
| 484 | 全球搜 / AI建站智能体 | 创贸科技（深圳）集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-03BAE5682F33DA42` |
| 485 | 前端程序设计 / 多数字人智能体协作办公系统 | 前端程序设计 / 多数字人智能体协作办公系统 | 中国 | 0 | 0 | — | — | `TEAM-8A927CBA2C6A124A` |
| 486 | 剑及智能科技 | 剑及智能科技 | 中国 | 0 | 0 | — | — | `TEAM-71AD800748F52C7B` |
| 487 | 北京京橙创意网络科技有限公司 / 京橙科技 | 北京京橙创意网络科技有限公司 / 京橙科技 | 中国 | 0 | 0 | — | — | `TEAM-EF6CAFC357CC754F` |
| 488 | 北京兴云数科技术有限公司 | 北京兴云数科技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6BA7830166FC60C5` |
| 489 | 北京华胜天成科技股份有限公司 / Teamsun | 北京华胜天成科技股份有限公司 / Teamsun | 中国 | 0 | 0 | — | — | `TEAM-27E72C3BA8D2C319` |
| 490 | 北京博研智通科技有限公司 / BeyondTraffic | 北京博研智通科技有限公司 / BeyondTraffic | 中国 | 0 | 0 | — | — | `TEAM-F58843A122D55B18` |
| 491 | 北京博雅睿视科技有限公司 / Realscene | 北京博雅睿视科技有限公司 / Realscene | 中国 | 0 | 0 | — | — | `TEAM-1AE4583CD5AE918B` |
| 492 | 北京呼波特人工智能科技有限公司 / WhoBot | 北京呼波特人工智能科技有限公司 / WhoBot | 中国 | 0 | 0 | — | — | `TEAM-2536F8DC465CD3D7` |
| 493 | 北京大学计算中心 / Peking University Computer Center | 北京大学 | 中国 | 0 | 0 | — | — | `TEAM-B50B78F01E8AA663` |
| 494 | 北京奇奇科技有限公司 / Qiqi Technology | 北京奇奇科技有限公司 / Qiqi Technology | 中国 | 0 | 0 | — | — | `TEAM-58D6019434B1D417` |
| 495 | 北京寄云鼎城科技有限公司（寄云科技） | 北京寄云鼎城科技有限公司（寄云科技） | 中国 | 0 | 0 | — | — | `TEAM-6E884AC8FA8A2645` |
| 496 | 左手医生 | 北京左医科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6066E58CF1CE57AF` |
| 497 | 北京微语天下科技有限公司 | 北京微语天下科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-AB2B1578D859F69F` |
| 498 | 北京斯朗科技有限公司 / See-Long | 北京斯朗科技有限公司 / See-Long | 中国 | 0 | 0 | — | — | `TEAM-37626BF6BEAF108C` |
| 499 | 北京智体纪元科技有限公司 / AgentEra | 北京智体纪元科技有限公司 / AgentEra | 中国 | 0 | 0 | — | — | `TEAM-DC67FF580ECB08C1` |
| 500 | 北京深演智能科技股份有限公司 | 北京深演智能科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E9FA803F4C34454A` |
| 501 | 北京彩智科技有限公司 / 深知智能 | 北京深知智新科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6D59A5AC98541399` |
| 502 | 北京深维智信科技有限公司 / OmniMay | 北京深维智信科技有限公司 / OmniMay | 中国 | 0 | 0 | — | — | `TEAM-5955CC0BAD01EF4E` |
| 503 | 北京瑞索科技有限公司 | 北京瑞索科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-F0B339F82DC7B204` |
| 504 | 北京百炼智能科技有限公司 / 百炼智能 | 北京百炼智能科技有限公司 / 百炼智能 | 中国 | 0 | 0 | — | — | `TEAM-70EB844F9FC2CA3C` |
| 505 | 北京睿来智能体技术有限公司 / Reliable Agent | 北京睿来智能体技术有限公司 / Reliable Agent | 中国 | 0 | 0 | — | — | `TEAM-6C3E583128AD642D` |
| 506 | 墨刀 / Modao | 北京磨刀刻石科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-C5C04DCAB1958194` |
| 507 | 小冰 | 北京红棉小冰科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A8C781909E4EC090` |
| 508 | 北京网医联盟科技有限公司 | 北京网医联盟科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-92A256E938C86F60` |
| 509 | 行旅国际 / Auvgo | 北京艾优薇文化科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3741A93773B9FC2E` |
| 510 | 北京超图软件股份有限公司 / SuperMap | 北京超图软件股份有限公司 / SuperMap | 中国 | 0 | 0 | — | — | `TEAM-DEED5B555E30AE99` |
| 511 | 北京跨赴科技有限公司 | 北京跨赴科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-15BDA0D837C68382` |
| 512 | 北京通用人工智能研究院 / BIGAI | 北京通用人工智能研究院 / BIGAI | 中国 | 0 | 0 | — | — | `TEAM-ECBD45D87AA6BF28` |
| 513 | 北森 Beisen | 北森 Beisen | 中国 | 1 | 0 | — | 产品与设计 1 | `TEAM-ABECF44E032573CA` |
| 514 | 北京汽车研究总院有限公司 | 北汽集团 | 中国 | 0 | 0 | — | — | `TEAM-D42C496B8E33E6D0` |
| 515 | 医联 MedGPT | 医联 MedGPT | 中国 | 0 | 0 | — | — | `TEAM-346FFA1A5D129A3F` |
| 516 | 十镜科技 / Spiro | 十镜科技 / Spiro | 中国 | 0 | 0 | — | — | `TEAM-F821AE380D1111A7` |
| 517 | 华中师范大学人工智能教育学部 | 华中师范大学人工智能教育学部 | 中国 | 0 | 0 | — | — | `TEAM-8AC4E1E113D672E4` |
| 518 | 华宇元典 | 华宇元典 | 中国 | 0 | 0 | — | — | `TEAM-62691ADEDDF28D7D` |
| 519 | 华宇元典 / Yuandian Legal Data | 华宇元典 | 中国 | 0 | 0 | — | — | `TEAM-0BB0FF1B86E16E4A` |
| 520 | 南京上智涌现科技有限公司 / MindSparks AI | 南京上智涌现科技有限公司 / MindSparks AI | 中国 | 0 | 0 | — | — | `TEAM-67C4FE1C4DE6491E` |
| 521 | 南京伊克罗德信息科技有限公司 | 南京伊克罗德信息科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-F153AC08BCF7FAF7` |
| 522 | 南京众智维信息科技有限公司 / OpenXorg | 南京众智维信息科技有限公司 / OpenXorg | 中国 | 0 | 0 | — | — | `TEAM-1A3D6AB0205D4E28` |
| 523 | 南京元数信息技术有限公司 | 南京元数信息技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-FE22C16A40DCA03E` |
| 524 | 南京大学 / Nanjing University | 南京大学 / Nanjing University | 中国 | 0 | 0 | — | — | `TEAM-CC83CCF8E695C953` |
| 525 | 南京大学智能科学与技术学院 / Nanjing University School of Intelligent Science and Technology | 南京大学 / Nanjing University | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-0FB18D186F691E2E` |
| 526 | 南京大学大规模智能与知识实验室 / NJU-LINK | 南京大学大规模智能与知识实验室 / NJU-LINK | 中国 | 0 | 0 | — | — | `TEAM-61944BAADD6BA991` |
| 527 | 南京智子互联科技有限公司 | 南京智子互联科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-5F45A454A08C31F8` |
| 528 | 南方科技大学自动化与智能制造学院林志赟课题组 | 南方科技大学 | 中国 | 0 | 0 | — | — | `TEAM-617A9EBDF5EA8129` |
| 529 | 熊鹏文教授课题组 / 智能机器人江西省重点实验室 | 南昌大学先进制造学院 | 中国 | 0 | 0 | — | — | `TEAM-5A84C8F319CD3B8B` |
| 530 | 南昌科技职业大学 | 南昌科技职业大学 | 中国 | 0 | 0 | — | — | `TEAM-9B0ED393F27A2233` |
| 531 | 厚锋科技（上海）有限公司 | 厚锋科技（上海）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-0E8003F1AA64EDA6` |
| 532 | 厦门大学信息学院俞容山课题组 / XMU Yu Rongshan team | 厦门大学 / Xiamen University | 中国 | 0 | 0 | — | — | `TEAM-008CE94406596C4A` |
| 533 | 厦门大学未来海洋生物智造前沿研究中心 / XMU OceanBioX FutureLab | 厦门大学 / Xiamen University | 中国 | 0 | 0 | — | — | `TEAM-C9EDBA4C965F2B95` |
| 534 | 厦门市拾光信维科技有限公司 / Opstime | 厦门市拾光信维科技有限公司 / Opstime | 中国 | 0 | 0 | — | — | `TEAM-9D2C4A4A7985A52C` |
| 535 | 厦门雅迅智联科技股份有限公司 | 厦门雅迅智联科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A60342136A27B7C5` |
| 536 | 合肥中科类脑智能技术有限公司 | 合肥中科类脑智能技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-89DB579E9FA353AA` |
| 537 | 合肥工业大学白羽团队 | 合肥工业大学 | 中国 | 0 | 0 | — | — | `TEAM-0E2837857D875960` |
| 538 | 吉林省济元信息科技有限公司 / Jiyuan Information | 吉林省济元信息科技有限公司 / Jiyuan Information | 中国 | 0 | 0 | — | — | `TEAM-E6A0A21199134802` |
| 539 | 同花顺问财 | 同花顺问财 | 中国 | 0 | 0 | — | — | `TEAM-5D40604A6D1F40BB` |
| 540 | 启元实验室 | 启元实验室 | 中国 | 0 | 0 | — | — | `TEAM-7B8901399A21C916` |
| 541 | 呆码信息技术研究院 / 呆马区块链网络科技有限公司 | 呆码信息技术研究院 / 呆马区块链网络科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E7B1DEA626E195FE` |
| 542 | 品览（杭州）科技有限公司 | 品览（杭州）科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-4FEE41E13F1FB4CB` |
| 543 | 哈尔滨工业大学数据智能安全课题组 / Sun Xinyue team | 哈尔滨工业大学数据智能安全课题组 / Sun Xinyue team | 中国 | 0 | 0 | — | — | `TEAM-F23F5DCF4C6F181C` |
| 544 | 喆塔科技 / ZetaTech | 喆塔科技 / ZetaTech | 中国 | 0 | 0 | — | — | `TEAM-A164FD3E44A06891` |
| 545 | 噢易云 | 噢易云 | 中国 | 0 | 0 | — | — | `TEAM-0B43BC4752726452` |
| 546 | 四川华鲲振宇智能科技有限责任公司 | 四川华鲲振宇智能科技有限责任公司 | 中国 | 0 | 0 | — | — | `TEAM-6EA36DFB3F039778` |
| 547 | 复旦大学类脑智能科学与技术研究院 | 复旦大学 | 中国 | 1 | 0 | — | 算法、研究与模型 1 | `TEAM-8A87601D3E360562` |
| 548 | 大汉软件股份有限公司 / Hanweb | 大汉软件股份有限公司 / Hanweb | 中国 | 0 | 0 | — | — | `TEAM-46BBB441CA7C0F39` |
| 549 | 大连久元鼎晟科技有限公司 | 大连久元鼎晟科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A161E4DBE8283E5E` |
| 550 | 大商所飞泰测试技术有限公司 | 大连商品交易所 | 中国 | 0 | 0 | — | — | `TEAM-DE077B553B0A4035` |
| 551 | 大连文产教育科技有限公司 | 大连文化教育产业集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-8D79449F49809A15` |
| 552 | 大连理工大学化工学院张博宇团队 | 大连理工大学 | 中国 | 0 | 0 | — | — | `TEAM-92B5125CA8902357` |
| 553 | 大连理工大学软件学院 WISDOM实验室 | 大连理工大学 | 中国 | 0 | 0 | — | — | `TEAM-1E8E3F0370FDDF67` |
| 554 | 天工 AI | 天工 AI | 中国 | 0 | 0 | — | — | `TEAM-5CE4A15782E47C72` |
| 555 | 天津大学佟鑫宇团队 | 天津大学 | 中国 | 0 | 0 | — | — | `TEAM-17B3C281EDFAAACB` |
| 556 | 妙盈科技 | 妙盈科技 | 中国 | 0 | 0 | — | — | `TEAM-1BDF5D6486D2AE92` |
| 557 | 季华实验室 / Ji Hua Laboratory | 季华实验室 / Ji Hua Laboratory | 中国 | 0 | 0 | — | — | `TEAM-4730F5AAAA841CCC` |
| 558 | 宁波数字孪生（东方理工）研究院 / Ningbo Institute of Digital Twin | 宁波东方理工大学 / Eastern Institute of Technology Ningbo | 中国 | 0 | 0 | — | — | `TEAM-85647681D66F0063` |
| 559 | 它石智航 / TARS | 它石智航 / TARS | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-5FEB18689E84BDE1` |
| 560 | 安徽三禾一信息科技有限公司 | 安徽三禾一信息科技有限公司 | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-D2182937C1A57DE6` |
| 561 | 安徽百得思维信息科技有限公司 / iBestServices | 安徽百得思维信息科技有限公司 / iBestServices | 中国 | 0 | 0 | — | — | `TEAM-31133DAE1AB2CD6E` |
| 562 | 安诺优达 / Annoroad | 安诺优达基因科技（北京）股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-2C9D687E2A188490` |
| 563 | 实在智能 | 实在智能 | 中国 | 0 | 0 | — | — | `TEAM-B5AB1211ABE01CE2` |
| 564 | 尊创数字科技南京有限公司 / AgenticAudit | 尊创数字科技南京有限公司 / AgenticAudit | 中国 | 0 | 0 | — | — | `TEAM-9D0E5AA426BBA846` |
| 565 | 小i机器人 华藏大模型 | 小i机器人 华藏大模型 | 中国 | 0 | 0 | — | — | `TEAM-7943FDD582D8637A` |
| 566 | 小多科技 | 小多科技 | 中国 | 0 | 0 | — | — | `TEAM-E8A4BBF525B1B717` |
| 567 | 小马智行 / Pony.ai | 小马智行 / Pony.ai | 中国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-FB53C4EF499FB7E0` |
| 568 | 山东中创软件商用中间件股份有限公司 | 山东中创软件商用中间件股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-D011C1D4F1736FBC` |
| 569 | 山东华越智能科技有限公司 / Huayue Intelligent | 山东华越智能科技有限公司 / Huayue Intelligent | 中国 | 0 | 0 | — | — | `TEAM-392851C5B5E4279C` |
| 570 | 山东大学通用智能实验室 | 山东大学通用智能实验室 | 中国 | 0 | 0 | — | — | `TEAM-A066E5269B682597` |
| 571 | 山东恒远智能科技有限公司 / Hengyuan Technology | 山东恒远智能科技有限公司 / Hengyuan Technology | 中国 | 0 | 0 | — | — | `TEAM-5200091C5E8B118C` |
| 572 | 山东极视角科技股份有限公司 / Extreme Vision | 山东极视角科技股份有限公司 / Extreme Vision | 中国 | 0 | 0 | — | — | `TEAM-20AA16B274D13372` |
| 573 | 星数为来（杭州）科技有限公司 | 巴瓜潭数科 | 中国 | 0 | 0 | — | — | `TEAM-AE062025486B2A1A` |
| 574 | 幂律智能 / PowerLaw | 幂律智能 / PowerLaw | 中国 | 0 | 0 | — | — | `TEAM-4BA5705BF8F9EA19` |
| 575 | 平安 AskBob | 平安 AskBob | 中国 | 0 | 0 | — | — | `TEAM-8F1FAA6085D1FB04` |
| 576 | 幸识 / 此间临客 | 幸识 / 此间临客 | 中国 | 0 | 0 | — | — | `TEAM-F9D692CD3C8D8629` |
| 577 | 广东九悦科技有限公司 | 广东九悦科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-B6961795C628B55F` |
| 578 | 广东信息通信业 / 电信服务监管智能体 | 广东信息通信业 / 电信服务监管智能体 | 中国 | 0 | 0 | — | — | `TEAM-F204881CC1F20305` |
| 579 | 广东南粤 / 粤聘云 | 广东南粤 / 粤聘云 | 中国 | 0 | 0 | — | — | `TEAM-878A69B0D4D4808B` |
| 580 | 广州迅易科技有限公司 | 广州迅易科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3BCB75E2F9D37C3B` |
| 581 | 广州金域医学检验集团股份有限公司 / KingMed Diagnostics | 广州金域医学检验集团股份有限公司 / KingMed Diagnostics | 中国 | 0 | 0 | — | — | `TEAM-A201703F1718FB9A` |
| 582 | 广西北投信创科技投资集团有限公司 | 广西北部湾投资集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-AD4F0D4222C6016C` |
| 583 | 广西天起人工智能科技有限公司 / 天起 AI | 广西天起科技集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-83217E75D593CE27` |
| 584 | 廖品正中医眼科技术创新研究院 / 传承智能体 | 廖品正中医眼科技术创新研究院 / 传承智能体 | 中国 | 0 | 0 | — | — | `TEAM-384860BCC2A9E32C` |
| 585 | 影刀 AI | 影刀 AI | 中国 | 0 | 0 | — | — | `TEAM-267ED89E9E4DF506` |
| 586 | 徐州重型机械有限公司 / Xuzhou Heavy Machinery | 徐工集团 / XCMG | 中国 | 0 | 0 | — | — | `TEAM-7A56921EAF4FA072` |
| 587 | 得理法搜 | 得理法搜 | 中国 | 0 | 0 | — | — | `TEAM-A5DB8473947474E0` |
| 588 | 微脉技术有限公司 | 微脉技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3F1BF07DC6BC65C6` |
| 589 | 思必驰科技股份有限公司 | 思必驰科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-825856773B3052AD` |
| 590 | 成都数有引力科技有限公司 | 成都数有引力科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-26027A360931BB94` |
| 591 | 摩尔元数 / Morewis | 摩尔元数 / Morewis | 中国 | 0 | 0 | — | — | `TEAM-3CE5A7BA081F5D15` |
| 592 | 数库科技 | 数库科技 | 中国 | 0 | 0 | — | — | `TEAM-1AFE7D8D7CD27A84` |
| 593 | 数睿数据 / Smardaten | 数睿数据 / Smardaten | 中国 | 0 | 0 | — | — | `TEAM-C7456D66617FD2AD` |
| 594 | BetterYeah | 斑头雁（杭州）智能科技有限责任公司 | 中国 | 0 | 0 | — | — | `TEAM-D1697E4E74A4F0C6` |
| 595 | 斑马网络 | 斑马网络 | 中国 | 0 | 0 | — | — | `TEAM-3193205D25CE6DE5` |
| 596 | 新华三集团 / H3C | 新华三集团 / H3C | 中国 | 0 | 0 | — | — | `TEAM-BB70C2D3EBC9A5AA` |
| 597 | 新奥科技发展有限公司 / 新奥能源研究院 | 新奥集团 | 中国 | 0 | 0 | — | — | `TEAM-2513989A81589845` |
| 598 | 新潮传媒集团 | 新潮传媒集团 | 中国 | 0 | 0 | — | — | `TEAM-31FE5CCF6627B76D` |
| 599 | 旷世传声传媒科技有限责任公司 | 旷世传声传媒科技有限责任公司 | 中国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-A7029FDD8CDB3E8E` |
| 600 | 明道云 AI Agent | 明道云 AI Agent | 中国 | 0 | 0 | — | — | `TEAM-21BD424E864CA721` |
| 601 | 明鉴智律 / InsightLex.AI | 明鉴智律 / InsightLex.AI | 中国 | 0 | 0 | — | — | `TEAM-036AF8D7802F522A` |
| 602 | 易路 eRoad | 易路 eRoad | 中国 | 0 | 0 | — | — | `TEAM-842CEB84559134DE` |
| 603 | 星驰智驾 / ShineAuto | 星驰智驾 / ShineAuto | 中国 | 0 | 0 | — | — | `TEAM-D26F1B2444D3F629` |
| 604 | 春客科技集团 | 春客科技集团 | 中国 | 0 | 0 | — | — | `TEAM-12F8839C47CF800C` |
| 605 | 晓多科技 | 晓多科技 | 中国 | 0 | 0 | — | — | `TEAM-82AE0C43C84DF0D0` |
| 606 | 智慧树 | 智慧树 | 中国 | 0 | 0 | — | — | `TEAM-AC7A45562409FDEA` |
| 607 | 智慧海事 / 危货智审 | 智慧海事 / 危货智审 | 中国 | 0 | 0 | — | — | `TEAM-E1953FA9612AEB5B` |
| 608 | 智齿 AI Agent | 智齿 AI Agent | 中国 | 0 | 0 | — | — | `TEAM-5441E1D0D63DEB33` |
| 609 | 曦望Sunrise | 曦望Sunrise | 中国 | 0 | 0 | — | — | `TEAM-A288FED8081D37BB` |
| 610 | 有道翻译 AI 助手 | 有道翻译 AI 助手 | 中国 | 0 | 0 | — | — | `TEAM-EA073EE304D71C22` |
| 611 | 来也 APA Creator | 来也 APA Creator | 中国 | 0 | 0 | — | — | `TEAM-33FEF12346FC04A8` |
| 612 | 杭州叙简科技股份有限公司 / Scooper | 杭州叙简科技股份有限公司 / Scooper | 中国 | 0 | 0 | — | — | `TEAM-F0FA6F4A0E01B998` |
| 613 | 杭州星舟渡科技有限公司 / DevStudio AI | 杭州星舟渡科技有限公司 / DevStudio AI | 中国 | 0 | 0 | — | — | `TEAM-6CDE84E7ADA6361F` |
| 614 | TorchV / 杭州萌嘉网络科技有限公司 | 杭州萌嘉网络科技有限公司 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-C69059B62B75CB90` |
| 615 | 极熵科技 / Maxtropy | 极熵科技 / Maxtropy | 中国 | 0 | 0 | — | — | `TEAM-CF9D08DBA7F85744` |
| 616 | 武汉光庭信息技术股份有限公司 | 武汉光庭信息技术股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E418A27BAE5EBC04` |
| 617 | 武汉智跃创达科技有限公司 | 武汉智跃创达科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-AE16F221705AE3CB` |
| 618 | 江淮前沿技术协同创新中心（江淮实验室） | 江淮前沿技术协同创新中心（江淮实验室） | 中国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-240D29DA8B509779` |
| 619 | 江苏千桐科技有限公司 | 江苏千桐科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-C9CDF262C9560A51` |
| 620 | 江苏经发信息科技服务有限公司 | 江苏经发阳湖数据服务有限公司 | 中国 | 0 | 0 | — | — | `TEAM-617EB2FEB977875B` |
| 621 | 江苏赞奇科技股份有限公司 | 江苏赞奇科技股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A00D3029D5C44B4D` |
| 622 | 江苏集萃华科智能装备科技有限公司 / JITRI Huake Intelligent Equipment | 江苏集萃华科智能装备科技有限公司 / JITRI Huake Intelligent Equipment | 中国 | 0 | 0 | — | — | `TEAM-94F502B48A84D10F` |
| 623 | 江西省金控科技产业集团有限公司 / 金信数科公司 | 江西省金融控股集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-226244BE640B7F75` |
| 624 | 河南宏博测控技术有限公司 / Henan Hongbo Measurement and Control | 河南宏博测控技术有限公司 / Henan Hongbo Measurement and Control | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-4EA9915E6024B6BD` |
| 625 | 河南日报报业集团有限公司 | 河南日报报业集团有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3A8B4692A8304042` |
| 626 | 河钢集团有限公司 / HBIS Group | 河钢集团有限公司 / HBIS Group | 中国 | 0 | 0 | — | — | `TEAM-0C0829DA97B7891C` |
| 627 | 法大大 iTerms | 法大大 iTerms | 中国 | 0 | 0 | — | — | `TEAM-B7F7E9253B43CDA0` |
| 628 | 波克 / Boke | 波克 / Boke | 中国 | 0 | 0 | — | — | `TEAM-D6CC7C4A43A711CD` |
| 629 | 泰华智慧产业集团股份有限公司 / Telchina | 泰华智慧产业集团股份有限公司 / Telchina | 中国 | 0 | 0 | — | — | `TEAM-938663BC741531B1` |
| 630 | 洛阳灵睿网络技术有限公司 | 洛阳灵睿网络技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-F01146162B011539` |
| 631 | 津渡生科 / OxTium Technology | 津渡生科 / OxTium Technology | 中国 | 0 | 0 | — | — | `TEAM-8C6AD2D89FF32087` |
| 632 | PPIO | 派欧云计算（上海）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-94BE64B96E05D468` |
| 633 | 济南数字进化网络技术有限公司 | 济南数字进化网络技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-717BC131A004D060` |
| 634 | 浙江中医药大学金华研究院 / 浙中实验室 | 浙江中医药大学 / 金华市人民政府 | 中国 | 0 | 0 | — | — | `TEAM-098CF12A4D72DD7E` |
| 635 | 浙江大学智能感知与集群控制团队 | 浙江大学 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-BBFF6FF802C215DD` |
| 636 | 浙江大学医学院附属第一医院医学人工智能研究与转化平台 | 浙江大学医学院附属第一医院 | 中国 | 0 | 0 | — | — | `TEAM-B87D851346D505DE` |
| 637 | 浙江大学宁波国际科创中心未来计算技术创新中心 | 浙江大学宁波国际科创中心未来计算技术创新中心 | 中国 | 0 | 0 | — | — | `TEAM-BC4F035B6003E0E3` |
| 638 | 浙江太美医疗科技股份有限公司 / Taimei Medical Technology | 浙江太美医疗科技股份有限公司 / Taimei Medical Technology | 中国 | 0 | 0 | — | — | `TEAM-9C5FC34ED3541F22` |
| 639 | 实在 Agent | 浙江实在智能科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-37448A1F5D3A94D5` |
| 640 | 浙江米奥兰特商务会展股份有限公司 / Meorient | 浙江米奥兰特商务会展股份有限公司 / Meorient | 中国 | 0 | 0 | — | — | `TEAM-149FA70F13222BF0` |
| 641 | 浙江纳里数智健康科技股份有限公司 / 纳里健康 | 浙江纳里数智健康科技股份有限公司 / 纳里健康 | 中国 | 0 | 0 | — | — | `TEAM-7AFB64EA7FF0FE95` |
| 642 | 浮点涌现 / SellMate | 浮点涌现 / SellMate | 中国 | 0 | 0 | — | — | `TEAM-F046A3742B7A6133` |
| 643 | 润开鸿 / 鸿境 | 润开鸿 / 鸿境 | 中国 | 0 | 0 | — | — | `TEAM-F835C5011CCA30AD` |
| 644 | 深圳力维智联技术有限公司 | 深圳力维智联技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-C2834C585C0CAD4C` |
| 645 | 深圳十沣科技有限公司 / Tenfong | 深圳十沣科技有限公司 / Tenfong | 中国 | 0 | 0 | — | — | `TEAM-0FE8537254636752` |
| 646 | 深圳大学明德书院 | 深圳大学 | 中国 | 0 | 0 | — | — | `TEAM-2858823FC4DEAACD` |
| 647 | 模力方舟（Gitee AI） | 深圳奥思研工智能科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-F1A4C30744F8EA99` |
| 648 | 深圳市明心数智科技有限公司 / Mingxin Digital Intelligence | 深圳市明心数智科技有限公司 / Mingxin Digital Intelligence | 中国 | 0 | 0 | — | — | `TEAM-40EB854EE5DEBDBC` |
| 649 | 深圳市未来智联网络研究院 | 深圳市未来智联网络研究院 | 中国 | 0 | 0 | — | — | `TEAM-83D874C3AFA8624C` |
| 650 | 深圳市磅旗科技智能发展有限公司 / Bangqi Technology | 深圳市磅旗科技智能发展有限公司 / Bangqi Technology | 中国 | 0 | 0 | — | — | `TEAM-9BF9FD12FC290FB2` |
| 651 | 思谋科技 / SmartMore | 深圳思谋信息科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-A18A0B44B8B83931` |
| 652 | 深圳河套学院教育人工智能创新中心 | 深圳河套学院 | 中国 | 0 | 0 | — | — | `TEAM-184B65F44F41A2AA` |
| 653 | 深圳理工大学 | 深圳理工大学 | 中国 | 0 | 0 | — | — | `TEAM-E9F3D28C1A0064D3` |
| 654 | 深圳甄才智能科技有限公司 / succAIss | 深圳甄才智能科技有限公司 / succAIss | 中国 | 0 | 0 | — | — | `TEAM-8306875679250C6E` |
| 655 | 深圳远方有光科技有限公司 / Stoke Voltaics | 深圳远方有光科技有限公司 / Stoke Voltaics | 中国 | 0 | 0 | — | — | `TEAM-027A3B6CA3F0C87E` |
| 656 | 深度动力 / 智能体系统标准参编团队 | 深度动力 / 智能体系统标准参编团队 | 中国 | 0 | 0 | — | — | `TEAM-D647CF4982852E84` |
| 657 | 清华四川能源互联网研究院 | 清华四川能源互联网研究院 | 中国 | 0 | 0 | — | — | `TEAM-0B6C68722A839BCD` |
| 658 | 清华大学智能产业研究院 / Tsinghua AIR | 清华大学 / Tsinghua University | 中国 | 0 | 0 | — | — | `TEAM-6E161D9AC6D6D712` |
| 659 | 清华大学电子工程系 / Tsinghua University Department of Electronic Engineering | 清华大学 / Tsinghua University | 中国 | 1 | 0 | — | 算法、研究与模型 1 | `TEAM-F89DF96C0085255C` |
| 660 | 温州科技职业学院（温州市农业科学研究院） / Wenzhou Vocational College of Science and Technology | 温州科技职业学院（温州市农业科学研究院） / Wenzhou Vocational College of Science and Technology | 中国 | 0 | 0 | — | — | `TEAM-9D2335824C0953FC` |
| 661 | 湖北省生态环境科学研究院 / Hubei Academy of Environmental Sciences | 湖北省生态环境厅 / Hubei Department of Ecology and Environment | 中国 | 0 | 0 | — | — | `TEAM-528899D3450A53A1` |
| 662 | 湖南中南智能装备有限公司 / Hunan Zhongnan Intelligent Equipment | 湖南中南智能装备有限公司 / Hunan Zhongnan Intelligent Equipment | 中国 | 0 | 0 | — | — | `TEAM-81564033BE39F093` |
| 663 | 湖南大学金敏团队 | 湖南大学 | 中国 | 0 | 0 | — | — | `TEAM-08F3405B01EBFD89` |
| 664 | 湖南工商大学计算机学院 AI大模型与智能体研究团队 | 湖南工商大学 | 中国 | 0 | 0 | — | — | `TEAM-239503AD34DF10A1` |
| 665 | 湖南涉外经济学院 / Hunan International Economics University | 湖南涉外经济学院 / Hunan International Economics University | 中国 | 0 | 0 | — | — | `TEAM-99F351A3BB0E2F6D` |
| 666 | Didi / 滴滴 | 滴滴全球股份有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E2B9BB1E6A3C96E4` |
| 667 | 潜入梦科技 infiDive | 潜入梦科技 infiDive | 中国 | 0 | 0 | — | — | `TEAM-3CB8E15941D6E15B` |
| 668 | 煜象科技（杭州）有限公司 | 煜象科技（杭州）有限公司 | 中国 | 0 | 0 | — | — | `TEAM-8576D99E10244411` |
| 669 | 牛客企业版 | 牛客企业版 | 中国 | 0 | 0 | — | — | `TEAM-9CB7F23E92465B97` |
| 670 | 猎户星空 / OrionStarAI | 猎户星空 / OrionStarAI | 中国 | 0 | 0 | — | — | `TEAM-C7CBA741406F1D8D` |
| 671 | 环信 AI 客服 | 环信 AI 客服 | 中国 | 0 | 0 | — | — | `TEAM-0723C20DE6604F55` |
| 672 | 珍岛信息技术（上海）股份有限公司 / Marketingforce | 珍岛信息技术（上海）股份有限公司 / Marketingforce | 中国 | 0 | 0 | — | — | `TEAM-71CBB1904E8F9452` |
| 673 | 用AI伴学 / 教育智能体产品群 | 用AI伴学 / 教育智能体产品群 | 中国 | 0 | 0 | — | — | `TEAM-0A3647E873CB19A7` |
| 674 | 瘦吧健康产业集团 / 招聘智能体 | 瘦吧健康产业集团 / 招聘智能体 | 中国 | 0 | 0 | — | — | `TEAM-D7A306AE18CF1282` |
| 675 | 睿创微纳 / Raytron Technology | 睿创微纳 / Raytron Technology | 中国 | 0 | 0 | — | — | `TEAM-53E35F3C8D10C357` |
| 676 | 福州软件职业技术学院 | 福州软件职业技术学院 | 中国 | 0 | 0 | — | — | `TEAM-5B7D5E031EF24721` |
| 677 | 福建拓尔通软件有限公司 | 福建拓尔通软件有限公司 | 中国 | 0 | 0 | — | — | `TEAM-B483057A24015210` |
| 678 | 科创苏州 / 苏小研 | 科创苏州 / 苏小研 | 中国 | 0 | 0 | — | — | `TEAM-D0174F1BDD7A9DE7` |
| 679 | 科迈生物 / Click.mAb. | 科迈生物 / Click.mAb. | 中国 | 0 | 0 | — | — | `TEAM-35F54DACA1FD0103` |
| 680 | 秘塔 AI 搜索 | 秘塔 AI 搜索 | 中国 | 0 | 0 | — | — | `TEAM-ABFE152C5A3FE639` |
| 681 | 积加科技 / addx.ai | 积加科技 / addx.ai | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-F4FFF2EA77D4CF33` |
| 682 | 稿定 AI | 稿定（厦门）科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-761335B8FCEB0C21` |
| 683 | 竹间智能 | 竹间智能 | 中国 | 0 | 0 | — | — | `TEAM-C102C74F54E06AD1` |
| 684 | 纷享销客 / FXiaoke | 纷享销客 / FXiaoke | 中国 | 0 | 0 | — | — | `TEAM-362078D36D1B2818` |
| 685 | 经纬恒润 Hirain | 经纬恒润 Hirain | 中国 | 0 | 0 | — | — | `TEAM-B525092E9951EDA2` |
| 686 | 美洽 AI 智能体 | 美洽 AI 智能体 | 中国 | 0 | 0 | — | — | `TEAM-9C60C1EC1704CCEB` |
| 687 | 航星永志 | 航星永志 | 中国 | 0 | 0 | — | — | `TEAM-7E9015C9436BF23C` |
| 688 | 航链科技 / ARC OS | 航链科技 / ARC OS | 中国 | 0 | 0 | — | — | `TEAM-D17FC60B3891B217` |
| 689 | 芜湖雄狮汽车科技有限公司 / Lion Tech | 芜湖雄狮汽车科技有限公司 / Lion Tech | 中国 | 0 | 0 | — | — | `TEAM-CDB1DCFB17DF1112` |
| 690 | 莫干山地信实验室 | 莫干山地信实验室 | 中国 | 0 | 0 | — | — | `TEAM-97C4CEDDDA6CC2BD` |
| 691 | 北京蓝色光标数据科技股份有限公司 | 蓝色光标集团 | 中国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-F72C5AA4A9BD83A1` |
| 692 | 蜜度 / Midu | 蜜度 / Midu | 中国 | 0 | 0 | — | — | `TEAM-4B2B3480EC6E74C9` |
| 693 | 行云创新 / 深圳行云创新科技有限公司 | 行云创新 / 深圳行云创新科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-6A5C33DAE8602821` |
| 694 | 西南财经大学赵宇通用人工智能与数字经济创新团队 | 西南财经大学 | 中国 | 0 | 0 | — | — | `TEAM-3305596BBC220E60` |
| 695 | 西安众邦网络科技有限公司 | 西安众邦网络科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-E1D5BB867198FDE3` |
| 696 | 西安电子科技大学智能软件工程技术实验室 / ISET Lab | 西安电子科技大学 | 中国 | 0 | 0 | — | — | `TEAM-4847DAF2A7E9B2C7` |
| 697 | 西安领铄智能科技有限公司 | 西安领铄智能科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-967070685D3E251D` |
| 698 | 西湖大学工学院张驰实验室 | 西湖大学 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-AFA0EF3BBF4D9772` |
| 699 | 西湖大学工学院金耀初实验室 | 西湖大学 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-5A05461C5A0B09D5` |
| 700 | 观远数据 ChatBI | 观远数据 ChatBI | 中国 | 0 | 0 | — | — | `TEAM-FE332DC7485855D8` |
| 701 | 谐云科技 / HarmonyCloud | 谐云科技 / HarmonyCloud | 中国 | 0 | 0 | — | — | `TEAM-9AD2270E45FECBF1` |
| 702 | 豆包 | 豆包 | 中国 | 0 | 0 | — | — | `TEAM-DA73563CF61577FA` |
| 703 | 贵阳恒智网络科技 / Hengzhi Network | 贵阳恒智网络科技 / Hengzhi Network | 中国 | 0 | 0 | — | — | `TEAM-B761264118D5B01F` |
| 704 | 赛尔网络 / CERNET | 赛尔网络有限公司 | 中国 | 0 | 0 | — | — | `TEAM-16EC121A8DA97664` |
| 705 | WonderClaw / ClawCV | 超级简历 WonderCV | 中国 | 0 | 0 | — | — | `TEAM-30384FA41858AFA7` |
| 706 | 越疆机器人 | 越疆机器人 | 中国 | 0 | 0 | — | — | `TEAM-B76847F7672332ED` |
| 707 | 跃盟科技 / Deepleaper Technology | 跃盟科技 / Deepleaper Technology | 中国 | 0 | 0 | — | — | `TEAM-5D448AC0A04C94D8` |
| 708 | 跨越速运 | 跨越速运 | 中国 | 0 | 0 | — | — | `TEAM-5591D93252EB4706` |
| 709 | 软通智慧科技有限公司 / iSoftStone Smart | 软通智慧科技有限公司 / iSoftStone Smart | 中国 | 0 | 0 | — | — | `TEAM-F35318012D70B4C6` |
| 710 | 辽宁华擎智工云计算有限公司 | 辽宁华擎智工云计算有限公司 | 中国 | 0 | 0 | — | — | `TEAM-5F5AD88C6A80325C` |
| 711 | 达观数据 / DataGrand | 达观数据 / DataGrand | 中国 | 0 | 0 | — | — | `TEAM-3E57F7E02A342FCB` |
| 712 | 酷睿程 / CARIZON | 酷睿程 / CARIZON | 中国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-63CF26DEF67A1DB9` |
| 713 | 重庆小易智联智能技术有限公司 / Xiaoyi | 重庆小易智联智能技术有限公司 / Xiaoyi | 中国 | 0 | 0 | — | — | `TEAM-E6E26FE7B11CDB8D` |
| 714 | 渝欧新物智 / 重庆渝欧新物智（重庆）科技有限责任公司 | 重庆渝欧跨境电子商务股份有限公司 | 中国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5CEE5377C1D55378` |
| 715 | 重庆通用人工智能研究院 | 重庆通用人工智能研究院 | 中国 | 0 | 0 | — | — | `TEAM-5676E68A668B88D3` |
| 716 | 金智维 AI 数字员工 | 金智维 AI 数字员工 | 中国 | 0 | 0 | — | — | `TEAM-8B1125E43620D1D3` |
| 717 | 金科环境股份有限公司 / GreenTech Environmental | 金科环境股份有限公司 / GreenTech Environmental | 中国 | 0 | 0 | — | — | `TEAM-5A88400A966CA74C` |
| 718 | 长沙小艾引擎科技有限公司 / 小A引擎 | 长沙小艾引擎科技有限公司 / 小A引擎 | 中国 | 0 | 0 | — | — | `TEAM-062289DCA8646379` |
| 719 | 阿里妈妈数字营销 / AI万相 | 阿里妈妈数字营销 / AI万相 | 中国 | 0 | 0 | — | — | `TEAM-BE83DEE1B97D9CFB` |
| 720 | 零次方量化 / Zerith | 零次方量化 / Zerith | 中国 | 0 | 0 | — | — | `TEAM-E22DAB89391F7E0C` |
| 721 | 青岛未来城市信息技术有限公司 | 青岛未来城市信息技术有限公司 | 中国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-F67594F827E0575B` |
| 722 | 青藤云安全 / Qingteng | 青藤云安全 / Qingteng | 中国 | 0 | 0 | — | — | `TEAM-5C1A55CFC51D0D21` |
| 723 | 飞捷科思智能科技（上海）有限公司 / Fysics | 飞捷科思智能科技（上海）有限公司 / Fysics | 中国 | 0 | 0 | — | — | `TEAM-04049400D3E66A56` |
| 724 | FreedomAI | 香港中文大学（深圳） | 中国 | 0 | 0 | — | — | `TEAM-971677FBD9123E25` |
| 725 | 鲲云科技 / Corerain | 鲲云科技 / Corerain | 中国 | 0 | 0 | — | — | `TEAM-1BB60F4DC8496EB4` |
| 726 | 鲲锦天下（厦门）科技有限公司 / MacsMind | 鲲锦天下（厦门）科技有限公司 / MacsMind | 中国 | 0 | 0 | — | — | `TEAM-51E31B4FBB52FF84` |
| 727 | 鼎桥技术有限公司 | 鼎桥技术有限公司 | 中国 | 0 | 0 | — | — | `TEAM-3D74E7D233983929` |
| 728 | 龙岩龙安安全科技有限公司 | 龙岩龙安安全科技有限公司 | 中国 | 0 | 0 | — | — | `TEAM-03EF763F36A31FA5` |
| 729 | 1mind | 1mind | 美国 | 5 | 5 | 产品与设计 2；客户解决方案与交付 1；算法、研究与模型 1；平台、基础设施与数据 1 | 产品与设计 2；客户解决方案与交付 1；算法、研究与模型 1；平台、基础设施与数据 1 | `TEAM-581BDF3619F405E1` |
| 730 | NewCo (Stealth) | 25madison | 美国 | 0 | 0 | — | — | `TEAM-990B5E3F6DCDA9F3` |
| 731 | AArete | AArete | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E05D7E2CE76A8E29` |
| 732 | Acadia Pharmaceuticals | Acadia Pharmaceuticals | 美国 | 0 | 0 | — | — | `TEAM-E507D335D0E58B36` |
| 733 | Acclaim | Acclaim | 美国 | 0 | 0 | — | — | `TEAM-663FF21EF15368A3` |
| 734 | AccuroAI | AccuroAI | 美国 | 0 | 0 | — | — | `TEAM-1BE01AC6EA589837` |
| 735 | Acquisition.com | Acquisition.com | 美国 | 0 | 0 | — | — | `TEAM-1AB8DD98C152F19A` |
| 736 | Acrely | Acrely | 美国 | 0 | 0 | — | — | `TEAM-A492C6FDD37BFAC8` |
| 737 | Activepieces | Activepieces Inc. | 美国 | 0 | 0 | — | — | `TEAM-8E77AEC8478ACD3C` |
| 738 | Actual AI | Actual AI | 美国 | 0 | 0 | — | — | `TEAM-EE695F597BA6FF9A` |
| 739 | Ad Hoc | Ad Hoc | 美国 | 0 | 0 | — | — | `TEAM-497004CEE4D19808` |
| 740 | Advanced Micro Devices / AMD | Advanced Micro Devices / AMD | 美国 | 0 | 0 | — | — | `TEAM-61AB8985C301787F` |
| 741 | Advisor360° | Advisor360° | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9D4092C167603877` |
| 742 | Aeris Communications | Aeris Communications | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-01A6218D53F838CC` |
| 743 | Afelyon | Afelyon | 美国 | 0 | 0 | — | — | `TEAM-77B1DA2F7957F8C2` |
| 744 | AgentDM | AgentDM | 美国 | 0 | 0 | — | — | `TEAM-93231138781768F0` |
| 745 | AgentMail | AgentMail | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-74F5A33EF9274AAA` |
| 746 | Agnost AI | Agnost AI | 美国 | 0 | 0 | — | — | `TEAM-9D9C18B0EDB3BE88` |
| 747 | DeepLearning.AI / Context Hub | AI Fund | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9BDB15FE3D2E738E` |
| 748 | AiPrise | AiPrise | 美国 | 0 | 0 | — | — | `TEAM-E6EDBFD7D66FE25F` |
| 749 | Airbnb | Airbnb | 美国 | 0 | 0 | — | — | `TEAM-EFB3EDD7D0528357` |
| 750 | Airweave | Airweave | 美国 | 0 | 0 | — | — | `TEAM-B855368AF7F9761E` |
| 751 | AIS | AIS | 美国 | 0 | 0 | — | — | `TEAM-3664CC1F7E080379` |
| 752 | Alaro | Alaro | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5A10C3088E1121F6` |
| 753 | Albert Invent | Albert Invent | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-8A0A37E491D07418` |
| 754 | Aline | Aline | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4B30A2EF682EB8FE` |
| 755 | Alkera AI | Alkera AI | 美国 | 0 | 0 | — | — | `TEAM-148CCC51FBA1ACE0` |
| 756 | The Allen Institute for Artificial Intelligence | Allen Institute | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-5920148F3BDB3F9C` |
| 757 | Allowance | Allowance | 美国 | 0 | 0 | — | — | `TEAM-9362F3E46D4EFB2D` |
| 758 | Answer Financial | Allstate | 美国 | 0 | 0 | — | — | `TEAM-D89FF1334720690C` |
| 759 | SquareTrade | Allstate | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CA8380314CB9F7C6` |
| 760 | Allus AI | Allus AI | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-4B401111C25CD0B0` |
| 761 | Alpha Vantage | Alpha Vantage | 美国 | 0 | 0 | — | — | `TEAM-EC9C6B17D2E77554` |
| 762 | Google | Alphabet / Google | 美国 | 0 | 0 | — | — | `TEAM-085CF1D5BF408EA0` |
| 763 | Waymo | Alphabet / Google | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CF068A3AAF6D296A` |
| 764 | Alphawatch AI | Alphawatch AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-637C34B0E21C0E11` |
| 765 | Alterion | Alterion | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-366B5E80DBDCE6E7` |
| 766 | Alteryx, Inc. | Alteryx, Inc. | 美国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-A3FCF33B933595A7` |
| 767 | Amazon Ads | Amazon / AWS | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5B16D4D6EAFB8853` |
| 768 | Amazon Ring | Amazon / AWS | 美国 | 1 | 0 | — | 产品与设计 1 | `TEAM-17D09010C88F858E` |
| 769 | Amazon Web Services | Amazon / AWS | 美国 | 5 | 0 | — | 其他或边界岗位 5 | `TEAM-9313656567665E44` |
| 770 | Ambral | Ambral | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6E1893F144E43321` |
| 771 | American Bureau of Shipping (ABS) | American Bureau of Shipping (ABS) | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-4886DD8E8C7458BE` |
| 772 | CAS | American Chemical Society | 美国 | 0 | 0 | — | — | `TEAM-A09A9F202E613752` |
| 773 | American Express | American Express | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-49DC4441CE109507` |
| 774 | AmeriSave Mortgage Corp. | AmeriSave Mortgage Corp. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D17885D5232500C4` |
| 775 | Amira Learning | Amira Learning | 美国 | 0 | 0 | — | — | `TEAM-3535EA17DA1C765C` |
| 776 | Amulet | Amulet | 美国 | 0 | 0 | — | — | `TEAM-0EE7CED14396860B` |
| 777 | Andco | Andco | 美国 | 0 | 0 | — | — | `TEAM-14C90D1762042191` |
| 778 | Andera | Andera | 美国 | 0 | 0 | — | — | `TEAM-650F4C4ECF6FA01D` |
| 779 | OpenCode | Anomaly Innovations, Inc. | 美国 | 0 | 0 | — | — | `TEAM-82C5746C32D97316` |
| 780 | AnswerMyQ, Inc. | AnswerMyQ, Inc. | 美国 | 0 | 0 | — | — | `TEAM-577AB4552EBE685B` |
| 781 | Anterior | Anterior | 美国 | 0 | 0 | — | — | `TEAM-4923AF3638182963` |
| 782 | Anthropic | Anthropic | 美国 | 65 | 55 | 产品与设计 15；安全、治理与合规 14；评测、测试与质量 12；平台、基础设施与数据 8；商务、市场与合作 3；运营、项目与职能 3 | 产品与设计 15；安全、治理与合规 14；评测、测试与质量 12；其他或边界岗位 10；平台、基础设施与数据 8；商务、市场与合作 3；运营、项目与职能 3 | `TEAM-A6A6891ED31429E7` |
| 783 | Anthropic / Convogo | Anthropic | 美国 | 0 | 0 | — | — | `TEAM-44E39038636640EC` |
| 784 | Vercept | Anthropic | 美国 | 0 | 0 | — | — | `TEAM-E1B71955F2B3E91C` |
| 785 | Cursor / Anysphere | Anysphere, Inc. | 美国 | 2 | 2 | 评测、测试与质量 1；平台、基础设施与数据 1 | 评测、测试与质量 1；平台、基础设施与数据 1 | `TEAM-DE5EA4B969E019CE` |
| 786 | Create.xyz / Anything | Anything | 美国 | 0 | 0 | — | — | `TEAM-07D6E54032BD3E9B` |
| 787 | Blue Machines AI | apna | 美国 | 0 | 0 | — | — | `TEAM-E34DD82B87222686` |
| 788 | Apollo GraphQL | Apollo Graph Inc. | 美国 | 0 | 0 | — | — | `TEAM-7D4D1594666EF6F7` |
| 789 | AppFolio | AppFolio | 美国 | 0 | 0 | — | — | `TEAM-30EB4B9407DF0433` |
| 790 | AppGate | AppGate | 美国 | 0 | 0 | — | — | `TEAM-D89AC0B3E50D3F1E` |
| 791 | Applied Systems | Applied Systems | 美国 | 0 | 0 | — | — | `TEAM-84D65E2DF2E5F775` |
| 792 | AppZen | AppZen | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-C4A0C1A605D09760` |
| 793 | Archer | Archer | 美国 | 0 | 0 | — | — | `TEAM-1348A9188B2C9048` |
| 794 | Archy | Archy | 美国 | 8 | 3 | 平台、基础设施与数据 3 | 平台、基础设施与数据 5；产品与设计 2；商务、市场与合作 1 | `TEAM-DF697C6EC036B349` |
| 795 | Arctic Health | Arctic Health | 美国 | 0 | 0 | — | — | `TEAM-70B1445C14F3BADB` |
| 796 | Arden | Arden | 美国 | 0 | 0 | — | — | `TEAM-4AD1A2585FD0E5EA` |
| 797 | Ardent | Ardent | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DF443B08CC081ABB` |
| 798 | Ariso | Ariso | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2E8FE114F8B33769` |
| 799 | Arize AI | Arize AI | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-09D3583F88D3FB07` |
| 800 | Arize Phoenix / Arize AI | Arize AI | 美国 | 0 | 0 | — | — | `TEAM-844AADA1B31CA505` |
| 801 | Armature | Armature | 美国 | 0 | 0 | — | — | `TEAM-E513004C6FE08588` |
| 802 | arnata | arnata | 美国 | 0 | 0 | — | — | `TEAM-A6B7B263C2B5D1EA` |
| 803 | ARSIEM Corporation | ARSIEM Corporation | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-54E3BBA678037B8B` |
| 804 | Articul8 AI | Articul8 AI | 美国 | 0 | 0 | — | — | `TEAM-104A59F429C17DCE` |
| 805 | Arva AI | Arva AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4F14482C757253D3` |
| 806 | Asha Health | Asha Health | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F55B5D7E4BBB4F7D` |
| 807 | Assembled | Assembled | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BAFC4D65D2C53B38` |
| 808 | Astraea | Astraea | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-46E23C5007A1BC08` |
| 809 | Atlassian | Atlassian | 美国 | 0 | 0 | — | — | `TEAM-7EA3DF1145E13AB8` |
| 810 | Atomic Object | Atomic Object | 美国 | 0 | 0 | — | — | `TEAM-5326263EA28E2C7B` |
| 811 | Atria Health and Research Institute | Atria Health and Research Institute | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3726905310E33DF6` |
| 812 | Atrisa | Atrisa | 美国 | 0 | 0 | — | — | `TEAM-A69C59B5B75D7B24` |
| 813 | Attinio AI | Attinio AI | 美国 | 0 | 0 | — | — | `TEAM-B700CB6FD49FE919` |
| 814 | Auditoria.AI | Auditoria.AI | 美国 | 0 | 0 | — | — | `TEAM-EEC8370EE79D45E1` |
| 815 | Augusto Digital | Augusto Digital | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-129F611F20AF2972` |
| 816 | Aurelian | Aurelian | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9AE88DB88A5EEBA7` |
| 817 | Autohand AI | Autohand AI | 美国 | 0 | 0 | — | — | `TEAM-A3A3F2DB89B184A0` |
| 818 | Automat | Automat | 美国 | 5 | 4 | 产品与设计 1；商务、市场与合作 1；算法、研究与模型 1；平台、基础设施与数据 1 | 商务、市场与合作 2；产品与设计 1；算法、研究与模型 1；平台、基础设施与数据 1 | `TEAM-9E5E11947410F8E0` |
| 819 | AutoSitu | AutoSitu | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9FD8C0D68FBF1576` |
| 820 | Autostep | Autostep | 美国 | 0 | 0 | — | — | `TEAM-254BBBEF8828D4D8` |
| 821 | Avalara | Avalara | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-31C4A65D730EA4FF` |
| 822 | Aware Health | Aware Health | 美国 | 0 | 0 | — | — | `TEAM-16114EB719A5808B` |
| 823 | Baselayer | Baselayer | 美国 | 0 | 0 | — | — | `TEAM-346EF48EDAED5880` |
| 824 | Bay Cities Container | Bay Cities Container | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FCA0A6046182F722` |
| 825 | BCU | BCU | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-67D7A10EEC4A98F7` |
| 826 | BDIPlus | BDIPlus | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7FF9DD3DA69FAB7A` |
| 827 | Belay Technologies | Belay Technologies | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4C9DF10D8686EEA3` |
| 828 | GEICO | Berkshire Hathaway | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2824F6BC9CE5367C` |
| 829 | BIK | BIK | 美国 | 0 | 0 | — | — | `TEAM-DCEC6851D574158C` |
| 830 | BioStack Platforms | BioStack Platforms | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0032267A8833B692` |
| 831 | Birdeye | Birdeye | 美国 | 0 | 0 | — | — | `TEAM-1EC6ECA4AC600E07` |
| 832 | BLEN | BLEN | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-89C3427EEE1BF1C0` |
| 833 | Blue Water Hospitality / Blue Water Development Corporation | Blue Water Hospitality / Blue Water Development Corporation | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4995DA033B1815BD` |
| 834 | Bluejay | Bluejay | 美国 | 0 | 0 | — | — | `TEAM-D45488175D8126A6` |
| 835 | Bolder Apps | Bolder Apps | 美国 | 0 | 0 | — | — | `TEAM-9EDB1E8DFAC484E9` |
| 836 | Boom AI | Boom AI | 美国 | 0 | 0 | — | — | `TEAM-7DB65B2D20ADA5F7` |
| 837 | boost.ai | boost.ai | 美国 | 0 | 0 | — | — | `TEAM-70D8EF03E8DCED99` |
| 838 | Booz Allen Hamilton | Booz Allen Hamilton | 美国 | 0 | 0 | — | — | `TEAM-E5260EA36D6F4FD5` |
| 839 | Bosch Group | Bosch Group | 美国 | 3 | 1 | 算法、研究与模型 1 | 其他或边界岗位 2；算法、研究与模型 1 | `TEAM-192A17096D2B8FD5` |
| 840 | Boundary | Boundary | 美国 | 0 | 0 | — | — | `TEAM-49EF352537BC3ADB` |
| 841 | Bread Financial | Bread Financial | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-87A382B8F0AF18EE` |
| 842 | Bretton AI | Bretton AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-B7BC5592E082D3AF` |
| 843 | Bridgewater Associates | Bridgewater Associates | 美国 | 0 | 0 | — | — | `TEAM-652E0A72942A695E` |
| 844 | Bristol Myers Squibb | Bristol Myers Squibb | 美国 | 0 | 0 | — | — | `TEAM-ED30A4F8C1D90100` |
| 845 | Broccoli AI | Broccoli AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-45F21068781CC00A` |
| 846 | Burnt | Burnt | 美国 | 0 | 0 | — | — | `TEAM-B4E94356E46B2367` |
| 847 | Burq, Inc. | Burq, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C72209874334B7CB` |
| 848 | C the Signs | C the Signs | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-32225CADB23144E6` |
| 849 | C2 Labs, Inc. | C2 Labs, Inc. | 美国 | 0 | 0 | — | — | `TEAM-59827D007ED8A290` |
| 850 | C3 AI | C3 AI | 美国 | 0 | 0 | — | — | `TEAM-41F73149C86E9A28` |
| 851 | Cain Watters & Associates | Cain Watters & Associates | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DF8A24BA36126886` |
| 852 | Cair Health | Cair Health | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D5F9A7F021CAA665` |
| 853 | Callab AI | Callab AI | 美国 | 0 | 0 | — | — | `TEAM-386FD671DFE69A61` |
| 854 | candidate.fyi | candidate.fyi | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C258E5AFBF8C1D4C` |
| 855 | Capital Group | Capital Group | 美国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-AF7A2EE3D7B89141` |
| 856 | Capitol Services | Capitol Services | 美国 | 0 | 0 | — | — | `TEAM-2470BA637A45DDC2` |
| 857 | Cardinal | Cardinal | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E1968090CAA7056C` |
| 858 | Careforce | Careforce | 美国 | 0 | 0 | — | — | `TEAM-6933DC6D237364F2` |
| 859 | CarMax | CarMax | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F47AF4586E763872` |
| 860 | Casco | Casco | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6022CD924016471D` |
| 861 | Catena | Catena | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-223BA09C2824CC00` |
| 862 | Cato Institute | Cato Institute | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FD9A9E02388EF851` |
| 863 | CBT | CBT | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-83E84DD85BB7F869` |
| 864 | Cekura | Cekura | 美国 | 0 | 0 | — | — | `TEAM-E153E0F7D53CAB5F` |
| 865 | CellType | CellType | 美国 | 0 | 0 | — | — | `TEAM-61E8FD04AED57338` |
| 866 | CentralComs | CentralComs | 美国 | 0 | 0 | — | — | `TEAM-877D6ECF51CE60EC` |
| 867 | CertiK | CertiK | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-71B90E23FB0D0348` |
| 868 | CGI | CGI | 美国 | 0 | 0 | — | — | `TEAM-1A4A8470F0A386F0` |
| 869 | Champ AI | Champ AI | 美国 | 0 | 0 | — | — | `TEAM-114809FBC8A88F8C` |
| 870 | CharacterQuilt | CharacterQuilt | 美国 | 0 | 0 | — | — | `TEAM-DDE6A67F2C17B6D1` |
| 871 | Charles River Associates | Charles River Associates | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-76BCA7D5080F852A` |
| 872 | Chasi | Chasi | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E172B9E1D2F9E6A1` |
| 873 | Cheiron | Cheiron | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-21D8711C1B59EEFD` |
| 874 | Cherry Bekaert | Cherry Bekaert | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0689B47C9AD089BE` |
| 875 | ChipAgents | ChipAgents | 美国 | 0 | 0 | — | — | `TEAM-93FE6417612CC701` |
| 876 | Chroma | Chroma | 美国 | 0 | 0 | — | — | `TEAM-AEC727FB241AD666` |
| 877 | Circle Logistics | Circle Logistics | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CB1A612FAD12E317` |
| 878 | Citi / Citigroup | Citi / Citigroup | 美国 | 0 | 0 | — | — | `TEAM-8F5BAB804D8641A8` |
| 879 | Clarion | Clarion | 美国 | 0 | 0 | — | — | `TEAM-CC440300784D64DB` |
| 880 | Clawvisor | Clawvisor | 美国 | 0 | 0 | — | — | `TEAM-D64B65277412B32D` |
| 881 | Langfuse | ClickHouse | 美国 | 0 | 0 | — | — | `TEAM-BCA0DAC0F607604A` |
| 882 | Climb | Climb | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-976427B45BAE3EB1` |
| 883 | CloudNSite | CloudNSite | 美国 | 0 | 0 | — | — | `TEAM-260459EC257F13A1` |
| 884 | CocoIndex | CocoIndex | 美国 | 0 | 0 | — | — | `TEAM-D26C7C656D09532A` |
| 885 | Codoxo | Codoxo | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5D9951F96F4F70C0` |
| 886 | Cogniify | Cogniify | 美国 | 0 | 0 | — | — | `TEAM-27054724599E26A6` |
| 887 | Cognizant | Cognizant | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-787BEEA23696CE4F` |
| 888 | Cohere Commerce | Cohere | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6EB79ACCD7244059` |
| 889 | Cohere Health | Cohere | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-01BC17E27A47F675` |
| 890 | Cohesion | Cohesion | 美国 | 0 | 0 | — | — | `TEAM-46F61B73DB4E12F5` |
| 891 | Comcast | Comcast | 美国 | 0 | 0 | — | — | `TEAM-B1FD2A013CD5F866` |
| 892 | NBCUniversal | Comcast Corporation | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-C56712829ED75B8D` |
| 893 | Commercial Bank of California | Commercial Bank of California | 美国 | 0 | 0 | — | — | `TEAM-08E0D7FD431A9FF6` |
| 894 | Compliance Registry / TESSA | Compliance Registry / TESSA | 美国 | 0 | 0 | — | — | `TEAM-A28CECFADAB1D7FB` |
| 895 | Complir | Complir | 美国 | 0 | 0 | — | — | `TEAM-D93402DE29BE3EA5` |
| 896 | Complyance | Complyance | 美国 | 0 | 0 | — | — | `TEAM-8565AF5862F6A7B7` |
| 897 | Composio | Composio | 美国 | 4 | 0 | — | 其他或边界岗位 4 | `TEAM-E224E19C314CFEAA` |
| 898 | Concourse | Concourse | 美国 | 0 | 0 | — | — | `TEAM-F5C0C41F3A46C5E5` |
| 899 | Conduit | Conduit | 美国 | 0 | 0 | — | — | `TEAM-2945D6C45C658601` |
| 900 | Confido | Confido | 美国 | 0 | 0 | — | — | `TEAM-4591B5B585ECC966` |
| 901 | Harris Computer | Constellation Software Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-969BE6C324C46FB1` |
| 902 | CopilotKit | CopilotKit, Inc. | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-6EED43646570851F` |
| 903 | Coralogix | Coralogix | 美国 | 1 | 0 | — | 客户解决方案与交付 1 | `TEAM-37F3D41C2FB18952` |
| 904 | Cotton Holdings | Cotton Holdings | 美国 | 0 | 0 | — | — | `TEAM-3E9328CD79CE4B99` |
| 905 | Cova | Cova | 美国 | 0 | 0 | — | — | `TEAM-AB4130E1305BBFDF` |
| 906 | Coval | Coval | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7CCB7EBD61E450FD` |
| 907 | Cox Enterprises | Cox Enterprises | 美国 | 0 | 0 | — | — | `TEAM-A2451DD5E213EA89` |
| 908 | Craft Technologies / CraftFlow | Craft Technologies / CraftFlow | 美国 | 0 | 0 | — | — | `TEAM-32EF07C5549A3C69` |
| 909 | Cranston AI | Cranston AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FA81F968BC479DA4` |
| 910 | Credal.ai | Credal.ai | 美国 | 0 | 0 | — | — | `TEAM-DF9BDD4342F1CD6A` |
| 911 | Cresta | Cresta | 美国 | 3 | 0 | — | 产品与设计 1；客户解决方案与交付 1；工程与应用开发 1 | `TEAM-780F90A660C3B4FE` |
| 912 | CrowdStrike | CrowdStrike | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2CAFCC0F09BEBF63` |
| 913 | Crunchyroll | Crunchyroll | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5498DE1FF49F6947` |
| 914 | Cua | Cua | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FB018B485FE56DE3` |
| 915 | Cummins | Cummins | 美国 | 0 | 0 | — | — | `TEAM-372A2865602113D7` |
| 916 | CVS Health | CVS Health | 美国 | 0 | 0 | — | — | `TEAM-4D6F7A2BC7525002` |
| 917 | Datadog | Datadog | 美国 | 0 | 0 | — | — | `TEAM-E99FC396397FB765` |
| 918 | Dataleap | Dataleap | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-33710F889DBBF1EE` |
| 919 | DataSpring | DataSpring | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DC67E57393B8520F` |
| 920 | Datastrato | Datastrato | 美国 | 0 | 0 | — | — | `TEAM-638E95F6632386CF` |
| 921 | David Condrey / misterdev | David Condrey / misterdev | 美国 | 0 | 0 | — | — | `TEAM-B7078A638D8DE2CE` |
| 922 | Day & Zimmermann | Day & Zimmermann | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-51A83BFE0ECE3C11` |
| 923 | Dayforce | Dayforce | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BF0E2DB887AD369E` |
| 924 | Daytona | Daytona PlatformS Inc. (official footer spelling) | 美国 | 1 | 0 | — | 平台、基础设施与数据 1 | `TEAM-699E5445283515AC` |
| 925 | Deccan AI | Deccan AI | 美国 | 0 | 0 | — | — | `TEAM-FE1A0969110376AF` |
| 926 | Deduction | Deduction | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6BDBA211023B05A0` |
| 927 | Deepgram | Deepgram | 美国 | 3 | 3 | 工程与应用开发 2；产品与设计 1 | 工程与应用开发 2；产品与设计 1 | `TEAM-631D2B14D59AAFE7` |
| 928 | Delan Associates, Inc. | Delan Associates, Inc. | 美国 | 0 | 0 | — | — | `TEAM-D77D8D7A9FD2968D` |
| 929 | Delegance | Delegance | 美国 | 0 | 0 | — | — | `TEAM-22DCD7664BDF3A48` |
| 930 | Deloitte | Deloitte | 美国 | 0 | 0 | — | — | `TEAM-96DDB8C70E35398F` |
| 931 | Denta | Denta | 美国 | 0 | 0 | — | — | `TEAM-DB652ACA4DE63DB0` |
| 932 | Depot | Depot | 美国 | 0 | 0 | — | — | `TEAM-D6FB004FA33EB7A3` |
| 933 | DepthFirst | DepthFirst | 美国 | 6 | 5 | 客户解决方案与交付 2；安全、治理与合规 1；评测、测试与质量 1；平台、基础设施与数据 1 | 客户解决方案与交付 2；安全、治理与合规 1；评测、测试与质量 1；产品与设计 1；平台、基础设施与数据 1 | `TEAM-12D1466D041A8784` |
| 934 | DevIQ | DevIQ | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-AECC804300A9A130` |
| 935 | DeVry University | DeVry University | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D44F484F107704AC` |
| 936 | Discovered Materials | Discovered Materials | 美国 | 0 | 0 | — | — | `TEAM-830C6CE187AD0583` |
| 937 | Distru | Distru | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-A0696C641AD75A38` |
| 938 | DocVerify | DocVerify | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-48D1B1BC300F0555` |
| 939 | DomainTools | DomainTools | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D7A9713AF2C6FBDC` |
| 940 | Doss | Doss | 美国 | 0 | 0 | — | — | `TEAM-408529EBC4F1F7EB` |
| 941 | Double Blind Bio | Double Blind Bio | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C8B96E9A3F467DCF` |
| 942 | DPR Construction | DPR Construction | 美国 | 0 | 0 | — | — | `TEAM-D6754BD0F05A307A` |
| 943 | ECI Software Solutions | ECI Software Solutions | 美国 | 0 | 0 | — | — | `TEAM-8EEBDA5AD7D90AD2` |
| 944 | eClerx | eClerx | 美国 | 0 | 0 | — | — | `TEAM-F3B6B1C1D2F0AAAA` |
| 945 | ego / Ego AI | ego / Ego AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CF8C414B446EB7F6` |
| 946 | Elevance Health | Elevance Health | 美国 | 0 | 0 | — | — | `TEAM-ECB913AC2996FFDC` |
| 947 | Eli Lilly and Company | Eli Lilly and Company | 美国 | 0 | 0 | — | — | `TEAM-B2B98D17D1DADB42` |
| 948 | Elixirr Digital | Elixirr | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-82A16882592804C7` |
| 949 | Eliza | Eliza | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C2C8233BEFFBAAAF` |
| 950 | elly client (employer undisclosed) | elly recruiting locator | 美国 | 0 | 0 | — | — | `TEAM-D6615B6D867FA328` |
| 951 | Emergence AI | Emergence AI | 美国 | 0 | 0 | — | — | `TEAM-BE24207FD0029D82` |
| 952 | Encora | Encora | 美国 | 0 | 0 | — | — | `TEAM-64EBAE5E61D60972` |
| 953 | Epic Games, Inc. | Epic Games, Inc. | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-BB4AB003D68E8098` |
| 954 | Equi | Equi | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-9E1069FB9ADA5132` |
| 955 | Equifax | Equifax | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C86445E5399F2AA0` |
| 956 | eSimplicity | eSimplicity | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-92F60457EC39ECFB` |
| 957 | Espa Labs | Espa Labs | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9CDB0F2FDD7B394C` |
| 958 | Generali Global Assistance | Europ Assistance Group | 美国 | 0 | 0 | — | — | `TEAM-A2D5A6B442B94CD1` |
| 959 | Eversheds Sutherland (US) LLP | Eversheds Sutherland (US) LLP | 美国 | 0 | 0 | — | — | `TEAM-3DE3C3156B47722F` |
| 960 | Exa | Exa Labs Inc. | 美国 | 0 | 0 | — | — | `TEAM-5BBA87672E545D41` |
| 961 | Expedia Group | Expedia Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-661C38562FA6471F` |
| 962 | Extra Space Storage Inc. | Extra Space Storage Inc. | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-8C5E4106DC3E7859` |
| 963 | Fabraix | Fabraix | 美国 | 0 | 0 | — | — | `TEAM-645E78F7999D5152` |
| 964 | fabric, Inc. | fabric, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4792DF61FA4A624C` |
| 965 | Fairmarkit | Fairmarkit | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-8AD8C937B7192592` |
| 966 | Fenrock AI | Fenrock AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5464A6015770EA3B` |
| 967 | Fervo Energy | Fervo Energy | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-5E4B469CA211F00D` |
| 968 | FieldAI | FieldAI | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-88C75A0042587C4C` |
| 969 | Fifth Third Bank | Fifth Third Bank | 美国 | 0 | 0 | — | — | `TEAM-34915E879CE3E3E5` |
| 970 | Filevine | Filevine | 美国 | 9 | 2 | 平台、基础设施与数据 2 | 平台、基础设施与数据 4；产品与设计 3；评测、测试与质量 1；客户解决方案与交付 1 | `TEAM-340EBFA3421F32EE` |
| 971 | Finic | Finic | 美国 | 0 | 0 | — | — | `TEAM-4B58D8136588342F` |
| 972 | FinThrive | FinThrive | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-72548895BE9C8AC8` |
| 973 | Fisher Phillips LLP | Fisher Phillips LLP | 美国 | 0 | 0 | — | — | `TEAM-648F14B9FDE89672` |
| 974 | Flagship Pioneering / Pioneering Intelligence | Flagship Pioneering | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9402AF7091F5D867` |
| 975 | Flair Labs | Flair Labs | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-67DD25A4628F75BE` |
| 976 | FlowGen Labs | FlowGen Labs | 美国 | 0 | 0 | — | — | `TEAM-B917F163569D3E2E` |
| 977 | Flowtel | Flowtel | 美国 | 0 | 0 | — | — | `TEAM-77010CDC2A166214` |
| 978 | FLUXAI US INC. | FLUXAI US INC. | 美国 | 0 | 0 | — | — | `TEAM-F8B6BB67D831CF7E` |
| 979 | forgd, inc. | forgd, inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BCAE6B530D0D582C` |
| 980 | Hamming AI | Forward Inc. | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-C457A7247B8B1BE9` |
| 981 | Freestyle | Freestyle | 美国 | 0 | 0 | — | — | `TEAM-937C0DFF71CE14CE` |
| 982 | Freshworks | Freshworks | 美国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-A1CC54B38A603474` |
| 983 | Fullthrottle.ai | Fullthrottle.ai | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-423A984676AB460C` |
| 984 | FurtherAI | FurtherAI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F76E2A020C2DE9EE` |
| 985 | FuseAI | FuseAI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-00342A86C8014AEC` |
| 986 | Future Works | Future Works | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-559C41620622193A` |
| 987 | Emdash / General Action | General Action, Inc. | 美国 | 0 | 0 | — | — | `TEAM-2FAC4FF31CC21830` |
| 988 | General Context | General Context | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-F42511097C96D196` |
| 989 | General Motors | General Motors | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-25934CB8EE0DEB7B` |
| 990 | GM Financial | General Motors | 美国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-C6AFF0A85DDB2EE7` |
| 991 | Genpact Experience | Genpact | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-75DFD30B60962DF8` |
| 992 | GeoDelphi / Whitespace | GeoDelphi / Whitespace | 美国 | 0 | 0 | — | — | `TEAM-FD22E902E416F154` |
| 993 | Ghost | Ghost | 美国 | 0 | 0 | — | — | `TEAM-A119CC2E08E32E6B` |
| 994 | Giga | Giga | 美国 | 13 | 12 | 平台、基础设施与数据 5；商务、市场与合作 2；客户解决方案与交付 2；安全、治理与合规 1；评测、测试与质量 1；产品与设计 1 | 平台、基础设施与数据 5；产品与设计 2；商务、市场与合作 2；客户解决方案与交付 2；安全、治理与合规 1；评测、测试与质量 1 | `TEAM-50AEB088B6BF6D15` |
| 995 | Gigacatalyst | Gigacatalyst | 美国 | 0 | 0 | — | — | `TEAM-BE58C7A83DF947B7` |
| 996 | GIGR | GIGR | 美国 | 0 | 0 | — | — | `TEAM-5852F410851BAD38` |
| 997 | Gilead Sciences | Gilead Sciences | 美国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-0E97E1923CB4B8A0` |
| 998 | Gimlet Labs | Gimlet Labs | 美国 | 0 | 0 | — | — | `TEAM-92A1C132F0418B78` |
| 999 | Glean | Glean | 美国 | 2 | 0 | — | 产品与设计 1；工程与应用开发 1 | `TEAM-67B1F196D17FDDE5` |
| 1000 | Glen | Glen | 美国 | 0 | 0 | — | — | `TEAM-55436E36464BE8DF` |
| 1001 | GodHands | GodHands | 美国 | 0 | 0 | — | — | `TEAM-37F673043A320133` |
| 1002 | goodfin | goodfin | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-43D6B65F495C4DF6` |
| 1003 | Govly, Inc. | Govly, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7D1F2FD83F3D09E6` |
| 1004 | Graebel Companies, Inc. | Graebel Companies, Inc. | 美国 | 0 | 0 | — | — | `TEAM-A7E76A97B076F4E6` |
| 1005 | Gravitee | Gravitee | 美国 | 0 | 0 | — | — | `TEAM-9ADAEF4D52517466` |
| 1006 | Great American Insurance Group | Great American Insurance Group | 美国 | 0 | 0 | — | — | `TEAM-BF87157518246F6C` |
| 1007 | Greater New York Mutual Insurance Company | Greater New York Mutual Insurance Company | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6AAB78F4E087B85B` |
| 1008 | Greptile | Greptile | 美国 | 5 | 4 | 平台、基础设施与数据 3；算法、研究与模型 1 | 平台、基础设施与数据 3；客户解决方案与交付 1；算法、研究与模型 1 | `TEAM-AA286618731A7B97` |
| 1009 | Stratus | GTP Software, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CCC28B9E90A24167` |
| 1010 | Guide Labs | Guide Labs | 美国 | 0 | 0 | — | — | `TEAM-EEF0DBDD453CD8BF` |
| 1011 | Guild.ai | Guild.ai | 美国 | 0 | 0 | — | — | `TEAM-FA32B955448DD636` |
| 1012 | Halluminate | Halluminate | 美国 | 0 | 0 | — | — | `TEAM-C78E9D5CECC39AC4` |
| 1013 | HappyRobot | HappyRobot | 美国 | 7 | 4 | 平台、基础设施与数据 2；评测、测试与质量 1；商务、市场与合作 1 | 评测、测试与质量 2；商务、市场与合作 2；平台、基础设施与数据 2；产品与设计 1 | `TEAM-327C1F0DE62CBF74` |
| 1014 | hardware intelligence | hardware intelligence | 美国 | 0 | 0 | — | — | `TEAM-284FBE7BBB12419B` |
| 1015 | Harper | Harper | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9D1302E24CDC6586` |
| 1016 | Harvard University | Harvard University | 美国 | 0 | 0 | — | — | `TEAM-AA138E5BF5F7DF9B` |
| 1017 | Haven | Haven | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FF93041FC22A5031` |
| 1018 | Hazel | Hazel | 美国 | 0 | 0 | — | — | `TEAM-AC4E4EE259ED90A7` |
| 1019 | Healiom | Healiom | 美国 | 1 | 1 | 算法、研究与模型 1 | 算法、研究与模型 1 | `TEAM-A3E5134E875492B7` |
| 1020 | Heartbeat | Heartbeat | 美国 | 0 | 0 | — | — | `TEAM-DE557C4610B1C0E3` |
| 1021 | Hellyeah AI | Hellyeah AI | 美国 | 0 | 0 | — | — | `TEAM-D3F9107C765B160E` |
| 1022 | Hex Security | Hex Security | 美国 | 0 | 0 | — | — | `TEAM-1BD72407384CBB4F` |
| 1023 | Hexion Inc. | Hexion Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4A9659E8AC7C647E` |
| 1024 | HeyGen | HeyGen | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-914EDB1F2ACF5317` |
| 1025 | High Side Technology | High Side Technology | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7E69ED7E4133EC75` |
| 1026 | Highspot | Highspot | 美国 | 0 | 0 | — | — | `TEAM-16436F886A9BD3C7` |
| 1027 | Hobbes | Hobbes | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-41CA882749F865CA` |
| 1028 | Horizon3.ai | Horizon3.ai | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-7A51B8F340765547` |
| 1029 | HUD | HUD | 美国 | 0 | 0 | — | — | `TEAM-ABF91EF59F8CCE0F` |
| 1030 | Humaans | Humaans | 美国 | 0 | 0 | — | — | `TEAM-8C59CEC121492FE7` |
| 1031 | Humans& | Humans& | 美国 | 0 | 0 | — | — | `TEAM-1E3F3E43EA948BBB` |
| 1032 | Humwork | Humwork | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D2AD61DB8C9BED9E` |
| 1033 | HungerRush / Menufy | HungerRush / Menufy | 美国 | 0 | 0 | — | — | `TEAM-70B3A3445E2705A5` |
| 1034 | HyperProbe | HyperProbe | 美国 | 0 | 0 | — | — | `TEAM-4BC99E703D58D972` |
| 1035 | Hyperspell | Hyperspell | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2E6B73090B62C0F9` |
| 1036 | Hyundai Capital America | Hyundai Capital America | 美国 | 0 | 0 | — | — | `TEAM-870D647779BFDB45` |
| 1037 | ID.me | ID.me | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CFEE8F75E68E40E7` |
| 1038 | Identity Digital | Identity Digital | 美国 | 0 | 0 | — | — | `TEAM-0D80818D648580BD` |
| 1039 | IFS | IFS | 美国 | 5 | 5 | 产品与设计 2；算法、研究与模型 2；客户解决方案与交付 1 | 产品与设计 2；算法、研究与模型 2；客户解决方案与交付 1 | `TEAM-18B8A4B99524EC7F` |
| 1040 | IFS / TheLoops | IFS | 美国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-212FFCD8DF7B1A1A` |
| 1041 | Illume Labs | Illume Labs | 美国 | 0 | 0 | — | — | `TEAM-8635E339ECC0334D` |
| 1042 | Imprezia | Imprezia | 美国 | 0 | 0 | — | — | `TEAM-B86A5C594BF0B0EF` |
| 1043 | Index Analytics LLC | Index Analytics LLC | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5427376B4A4DC4DF` |
| 1044 | Infer | Infer | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C296B58149874037` |
| 1045 | Inferact | Inferact | 美国 | 0 | 0 | — | — | `TEAM-47E7C4C6201C498A` |
| 1046 | Influur | Influur | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5847CE6A7A4F2B9E` |
| 1047 | InRule Technology, Inc. | InRule Technology, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-8F077B293D842CD3` |
| 1048 | InsForge | InsForge | 美国 | 0 | 0 | — | — | `TEAM-EBCA3F3E4FAE0035` |
| 1049 | Insight Enterprises | Insight Enterprises | 美国 | 0 | 0 | — | — | `TEAM-1F1FCFAB981E32FB` |
| 1050 | InstaLILY AI | InstaLILY AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0B9623C1E9E446CC` |
| 1051 | Intel Corporation | Intel Corporation | 美国 | 0 | 0 | — | — | `TEAM-8A6399BF0DFF529F` |
| 1052 | IntelePeer Cloud Communications LLC | IntelePeer Cloud Communications LLC | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-626CE2C703B75934` |
| 1053 | InterConnect Defense / IC Defense | InterConnect Defense / IC Defense | 美国 | 0 | 0 | — | — | `TEAM-6D25A334D21E876A` |
| 1054 | Interfere | Interfere | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6CE68A71D8847CE1` |
| 1055 | Intuigence AI | Intuigence AI | 美国 | 0 | 0 | — | — | `TEAM-CE9716D6E09F708E` |
| 1056 | Intuit Inc. | Intuit Inc. | 美国 | 1 | 0 | — | 产品与设计 1 | `TEAM-4402159A92A4F36C` |
| 1057 | ISO New England | ISO New England | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-1D11CF3DBE2EDD53` |
| 1058 | Johnson & Johnson | Johnson & Johnson | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4E66783AD2FA133E` |
| 1059 | JPMorgan Chase & Co. | JPMorgan Chase & Co. | 美国 | 0 | 0 | — | — | `TEAM-77FFB7E58253704F` |
| 1060 | Judi Health | Judi Health | 美国 | 1 | 1 | 安全、治理与合规 1 | 安全、治理与合规 1 | `TEAM-C1023D0EB67C0274` |
| 1061 | Juicebox | Juicebox | 美国 | 6 | 5 | 客户解决方案与交付 2；安全、治理与合规 1；商务、市场与合作 1；平台、基础设施与数据 1 | 商务、市场与合作 2；客户解决方案与交付 2；安全、治理与合规 1；平台、基础设施与数据 1 | `TEAM-E74F634204F775B9` |
| 1062 | Justinian | Justinian | 美国 | 0 | 0 | — | — | `TEAM-2334C936850AF7C5` |
| 1063 | Kai Cyber, Inc. | Kai Cyber, Inc. | 美国 | 0 | 0 | — | — | `TEAM-A4EFBDCD09BB92B7` |
| 1064 | Kai Security | Kai Security | 美国 | 0 | 0 | — | — | `TEAM-72EFFDACB9A238DE` |
| 1065 | Kargo | Kargo | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-A184671519D961A7` |
| 1066 | Kastle | Kastle | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BC75C3A3F330A0E4` |
| 1067 | Keycard Labs | Keycard Labs | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6EE44F374C78AC5D` |
| 1068 | Kinelo | Kinelo | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-74773236E1556A16` |
| 1069 | Kino AI | Kino AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4AC3F2968415BD59` |
| 1070 | Kinro | Kinro | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7FD2619F57C997F2` |
| 1071 | Dematic | KION Group | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-B095EC3A27BE409B` |
| 1072 | Klaimee | Klaimee | 美国 | 0 | 0 | — | — | `TEAM-A88631CC0A0CD742` |
| 1073 | Klarify | Klarify | 美国 | 0 | 0 | — | — | `TEAM-B5185B66AEB8F503` |
| 1074 | Klavis AI | Klavis AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-1619AE0E3F71E7AD` |
| 1075 | Knotch, Inc. | Knotch, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-8DAA7C390C69C3EF` |
| 1076 | Komodo Health | Komodo Health | 美国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-A47FB816A6B46D1D` |
| 1077 | Kong Inc. | Kong Inc. | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-A1E31AC245E34E0E` |
| 1078 | Kortix | Kortix AI Corp | 美国 | 0 | 0 | — | — | `TEAM-7383F7F71F4F8C8F` |
| 1079 | KPMG US | KPMG US | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-257AD6F9FDFF7AA7` |
| 1080 | Kraken / Payward | Kraken / Payward | 美国 | 0 | 0 | — | — | `TEAM-12F60899333D1D47` |
| 1081 | Kuli | Kuli | 美国 | 0 | 0 | — | — | `TEAM-124138C20689747F` |
| 1082 | Kura AI | Kura AI | 美国 | 0 | 0 | — | — | `TEAM-A74D693CA4ABE042` |
| 1083 | Lance | Lance | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-0FE11DE64CA45A85` |
| 1084 | LangChain | LangChain | 美国 | 3 | 0 | — | 其他或边界岗位 3 | `TEAM-441D6B22770E7A85` |
| 1085 | Layerup | Layerup | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-172CBB26FB16DAFE` |
| 1086 | Lean Solutions Group | Lean Solutions Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-28ABA5236F6847C6` |
| 1087 | Leonardo DRS Land Electronics | Leonardo DRS | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-3B7E0B0E1274F75D` |
| 1088 | Letterbook | Letterbook | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-56632E22A7AD7DE9` |
| 1089 | Lifepoint Health, Inc. | Lifepoint Health, Inc. | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-8DBFEE6C6133C2E2` |
| 1090 | Light Anchor | Light Anchor | 美国 | 0 | 0 | — | — | `TEAM-BB72E6781F83AD97` |
| 1091 | Lighthouz AI | Lighthouz AI | 美国 | 0 | 0 | — | — | `TEAM-A2ACD385D67C4A39` |
| 1092 | Lightsprint | Lightsprint | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7944C411BD3B25B6` |
| 1093 | Liminal Strategy | Liminal Strategy | 美国 | 0 | 0 | — | — | `TEAM-595A1E59A4F1CC54` |
| 1094 | Liner | Liner | 美国 | 8 | 8 | 运营、项目与职能 5；商务、市场与合作 2；产品与设计 1 | 运营、项目与职能 5；商务、市场与合作 2；产品与设计 1 | `TEAM-567669C2033C7C30` |
| 1095 | Linzumi | Linzumi | 美国 | 0 | 0 | — | — | `TEAM-A3A82C40A9D3725C` |
| 1096 | LocalStack | LocalStack | 美国 | 0 | 0 | — | — | `TEAM-D4C6F06A3299B875` |
| 1097 | Lockheed Martin Space | Lockheed Martin | 美国 | 0 | 0 | — | — | `TEAM-6869CF6259312437` |
| 1098 | Loman AI | Loman AI | 美国 | 0 | 0 | — | — | `TEAM-C06A95EE3E6FC20F` |
| 1099 | Longroad Energy | Longroad Energy | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2CE54FE73EC3A94D` |
| 1100 | Lorikeet | Lorikeet | 美国 | 0 | 0 | — | — | `TEAM-85726424CBDD0FCC` |
| 1101 | Lovable | Lovable | 美国 | 0 | 0 | — | — | `TEAM-35A04C97D829D2C6` |
| 1102 | Orca / Stably AI | Lovecast Inc. | 美国 | 0 | 0 | — | — | `TEAM-BA6FA0E12B169BCF` |
| 1103 | Lowenstein Sandler | Lowenstein Sandler | 美国 | 0 | 0 | — | — | `TEAM-011EED7D365E63E6` |
| 1104 | Lumari | Lumari | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-22339A98F83A9D18` |
| 1105 | Luxury Presence | Luxury Presence | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-7F8A2BD624DD36CD` |
| 1106 | LVT | LVT | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-A0A53D21CC1EE3FF` |
| 1107 | Lyzr AI | Lyzr AI | 美国 | 0 | 0 | — | — | `TEAM-B13F13B16E2E2755` |
| 1108 | Machinify | Machinify | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-E1763C4650540962` |
| 1109 | MACOM | MACOM | 美国 | 0 | 0 | — | — | `TEAM-E00EB1E438FE0C06` |
| 1110 | MacStadium | MacStadium | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-EE15635BA1D4BB53` |
| 1111 | MAI | MAI | 美国 | 0 | 0 | — | — | `TEAM-53EBB103B722194B` |
| 1112 | Make | Make | 美国 | 0 | 0 | — | — | `TEAM-1A77460ED703A35E` |
| 1113 | Mango Languages | Mango Languages | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-09BA178CF086C9E1` |
| 1114 | Manicule | Manicule | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FB7BFD64012E9C8F` |
| 1115 | Manufact (formerly mcp-use) | Manufact (formerly mcp-use) | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-E763AFBE3EA02D89` |
| 1116 | MarginFront | MarginFront | 美国 | 0 | 0 | — | — | `TEAM-39A8D8210EA0FF37` |
| 1117 | Marion Counseling Services | Marion Counseling Services | 美国 | 0 | 0 | — | — | `TEAM-A59A9208C475864F` |
| 1118 | Misfits & Machines | Marketing Architects | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4A9A727D36E79609` |
| 1119 | Massachusetts Institute of Technology / MGHPCC | Massachusetts Institute of Technology / MGHPCC | 美国 | 0 | 0 | — | — | `TEAM-6DC9C9D59A5E8C4B` |
| 1120 | Matrices | Matrices | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D95DB777040B5504` |
| 1121 | Medeloop | Medeloop | 美国 | 1 | 1 | 安全、治理与合规 1 | 安全、治理与合规 1 | `TEAM-52CE358C9132B40A` |
| 1122 | MedPro Disposal / MP1 Solutions | MedPro Disposal / MP1 Solutions | 美国 | 0 | 0 | — | — | `TEAM-FD3C5196DEDC37E7` |
| 1123 | Meeting Tomorrow | Meeting Tomorrow | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E948D36C4B0DBF1A` |
| 1124 | Memory Store | Memory Store | 美国 | 0 | 0 | — | — | `TEAM-0F85B636A1E0C67D` |
| 1125 | Intermolecular / EMD Electronics | Merck KGaA | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F74BE0FFB1B674C8` |
| 1126 | Meridian | Meridian | 美国 | 0 | 0 | — | — | `TEAM-95E7487C89A7CBD2` |
| 1127 | Micron Technology | Micron Technology | 美国 | 0 | 0 | — | — | `TEAM-741712D4388326C5` |
| 1128 | Mimecast | Mimecast | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6AD66C345246FB8C` |
| 1129 | MindFort | MindFort | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-101FA2B1547A3F54` |
| 1130 | Minicor | Minicor | 美国 | 0 | 0 | — | — | `TEAM-0020A524760E4EC5` |
| 1131 | Helicone | Mintlify | 美国 | 0 | 0 | — | — | `TEAM-B4F5815862EF77FD` |
| 1132 | MintMCP | MintMCP | 美国 | 0 | 0 | — | — | `TEAM-C526BB2670CA239C` |
| 1133 | AnythingLLM / Mintplex Labs | Mintplex Labs | 美国 | 0 | 0 | — | — | `TEAM-4D304F1210F3AFA2` |
| 1134 | MochaCare | MochaCare | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FAF05E6A588CFC41` |
| 1135 | Modal Labs | Modal Labs | 美国 | 0 | 0 | — | — | `TEAM-39796B4003CFB9CE` |
| 1136 | Modern | Modern | 美国 | 0 | 0 | — | — | `TEAM-AB427E646B411ED7` |
| 1137 | Molina Healthcare | Molina Healthcare | 美国 | 0 | 0 | — | — | `TEAM-8C4B5E09E035D253` |
| 1138 | Momentic | Momentic | 美国 | 0 | 0 | — | — | `TEAM-6125BA7381E8850B` |
| 1139 | Monte Carlo | Monte Carlo | 美国 | 0 | 0 | — | — | `TEAM-54691A47600A7124` |
| 1140 | Mor Furniture For Less Inc. | Mor Furniture For Less Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-063DE3F3BDDCC7D1` |
| 1141 | Mount | Mount | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-48711AE0E2A45BFF` |
| 1142 | Mount Sinai Health System | Mount Sinai Health System | 美国 | 0 | 0 | — | — | `TEAM-0DBB647A18D14271` |
| 1143 | Mural | Mural | 美国 | 0 | 0 | — | — | `TEAM-9E4FFF7669B36030` |
| 1144 | Mutual of Omaha | Mutual of Omaha | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3A78F5B5991D148A` |
| 1145 | Nango | Nango | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-30FF2FCAAB0F4850` |
| 1146 | Narrative | Narrative | 美国 | 0 | 0 | — | — | `TEAM-88260DBC7E8ECD3E` |
| 1147 | Naver U.Hub INC | NAVER | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9E13A1985648BA3F` |
| 1148 | Navy Federal Credit Union | Navy Federal Credit Union | 美国 | 0 | 0 | — | — | `TEAM-3EA9C14F8C59A5B8` |
| 1149 | Tavily | Nebius | 美国 | 0 | 0 | — | — | `TEAM-43C209FDD6DC4FB0` |
| 1150 | Nebula Security | Nebula Security | 美国 | 0 | 0 | — | — | `TEAM-0B79C46C5A12DB48` |
| 1151 | Nex | Nex | 美国 | 0 | 0 | — | — | `TEAM-3E4F4E4773A32E14` |
| 1152 | Nextdev | Nextdev | 美国 | 0 | 0 | — | — | `TEAM-A9930923CC9BC706` |
| 1153 | NexusTek | NexusTek | 美国 | 0 | 0 | — | — | `TEAM-EAE203ED6C42114E` |
| 1154 | Nitra | Nitra | 美国 | 0 | 0 | — | — | `TEAM-4C3BDAFC9BF96A5D` |
| 1155 | NovaVoxx AI | NovaVoxx AI | 美国 | 0 | 0 | — | — | `TEAM-4A56A5E62CB980BF` |
| 1156 | Nozomio | Nozomio | 美国 | 0 | 0 | — | — | `TEAM-D8BCD00F11948C42` |
| 1157 | NTT DATA Services | NTT DATA | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-DF473991675C2B64` |
| 1158 | Nutanix | Nutanix | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0D2DBE4C3A9333A9` |
| 1159 | Nutrient | Nutrient | 美国 | 0 | 0 | — | — | `TEAM-BB5BDB2D7A65721C` |
| 1160 | Observe.AI | Observe.AI | 美国 | 0 | 0 | — | — | `TEAM-887E6902D44E1AD0` |
| 1161 | Ocient | Ocient | 美国 | 0 | 0 | — | — | `TEAM-30C9B0ABF4197C17` |
| 1162 | Onix | Onix | 美国 | 0 | 0 | — | — | `TEAM-76119403CDD6DCE0` |
| 1163 | Onton | Onton | 美国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-F080D45DB10E365F` |
| 1164 | Ontora | Ontora | 美国 | 0 | 0 | — | — | `TEAM-96AD18605ECA0BB3` |
| 1165 | Ooak Data | Ooak Data | 美国 | 0 | 0 | — | — | `TEAM-F840350B5B43DF6A` |
| 1166 | Opendoor | Opendoor | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-FC7388A93C0E8CB9` |
| 1167 | OpenHands | OpenHands | 美国 | 0 | 0 | — | — | `TEAM-357EED72347FC702` |
| 1168 | OpenProse | OpenProse | 美国 | 0 | 0 | — | — | `TEAM-7C8F7C78E5C43518` |
| 1169 | Operon | Operon | 美国 | 0 | 0 | — | — | `TEAM-DC9BAADE52520133` |
| 1170 | OPPO US Research Center / InnoPeak | OPPO | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4B3A5805D1736436` |
| 1171 | Oracle | Oracle | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-C3C7A6C48068D1EA` |
| 1172 | Orbis Operations | Orbis Operations | 美国 | 0 | 0 | — | — | `TEAM-06AEE371DA7F0C37` |
| 1173 | Origin | Origin | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DEEAD9A1F39E88D7` |
| 1174 | Orkes | Orkes | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-1BB8E654B527E7E5` |
| 1175 | Roamly Labs / The Ride Platform | Outdoorsy Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F72DF3F46A20907D` |
| 1176 | Outreach | Outreach | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-B169E4BC9EEB02D7` |
| 1177 | Outtake | Outtake | 美国 | 0 | 0 | — | — | `TEAM-EC7831E3635F3B89` |
| 1178 | Owkin | Owkin | 美国 | 0 | 0 | — | — | `TEAM-BEEE17B40A581477` |
| 1179 | P-1 AI | P-1 AI | 美国 | 0 | 0 | — | — | `TEAM-A8F21C78C10DAB2D` |
| 1180 | Pace | Pace | 美国 | 0 | 0 | — | — | `TEAM-2110EE80A53AD573` |
| 1181 | PaleBlueDot AI | PaleBlueDot AI | 美国 | 0 | 0 | — | — | `TEAM-333320584443A693` |
| 1182 | Pallet | Pallet | 美国 | 0 | 0 | — | — | `TEAM-8CC38D17728FD26B` |
| 1183 | Palo Alto Networks | Palo Alto Networks / Venafi EOOD | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-B681D44C5B735901` |
| 1184 | Parahelp | Parahelp | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-A07CFD7B63D01B42` |
| 1185 | Paramount Global | Paramount Global | 美国 | 0 | 0 | — | — | `TEAM-991EA2A0222C47C4` |
| 1186 | Paramount Streaming | Paramount Skydance Corporation | 美国 | 1 | 1 | 平台、基础设施与数据 1 | 平台、基础设施与数据 1 | `TEAM-D115BE1146966A44` |
| 1187 | Parloa | Parloa | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-08F8201B96D6A77E` |
| 1188 | Pasito | Pasito | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-A30C0BE17F6E05E8` |
| 1189 | Patch My PC | Patch My PC | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-B7EF8F81BB2CEE40` |
| 1190 | Shiplight AI | Pear VC | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-912103D167E16664` |
| 1191 | Pepper | Pepper | 美国 | 0 | 0 | — | — | `TEAM-1EC33570FC87D455` |
| 1192 | Peppr AI | Peppr AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4B8BF42C870F5A09` |
| 1193 | PepsiCo | PepsiCo | 美国 | 0 | 0 | — | — | `TEAM-C4C2F6865E360D71` |
| 1194 | Perforce Software | Perforce Software | 美国 | 0 | 0 | — | — | `TEAM-3DBBB917F6E71288` |
| 1195 | Phase2 | Phase2 | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5EA2653F8B640972` |
| 1196 | Phonely | Phonely | 美国 | 0 | 0 | — | — | `TEAM-0C39340AA026AE3A` |
| 1197 | Phylo | Phylo | 美国 | 0 | 0 | — | — | `TEAM-2AC336E3377D95BC` |
| 1198 | Pilot Company | Pilot Company | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CC2D062DE05C7A3C` |
| 1199 | Pilotcrew AI | Pilotcrew AI | 美国 | 0 | 0 | — | — | `TEAM-58473A9EB5D0F0DB` |
| 1200 | Pipe17 | Pipe17 | 美国 | 0 | 0 | — | — | `TEAM-A3E360BA2668BC4B` |
| 1201 | RipperMercs / TensorFeed | Pizza Robot Studios LLC | 美国 | 0 | 0 | — | — | `TEAM-C72F1A4EF24F39E9` |
| 1202 | Planera | Planera | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9741280473BCD062` |
| 1203 | Plot Technologies, Inc. | Plot Technologies, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5829AF45C103F2C0` |
| 1204 | Plura AI | Plura AI | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-D7EA3C6BEB43A389` |
| 1205 | Pluto | Pluto | 美国 | 0 | 0 | — | — | `TEAM-B7C6B7F6BCE9699F` |
| 1206 | Poetiq | Poetiq | 美国 | 2 | 0 | — | 产品与设计 2 | `TEAM-EFDC8AFD0FEE1589` |
| 1207 | Pond & Company / Enercon Services | Pond & Company / Enercon Services | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-89E7CC9E7630FC64` |
| 1208 | Postman | Postman | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F101A6DC9BD315D9` |
| 1209 | Powder | Powder | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0D1F32A85B8D76AD` |
| 1210 | Praxis AI, Inc. | Praxis AI, Inc. | 美国 | 0 | 0 | — | — | `TEAM-016F068A93A55C0E` |
| 1211 | primitive | primitive | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BA3B43460A671406` |
| 1212 | Procter & Gamble / P&G | Procter & Gamble / P&G | 美国 | 1 | 0 | — | 算法、研究与模型 1 | `TEAM-8ABE19FB4EBC6481` |
| 1213 | Prodigal | Prodigal | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-AD88DD6EB20A7632` |
| 1214 | ProfitSolv | ProfitSolv | 美国 | 0 | 0 | — | — | `TEAM-CADBFA5A9286CE85` |
| 1215 | PromptLayer | PromptLayer | 美国 | 0 | 0 | — | — | `TEAM-28D7C58BEB5B31AE` |
| 1216 | Promptless | Promptless | 美国 | 0 | 0 | — | — | `TEAM-5887A6BE694A2E49` |
| 1217 | Prototyping.io | Prototyping.io | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-C3FA9D286FEB60EB` |
| 1218 | Prox | Prox | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E6E65262CDDBD790` |
| 1219 | Proximitty | Proximitty | 美国 | 0 | 0 | — | — | `TEAM-B5A6626D7B3AA8D5` |
| 1220 | PTP | PTP | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-63A4C2A5EA224033` |
| 1221 | PulsePoint | PulsePoint | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-05FDF0F0759F0D85` |
| 1222 | PwC US | PwC US | 美国 | 0 | 0 | — | — | `TEAM-FE83A45023E90A6C` |
| 1223 | Qualtrics | Qualtrics | 美国 | 0 | 0 | — | — | `TEAM-ADCF62B1461BCB0F` |
| 1224 | RamAIn | RamAIn | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-B28A014BA9A0FFEA` |
| 1225 | Rational | Rational | 美国 | 0 | 0 | — | — | `TEAM-F5DA0D268B964AD9` |
| 1226 | Re:Build Manufacturing / Reflow | Re:Build Manufacturing | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0B090027B508CC93` |
| 1227 | RealPact | RealPact | 美国 | 0 | 0 | — | — | `TEAM-B490754B8CBA12A5` |
| 1228 | Leadpages | Redbrick | 美国 | 0 | 0 | — | — | `TEAM-DC797C77B5618BFD` |
| 1229 | Redis | Redis | 美国 | 0 | 0 | — | — | `TEAM-CCB4B33574BF7179` |
| 1230 | Refactor | Refactor | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0FAF84AA06E01109` |
| 1231 | ReFiBuy, Inc. | ReFiBuy, Inc. | 美国 | 0 | 0 | — | — | `TEAM-2E3D6846B07FECA4` |
| 1232 | Reforged Labs | Reforged Labs | 美国 | 0 | 0 | — | — | `TEAM-FB94D189FBE2E1A2` |
| 1233 | Regal | Regal | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-A32BB80DFADE1A6F` |
| 1234 | Relari | Relari | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-2D72D66D258FE6F0` |
| 1235 | Relevance AI | Relevance AI | 美国 | 2 | 0 | — | 其他或边界岗位 2 | `TEAM-BD8C5A1932A48834` |
| 1236 | Renesas Electronics | Renesas Electronics | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-CF6ADCD824285DED` |
| 1237 | Renew Home | Renew Home | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-71F9C0B9FC3727A6` |
| 1238 | RentAHuman | RentAHuman | 美国 | 0 | 0 | — | — | `TEAM-5F0B671725D50B65` |
| 1239 | Replicas | Replicas | 美国 | 0 | 0 | — | — | `TEAM-33C949FF98FEFB71` |
| 1240 | Rescript | Rescript | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-8A65048DE05DF075` |
| 1241 | Resorius / 리소리우스 | Resorius / 리소리우스 | 美国 | 0 | 0 | — | — | `TEAM-8ED2C41CA7837F6B` |
| 1242 | Restate | Restate | 美国 | 0 | 0 | — | — | `TEAM-D06ABFE7EFAC7F25` |
| 1243 | Resultant | Resultant | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-58954907EFF3DA89` |
| 1244 | Revion | Revion | 美国 | 0 | 0 | — | — | `TEAM-9997587D5BE1DCE2` |
| 1245 | Revnu | Revnu | 美国 | 0 | 0 | — | — | `TEAM-9E1C7C48FBE89FA4` |
| 1246 | Revyl | Revyl | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-F71B02E220FAFF50` |
| 1247 | Rezolve.ai | Rezolve.ai | 美国 | 0 | 0 | — | — | `TEAM-96E2BF9F705B21A1` |
| 1248 | Ricursive Intelligence | Ricursive Intelligence | 美国 | 0 | 0 | — | — | `TEAM-AF53D6B682A43332` |
| 1249 | RightSeat.AI | RightSeat.AI | 美国 | 0 | 0 | — | — | `TEAM-2F18FA7EB21C9F26` |
| 1250 | Ripple | Ripple | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-1BB8C95796BC9070` |
| 1251 | Risotto | Risotto | 美国 | 0 | 0 | — | — | `TEAM-B7E28D77A7D52D45` |
| 1252 | Robby | Robby | 美国 | 0 | 0 | — | — | `TEAM-3DFC93D0A503DDDE` |
| 1253 | Rockhopper | Rockhopper | 美国 | 0 | 0 | — | — | `TEAM-D85DA82DD937430C` |
| 1254 | Rollio | Rollio | 美国 | 0 | 0 | — | — | `TEAM-13D2C9B604DB7B60` |
| 1255 | Rovi Health | Rovi Health | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0FA075D6B8D464C5` |
| 1256 | Rownd | Rownd | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3C030821DD3DFBA1` |
| 1257 | Ruma Care | Ruma Care | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6416B0B13DEC015A` |
| 1258 | Ryde Technologies, LLC | Ryde Technologies, LLC | 美国 | 0 | 0 | — | — | `TEAM-8D4B6C5880FA41DA` |
| 1259 | Saffron | Saffron | 美国 | 0 | 0 | — | — | `TEAM-D5CFD2B2B2A7ED92` |
| 1260 | Sage Care | Sage Care | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-ECB4E6693CF9EBC8` |
| 1261 | Sail Research | Sail Research | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-E0DB339349AFA382` |
| 1262 | Salesforce | Salesforce | 美国 | 0 | 0 | — | — | `TEAM-B84AE0D1C530C28C` |
| 1263 | Salus | Salus | 美国 | 0 | 0 | — | — | `TEAM-2C3F93DCD8129C02` |
| 1264 | Sandia National Laboratories | Sandia National Laboratories | 美国 | 0 | 0 | — | — | `TEAM-C42872DDDA90B26E` |
| 1265 | Sanity | Sanity | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-64725CA797277BBC` |
| 1266 | Saris AI | Saris AI | 美国 | 0 | 0 | — | — | `TEAM-019692BC2D1BA907` |
| 1267 | Scrapybara | Scrapybara | 美国 | 0 | 0 | — | — | `TEAM-B75F6F15DA842487` |
| 1268 | screenpipe | screenpipe | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-115C0A72563C9FC8` |
| 1269 | SDL / GovPilot ecosystem | SDL / GovPilot ecosystem | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0D21D5920364D353` |
| 1270 | Sekai | Sekai | 美国 | 0 | 0 | — | — | `TEAM-1C25079C7A062B39` |
| 1271 | SellScale | SellScale | 美国 | 0 | 0 | — | — | `TEAM-740915524E6E263B` |
| 1272 | Moveworks | ServiceNow | 美国 | 0 | 0 | — | — | `TEAM-431EEBA48C5B0A43` |
| 1273 | ServiceNow | ServiceNow | 美国 | 40 | 22 | 工程与应用开发 13；算法、研究与模型 5；产品与设计 2；安全、治理与合规 1；其他或边界岗位 1 | 工程与应用开发 16；其他或边界岗位 7；产品与设计 6；算法、研究与模型 6；安全、治理与合规 4；客户解决方案与交付 1 | `TEAM-EC30E55EE8695AA4` |
| 1274 | Sesame | Sesame | 美国 | 11 | 9 | 算法、研究与模型 4；平台、基础设施与数据 4；产品与设计 1 | 平台、基础设施与数据 5；算法、研究与模型 4；产品与设计 2 | `TEAM-8724C4A4142BAC41` |
| 1275 | Shepherd | Shepherd | 美国 | 1 | 1 | 运营、项目与职能 1 | 运营、项目与职能 1 | `TEAM-040324B34E9919E8` |
| 1276 | Shinsegae / Reflection AI | Shinsegae / Reflection AI | 美国 | 0 | 0 | — | — | `TEAM-4C19988EF5615FE2` |
| 1277 | Sia | Sia | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4BCA345BAA49C814` |
| 1278 | Siblings Software | Siblings Software | 美国 | 0 | 0 | — | — | `TEAM-62E0FE97B1FCCE03` |
| 1279 | Signature Aviation | Signature Aviation | 美国 | 1 | 1 | 运营、项目与职能 1 | 运营、项目与职能 1 | `TEAM-D48A27C103CA6B00` |
| 1280 | Simantic | Simantic | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-63421B3F0E754688` |
| 1281 | Simbie AI | Simbie AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0199681C006A2D79` |
| 1282 | Simile | Simile | 美国 | 0 | 0 | — | — | `TEAM-849A7059C3021354` |
| 1283 | Sixfold | Sixfold | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-81CE721AEB2006EF` |
| 1284 | Sixtyfour | Sixtyfour | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-919E2D77858477B0` |
| 1285 | Skai | Skai | 美国 | 0 | 0 | — | — | `TEAM-C40DF7BBBED84CD4` |
| 1286 | Skaled Consulting | Skaled Consulting | 美国 | 0 | 0 | — | — | `TEAM-477D0FF53E3607D0` |
| 1287 | Skit.ai | Skit.ai | 美国 | 0 | 0 | — | — | `TEAM-E626864C2EE7255F` |
| 1288 | Skypher | Skypher | 美国 | 0 | 0 | — | — | `TEAM-D73B9671E6D38BFB` |
| 1289 | Slalom, LLC | Slalom, LLC | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-44DB5B2D1F60D453` |
| 1290 | Slipstream IT | Slipstream IT | 美国 | 0 | 0 | — | — | `TEAM-AF4FD507F80C6E15` |
| 1291 | SmarterX Ventures, LLC | SmarterX Ventures, LLC | 美国 | 0 | 0 | — | — | `TEAM-597371A23CEDCD37` |
| 1292 | Software AG | Software AG | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5E4BD7BE00737BDF` |
| 1293 | Software Defined Automation | Software Defined Automation | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-0AB7AA339624B97C` |
| 1294 | Solum Health | Solum Health | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-A1CA9340F4CA9C58` |
| 1295 | Sourcebot | Sourcebot | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-BE8F243CBCCD2401` |
| 1296 | preloop / preloop | Spacecode.AI, Inc. | 美国 | 0 | 0 | — | — | `TEAM-DC6F6D77AB19A414` |
| 1297 | Spur | Spur | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D2DF1FA39240A80F` |
| 1298 | Spurs Sports & Entertainment | Spurs Sports & Entertainment | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D60073C052DEBA4D` |
| 1299 | SQDM | SQDM | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-E58087678B779B81` |
| 1300 | Squid AI | Squid Cloud, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6567779FA67E4257` |
| 1301 | St. Jude Children's Research Hospital | St. Jude Children's Research Hospital | 美国 | 1 | 0 | — | 安全、治理与合规 1 | `TEAM-C13B4E667A57DC54` |
| 1302 | Stage | Stage | 美国 | 0 | 0 | — | — | `TEAM-A9B3C163771F9E9F` |
| 1303 | Standout | Standout | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-FAC9728D96716411` |
| 1304 | StitchFin Inc. | StitchFin Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-ED9A5D9783C3F1F4` |
| 1305 | Strata Decision Technology | Strata Decision Technology | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5A34E0B37F3A7248` |
| 1306 | Structured AI | Structured AI | 美国 | 0 | 0 | — | — | `TEAM-18D3A2ACF689BA0D` |
| 1307 | Substrate | Substrate | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DD8D2025D2E97AEE` |
| 1308 | Sully.ai | Sully.ai | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-130C491599B86CF0` |
| 1309 | Super.com | Super.com | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0938544CB90CF5CB` |
| 1310 | Superconductor | Superconductor | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-27925BF6E4A7BE0D` |
| 1311 | Superset | Superset | 美国 | 0 | 0 | — | — | `TEAM-9E6B7AE15D237712` |
| 1312 | Sutherland | Sutherland | 美国 | 1 | 1 | 客户解决方案与交付 1 | 客户解决方案与交付 1 | `TEAM-E230AC04719BDE3D` |
| 1313 | Swap | Swap | 美国 | 0 | 0 | — | — | `TEAM-1E5D4E9177637481` |
| 1314 | SWARM Engineering | SWARM Engineering | 美国 | 0 | 0 | — | — | `TEAM-1570D7C0665E2392` |
| 1315 | Synphony | Synphony | 美国 | 0 | 0 | — | — | `TEAM-010F61421AEDE424` |
| 1316 | Synthio Labs | Synthio Labs | 美国 | 0 | 0 | — | — | `TEAM-9BBD1C103B66CE70` |
| 1317 | Tabnine | Tabnine | 美国 | 0 | 0 | — | — | `TEAM-3781821C7ADD684E` |
| 1318 | Talcott Financial Group | Talcott Financial Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-23946CFDBE8F1BFD` |
| 1319 | Taxbit | Taxbit | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-57799B4AC6B45F06` |
| 1320 | Tebra | Tebra | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-56E05C60970F21E9` |
| 1321 | Temper | Temper | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-162B81219CD88E4B` |
| 1322 | TesterArmy | TesterArmy | 美国 | 0 | 0 | — | — | `TEAM-843E82CA4FA5FBCA` |
| 1323 | The General Intelligence Company of New York | The General Intelligence Company of New York | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-AD2FB280FC7FBA37` |
| 1324 | The Hog | The Hog | 美国 | 0 | 0 | — | — | `TEAM-16F82F35D9D625C2` |
| 1325 | The Paper Store | The Paper Store | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D31214BFCDA8D152` |
| 1326 | The Trade Desk | The Trade Desk | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-D388021F1324F85D` |
| 1327 | Travelers | The Travelers Indemnity Company | 美国 | 1 | 0 | — | 产品与设计 1 | `TEAM-10D2DA7ACB9A13C3` |
| 1328 | Third Way Health | Third Way Health | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3D62ACD48A405148` |
| 1329 | Tiger Analytics Inc. | Tiger Analytics Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-52D7A1FAEEFEDE36` |
| 1330 | Titan AI | Titan AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4261A4F5AC15229A` |
| 1331 | Titan Holdings | Titan Holdings | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-CDA4FC6D90104FF7` |
| 1332 | Tivara | Tivara | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-40EE790590CDA6FC` |
| 1333 | Tolmo | Tolmo | 美国 | 0 | 0 | — | — | `TEAM-9973ECC00A7745F8` |
| 1334 | ToolJet | ToolJet Solutions, Inc. | 美国 | 0 | 0 | — | — | `TEAM-93152B2C94EB3F2D` |
| 1335 | Cognee / Topoteretes UG | Topoteretes UG (haftungsbeschraenkt) | 美国 | 0 | 0 | — | — | `TEAM-88A3922A420AB861` |
| 1336 | Cognee | Topoteretes UG (haftungsbeschränkt) | 美国 | 0 | 0 | — | — | `TEAM-246A1BD6B35A6871` |
| 1337 | Toshiba America Business Solutions, Inc. | Toshiba | 美国 | 0 | 0 | — | — | `TEAM-9B2FFF26ADA93E9D` |
| 1338 | TraceRoot.AI | TraceRoot.AI | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-87C0C3C8421FF53D` |
| 1339 | Trase Systems | Trase Systems | 美国 | 0 | 0 | — | — | `TEAM-0772C884A728885D` |
| 1340 | Tray.ai | Tray.ai | 美国 | 0 | 0 | — | — | `TEAM-6C0EB30F4B83F31D` |
| 1341 | Tread | Tread | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4E10FC2CCE55F077` |
| 1342 | Trellis | Trellis | 美国 | 0 | 0 | — | — | `TEAM-291FB386055B6BB2` |
| 1343 | TREND Health Partners | TREND Health Partners | 美国 | 0 | 0 | — | — | `TEAM-AD2454B91B2933CC` |
| 1344 | Trico Electric Cooperative, Inc. | Trico Electric Cooperative, Inc. | 美国 | 0 | 0 | — | — | `TEAM-D52CA1BF0EE7AC27` |
| 1345 | Trilagen | Trilagen | 美国 | 0 | 0 | — | — | `TEAM-C5AC901212D1D1DE` |
| 1346 | Trilon Group | Trilon Group | 美国 | 1 | 1 | 评测、测试与质量 1 | 评测、测试与质量 1 | `TEAM-6B962AB0D73F9138` |
| 1347 | Truewind | Truewind | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4C46D6823986F6B6` |
| 1348 | Truity Credit Union | Truity Credit Union | 美国 | 0 | 0 | — | — | `TEAM-A3926526DA8FBC54` |
| 1349 | Kompato AI | Trusting Social | 美国 | 0 | 0 | — | — | `TEAM-477FCCCAECF02CD7` |
| 1350 | Tsenta | Tsenta | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-51085C7FD8F13CC5` |
| 1351 | Twelve Labs / 트웰브랩스 | Twelve Labs / 트웰브랩스 | 美国 | 0 | 0 | — | — | `TEAM-207EFD4F6CD1D1CC` |
| 1352 | Uber | Uber | 美国 | 0 | 0 | — | — | `TEAM-CD5D3CFD68269F93` |
| 1353 | Udacity | Udacity | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-478E90CAAB0D4B76` |
| 1354 | UiPath Agentic Automation | UiPath | 美国 | 6 | 0 | — | 其他或边界岗位 6 | `TEAM-73B0E62F6BB10A9C` |
| 1355 | Ujwal Inc. / Level AI (attribution unresolved) | Ujwal Inc. / Level AI (attribution unresolved) | 美国 | 0 | 0 | — | — | `TEAM-5F40B7801E7FB502` |
| 1356 | Ultimate Knowledge Institute | Ultimate Knowledge Institute | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-317603D3C42A7491` |
| 1357 | Uniphore | Uniphore Technologies North America Inc | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-AB3F4D9F7369C318` |
| 1358 | United Global Technologies | United Global Technologies | 美国 | 0 | 0 | — | — | `TEAM-25BAA738D30CE0DE` |
| 1359 | United Placement Group | United Placement Group | 美国 | 0 | 0 | — | — | `TEAM-C196C09081D3FB2E` |
| 1360 | Optum Tech | UnitedHealth Group | 美国 | 0 | 0 | — | — | `TEAM-06BF6F337924443D` |
| 1361 | University of Wisconsin–Madison | Universities of Wisconsin | 美国 | 0 | 0 | — | — | `TEAM-C6ACA6BA52361640` |
| 1362 | First State AI Institute / University of Delaware | University of Delaware | 美国 | 0 | 0 | — | — | `TEAM-1ACFF315E0519C90` |
| 1363 | Unsiloed AI | Unsiloed AI | 美国 | 0 | 0 | — | — | `TEAM-94994EBFFDAECC7F` |
| 1364 | UpDoc | UpDoc | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0B077012D3864895` |
| 1365 | UpSmith | UpSmith | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DA9E7E1BBC9ABD2D` |
| 1366 | Oak Ridge National Laboratory (ORNL) | UT-Battelle | 美国 | 0 | 0 | — | — | `TEAM-93AE5C762E98183D` |
| 1367 | V7 | V7 | 美国 | 0 | 0 | — | — | `TEAM-7CADD3498F4B32F2` |
| 1368 | Vacatia | Vacatia | 美国 | 1 | 0 | — | 评测、测试与质量 1 | `TEAM-1C2A055280131EB0` |
| 1369 | Valiant Harbor International, LLC | Valiant Harbor International, LLC | 美国 | 0 | 0 | — | — | `TEAM-F527886F888C8ADB` |
| 1370 | Valitana LLC | Valitana LLC | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5135984845F89929` |
| 1371 | Variance | Variance | 美国 | 4 | 4 | 评测、测试与质量 2；产品与设计 2 | 评测、测试与质量 2；产品与设计 2 | `TEAM-D3013E330DB2EB98` |
| 1372 | Varos | Varos | 美国 | 0 | 0 | — | — | `TEAM-A40C5082F416921E` |
| 1373 | VAST Data | VAST Data | 美国 | 0 | 0 | — | — | `TEAM-C44D098C4236AC5A` |
| 1374 | Vector Legal | Vector Legal | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5A0A19CE1E2EB0C9` |
| 1375 | Vehlo | Vehlo | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-3574D33242823EB7` |
| 1376 | Vela | Vela | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-9B98BC4B264782A1` |
| 1377 | Ventus AI | Ventus AI | 美国 | 0 | 0 | — | — | `TEAM-DE151D947B84A65D` |
| 1378 | Vercel | Vercel | 美国 | 5 | 5 | 产品与设计 1；商务、市场与合作 1；客户解决方案与交付 1；工程与应用开发 1；其他或边界岗位 1 | 产品与设计 1；商务、市场与合作 1；客户解决方案与交付 1；工程与应用开发 1；其他或边界岗位 1 | `TEAM-CA3D9ABA45E7E193` |
| 1379 | Veritus | Veritus | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-6FA5F2BBDD968674` |
| 1380 | VeryAI / Veros Inc. | VeryAI / Veros Inc. | 美国 | 0 | 0 | — | — | `TEAM-137FEE2019DB4610` |
| 1381 | Vibranium Labs | Vibranium Labs | 美国 | 0 | 0 | — | — | `TEAM-6A7622716793404E` |
| 1382 | VikingCloud | VikingCloud | 美国 | 0 | 0 | — | — | `TEAM-E3BC17AEED7F084C` |
| 1383 | Visionary Integration Professionals | Visionary Integration Professionals | 美国 | 0 | 0 | — | — | `TEAM-047F8CD824103B7C` |
| 1384 | Vista Fulfillment Group | Vista Fulfillment Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-0BCB4B899F38568F` |
| 1385 | Voiceops | Voiceops | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-4CEF3E40D1538AFE` |
| 1386 | Voiceops, Inc. | Voiceops | 美国 | 0 | 0 | — | — | `TEAM-9EA46E740754BBF0` |
| 1387 | VoiceRun | VoiceRun | 美国 | 0 | 0 | — | — | `TEAM-3FC6A01CE9708981` |
| 1388 | VoltAgent | VoltAgent Inc. | 美国 | 0 | 0 | — | — | `TEAM-63F4796A7D2A5108` |
| 1389 | Vooma | Vooma | 美国 | 0 | 0 | — | — | `TEAM-4506472FBAF3DB03` |
| 1390 | Voquill | Voquill | 美国 | 0 | 0 | — | — | `TEAM-387FE8E6103D350D` |
| 1391 | VOYGR | VOYGR | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-344CBF0E9D443FDF` |
| 1392 | Vulcan Technologies | Vulcan Technologies | 美国 | 0 | 0 | — | — | `TEAM-A2793C43AA3EE227` |
| 1393 | Wato | Wato | 美国 | 0 | 0 | — | — | `TEAM-819D0A177B2B9CC8` |
| 1394 | Wellmark, Inc. | Wellmark, Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-12C3979F0086A08B` |
| 1395 | Wells Fargo | Wells Fargo | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-DBBBB19043303754` |
| 1396 | Westcore | Westcore | 美国 | 0 | 0 | — | — | `TEAM-46F212C780E9FD35` |
| 1397 | Western Digital | Western Digital | 美国 | 0 | 0 | — | — | `TEAM-27DB63E03DF5C23D` |
| 1398 | Wildcard | Wildcard | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5841E7B611D9A719` |
| 1399 | Wilmac Technologies | Wilmac Technologies | 美国 | 1 | 1 | 产品与设计 1 | 产品与设计 1 | `TEAM-C728FF2F2AD487B5` |
| 1400 | Wilson Sonsini Goodrich & Rosati | Wilson Sonsini Goodrich & Rosati | 美国 | 1 | 1 | 安全、治理与合规 1 | 安全、治理与合规 1 | `TEAM-9F15F4E9F11D8823` |
| 1401 | Windward Consulting | Windward Consulting | 美国 | 0 | 0 | — | — | `TEAM-E743ABB8DC19244E` |
| 1402 | Wipro Limited | Wipro Limited | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-142974405866D749` |
| 1403 | withQ / Quickserve AI Inc. | withQ / Quickserve AI Inc. | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-8820819DD1CA3445` |
| 1404 | Wolfia | Wolfia | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-5F9A0424F83D4586` |
| 1405 | Womble Bond Dickinson | Womble Bond Dickinson | 美国 | 0 | 0 | — | — | `TEAM-05B8CB7A0B503CD6` |
| 1406 | Workato | Workato | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-2B1B83989B194597` |
| 1407 | Workday | Workday | 美国 | 2 | 0 | — | 其他或边界岗位 2 | `TEAM-E4849ECB220AA5E4` |
| 1408 | World Bank Group | World Bank Group | 美国 | 0 | 0 | — | — | `TEAM-3B9BC10A7584659F` |
| 1409 | World Wide Technology | World Wide Technology | 美国 | 0 | 0 | — | — | `TEAM-FCBC732D691DD073` |
| 1410 | XBOW | XBOW | 美国 | 0 | 0 | — | — | `TEAM-E8FC6DC560E338BE` |
| 1411 | YouArt | YouArt | 美国 | 0 | 0 | — | — | `TEAM-9F38DEC24ED1E6D8` |
| 1412 | Yuma AI | Yuma AI | 美国 | 0 | 0 | — | — | `TEAM-DFBB30AEBE356FA9` |
| 1413 | Yutori | Yutori | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-735D0210A28030B8` |
| 1414 | Zania | Zania | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-49A81BBF084D625E` |
| 1415 | Zenity | Zenity | 美国 | 1 | 1 | 安全、治理与合规 1 | 安全、治理与合规 1 | `TEAM-7E3F6E18E032790D` |
| 1416 | ZeroPath | ZeroPath | 美国 | 1 | 0 | — | 工程与应用开发 1 | `TEAM-86AEB3F9A34CF98F` |
| 1417 | Zillow Group | Zillow Group | 美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-EF45994558C78C62` |
| 1418 | zudo.work | zudo.work | 美国 | 0 | 0 | — | — | `TEAM-BDB4136D2C307A22` |
| 1419 | Zuma | Zuma | 美国 | 1 | 1 | 工程与应用开发 1 | 工程与应用开发 1 | `TEAM-381882982FB7869E` |
| 1420 | Zylo | Zylo | 美国 | 1 | 0 | — | 平台、基础设施与数据 1 | `TEAM-3EEAFEF391FAED56` |
| 1421 | 合同会社Nonagon Capital | 合同会社Nonagon Capital | 美国 | 0 | 0 | — | — | `TEAM-776953521C97FAB6` |
| 1422 | AbbVie | AbbVie | 中国、美国 | 9 | 4 | 工程与应用开发 2；安全、治理与合规 1；客户解决方案与交付 1 | 工程与应用开发 5；客户解决方案与交付 2；安全、治理与合规 1；其他或边界岗位 1 | `TEAM-9C57045FA4FFB418` |
| 1423 | Microsoft | Microsoft | 中国、美国 | 1 | 0 | — | 其他或边界岗位 1 | `TEAM-B656B917C8BBBA70` |
| 1424 | Nagarro | Nagarro | 中国、美国 | 2 | 2 | 工程与应用开发 2 | 工程与应用开发 2 | `TEAM-0D4C26B19C72E699` |

## 如何更新本页

正式数据经过审核、全量重建和验证后，运行：

```bash
python3 scripts/build_team_role_overview.py
python3 scripts/build_team_role_overview.py --check
python3 scripts/validate_public_package.py --final
```

`--check` 只比较生成结果，不写文件。公开验证器也会执行同一检查，防止数据已更新而总览仍停留在旧版本。

## 限制

- 这是中国和美国公开来源的有界快照，不是绝对市场完整清单。
- 一条 Role 是一个标准化岗位记录，不是招聘名额或人数。
- 7,217 条安全证据索引可能包含产品页、招聘入口、过期记录或定位线索，不能用于推算当前岗位数。
- 派生岗位类别适合总览和导航，不替代岗位原始标题、原始岗位族标签或人工判断。
- 求职前应打开官方链接重新确认岗位状态、地点、资格和申请要求。
