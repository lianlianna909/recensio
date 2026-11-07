# Architecture Decisions — Phase 0

> 版本：v0.1 · 2026-11-06
> 状态标记：**ACCEPTED**（Phase 0 内由 Technical Lead 裁定）/ **PENDING**（必须用户批准）/ **OPEN**（证据不足，待验证）
> 任何 PENDING 决策在获批前不得进入实现。

---

## 决策索引

| ID | 决策 | 状态 |
|---|---|---|
| D-01 | 文件即真，不引入数据库作为事实来源 | ACCEPTED |
| D-02 | 转换逻辑放在 Obsidian 之外的本地引擎进程 | ACCEPTED |
| D-03 | DOCX 导入器选型 | OPEN |
| D-04 | frontmatter 禁止嵌套对象 | ACCEPTED |
| D-05 | 实体文件名 = 实体 ID | **PENDING** |
| D-06 | 编号在渲染时解析，导出时固化 | ACCEPTED |
| D-07 | Bases 只作浏览层，不作查询引擎 | ACCEPTED |
| D-08 | 修订三层：sidecar + 快照 + Git | ACCEPTED |
| D-09 | 分发形态 = 宽松许可开源；不 Fork 任何项目 | **ACCEPTED** |
| D-10 | WritingLab Core 为可选 Adapter | **PENDING** |
| D-11 | 移动端只读 | **PENDING** |
| D-12 | Vault 目录结构 | **PENDING** |
| D-13 | 核心技术栈 | **PENDING** |
| D-14 | 实体分期实现（17 → 6） | ACCEPTED |
| D-15 | 原始件不可变，sha256 内容寻址 | ACCEPTED |
| D-16 | 阻断项关闭以原始审计原文为判据，须由独立方复核 | ACCEPTED |
| ADR-LIC-001 | 项目许可证 = Apache License 2.0 | **ACCEPTED（已执行）** |
| ADR-LIC-002 | 贡献者协议 = DCO 1.1，暂不采用 CLA | **ACCEPTED（已执行）** |
| ADR-LIC-003 | 第三方依赖治理（THIRD-PARTY.md 强制登记） | **ACCEPTED（已执行）** |
| ADR-NAME-001 | 项目对外名称 = Recensio | **ACCEPTED** |

> **ADR-LIC-001 ~ 003 与 ADR-NAME-001 的完整内容见 [`ADR-LIC-001-003.md`](ADR-LIC-001-003.md)。**
> 执行状态：`LICENSE`、`NOTICE`、`DCO.md`、`CONTRIBUTING.md`、`THIRD-PARTY.md`、`docs/LICENSE-POLICY.md` 已创建；两个自有 `.py` 已加 SPDX 头。
> 仍待办：首个带 `Signed-off-by` 的提交（需负责人本人的 Git 身份）、`reuse lint` 实测（工具未安装）、商标与域名核查。

---

## D-01 文件即真

**Context**：Worker C 提出 P1「文件是唯一事实来源」，并给出"删除索引后可逐字节重建"的可验证标准。

**Decision**：接受。L0+L1 必须自足，L2/L3/L4 全部删除后稿件仍完整可读。

**Consequences**：所有查询必须能降级为"遍历文件"；性能靠派生索引解决，不靠数据库；任何只存在于索引中的信息都是 bug。

---

## D-02 引擎外置

**Context**：Worker A 证明插件无 `fs`/`child_process`，移动端调用 Node/Electron API 会崩溃；Worker B 的推荐方案（docx4j / python-docx / Pandoc）全部需要外部进程。

**Decision**：转换、导出、全库索引、全库校验全部在独立的本地引擎进程中完成；插件通过 127.0.0.1 的 JSON-RPC 桥调用。

**Consequences**：用户需要安装引擎；移动端无导入导出；引擎必须能独立 CLI 运行以便 CI 与故障隔离；桥的安全模型必须显式设计（随机端口 + token）。

**Alternative rejected**：纯 JS 插件内实现（mammoth.js 可做 DOCX→HTML，但无法还原 Track Changes、无法导出、无法处理大文件）。

---

## D-03 DOCX 导入器选型 — OPEN

**Context**：Worker B 推荐 docx4j（Java，功能最全）或 python-docx（生态好）。两者在 Track Changes、合并单元格、OMML 上的能力不同。

**Decision**：**未定**。Phase 1 第 1 周用同一批 5 篇真实稿件做对比，判据：
1. `w:ins`/`w:del`/`comments.xml` 的解析完整度
2. 合并单元格与嵌套表格的结构还原
3. OMML → LaTeX 的质量
4. 部署复杂度（Java 运行时 vs Python 环境）

**Blocking**：Phase 1 的 ingest 实现。

---

## D-04 frontmatter 禁止嵌套

**Context**：Worker C 的模型使用 `list<object>`（Citation、Issue.targets、section_meta）。Worker A 引用官方文档：Obsidian 明列 **Nested properties 不支持**，且 Properties 面板会重写 frontmatter。

