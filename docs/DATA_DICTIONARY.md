# 字段和状态说明

## Evidence

Evidence 是一条公开来源观察的稳定索引。它可能只是产品页、公司招聘入口、第三方定位线索、过期记录或无法确认的信号。

因此：

- Evidence 行数不等于岗位数；
- Evidence 不自动代表岗位仍然开放；
- Evidence 不自动代表唯一公司、团队或岗位；
- Other/Global/Unknown Evidence 不进入本版本的标准化地图。

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

## Role 双语与地点派生字段

Role 仍只有一套正式记录。以下字段是同一记录中的确定性展示派生，不是第二套岗位事实：

- `role_display_version`：展示派生规则版本；
- `display_title_zh`：中文岗位方向显示；
- `display_title_en`：英文岗位方向显示；
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
