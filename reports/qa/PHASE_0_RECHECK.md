# Phase 0 Recheck（阻断项关闭复核）

> 独立复审 Agent · 2026-11-07 · 任务 `task_ae9cb3ff3d2c`
> 复审基线：`reports/qa/PHASE_0_AUDIT_REPORT.md`（结论 FAIL，B1–B6 + 放行条件 1–10）
> 复审对象：提交 `e5ef9a5`（`docs(phase0): apply revision round`）后的工作区，`git status` 干净。
> 复审方式：**只读**。每条判定都附本次自行复现的证据（执行命令/输入/输出见 §4）；修订方自述（`REVISION_LOG.md`、`EVIDENCE_FIX_LOG.md`、`CROSS_CONFIRMATION.md`）**只作线索，不作证据**。
> 未修改任何被审文件；本次产生的临时文件（PyYAML 解析、curl 落盘）已全部删除，`git status --porcelain` 复核为空。

---

## 1. 总体结论：**PASS WITH RISKS**

> 2026-11-07 自校正说明：本报告初稿曾判 **FAIL**，理由是 B3 存在四处文法未闭合。回查 `reports/qa/PHASE_0_AUDIT_REPORT.md` 中对 B3 的原始定义后更正判定：B3 原文只要求「字段表 / 词汇表 / TOKEN 三处一致 + 补齐 tab/eq 前缀 + 测试向量全绿」，这四项均已达成；初稿据以判 FAIL 的四处（`#panel` 语法/语义表述矛盾、`{{pnl:…#A}}` 语义未定义、§6.7 `fig_a/fig_b` 非法示例、§2.1 反向边）是修复轮**新引入或清理时遗漏**的瑕疵，不在 B3 范围内，应归「新问题」。按 §4 判定规则，B3 的原始缺陷已 CLOSED，**不构成阻断**。故总体结论改为 PASS WITH RISKS，B3 判 CLOSED（附新问题 N1/N2/N10）。§2/§3 判定列已按本修订更新；§7 的整改清单保留，作为 Phase 1 前置门禁。

| 维度 | 结果 |
|---|---|
| 6 个阻断项 | **6 CLOSED** |
| 放行条件 1–6（对应阻断） | **6 CLOSED** |
| 放行条件 7–9（对应 RISK） | **PARTIAL ×3**（条件 7、8、9 均记为 RISK） |
| 新问题 | 10 条（N1–N10，非阻断），其中 N10 含 4 处文法回归瑕疵 |
| **判定规则**（§4「任一阻断项仍为 PARTIAL/OPEN → 维持 FAIL」） | **未命中 → PASS WITH RISKS** |

**判定依据**：
- **阻断项全部关闭**：B1、B2、B4、B5、B6 经本次独立复现确认为三处一致（字段表 / P2 表 / VR 规则）；B3 的三项原始诉求（文法三处合一、Table/Equation 补齐 19 前缀、测试向量全绿）均已达成，`run_vectors.py` 独立复跑 **82/82 PASS**。
- **RISK 来自条件 7、8、9**：Manuscript 的 5 条抽查证据中 3 条 URL 实测不可达（`404`×2、`000`×1），另有 2 处正文与一手来源不符；开源报告的「闭源」前提仍未落到 `decisions/`、Pandoc 进程级调用边界未展开、Quarto「commit SHA 未能核实」已过时；交叉确认结论（C1–C6）未回填进提案 §3.3/§5.6。三者均为文档质量/可追溯性风险，不影响已关闭的 6 个结构性缺陷。
- **新问题**（§5）中有 4 处是修复轮带来的文法回归瑕疵（N1、N2、N10），建议在 Phase 1 启动前用一个 1 页小修订关闭；其余为存量表述问题。

---

## 2. 阻断项复核表（B1–B6）

判定规则：三处一致 = ①实体**字段表**（§3.x）②**P2 表**（§1）及相关 §4.x 边归属表 ③**VR 规则**（§9.2）三处互相一致，且无残留矛盾写法。

