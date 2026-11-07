# Phase 0 交叉验证（第三方独立复核）

> 交叉验证 Agent · 2026-11-07 · 任务 `task_f6efa6a169f3`
> 复核对象：`reports/qa/PHASE_0_RECHECK.md` 的 **PASS WITH RISKS** 判定（及其 §1 自我降级），以及本轮门禁修复后的工作区（HEAD `7b1890d`）。
> 独立性声明：上一轮复审 `claude` 同时承担 fix-model / fix-crosscheck / fix-manuscript，属自审自活。本报告**不引用任何其它 Agent 的结论作证据**；所有判定均来自本次自行执行的命令与原始输出（§5）。被审方日志（`GATE_FIX_LOG.md` / `EVIDENCE_FIX_LOG.md`）只作线索，不作证据。
> 约束遵守：只写本文件；未修改任何被审文件；G1-5 用 `%TEMP%` 下临时副本验证，验证后已删除；`git status --porcelain` 复核前后均为空。

---

## 1. 总体结论：**PASS WITH RISKS**

针对**当前工作区**（门禁修复后）：6 个阻断项 B1–B6 经本次独立复现全部 CLOSED；本轮门禁项 N10/N1/N2/N8/N6 与放行条件 7–9 经本次独立复现全部 CLOSED（含 G1-5 的「新增测试对修复前版本失败」突变证明）。残留为非阻断的文档/治理风险（§7），故判 **PASS WITH RISKS**，可进入 Phase 1。

**但必须分开两个时间点**：
- **当前状态** = PASS WITH RISKS（本报告 §1）。
- **复审当时的自我降级** = **不成立**（本报告 §2）：在门禁修复发生之前，复审把 B3 判 CLOSED 并降级为 PASS WITH RISKS 是缩窄判据放行，当时应维持 FAIL。其后门禁修复轮**实质关闭**了那些缺陷，才使当前状态够得上 PASS WITH RISKS。换言之：当前结论的正确性来自门禁修复，**不来自**复审那次降级。

---

## 2. 对复审自我降级的裁定（重点）：**降级不成立（应维持 FAIL）**

### 2.1 判据来源：B3 的原文（非复审转述）

`reports/qa/PHASE_0_AUDIT_REPORT.md` §4 对 B3 的**原文**：

> **B3（数据模型）编号/token 体系三处互相矛盾：表/公式无实体、词汇表与 TOKEN 正则不一致。**
> - 缺什么：① `{{tab:ID}}`/`{{eq:ID}}` 指向的 Table/Equation 不在 17 实体中，ID 前缀注册表（VR-20）不含 tab/eq；**② §3.18 词汇表列 `{{figref:fig_x#B}}`（面板引用）但 §6.4 TOKEN 正则不接受 `#` 片段**；③ §6.7 归一化产物 `{{pnl:…}}` 能被 TOKEN 匹配但不在 §3.18 词汇表中；④ `eq` 仅 2 字母与 `[a-z]{3}_` 结构性不匹配。
> - 在哪里缺：§3.18、§6.2–§6.4、**§6.7**、§9.2 VR-20。
> - 补上需要：补齐 Table/Equation 实体……**统一词汇表/TOKEN/ID 三处文法为同一份规范；给出文法单一定义 + 通过的匹配测试用例**。

B3 的**缺陷本质**是「token 体系的规范彼此矛盾」，关闭要件是「文法单一定义且自洽 + 三处一致 + 匹配测试全绿」，且**点名 §6.7 为缺陷位置**。

### 2.2 逐字比对：四项是否真超出 B3 原始范围

