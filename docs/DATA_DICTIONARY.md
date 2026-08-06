# 字段和状态说明

## Evidence

Evidence 是一条公开来源观察的稳定索引。它可能只是产品页、公司招聘入口、第三方定位线索、过期记录或无法确认的信号。

因此：

- Evidence 行数不等于岗位数；
- Evidence 不自动代表岗位仍然开放；
- Evidence 不自动代表唯一公司、团队或岗位；
- Other/Global/Unknown Evidence 只有在官方标题、稳定岗位定位、组织归属和 Agent 相关性通过门时才会形成标准化岗位；其余仍保留为 Evidence/线索终态。

安全证据字段：

- `evidence_id`：稳定证据编号；
- `geography_bucket`：既有地域桶；
- `coverage_scope`：是否属于中美标准化范围；
- `organization_observed`：来源中观察到的组织或团队标签；
- `parent_organization_inferred`：已有集团归属判断，属于推导字段；
- `product_or_work_surface`：产品或工作面标签；
- `source_class`：粗粒度来源类别；
- `source_urls`：清理后的公开链接；
- `access_requirement`：访问是否需要登录；
- `observed_at`：证据观察日期；
- `evidence_grade`：A–E 证据等级；
- `public_excerpt`：允许公开的最短必要引文；
- `quote_publication_status`：引文公开或隐去状态；
- `limitations`：受控限制代码。

## 标准化对象

- Organization：集团或明确公司主体；
- Team：组织下的团队；
- Product：产品或工作面；
- Role：具体岗位；
- Relation：对象之间的关系。

每个对象都通过 `evidence_ids` 回到 Evidence。

## Role 岗位标题真实性、双语与地点字段

Role 仍只有一套正式记录。岗位标题与岗位类别严格分开：`role_family` 只表示阅读用类别，不能填入 `title` 或 `display_title_*`。

公开岗位列表只接收两种可信度：

- `public_confidence_tier=verified`：已核实岗位，标题、组织、官方来源和稳定岗位定位均通过完整门；
- `public_confidence_tier=probable`：高概率岗位，官方标题和稳定定位成立，但仍缺一项非核心事实；`eligible_for_strict_current` 必须为 `false`。

`recovery_origin` 区分 `existing_role_revalidated`（旧 Role 重新验收后保留）和
`unlinked_evidence_recovered`（从中美未转 Evidence 恢复）和
`global_deferred_evidence_recovered`（从全球冻结线索恢复）。待追溯线索不拥有公开岗位卡，也不计入 1,315 条岗位记录。

岗位标题真实性字段：

- `official_title_raw`：官方来源中的岗位标题原文；无法证明时为 `null`；
- `title_support_status`：`verified_official_title`、`verified_official_listing`、`pending_title_review`、`source_granularity_insufficient` 或 `disputed`；
- `title_source_url`：支持标题判断的官方来源；
- `title_source_granularity`：具体岗位详情、稳定岗位定位、普通列表、招聘总入口或未分类；
- `stable_role_locator`：岗位编号或稳定定位参数；
- `citation_supports_title`：该来源是否真的支持当前标题；
- `title_source_observed_at`：成功读取该来源并核对标题的日期；
- `title_source_recheck_performed`、`title_source_recheck_attempted_at`、`title_source_observation_status`：复核是否执行、时间和结果；
- `title_current_eligible_after_gate`：是否通过标题真实性 Current 门；
- `source_role_descriptor`：历史证据中的工作面描述，仅供溯源，不能当作岗位标题。

以下字段是同一记录中的双语和地点展示，不是第二套岗位事实：

- `role_display_version`：展示派生规则版本；
- `display_title_zh`：中文界面岗位标题；
- `display_title_en`：英文界面岗位标题；
- `display_location_zh`：中文地点显示；
- `display_location_en`：英文地点显示；
- `location_data_status`：地点数据状态；
- `work_arrangement`：办公方式；
- `work_arrangement_basis`：办公方式判断依据。

`location_data_status`：

- `normalized_or_descriptive`：已规范化或可安全描述；
- `official_role_title_location_reviewed`：已按官方岗位标题/详情定向复核；
- `company_or_context_only`：来源只支持公司、团队或上下文地点，不能当作岗位地点；
- `pending_review`：现有信息不足或含残片，地点待复核。

地点与办公方式严格分开。`display_location_zh/en` 不得包含招聘渠道、期限、岗位人数、法律页脚或其他来源说明。

`work_arrangement`：

- `onsite`：现场办公；
- `remote_or_hybrid`：远程或混合办公。

`work_arrangement_basis`：

- `explicit_remote_or_hybrid`：来源明确写明远程或混合；
- `explicit_onsite`：来源明确写明现场或驻场；
- `default_onsite_no_remote_signal`：来源未写远程或混合，按本项目规则默认现场。

最后一种是项目分类规则，不表示招聘方逐条明确声明现场办公。

## 当前岗位

当前岗位视图只允许：

- `current_verified`：有充分一手证据确认当前；
- `current_probable`：在冻结期限内、证据足够但仍保留边界。

此外必须同时满足：`public_confidence_tier=verified`、标题已核验、引用支持标题、来源为具体岗位页或带稳定岗位定位的官方列表、无需登录公开访问。高概率岗位和需要协助认证的岗位不能进入公开 Current；新恢复岗位只有逐项通过上述门才可进入。

以下状态不能进入当前岗位：

- `unknown`
- `stale`
- `blocked`
- `disputed`
- `duplicate`
- `superseded`
- `closed`

## 访问要求

- `public_no_login`：无需登录即可查看；
- `official_free_account`：官方免费账号后可查看；
- `user_assisted_auth`：需要用户协助认证；
- `paid_or_private_blocked`：付费或私人来源，不能进入当前岗位。

登录后可以验证，不等于可以复制或再发布正文。

## 时间

- `last_verified_at`：实际完成来源复核的日期，不是发布日期、截止日期或未来计划日期；
- 当前岗位复核期限为 14 天；
- 未来日期、缺失日期和超过期限的记录必须离开当前视图并进入复核。


## 存量岗位公开处置

每条公开 Role 都包含 `public_disposition`、`currentness_terminal`、`evidence_exhausted`、`public_is_current`、`currentness_next_check_at` 和 `decision_sha256`。默认 Current 只由 `969` 条 `publish_current` 组成；closed、blocked、disputed、exhausted unresolved 与相关性/标题失败只保留为非当前历史记录。