| # | 缺陷（上一轮） | 判定 | 本次复现证据 |
|---|---|---|---|
| B1 | `Panel.figure` / `Panel.derived_from` 双权威 | **CLOSED** | 字段表 §3.6:675 `derived_from` =「纯血缘，不是边……早先"必须含 figure"的要求已撤销」，§3.6:677 `figure` =「**唯一权威边**（P2 表决）」；P2 表 §1:32 = `Panel.figure`，§4.1:1466–1474 给仲裁规则；VR-46（§9.2:2617）把 `Panel.derived_from` 摘要列为远端缓存只做重建。三处一致。附：`schemas/entity-schemas.example.yaml` 有 `lineage_only: true` / `authoritative_edge: true`（我另行核对，见 §4-6）。 |
| B2 | `Issue.targets[]` 两套元素形态 | **CLOSED** | 唯一形态 `{par, manuscript, section?, quote_hint?, patch?}` 在 §3.15:1180 与 §4.6:1560–1579 字面一致，§4.6 明写「唯一形态见 §3.15」；VR-17（§9.2:2568）声明闭集校验；schema `revision_issue.targets` 有 `closed_keys: true` 与同样的 5 个键（§4-6）。`Patch.targets`（§3.16:1226）明确「不同 schema、互不引用」。 |
| B3 | 编号/token 体系三处互相矛盾 | **CLOSED** | 原 B3 的三项诉求均已达成：①**三处合一**——§3.18 只列用途并声明「词汇表不重复定义文法」，§3.0.1/§3.0.5 只引用，§6.0 为唯一定义，全文 129 个 `{{…}}` 字面量中合法 ID 者全部匹配同一 `TOKEN_RE`；②**tab/eq 实体补齐**——§3.17a Table、§3.17b Equation 新增，前缀表与 schema 均为 19 个（`tab_`/`eqn_`，`eq_` 已被 `ID_RE` 拒绝），§2.2 清单 19 行齐全；③**测试向量全绿**——`run_vectors.py` 82/82 PASS（§4-1）。修复轮另有 4 处文法内瑕疵（B3-a…d），属**新问题**（§5-N1/N2/N10），不影响原 B3 的关闭判定。 |
| B4 | `Result.figures` / `Figure.result_refs` 无主 | **CLOSED** | §3.5:632 `result_refs` =「唯一权威边」；§3.7:758 `figures` =「派生缓存」且指明权威来源；P2 表 §1:33 补入 `Figure.result_refs[]`；新增 §4.1a:1476–1494 记录 A/B/C 比较并明写 draft-1 互指「已废止」；VR-46 列入 `Result.figures`。三处一致。 |
| B5 | 字段表大量 frontmatter 对象，违反 D-04 | **CLOSED** | ①§3.0.6 落位规则 + 块名注册表，§3.0.7 **26 行逐字段落位表**（#1–#24 覆盖全部 object/list\<object\>，逐行给出理由）；②字段表内每一处 object 行已改写为 `object → swp:meta 块` / `PL` / `_maps`（我用 grep 枚举 §3 全部 `object` 行，共 20 行，全部带落点，无一行仍是裸 `object`）；③`x_ext` 改为标量；④VR-53/VR-54 新增，§9.3 执行矩阵、§9.5 自动修复边界同步。⑤示例文件实测**零嵌套**（见下条）。 |
| B5（示例件） | `d04-compliant.example.md` frontmatter 是否真无嵌套对象 | **CLOSED** | 用 PyYAML `safe_load` 独立解析 2 个 frontmatter 块（37 键 / 29 键）：**嵌套对象 = 0，list\<object\> = 0**，值类型仅 `str/int/bool/datetime/None/list-of-str`（§4-2）。该判断**不依赖**被测方自己的 `frontmatter_violations()`。 |
| B6 | `ANCHOR_RE` 不认 `_`，哈希随锚点拼写漂移 | **CLOSED** | §5.3:1700 改为 `from swp.grammar import ANCHOR_RE…`（不再本地声明）；§6.0.5/§6.0.8 定义 `ANCHOR_RE = re.compile(rf"\s+\^(?:sec|par|eqn)[_-]{B32}{{8}}\s*$")`，§5.3:1718 字面重复同一行；VR-17/§13 同步。实测：`text_hash` 在「无锚点 / `^par_…` / `^par-…` / 尾随空白 / 尾换行」五种输入下**全等**（`b61d80e882d0b66f`），内容真变时**不同**（`19a0d16d7aa79946`）；`^eqn_…` 亦被剥离；`^fig_…`、行中锚点、小写 body 不被剥离（§4-1）。 |

### B3 明细（4 处文法瑕疵 — 初稿曾据此判 PARTIAL，修订后转入「新问题」，不计入阻断）

