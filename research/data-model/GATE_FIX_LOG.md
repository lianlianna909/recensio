# Phase 1 门禁修复日志 — 数据模型文法回归（G1-1 … G1-7）

> 修订对象：`research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md`（就地修订）及配套示例 / schema / 测试。
> 缺陷来源：`reports/qa/PHASE_0_RECHECK.md` §5（N1/N2/N6/N8/N10a–d）与 §7「Phase 1 开工前门禁」、放行条件 9。
> 交叉确认来源：`research/obsidian/CROSS_CONFIRMATION.md` C1/C2/C5（2026-11-06）。
> 约束遵守：**只改 `research/data-model/` 下文件**；不引入新实体、新原则；不删除复审报告任何条目来「关闭」问题；只做一致性与闭环。
> 自动验证：`python -I research/data-model/tests/run_vectors.py`。

---

## 0. 测试证据（新增测试对修复前失败、修复后通过）

| 阶段 | 命令 | 结果 |
| --- | --- | --- |
| 基线（修复轮原稿） | `python -I tests/run_vectors.py` | **82 checks, 0 failed** |
| 先加测试、文档未修（本门禁回归证明） | 同上 | **94 checks, 9 failed** |
| 文档修复后 | 同上 | **94 checks, 0 failed**（退出码 0） |

- 测试条数 **82 → 94**（+12）：新增 3 条 `{{pnl:…#A}}` 仲裁向量（G3-18/19/20）+ 9 条跨文档门禁断言（B3-07/08/09、B4-03、B5-05/06、C1-01、C2-01、C5-01）。
- 「先加测试、文档未修」一步**精确失败 9 条**：`B3-07 B3-08 B3-09 B4-03 B5-05 B5-06 C1-01 C2-01 C5-01`，与下方 G1-1…G1-7 一一对应；修复后全绿。这证明新增测试能捕获修复前的散文/示例缺陷（关闭 N8：测试不再只比对 §6.0.8 代码块与脚本自身，而是把散文裁定编码进断言）。
- 产物 `tests/grammar_vectors.md` 已由 `--emit` 重新生成（94 向量）。
- 附带健壮性修复：`main()` 增 `sys.stdout.reconfigure(errors="replace")`，避免 Windows GBK 控制台遇到 `↔` 等字符时崩溃（退出码只反映测试判定，不影响 `--emit` 的 UTF-8 落盘）。

**G1-1 最终裁定（一句话）**：保留宽 `TOKEN_RE`（不按 kind 拆分支），把非白名单 kind 带 `#panel` 统一裁为「**语法接受、语义拒绝**」（渲染器入口丢弃片段并报 VR-06），全文「语法错误」表述已清除。

---

## G1-1（N10a / B3-a）— `#panel` 语法判定自相矛盾

- **问题**：§6.0.4 规则 1 称非 `figref`/`pnl` kind 带 `#` 为「语法错误」，但 `TOKEN_RE` 对所有 kind 接受 `(?:\#panel)?`，§6.0.9/§6.4 又写「语法接受、语义拒绝」——同一节两种判定。
- **裁定**：取方案 **(b)**（宽正则 + 语义拒绝）。理由：① 若正则层收紧，非法组合按规则 5 落为普通文本，作者无报错；宽正则使非法组合仍被识别为 token，VR-06 才能精确定位（错误提示质量）；② 白名单作为数据（schema `token_panel_allowed_on`）维护，调整不必改改正则及其副本（实现成本）。
- **改了什么 / 位置**：
  - §6.0.4 规则 1 重写为「语法层一律接受、语义层白名单 `{figref, pnl}`、其它 kind 语法接受语义拒绝报 VR-06」，并写明不在正则层收紧的两条理由（`SCIENTIFIC_DATA_MODEL_PROPOSAL.md:1848`）。
  - §6.0.8 注文补「`(?:\#panel)?` 对所有 kind 开放是有意为之」（:1916）。
  - §6.4 渲染输入约定保持「语法接受、语义层校验」口径（:2050）；§9.2 VR-06 同步为「语义上只允许…语法接受、语义拒绝」（:2561）。
  - schema `token_panel_allowed_on` 注释同步（`entity-schemas.example.yaml:28`）。
