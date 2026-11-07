# 修订日志 — 数据模型阻断项修复（B1–B6，draft-1 → draft-2）

> 修订对象：`research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md`
> 缺陷来源：`reports/qa/PHASE_0_AUDIT_REPORT.md` §4（B1–B6），其中 B3/B4 的处置方式由总控裁定。
> 约束遵守：只改 `research/data-model/` 下文件；不引入新实体设计原则（新增的两个实体由 B3 裁定要求）；原章节编号保留（新增内容以 §3.0.5–§3.0.7、§3.17a、§3.17b、§4.1a、§6.0、§13 插入）。
> 自动验证：`python -I research/data-model/tests/run_vectors.py` → **82 checks, 0 failed**（2026-11-06）。产物：`tests/grammar_vectors.md`。

---

## 一览

| # | 缺陷 | 修复性质 | 类型 | 验收证据 |
| --- | --- | --- | --- | --- |
| B1 | Figure↔Panel 双权威边 | 降级一处为血缘 | 一致性 | 向量 B1-01/02/03；§4.1 |
| B2 | `RevisionIssue.targets[]` 两套形态 | 合并为唯一形态 | 一致性 | 向量 B2-01/02；§4.6 |
| B3 | 实体缺失 + 文法分散/冲突 | 新增 2 实体 + 文法单点化 | 裁定项 | 向量 G1–G5、B3-00…B3-06 |
| B4 | Result↔Figure 双写未入 P2 | 降级一处为缓存 | 一致性 | 向量 B4-01/02；§4.1a |
| B5 | 字段表违反 D-04 | 落位重构（不改语义） | 裁决落地 | 向量 B5-01…B5-04；示例文件 |
| B6 | `ANCHOR_RE` 不接受 `_` | 正则修正 | 缺陷 | 向量 G4-01…G4-10、B6-01…B6-06 |

---

## B1 — `Panel.figure` 与 `Panel.derived_from` 构成双权威边

**缺陷（QA §4 B1）**：Figure↔Panel 关系同时由 `Panel.figure` 与 `Panel.derived_from` 表达，P2「单一写入点」被违反；`Figure.panels` 又未声明权威归属，三处可写。

**修复**
1. `Panel.figure` 定为**唯一权威边**，字段表直接标注「**唯一权威边**（P2 表决）」。
2. `Panel.derived_from` **降级为纯血缘**：类型仍为 `list<wikilink>`，但说明改为「纯血缘，不是边」，并撤销 draft-1 中「必须含 figure」的要求（该要求正是双权威的来源）。
3. `Figure.panels` 标注为**派生缓存**（`cache_of: Panel.figure`），由 `_index/` 重建。
4. P2 表补「Figure ↔ Panel」行并加合并注：`derived_from` 任何类型都不承担边语义（`Figure.derived_from` 同样改为纯血缘）。
5. §4.1 增加仲裁规则：两份数据冲突时 `Panel.figure` 无条件胜出（VR-46）。

**位置**：§1 P2 表；§3.5 `panels` / `derived_from` 行 + 「B4 边归属」注；§3.6 `figure` / `derived_from` 行；§4.1；§4.8 权威边一览；§9.2 VR-46；`schemas/entity-schemas.example.yaml`（`panel.figure.authoritative_edge: true`、`panel.derived_from.lineage_only: true`、`figure.panels.cache_of`）。

**证据**：`tests/grammar_vectors.md` → B1-01（P2 表存在 `| Figure ↔ Panel | \`Panel.figure\` |`）、B1-02（`derived_from` 行含「纯血缘」）、B1-03（`figure` 行含「唯一权威边」）。

---

## B2 — `RevisionIssue.targets[]` 在 §3.15 与 §4.6 各写一套

**缺陷（QA §4 B2）**：两处键集与必填规则不一致（一处 `{par, para_ref, quote, note}`，一处 `{par, manuscript, section?, quote_hint?, patch?}`），校验器无所适从。

