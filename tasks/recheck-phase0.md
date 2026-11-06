# TASK: 复审 — Phase 0 关闭项复核

## 0. 背景

你是独立复审 Agent。上一轮 QA 判定 Phase 0 为 **FAIL**，列出 6 个阻断级缺陷与 9 条放行条件。本轮只复核**这些条目是否真的关闭**，不做全面重审。

## 1. 输入

- `reports/qa/PHASE_0_AUDIT_REPORT.md`（上一轮报告，含 B1–B6 与放行条件）
- `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` + `REVISION_LOG.md` + `tests/grammar_vectors.md` + `schemas/d04-compliant.example.md`
- `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` + `EVIDENCE_FIX_LOG.md` + `evidence/`
- `research/open-source-audit/OPEN_SOURCE_AUDIT.md` + `EVIDENCE_FIX_LOG.md` + `evidence/`
- `research/obsidian/CROSS_CONFIRMATION.md`
- `research/architecture/`、`decisions/`（仅用于比对一致性）

## 2. 交付物

`reports/qa/PHASE_0_RECHECK.md`

## 3. 复核方法

对每条放行条件给出：**CLOSED / PARTIAL / OPEN**，并附**你自己复现的证据**（不得只引用修订方自述）。

必须实际执行的验证（不得只看文字声明）：
1. 逐条比对 B1–B6 的修订是否与字段表、P2 表、VR 规则**三处一致**
2. 执行 `grammar_vectors.md` 中的测试向量，确认 B3/B6 的正则真的能匹配/不匹配
3. 检查 `d04-compliant.example.md` 的 frontmatter 是否真的**没有**任何嵌套对象
4. 重数 Manuscript §9 映射表，确认统计与逐行一致
5. 抽查 5 条 Manuscript 证据的 URL 是否可访问、结论是否与来源一致
6. 抽查 3 条 Open-source 证据，重点验证 Manubot 许可证与兼容矩阵
7. 检查「17 个实体」的表述是否已全部同步为 19

## 4. 判定规则

- 6 个阻断项全部 CLOSED → 至少 PASS WITH RISKS
- 任一阻断项仍为 PARTIAL / OPEN → 维持 FAIL
- 非阻断项（放行条件 7–9）为 PARTIAL → 记 RISK，不阻断

总体结论只能是：**PASS / PASS WITH RISKS / FAIL**。

## 5. 硬性约束

- 只写 `reports/qa/PHASE_0_RECHECK.md`。不得修改任何被审文件。
- 不得因为「改了很多」就放行；只看证据。
- 新发现的问题单独列「新问题」章节，不与原 B1–B6 混淆。

## 6. 交付文件结构

```
# Phase 0 Recheck
## 1. 总体结论
## 2. 阻断项复核表（B1–B6，含复现证据）
## 3. 放行条件复核表（1–9）
## 4. 实际执行的验证记录（命令/输入/输出）
## 5. 新问题
## 6. 剩余风险
## 7. 是否可进入 Phase 1
```

## 7. 交付方式

≤500 字总结 + 总体结论 + 仍开放条目数。