**Decision**：frontmatter 只允许标量、标量列表、wikilink 列表。结构化子对象放正文 fenced YAML 块（```yaml swp:xxx```），或平铺为等长平行列表。

**Consequences**：Properties 面板无法编辑引用详情，需要专用编辑视图；C 的 R4 降级方案成为主线而非备选。

**Alternative rejected**：把嵌套结构强塞进 frontmatter 并依赖 Obsidian"不破坏未知结构"——无证据支持，且官方明确会重写。

---

## D-05 文件名 = 实体 ID — PENDING

**Context**：Worker C 的 P3 主张文件名采用 ID（`fig_7K3M9Q.md`），以消除重命名断链。代价是可读性。

**Decision（待批）**：建议**分区执行**——
- 机器实体（Figure / Panel / Asset / Reference）用 ID 文件名
- 人类实体（Manuscript / Section）用可读文件名 + `id` 字段

**Why not all-ID**：作者会直接在文件浏览器里找稿件，全 ID 文件名会让 Vault 不可用。
**Why not all-readable**：Figure 重命名会导致 `[[...]]` 断链，而 Figure 改名是高频操作。

**Needs**：用户确认是否接受混合方案。

---

## D-06 编号渲染时解析

**Context**：Worker C 主张编号是派生量；Worker A 证明 post-processor 与 CM6 装饰器都是公开 API，但底层 `EditorView` 访问未类型化。

**Decision**：默认渲染时解析；保留"写入时固化 + 重排命令"作为降级路径；导出时强制固化。

**Consequences**：正文中的字面量 `Figure 3` 被校验规则拦截；渲染失效时用户体验降级但不丢数据。

---

## D-07 Bases 只作浏览层

**Context**：Worker A 证明 Bases 的 `QueryController` 是空类，查询只能通过 `.base` 文件语法，插件无法在任意上下文执行查询；且 Bases 是"文件为行"模型。

**Decision**：Bases 只用于一文件一实体的只读表格。反向关系与聚合视图由引擎生成 JSON，插件用 ItemView 渲染。

**Alternative rejected**：把业务规则写进 `.base`（不可测试、不可版本迁移、无法在导出时复用）。

---

## D-08 修订三层

**Context**：Worker B 明确 Markdown 无法无损承载 Track Changes，给出四种退路并推荐 Sidecar JSON。

**Decision**：Sidecar JSON（Word 修订语义）+ RevisionRound 快照（回滚）+ Git（提交历史）。三者职责不重叠。

**Consequences**：导出时需从 sidecar 重建 `w:ins`/`w:del`，重建保真度是 Phase 3 的核心验收项。

---

## D-09 分发形态与开源复用 — ACCEPTED（2026-11-07）

**Decision（用户裁定）**：本项目以**宽松许可证开源**（MIT 或 Apache-2.0，二选一待定）。据此：

1. **不 Fork 任何开源项目**，Reference-only 为主，Manubot 作有限 Adapt（BSD-2-Clause-Patent 与宽松许可兼容）。
2. **TeXlyre / Oleafly（AGPL-3.0）仍不可用**：AGPL 的传染义务与 MIT/Apache-2.0 目标许可不兼容，只能作 Reference。
3. **Quarto 现行版本（MIT）可用**；早期 GPL-2.0 版本不可合入。
4. **Pandoc（GPL-2.0-or-later）仅以独立进程调用**；随产品分发二进制须履行 GPL 义务（见 `research/open-source-audit/PANDOC_BOUNDARY.md`）。

**Consequences**：
- 开源复用结论与裁决前**完全一致**——宽松许可并没有解锁 AGPL/GPL 代码，只是把「法务阻断」从「闭源冲突」换成「许可不兼容」。
- SaaS 场景不再触发 AGPL 的源码提供义务（因为项目本身不含 AGPL 代码）。
- **仍待定**：MIT vs Apache-2.0。二者在复用结论上等价，差异在专利条款（Apache-2.0 含显式专利许可与 retaliation 条款）。代码落地前必须定。
- 开源后需配套：贡献者许可（DCO 或 CLA）、第三方依赖清单（NOTICE / THIRD-PARTY）、以及 Phase 1 起每个依赖的许可证登记。

---

## D-09 原始记录 — 不 Fork 开源项目

**Context**：Worker D 建议 Fork Quarto（MIT），Adapt Curvenote Editor（MIT）与 Manubot。

**Decision（待批）**：改为 **Reference-only 为主**，Manubot 仅作有限 Adapt（借鉴 citation CLI 契约）。不 Fork 任何项目。

**Rationale**：
- Quarto 是打包的 CLI 发行版，Fork 等于接管一个大型工具的维护，与本项目目标不匹配；且 MIT 允许调用其二进制，无需 Fork。
- Curvenote Editor 是 ProseMirror 栈，Obsidian 是 CM6，编辑器层无法复用，只能借鉴 schema 设计。