**修复**
1. 唯一形态：`{par, manuscript, section?, quote_hint?, patch?}`，**仅 `par` 与 `manuscript` 必填**；可选键缺省即省略，不写 `null`/空串。
2. §3.15 字段表逐键给出约束；§4.6 改为「唯一形态见 §3.15」，只展开键语义与校验，不再自带第二套定义。
3. `Patch.targets` 明确为另一 schema `{par, field?, operation?}`，复用块名 `swp:targets` 但互不引用。
4. VR-17 增加**闭集校验**：未知键 → 错误。

**位置**：§3.15 `targets` 行；§4.6「B2 修订（唯一形态）」段 + 键表 + YAML 示例；§9.2 VR-17；§13 表。

**证据**：向量 B2-01（提案出现唯一形态字面量）、B2-02（§4.6 出现「唯一形态见 §3.15」）；`schemas/entity-schemas.example.yaml` `revision_issue.targets` 的 `placement: swp:targets` + `closed_keys: true`。

---

## B3 — 正文 token 无实体承载，且文法分散在四处互相矛盾（总控裁定）

**缺陷（QA §4 B3，总控裁定）**：`{{tab:}}`、`{{eq:}}`、`{{figref:…#B}}` 在正文语法里有，实体清单里没有；`{{pnl:}}` 在 §3.18 词汇表缺失；ID 前缀、块锚点、TOKEN、哈希剥离四类文法在 §3/§5/§6 各写一套，其中 §6.7 的 `[a-z]{3}_` 与 `eq_` 两字母前缀直接冲突——这就是审计复现报错的根因。

**修复**
1. **新增 Table（`tab_`）**：§3.17a，独立文件 `Tables/tab_XXXXXXXX.md`，完整字段表（`caption` / `caption_title` / `number`（派生不落盘）/ `anchor`（派生）/ `label_prefix` / `body_columns` / `footnotes` / `source_asset` / `source_anchor` / `width_mm` …）。
2. **新增 Equation（`eqn_`）**：§3.17b，内联弱实体，ID 权威 = 公式行尾 `^eqn_…`，元数据进 `swp:equations`；`number` / `anchor` 为派生不落盘。
3. **实体总数 17 → 19**：§2.1 关系图、§2.2 清单（第 18/19 行）、§3.0.1 前缀注册表、§9.1、§11.4 W3、附录 A/B、§13 全部同步；全文不再出现「17 个实体」表述。
4. **`#panel` 进入 TOKEN 文法**：`PANEL_LETTER := [A-Z][0-9]?`，只允许出现在 `figref` / `pnl`（语法层接受，语义层拒绝，VR-06）。
5. **`{{pnl:}}` 保留**：不删除，给出理由（Panel 有自有 ID，可被 targets/derived_from/索引直引；`{{figref:…\#B}}` 只是渲染便捷写法、不产生 Panel ID），并规定二者去重规则（按解析出的 (fig, panel) 对比较，VR-03）。
6. **`eq_` 不采用**：统一 `eqn_`；token kind `eq`/`eqref` 与前缀 `eqn` **解耦**，映射只在 §6.0.2 表维护。
7. **文法单点化**：新建 **§6.0**（6.0.1 设计目标 → 6.0.8 可执行定义 → 6.0.9 测试向量），ID / 块锚点 / TOKEN / `ANCHOR_RE` / 内联引文 / `swp:` 块六类文法**只在此定义**；§3.0.1、§3.0.5、§3.18、§5.3、§5.6、§6.2–§6.7、§9.2（VR-01/VR-20）只引用。
8. 既有章节内的旧正则全部拆除：§6.4 `renderText` 不再声明 `TOKEN`，改为消费 §6.0.8 `TOKEN_RE`；§6.3 `flattenInDocumentOrder` 覆盖 `tab`/`tabref`/`eq`/`eqref`/`pnl`。

**位置**：§2.1、§2.2、§3.0.1、§3.0.5、§3.17a、§3.17b、§3.18、§6.0（新）、§6.2、§6.3、§6.4、§6.7、§9.1、§9.2（VR-01、VR-20）、§11.4 W3/W7、附录 A/B、§13；`schemas/entity-schemas.example.yaml`（`id_pattern` 含 `tab|eqn`、`id_prefix_count: 19`、`token_kinds`、`kind_to_prefix`、`table`/`equation` 实体）。

