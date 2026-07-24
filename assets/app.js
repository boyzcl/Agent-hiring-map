"use strict";

const DATA_PATHS = Object.freeze({
  metadata: "./data/metadata/release-metadata.json",
  organizations: "./data/map/organizations.jsonl",
  teams: "./data/map/teams.jsonl",
  products: "./data/map/products.jsonl",
  roles: "./data/map/roles.jsonl",
  current: "./data/current/current-opportunities.jsonl",
});

const I18N = Object.freeze({
  zh: Object.freeze({
    metaDescription: "基于公开来源、可追溯的中国与美国 Agent 岗位筛选地图。",
    pageTitle: "中美 Agent 岗位地图",
    skipToExplorer: "跳到岗位筛选",
    brandHomeLabel: "中美 Agent 岗位地图首页",
    brandSubtitle: "中美公开岗位地图",
    projectNavigation: "项目导航",
    navExplore: "筛选岗位",
    navOverview: "文本总览",
    languageSwitcherLabel: "界面语言",
    heroEyebrow: "中国 × 美国 · 公开来源",
    heroTitleLead: "找到真正和",
    heroTitleTail: "有关的工作。",
    heroLead: "从团队、岗位类别、地域和证据状态出发，筛选中国与美国公开来源中的 Agent 岗位。每条当前岗位都能回到官方来源。",
    startFiltering: "开始筛选",
    learnMethod: "了解方法与限制",
    importantDefinition: "重要口径",
    evidenceNotJobs: "证据行不是岗位数。",
    evidenceExplanation: "条安全证据索引用于溯源，可能包含产品页、招聘入口、过期记录或定位线索。",
    dataSummary: "数据概况",
    statCurrentLabel: "当前岗位",
    statCurrentNote: "默认检索范围",
    statRolesLabel: "地图岗位记录",
    statRolesNote: "不等于招聘人数",
    statTeamsLabel: "已收录团队",
    statTeamsNote: "包括当前岗位为 0",
    statActiveTeamsLabel: "有当前岗位的团队",
    statActiveTeamsNote: "按当前快照计算",
    explorerIndex: "02 · 探索岗位地图",
    explorerTitle: "筛选岗位，也看团队全貌",
    snapshotLabel: "数据快照：",
    loading: "载入中",
    autoUpdateNote: "页面随正式数据自动更新",
    viewSelector: "选择视图",
    jobsView: "岗位视图",
    jobsViewNote: "按具体岗位筛选",
    teamsView: "团队视图",
    teamsViewNote: "查看每个团队的岗位数",
    filterConditions: "筛选条件",
    searchLabel: "搜索",
    searchPlaceholder: "搜索岗位、组织、团队、产品或地点",
    scopeLabel: "数据范围",
    geographyLabel: "国家或地区",
    categoryLabel: "阅读用岗位类别",
    workArrangementLabel: "办公方式",
    evidenceGradeLabel: "证据等级",
    confidenceLabel: "岗位可信度",
    teamCurrentRolesLabel: "团队当前岗位",
    sortLabel: "排序",
    clearFilters: "清除筛选",
    loadingPublicData: "正在载入公开数据……",
    currentScopeNote: "仅显示官方岗位标题可核验，并通过当前性、日期、来源粒度和访问要求门的岗位。",
    allScopeNote: "展示已核实和高概率岗位；高概率岗位有独立标签，未进入当前视图不代表仍在招聘。",
    teamCurrentScopeNote: "团队列表保持完整；类别摘要按当前岗位计算。",
    teamAllScopeNote: "团队列表保持完整；类别摘要按全部地图岗位记录计算。",
    loadErrorTitle: "数据暂时无法载入",
    loadErrorFallback: "请稍后刷新页面，或从 GitHub 下载公开数据。",
    goToRepository: "前往 GitHub 仓库",
    paginationLabel: "结果分页",
    previousPage: "上一页",
    nextPage: "下一页",
    principlesIndex: "03 · 阅读须知",
    principlesTitle: "清楚知道这里有什么，也知道没有什么。",
    principleCurrentTitle: "当前不等于永久",
    principleCurrentBody: "页面展示的是有日期边界的公开快照。求职前仍应打开官方链接重新确认。",
    principleCountTitle: "记录不等于人数",
    principleCountBody: "一条标准化岗位记录不是招聘名额、在职人数或市场规模。",
    principleCategoryTitle: "类别用于阅读",
    principleCategoryBody: "高层类别由已有岗位族标签确定性生成，只用于筛选，不改写正式数据。",
    principleScopeTitle: "范围只有中美",
    principleScopeBody: "标准化地图和当前岗位只覆盖中国与美国，不代表其他地区没有相关岗位。",
    footerDescription: "中国与美国公开来源 P4 只读开源试点。",
    footerReadme: "项目说明",
    footerFields: "字段说明",
    footerSecurity: "安全政策",
    footerState: "无追踪 · 无登录 · 无业务写入",
    scopeCurrent: "当前岗位",
    scopeAll: "全部地图岗位记录",
    geographyAll: "中国和美国",
    geographyChina: "中国",
    geographyUnitedStates: "美国",
    filterAllCategories: "全部类别",
    arrangementAll: "全部办公方式",
    arrangementOnsite: "现场办公",
    arrangementRemoteHybrid: "远程或混合办公",
    gradeAll: "全部等级",
    gradeOption: "{grade}级",
    confidenceAll: "全部可信度",
    confidenceVerified: "已核实岗位",
    confidenceProbable: "高概率岗位",
    teamStateAll: "全部团队",
    teamStateActive: "有当前岗位",
    teamStateZero: "当前岗位为 0",
    sortVerified: "最后复核日期：由近到远",
    sortOrganization: "组织名称：正序",
    sortTeam: "团队名称：正序",
    sortCategory: "岗位类别：正序",
    sortCurrentCount: "当前岗位数：由多到少",
    sortMapCount: "地图岗位记录：由多到少",
    geographyBoth: "中国、美国",
    geographyUnknown: "未记录地域",
    organizationUnknown: "未解析组织",
    teamUnknown: "未解析团队",
    roleUntitled: "未命名岗位",
    teamUntitled: "未命名团队",
    teamProductUnknown: "未记录团队或产品",
    notRecorded: "未记录",
    currentRole: "当前岗位",
    notInCurrentView: "未进入当前岗位视图",
    workLocation: "工作地点",
    lastVerified: "最后复核",
    evidenceAndAccess: "证据与访问",
    titleAuthenticity: "岗位标题真实性",
    titleVerified: "官方具体岗位标题已核验",
    titleListingVerified: "官方稳定列表标题已核验",
    titlePending: "岗位标题待复核",
    titleSourceInsufficient: "来源粒度不足，不能证明具体岗位标题",
    titleDisputed: "岗位标题存在争议",
    sourceDirectRole: "官方具体岗位页",
    sourceStableListing: "带稳定岗位定位的官方列表",
    sourceGeneralEntry: "招聘总入口",
    sourceOfficialListing: "普通官方列表或路径",
    sourceUnclassified: "来源粒度未确认",
    openOfficialSource: "打开官方来源 ↗",
    noPublicRoleLink: "未公开岗位链接",
    arrangementOnsiteExplicit: "现场办公（来源明确）",
    arrangementOnsiteDefault: "现场办公（来源未标远程或混合）",
    arrangementRemoteHybridExplicit: "远程或混合办公（来源明确）",
    teamId: "团队编号",
    currentRoles: "当前岗位",
    mapRoleRecords: "地图岗位记录",
    noCurrentRoles: "当前岗位为 0",
    noMapRoles: "地图岗位记录为 0",
    emptyTitle: "没有符合条件的结果",
    emptyBody: "可以减少筛选条件、清除关键词，或切换到全部地图岗位记录。",
    pageStatus: "第 {page} / {pages} 页",
    jobsFound: "找到 {count} 个岗位",
    teamsFound: "找到 {count} 个团队",
    releaseMetadata: "发布元数据",
    organizationsData: "组织数据",
    teamsData: "团队数据",
    productsData: "产品数据",
    rolesData: "岗位数据",
    currentData: "当前岗位数据",
    invalidJsonLine: "{label}第 {line} 行不是合法数据。",
    loadFailed: "{label}载入失败（{status}）。",
    unknownError: "发生未知错误。",
    dataLoadFailed: "数据载入失败",
    categorySafety: "安全、治理与合规",
    categoryEvaluation: "评测、测试与质量",
    categoryProduct: "产品与设计",
    categoryBusiness: "商务、市场与合作",
    categorySolutions: "客户解决方案与交付",
    categoryOperations: "运营、项目与职能",
    categoryResearch: "算法、研究与模型",
    categoryPlatform: "平台、基础设施与数据",
    categoryEngineering: "工程与应用开发",
    categoryOther: "其他或边界岗位",
    accessPublic: "公开网页、无需登录",
    accessFreeAccount: "官方免费账号后可查看",
    accessAssisted: "需要用户协助认证",
    accessBlocked: "付费或私人来源",
    currentVerified: "已确认当前有效",
    currentProbable: "很可能当前有效",
    currentStale: "已过期、未重新确认",
    currentClosed: "已确认关闭",
    currentDisputed: "存在争议",
  }),
  en: Object.freeze({
    metaDescription: "A traceable public-source map of Agent roles in China and the United States.",
    pageTitle: "China–United States Agent Hiring Map",
    skipToExplorer: "Skip to role filters",
    brandHomeLabel: "Agent Hiring Map home",
    brandSubtitle: "China–United States public role map",
    projectNavigation: "Project navigation",
    navExplore: "Explore roles",
    navOverview: "Text overview",
    languageSwitcherLabel: "Interface language",
    heroEyebrow: "China × United States · Public sources",
    heroTitleLead: "Find work truly about",
    heroTitleTail: "roles.",
    heroLead: "Filter public-source Agent roles in China and the United States by team, role category, geography, and evidence status. Every current role links back to an official source.",
    startFiltering: "Start filtering",
    learnMethod: "Method and limitations",
    importantDefinition: "Important definition",
    evidenceNotJobs: "Evidence rows are not job counts.",
    evidenceExplanation: "safe evidence records support traceability and may include product pages, career entry points, expired records, or locator leads.",
    dataSummary: "Data summary",
    statCurrentLabel: "Current roles",
    statCurrentNote: "Default search scope",
    statRolesLabel: "Map role records",
    statRolesNote: "Not hiring headcount",
    statTeamsLabel: "Teams included",
    statTeamsNote: "Includes teams with zero current roles",
    statActiveTeamsLabel: "Teams with current roles",
    statActiveTeamsNote: "Calculated from this snapshot",
    explorerIndex: "02 · Explore the hiring map",
    explorerTitle: "Filter roles and see the full team landscape",
    snapshotLabel: "Data snapshot:",
    loading: "Loading",
    autoUpdateNote: "The page updates with approved data",
    viewSelector: "Select a view",
    jobsView: "Role view",
    jobsViewNote: "Filter individual roles",
    teamsView: "Team view",
    teamsViewNote: "See role counts for every team",
    filterConditions: "Filter conditions",
    searchLabel: "Search",
    searchPlaceholder: "Search roles, organizations, teams, products, or locations",
    scopeLabel: "Data scope",
    geographyLabel: "Country or region",
    categoryLabel: "Reading category",
    workArrangementLabel: "Work arrangement",
    evidenceGradeLabel: "Evidence grade",
    confidenceLabel: "Role confidence",
    teamCurrentRolesLabel: "Team current-role status",
    sortLabel: "Sort",
    clearFilters: "Clear filters",
    loadingPublicData: "Loading public data…",
    currentScopeNote: "Only roles with a verifiable official title that pass currentness, date, source-granularity, and access gates are shown.",
    allScopeNote: "Shows verified and probable roles. Probable roles are labeled, and records outside Current are not necessarily still hiring.",
    teamCurrentScopeNote: "The team list stays complete; category summaries use current roles.",
    teamAllScopeNote: "The team list stays complete; category summaries use all map role records.",
    loadErrorTitle: "Data is temporarily unavailable",
    loadErrorFallback: "Refresh later or download the public data from GitHub.",
    goToRepository: "Open the GitHub repository",
    paginationLabel: "Result pages",
    previousPage: "Previous",
    nextPage: "Next",
    principlesIndex: "03 · How to read this map",
    principlesTitle: "Know what is here—and what is not.",
    principleCurrentTitle: "Current is not permanent",
    principleCurrentBody: "This page is a dated public-source snapshot. Recheck the official source before applying.",
    principleCountTitle: "Records are not headcount",
    principleCountBody: "A normalized role record is not an opening count, employee count, or market-size estimate.",
    principleCategoryTitle: "Categories aid reading",
    principleCategoryBody: "High-level categories are derived deterministically from existing role-family labels and do not rewrite formal data.",
    principleScopeTitle: "The map is bounded to two countries",
    principleScopeBody: "The canonical map and current role view cover China and the United States only. Other regions may also have relevant roles.",
    footerDescription: "China and United States public-source P4 read-only open-source pilot.",
    footerReadme: "Project guide",
    footerFields: "Field guide",
    footerSecurity: "Security policy",
    footerState: "No tracking · No login · No business writes",
    scopeCurrent: "Current roles",
    scopeAll: "All map role records",
    geographyAll: "China and the United States",
    geographyChina: "China",
    geographyUnitedStates: "United States",
    filterAllCategories: "All categories",
    arrangementAll: "All work arrangements",
    arrangementOnsite: "On-site",
    arrangementRemoteHybrid: "Remote or hybrid",
    gradeAll: "All grades",
    gradeOption: "Grade {grade}",
    confidenceAll: "All confidence tiers",
    confidenceVerified: "Verified role",
    confidenceProbable: "Probable role",
    teamStateAll: "All teams",
    teamStateActive: "Has current roles",
    teamStateZero: "Zero current roles",
    sortVerified: "Last verified: newest first",
    sortOrganization: "Organization: A–Z",
    sortTeam: "Team: A–Z",
    sortCategory: "Role category: A–Z",
    sortCurrentCount: "Current roles: high to low",
    sortMapCount: "Map role records: high to low",
    geographyBoth: "China and the United States",
    geographyUnknown: "Geography not recorded",
    organizationUnknown: "Organization unresolved",
    teamUnknown: "Team unresolved",
    roleUntitled: "Untitled role",
    teamUntitled: "Untitled team",
    teamProductUnknown: "Team or product not recorded",
    notRecorded: "Not recorded",
    currentRole: "Current role",
    notInCurrentView: "Outside the current role view",
    workLocation: "Work location",
    lastVerified: "Last verified",
    evidenceAndAccess: "Evidence and access",
    titleAuthenticity: "Role-title authenticity",
    titleVerified: "Verified official role-detail title",
    titleListingVerified: "Verified title at a stable official listing locator",
    titlePending: "Role title pending review",
    titleSourceInsufficient: "Source is too broad to prove a specific role title",
    titleDisputed: "Role title is disputed",
    sourceDirectRole: "Official role-detail page",
    sourceStableListing: "Official listing with a stable role locator",
    sourceGeneralEntry: "General recruiting entry",
    sourceOfficialListing: "General official listing or path",
    sourceUnclassified: "Source granularity unconfirmed",
    openOfficialSource: "Open official source ↗",
    noPublicRoleLink: "No public role link",
    arrangementOnsiteExplicit: "On-site (explicitly stated by source)",
    arrangementOnsiteDefault: "On-site (default; source does not state remote or hybrid)",
    arrangementRemoteHybridExplicit: "Remote or hybrid (explicitly stated by source)",
    teamId: "Team ID",
    currentRoles: "Current roles",
    mapRoleRecords: "Map role records",
    noCurrentRoles: "Zero current roles",
    noMapRoles: "Zero map role records",
    emptyTitle: "No results match these filters",
    emptyBody: "Use fewer filters, clear the search term, or switch to all map role records.",
    pageStatus: "Page {page} of {pages}",
    jobsFound: "{count} roles found",
    teamsFound: "{count} teams found",
    releaseMetadata: "release metadata",
    organizationsData: "organization data",
    teamsData: "team data",
    productsData: "product data",
    rolesData: "role data",
    currentData: "current-role data",
    invalidJsonLine: "Line {line} of {label} is not valid data.",
    loadFailed: "Failed to load {label} ({status}).",
    unknownError: "An unknown error occurred.",
    dataLoadFailed: "Data failed to load",
    categorySafety: "Safety, governance, and compliance",
    categoryEvaluation: "Evaluation, testing, and quality",
    categoryProduct: "Product and design",
    categoryBusiness: "Business, marketing, and partnerships",
    categorySolutions: "Customer solutions and delivery",
    categoryOperations: "Operations, programs, and functions",
    categoryResearch: "Algorithms, research, and models",
    categoryPlatform: "Platform, infrastructure, and data",
    categoryEngineering: "Engineering and application development",
    categoryOther: "Other or boundary roles",
    accessPublic: "Public page; no login",
    accessFreeAccount: "Visible with a free official account",
    accessAssisted: "User-assisted authentication required",
    accessBlocked: "Paid or private source",
    currentVerified: "Verified current",
    currentProbable: "Probably current",
    currentStale: "Stale and not reverified",
    currentClosed: "Verified closed",
    currentDisputed: "Disputed",
  }),
});

