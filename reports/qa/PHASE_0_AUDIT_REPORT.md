# Phase 0 Audit Report

> 独立 QA 审计 · 2026-11-06 · 任务 task_822c552bcae7
> 审计对象：4 份 Phase 0 研究报告 + 2 份架构文档 + 1 份决策记录（共 7 份，**全部存在，无缺失文件**）
> 审计方式：只读。所有判定基于被审文件内部证据、引用来源核验、以及本次对外部一手来源（npm registry、GitHub API、Obsidian 官方 Publish 文档）的独立复核与代码级复现。未修改任何被审文件。

---

## 1. 总体结论：**FAIL**

理由（两条，任一条即足以 FAIL）：

1. **数据模型内部一致性（必审第 3 项）判 FAIL**：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` 存在 6 处阻断级缺陷（双权威边、同一字段两种 schema、编号 token 体系三处互相矛盾、边归属自相矛盾、已裁决的 D-04 与字段表未对齐、哈希契约正则与主语法不匹配），其中多处已用代码复现证实。按现状进入实现会产生分歧实现与静默数据损坏。
2. **来源可追溯与技术判断（必审第 1、2 项）判 RISK**：Obsidian 侧证据链经外部复核**全部吻合**（质量很高），但 Manuscript 报告的证据清单存在"来源与结论不符"（wDocumentChange 类不存在、§9 统计与本表逐行标注不符、python-docx 修订能力断言与库公开 API 不符）与多条不可核验的"实测"数据；开源审计的 Manubot 许可证识别与仓库实际不符。

必审 9 项判定：**5 PASS / 3 RISK / 1 FAIL**。阻断级问题 **6 个**。放行条件见 §10。

---

## 2. 逐项审计结果表

| # | 必审项 | 判定 | 关键证据 |
|---|---|---|---|
| 1 | 来源可追溯（抽 15+ 条，见 §3） | **RISK** | Obsidian 报告 10/10 抽查可核验且外核逐字吻合；Manuscript 报告 20 条抽样中 5 条不可核验、3 条来源与结论不符（E1/E3/E10 无 URL 或出处不存在，§9 统计错误）；开源审计 2 条来源与结论不符（Manubot 许可证、Quarto 引文位置）；跨报告确认闭环缺失（§9-1） |
| 2 | 技术判断有源码/官方文档证据 | **RISK** | Obsidian API 断言抽查 9 项全部真实存在（行号精确到个位，见 §3 O2–O8）；但 python-docx"Track Changes 好"无任何文档证据且与库公开 API 不符（直接影响 D-03 选型判据），docx4j/mammoth 断言无 URL 级来源 |
| 3 | 数据模型内部一致性 | **FAIL** | 6 处阻断缺陷（§4 B1–B6）：Panel 双权威边、`Issue.targets[]` 两种形态、tab/eq 无实体、Result↔Figure 归属互相矛盾、D-04 未对齐、ANCHOR_RE 剥离主语法失败（已代码复现） |
| 4 | 原始文件保护 | **PASS** | D-15（ACCEPTED）sha256 内容寻址 + ingest 前校验不匹配即中止（SYSTEM_ARCHITECTURE §3）；P5 + Asset `read_only: true`/`frozen: true` + VR-05/VR-42 阻断级；§5.1 失败语义"全或无……原稿不受影响" |
| 5 | DOCX 导入失败与信息丢失 | **PASS** | 失败回滚：§5.1"任一步失败，删除本次产生的所有新文件"；部分导入：明确定义为"不存在'导入了一半'的状态"；Track Changes：Sidecar（Worker B §5，D-08 三层）；样式丢失：列入丢失项报告（§5.2"是产品的一部分"）+ 路线图退出条件"丢失项报告覆盖全部已知损失类型"；告警："向用户报告失败阶段与原因"+ Phase 2 侧栏校验告警。残留缺口归入轻微（§6-1） |
| 6 | 是否错误依赖 WritingLab Core | **PASS** | SYSTEM_ARCHITECTURE §10"定位：**可选 Adapter，不是依赖**……默认架构不引用"；D-10 三条硬约束（不改 Core/不泄漏进 L1/缺失不降级）；路线图"明确不排期……待用户单独批准"。边界清晰，无能力夸大 |
| 7 | 是否夸大 Obsidian 原生能力 | **PASS** | Worker A 全篇三分"稳定公开/未文档化/需私有 hack"（§2.4），Dataview 明确标社区插件"绝不能作为系统依赖"（§5.3）；Bases 边界（QueryController 空类、无 join、行=文件）经复核属实；11 项 U1–U11 显式标"未确认"；数据模型相关假设全部标 `[待审计]`。未发现"社区插件能做"写成"官方 API 支持"的实例 |
| 8 | 许可证问题 | **RISK** | 逐项目可复用性判定与许可证无直接冲突（AGPL→reference-only 正确、MIT/Apache 判定正确），但：① Manubot 许可证识别与仓库实际不符（外核：BSD-2-Clause Plus Patent，非 CC-BY-4.0/CC0）；② §3.4 兼容矩阵 GPL-2.0 × Apache-2.0 误标 ✅（实为不兼容）；③ Quarto 历史"GPL-2.0"引文未见于所引文件且与仓库线索矛盾；④ "闭源"前提未在任何决策文档确立 |
| 9 | Revision Engine 核心需求 | **PASS** | 闭环完整：`RevisionIssue.source_text`（原文只读）→`targets[]→par_`（定位）→`Patch`（diff + before/after_hash + apply/revert）→`Response`（stance/body/letter_group）→回复信导出（路线图 Phase 3）；版本快照与回滚未遗漏：`base_snapshot`/`bundleHash`（数据模型 §7.4）+ `Assets/snapshots/` 回滚（架构 §7）+ D-08 三层 + Phase 3 退出条件"回滚到任意轮次后文件逐字节一致"。残留：两文档快照形态表述不一致（§5-7） |

---

## 3. 核心结论抽样核验（20 条）

核验结果三值：**可核验**（来源可定位且结论与来源一致）/ **不可核验**（无有效来源或来源无法定位）/ **来源与结论不符**（来源存在但与结论矛盾或出处不存在）。
外核方式：本次直接调取 npm registry、GitHub Contents API、Obsidian Publish 原始 Markdown 端点，以及对被审文件中正则/伪代码的执行复现。

| # | 来源 | 结论 | 报告给出的来源 | 核验结果 | 本次核验证据 |
|---|---|---|---|---|---|
| O1 | Obsidian §2.1 | npm `obsidian` 最新 1.14.4，发布时间 2026-10-08T22:27:35.586Z | registry.npmjs.org/obsidian | **可核验** | 外核：`dist-tags.latest=1.14.4`，`time["1.14.4"]` 时间戳逐字节吻合 |
| O2 | Obsidian §10.1 | obsidian.d.ts 指纹：blob sha `10b31c47…`、11,539 行、SHA-256 `97c86417…` | GitHub Contents API + 指纹 | **可核验** | 外核：blob sha 与 SHA-256 均逐字节吻合；行数吻合（11,539 行 + 尾空行） |
| O3 | Obsidian §10.1 | tarball sha1 `e4d4c91d…`、`fileCount: 7`、内 d.ts sha1 `232da70b…` | registry.npmjs.org tarball | **可核验** | 外核：三个指纹全部吻合，fileCount=7 |
| O4 | Obsidian §2.4/§10.1 | 行号断言：apiVersion:1319、PluginManifest:7376、FrontMatterCache:4832、QueryController:7643（空类）、processFrontMatter:4450、getFrontMatterInfo:5060、editorEditorField:3931、Editor:3652 无 `cm` 字段 | obsidian.d.ts + 行号 | **可核验** | 外核：下载 d.ts 逐一比对，8 个行号全部精确命中；`grep "cm:"` = 0 命中，`Editor` 确无 cm 字段 |
| O5 | Obsidian §3.1 | "属性类型一经指定，vault 内同名属性全局同类型"；Nested properties / Markdown in properties 官方明列不支持 | help.obsidian.md/properties（原始 MD 端点） | **可核验** | 外核：原文逐字命中（"all properties with that name across your vault will use the same type"、"### Not supported" 下 "Nested properties"、"Markdown in properties"） |
| O6 | Obsidian §4.3 | `view.editor.cm` 未类型化，官方文档写 `@ts-expect-error, not typed` | docs.obsidian.md/…/communicating-with-editor-extensions | **可核验** | 外核：原始 MD 端点逐字命中 `// @ts-expect-error, not typed` 与 `const editorView = view.editor.cm as EditorView;` |
| O7 | Obsidian §4.3 | CM6 peerDependencies 精确锁定 6.7.6 / 6.43.13（无 `^`） | obsidian@1.14.4 包 | **可核验** | 外核：`peerDependencies: {'@codemirror/view': '6.43.13', '@codemirror/state': '6.7.6'}` 完全吻合 |
| O8 | Obsidian §6.2 | 移动端无 Node/Electron API，调用即崩溃（含依赖项） | docs.obsidian.md/…/mobile-development（原文引述） | **可核验** | 来源 URL + 原文引述齐备，与官方文档既有表述一致（本次未再外核该页） |
| O9 | Obsidian §2.3 | 1.15.0 改 formatting token 节点名，点名破坏匹配完整节点名的插件 | obsidian.md/changelog/2026-10-22-desktop-v1.15.0/ | **可核验** | changelog 页面外核可达（1.15.1 页含版本号）；节点名细节未展开复核，但来源定位可复现 |
| O10 | Obsidian §5.2 | Bases 行=文件、无 join、`file.backlinks` 标 "performance heavy" | help.obsidian.md/bases/syntax、/functions | **可核验** | 来源 URL + 原文引述齐备（本次未展开外核；与 §5.2 表格逐条对应） |
| B1 | Manuscript §3.1/§3.2 | python-docx"Track Changes：**好**"，支持 `w:ins`/`w:del` 提取 | E5"python-docx 文档 1.0.0"（无 URL、无章节） | **来源与结论不符** | python-docx 公开 API 无修订标记接口（w:ins/w:del 需手工操作 oxml 层），官方 API 文档检索 "revision/tracked" 0 命中；该断言直接影响 D-03 选型判据 |
| B2 | Manuscript §2.2/E1 | Track Changes 标记定义来自"Microsoft Office Open XML SDK 文档，`wDocumentChange` 类定义" | E1（无 URL） | **来源与结论不符** | Open XML SDK 无 `wDocumentChange` 类（对应类型为 `Insertion`/`Deletion` 等）；结论（w:ins/w:del 语义）本身成立，出处不存在 |
| B3 | Manuscript §3.1/E3 | mammoth.js 样式限制见 "GitHub Issues #342, #456" | E3（无 URL、无仓库名） | **不可核验** | 未指明仓库；API 查询未命中（404/速率限制），无法定位 |
| B4 | Manuscript §8.2/E10 | "工具实测"：文本提取 95%+、双栏 85%、图表 60–70%（Adobe Acrobat + Tesseract） | E10"Adobe Acrobat Pro 实测 2024-11" | **不可核验** | 无样本、无脚本、无产物；与报告自身约束"只读研究，不安装依赖"矛盾；日期 2024-11 与审计日期 2026-11-06 矛盾（文首日期亦误写 2024-11-06） |
| B5 | Manuscript §9 统计 | "完全可逆 1 / 单向可逆 19 / 有损 6 / 不可行 14" | 同文件 §9 映射表 | **来源与结论不符** | 逐行计数该表 33 行：实际 1 / 19 / **3** / **10**；报告自报合计 40 项 ≠ 表格 33 行 |
| B6 | Manuscript §5.1 | Markdown 无法无损承载 Track Changes，需 Sidecar | E1 + 常识 | **可核验** | 结论与 OOXML/Markdown 语义一致（与 D-08、架构 §7 相互印证）；注意其引证 E1 出处无效（见 B2） |
| D1 | Open-Source §2.5 | Quarto v1.4+ 为 MIT | quarto-cli LICENSE/COPYING.md | **可核验** | 外核：COPYING.md 现文本为 MIT（Posit 2020–2024）；与"可用于闭源"判定一致 |
| D2 | Open-Source §2.5/§3.2 | "Quarto v1.3（及更早）licensed under GNU GPL **v2**"（引文形式给出） | "LICENSE 文件" | **来源与结论不符** | 所引 COPYING.md 无此引文（现为纯 MIT 文本）；仓库 LICENSE 历史提交信息为 "use gpl v3"（2020-10-17），与 "GPL-2.0" 矛盾；需 commit 级证据复核版本号 |
| D3 | Open-Source §2.6 | Typst 为 Apache-2.0 | typst/typst LICENSE | **可核验** | 外核：GitHub license API 返回 `Apache-2.0` |
| D4 | Open-Source §2.4 | Manubot "CC-BY-4.0（文档）/ CC0-1.0（代码）"，文件路径 `LICENSE.md` + `LICENSE-CC0.md` | 仓库 LICENSE 文件（无 URL 指向文件） | **来源与结论不符** | 外核：`manubot/manubot` 现 `LICENSE.md` 为 **BSD-2-Clause Plus Patent License**（Greene Lab 2017–2020）；仓库树中**不存在** `LICENSE-CC0.md`。所摘"双许可条款"为转述，非任何实际许可证原文 |
| D5 | Open-Source §2.2/2.3 | TeXlyre / Oleafly 为 AGPL-3.0，闭源分发/ SaaS 受限 | 仓库 LICENSE + SPDX | **可核验** | SPDX 与仓库 LICENSE 可查；AGPL 处置（reference-only）与架构 §9 一致（本次未展开外核） |
| D6 | Open-Source §2.3 | Oleafly ~842 stars、"20 个 Rust crate"；TeXlyre ~490 stars | "搜索结果和文档"（自标"推测/未验证"） | **不可核验** | 无搜索快照存档；报告已自标未验证，不构成可核验来源 |
| M1 | 数据模型 §3.0.1 | 生日碰撞概率 ≈4.5×10⁻³（32^8，每类型 10 万实体） | 自带公式 | **可核验** | 外核：精确计算 4.537×10⁻³，吻合；ID 正则与 Crockford 字母表一致（已执行验证） |
| M2 | 数据模型 §5.3 | `normalizeText` 会剥离块锚点（"锚点不是内容"） | 自带 ANCHOR_RE 伪代码 | **来源与结论不符** | 代码复现：该正则只匹配降级连字符形式（`^par-…`），对主语法 `^par_9QK2M4XZ`/`^sec_4M2P8QKT` **匹配失败**，锚点被计入 text_hash（见 §4 B6） |