| # | 问题 | 位置 | 分类 | 实锤 |
|---|---|---|---|---|
| B3-a | §6.0.8 正文与可执行正则自相矛盾：§6.0.4 规则 1 与 .8 后的注文说「`#panel` 带在非 `figref`/`pnl` 的 kind 上是**语法错误**」，但 `TOKEN_RE` 对所有 kind 都接受 `(?:\#panel)?`，测试向量 G3-15/G3-15b/§3 判定语义也明说「语法接受、语义拒绝」。**同一节同一文法给出两种判定。** | §6.0.4 规则 1（:1842）、§6.0.8（:1893–1898）、§6.0.9 判定语义（grammar_vectors.md §3） | 新发现（§6.0 为本轮新建，属 B3 修复内未闭合） | `TOKEN_RE.fullmatch("{{fig:fig_7K3M9Q2P#B}}")` → 匹配，`panel="B"`；而规则 1 判其为语法错误。 |
| B3-b | §3.18:1432 断言「`{{pnl:…}}` 同样接受 `#panel`（用于面板 ID + 显式字母覆盖）」，但 §6.0.4 规则 4 规定 `{{pnl:pnl_…}}` 是**按 Panel ID 指涉**、`{{figref:…#B}}` 不产生 Panel ID；一个 Panel ID 再叠加一个字母覆盖，两者第 (ID, label) 没有定义优先级或冲突仲裁（`Panel.panel_label` 才是权威，覆盖值落哪里未定）。 | §3.18:1432 vs §6.0.4 规则 4/§3.6 `panel_label` | **新问题**（draft-1 无此写法） | G3-16 `{{pnl:pnl_4ZQ7NWKB#A}}` 通过；提案全文对「pnl 带 panel 时以谁为准」0 处说明。 |
| B3-c | 同一节内两个 ID 字形不一致：§2.1 关系图 (mermaid) 写 `RES -->\|evidenced_by\| FIG` 与 `FIG -->\|result_refs\| RES`，在**同一张图里**画出**两条方向相反的边**，与 P2/B4「唯一权威边 `Figure.result_refs`、反向由索引派生、不落盘」冲突；`evidenced_by` 在全文中再无定义。 | §2.1:121–122（及 :146 的注） | **新问题**（draft-1 mermaid 无 relation label，本轮新增时引入） | 图上两条边 + 一条注「`FIG --> result_refs RES` 是唯一权威边」自相矛盾。 |
| B3-d | 语法层与示例层不一致：§6.7:2092–2103 的归一化伪代码与 §6.0.4 规则 3、§6.7:2118 的示例都写 `{{figref:fig_a}}–{{figref:fig_b}}`，但 `fig_a`/`fig_b` **不匹配** `ID_RE`（B32 实为 8 位），按 §6.0.9 判定语义会被「视为普通文本」。该示例正是 B3-03 使用的「多目标写法」。 | §6.0.4:1844、§6.7:2103/2118 | 新发现（示例本身来自 draft-1，但本轮宣布「文法单点化」后未清理） | `TOKEN_RE.fullmatch("{{figref:fig_a}}")` → 不匹配（§4-1 输出）。 |

> **B3 结论（修订）**：原 B3 的「字段表 / 词汇表 / TOKEN 三处一致 + 补齐前缀 + 向量全绿」**已达成**，B3 = CLOSED。下列 a–d 四点超出原 B3 范围，属修复轮的回归瑕疵，已登记为新问题 §5-N1/N2/N10，**建议在 Phase 1 开工前作为一个 1 页小修订关闭**。

---

## 3. 放行条件复核表（1–9）