const CATEGORY_DEFINITIONS = Object.freeze([
  Object.freeze({ id: "safety", label: "categorySafety", keywords: ["security", "safety", "governance", "compliance", "risk", "trust", "identity", "policy", "secure", "安全", "治理", "合规"] }),
  Object.freeze({ id: "evaluation", label: "categoryEvaluation", keywords: ["evaluation", "eval", "test", "quality", "observability", "benchmark", "red_team", "red team", "评测", "测试", "质量"] }),
  Object.freeze({ id: "product", label: "categoryProduct", keywords: ["product", "design", "designer", "ux", "ui", "产品", "设计"] }),
  Object.freeze({ id: "business", label: "categoryBusiness", keywords: ["gtm", "sales", "marketing", "commercial", "partnership", "partner", "business_development", "business development", "growth", "account executive", "销售", "市场", "商务", "合作"] }),
  Object.freeze({ id: "solutions", label: "categorySolutions", keywords: ["solution", "solutions", "forward_deployed", "forward deployed", "fde", "delivery", "implementation", "customer", "adoption", "consult", "architect", "support", "解决方案", "交付", "客户", "架构"] }),
  Object.freeze({ id: "operations", label: "categoryOperations", keywords: ["operations", "operation", "program", "project", "recruit", "talent", "strategy", "human_resources", "human resources", "finance", "legal", "chief_of_staff", "chief of staff", "运营", "项目", "招聘", "战略"] }),
  Object.freeze({ id: "research", label: "categoryResearch", keywords: ["research", "scientist", "algorithm", "training", "post_training", "post-training", "model", "machine_learning", "machine learning", "reinforcement", "reasoning", "alignment", "算法", "研究", "训练", "模型"] }),
  Object.freeze({ id: "platform", label: "categoryPlatform", keywords: ["platform", "infra", "infrastructure", "orchestration", "data", "backend", "cloud", "devops", "sre", "database", "distributed", "systems", "rag", "retrieval", "context", "平台", "基础设施", "数据", "后端"] }),
  Object.freeze({ id: "engineering", label: "categoryEngineering", keywords: ["engineer", "engineering", "developer", "application", "full_stack", "full stack", "frontend", "software", "coding", "开发", "工程"] }),
  Object.freeze({ id: "other", label: "categoryOther", keywords: [] }),
]);