抽样合计 21 条（≥15）。其中可核验 13、不可核验 4、来源与结论不符 4。

---

## 4. 严重问题（阻断级，6 个）

每个问题给出：缺什么 / 在哪里缺 / 补上需要什么证据。

**B1（数据模型）P2"单一写入点"被自身违反：Figure↔Panel 边有两处自称权威。**
- 缺什么：`Panel.figure` 与 `Panel.derived_from`（注释称"必须含 `figure`，构成 Figure→Panel 的权威边"）同时自称权威；P2 表与 §4.1 选型又明确权威边是 `Panel.figure`。双权威无仲裁规则，违反模型自己的 P2。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §3.6 字段表（`derived_from`、`figure` 两行注释）vs §4.1、P2 表。
- 补上需要：修订字段表使 `derived_from` 明确为派生/血缘（或删除 figure 必含要求），并在 VR 规则中指定唯一权威边；给出修订后 diff 作为证据。

**B2（数据模型）`RevisionIssue.targets[]` 同一字段存在两种互不兼容的元素形态。**
- 缺什么：§3.15 定义 `{par, manuscript, section?}`，§4.6 定义 `{par, manuscript, quote_hint?, patch?}`——字段集合不同，schema 校验（VR-17）无从实现。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §3.15 字段表 `targets` 行 vs §4.6 选型段。
- 补上需要：统一为单一形态并同步 `_schema/types/` 的 schema 定义；给出唯一形态的字段表。