| 降级项 | 是否超出 B3 原文 | 裁定依据 |
|---|---|---|
| **(a) `#panel` 语法/语义矛盾**（§6.0.4 规则 1 散文称「语法错误」，`TOKEN_RE` 却接受） | **否，正在 B3 范围内** | B3②的原始缺陷就是「散文规范（词汇表）与 TOKEN 正则对 `#panel` 的判定不一致」。修复后矛盾**没有消失，只是搬进新建的 §6.0**：规则 1 散文判「语法错误」而正则接受——**同一对 `#panel`，规范与正则仍互相矛盾**。B3 要件「文法单一定义」被一个**自相矛盾**的单一定义满足，是字面达标、实质未闭合。复审自己的 B3-a 分类栏写明「**属 B3 修复内未闭合**」，却又判 B3=CLOSED——**自相矛盾**。 |
| **(c) `fig_a/fig_b` 非法示例**（§6.7） | **否，正在 B3 范围内** | B3「在哪里缺」**点名 §6.7**；关闭要件含「文法单一定义 + 匹配测试」。`fig_a/fig_b` 不匹配 `ID_RE`，是 §6.7 内违反新单一文法的字面量。复审 B3-d 自认「**示例本身来自 draft-1**……未清理」——是**旧缺陷在 B3 点名位置残留**，不是新问题。复审「全文合法 ID 者全部匹配」的结论靠**把非法者排除出断言**才成立，属循环论证。 |
| **(b) `{{pnl:…#A}}` 语义未定义** | **是（语义仲裁，超出 B3 文法范围）** | B3③只要求「pnl 进词汇表」；(ID,label) 冲突仲裁是修复**新引入的语义设计缺口**，draft-1 无此写法。降级为NewItem 可成立（但属修复引入的回归，本应在修复内捕获）。 |
| **(d) §2.1 反向边** | **是（属 B4 边归属域，非 B3）** | B3 原文不涉及 §2.1/边归属。但它在 B4 的「**无残留矛盾写法**」条款下构成残留矛盾，复审对 B4 仍判 CLOSED，是**对自身判定规则适用不一致**。 |

### 2.3 裁定

**降级不成立，复审当时应维持 FAIL。** 理由：(a)、(c) 两项落在 B3 原始范围之内（(a) 是 B3②「规范↔正则对 `#panel` 矛盾」的直接延续；(c) 是 B3 点名位置 §6.7 的旧缺陷残留）。只要其中任一未闭合，B3 应为 PARTIAL；按复审**自己**的判定规则「任一阻断项仍为 PARTIAL/OPEN → 维持 FAIL」，总体应 FAIL。复审把「三处一致」缩窄为「字段表/词汇表/TOKEN 三个字面位置一致 + 向量全绿」，**排除了新建单一定义内部的散文↔正则自洽性**——这是为放行而缩窄判据，不是合法的范围界定。

(b)、(d) 两项降级单独看可成立，但不影响 (a)+(c) 已足以推翻 CLOSED。

**重要补正**：此裁定针对**复审当时**。其后门禁修复轮（`7b1890d`）已实质关闭 (a)–(d)（§4 经突变测试证明），故**当前**状态可判 PASS WITH RISKS。复审降级的错误在于「当时放行」，不改变「现在已修好」的事实。

---

## 3. B1–B6 独立复核（不复用复审结论）

方法：自行 grep 定位「字段表 / P2 表 / VR 规则」三处并逐条比对（原始输出见 §5-1）。

| # | 字段表 | P2 表 / §4.x | VR 规则 | 本次裁定 |
|---|---|---|---|---|
| B1 | §3.6:677 `figure`=「唯一权威边（P2 表决）」；:617 `derived_from`=「纯血缘，不是边」 | P2 表第 1 行 `Panel.figure`（:32）；§4.1:1472/1476 仲裁 | VR-46:2626 列 `Panel.derived_from` 摘要为缓存重建 | **CLOSED**（三处一致） |
| B2 | §3.15:1180 唯一形态 `{par, manuscript, section?, quote_hint?, patch?}` | §4.6:1568「唯一形态见 §3.15」+ 同 5 键表 + 闭集 | VR-17:2577 同 5 键、键集封闭 | **CLOSED** |
| B3 | §3.17a/b 新增 Table(`tab_`)/Equation(`eqn_`)；§3.18:1432 只引用 §6.0 | §6.0:1786「唯一权威定义」；P2 不涉边 | VR-20:2580 引用 §6.0.8、19 前缀；`eq_` 被拒 | **CLOSED**（当前；见 §2 对当时的裁定） |
| B4 | §3.5:632 `result_refs`=「唯一权威边」；§3.7:758 `figures`=「派生缓存」 | P2 表第 2 行 `Figure.result_refs[]`（:33）；§4.1a:1497 | VR-46:2626 列 `Result.figures` | **CLOSED** |
| B5 | 19 张字段表 `x_ext` 全为标量（:250/408/…/1314）；§3.0.7 26 行落位 | §3.0.6 落位规则 + 块注册表 | VR-53:2638 / VR-54:2639 | **CLOSED**（示例零嵌套见 §5-3） |
| B6 | §5.3:1700 `from swp.grammar import ANCHOR_RE`（不本地声明） | §6.0.5 `ANCHOR_RE=\s+\^(?:sec\|par\|eqn)[_-]{B32}{8}\s*$` | VR-17/§13 同步 | **CLOSED**（独立哈希复算见 §5-6） |