const CATEGORY_BY_ID = new Map(
  CATEGORY_DEFINITIONS.map((definition) => [definition.id, definition]),
);
const CATEGORY_ORDER = Object.freeze(
  CATEGORY_DEFINITIONS.map((definition) => definition.id),
);
const LEGACY_CATEGORY_IDS = new Map(
  CATEGORY_DEFINITIONS.map((definition) => [
    I18N.zh[definition.label],
    definition.id,
  ]),
);

const ACCESS_LABEL_KEYS = Object.freeze({
  public_no_login: "accessPublic",
  official_free_account: "accessFreeAccount",
  user_assisted_auth: "accessAssisted",
  paid_or_private_blocked: "accessBlocked",
});

const CURRENTNESS_LABEL_KEYS = Object.freeze({
  current_verified: "currentVerified",
  current_probable: "currentProbable",
  stale_unverified: "currentStale",
  closed_verified: "currentClosed",
  disputed: "currentDisputed",
});

const TITLE_SUPPORT_LABEL_KEYS = Object.freeze({
  verified_official_title: "titleVerified",
  verified_official_listing: "titleListingVerified",
  pending_title_review: "titlePending",
  source_granularity_insufficient: "titleSourceInsufficient",
  disputed: "titleDisputed",
});

const TITLE_SOURCE_LABEL_KEYS = Object.freeze({
  direct_role_detail: "sourceDirectRole",
  stable_official_listing_locator: "sourceStableListing",
  general_recruiting_entry: "sourceGeneralEntry",
  official_listing_or_slug: "sourceOfficialListing",
  unclassified: "sourceUnclassified",
});