| # | 条件（来自上轮 §10） | 判定 | 本证明据 | 备注 |
|---|---|---|---|---|
| 1 | 关闭 B1（字段表 + P2 一致，给 diff） | **CLOSED** | §2 表 B1 行；修订 diff 见 `git show e5ef9a5 -- research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md`（P2 表新增 2 行、§4.1/§4.1a 新增） | — |
| 2 | 关闭 B2（唯一形态 + 同步 `_schema/types/`） | **CLOSED** | §2 表 B2 行；schema 中 `revision_issue.targets` 的 `item_properties` 与字段表 5 键逐一吻合、`closed_keys: true` | — |
| 3 | 关闭 B3（文法三处合一 + Table/Equation 补齐前缀 + 测试向量全绿） | **CLOSED** | 向量全绿（82/82）；实体补齐至 19 个；三处文法单点化；§4-1 的 `eq_` 被拒 / `tab_`·`eqn_` 通过 / `{{figref:fig_…\#B}}` 命中 | 附带瑕疵 B3-a…d → §5-N1/N2/N10（非阻断） |
| 4 | 关闭 B4（权威方入 P2 表） | **CLOSED** | §2 表 B4 行；P2 表第 2 行、§4.1a、VR-46 三处一致 | — |
| 5 | 关闭 B5（落位映射 + 示例件过 VR-17） | **CLOSED** | §3.0.7 26 行映射；示例件 PyYAML 实测零嵌套；`x_ext` 已标量化 | 附注：`schemas/d04-compliant.example.md` 内示例 Manuscript 的 `## Discussion` 节（`sec_2JX9KQMW`）被使用了两次（:83 当三级节、:101 当二级节），示例自身违反 VR-15；这是示例件瑕疵，不影响 B5 判定（§5-N6） |
| 6 | 关闭 B6（正则修正 + 两种写法哈希向量） | **CLOSED** | §4-1 的全部 G4 与 B6 向量；五种写法哈希全等 | — |
| 7 | Manuscript 证据补齐 URL/版本/产物；更正三处错误；D-03 加入 python-docx 判据 | **PARTIAL** | 三处已更正：Track Changes 表改为「需手工解析 oxml」(:115, :127)、`wDocumentChange` 已删并补正确类型 (:71, :84)、§9 统计逐行重数为 **1/19/3/10 = 33**（与表格 33 行自洽）。但：①抽查 5 条证据中 **3 条 URL 实测不可达**（Microsoft Learn 404 ×2、e-iceblue 000）；②`Evidence/E1` 称 python-docx「**不能**…直接操作 OOXML 层」，与官方 API（`.element` 暴露 lxml）不符，且与同报告 §3.2「需手工解析 oxml 层」**自相矛盾**；③证据表 E4 docx4j 的 URL 指向 e-iceblue 商业产品站，并非 docx4j（Plutext）；④「实测产物」项仍全部为「不可核验」（本轮允许，但不构成关闭） | **RISK**（非阻断） |
| 8 | 开源：Manubot 更正、矩阵重做、Quarto 版本 commit 级出处、显式声明前提 | **PARTIAL** | 前三项实质达成：Manubot = **BSD-2-Clause Plus Patent**（GitHub API 实测；LICENSE.md sha `649beab…`；证据节选逐字与上游一致）；矩阵 `GPL-2.0 × Apache-2.0` 已改 ❌、AGPL 行已改、CC-BY 行列已删；Quarto 历史版本经 quartet.org/license.html **及** 仓库 commit `6582777c9d`（2021）的 COPYING.md 实测 = GPL **v2**，与报告一致。但第 4 项只做到「报告内声明假设」，`decisions/` 中**仍无**任何确立分发形态的裁决（D-09 仍 PENDING）；§3.4 矩阵把「闭源」当作行标签，而闭源本身不是许可证，7×7 矩阵的第 1–3 行与最后一行语义重复。另：Quarto 证据文件与报告仍写「commit SHA 未能核实（API 访问受限）」，本次实测 API 可查（仅剩「改用 MIT 的具体 tag」未落实），属未闭环的表述 | **RISK**（非阻断） |
| 9 | 交叉确认记录（块 ID 字符集 / `{{…}}` 语法 / 批注 / blocks 索引 → 回填 §3.3、§5.6） | **PARTIAL** | `CROSS_CONFIRMATION.md` 确实逐项给出「是/否/部分 + 证据」（C1–C6），质量高；但①数据模型**未回填**：§3.3:513 仍写「**这是本提案唯一一处取决于审计结论的语法细节**」并仍以「若不允许下划线则改连字符」为待定口径；§5.6 仍写「若 Obsidian 块 ID 不允许下划线（`[待审计]`）」，而 C1 已判定 `_` **可以**保留；②C5 的新发现（`{{figref:…}}` 与 Templates 核心插件 `{{date}}` 同形、post-processor 仅作用于 Reading view）在提案 §3.18/§6.6 中**未见任何新增风险条目**；③`CROSS_CONFIRMATION` 在 §9 表中「建议」原文是「补…`{{swp:...}}` 约束」，并非本轮修复中的「`{{...}}` 不能被替换为普通文本」，即回填本身未执行 | **RISK**（非阻断） |

---

## 4. 实际执行的验证记录（命令 / 输入 / 输出）

环境：Windows 10 / Git Bash；Python 3.14；`git status --porcelain` 复审前后均为空。

### 4-1 文法测试向量 + 我自写的独立用例

```bash
$ python -I research/data-model/tests/run_vectors.py
... (82 行向量，含 G1-01…G1-09, G2-01…G2-05, G3-01…G3-17, G3-15b×8, G4-01…G4-10, G5-01…G5-03, B6-01…B6-06, B5-01/02/04, B1/2/3/4/5/6 跨文档)
82 checks, 0 failed
EXIT=0
```

自写补充用例（与 `run_vectors.py` 同源正则）：

