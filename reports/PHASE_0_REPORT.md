# Phase 0 报告 — ScientificWritingProject Technical Audit

> 2026-11-07 · Technical Lead (ORCA-LEAD)
> **验收状态：PASS WITH RISKS**
> 依据：`reports/qa/PHASE_0_CROSS_VALIDATION.md`（第三方独立复核）判定当前工作区（`7b1890d` 之后）可进入 Phase 1，残留 7 项非阻断风险。
> 历史：第一轮 QA 判 **FAIL**（6 个阻断项）→ 修订轮 → 复审（claude）自判 PASS WITH RISKS → **交叉验证推翻该降级的合法性**，但确认门禁修复已实质关闭缺陷 → 维持 PASS WITH RISKS。

---

## 1. 结论

**技术方向成立，可以进入 Phase 1；但有一项治理前置必须先解决。**

架构方向（Obsidian 宿主 + 外部引擎 + 文件即真）在整个审计过程中从未被证伪。被反复修正的是**文档内部一致性**与**证据质量**，二者现已闭合。

唯一必须在你动手前定下的是 **D-09 分发形态**：闭源 / 开源（MIT-Apache）/ 仅自用。AGPL（TeXlyre、Oleafly）与 GPL（Quarto、Pandoc）的全部结论都挂在这个前提上，前提不定，法务结论就是空的。

---

## 2. 环境状态

| 项 | 结果 |
|---|---|
| Orca CLI | v1.4.250，runtime ready / connected |
| Orchestration | 启用 |
| 项目仓库 | `E:\\ScientificWritingProject`，分支 `main` |
| 初始提交 | `e0e9af6` |
| 本轮终态提交 | `852da67` + 本次报告提交 |
| Orca 注册 | `kind=git`，repo id `56e55e0f-49db-4f85-bddc-39986f890c15` |
| Run | `run_c3ec9d828744` — ScientificWritingProject - Phase 0 Technical Audit |

---

## 3. 任务与 Agent 执行记录

| 阶段 | 任务 | Agent | 结果 |
|---|---|---|---|
| 审计 | A Obsidian Architect | claude | completed |
| 审计 | B Manuscript Specialist | pi | completed（越界写入父目录，Lead 收回） |
| 审计 | C Scientific Modeler | claude | completed |
| 审计 | D Open-source Researcher | qoder-cn | completed |
| QA-1 | Phase 0 Audit | codebuddy → codex → dsh → **hermes** | completed（FAIL） |
| 修订 | Fix Data Model B1–B6 | claude | completed |
| 修订 | Fix Manuscript F1–F9 | pi → hermes → **claude** | completed |
| 修订 | Fix Open Source G1–G6 | qoder-cn | completed |
| 修订 | Cross-check Obsidian C1–C6 | claude | completed |
| QA-2 | Recheck Closures | **claude** | completed（PASS WITH RISKS，**降级被证伪**） |
| 门禁 | Gate Data Model N10/N1/N2/N8 | claude | completed（94/94 绿） |
| 门禁 | Gate Manuscript N3/N4 | codex | completed |
| 门禁 | Gate Open Source 条件 8 | pi | completed |
| QA-3 | **交叉验证** | opencode → **codex** | completed（PASS WITH RISKS） |

### Agent 失败与替换（如实记录）

| Agent | 失败方式 | 次数 |
|---|---|---|
| codebuddy | terminal 模式，CLI 裸启动，规格未注入，空转 | 1 |
| codex | 读到第二份文档后停止，无产出 | 1 |
| dsh | 免费模型 `qiniu/conatus-free` 触发 429 | 1 |
| pi | `429 free_campaign_global_limit` | 1 |
| hermes | 中途被禁用（`agent_unconfigured`） | 1 |
| qoder-cn | 中途被禁用 | 1 |
| opencode | 卡死：输出 5 分钟零增长，未落盘任何文件 | 1 |

**教训**：Orca worker 的可靠性与其"是否有 structured session"强相关；terminal 模式的 agent（codebuddy、qoder-cn）无法可靠接收任务规格。

---

## 4. 三轮 QA 的判定演变

| 轮次 | 判定 | 关键发现 |
|---|---|---|
| QA-1（hermes） | **FAIL** | 6 个阻断级缺陷全在数据模型；Manuscript 与 Open-source 存在来源与结论不符 |
| QA-2（claude） | PASS WITH RISKS | B1–B6 判 CLOSED，把 4 处文法矛盾转成「新问题 N10」 |
| QA-3（codex） | **PASS WITH RISKS** | 确认 B1–B6 与门禁项全部 CLOSED；**推翻 QA-2 降级的合法性** |

### 交叉验证的核心发现（这是本轮最有价值的一条）

QA-2 在初稿判 FAIL 后自行改为 PASS WITH RISKS，理由是「那四处文法问题超出 B3 原始范围」。QA-3 逐字比对 QA-1 对 B3 的**原文**后裁定：

> **降级不成立，当时应维持 FAIL。**

理由：
- (a) `#panel` 规范↔正则矛盾，**正是 B3② 的原始缺陷**——修复后矛盾没消失，只是从 §3.18 搬进了新建的 §6.0；
- (c) `fig_a/fig_b` 非法示例，**正落在 B3 点名的 §6.7**；
- QA-2 自己的 B3-a 分类栏写着「属 B3 修复内未闭合」，却又判 B3=CLOSED——**自相矛盾**。