const PAGE_SIZE = Object.freeze({ jobs: 24, teams: 30 });

const state = {
  lang: "zh",
  view: "jobs",
  scope: "current",
  query: "",
  geography: "all",
  category: "all",
  remote: "all",
  grade: "all",
  confidence: "all",
  teamState: "all",
  sort: "verified_desc",
  page: 1,
};

const store = {
  metadata: null,
  jobs: [],
  teams: [],
  loaded: false,
};

const elements = {};

function t(key, values = {}) {
  const template = I18N[state.lang][key] ?? I18N.zh[key] ?? key;
  return Object.entries(values).reduce(
    (output, [name, value]) =>
      output.replaceAll(`{${name}}`, String(value)),
    template,
  );
}

function locale() {
  return state.lang === "zh" ? "zh-CN" : "en-US";
}

function collator() {
  return new Intl.Collator(locale(), {
    numeric: true,
    sensitivity: "base",
  });
}

function parseJsonLines(text, label) {
  const rows = [];
  for (const [index, line] of text.split(/\r?\n/u).entries()) {
    if (!line.trim()) continue;
    try {
      rows.push(JSON.parse(line));
    } catch {
      throw new Error(t("invalidJsonLine", { label, line: index + 1 }));
    }
  }
  return rows;
}

async function fetchJson(path, label) {
  const response = await fetch(path, { credentials: "same-origin" });
  if (!response.ok) {
    throw new Error(t("loadFailed", { label, status: response.status }));
  }
  return response.json();
}

async function fetchJsonLines(path, label) {
  const response = await fetch(path, { credentials: "same-origin" });
  if (!response.ok) {
    throw new Error(t("loadFailed", { label, status: response.status }));
  }
  return parseJsonLines(await response.text(), label);
}

function roleCategory(role) {
  const categoryText = String(
    role.role_family || role.title || "",
  ).toLocaleLowerCase();
  for (const definition of CATEGORY_DEFINITIONS) {
    if (
      definition.id !== "other" &&
      definition.keywords.some((keyword) => categoryText.includes(keyword))
    ) {
      return definition.id;
    }
  }
  return "other";
}

function categoryLabel(categoryId) {
  const definition = CATEGORY_BY_ID.get(categoryId);
  return definition ? t(definition.label) : t("categoryOther");
}

function geographyValues(team, current) {
  if (current?.geography) return [current.geography];
  return Array.isArray(team?.team_geography) ? team.team_geography : [];
}

function geographyLabel(values) {
  const hasChina = values.includes("China");
  const hasUnitedStates = values.includes("United States");
  if (hasChina && hasUnitedStates) return t("geographyBoth");
  if (hasChina) return t("geographyChina");
  if (hasUnitedStates) return t("geographyUnitedStates");
  return t("geographyUnknown");
}

function compactText(values) {
  return values
    .filter(Boolean)
    .map((value) => String(value).trim())
    .filter(Boolean)
    .join(" · ");
}