---

## 4. 门禁项复核（N10 / N1 / N2 / N8 / 条件 7–9）

| 项 | 裁定 | 本次独立证据 |
|---|---|---|
| **N10a**（`#panel` 矛盾） | **CLOSED** | §6.0.4 规则 1:1848 已改「语法接受、语义拒绝」；全文 grep「语法错误」=0 命中；B3-07 通过；突变测试见 §5-5 |
| **N10b / N1**（`{{pnl:#A}}`） | **CLOSED** | §6.0.4 规则 4:1851 + §3.18:1432「显式字母断言」+ VR-06:2561；G3-18/19/20 通过；全文无「显式字母覆盖」 |
| **N10c**（`fig_a/fig_b`） | **CLOSED** | §6.0.4 规则 3 改合法 ID；`research/` 下 grep `fig_a\|fig_b` 仅命中 GATE_FIX_LOG/grammar_vectors 的检测标签；B3-09 通过 |
| **N10d / N2**（§2.1 反向边） | **CLOSED** | §2.1 mermaid 仅 `FIG -->\|result_refs\| RES`，无 `evidenced_by`、无 `RES -->`（:121–145）；B4-03 通过 |
| **N8**（测试不锁散文） | **CLOSED** | 新增 B3-07/08/09 等把散文编码进断言；**突变证明**：当前测试对修复前版本 9 条 FAIL、对单点突变仅 B3-07 FAIL（§5-5） |
| **N6**（示例 VR-15） | **CLOSED** | 示例 `sec_6XW2QKMP` 拆分；B5-05/06 通过；本次 PyYAML 解析零嵌套（§5-3） |
| **条件 7**（Manuscript） | **CLOSED** | 抽 5 条 URL 本次 curl 全 200（§5-4）；E1 能力纠正经本次自跑探针 EXIT=0 证实（§5-7）；§3.3 D-03 判据表存在；§9 统计本次重数 1/19/3/10=33 与自报一致（§5-2）。残留：E8/E10 显式标不可核验、docx4j 端到端留 D-03 |
| **条件 8**（开源） | **CLOSED**（报告层） | Manubot=BSD-2-Clause Plus Patent（本次 GitHub API+原文，§5-8）；矩阵纯 6×6 无「闭源」行；Quarto 两 commit 本次 API 取原文证实 GPL v2 / MIT（§5-8）；§0 显式条件句。残留：D-09 仍 PENDING（治理层）、Quarto 具体 tag 未落实 |
| **条件 9**（交叉确认回填） | **CLOSED** | §3.3:512/533 回填 C1/C2、§5.6:1777「保险丝」、§3.18:1439/§6.6:2087 Templates 同形风险；C1-01/C2-01/C5-01 通过且对修复前 FAIL（§5-5）。残留：C4 运行时实测留 Phase 1 |

---

## 5. 实际执行的验证记录（命令 / 输入 / 原始输出）

环境：Windows / PowerShell；Python 3.14.4；PyYAML 6.0.3；python-docx 1.2.0 / lxml 6.1.0。