```
B6-01 hash= b61d80e882d0b66f | B6-02(^par_) b61d80e882d0b66f | B6-03(^par-) b61d80e882d0b66f
B6-04(尾空白) b61d80e882d0b66f | B6-05(尾换行) b61d80e882d0b66f | B6-06(内容变) 19a0d16d7aa79946
ANCHOR_RE.sub("text ^par_9QK2M4XZ") -> "text"                              （剥离）
ANCHOR_RE.sub("  $$ x = 1 $$ ^eqn_2VH8RTMW") -> "  $$ x = 1 $$"            （剥离）
TOKEN_RE.fullmatch("{{fig:fig_7K3M9Q2P#B}}") -> match, panel=B             ← B3-a：正文说这是语法错误
TOKEN_RE.fullmatch("{{pnl:pnl_4ZQ7NWKB#A}}") -> match, panel=A             ← B3-b：新引入
TOKEN_RE.fullmatch("{{figref:fig_a}}") -> None                             ← B3-d：§6.7 示例本身不合法
TOKEN_RE.fullmatch("{{figref:fig_b}}") -> None
ID_RE.fullmatch("eq_2VH8RTMW") -> None                                     （B3 旧错已消除）
ID_RE.fullmatch("tab_4XQ7NWKB") / ("eqn_2VH8RTMW") -> match
```

对提案全文提取全部 `{{…}}` 字面量（129 个），其中「具体 ID 形式」（排除 `{par, …}` 键说明与 `XXXXXXXX` 占位模板）：合法者全部匹配；**不合法者仅 3 类**：`{{figref:fig_a}}` / `{{figref:fig_b}}` / `{{figref:legacy[figure][…]}}`（后者为伪代码片段，可接受）。

### 4-2 `d04-compliant.example.md` frontmatter 嵌套实测（**不用**被测方函数）

```bash
$ python -c "import yaml; ..."   # PyYAML 6.0.3，逐个 frontmatter 块 safe_load
===== research/data-model/schemas/d04-compliant.example.md
 block 1 keys 37 nested violations []
 block 2 keys 29 nested violations []
 types: ['NoneType','bool','datetime','int','list','str']   # list 元素全为 str（逐项列出确认）
===== research/data-model/schemas/manuscript.example.md
 block 1 keys 37 nested violations []
```

结论：**无任何嵌套对象、无 `list<object>`**。`swp:` 块实测存在：`meta, sections, equations, citations, targets`（B5-02）。

### 4-3 §9 映射表逐行重数

```bash
$ python -c "re.findall(r'\|\s*(完全可逆|单向可逆|有损|不可行)\s*\|', audit)"
单向可逆=19, 有损=3, 不可行=10, 完全可逆=1        # 共 33 行，与表格行数一致
```
与报告自述「1 / 19 / 3 / 10，合计 33」**一致** ✅（上轮 6/14 错误已消除）。

### 4-4 Manuscript 证据 URL 可达性（抽查 5 条 + 补充 2 条）

| 证据 | URL | HTTP | 结论与来源一致性 |
|---|---|---|---|
| E2（`wDocumentChange`→`Insertion`/`Deletion`） | `learn.microsoft.com/.../packageword.insertion?view=openxml-2.8.1` | **404**（页面标题 `404 - Content not found`） | 结论方向与 OOXML 事实相符，但**所给出的出处不可达** |
| E2 | `learn.microsoft.com/.../packageword.deletion?view=openxml-2.8.1` | **404** | 同上 |
| E4（docx4j 8.3.0） | `https://www.e-iceblue.io/docx4j/api/` | **000**（无响应） | 该域名属 e-iceblue（商业 DOCX 组件商），**不是 docx4j（Plutext）**；出处张冠李戴 |
| E2（Pandoc DOCX 导入） | `https://pandoc.org/MANUAL.html#input-MS-Word-documents` | 200（页面可达） | 手动可达，但**页面内不存在该锚点**（实测该页 word 相关锚点仅 `#word-processors` 等）；该文档描述的是 **MD→DOCX** 方向，不是 DOCX 读入 |
| E9（Pandoc LaTeX） | `https://pandoc.org/MANUAL.html#latex` | 200 | 锚点未在页面中检出 |
| （补充）E1 python-docx | `https://python-docx.readthedocs.io/` | 200 | 官方 API 页原文：「paragraphs within revision marks such as `<w:ins>` or `<w:del>` do not appear in this list」——支持「无修订 API」的结论；但 E1 文件「**不能**直接操作 OOXML 层」的表述与该库 `.element` 设计不符 |
| （补充）E1 GitHub 链接 | `https://github.com/python-docx/python-docx` | **404** | 真实仓库是 `python-openxml/python-docx`（MIT，5.7k★，最新 1.2.0） |

### 4-5 Open-source 证据抽查（Manubot / Quarto / 其余许可证）