function safePublicUrl(value) {
  if (!value) return null;
  try {
    const url = new URL(value);
    return ["http:", "https:"].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
}

function countCategories(jobs) {
  const counts = new Map();
  for (const job of jobs) {
    counts.set(job.category, (counts.get(job.category) || 0) + 1);
  }
  return counts;
}

function buildStore(raw) {
  const organizationById = new Map(
    raw.organizations.map((row) => [row.organization_id, row]),
  );
  const teamById = new Map(raw.teams.map((row) => [row.team_id, row]));
  const productById = new Map(raw.products.map((row) => [row.product_id, row]));
  const currentByRoleId = new Map(
    raw.current.map((row) => [row.role_id, row]),
  );

  const jobs = raw.roles.map((role) => {
    const current = currentByRoleId.get(role.role_id) || null;
    const organization = organizationById.get(role.organization_id) || null;
    const team = teamById.get(role.team_id) || null;
    const product = productById.get(role.product_id) || null;
    const geographies = geographyValues(team, current);
    const sourceCandidate =
      role.title_source_url ||
      current?.title_source_url ||
      current?.source_urls?.[0] ||
      role.official_role_url ||
      null;
    const category = roleCategory(role);
    const organizationName =
      organization?.canonical_name || t("organizationUnknown");
    const teamName = team?.team_name || t("teamUnknown");
    const productName = product?.name || "";
    const titleZh = role.display_title_zh || role.title || t("roleUntitled");
    const titleEn = role.display_title_en || role.title || t("roleUntitled");
    const locationZh = role.display_location_zh || I18N.zh.notRecorded;
    const locationEn = role.display_location_en || I18N.en.notRecorded;
    const searchText = compactText([
      role.title,
      titleZh,
      titleEn,
      role.role_family,
      organizationName,
      teamName,
      productName,
      I18N.zh[CATEGORY_BY_ID.get(category)?.label],
      I18N.en[CATEGORY_BY_ID.get(category)?.label],
      locationZh,
      locationEn,
    ]).toLocaleLowerCase();

    return {
      id: role.role_id,
      titleZh,
      titleEn,
      roleFamily: role.role_family || "",
      organizationName,
      teamName,
      productName,
      teamId: role.team_id,
      category,
      locationZh,
      locationEn,
      locationDataStatus: role.location_data_status,
      workArrangement: role.work_arrangement,
      workArrangementBasis: role.work_arrangement_basis,
      geographies,
      evidenceGrade:
        current?.evidence_grade || role.evidence_grade || t("notRecorded"),
      confidenceTier: role.public_confidence_tier || "probable",
      accessRequirement:
        current?.access_requirement ||
        role.access_requirement ||
        t("notRecorded"),
      currentnessStatus: role.currentness_status || "",
      lastVerifiedAt:
        current?.last_verified_at ||
        role.title_source_observed_at ||
        role.last_verified_at ||
        "",
      titleSupportStatus: role.title_support_status || "pending_title_review",
      titleSourceGranularity:
        role.title_source_granularity || "unclassified",
      isCurrent: Boolean(current),
      sourceUrl: safePublicUrl(sourceCandidate),
      searchText,
    };
  });

  const jobsByTeam = new Map();
  for (const job of jobs) {
    if (!jobsByTeam.has(job.teamId)) jobsByTeam.set(job.teamId, []);
    jobsByTeam.get(job.teamId).push(job);
  }

  const teams = raw.teams.map((team) => {
    const organization = organizationById.get(team.organization_id) || null;
    const teamJobs = jobsByTeam.get(team.team_id) || [];
    const currentJobs = teamJobs.filter((job) => job.isCurrent);
    const allCategoryCounts = countCategories(teamJobs);
    const currentCategoryCounts = countCategories(currentJobs);
    const organizationName =
      organization?.canonical_name || t("organizationUnknown");
    const searchText = compactText([
      team.team_name,
      organizationName,
      team.team_id,
      ...allCategoryCounts.keys(),
      ...[...allCategoryCounts.keys()].map((category) =>
        I18N.zh[CATEGORY_BY_ID.get(category)?.label]),
      ...[...allCategoryCounts.keys()].map((category) =>
        I18N.en[CATEGORY_BY_ID.get(category)?.label]),
    ]).toLocaleLowerCase();

    return {
      id: team.team_id,
      name: team.team_name || t("teamUntitled"),
      organizationName,
      geographies: team.team_geography || [],
      mapRoleCount: teamJobs.length,
      currentRoleCount: currentJobs.length,
      allCategoryCounts,
      currentCategoryCounts,
      searchText,
    };
  });

  store.metadata = raw.metadata;
  store.jobs = jobs;
  store.teams = teams;
  store.loaded = true;
}

function formatNumber(value) {
  return new Intl.NumberFormat(locale()).format(Number(value) || 0);
}

function formatDate(value) {
  if (!value) return t("notRecorded");
  const parsed = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(parsed.getTime())) return value;
  return new Intl.DateTimeFormat(locale(), {
    year: "numeric",
    month: state.lang === "zh" ? "numeric" : "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(parsed);
}

function setText(element, value) {
  element.textContent = String(value);
}

function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) setText(element, text);
  return element;
}

function appendChip(parent, text, variant = "") {
  const chip = createElement("span", `chip ${variant}`.trim(), text);
  parent.append(chip);
  return chip;
}

function setOptions(element, options) {
  element.replaceChildren();
  for (const [value, label] of options) {
    const option = document.createElement("option");
    option.value = value;
    setText(option, label);
    element.append(option);
  }
}

function bindElements() {
  const ids = [
    "meta-description",
    "lang-zh",
    "lang-en",
    "evidence-count",
    "stat-current",
    "stat-roles",
    "stat-teams",
    "stat-active-teams",
    "release-date",
    "tab-jobs",
    "tab-teams",
    "filter-query",
    "filter-scope",
    "filter-geography",
    "filter-category",
    "filter-remote",
    "filter-grade",
    "filter-confidence",
    "filter-team-state",
    "filter-sort",
    "reset-filters",
    "result-status",
    "scope-note",
    "error-panel",
    "error-message",
    "results",
    "pagination",
    "previous-page",
    "next-page",
    "page-status",
  ];
  for (const id of ids) elements[id] = document.getElementById(id);
  elements.jobOnly = [...document.querySelectorAll(".job-only")];
  elements.teamOnly = [...document.querySelectorAll(".team-only")];
}

function populateFilterOptions() {
  setOptions(elements["filter-scope"], [
    ["current", t("scopeCurrent")],
    ["all", t("scopeAll")],
  ]);
  setOptions(elements["filter-geography"], [
    ["all", t("geographyAll")],
    ["China", t("geographyChina")],
    ["United States", t("geographyUnitedStates")],
  ]);
  setOptions(elements["filter-category"], [
    ["all", t("filterAllCategories")],
    ...CATEGORY_DEFINITIONS.map((definition) => [
      definition.id,
      t(definition.label),
    ]),
  ]);
  setOptions(elements["filter-remote"], [
    ["all", t("arrangementAll")],
    ["onsite", t("arrangementOnsite")],
    ["remote_or_hybrid", t("arrangementRemoteHybrid")],
  ]);
  setOptions(elements["filter-grade"], [
    ["all", t("gradeAll")],
    ...["A", "B", "C", "E"].map((grade) => [
      grade,
      t("gradeOption", { grade }),
    ]),
  ]);
  setOptions(elements["filter-confidence"], [
    ["all", t("confidenceAll")],
    ["verified", t("confidenceVerified")],
    ["probable", t("confidenceProbable")],
  ]);
  setOptions(elements["filter-team-state"], [
    ["all", t("teamStateAll")],
    ["active", t("teamStateActive")],
    ["zero", t("teamStateZero")],
  ]);
}

function sortOptionsForView() {
  const options =
    state.view === "jobs"
      ? [
          ["verified_desc", t("sortVerified")],
          ["organization_asc", t("sortOrganization")],
          ["team_asc", t("sortTeam")],
          ["category_asc", t("sortCategory")],
        ]
      : [
          ["current_desc", t("sortCurrentCount")],
          ["map_desc", t("sortMapCount")],
          ["organization_asc", t("sortOrganization")],
          ["team_asc", t("sortTeam")],
        ];
  setOptions(elements["filter-sort"], options);
  if (!options.some(([value]) => value === state.sort)) {
    state.sort = options[0][0];
  }
  elements["filter-sort"].value = state.sort;
}