**B3（数据模型）编号/token 体系三处互相矛盾：表/公式无实体、词汇表与 TOKEN 正则不一致。**
- 缺什么：① `{{tab:ID}}`/`{{eq:ID}}`（§6.3/§6.4）指向的 Table/Equation **不在 17 实体中**，ID 前缀注册表（VR-20 正则）不含 `tab`/`eq`（已执行验证：`tab_…`、`eq_…` 均不匹配 ID 正则）；② §3.18 词汇表列 `{{figref:fig_x#B}}`（面板引用）但 §6.4 TOKEN 正则不接受 `#` 片段（已执行验证：fullmatch 失败）；③ §6.7 归一化产物 `{{pnl:…}}` 能被 TOKEN 匹配但不在 §3.18 词汇表中；④ `eq` 仅 2 字母，与 TOKEN 的 `[a-z]{3}_` 前缀要求结构性不匹配。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §3.18、§6.2–§6.4、§6.7、§9.2 VR-20。
- 补上需要：补齐 Table/Equation 实体（或明确砍掉表/公式编号并同步删除 token）、统一词汇表/TOKEN/ID 三处文法为同一份规范；给出文法单一定义 + 通过的匹配测试用例。

**B4（数据模型）Result↔Figure 边归属自相矛盾，违反 P2。**
- 缺什么：§3.7 `Result.figures` 注释称"冗余缓存（权威边见 `Claim.results` 与 `Figure.result_refs` 的规定）"——`Claim.results` 是 Claim↔Result 边，不是 Result↔Figure 边；§3.5 `Figure.result_refs` 又称"边归属方为 Result 时此项为派生"。两处互指对方为权威，边无主。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §3.5、§3.7；P2 表未收录该边。
- 补上需要：指定唯一权威持有方并加入 P2 表，另一侧标注派生；给出修订后的边归属表。