- **自验**：新增 **B3-07**——断言 §6.0.4 含「语法接受、语义拒绝」且**不含**「语法错误」，同时断言可执行行为（`panel_scope_ok` 对 figref/pnl 放行、对其余 8 个 kind 拒绝）与 schema 白名单一致。修复前 FAIL（散文写「语法错误」），修复后 PASS。既有 G3-15b（8 个非白名单 kind 语法匹配但语义拒绝）继续守门。

## G1-2（N1 / B3-b）— `{{pnl:pnl_x#A}}` 语义未定义

- **问题**：§3.18 断言 `{{pnl:…}}` 接受 `#panel`（「显式字母覆盖」），但 Panel ID 再叠加字母时 (ID, label) 无优先级与冲突仲裁。
- **裁定**：**保留该写法并给出仲裁**——Panel ID 是身份唯一权威，面板字母权威来源是 `Panel.panel_label`；token 上的字母只作**渲染期断言**（assert，非 override），不一致报 VR-06，渲染仍以 `Panel.panel_label` 为准。
- **改了什么 / 位置**：
  - §6.0.4 规则 4 增「`{{pnl:pnl_…#A}}` 的仲裁」段（:1851）。
  - §3.18 一致性断言 3：「显式字母覆盖」→「显式字母断言」+ 权威来源说明（:1432）。
  - §6.4 渲染输入约定补 pnl 断言分支（:2050）；`renderText` 伪代码 `case "pnl"` 改为先 `assertPanelLabel` 再渲染，且不再把 token 字母拼进已含字母的编号（修正潜在的 `Figure 3BA` 双字母）。
  - §9.2 VR-06 增「`{{pnl:…#X}}` 字母与 `Panel.panel_label` 不一致亦报本规则」（:2561）。
- **自验**：新增 helper `pnl_label_assertion(token_panel, panel_label)` + 向量 **G3-18/19/20**（一致→ok、不一致→VR-06、省略→ok）；新增 **B3-08** 断言 §6.0.4 含「渲染期断言」、§3.18 含「显式字母断言」且全文不再有「显式字母覆盖」。修复前 FAIL，修复后 PASS。

## G1-3（N10c / B3-d）— §6.7 及全文非法示例 ID

- **问题**：`{{figref:fig_a}}–{{figref:fig_b}}` 中 `fig_a`/`fig_b` 不匹配 `ID_RE`（8 位 B32），按 §6.0.9 会被当普通文本。
- **改了什么 / 位置**：§6.0.4 规则 3 与 §6.4 `labelFor` 注释的并列 token 改为合法 ID `{{figref:fig_7K3M9Q2P}}–{{figref:fig_9WD4PKMR}}`。**全量 grep** 另清除以下非法占位 ID（均改为合法 ID 或 `XXXXXXXX` 占位 / `<msc_id>`  metavariable）：
  - `fig_7K3M9Q`（P4，:48，7 位）→ `fig_7K3M9Q2P`；`msc_x`（:489）→ `<msc_id>`；
  - `tab_x`（§3.17a :1325/1332）→ `tab_4XQ7NWKB`；`mth_x`（:1435）→ `mth_XXXXXXXX`；`fig_x`（:1437/2742）→ `fig_XXXXXXXX`；
  - `pnl_x--fig_y`（:1461）、`res_x--fig_y`（:1484）、`clm_x--res_y`（:1504）→ `XXXXXXXX` 占位；
  - `prj_A/prj_B/prj_C`（§4.5 :1541）→ `prj_AAAAAAAA/BBBBBBBB/CCCCCCCC`；
  - `par_x`（:2489/2722）、`par_xxx`（:2679）→ `par_XXXXXXXX`；
  - `REVISION_LOG.md:61` `Tables/tab_x.md` → `Tables/tab_XXXXXXXX.md`；
  - 测试 G3-11 负向用例输入改为「两个合法 ID 逗号合并」`{{figref:fig_7K3M9Q2P,fig_9WD4PKMR}}`（仍不匹配， stronger 负向），TAIL 等价断言同步。