function applyTranslations() {
  document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
  document.title = t("pageTitle");
  elements["meta-description"].content = t("metaDescription");
  for (const element of document.querySelectorAll("[data-i18n]")) {
    setText(element, t(element.dataset.i18n));
  }
  for (const element of document.querySelectorAll("[data-i18n-placeholder]")) {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  }
  for (const element of document.querySelectorAll("[data-i18n-aria-label]")) {
    element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
  }
  elements["lang-zh"].setAttribute("aria-pressed", String(state.lang === "zh"));
  elements["lang-en"].setAttribute("aria-pressed", String(state.lang === "en"));
  document.querySelector(".brand").href = `?lang=${state.lang}`;
  populateFilterOptions();
}

function updateSummary() {
  const activeTeams = store.teams.filter(
    (team) => team.currentRoleCount > 0,
  ).length;
  setText(elements["evidence-count"], formatNumber(store.metadata.evidence_rows));
  setText(
    elements["stat-current"],
    formatNumber(store.jobs.filter((job) => job.isCurrent).length),
  );
  setText(elements["stat-roles"], formatNumber(store.jobs.length));
  setText(elements["stat-teams"], formatNumber(store.teams.length));
  setText(elements["stat-active-teams"], formatNumber(activeTeams));
  setText(
    elements["release-date"],
    formatDate(store.metadata.release_as_of),
  );
  elements["release-date"].dateTime = store.metadata.release_as_of || "";
}

function applyStateToControls() {
  elements["filter-query"].value = state.query;
  elements["filter-scope"].value = state.scope;
  elements["filter-geography"].value = state.geography;
  elements["filter-category"].value = state.category;
  elements["filter-remote"].value = state.remote;
  elements["filter-grade"].value = state.grade;
  elements["filter-confidence"].value = state.confidence;
  elements["filter-team-state"].value = state.teamState;
  elements["tab-jobs"].classList.toggle("is-active", state.view === "jobs");
  elements["tab-teams"].classList.toggle("is-active", state.view === "teams");
  elements["tab-jobs"].setAttribute(
    "aria-selected",
    String(state.view === "jobs"),
  );
  elements["tab-teams"].setAttribute(
    "aria-selected",
    String(state.view === "teams"),
  );
  elements.results.setAttribute(
    "aria-labelledby",
    state.view === "jobs" ? "tab-jobs" : "tab-teams",
  );
  for (const element of elements.jobOnly) {
    element.hidden = state.view !== "jobs";
  }
  for (const element of elements.teamOnly) {
    element.hidden = state.view !== "teams";
  }
  sortOptionsForView();
}

function normalizeQuery(value) {
  return value.trim().toLocaleLowerCase();
}

function geographyMatches(values) {
  return state.geography === "all" || values.includes(state.geography);
}

function filteredJobs() {
  const query = normalizeQuery(state.query);
  const rows = store.jobs.filter((job) => {
    if (state.scope === "current" && !job.isCurrent) return false;
    if (!geographyMatches(job.geographies)) return false;
    if (state.category !== "all" && job.category !== state.category) return false;
    if (state.remote !== "all" && job.workArrangement !== state.remote) {
      return false;
    }
    if (state.grade !== "all" && job.evidenceGrade !== state.grade) return false;
    if (
      state.confidence !== "all" &&
      job.confidenceTier !== state.confidence
    ) return false;
    if (query && !job.searchText.includes(query)) return false;
    return true;
  });

  const compare = collator().compare;
  rows.sort((left, right) => {
    if (state.sort === "organization_asc") {
      return (
        compare(left.organizationName, right.organizationName) ||
        compare(displayTitle(left), displayTitle(right))
      );
    }
    if (state.sort === "team_asc") {
      return (
        compare(left.teamName, right.teamName) ||
        compare(displayTitle(left), displayTitle(right))
      );
    }
    if (state.sort === "category_asc") {
      return (
        CATEGORY_ORDER.indexOf(left.category) -
          CATEGORY_ORDER.indexOf(right.category) ||
        compare(displayTitle(left), displayTitle(right))
      );
    }
    return (
      String(right.lastVerifiedAt).localeCompare(String(left.lastVerifiedAt)) ||
      compare(left.organizationName, right.organizationName) ||
      compare(displayTitle(left), displayTitle(right))
    );
  });
  return rows;
}

function categoriesForTeam(team) {
  return state.scope === "current"
    ? team.currentCategoryCounts
    : team.allCategoryCounts;
}

function filteredTeams() {
  const query = normalizeQuery(state.query);
  const rows = store.teams.filter((team) => {
    if (!geographyMatches(team.geographies)) return false;
    if (state.teamState === "active" && team.currentRoleCount === 0) return false;
    if (state.teamState === "zero" && team.currentRoleCount > 0) return false;
    if (
      state.category !== "all" &&
      !categoriesForTeam(team).has(state.category)
    ) {
      return false;
    }
    if (query && !team.searchText.includes(query)) return false;
    return true;
  });

  const compare = collator().compare;
  rows.sort((left, right) => {
    if (state.sort === "map_desc") {
      return (
        right.mapRoleCount - left.mapRoleCount ||
        compare(left.organizationName, right.organizationName)
      );
    }
    if (state.sort === "organization_asc") {
      return (
        compare(left.organizationName, right.organizationName) ||
        compare(left.name, right.name)
      );
    }
    if (state.sort === "team_asc") {
      return compare(left.name, right.name);
    }
    return (
      right.currentRoleCount - left.currentRoleCount ||
      right.mapRoleCount - left.mapRoleCount ||
      compare(left.organizationName, right.organizationName)
    );
  });
  return rows;
}

function displayTitle(job) {
  return state.lang === "zh" ? job.titleZh : job.titleEn;
}

function displayLocation(job) {
  return state.lang === "zh" ? job.locationZh : job.locationEn;
}

function workArrangementLabel(job) {
  if (job.workArrangement === "remote_or_hybrid") {
    return t("arrangementRemoteHybridExplicit");
  }
  if (job.workArrangementBasis === "explicit_onsite") {
    return t("arrangementOnsiteExplicit");
  }
  return t("arrangementOnsiteDefault");
}

function accessLabel(value) {
  const key = ACCESS_LABEL_KEYS[value];
  return key ? t(key) : value || t("notRecorded");
}