**Consequences**：无 copyleft 传染风险；但需要自研编辑体验的科研特化部分。

---

## D-10 WritingLab Core — PENDING

**Context**：用户要求评估其是否适合作为可选 Adapter。

**Decision（待批）**：定位为可选 Adapter，默认不依赖。接入须满足三条硬约束：不改 Core、不把 Core 数据结构泄漏进 L1、Core 缺失时功能不降级。

**Needs**：用户确认是否在 Phase 1 就做接口预留，还是 Phase 4 之后再评估。

---

## D-11 移动端只读 — PENDING

**Context**：Worker A 证明移动端无 Node/Electron API。

**Decision（待批）**：移动端为阅读端，不提供导入、导出、全库校验。

**Needs**：用户确认产品边界。

---

## D-12 Vault 目录结构 — PENDING

**Decision（待批）**：采用架构文档 §3 的目录布局（`Manuscripts/ Figures/ Results/ Methods/ Experiments/ Claims/ References/ Assets/ _maps/ _index/`）。

**Needs**：用户确认命名与是否与现有 Vault 合并。

---

## D-13 核心技术栈 — PENDING

**Decision（待批）**：
- 引擎：Python 3.11+（lxml / python-docx / PyYAML），Pandoc 作为导出后端
- 插件：TypeScript，Obsidian 官方 API，无框架
- 索引：JSON（<5k 实体）→ SQLite（超出）

**Needs**：用户确认。若倾向 Node 引擎（mammoth.js / docx），需重新评估 Track Changes 能力（当前证据表明不足）。

---

## D-14 实体分期

**Context**：Worker C 自审 W3 指出 17 实体对 Phase 1 过重。

**Decision**：Phase 1 只实现 Manuscript / Section / Paragraph / Figure / Panel / Asset；Result / Method / Experiment / Claim 在 Phase 2-3；Reference / Citation 在 Phase 4。

**Consequences**：Schema 必须从第一天就带 `schema_version` 与迁移链。

---

## D-15 原始件不可变

**Decision**：`Assets/` 只增不改；内容按 `sha256` 寻址；ingest 前校验哈希，不匹配即中止。

**Consequences**：重复导入同一文件会产生相同哈希、复用同一 Asset；修改过的原稿被视为新 Asset，旧映射表标记失效。

---

## 待用户批准清单（Phase 1 启动前必须全部落定）

1. D-05 文件名策略
2. D-09 开源复用策略（是否允许 Fork）
3. D-10 WritingLab Core 接入方式与时机
4. D-11 移动端定位
5. D-12 Vault 目录结构
6. D-13 核心技术栈
7. Phase 1 是否启动

---

## D-16 阻断项关闭的判据与独立性

**Context**：Phase 0 复审（claude）在初稿判 FAIL 后，自行把 B3 判为 CLOSED 并将总体改为 PASS WITH RISKS，理由是「那四处文法问题超出 B3 原始范围」。第三方交叉验证（codex）逐字比对上一轮 QA 对 B3 的原文后裁定：**该降级不成立，当时应维持 FAIL**——(a) `#panel` 规范↔正则矛盾正是 B3② 的原始缺陷，(c) `fig_a/fig_b` 非法示例正落在 B3 点名的 §6.7。降级靠的是把「三处一致」缩窄为「三个字面位置一致 + 向量全绿」，排除了新建单一定义内部的散文↔正则自洽性。

**Decision**：
1. 阻断项是否关闭，**以原始审计报告对该项的原文为唯一判据**，不得由修复方或复审方重新界定范围。
2. 修复方不得承担同一批次的复审；复审方不得是本次修复的实施者。
3. 复审报告若在成文后修改判定，必须保留初稿判定与修改理由，且该修改本身须经独立方复核。

**Consequences**：Phase 0 的 PASS WITH RISKS 成立，但依据是门禁修复（`7b1890d`）实质关闭了缺陷，**不是**那次降级。此后每轮关闭都需一次独立复核；在只有单一 agent 可用的极端情况下，必须在报告中显式标注「弱独立性验证」。

**Evidence**：`reports/qa/PHASE_0_CROSS_VALIDATION.md` §2、§6-1。

---

## D-09 补充：分发形态是前置决策

AGPL（TeXlyre / Oleafly）与 GPL（Quarto、Pandoc）的结论全部依赖分发形态，而 D-09 仍为 PENDING。已做两处处理：
- 开源报告开头改为显式条件句 + 两情形差异表；
- `SYSTEM_ARCHITECTURE.md` §9 的 AGPL 行补条件标记（不再写成无条件结论）。

**未决**：项目是闭源分发、开源分发（MIT/Apache）、还是仅自用不分发？这三种情形下 AGPL/GPL 的义务完全不同，**必须在 Phase 1 动手前定**。