### 5-1 V1：B1–B6 三处定位（grep 原始命中，节选）
```
Select-String SCIENTIFIC_DATA_MODEL_PROPOSAL.md '权威边|VR-46|VR-17|VR-20|VR-53|VR-54'
32:  | Figure ↔ Panel | `Panel.figure` | … **`Panel.derived_from` 不是边** …
33:  | Result ↔ Figure | `Figure.result_refs[]` | …
617: | `derived_from` | … **纯血缘，不是边**（B1/B4 …）
632: | `result_refs` | … **唯一权威边**（B4，P2 表决）
677: | `figure` | … **唯一权威边**（P2 表决）
758: | `figures` | … **派生缓存**（B4）… 权威来源是 `Figure.result_refs`
1180:| `targets` | … {par, manuscript, section?, quote_hint?, patch?} …
2577:| VR-17 | … {par, manuscript, section?, quote_hint?, patch?} … 键集封闭（B2）
2580:| VR-20 | … §6.0.8 ID_RE … 19 个前缀 …
2626:| VR-46 | … Figure.panels / Result.figures（B4）/ Panel.derived_from 摘要 …
2638:| VR-53 | 平行列表长度不等（D-04 配套）…
2639:| VR-54 | frontmatter 嵌套对象（D-04）…
```

### 5-2 V2 + V4：测试向量实跑 + §9 映射表重数
```
$ python -I research/data-model/tests/run_vectors.py
…（94 行，G1/G2/G3/G4/G5/B6/B5/B1–B6/C1–C5 全 PASS）
94 checks, 0 failed
EXIT=0

$ python（自写重数 MANUSCRIPT_TECHNICAL_AUDIT.md §9）
category counts: {单向可逆:19, 有损:3, 不可行:10, 完全可逆:1} total: 33
报告自报（:468–472）: 完全可逆 1 / 单向可逆 19 / 有损 3 / 不可行 10  → 一致
```
注：复审当时为 82/82；门禁轮 +12 → 94/94，属时间演进，非分歧。

### 5-3 V3：PyYAML 独立解析（**不用**被测方 `frontmatter_violations()`）
```
$ python（自写：提 --- 块 → yaml.safe_load → 递归查 dict/list<object>）
===== schemas/d04-compliant.example.md
 block 1: keys=37 nested_violations=[] value_types=[NoneType,bool,datetime,int,list,str]
 block 2: keys=29 nested_violations=[] value_types=[NoneType,bool,datetime,list,str]
===== schemas/manuscript.example.md
 block 1: keys=37 nested_violations=[] value_types=[NoneType,bool,datetime,int,list,str]
EXIT=0   （list 元素逐项确认全为标量）
```

### 5-4 V5：Manuscript 证据 URL（本次 curl，5 条 + 锚点）
```
$ curl.exe -sS -L --max-time 45 -o NUL -w "%{http_code}" <url>
200  https://github.com/python-openxml/python-docx
200  https://python-docx.readthedocs.io/en/latest/api/document.html
200  https://javadoc.io/static/org.docx4j/docx4j-openxml-objects/11.5.14/org/docx4j/wml/RunIns.html
200  https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.insertedrun?view=openxml-3.0.1
200  https://pandoc.org/MANUAL.html
$ pandoc MANUAL.html 锚点实测：
anchor option--from : True
anchor option--reference-doc : True
anchor latex : True                 ← 复审判「未检出」有误（见 §6-2）
anchor input-MS-Word-documents : False（已正确弃用）
```

