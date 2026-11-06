# TASK: 修订轮 — 数据模型阻断项修复 (B1–B6)

## 0. 背景

独立 QA 对 `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` 判定 FAIL，列出 6 个阻断级缺陷。你的任务是把这 6 项全部关闭，产出一份**可被 schema 直接实现**的修订版。

不要重写整篇文档。只修缺陷，保留原有结构与编号，用「修订说明」章节记录改动。

## 1. 交付物

1. `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` — 就地修订（保留原章节号）
2. `research/data-model/REVISION_LOG.md` — 逐条：缺陷 → 改了什么 → 在哪一节 → 证据
3. `research/data-model/tests/grammar_vectors.md` — B3/B6 的匹配测试向量（输入 → 期望结果）

## 2. 六项修复要求

### B1 Figure↔Panel 双权威边
`Panel.figure` 与 `Panel.derived_from` 同时自称权威。
**要求**：指定 `Panel.figure` 为唯一权威边；`derived_from` 改为纯血缘字段（仅记录来源 Figure/Panel，不承担边语义）。在 P2 表中补录该边。给出修订后的字段表行。

### B2 RevisionIssue.targets[] 两种形态
§3.15 是 `{par, manuscript, section?}`，§4.6 是 `{par, manuscript, quote_hint?, patch?}`。
**要求**：统一为**一种**形态，建议取并集 `{par, manuscript, section?, quote_hint?, patch?}`，必填仅 `par` 与 `manuscript`。同步 §4.6 与 §9 的 VR-17。

### B3 编号 token 体系三处矛盾
问题：`{{tab:}}`/`{{eq:}}` 无对应实体；ID 前缀正则不含 `tab`/`eq`；`{{figref:fig_x#B}}` 的 `#` 不被 TOKEN 正则接受；`{{pnl:…}}` 不在词汇表；`eq` 两字母不满足 `[a-z]{3}_`。

**总控已裁定**：
- **新增 Table 与 Equation 两个实体**（实体总数 17 → 19），前缀分别为 `tab_` 与 `eqn_`。
- 面板引用统一写成 `{{figref:fig_XXXXXXXX#B}}`，TOKEN 正则必须接受 `#<panel-letter>` 可选片段。
- `{{pnl:…}}` 补入 §3.18 词汇表，或删除（二选一并说明理由）。
- **建立唯一的文法定义节**（建议 §6.0），词汇表、TOKEN 正则、ID 前缀正则三处**引用同一份定义**，不得各写一套。

**要求**：给出 Table / Equation 的完整字段表（语义、ID、位置、字段、生命周期），至少覆盖 `caption / number / anchor / source / notes`。

### B4 Result↔Figure 边无主
**总控已裁定**：`Figure.result_refs[]` 为**唯一权威边**（Figure 是呈现方，指向它所呈现的 Result）；`Result.figures[]` 降级为派生缓存，并在注释中明确标注。P2 表补录该边。

### B5 字段表未对齐 D-04
D-04 已 ACCEPTED：frontmatter 只允许标量 / 标量列表 / wikilink 列表；结构化子对象必须放正文 fenced YAML 块。

**要求**：
1. 输出一张**逐字段落位映射表**，覆盖全部 object / list<object> 字段（`x_ext`、`numbering_scheme`、`Panel.crop/layout/canvas/transform`、`section_meta`、`targets`、`authors`、`affiliations`、`funding`、`abbreviations`、`parameters`、`software`、`reagents`、`conditions`、`citations` 等），每行标注：字段 → 落位（frontmatter / 正文 YAML 块 / 平行列表）→ 理由。
2. `x_ext` 必须改为正文 YAML 块或删除。
3. 提供一份符合 D-04 的完整示例文件 `research/data-model/schemas/d04-compliant.example.md`。

### B6 ANCHOR_RE 与主语法不匹配
`ANCHOR_RE = r"\s+\^[a-z]{3}-?[0-9A-HJKMNP-TV-Z]{8}\s*$"` 匹配不了 `^par_9QK2M4XZ`（下划线）。
**要求**：修正正则以同时接受 `_` 与 `-`；提供测试向量：同一段落加/不加锚点、两种锚点写法，`text_hash` 必须一致。

## 3. 硬性约束

- 只改 `research/data-model/` 下的文件。不得修改 `research/architecture/`、`decisions/`、`AGENTS.md`、其他 Worker 目录。
- 不得引入新的实体设计原则；只修一致性。
- 每个修复必须可验证：字段表 / 正则 / 示例文件三者一致。
- 修订后实体总数 19，全文所有「17 个实体」的表述必须同步更新。

## 4. 完成标准

- 6 项全部有「缺陷 → 修复 → 位置」记录
- 文法只有一处定义，其余引用
- `d04-compliant.example.md` 中不含任何嵌套对象 frontmatter
- 测试向量可被直接执行（给出输入与期望输出）

## 5. 交付方式

≤600 字总结 + 文件清单 + 每项一行修复说明。
