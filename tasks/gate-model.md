# TASK: Phase 1 门禁 — 数据模型文法回归修复

## 0. 背景

复审报告 `reports/qa/PHASE_0_RECHECK.md` 判定 Phase 0 为 PASS WITH RISKS，B1–B6 全部 CLOSED。但它同时列出 §7 的「Phase 1 开工前门禁」：修复轮给 `research/data-model/` 引入了 4 处文法回归瑕疵（N10 a–d），另有 N1/N2/N8 与放行条件 9 未闭环。本轮只关闭这些，不重做模型。

## 1. 交付物

1. `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` — 就地修订
2. `research/data-model/GATE_FIX_LOG.md` — 逐条：问题 → 改了什么 → 位置 → 自验方式
3. `research/data-model/tests/run_vectors.py` — 补测试（见 G1-5）

## 2. 必须关闭的条目

### G1-1（N10a / B3-a）`#panel` 的语法判定自相矛盾
§6.0.4 规则 1 与 §6.0.8 注文说「`#panel` 用在非 `figref`/`pnl` kind 上是**语法错误**」，但 `TOKEN_RE` 对所有 kind 都接受 `(?:\#panel)?`，§6.0.9 判定语义又写「语法接受、语义拒绝」。**同一节两种判定。**
**要求**：二选一并全文统一——(a) 按 kind 拆分支，让非白名单 kind 真的语法不匹配；或 (b) 保留宽正则，把所有「语法错误」的表述改写为「语法接受、语义拒绝」。选 (b) 时必须说明为何不在正则层收紧（例如实现成本、错误提示质量）。

### G1-2（N1 / B3-b）`{{pnl:pnl_x#A}}` 语义未定义
§3.18 断言 `{{pnl:…}}` 接受 `#panel`，但 §6.0.4 规则 4 说 `{{pnl:…}}` 是按 Panel ID 指涉，且 `{{figref:…#B}}` 不产生 Panel ID。一个 Panel ID 再叠加字母覆盖时，(ID, label) 无优先级与冲突仲裁。
**要求**：给出明确仲裁（例如「`Panel.panel_label` 为权威，token 上的字母只作渲染期断言，不一致则报 VR 错误」），或从词汇表删除该写法。删除时须同步 §3.18、§6.0.4 规则 4、测试向量。

### G1-3（N10c / B3-d）§6.7 示例使用非法 ID
§6.7 的归一化伪代码与示例写 `{{figref:fig_a}}–{{figref:fig_b}}`，但 `fig_a`/`fig_b` 不匹配 `ID_RE`（8 位 B32），按 §6.0.9 会被当普通文本。
**要求**：改为合法 ID，并检查全文是否还有其他非法示例 ID（`grep` 全量）。

### G1-4（N2 / B3-c）§2.1 关系图出现反向双权威边
mermaid 图里同时画 `RES -->|evidenced_by| FIG` 与 `FIG -->|result_refs| RES`，与 P2/B4「唯一权威边 `Figure.result_refs`，反向由索引派生、不落盘」冲突；`evidenced_by` 全文无定义。
**要求**：删除 `evidenced_by` 边，或改成显式标注为「派生视图（不落盘）」的虚线并加图例。图与 P2 表必须一致。

### G1-5（N8）测试无法锁定散文规则
`run_vectors.py` 的 B3-05 只在「§6.0.8 代码块」与「脚本自身 grammar_source()」之间比较，不检验 §6.0.2–§6.0.7 的散文描述——这正是 B3-a 未被捕获的原因。
**要求**：新增至少一条测试，把 G1-1 的最终裁定（kind 白名单或「语义拒绝」口径）编码进断言，使散文规则与可执行正则互相锁定。测试必须能对当前版本失败、对修复后版本通过（在 GATE_FIX_LOG 中说明这一点）。

### G1-6（放行条件 9）交叉确认结论未回填
`research/obsidian/CROSS_CONFIRMATION.md` 的 C1–C6 已给出判定，但提案未回填：
- §3.3 仍写「这是本提案唯一一处取决于审计结论的语法细节」并以「若不允许下划线则改连字符」为待定口径，而 C1 已判定 `_` **可以**保留；
- §5.6 仍写「若 Obsidian 块 ID 不允许下划线（`[待审计]`）」；
- C5 的新发现（`{{figref:…}}` 与 Templates 核心插件 `{{date}}` 同形；post-processor 仅作用于 Reading view）在 §3.18/§6.6 **无任何风险条目**。
**要求**：把 C1/C2/C5 的结论回填，删掉已过时的待定分支，并在 §3.18/§6.6 增加「与 Templates 语法同形」的风险条目与缓解（如统一前缀 `{{swp:…}}` 或要求 token 必须含 `_` 且匹配 ID_RE）。

### G1-7（N6，低优先）示例件自身违规
`schemas/d04-compliant.example.md` 中 `sec_2JX9KQMW` 被用两次（:83 三级节、:101 二级节），自身违反 VR-15；`swp:sections` 的 role 与标题层级不自洽。
**要求**：修正示例，并把「示例件过 VR-15」加入 `run_vectors.py`。

## 3. 硬性约束

- 只改 `research/data-model/` 下文件。**不得**修改 `reports/qa/`、`research/architecture/`、`decisions/`、其他 Worker 目录、`AGENTS.md`。
- 不得引入新实体、新原则；只做一致性与闭环。
- 不得删除复审报告中列出的任何条目来「关闭」问题。
- 每条修复必须可执行验证：`python tests/run_vectors.py` 必须全绿，且新增测试对修复前版本会失败。

## 4. 完成标准

- G1-1…G1-7 全部有「问题 → 裁定 → 位置 → 自验」记录
- `run_vectors.py` 全绿，且测试条数增加
- 全文再无「`fig_a`/`fig_b`」这类非法示例 ID
- §2.1 图与 P2 表无矛盾边

## 5. 交付方式

≤600 字总结 + 文件清单 + G1-1 的最终裁定一句话。