**证据**：
- `tests/grammar_vectors.md` G1-01…G1-09（ID）、G2-01…G2-05（锚点 ID 子集）、G3-01…G3-17（token，含 `{{figref:fig_7K3M9Q2P#B}}` → panel=B）、G3-15b（8 个 kind 的 `#panel` 语义拒绝）、G4、G5。
- 跨文档断言：B3-00（19 且无「17 个实体」）、B3-01（「唯一权威定义」）、B3-02（「词汇表不重复定义文法」）、B3-03、**B3-05（§6.0.8 代码块与 `run_vectors.py` 中可执行副本逐字相等 → 文法不可能再漂移）**、B3-06（schema 的 `id_pattern`/`kind_to_prefix` 与 §6.0 同步）。

---

## B4 — `Result.figures` 与 `Figure.result_refs` 双写且未进 P2 表（总控裁定）

**缺陷（QA §4 B4）**：Result↔Figure 有两处写入点，draft-1 在两处互相推诿（"权威见对方"），P2 表缺该行。

**修复**
1. `Figure.result_refs[]` 定为**唯一权威边**（Figure 是呈现方）。
2. `Result.figures` 标注 **派生缓存**（`cache_of: Figure.result_refs`），可整体重建。
3. P2 表补「Result ↔ Figure」行；§4.7 成本表补行；§4.8 权威边一览注明共 6 条。
4. 新增 §4.1a 记录 A/B/C 三方案比较与「Figure 侧权威」的裁定理由。

**位置**：§1 P2 表；§3.5 `result_refs`；§3.7 `figures`；§4.1a（新）；§4.7；§4.8；§9.2 VR-46；§13。

**证据**：向量 B4-01（P2 表出现 `| Result ↔ Figure | \`Figure.result_refs[]\` |`）、B4-02（`Result.figures` 行为「派生缓存」且指明「权威来源是 `Figure.result_refs`」）。

---

## B5 — 字段表大量使用 frontmatter 对象 / `list<object>`，与已 ACCEPTED 的 D-04 冲突

**缺陷（QA §4 B5 + D-04）**：`x_ext`（object）、`numbering_scheme`、`section_meta`、Panel 的 `crop`/`layout`/…、`Issue.targets`、`authors`/`affiliations`/`funding`/`abbreviations`、`parameters`/`software`/`reagents`、`conditions`、`Paragraph.citations` 全部落在 frontmatter，D-04 明令禁止。

**修复**
1. 新增 **§3.0.6**：三种落位（F / B(`swp:<name>`) / PL）+ `swp:` 块名注册表（`swp:meta`、`swp:sections`、`swp:equations`、`swp:citations`、`swp:targets`、`swp:params`、`swp:checks`）+ 5 条硬规则（frontmatter 四种合法形态、块必须可被纯文本解析、块是权威、`x_ext` 不再为对象、MINOR 兼容读）。
2. 新增 **§3.0.7**：**26 行逐字段落位映射表**，覆盖 draft-1/draft-2 全部 `object` / `list<object>` 字段，逐行给理由（为何选块而非平行列表，或反之）。
3. **`x_ext` 改为标量**：frontmatter 只是 `text`；结构化扩展落 `swp:meta` 的 `x_ext:` 键。§7.6 的弃用字段落点随之改写（`caption_html` → `swp:meta#x_ext.legacy.caption_html`）。
4. 各实体字段表逐行改写：Project（`author_*` 4 列 / `affiliation_*` 5 列 / `funder_*` 2 列 / `abbreviation_*` 2 列）、Manuscript（`numbering_*` 6 列、`section_meta`→`swp:sections`、`equation_meta`→`swp:equations`）、Figure（`panel_layout_cols/rows`）、Panel（7 项坐标进 `swp:meta`，附完整示例块）、Method（`parameter_*` 3 列、`software`/`reagents`→`swp:params`）、Experiment（`condition_*` 3 列）、Issue/Patch（`targets`→`swp:targets`）、Paragraph（`citations`→`_maps`）。
5. 新增两条校验规则：**VR-53**（平行列表两两等长）、**VR-54**（frontmatter 禁止映射/`list<object>`），并纳入 §9.3 执行矩阵与 §9.5 自动修复边界；§9.2 规则数 52 → 54。
6. R4（嵌套 frontmatter 风险）**关闭**；U1 收窄为「正文 `swp:` 代码块是否保真」。
7. 交付 **`schemas/d04-compliant.example.md`**：两份完整笔记（Manuscript + RevisionIssue），frontmatter 全标量/标量列表/wikilink 列表，四个 `swp:` 块齐备，并附 draft-1 反例与「为何 targets 用块而 authors 用平行列表」的对照。

