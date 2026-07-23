"use strict";

const DATA_PATHS = Object.freeze({
  metadata: "./data/metadata/release-metadata.json",
  organizations: "./data/map/organizations.jsonl",
  teams: "./data/map/teams.jsonl",
  products: "./data/map/products.jsonl",
  roles: "./data/map/roles.jsonl",
  current: "./data/current/current-opportunities.jsonl",
});

const CATEGORY_RULES = Object.freeze([
  ["安全、治理与合规", ["security", "safety", "governance", "compliance", "risk", "trust", "identity", "policy", "secure", "安全", "治理", "合规"]],
  ["评测、测试与质量", ["evaluation", "eval", "test", "quality", "observability", "benchmark", "red_team", "red team", "评测", "测试", "质量"]],
  ["产品与设计", ["product", "design", "designer", "ux", "ui", "产品", "设计"]],
  ["商务、市场与合作", ["gtm", "sales", "marketing", "commercial", "partnership", "partner", "business_development", "business development", "growth", "account executive", "销售", "市场", "商务", "合作"]],
  ["客户解决方案与交付", ["solution", "solutions", "forward_deployed", "forward deployed", "fde", "delivery", "implementation", "customer", "adoption", "consult", "architect", "support", "解决方案", "交付", "客户", "架构"]],
  ["运营、项目与职能", ["operations", "operation", "program", "project", "recruit", "talent", "strategy", "human_resources", "human resources", "finance", "legal", "chief_of_staff", "chief of staff", "运营", "项目", "招聘", "战略"]],
  ["算法、研究与模型", ["research", "scientist", "algorithm", "training", "post_training", "post-training", "model", "machine_learning", "machine learning", "reinforcement", "reasoning", "alignment", "算法", "研究", "训练", "模型"]],
  ["平台、基础设施与数据", ["platform", "infra", "infrastructure", "orchestration", "data", "backend", "cloud", "devops", "sre", "database", "distributed", "systems", "rag", "retrieval", "context", "平台", "基础设施", "数据", "后端"]],
  ["工程与应用开发", ["engineer", "engineering", "developer", "application", "full_stack", "full stack", "frontend", "software", "coding", "开发", "工程"]],
]);

const CATEGORY_ORDER = Object.freeze([
  ...CATEGORY_RULES.map(([name]) => name),
  "其他或边界岗位",
]);

const CURRENTNESS_LABELS = Object.freeze({
  current_verified: "已确认当前有效",
  current_probable: "很可能当前有效",
  stale_unverified: "已过期、未重新确认",
  closed_verified: "已确认关闭",
  disputed: "存在争议",
});

const ACCESS_LABELS = Object.freeze({
  public_no_login: "公开网页、无需登录",
  official_free_account: "官方免费账号后可查看",
  user_assisted_auth: "需要用户协助认证",
  paid_or_private_blocked: "付费或私人来源",
});

const PAGE_SIZE = Object.freeze({ jobs: 24, teams: 30 });
const collator = new Intl.Collator("zh-CN", {
  numeric: true,
  sensitivity: "base",
});

const state = {
  view: "jobs",
  scope: "current",
  query: "",
  geography: "all",
  category: "all",
  remote: "all",
  grade: "all",
  teamState: "all",
  sort: "verified_desc",
  page: 1,
};

const store = {
  metadata: null,
  jobs: [],
  teams: [],
};

const elements = {};

function parseJsonLines(text, label) {
  const rows = [];
  for (const [index, line] of text.split(/\r?\n/u).entries()) {
    if (!line.trim()) continue;
    try {
      rows.push(JSON.parse(line));
    } catch {
      throw new Error(`${label} 第 ${index + 1} 行不是合法数据。`);
    }
  }
  return rows;
}

async function fetchJson(path, label) {
  const response = await fetch(path, { credentials: "same-origin" });
  if (!response.ok) {
    throw new Error(`${label}载入失败（${response.status}）。`);
  }
  return response.json();
}

async function fetchJsonLines(path, label) {
  const response = await fetch(path, { credentials: "same-origin" });
  if (!response.ok) {
    throw new Error(`${label}载入失败（${response.status}）。`);
  }
  return parseJsonLines(await response.text(), label);
}

function roleCategory(role) {
  const text = String(role.role_family || role.title || "").toLocaleLowerCase();
  for (const [category, keywords] of CATEGORY_RULES) {
    if (keywords.some((keyword) => text.includes(keyword))) return category;
  }
  return "其他或边界岗位";
}

function geographyValues(team, current) {
  if (current?.geography) return [current.geography];
  return Array.isArray(team?.team_geography) ? team.team_geography : [];
}