function titleAuthenticityLabel(job) {
  const statusKey =
    TITLE_SUPPORT_LABEL_KEYS[job.titleSupportStatus] || "titlePending";
  const sourceKey =
    TITLE_SOURCE_LABEL_KEYS[job.titleSourceGranularity] ||
    "sourceUnclassified";
  return `${t(statusKey)} · ${t(sourceKey)}`;
}

function jobDetail(label, value) {
  const wrapper = document.createElement("div");
  wrapper.append(
    createElement("dt", "", label),
    createElement("dd", "", value || t("notRecorded")),
  );
  return wrapper;
}

function renderJobCard(job) {
  const card = createElement("article", "job-card");
  const topline = createElement("div", "card-topline");
  appendChip(topline, categoryLabel(job.category));
  appendChip(
    topline,
    job.isCurrent ? t("currentRole") : t("notInCurrentView"),
    job.isCurrent ? "chip-current" : "chip-muted",
  );
  appendChip(
    topline,
    job.confidenceTier === "verified"
      ? t("confidenceVerified")
      : t("confidenceProbable"),
    job.confidenceTier === "verified" ? "chip-current" : "chip-probable",
  );
  appendChip(topline, geographyLabel(job.geographies), "chip-muted");
  appendChip(
    topline,
    t(TITLE_SUPPORT_LABEL_KEYS[job.titleSupportStatus] || "titlePending"),
    job.isCurrent ? "chip-current" : "chip-muted",
  );

  const title = createElement("h3", "", displayTitle(job));
  const organization = createElement(
    "p",
    "job-org",
    job.organizationName,
  );
  const contextText = compactText([job.teamName, job.productName]);
  const context = createElement(
    "p",
    "job-context",
    contextText || t("teamProductUnknown"),
  );

  const details = createElement("dl", "job-details");
  const currentnessKey = CURRENTNESS_LABEL_KEYS[job.currentnessStatus];
  const evidenceText = [
    t("gradeOption", { grade: job.evidenceGrade }),
    accessLabel(job.accessRequirement),
    currentnessKey ? t(currentnessKey) : "",
  ].filter(Boolean).join(" · ");
  details.append(
    jobDetail(t("workLocation"), displayLocation(job)),
    jobDetail(t("workArrangementLabel"), workArrangementLabel(job)),
    jobDetail(t("lastVerified"), formatDate(job.lastVerifiedAt)),
    jobDetail(t("titleAuthenticity"), titleAuthenticityLabel(job)),
    jobDetail(t("evidenceAndAccess"), evidenceText),
  );

  const footer = createElement("div", "job-footer");
  if (job.sourceUrl) {
    const sourceLink = createElement("a", "source-link", t("openOfficialSource"));
    sourceLink.href = job.sourceUrl;
    sourceLink.target = "_blank";
    sourceLink.rel = "noopener noreferrer";
    footer.append(sourceLink);
  } else {
    footer.append(
      createElement("span", "chip chip-muted", t("noPublicRoleLink")),
    );
  }
  footer.append(createElement("span", "role-id", job.id));

  card.append(topline, title, organization, context, details, footer);
  return card;
}

function renderJobs(rows) {
  const list = createElement("div", "job-list");
  for (const job of rows) list.append(renderJobCard(job));
  elements.results.replaceChildren(list);
}

function sortedCategoryEntries(counts) {
  return [...counts.entries()].sort(
    (left, right) =>
      right[1] - left[1] ||
      CATEGORY_ORDER.indexOf(left[0]) - CATEGORY_ORDER.indexOf(right[0]),
  );
}

function renderTeamRow(team) {
  const row = createElement("article", "team-row");
  const identity = document.createElement("div");
  identity.append(
    createElement("h3", "", team.name),
    createElement(
      "p",
      "",
      `${team.organizationName} · ${geographyLabel(team.geographies)}`,
    ),
  );

  const identifier = document.createElement("div");
  identifier.append(
    createElement("p", "", t("teamId")),
    createElement("p", "", team.id),
  );

  const counts = createElement("div", "team-counts");
  const currentCount = document.createElement("div");
  currentCount.append(
    createElement("strong", "", formatNumber(team.currentRoleCount)),
    createElement("small", "", t("currentRoles")),
  );
  const mapCount = document.createElement("div");
  mapCount.append(
    createElement("strong", "", formatNumber(team.mapRoleCount)),
    createElement("small", "", t("mapRoleRecords")),
  );
  counts.append(currentCount, mapCount);

  const categories = createElement("div", "category-summary");
  const entries = sortedCategoryEntries(categoriesForTeam(team));
  if (entries.length === 0) {
    appendChip(
      categories,
      state.scope === "current" ? t("noCurrentRoles") : t("noMapRoles"),
      "chip-muted",
    );
  } else {
    for (const [category, count] of entries) {
      appendChip(categories, `${categoryLabel(category)} ${formatNumber(count)}`);
    }
  }

  row.append(identity, identifier, counts, categories);
  return row;
}

function renderTeams(rows) {
  const list = createElement("div", "team-list");
  for (const team of rows) list.append(renderTeamRow(team));
  elements.results.replaceChildren(list);
}

function renderEmpty() {
  const empty = createElement("div", "empty-state");
  const content = document.createElement("div");
  content.append(
    createElement("strong", "", t("emptyTitle")),
    createElement("p", "", t("emptyBody")),
  );
  empty.append(content);
  elements.results.replaceChildren(empty);
}

function updatePagination(total, totalPages) {
  elements.pagination.hidden = totalPages <= 1;
  elements["previous-page"].disabled = state.page <= 1;
  elements["next-page"].disabled = state.page >= totalPages;
  setText(
    elements["page-status"],
    t("pageStatus", {
      page: state.page,
      pages: Math.max(totalPages, 1),
    }),
  );
  if (total === 0) elements.pagination.hidden = true;
}

function updateUrl() {
  const params = new URLSearchParams();
  params.set("lang", state.lang);
  if (state.view !== "jobs") params.set("view", state.view);
  if (state.scope !== "current") params.set("scope", state.scope);
  if (state.query) params.set("q", state.query);
  if (state.geography !== "all") params.set("geo", state.geography);
  if (state.category !== "all") params.set("category", state.category);
  if (state.remote !== "all") params.set("remote", state.remote);
  if (state.grade !== "all") params.set("grade", state.grade);
  if (state.confidence !== "all") {
    params.set("confidence", state.confidence);
  }
  if (state.teamState !== "all") params.set("teams", state.teamState);
  const query = params.toString();
  const nextUrl = `${window.location.pathname}?${query}${window.location.hash}`;
  window.history.replaceState(null, "", nextUrl);
}