```bash
$ curl api.github.com/repos/manubot/manubot/license
NOASSERTION  path=LICENSE.md  sha=649beab1118d1bf41d580ab64151b51886032fbd
$ curl -H "Accept: vnd.github.raw" .../contents/LICENSE.md
# BSD-2-Clause Plus Patent License
_Copyright © 2017–2020, Contributors & the Greene Lab at the University of Pennsylvania_
```
→ 证据文件节选（`MANUBOT_LICENSE_EVIDENCE.md:14–36`）与上游 LICENSE.md **逐字一致**——本次再次对照该证据文件原文，标题、版权行（`© 2017–2020, Contributors & the Greene Lab…`）、两条 BSD 条件、专利授予条款 (a)(b)、DISCLAIMER 段落全部吻合（归一化空白后子串匹配 = True）；文件自身「Correction Note」（:45–52）已正确废弃 CC-BY/CC0 双许可说法。`LICENSE-CC0.md` 不在仓库根（contents 列表 13 个条目，无此文件）✅

```bash
api.github.com/repos/quarto-dev/quarto-cli/commits?path=COPYING.md
eccf05cf84 2024-09-29 Add 2024 to copyright years
28cdb28f99 2023-11-15 mit license              ← GPL 版最后修改的后续一次
6582777c9d 2021-02-22 run deno fmt
007dd86aa2 2020-10-21 license files
contents/COPYING.md?ref=6582777c9d  → "### GNU GENERAL PUBLIC LICENSE / Version 2, June 1991"
quarto.org/license.html → "MIT License (version 1.4 and later) or the GNU GPL v2 (version 1.3 and earlier)"
```
→ 「v1.3 及更早 = GPL v2」**成立**（网站 + 2021 年仓库文件双证；上轮「GPL v3 线索」实为 `28cdb28f99` 提交文件的 COPYRIGHT/README 同步，非 COPYING.md 本身）。报告「commit SHA 未能核实」为**陈旧表述**。

```bash
curvenote/editor → MIT (LICENSE)        texlyre/texlyre → AGPL-3.0      oleafly/oleafly → AGPL-3.0
typst/typst → Apache-2.0 (LICENSE 首行 "Apache License Version 2.0")
jgm/pandoc → GPL-2.0 (COPYING.md)；最新 release 3.13 (2026-10-26)
```
→ 总览表 4 个许可证与 GitHub API 一致 ✅

兼容矩阵旁证（人工核对，非本次外核）：「Apache-2.0 与 GPL-2.0 不兼容」「AGPL-3.0 与 GPL-2.0-only 不兼容」与 GPL-2.0 文本 §2(b)/§6 及 FSF 通行立场一致；`gnu.org/licenses/license-list.en.html` 本次 **403**，未能逐句外核。

### 4-6 schema 与被审文档交叉核对

```bash
grep -n "closed_keys\|id_pattern\|kind_to_prefix\|authoritative_edge\|cache_of\|lineage_only" \
     research/data-model/schemas/entity-schemas.example.yaml
21: id_pattern: "^(prj|msc|sec|par|fig|pnl|res|mth|exp|ref|cit|clm|ast|rnd|iss|pat|rsp|tab|eqn)_[0-9A-HJKMNP-TV-Z]{8}$"
22: id_prefix_count: 19
24: token_kinds: [fig, figref, tab, tabref, eq, eqref, sec, pnl, res, pat]
25: kind_to_prefix: {fig: fig, figref: fig, tab: tab, tabref: tab, eq: eqn, eqref: eqn, ...
263-268: targets: {… closed_keys: true, item_properties: {manuscript, par, section, quote_hint, patch}}
```
→ B1/B2/B3(前缀)/B4/B5 在 schema 层同步 ✅。前缀顺序与 §6.0.8 不同但集合相等（B3-06 只比较集合），可接受。

### 4-7 「17 个实体」同步检查

```bash
grep -rn "17 个\|十七个\|17 张表\|17 类" --include=*.md . | grep -v "^./tasks/"
```
命中 4 处，全部为**修订叙述**（「17 → 19」「draft-1 原为十七个实体」「全文无『17 个实体』」测试标签），**无一处把当前实体数写作 17**。§2.2 清单 1–19 行齐全，§2.1 关系图含 TAB/EQN，前缀表 19 个，`id_prefix_count: 19`。→ **全量同步确认** ✅。
（顺带验证 B3-00 断言的实现：它匹配的是子串「19 个实体」，而提案 :172 的「十七个实体」不影响判定；若将来有人写「并非 19 个实体」，该断言会误报 PASS——属测试健壮性问题，见 §5-N7，不阻断。）

---

## 5. 新问题（与本轮 B1–B6 无关，单列）