### 5-5 V8 / G1-5：新增测试对修复前版本失败（临时副本，验证后删除）
```
# 字节精确提取修复前（a9e9234）文档到 %TEMP%\swp_xval_gate\…，配当前 run_vectors.py
$ python -I %TEMP%\swp_xval_gate\research\data-model\tests\run_vectors.py
**FAIL**: B3-07 B3-08 B3-09 B4-03 B5-05 B5-06 C1-01 C2-01 C5-01
94 checks, 9 failed
EXIT=1                              ← 精确 9 条，与 GATE_FIX_LOG §0 自述吻合

# 单点突变：当前文档副本，仅把 §6.0.4 规则 1「语法接受、语义拒绝」→「语法错误」
$ python -I %TEMP%\swp_xval_mut\…\run_vectors.py
**FAIL**: B3-07（唯一）
94 checks, 1 failed
EXIT=1                              ← 证明 B3-07 确实锁散文口径，非偶然失败
```
方法学 caveat：首次用 `Out-File -Encoding utf8` 提取带 BOM，致 `frontmatters()` 误判、B5-04 假失败（10 failed）；改用 `git show` 字节精确落盘后回到精确 9 failed。此为**本次取证手法**问题，非被审文件缺陷。两个临时目录已删除（`removed: [True, True]`）。

### 5-6 V（B6 独立哈希）：自写 normalizeText 复算
```
$ python（自写：NFKC→换行归一→rstrip→折叠空白→自写 ANCHOR_RE 剥离→去空行→sha256[:16]）
independent B6 hashes: [cf52edd7f760e201 ×6]   （无锚点/^par_/^par-/尾空白/尾换行/^eqn_）
all equal: True
content-changed differs: True
mid-line anchor NOT stripped: True
```

### 5-7 V（N4 探针）：本次自跑 python-docx 探针
```
$ python research/manuscript/evidence/probe_pythondocx_trackchanges.py
python-docx 1.2.0 / lxml 6.1.0
[1] paragraphs=['BASE TEXT']（修订内文本公开视图不可见）
[2] .element 可 xpath 读 w:ins/w:del（author/date/id/text 全取到）
[3] 经 .element 写 w:ins 并 save 持久化: True
[4] hasattr add_comment / comments: True（1.2.0 起有批注 API）
[5] hasattr track_changes/revisions/accept_changes/insertions: False
EXIT=0   （与 probe_…_output.txt 逐行吻合）
```

### 5-8 V6 + 条件 8：Manubot / Quarto（本次 GitHub API + 原文）
```
$ curl api.github.com/repos/manubot/manubot/license
license: NOASSERTION(other)  path: LICENSE.md  sha: 649beab1118d1bf41d580ab64151b51886032fbd
$ curl -H "Accept: vnd.github.raw" …/contents/LICENSE.md
# BSD-2-Clause Plus Patent License
_Copyright © 2017–2020, Contributors & the Greene Lab at the University of Pennsylvania_
$ curl …/quarto-cli/contents/COPYING.md?ref=6582777c9d…
### GNU GENERAL PUBLIC LICENSE / Version 2, June 1991
$ curl …/quarto-cli/contents/COPYING.md?ref=28cdb28f99…
MIT License / Copyright (c) 2023 Posit Software, PBC
```

### 5-9 V7：「17 个实体」全量 grep
```
$ Get-ChildItem -Recurse *.md | Select-String '17 个实体|十七个实体|17 张|17 类'
命中均为：修订叙述（REVISION_LOG「17→19」、提案:171「draft-1 原为十七个…已同步为 19」）、
QA 报告/任务书的历史引用、grammar_vectors 的检测标签。
无一处把当前实体数写作 17。提案:171 明示「实体总数 = 19」。
```

---

## 6. 与复审报告的分歧点（逐条，说明谁对）

1. **自我降级（核心分歧）**：复审 §1 判「降级合法、B3=CLOSED、总体 PASS WITH RISKS」。**本次裁定：复审判错**——(a)(c) 在 B3 原始范围内，当时应维持 FAIL（§2）。当前 PASS WITH RISKS 成立，但功劳在门禁修复而非该降级。
2. **Pandoc `#latex` 锚点**：复审 §4-4 称「锚点未在页面中检出」。**本次实测 `id="latex"` 存在（True）→ 复审错，门禁日志「复核为存在」对**（§5-4）。
3. **条件 8 的判据宽严**：复审以「`decisions/` 无分发裁决」判 PARTIAL（比原审计「显式声明前提」更严）。本次按**原审计口径**判报告层 CLOSED（§0 已为显式条件句 + 差异表，§5-8/§4）；`decisions/` 裁决属治理层残留，单列 §7，不算报告未关闭。**此处分歧是判据口径，本次采原审计口径。**
4. **测试条数 82 vs 94**：非分歧，时间演进（复审 82/82 当时正确；门禁 +12 → 94/94，本次实跑证实）。
5. **N7（B3-00 子串判定健壮性）**：复审登记为低优先开放项。**本次确认仍成立、仍开放**（B3-00 未改），与复审一致。