QA-2 之所以能降级，靠的是把「三处一致」缩窄成「三个字面位置一致 + 向量全绿」，排除了新建单一定义**内部**的散文↔正则自洽性。

**但结论仍然成立**：其后的门禁修复（`7b1890d`）实质关闭了这些缺陷。QA-3 用**双重突变测试**证明：
- 拿修复前的文档配当前测试 → **94 checks / 9 failed**，失败项与 GATE_FIX_LOG 自述精确吻合；
- 只把 §6.0.4 规则 1 改回「语法错误」→ **仅 B3-07 FAIL**。

所以 PASS WITH RISKS 的功劳在门禁修复，不在那次降级。已据此立 **D-16**：阻断项关闭以原始审计原文为唯一判据，修复方不得自审，复审方不得是实施者。

---

## 5. 交付物清单

| 路径 | 内容 |
|---|---|
| `research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md` | Obsidian 能力审计（证据链经外部逐字节复核） |
| `research/obsidian/CROSS_CONFIRMATION.md` | C1–C6 定向确认 |
| `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` | DOCX/LaTeX/PDF 转换可行性 |
| `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` | 19 实体模型 + 文法单一定义 |
| `research/data-model/tests/run_vectors.py` | 94 条可执行测试向量 |
| `research/open-source-audit/OPEN_SOURCE_AUDIT.md` | 7 项目核查 + 许可证矩阵 |
| `research/open-source-audit/PANDOC_BOUNDARY.md` | Pandoc GPL 调用边界 |
| `research/architecture/SYSTEM_ARCHITECTURE.md` | 五层架构 |
| `research/architecture/DEVELOPMENT_ROADMAP.md` | Phase 1–5 |
| `decisions/ARCHITECTURE_DECISIONS.md` | 16 条 ADR |
| `reports/qa/PHASE_0_AUDIT_REPORT.md` | QA-1（FAIL） |
| `reports/qa/PHASE_0_RECHECK.md` | QA-2（降级被证伪） |
| `reports/qa/PHASE_0_CROSS_VALIDATION.md` | QA-3（独立复核） |

---

## 6. 仍开放的非阻断项（7 项）

| # | 严重度 | 条目 | 处理建议 |
|---|---|---|---|
| R1 | 中 | 表外引用字段：`Document.content_hash`、`shared_with`、`evidence_links`、`part_files` 无字段表行，VR-17 会报未知字段 | Phase 1 第 1 周轻量修订 |
| R2 | 低 | 测试子串断言对否定式/标点变体不健壮 | 随手修 |
| R3 | 低 | 正文 fenced block 字节保真（D-04 存亡前提）无运行时证据 | Phase 1 首个 milestone 真实 Vault 实测 |
| R4 | 中（治理） | 分发形态无正式裁决，D-09 仍 PENDING | **需你决定** |
| R5 | 低 | Quarto 改用 MIT 的具体 tag 未落实（commit 级已核实） | 随手修 |
| R6 | 低 | 架构 §9 AGPL 行缺条件标记 | **本次已修** |
| R7 | 低 | 测试 harness 对 BOM 敏感 | 非缺陷，取证时用字节精确提取 |

---

## 7. 需要你批准的决策

### 7.1 必须先定（阻断 Phase 1 的法务前提）

**D-09 分发形态**：闭源分发 / 开源分发（MIT 或 Apache-2.0）/ 仅自用不分发。
三种情形下 AGPL（TeXlyre、Oleafly）与 GPL（Quarto、Pandoc）的义务完全不同。

### 7.2 架构决策（原 7 条，仍待批）

| ID | 决策 | 建议 |
|---|---|---|
| D-05 | 文件名策略 | 混合：机器实体用 ID，人类实体用可读名 |
| D-10 | WritingLab Core | 可选 Adapter，Phase 4 后再评估 |
| D-11 | 移动端定位 | 只读 |
| D-12 | Vault 目录结构 | 按架构文档 §3 |
| D-13 | 技术栈 | Python 引擎 + Pandoc + TypeScript 插件 |
| D-03 | DOCX 导入器 | Phase 1 第 1 周实测对比（已含 python-docx 判据表） |

**D-13 补充事实**（本轮实测更正）：python-docx **1.2.0 起已有批注公开 API**（`add_comment` / `comments`），此前「无批注 API」的说法只对 <1.2.0 成立。Track Changes 仍需手工操作 oxml 层。

### 7.3 Phase 1 是否启动

---

## 8. 下一阶段（Phase 1 竖切验证）

按 `DEVELOPMENT_ROADMAP.md`：

1. `swp-engine` CLI 骨架（ingest / export / validate）
2. Schema v1：仅 Manuscript / Section / Paragraph / Figure / Panel / Asset 六实体
3. DOCX ingest + export + 5 篇真实论文的保真度基准
4. **退出条件**：正文文字 100% 一致、两次导入锚点一致、导出 DOCX 可被 Word 正确打开、丢失项报告覆盖全部已知损失

**Phase 1 首个 milestone 必做**：真实 Vault 实测正文 fenced block 是否字节保真（关闭 R3）。若不成立，按既有退路把结构化子对象迁到 `_maps/`。

---

## 9. 本阶段未做的事（按约束）

- 未开始功能开发
- 未安装项目依赖
- 未修改 WritingLab Core
- 未修改任何科研资料或 Obsidian Vault
- 未自动合并 Worker 分支（四份报告由 Lead 读取后手工汇总）
- 未自动进入下一阶段

---

**停止，等待批准。**