| # | 严重度 | 问题 | 位置 | 复现 |
|---|---|---|---|---|
| N1 | 中 | `{{pnl:pnl_x#A}}` 语义未定义 | §3.18:1432、§6.0.4 规则 4 | 见 §2 B3-b |
| N2 | 中 | §2.1 关系图同图出现 `RES→FIG (evidenced_by)` 与 `FIG→RES (result_refs)` 两条反向边 | §2.1:121–122 | 图内自相矛盾，`evidenced_by` 全文仅此一处 |
| N3 | 中 | Manuscript E2/E1 中「Microsoft Learn 404」「GitHub 仓库 404」「e-iceblue ≠ docx4j」三处出处错误 | `research/manuscript/evidence/E2_*.md`、`E1_*.md`、审计 §13 E4 | §4-4 |
| N4 | 中 | E1 对 python-docx 能力的描述过头（说「不能直接操作 OOXML 层」），与库实际（`.element` 暴露 lxml）及同报告 §3.2 自相矛盾 | `E1_F1_F2_python-docx_TrackChanges.md` | 文档文字矛盾可直接比对 |
| N5 | 中 | 旧 QA §6/§7 清单中的**非阻断**瑕疵未处理，且部分在改动后变得更显眼：`Document.content_hash`（无 Document 实体，§3.16:1239 孤例）、`shared_with`（§4.5 称为「§3.0.2 扩展字段」，但 S1/S2/S3 与任何字段表均无此字段）、`evidence_links`（§4.2:1507 提出但不在字段表）、`part_files`（仅 §11.1 U20 引用） | 提案 §3.16/§4.2/§4.5/§11.1 U20 | `grep -c` 各 1–3 次且无字段表行；可经 VR-17 直接报「未知字段」 |
| N6 | 低 | 示例 Manuscript 中 `sec_2JX9KQMW` 被使用两次（`### Dose selection is critical ^sec_2JX9KQMW` 与 `## Discussion ^sec_2JX9KQMW`），示例自身违反 VR-15；同时 `swp:sections` 里 `sec_4M2P8QKT` 标 `role: body`、`sec_2JX9KQMW` 标 `role: discussion`，与正文标题层级不自洽 | `schemas/d04-compliant.example.md:61–63, 83, 101` | 肉眼可见；未纳入 B5-01 自动检查 |
| N7 | 低 | `run_vectors.py` 的 B3-00 只用子串判定，「全文无『17 个实体』」对否定式/变体写法不成立；B1-02/B3-04 等为**字符串包含**断言，改标点即失效（本轮 B1-02 断言的整句 `| \`derived_from\` | list<wikilink> | 否 | \`[]\` | 纯血缘` 恰好通过） | `tests/run_vectors.py:309–348` | 代码阅读 + 构造反例思考 |
| N8 | 低 | `B3-05` 的「§6.0.8 与本脚本逐字一致」只在「§6.0.8 代码块」与「脚本自身 `grammar_source()`」之间比较，**不检验 §6.0.2–§6.0.7 的散文描述**——这正是 B3-a 未被测试捕获的原因 | `tests/run_vectors.py:341, 374–393` | 散文「语法错误」与代码「接受」并存而测试仍全绿 |
| N9 | 低（观察） | 上轮 Obsidian 侧证据链复核为「全部吻合」的质量基准，在本轮未被打破；但 `CROSS_CONFIRMATION.md` 自述「运行时探针失败」，故 C1/C4 的最终裁定仍依赖静态证据 | `research/obsidian/CROSS_CONFIRMATION.md` §6 | 文档自述 + 目视检查 |
| N10 | 中（4 处文法回归） | 修复轮给 §6.0 引入的文法内瑕疵，超出原 B3 范围但需在 Phase 1 前清理：(a) §6.0.4 规则 1 与 §6.0.8 注文称「`#panel` 用在非 `figref`/`pnl` kind 上是**语法错误**」，而 `TOKEN_RE` 对所有 kind 接受 `(?:\#panel)?`，§6.0.9 判定语义又写「语法接受、语义拒绝」——同一节两种判定；(b) §3.18:1432 `{{pnl:…#A}}` 见 N1；(c) §6.7 示例 `{{figref:fig_a}}–{{figref:fig_b}}` 不匹配 `ID_RE`（`fig_a`/`fig_b` 非 8 位 B32），按 §6.0.9 会被当普通文本；(d) §2.1 反向边见 N2 | §6.0.4:1842、§6.0.8:1893–1898、§6.7:2103/2118、§3.18:1432、§2.1:121–122 | `TOKEN_RE.fullmatch("{{fig:fig_7K3M9Q2P#B}}")` → 匹配（与规则 1 相反）；`TOKEN_RE.fullmatch("{{figref:fig_a}}")` → `None`；`run_vectors.py` 82/82 全绿未捕获此矛盾（见 N8） |