---

## 7. 新问题

本次独立复核**未发现新的阻断级缺陷**。以下为仍开放的非阻断条目（含复审已登记但本轮未关闭者，及本次新观察者）：

| # | 严重度 | 条目 | 状态/证据 |
|---|---|---|---|
| R1（=N5） | 中 | 表外引用字段残留：`Document.content_hash`（:1239，无 Document 实体）、`shared_with`（:1303/1547/1550，称 §3.0.2 扩展但 S1–S3 无）、`evidence_links`（:1513，提案扩展未进字段表）、`part_files`（:2740 U20） | 仍开放（本次 grep 证实仍在；VR-17 会报未知字段） |
| R2（=N7） | 低 | B3-00 子串判定对否定式/变体不健壮；B1-02 等字符串包含断言改标点即失效 | 仍开放 |
| R3（=N9/C4） | 低 | 正文 fenced block 字节保真（D-04 存亡前提）C4 运行时探针未获正面证据 | 仍开放，留 Phase 1 首 milestone 实测 |
| R4 | 中（治理） | 分发形态无正式裁决：`decisions/` D-09 仍 PENDING；开源 §0 已条件化，但项目层前提未立 | 仍开放（本次查 decisions/ 证实） |
| R5 | 低 | Quarto「改用 MIT 的具体发布 tag」未落实（commit 级已核实，tag 级抽样因 API 限速中止） | 仍开放（门禁日志如实标注） |
| R6（新观察） | 低 | `SYSTEM_ARCHITECTURE.md` §9 表仍无条件写「AGPL-3.0，不可用于闭源分发或 SaaS」，而 D-09 PENDING；本轮未触及架构文档，缺条件标记 | 仍开放（本次读 :191 区证实；复审 §6-3 已提示，未关闭） |
| R7 | 低（取证手法） | 测试 harness 对文件编码敏感：BOM 会使 `frontmatters()` 误判（本次首提取假失败 B5-04） | 非被审缺陷；建议后续提取一律字节精确 |

仍开放条目合计 **7 项（R1–R7），均非阻断**。

---

## 8. 是否可进入 Phase 1

**可以进入 Phase 1。** 依据：
- 6 个阻断项 B1–B6 本次独立复现全部 CLOSED（§3）；
- 门禁 N10/N1/N2/N8/N6 与条件 7–9 本次独立复现全部 CLOSED，且 G1-5 经**双重突变证明**（对修复前 9 条 FAIL、对单点突变仅 B3-07 FAIL）确认测试真能捕获回归（§4/§5-5）；
- 残留 R1–R7 均为非阻断的文档/治理/实测延后项。

**前置建议（不阻断开工）**：
1. Phase 1 首 milestone 做真实 Vault 实测关闭 R3（C4），不成立则按既有退路迁 `_maps/`；
2. 尽早把分发形态立为正式决策关闭 R4，并同步给 R6 的架构 §9 表加条件标记；
3. 用一个轻量修订清理 R1 的表外字段（免 VR-17 误报）；R2/R5/R7 可随手修。

**对流程的纠正建议**：复审「自审自活 + 自我降级」已被本次交叉验证证伪（§2）。后续凡涉及阻断项关闭，应以**原始审计原文**为关闭判据、由**独立方**复核，避免修复方自行缩窄范围放行。

---

*交叉验证执行：第三方 Agent（task_f6efa6a169f3）。本报告为唯一交付物；未修改任何被审文件；临时副本（%TEMP%\swp_xval_gate / swp_xval_mut）验证后已删除；`git status --porcelain` 复核为空。*