- **自验**：新增 **B3-09**——扫描提案 / schemas / REVISION_LOG 中所有 ID 形串（跳过 `<…>` metavariable），逐一 `ID_RE.fullmatch`。修复前 FAIL（列出 25 处非法 ID），修复后 PASS。`grep -rE "fig_a|fig_b"` 在提案/示例中零命中（仅测试的「检测标签」提及，属 intentional）。

## G1-4（N2 / B3-c）— §2.1 关系图反向双权威边

- **问题**：mermaid 同时画 `RES -->|evidenced_by| FIG` 与 `FIG -->|result_refs| RES`，与 P2/B4「唯一权威边 `Figure.result_refs`、反向由索引派生不落盘」冲突；`evidenced_by` 全文无定义。
- **裁定**：**删除** `evidenced_by` 边（反向视图不落盘，画边即误导），并在图例显式说明反向查询为派生视图。
- **改了什么 / 位置**：§2.1 删除 `RES -->|evidenced_by| FIG`（原 :121）；图例补「反向视图由索引派生、不落盘，故不画 `RES → FIG` 反向边；`Result.figures` 只是缓存字段」（:145）。图与 P2 表（`Figure.result_refs[]` 唯一权威边）一致。
- **自验**：新增 **B4-03**——断言 §2.1 mermaid 块**不含** `evidenced_by`、**不含** `RES -->`、且**含** `FIG -->|result_refs| RES`。修复前 FAIL，修复后 PASS。

## G1-5（N8）— 测试无法锁定散文规则

- **问题**：B3-05 只在「§6.0.8 代码块」与「脚本 `grammar_source()`」之间比对，不检验 §6.0.2–§6.0.7 散文——这正是 B3-a 未被捕获的原因。
- **改了什么 / 位置**：`tests/run_vectors.py` 新增把散文裁定编码进断言的测试：**B3-07**（G1-1 裁定：散文「语法接受、语义拒绝」↔ `panel_scope_ok` 行为 ↔ schema 白名单三方互锁）、**B3-08**（G1-2 仲裁措辞）、**B3-09**（示例 ID 合法性）、**B4-03**（图权威边）、**B5-05/06**（示例 VR-15）、**C1-01/C2-01/C5-01**（回填）。
- **自验**：见 §0——「先加测试、文档未修」一步 B3-07 等 9 条**对修复前版本失败**，修复后全绿。B3-07 即 G1-5 要求的「对当前版本失败、对修复后通过」的散文↔正则互锁测试。

## G1-6（放行条件 9）— 交叉确认结论未回填

- **问题**：C1–C6 已判定但提案未回填：§3.3 仍以「唯一一处取决于审计结论」「若不允许下划线则改连字符」为待定口径；§5.6 仍写「若不允许下划线（`[待审计]`）」；C5 新发现（与 Templates `{{date}}` 同形、post-processor 仅 Reading view）在 §3.18/§6.6 无风险条目。
- **改了什么 / 位置**：
  - **C1**：§3.3（:512）改为「下划线**可以保留**（官方站点自身用带 `_` 的块 ID），连字符降为保险丝；大小写敏感性未能确认→生成器只输出大写+数字」；删除「唯一一处取决于审计结论」过时分支。§5.6（:1777）改为「C1 判定合法、映射降为保险丝分支、判重按规范化大写键」。
  - **C2**：§3.3 增「标题挂锚点」注（:533）——`[[#^id]]` 引用已确认；标题挂锚点**未能确认**但 `SectionCache.id` 有落点；退路为**权威方向反转**（`section_meta[].id` 为权威 + 段落式挂法）。
  - **C5**：§3.18 增「与 Templates 语法同形的风险」条目（:1439，含 4 级缓解：判别式收紧/保留字拦截/操作约束/`{{swp:…}}` 退路）；§6.6 增第 5 点风险（:2087）并把「可实现性」行与第 2 点的 `[待审计]` 更新为「C5 已确认 post-processor 可用、**仅 Reading view**、Live Preview 需另写 CM6 装饰」。
  - §11.1 表后增「交叉确认回填」总注（C1–C6 对 U1/U2/U4/U5 的结论）；`manuscript.example.md` 阅读提示 comment 同步 C1（:91）。
