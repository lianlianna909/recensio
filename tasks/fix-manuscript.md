# TASK: 修订轮 — Manuscript 报告证据修复

## 0. 背景

独立 QA 对 `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` 判定 RISK，指出 3 条来源与结论不符、5 条不可核验、1 处统计错误。你的任务是把证据链补到可复核。

不要重写报告结构，只修证据与错误结论。

## 1. 交付物

1. `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` — 就地修订
2. `research/manuscript/evidence/` — 证据快照（每条证据一个文件或一份清单）
3. `research/manuscript/EVIDENCE_FIX_LOG.md` — 逐条：问题 → 改了什么 → 新证据位置

## 2. 必须修复的具体问题

### F1 python-docx 修订能力断言错误（最严重）
现报告称 python-docx「Track Changes：好」，但 python-docx 公开 API **没有**修订标记接口，`w:ins`/`w:del` 需手工操作 oxml 层。
**要求**：更正为准确描述，并给出证据（官方 API 文档页面 URL + 实际可用的底层接口说明）。这条直接影响 D-03 选型，必须写清楚「能做什么 / 不能做什么」。

### F2 `wDocumentChange` 类不存在
Open XML SDK 没有 `wDocumentChange` 这个类，对应类型是 `Insertion` / `Deletion` 等。
**要求**：更正出处，给出真实类型名与文档 URL。

### F3 mammoth.js GitHub Issues #342/#456 不可核验
**要求**：补全仓库名 + issue URL + 标题；若无法核实，删除该引用并改用可核验来源。

### F4 「工具实测」数据无产物
§8.2 的 95%/85%/60-70% 等数字无样本、无脚本、无产物，且与「只读研究、不安装依赖」的约束矛盾。
**要求**：删除这些数字，改为「需实测」并列入未确认事项；或补上可复现的测试方法。

### F5 §9 映射表统计错误
报告自报「完全可逆 1 / 单向可逆 19 / 有损 6 / 不可行 14」合计 40，实际表格 33 行，真实分布为 1 / 19 / 3 / 10。
**要求**：逐行重数并更正，确保分类合计 = 表格行数。同时复核分类本身。

### F6 `w:tblMergeCell` 不是标准 OOXML 元素
实际为 `w:gridSpan` / `w:vMerge`。
**要求**：更正元素名。

### F7 批注 XML 示例不规范
`w:commentRangeStart` 实际用 `w:id`，无 `w:ref` / `w:type="range"`。
**要求**：给出符合 OOXML 规范的批注示例。

### F8 文首日期错误
写成 2024-11-06，应为 2026-11-06。

### F9 证据清单缺 URL/版本
E1–E10 多数无 URL、无版本定位。
**要求**：每条证据补齐「URL 或 文件+版本+章节」；确实无法定位的，明确标注「不可核验」并从结论依赖中移除。

## 3. 硬性约束

- 只改 `research/manuscript/` 下文件。
- 不得修改 `research/architecture/`、`decisions/`、其他 Worker 目录、`AGENTS.md`。
- 不得编造 URL。无法核实的，如实标注。
- 结论若因证据不足需要下调置信度，必须显式下调，不得保留原置信度。

## 4. 完成标准

- F1–F9 全部有处理记录
- 证据清单每行都有 URL 或「不可核验」标注
- §9 统计与表格逐行一致
- 所有「实测」数字要么有产物，要么已删除

## 5. 交付方式

≤600 字总结 + 文件清单 + F1 的最终结论一句话。