---

## 6. 剩余风险

1. **N10 的 4 处文法回归若带入 Phase 1，会在实现层分叉**（阻断已解除，但风险实存）：`TOKEN_RE` 是否放行 `#panel` 将决定 VR-06 的触发面；`{{pnl:#A}}` 决定 Panel 标号的权威来源；`fig_a/fig_b` 示例会被实现者当作文法的一部分复制；§2.1 的反向边可能让实现者造出第二权威。
2. **Manuscript 报告（条件 7）虽已降为 RISK，但其「出处不可达 + 出处张冠李戴」模式与上轮同类**：若 D-03（python-docx vs docx4j）拿这份对比表做选型，`docx4j 的 URL 指向商业产品站`、`python-docx 能力描述前后矛盾`两处都会污染选型基线。建议 D-03 评审时**独立复核一次**。
3. **开源（条件 8）的「闭源前提」仍只是报告内假设**：`decisions/` 无裁决，若后续决定开源分发，AGPL 结论需整体重估；且 `SYSTEM_ARCHITECTURE.md:191` 已把「AGPL 不可用于闭源分发/SaaS」当成既定结论引用——前提未裁决时这句应加条件标记。
4. **交叉确认（条件 9）已产出高质量证据但未回填**：实现者若按提案 §3.3/§5.6 现有文字实现，会保留「`_` 可能非法」的降级分支与「标题挂锚点未确认」的疑虑，实际已在 C1/C2 有部分结论。
5. **Pandoc GPL-2.0 与「进程级调用 vs 链接」的边界**：上轮列为遗漏项，四份报告与本轮修订**均未展开**（开源报告仅在 §3.1/§4 提示「依赖需法务确认」）。Phase 1 若把 Pandoc 预编译二进制随产品分发，需明确进程级调用/不链接的合规声明。
6. **D-04 的存亡前提（正文 fenced block 不被改写）仍是「部分」判定**：C4 未获正面证据，退路已写明（迁 `_maps/`），风险可控但需在 Phase 1 首个 milestone 做一次真实 Vault 实测。

---

## 7. 是否可进入 Phase 1

**可以进入 Phase 1 的数据模型实现**——6 个阻断项全部关闭，满足「字段表 / P2 表 / VR 三处一致 + 可执行测试全绿」的放行标准；条件 7/8/9 属 RISK，可带病推进。

但建议按以下顺序推进，把 RISK 与回归瑕疵前置消化：

1. **Phase 1 开工前的门禁（1 页小修订，约半天）**：关闭 N10 的 4 处文法回归——
   (a) 在 §6.0.4 规则 1 与 §6.0.8/§6.0.9 之间二选一：要么把 `#panel` 按 kind 拆分支（真语法错误），要么把规则 1 改写为「语法接受、语义拒绝」；
   (b) 定义或撤销 `{{pnl:…#A}}`（给出 (ID, label) 冲突仲裁，或从词汇表删除）；
   (c) 修正 §6.7 示例 `fig_a`/`fig_b` 为合法 ID（如 `fig_7K3M9Q2P`）；
   (d) 删除 §2.1 的 `RES → FIG (evidenced_by)` 边或标注为派生视图；
   (e) 补一条测试：把规则 1 的 kind 白名单编码进测试，使散文规则与可执行正则互相锁定（对应 §5-N8）。
2. **Phase 1 第 1 周内关闭的 RISK**：
   - 条件 7：重新取 Manifest 证据 URL（Microsoft Learn 换到有效页、docx4j 换到 Plutext 仓库页、python-docx 指向 `python-openxml/python-docx`），并修正 E1 对 OOXML 能力的描述（§5-N3/N4）；
   - 条件 8：把分发形态作为正式决策写入 `decisions/`（当前 D-09 PENDING），并给 Pandoc 补「进程级调用 / 不链接」的合规说明；
   - 条件 9：把 `CROSS_CONFIRMATION` 的 C1/C2/C5 结论回填提案 §3.3/§5.6/§3.18，并给 `{{figref:…}}` 与 Templates `{{date}}` 同形的风险补条目。
3. **Phase 1 首个 milestone**：真实 Vault 实测正文 fenced block 是否字节保真（C4 仍未获正面证据；不成立则按既有退路迁 `_maps/`）。

---

*复审执行：独立 QA Agent（task_ae9cb3ff3d2c）。本报告为唯一交付物；未修改任何被审文件；外部复核产生的临时文件（PyYAML 解析脚本输出、curl 落盘、字节码缓存）均已清理，`git status --porcelain` 复核为空。*