- **自验**：新增 **C1-01**（§3.3 含 C1/「可以保留」、无「唯一一处」；§5.6 含「保险丝」、无旧 `[待审计]` 条件句）、**C2-01**（§3.3 含 C2/「未能确认」/「反转」）、**C5-01**（§3.18 与 §6.6 含 Templates/`{{date}}`/同形/Reading view）。三条修复前 FAIL，修复后 PASS。

## G1-7（N6，低优先）— 示例件自身违规

- **问题**：`d04-compliant.example.md` 中 `sec_2JX9KQMW` 用两次（三级节 :83 与二级节 :101），自身违反 VR-15；`swp:sections` 的 role 与标题层级不自洽。`manuscript.example.md` 存在**同样**的重复（:63/:77）。
- **改了什么 / 位置**：给「Dose selection is critical」三级节分配独立 ID `sec_6XW2QKMP`（role: body，挂在 Introduction 下），`sec_2JX9KQMW` 仅保留于 `## Discussion`（role: discussion）。两份示例同步更新：`section_order`、`swp:sections`（新增 sec_6XW2QKMP 行）、标题锚点；`manuscript.example.md` 的 `_maps` 中 `par_1A2B3C4D.section` 同步改为 `sec_6XW2QKMP`。
  - `d04-compliant.example.md:47/62/84`；`manuscript.example.md:45/51/64/110`。
- **自验**：新增 **B5-05**（示例件过 VR-15：每个示例笔记内 `sec_/par_/eqn_` 块锚点零重复）与 **B5-06**（`swp:sections` 的 id 集合 ↔ 正文标题锚点集合相等且各自唯一）。修复前 FAIL（两份示例各报 `sec_2JX9KQMW` 重复），修复后 PASS。

---

## 文件清单（本轮改动，全部位于 `research/data-model/`）

| 文件 | 改动 |
| --- | --- |
| `SCIENTIFIC_DATA_MODEL_PROPOSAL.md` | G1-1/2/3/4/6 就地修订（§2.1/§3.3/§3.18/§5.6/§6.0.4/§6.0.8/§6.4/§6.6/§9.2/§11.1 + 全文非法 ID） |
| `tests/run_vectors.py` | G1-5：新增 9 条门禁断言 + 3 条仲裁向量 + helper；G3-11 负向用例合法化；GBK 控制台健壮性 |
| `tests/grammar_vectors.md` | `--emit` 重新生成（94 向量） |
| `schemas/d04-compliant.example.md` | G1-7：sec_6XW2QKMP 拆分重复 ID |
| `schemas/manuscript.example.md` | G1-7 同上 + G1-6 C1 comment 回填 |
| `schemas/entity-schemas.example.yaml` | G1-1：`token_panel_allowed_on` 注释同步裁定 |
| `REVISION_LOG.md` | G1-3：`tab_x.md` → `tab_XXXXXXXX.md` |
| `GATE_FIX_LOG.md` | 本日志（新增） |

## 完成标准核对

- [x] G1-1…G1-7 全部有「问题 → 裁定 → 位置 → 自验」记录（本文件）。
- [x] `run_vectors.py` 全绿（94 checks, 0 failed），测试条数增加（82 → 94）。
- [x] 全文再无 `fig_a`/`fig_b` 这类非法示例 ID（B3-09 守门；提案/示例零命中）。
- [x] §2.1 图与 P2 表无矛盾边（B4-03 守门；唯一权威边 `Figure.result_refs`）。
- [x] 新增测试对修复前版本失败（9 条）、修复后通过（§0 证据）。
- [x] 只改 `research/data-model/`；未引入新实体/新原则；未删除复审报告条目。