function geographyLabel(values) {
  const hasChina = values.includes("China");
  const hasUnitedStates = values.includes("United States");
  if (hasChina && hasUnitedStates) return "中国、美国";
  if (hasChina) return "中国";
  if (hasUnitedStates) return "美国";
  return "未记录";
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
    const locations = Array.isArray(role.job_locations)
      ? role.job_locations.filter(Boolean)
      : [];
    const geographies = geographyValues(team, current);
    const sourceCandidate =
      current?.source_urls?.[0] || role.official_role_url || null;
    const category = roleCategory(role);
    const organizationName =
      organization?.canonical_name || "未解析组织";
    const teamName = team?.team_name || "未解析团队";
    const productName = product?.name || "";
    const searchText = compactText([
      role.title,
      role.role_family,
      organizationName,
      teamName,
      productName,
      category,
      ...locations,
    ]).toLocaleLowerCase();

    return {
      id: role.role_id,
      title: role.title || "未命名岗位",
      roleFamily: role.role_family || "",
      organizationName,
      teamName,
      productName,
      teamId: role.team_id,
      category,
      locations,
      geographies,
      geographyLabel: geographyLabel(geographies),
      remoteDeclared: Boolean(role.remote_scope),
      remoteScope: role.remote_scope || "",
      evidenceGrade: current?.evidence_grade || role.evidence_grade || "未记录",
      accessRequirement:
        current?.access_requirement || role.access_requirement || "未记录",
      currentnessStatus: role.currentness_status || "未记录",
      lastVerifiedAt:
        current?.last_verified_at || role.last_verified_at || "",
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
      organization?.canonical_name || "未解析组织";
    const searchText = compactText([
      team.team_name,
      organizationName,
      team.team_id,
      ...allCategoryCounts.keys(),
    ]).toLocaleLowerCase();

    return {
      id: team.team_id,
      name: team.team_name || "未命名团队",
      organizationName,
      geographies: team.team_geography || [],
      geographyLabel: geographyLabel(team.team_geography || []),
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
}

function countCategories(jobs) {
  const counts = new Map();
  for (const job of jobs) {
    counts.set(job.category, (counts.get(job.category) || 0) + 1);
  }
  return counts;
}

function formatNumber(value) {
  return new Intl.NumberFormat("zh-CN").format(Number(value) || 0);
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

function bindElements() {
  const ids = [
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

function populateCategoryFilter() {
  for (const category of CATEGORY_ORDER) {
    const option = document.createElement("option");
    option.value = category;
    setText(option, category);
    elements["filter-category"].append(option);
  }
}

function updateSummary() {
  const activeTeams = store.teams.filter(
    (team) => team.currentRoleCount > 0,
  ).length;
  setText(elements["evidence-count"], formatNumber(store.metadata.evidence_rows));
  setText(elements["stat-current"], formatNumber(store.jobs.filter((job) => job.isCurrent).length));
  setText(elements["stat-roles"], formatNumber(store.jobs.length));
  setText(elements["stat-teams"], formatNumber(store.teams.length));
  setText(elements["stat-active-teams"], formatNumber(activeTeams));
  setText(elements["release-date"], store.metadata.release_as_of || "未记录");
  elements["release-date"].dateTime = store.metadata.release_as_of || "";
}

function sortOptionsForView() {
  const options =
    state.view === "jobs"
      ? [
          ["verified_desc", "最后复核日期：由近到远"],
          ["organization_asc", "组织名称：正序"],
          ["team_asc", "团队名称：正序"],
          ["category_asc", "岗位类别：正序"],
        ]
      : [
          ["current_desc", "当前岗位数：由多到少"],
          ["map_desc", "地图岗位记录：由多到少"],
          ["organization_asc", "组织名称：正序"],
          ["team_asc", "团队名称：正序"],
        ];

  elements["filter-sort"].replaceChildren();
  for (const [value, label] of options) {
    const option = document.createElement("option");
    option.value = value;
    setText(option, label);
    elements["filter-sort"].append(option);
  }
  if (!options.some(([value]) => value === state.sort)) {
    state.sort = options[0][0];
  }
  elements["filter-sort"].value = state.sort;
}

function applyStateToControls() {
  elements["filter-query"].value = state.query;
  elements["filter-scope"].value = state.scope;
  elements["filter-geography"].value = state.geography;
  elements["filter-category"].value = state.category;
  elements["filter-remote"].value = state.remote;
  elements["filter-grade"].value = state.grade;
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
  return (
    state.geography === "all" || values.includes(state.geography)
  );
}

function filteredJobs() {
  const query = normalizeQuery(state.query);
  const rows = store.jobs.filter((job) => {
    if (state.scope === "current" && !job.isCurrent) return false;
    if (!geographyMatches(job.geographies)) return false;
    if (state.category !== "all" && job.category !== state.category) return false;
    if (state.remote === "declared" && !job.remoteDeclared) return false;
    if (state.remote === "unknown" && job.remoteDeclared) return false;
    if (state.grade !== "all" && job.evidenceGrade !== state.grade) return false;
    if (query && !job.searchText.includes(query)) return false;
    return true;
  });

  rows.sort((left, right) => {
    if (state.sort === "organization_asc") {
      return (
        collator.compare(left.organizationName, right.organizationName) ||
        collator.compare(left.title, right.title)
      );
    }
    if (state.sort === "team_asc") {
      return (
        collator.compare(left.teamName, right.teamName) ||
        collator.compare(left.title, right.title)
      );
    }
    if (state.sort === "category_asc") {
      return (
        CATEGORY_ORDER.indexOf(left.category) -
          CATEGORY_ORDER.indexOf(right.category) ||
        collator.compare(left.title, right.title)
      );
    }
    return (
      String(right.lastVerifiedAt).localeCompare(String(left.lastVerifiedAt)) ||
      collator.compare(left.organizationName, right.organizationName) ||
      collator.compare(left.title, right.title)
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

  rows.sort((left, right) => {
    if (state.sort === "map_desc") {
      return (
        right.mapRoleCount - left.mapRoleCount ||
        collator.compare(left.organizationName, right.organizationName)
      );
    }
    if (state.sort === "organization_asc") {
      return (
        collator.compare(left.organizationName, right.organizationName) ||
        collator.compare(left.name, right.name)
      );
    }
    if (state.sort === "team_asc") {
      return collator.compare(left.name, right.name);
    }
    return (
      right.currentRoleCount - left.currentRoleCount ||
      right.mapRoleCount - left.mapRoleCount ||
      collator.compare(left.organizationName, right.organizationName)
    );
  });
  return rows;
}

function jobDetail(label, value) {
  const wrapper = document.createElement("div");
  wrapper.append(
    createElement("dt", "", label),
    createElement("dd", "", value || "未记录"),
  );
  return wrapper;
}

function renderJobCard(job) {
  const card = createElement("article", "job-card");
  const topline = createElement("div", "card-topline");
  appendChip(topline, job.category);
  appendChip(
    topline,
    job.isCurrent ? "当前岗位" : "未进入当前岗位视图",
    job.isCurrent ? "chip-current" : "chip-muted",
  );
  appendChip(topline, job.geographyLabel, "chip-muted");

  const title = createElement("h3", "", job.title);
  const organization = createElement(
    "p",
    "job-org",
    job.organizationName,
  );
  const contextText = compactText([
    job.teamName,
    job.productName,
  ]);
  const context = createElement(
    "p",
    "job-context",
    contextText || "未记录团队或产品",
  );

  const details = createElement("dl", "job-details");
  details.append(
    jobDetail("工作地点", job.locations.join("；") || "未记录"),
    jobDetail(
      "远程信息",
      job.remoteDeclared ? job.remoteScope : "未记录远程或混合办公范围",
    ),
    jobDetail("最后复核", job.lastVerifiedAt || "未记录"),
    jobDetail(
      "证据与访问",
      `${job.evidenceGrade}级 · ${
        ACCESS_LABELS[job.accessRequirement] || job.accessRequirement
      }`,
    ),
  );

  const footer = createElement("div", "job-footer");
  if (job.sourceUrl) {
    const sourceLink = createElement("a", "source-link", "打开官方来源 ↗");
    sourceLink.href = job.sourceUrl;
    sourceLink.target = "_blank";
    sourceLink.rel = "noopener noreferrer";
    footer.append(sourceLink);
  } else {
    footer.append(createElement("span", "chip chip-muted", "未公开岗位链接"));
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
      `${team.organizationName} · ${team.geographyLabel}`,
    ),
  );

  const identifier = document.createElement("div");
  identifier.append(
    createElement("p", "", "团队编号"),
    createElement("p", "", team.id),
  );

  const counts = createElement("div", "team-counts");
  const currentCount = document.createElement("div");
  currentCount.append(
    createElement("strong", "", formatNumber(team.currentRoleCount)),
    createElement("small", "", "当前岗位"),
  );
  const mapCount = document.createElement("div");
  mapCount.append(
    createElement("strong", "", formatNumber(team.mapRoleCount)),
    createElement("small", "", "地图岗位记录"),
  );
  counts.append(currentCount, mapCount);

  const categories = createElement("div", "category-summary");
  const entries = sortedCategoryEntries(categoriesForTeam(team));
  if (entries.length === 0) {
    appendChip(
      categories,
      state.scope === "current" ? "当前岗位为 0" : "地图岗位记录为 0",
      "chip-muted",
    );
  } else {
    for (const [category, count] of entries) {
      appendChip(categories, `${category} ${count}`);
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
    createElement("strong", "", "没有符合条件的结果"),
    createElement(
      "p",
      "",
      "可以减少筛选条件、清除关键词，或切换到全部地图岗位记录。",
    ),
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
    `第 ${state.page} / ${Math.max(totalPages, 1)} 页`,
  );
  if (total === 0) elements.pagination.hidden = true;
}

function updateUrl() {
  const params = new URLSearchParams();
  if (state.view !== "jobs") params.set("view", state.view);
  if (state.scope !== "current") params.set("scope", state.scope);
  if (state.query) params.set("q", state.query);
  if (state.geography !== "all") params.set("geo", state.geography);
  if (state.category !== "all") params.set("category", state.category);
  if (state.remote !== "all") params.set("remote", state.remote);
  if (state.grade !== "all") params.set("grade", state.grade);
  if (state.teamState !== "all") params.set("teams", state.teamState);
  const query = params.toString();
  const nextUrl = `${window.location.pathname}${query ? `?${query}` : ""}${window.location.hash}`;
  window.history.replaceState(null, "", nextUrl);
}

function render() {
  const allRows = state.view === "jobs" ? filteredJobs() : filteredTeams();
  const pageSize = PAGE_SIZE[state.view];
  const totalPages = Math.ceil(allRows.length / pageSize);
  state.page = Math.min(Math.max(state.page, 1), Math.max(totalPages, 1));
  const start = (state.page - 1) * pageSize;
  const pageRows = allRows.slice(start, start + pageSize);
  const noun = state.view === "jobs" ? "个岗位" : "个团队";
  setText(
    elements["result-status"],
    `找到 ${formatNumber(allRows.length)} ${noun}`,
  );
  setText(
    elements["scope-note"],
    state.view === "jobs"
      ? state.scope === "current"
        ? "仅显示通过当前性、日期、来源和访问要求门的岗位。"
        : "展示全部地图岗位记录；未进入当前视图的记录不代表仍在招聘。"
      : state.scope === "current"
        ? "团队列表保持完整；类别摘要按当前岗位计算。"
        : "团队列表保持完整；类别摘要按全部地图岗位记录计算。",
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

function resetFilters() {
  Object.assign(state, {
    scope: "current",
    query: "",
    geography: "all",
    category: "all",
    remote: "all",
    grade: "all",
    teamState: "all",
    sort: state.view === "jobs" ? "verified_desc" : "current_desc",
    page: 1,
  });
  applyStateToControls();
  render();
}

function bindEvents() {
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
    view: params.get("view"),
    scope: params.get("scope"),
    query: params.get("q"),
    geography: params.get("geo"),
    category: params.get("category"),
    remote: params.get("remote"),
    grade: params.get("grade"),
    teamState: params.get("teams"),
  };
  if (["jobs", "teams"].includes(candidates.view)) state.view = candidates.view;
  if (["current", "all"].includes(candidates.scope)) state.scope = candidates.scope;
  if (candidates.query) state.query = candidates.query.slice(0, 200);
  if (["all", "China", "United States"].includes(candidates.geography)) {
    state.geography = candidates.geography;
  }
  if (["all", ...CATEGORY_ORDER].includes(candidates.category)) {
    state.category = candidates.category;
  }
  if (["all", "declared", "unknown"].includes(candidates.remote)) {
    state.remote = candidates.remote;
  }
  if (["all", "A", "B", "C", "E"].includes(candidates.grade)) {
    state.grade = candidates.grade;
  }
  if (["all", "active", "zero"].includes(candidates.teamState)) {
    state.teamState = candidates.teamState;
  }
  state.sort = state.view === "jobs" ? "verified_desc" : "current_desc";
}

async function load() {
  bindElements();
  populateCategoryFilter();
  readUrlState();
  applyStateToControls();
  bindEvents();

  try {
    const [
      metadata,
      organizations,
      teams,
      products,
      roles,
      current,
    ] = await Promise.all([
      fetchJson(DATA_PATHS.metadata, "发布元数据"),
      fetchJsonLines(DATA_PATHS.organizations, "组织数据"),
      fetchJsonLines(DATA_PATHS.teams, "团队数据"),
      fetchJsonLines(DATA_PATHS.products, "产品数据"),
      fetchJsonLines(DATA_PATHS.roles, "岗位数据"),
      fetchJsonLines(DATA_PATHS.current, "当前岗位数据"),
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
      error instanceof Error ? error.message : "发生未知错误。",
    );
    elements.results.replaceChildren();
    elements.pagination.hidden = true;
    setText(elements["result-status"], "数据载入失败");
  }
}

document.addEventListener("DOMContentLoaded", load);