**位置**：§3.0.2、§3.0.6、§3.0.7、§3.1–§3.16 各字段表、§7.3、§7.6、§9.2（VR-53/VR-54）、§9.3、§9.5、§10 R4、§11.1 U1、附录 A、§13；`schemas/d04-compliant.example.md`（新）、`schemas/entity-schemas.example.yaml`（`placement:` 标注 + `d04_placement:` 声明块）、`schemas/manuscript.example.md`（frontmatter 扁平化 + `swp:sections` + `x_ext` 标量）。

**证据**：向量 B5-01（示例文件**每个** frontmatter 块零嵌套）、B5-02（`swp:meta`/`sections`/`equations`/`citations`/`targets` 齐备）、B5-03（VR-53/VR-54 在提案中存在）、B5-04（`manuscript.example.md` 亦零嵌套）；跨文档 B5-02 行（§3.0.7 含 `x_ext`→`swp:meta`）。

---

## B6 — `ANCHOR_RE` 不接受下划线，`text_hash` 随锚点拼写漂移

**缺陷（QA §4 B6）**：`ANCHOR_RE = \s+\^[a-z]{3}-?[0-9A-HJKMNP-TV-Z]{8}\s*$` 只接受 `-`，而主写法是 `^par_…`；于是同一段落加锚点前后 `text_hash` 不同，全库漂移误报。

**修复**
1. `ANCHOR_RE = re.compile(rf"\s+\^(?:sec|par|eqn)[_-]{B32}{{8}}\s*$")`，定义只在 §6.0.5，§5.3 伪代码改为从 `swp.grammar` 导入，不再本地声明。
2. `eqn_` 纳入（否则公式块锚点污染哈希）。
3. §5.6 明确编解码器对 `_` / `-` 两种拼写都透明处理，且它是唯一产出锚点字符串的地方。
4. §11.1 U2 增加「`_` 是否合法块 ID 字符」的实测请求。

**位置**：§5.3、§5.6、§6.0.5、§6.0.8、§9.2 VR-17、§11.1 U2、§13。

**证据**：向量 B6-01…B6-06 —— 同一段落「无锚点 / `^par_…` / `^par-…` / 锚点+行尾空白 / 尾换行」五种写法 `text_hash` **全等**（`b61d80e882d0b66f`），内容真的变化时（B6-06）哈希**不同**（`19a0d16d7aa79946`）；G4-01/02/03/04/09/10 证明 `_`、`-`、标题行、公式块锚点均被正确剥离；跨文档 B6-00 断言 §5.3 与 §6.0.5 使用同一条正则字面量。

---

## 验证方式（可直接执行）

```bash
python -I research/data-model/tests/run_vectors.py          # 82 checks, 0 failed; 非 0 退出码 = 有回归
python -I research/data-model/tests/run_vectors.py --emit   # 重新生成 tests/grammar_vectors.md
```

覆盖：ID/锚点 ID/token/内联引文/哈希剥离/`swp:` 块六类文法向量（G1–G5，B6），D-04 示例文件结构（B5-01/02/04），以及 15 条跨文档一致性断言（B1/B2/B3/B4/B5/B6），其中 B3-05 逐字比对 §6.0.8 代码块与本脚本的可执行副本，B3-06 比对 schema 的 `id_pattern`/`kind_to_prefix` —— **字段表 / 正则 / 示例文件三者的同步由测试强制，不靠人工**。

## 影响范围声明

- 未改动 `research/architecture/`、`decisions/`、`AGENTS.md` 及其它 Worker 目录。
- 实体语义未变：B1/B4 只改「谁是权威」，B5 只改「字段放在哪」，B6 只改「锚点怎么写都不影响哈希」。
- 新增两个实体（Table/Equation）与两条校验规则（VR-53/54）均来自总控对 B3 的裁定与 D-04 的落地需要，不是新设计原则。