function render() {
  if (!store.loaded) {
    updateUrl();
    return;
  }
  const allRows = state.view === "jobs" ? filteredJobs() : filteredTeams();
  const pageSize = PAGE_SIZE[state.view];
  const totalPages = Math.ceil(allRows.length / pageSize);
  state.page = Math.min(Math.max(state.page, 1), Math.max(totalPages, 1));
  const start = (state.page - 1) * pageSize;
  const pageRows = allRows.slice(start, start + pageSize);
  setText(
    elements["result-status"],
    state.view === "jobs"
      ? t("jobsFound", { count: formatNumber(allRows.length) })
      : t("teamsFound", { count: formatNumber(allRows.length) }),
  );
  setText(
    elements["scope-note"],
    state.view === "jobs"
      ? state.scope === "current"
        ? t("currentScopeNote")
        : t("allScopeNote")
      : state.scope === "current"
        ? t("teamCurrentScopeNote")
        : t("teamAllScopeNote"),
  );

  if (pageRows.length === 0) {
    renderEmpty();
  } else if (state.view === "jobs") {
    renderJobs(pageRows);
  } else {
    renderTeams(pageRows);
  }
  updatePagination(allRows.length, totalPages);
  updateUrl();
}

function setView(view) {
  if (!["jobs", "teams"].includes(view)) return;
  state.view = view;
  state.page = 1;
  state.sort = view === "jobs" ? "verified_desc" : "current_desc";
  applyStateToControls();
  render();
}

function setLanguage(language) {
  if (!["zh", "en"].includes(language) || language === state.lang) return;
  state.lang = language;
  state.page = 1;
  applyTranslations();
  applyStateToControls();
  if (store.loaded) updateSummary();
  render();
}

function resetFilters() {
  Object.assign(state, {
    scope: "current",
    query: "",
    geography: "all",
    category: "all",
    remote: "all",
    grade: "all",
    confidence: "all",
    teamState: "all",
    sort: state.view === "jobs" ? "verified_desc" : "current_desc",
    page: 1,
  });
  applyStateToControls();
  render();
}

function bindEvents() {
  elements["lang-zh"].addEventListener("click", () => setLanguage("zh"));
  elements["lang-en"].addEventListener("click", () => setLanguage("en"));
  elements["tab-jobs"].addEventListener("click", () => setView("jobs"));
  elements["tab-teams"].addEventListener("click", () => setView("teams"));
  elements["filter-query"].addEventListener("input", (event) => {
    state.query = event.target.value;
    state.page = 1;
    render();
  });
  const selectBindings = [
    ["filter-scope", "scope"],
    ["filter-geography", "geography"],
    ["filter-category", "category"],
    ["filter-remote", "remote"],
    ["filter-grade", "grade"],
    ["filter-confidence", "confidence"],
    ["filter-team-state", "teamState"],
    ["filter-sort", "sort"],
  ];
  for (const [id, key] of selectBindings) {
    elements[id].addEventListener("change", (event) => {
      state[key] = event.target.value;
      state.page = 1;
      render();
    });
  }
  elements["reset-filters"].addEventListener("click", resetFilters);
  elements["previous-page"].addEventListener("click", () => {
    state.page -= 1;
    render();
    elements.results.scrollIntoView({ block: "start" });
  });
  elements["next-page"].addEventListener("click", () => {
    state.page += 1;
    render();
    elements.results.scrollIntoView({ block: "start" });
  });
}

function readUrlState() {
  const params = new URLSearchParams(window.location.search);
  const candidates = {
    lang: params.get("lang"),
    view: params.get("view"),
    scope: params.get("scope"),
    query: params.get("q"),
    geography: params.get("geo"),
    category: params.get("category"),
    remote: params.get("remote"),
    grade: params.get("grade"),
    confidence: params.get("confidence"),
    teamState: params.get("teams"),
  };
  if (["zh", "en"].includes(candidates.lang)) state.lang = candidates.lang;
  if (["jobs", "teams"].includes(candidates.view)) state.view = candidates.view;
  if (["current", "all"].includes(candidates.scope)) state.scope = candidates.scope;
  if (candidates.query) state.query = candidates.query.slice(0, 200);
  if (["all", "China", "United States"].includes(candidates.geography)) {
    state.geography = candidates.geography;
  }
  const categoryId =
    LEGACY_CATEGORY_IDS.get(candidates.category) || candidates.category;
  if (["all", ...CATEGORY_ORDER].includes(categoryId)) {
    state.category = categoryId;
  }
  const remoteCompatibility = {
    declared: "remote_or_hybrid",
    unknown: "onsite",
  };
  const remote = remoteCompatibility[candidates.remote] || candidates.remote;
  if (["all", "onsite", "remote_or_hybrid"].includes(remote)) {
    state.remote = remote;
  }
  if (["all", "A", "B", "C", "E"].includes(candidates.grade)) {
    state.grade = candidates.grade;
  }
  if (["all", "verified", "probable"].includes(candidates.confidence)) {
    state.confidence = candidates.confidence;
  }
  if (["all", "active", "zero"].includes(candidates.teamState)) {
    state.teamState = candidates.teamState;
  }
  state.sort = state.view === "jobs" ? "verified_desc" : "current_desc";
}

async function load() {
  bindElements();
  readUrlState();
  applyTranslations();
  applyStateToControls();
  bindEvents();
  render();

  try {
    const [
      metadata,
      organizations,
      teams,
      products,
      roles,
      current,
    ] = await Promise.all([
      fetchJson(DATA_PATHS.metadata, t("releaseMetadata")),
      fetchJsonLines(DATA_PATHS.organizations, t("organizationsData")),
      fetchJsonLines(DATA_PATHS.teams, t("teamsData")),
      fetchJsonLines(DATA_PATHS.products, t("productsData")),
      fetchJsonLines(DATA_PATHS.roles, t("rolesData")),
      fetchJsonLines(DATA_PATHS.current, t("currentData")),
    ]);
    buildStore({
      metadata,
      organizations,
      teams,
      products,
      roles,
      current,
    });
    updateSummary();
    render();
  } catch (error) {
    elements["error-panel"].hidden = false;
    setText(
      elements["error-message"],
      error instanceof Error ? error.message : t("unknownError"),
    );
    elements.results.replaceChildren();
    elements.pagination.hidden = true;
    setText(elements["result-status"], t("dataLoadFailed"));
  }
}

document.addEventListener("DOMContentLoaded", load);