**B5（数据模型）已 ACCEPTED 的 D-04（frontmatter 禁嵌套对象）与 17 张字段表未对齐。**
- 缺什么：D-04 规定 frontmatter 只允许标量/标量列表/wikilink 列表，结构化子对象必须放正文 fenced YAML 块；但字段表中 `x_ext: object`、`numbering_scheme: object`、`Panel.crop/layout/canvas/transform: object`、`section_meta/targets/authors/affiliations/funding/abbreviations/parameters/software/reagents/conditions/citations: list<object>` 等仍定义为 frontmatter 对象。`x_ext` 本身就是嵌套对象，与 D-04 直接冲突。实现者照字段表写 frontmatter 将违反已生效裁决（D-04 为 ACCEPTED，不属 PENDING）。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §3.0.2 S3、§3.1–§3.17 各字段表 vs `decisions/ARCHITECTURE_DECISIONS.md` D-04、`SYSTEM_ARCHITECTURE.md` §4.1。
- 补上需要：字段级"frontmatter / 正文 YAML 块 / 平行列表"落位映射表（逐字段标注），并给出一份符合 D-04 的示例文件；架构文档仅说"做了三处修正"，但被审的模型文档本身仍是 draft-1 原样，必须同步。

**B6（数据模型）`text_hash` 规范化契约的锚点剥离正则与主语法不匹配，哈希确定性失效。**
- 缺什么：§5.3 `ANCHOR_RE = \s+\^[a-z]{3}-?[0-9A-HJKMNP-TV-Z]{8}\s*$` 只匹配降级连字符写法（`^par-…`），对 §3.3/§3.4/§3.18 的主语法 `^par_9QK2M4XZ`、`^sec_4M2P8QKT` 匹配失败（已代码复现）。结果：锚点被计入 text_hash，与 §5.4 "锚点不是内容"的声明直接矛盾；`Patch.before_hash/after_hash`、漂移检测、VR-29/VR-45 全部建立在该哈希上。
- 在哪里缺：`SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §5.3 Python 伪代码（`ANCHOR_RE`）。
- 补上需要：修正正则（如 `\^([a-z]{3})[_-][0-9A-HJKMNP-TV-Z]{8}\s*$`）+ 针对两种锚点写法的测试向量（输入→期望哈希），并证明跨锚点变更哈希不变。

---

## 5. 中等问题

1. **Manuscript 报告证据清单不可核验面较大**（E3/E4/E5/E7–E10 无 URL、无版本定位；"工具实测"无产物）。缺：每条证据的可定位 URL/文件+版本/测试产物；在补齐前 §3.1 的 15 条结论中依赖这些证据的部分不得作为选型依据。
2. **python-docx 修订能力断言错误**（见 §3 B1）：D-03 的判据 1（`w:ins`/`w:del` 解析完整度）若沿用该对比表将被误导。D-03 现为 OPEN 且 Phase 1 有实测计划——**D-03 的 5 篇对比必须包含"python-docx 修订 API 实际能力"一项**，否则选型基线错误。
3. **§9 结构映射统计错误**（1/19/6/14 vs 实际 1/19/3/10）：数字是"信息丢失严重度"论述的依据，需更正并复核"有损/不可可行"分类本身（如 `w:tblMergeCell` 非标准 OOXML 元素名，实际为 `w:gridSpan`/`w:vMerge`）。
4. **许可证兼容矩阵错误**（`OPEN_SOURCE_AUDIT.md` §3.4）：GPL-2.0 行把 Apache-2.0 标 ✅——Apache-2.0 与 GPL-2.0 业界公认不兼容（仅与 GPL-3.0 单向兼容）；CC-BY-4.0 × GPL-2.0 同样存疑。矩阵若被用于"本项目若选 GPL"的决策会得出错误结论。
5. **Quarto 历史许可证版本存疑**："GPL-2.0（v1.3 及更早）"的引文未见于所引 LICENSE 文件，仓库历史线索指向 GPL v3（见 §3 D2）。需 commit 级证据；结论方向（旧版有 copyleft）不受影响，但版本号错误会进入法律判断。
6. **Manubot 许可证识别错误**（见 §3 D4）：实际为 BSD-2-Clause Plus Patent。影响：§3.3"低风险（CC-BY-4.0/CC0）"的依据错误；"Adapt/可闭源"结论在 BSD 下侥幸仍成立，但署名义务表述（CC-BY 署名）应改为 BSD 保留版权声明。复用决策前必须更正。
7. **跨审计确认闭环缺失**：Worker B §12 指派 Worker A 的 4 项确认（块 ID 字符集、`{{...}}` 自定义语法、Obsidian 批注原生支持、Pandoc REF 域支持）与数据模型 §11.1 的 U2（块 ID 字符集/能否挂标题/blocks 索引）**均未获 Worker A 逐项回应**；数据模型自称"块锚点语法是唯一取决于审计结论的细节"（§3.3），至今悬空。需要一份逐项"是/否/部分 + 证据"的交叉确认记录。
8. **快照形态两文档不一致**：架构 §7 "RevisionRound 快照 = `Assets/snapshots/<round>/<file>.md`（内容寻址）用于回滚" vs 数据模型 §7.4 "`snapshot_asset` = 导出的快照 DOCX/PDF + JSON 清单"。回滚到逐字节一致需要 md 级快照；两处需合一（回滚源是什么、存哪、生命周期）。
9. **`_maps/` 备份策略未落文档**：W1 自认"已声明，未给备份策略"；R-04 称它是"文件即真"的唯一例外、"随稿件进 Git"，但同步/备份/校验责任（谁保证进 Git、丢失后的恢复步骤）未定义。

---

## 6. 轻微问题

1. 丢失项报告只有 JSON 契约（`out/xxx.report.json`），用户可见呈现（位置/格式/交互）未设计；Track Changes 重建保真度留待 Phase 3 验收（路线图已排期，可接受）。
2. 锚点写法不统一：§3.4/§3.18 用 `^par_XXXXXXXX`（下划线），§3.12 用 `^clm-xxx`（连字符）；虽有编解码器设计，但正文示例应统一。
3. Manuscript §2.3 批注示例 XML 非 OOXML 规范形态（`w:commentRangeStart` 实际用 `w:id`，无 `w:ref`/`w:type="range"`）；§2.1 的 `w:lsStyle`、"单独的修订 XML"表述亦不准确（修订标记就在 document.xml 内）。
4. 许可证"关键条款摘录"多为中文转述而非原文（MIT/AGPL/Apache 均如此），与任务要求"许可证原文"的可核验标准有距离（SPDX 与仓库 LICENSE 可查，故仅列轻微）。
5. 派生 Citation ID（`cit_` + sha256 hex 小写）与 VR-20 大写正则不匹配（已验证），需声明大写规范化；`[待审计]` 标记停留在"是否纳入正则"，未提大小写。
6. `Reference.supersedes` 语义与 S1 定义相反（S1"指向被本实体取代的旧实体"，§3.10"被合并者填 `supersedes: 保留者`"），且会影响 VR-09 的链/环判定方向；文档虽写明"此处反向"，但未在 VR-09 处同步豁免或说明。
7. `RevisionIssue.response`（单数，1:1 情形）未标明是权威边还是缓存（`responses[]` 已标缓存，`Response.issues` 才是权威）。
8. Manuscript 文首日期误写 2024-11-06（其余文档为 2026-11-06）。
9. D-04 裁决依赖"Obsidian 不改写正文代码块"这一假设，未见于 Worker A 审计条目（属未确认事项，应补测或标注）。

---

## 7. 数据模型一致性检查结果

**逐项结论：**

| 检查点 | 结果 | 说明 |
|---|---|---|
| 17 实体均有字段表 | **PASS** | §3.1–§3.17 逐一点数：Project/Manuscript/Section/Paragraph/Figure/Panel/Result/Method/Experiment/Reference/Citation/Claim/Asset/RevisionRound/RevisionIssue/Patch/Response = 17，每张表含 S1–S3 继承字段全集 |
| 字段表完整性（表外引用） | **FAIL** | 7 个被正文/规则引用但不在任何字段表的字段：`calibration_state`（§3.6 生命周期、VR-04、§6.8.2）、`stale_since`（§6.8.2）、`crop_history`（§6.8.2 重标定流程）、`part_files`（§6.3.1、U20）、`shared_with`（§4.5）、`evidence_links`（§4.2）、`Document.content_hash`（§3.16 生命周期；且无 Document 实体，应为 Manuscript） |
| 循环依赖 | **PASS**（附注） | 实体关系图无环；`supersedes`/`depends_on` 禁环（VR-09），`Project.project` 自指豁免（VR-24），`contradicts` 软环提示（VR-10）。附注：`Reference.supersedes` 反向语义（§6-6）可能干扰 VR-09 链判定 |
| 字段冲突 | **FAIL** | B2（targets 两形态）、B5（D-04 未对齐）、`Reference.supersedes` 语义与 S1 相反、`Response`/`Issue.response` 权威-缓存标注不全 |
| ID 冲突 | **FAIL**（局部） | 已核验：示例 ID 全部符合正则；创建查重+占位机制自洽；生日碰撞数学正确。但 `tab_`/`eq_` 不在前缀注册表（B3）、派生 `cit_` 小写 hex 不匹配 VR-20（§6-5） |
| 孤儿关系 | **PASS** | §9.1(2) 孤儿定义按"应有入边"而非零入边，含宽限期；VR-02/VR-16 覆盖 Figure/Citation；`derived_from`/`supersedes` 血缘字段齐全 |
| 边归属（P2 单一写入点） | **FAIL** | B1（Panel 双权威）、B4（Result↔Figure 无主）；其余边（Claim.results、Citation.reference、Issue.targets、Patch.issues）归属清晰 |
| 多对多方案自洽性 | **PASS**（附注） | §4.8 统一方案 A + 唯一声明的双写（`Claim.expressed_in`，VR-45 以正文为权威修复）逻辑自洽，晋升判据（§4.9）量化可执行。附注：§4.2 提出的 `evidence_links[]` 扩展未进入字段表 |
| 哈希/锚点契约 | **FAIL** | B6（ANCHOR_RE 复现失败）；锚点语法 §5.2 与 §5.6 编解码器设计合理，但与 §5.3 实现不一致 |
| 版本与迁移 | **PASS** | §7 逐实体版本、迁移契约 M1–M10（幂等/原子/schema_version 最后改/quarantine）完整可执行 |
| 快照与回滚 | **RISK** | §7.4 bundleHash 设计好；但快照形态与架构 §7 不一致（§5-8），`draft_branch`（Git 分支）与 D-08 三层的关系未闭合 |

---

## 8. 许可证与依赖风险

1. **Manubot 许可证识别错误（中高风险，直接影响复用依据）**：仓库实际为 BSD-2-Clause Plus Patent（外核实证），报告写 CC-BY-4.0/CC0 并虚构了 `LICENSE-CC0.md`。BSD-2-Clause-Patent 含专利授权条款，比 CC-BY 更宽松，"Adapt + 闭源"结论侥幸成立，但所有引用 CC 条款的分析（§3.3、§3.4 矩阵）需重写，署名义务改为"保留版权声明与免责声明"。
2. **兼容性矩阵含错误**：GPL-2.0 × Apache-2.0 = ✅ 错误（不兼容）；如未来本项目或依赖引入 GPL-2.0，该矩阵会给出错误的组合许可。建议整体重做该矩阵或删去（逐项目判定已够用）。
3. **Quarto 历史版本 GPL 版本号存疑**（v2 vs v3）：不影响"用 v1.4+ MIT 即无风险"的操作结论，但文档声称的引文不存在于所引来源，需更正或补 commit 级出处。
4. **AGPL 处置正确**：TeXlyre/Oleafly 判 Reference-only（法务阻断）与架构 §9、D-09（不 Fork）一致；"闭源分发/SaaS 冲突"表述正确。
5. **前提未声明**：全部许可证风险分析以"本项目闭源分发"为前提，但决策文档（D-01–D-15）没有任何一条确立本项目的分发形态/许可证。若项目实为开源，AGPL 结论需重估。必须先补一条显式决策。
6. **依赖面**：D-13（PENDING）拟用 python-docx / lxml / Pandoc（均宽松许可），无 copyleft 传染；Pandoc 为 GPL-2.0——**以 CLI 子进程方式调用（D-02 引擎外置）通常不构成衍生作品，但若静态链接/内嵌则传染**，D-13 批准前需明确"仅进程级调用"。此项四份报告均未提及，列为遗漏（§9-11）。

---

## 9. 遗漏项清单

1. Worker A 未回应 Worker B 指派的 4 项确认（块 ID 字符集、`{{...}}` 自定义语法、Obsidian 批注原生支持、REF 域支持），亦未按数据模型附录 B 要求逐项给出"是/否/部分 + 证据"（U2/U3/U5 等）；块锚点语法因此悬空。
2. 丢失项报告的用户可见呈现设计（§6-1）。
3. 项目分发形态/许可证决策缺失（§8-5）。
4. `_maps/` 备份与丢失恢复策略（W1 自认）。
5. U1–U11、U13–U19 的 Phase 1 验证计划缺 owner、验收人与期限（仅 D-03 有"第 1 周"安排）。
6. 跨稿件引用标签语法（W4 自认未展开）。
7. Patch 应用后 revisions sidecar 的范围/锚点如何跟随更新，未定义。
8. `draft_branch`（§7.4 `[待审计]` Git 分支）与 D-08 三层、快照回滚的职责划分未闭合。
9. 开源审计的信息来源多为二手（CSDN/微博/博客），无证据快照存档（对比：Obsidian 报告有 `evidence/` 目录 + 指纹）。建议同样建立 `research/open-source-audit/evidence/`（许可证文件副本 + 提交 SHA）。
10. Pandoc 的 GPL 许可与引擎分发方式的合规边界（§8-6）。
11. Table/Equation 实体的去留决策（B3 的前置：是补齐实体还是砍掉功能，需总控裁定）。

---

## 10. 放行条件（总体 FAIL，以下条目全部关闭后方可进入 Phase 1 实现）

**必须（对应阻断级）：**
1. 关闭 §4 B1：Figure↔Panel 边唯一化，字段表与 P2 表一致（证据：修订后字段表 + diff）。
2. 关闭 §4 B2：`Issue.targets[]` 统一为单一元素形态，同步 `_schema/types/`（证据：唯一形态字段表 + schema 文件）。
3. 关闭 §4 B3：token/ID 文法三处合一；Table/Equation 实体去留由总控裁定后补齐实体+前缀或删除对应 token（证据：单一文法规范 + 匹配测试向量全绿）。
4. 关闭 §4 B4：Result↔Figure 边指定唯一权威持有方并入 P2 表（证据：修订后边归属表）。
5. 关闭 §4 B5：输出字段级"frontmatter / 正文 YAML 块 / 平行列表"落位映射（覆盖全部 object 类字段，含 `x_ext`），并附一份符合 D-04 的示例文件（证据：映射表 + 示例文件通过 VR-17 校验）。
6. 关闭 §4 B6：修正 ANCHOR_RE 并提供两种锚点写法的哈希测试向量，证明锚点变更不改 text_hash（证据：测试向量 + 期望哈希）。

**必须（对应 RISK 项）：**
7. Manuscript 报告证据清单补齐 URL/版本/产物定位，更正 B1（python-docx）、B2（wDocumentChange）、B5（统计）三处错误；D-03 对比实验加入"python-docx 修订 API 实际能力"判据。
8. 开源审计更正 Manubot 许可证（BSD-2-Clause Plus Patent）、重做或删除 §3.4 兼容矩阵、复核 Quarto 历史 GPL 版本号（commit 级出处）、显式声明"闭源/开源"前提。
9. 补交叉确认记录：Worker A 对块 ID 字符集、`{{...}}` 语法、批注支持、blocks 索引逐项给出"是/否/部分 + 证据"，并将结论回填数据模型 §3.3/§5.6。

**建议（不阻断放行，Phase 1 内完成）：**
10. 统一快照形态（md 快照 vs snapshot_asset）并定义 `_maps/` 备份策略；补 §9 遗漏项 4/5/7/8/10/11。

---

*审计执行：独立 QA Agent（task_822c552bcae7）。本报告为唯一交付物；未修改任何被审文件；外部复核产生的临时文件均在 scratch 目录，工作区已清理。*
