# TASK: Independent QA - Phase 0 Audit Review

## 0. 角色

你是独立 QA Agent，不属于任何 Worker 团队。你的职责是**证伪**，不是背书。你审的是四份 Phase 0 研究报告，以及由总控 Agent 汇总的架构文档。

## 1. 输入

- `research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md`
- `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md`
- `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md`
- `research/open-source-audit/OPEN_SOURCE_AUDIT.md`
- `research/architecture/SYSTEM_ARCHITECTURE.md`
- `research/architecture/DEVELOPMENT_ROADMAP.md`
- `decisions/ARCHITECTURE_DECISIONS.md`

若某文件缺失，直接记为 FAIL 项并在报告中说明，不要臆测其内容。

## 2. 唯一交付物

在工作区根目录创建：

`reports/qa/PHASE_0_AUDIT_REPORT.md`

除此之外不得写任何文件。

## 3. 必审清单（逐项给出 PASS / FAIL / RISK，并附证据）

1. **来源可追溯**：所有核心结论是否有可核验来源（URL、源码文件+行号、官方类型定义、许可证原文）？抽查至少 15 条结论，逐条标注"可核验 / 不可核验 / 来源与结论不符"。
2. **技术判断有源码或官方文档证据**：抽查关键 API 断言，验证是否真实存在。
3. **数据模型内部一致性**：实体间是否存在循环依赖、字段冲突、ID 冲突、孤儿关系；17 个实体是否都有字段表；多对多方案是否自洽。
4. **原始文件保护**：是否明确原稿（DOCX/PDF/图片）只读、不可变、有校验（哈希）；是否有"导入失败不会破坏原稿"的机制。
5. **DOCX 导入失败与信息丢失**：是否覆盖失败回滚、部分导入、Track Changes 丢失、样式丢失；是否有明确的用户可见告警设计。
6. **是否错误依赖 WritingLab Core**：架构是否把 WritingLab Core 当成必需组件？是否明确其为可选 Adapter？边界是否清晰。
7. **是否夸大 Obsidian 原生能力**：是否把"社区插件能做"写成"官方 API 支持"；Bases 能力描述是否超出实际。
8. **许可证问题**：可复用性判定是否与许可证冲突（尤其 GPL/AGPL 与闭源分发）。
9. **Revision Engine 核心需求**：RevisionRound / RevisionIssue / Patch / Response 是否覆盖"审稿意见 → 定位段落 → 生成修改 → 回复信"的完整闭环；是否遗漏版本快照与回滚。

## 4. 硬性约束

- 不得修改任何被审文件。你只读、只写自己的报告。
- 不得因为"看起来合理"就判 PASS。无证据即 FAIL 或 RISK。
- 不得提出新的架构方案——只指出问题与缺口。
- 结论必须可执行：每个 FAIL 要写"缺什么、在哪里缺、补上需要什么证据"。

## 5. 交付文件结构（必须遵守）

```
# Phase 0 Audit Report
## 1. 总体结论：PASS / PASS WITH RISKS / FAIL
## 2. 逐项审计结果表（9 项，含判定与证据）
## 3. 核心结论抽样核验（≥15 条）
## 4. 严重问题（阻断级）
## 5. 中等问题
## 6. 轻微问题
## 7. 数据模型一致性检查结果
## 8. 许可证与依赖风险
## 9. 遗漏项清单
## 10. 放行条件（若为 PASS WITH RISKS 或 FAIL，列出必须补齐的条目）
```

## 6. 完成标准

- 9 项全部有判定，不允许"部分通过"这种模糊结论。
- 总体结论只能是 PASS / PASS WITH RISKS / FAIL 三者之一。
- 抽样核验表至少 15 行。
- 回复中报告：审计范围、总体结论、阻断问题数、放行条件、文件路径。

## 7. 交付方式

简短总结（≤500 字）+ 文件路径。
