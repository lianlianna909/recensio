# TASK: Worker C - Scientific Modeler

## 0. 角色与项目背景

你是 ScientificWritingProject 的 Scientific Modeler，负责设计整个系统的科研数据模型。系统宿主是 Obsidian，存储介质是 Markdown 文件 + YAML Properties，因此数据模型必须"落在文件上"，而不是先设计数据库再映射。

本阶段（Phase 0）只做模型设计，不写代码、不建 Vault。

## 1. 唯一交付物

在工作区根目录创建：

`research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md`

允许在同目录附带 schema 示例文件（如 `schemas/*.yaml` 示例）。除此之外不得写任何文件。

## 2. 必须建模的实体

Project、Manuscript、Section、Paragraph、Figure、Panel、Result、Method、Experiment、Reference、Citation、Claim、Asset、RevisionRound、RevisionIssue、Patch、Response。

对每个实体必须给出：
- 语义定义（一句话）与存在理由（为什么不能合并到别的实体）。
- 稳定 ID 方案：格式、生成规则、是否可读、是否可重命名后保持不变。
- 存放位置：独立文件 / 某个 Markdown 的 frontmatter / 内联标记。
- YAML Properties 完整字段表：字段名、类型、是否必填、默认值、约束。
- 生命周期：创建、修改、废弃。

## 3. 必须明确回答的问题

1. **多对多关系**：Figure↔Panel、Claim↔Result、Reference↔Citation、RevisionIssue↔Paragraph 如何在纯文件系统中表达？给出至少两种方案（wikilink 列表 / 中间实体文件 / 双向冗余），并比较一致性维护成本。
2. **文件溯源（provenance）**：每个实体如何指回原始 DOCX 段落 / 原始 PDF 页 / 原始图片文件？给出可验证的锚点方案。
3. **Figure 编号动态解析**：图号在正文中以 `Figure 3`、`Fig. 3`、`图 3` 等形式出现，重排后必须自动更新。给出解析与替换机制，说明 Markdown 中"渲染时解析"与"写入时固化"的取舍。
4. **Panel 坐标**：多面板图（A/B/C 子图）的坐标与裁切信息如何存储？是否需要像素级坐标？坐标在图片替换后如何失效与重标定。
5. **版本兼容**：schema 演进（加字段、改字段、拆实体）时，旧文件如何迁移？给出 `schema_version` 策略与迁移脚本契约。
6. **索引与检索**：不依赖数据库的前提下，如何支持"找出所有引用 Reference X 的 Claim"这类查询？评估 Obsidian 原生搜索、MetadataCache、Bases、外部索引（可选）的成本。
7. **关系完整性校验**：断链、孤儿实体、循环引用如何检测？给出校验规则清单与执行时机（编辑时 / 保存时 / 批量）。

## 4. 硬性约束

- 模型必须"可落地在 Markdown + YAML"上。任何需要数据库或后台服务的部分，必须显式标注为"可选外部组件"。
- 不得修改 `AGENTS.md`、不得碰其他 Worker 目录、不得安装依赖、不得创建真实 Vault 内容。
- 每个设计选择必须给出取舍理由（为什么不选另一个方案），禁止只给结论。
- 与 Obsidian 能力相关的假设必须标注为"待 Worker A 审计确认"，不要假定 API 一定存在。

## 5. 交付文件结构（必须遵守）

```
# Scientific Data Model Proposal
## 1. 设计原则
## 2. 实体总览（一张关系图，用 mermaid）
## 3. 实体定义（逐实体：语义 / ID / 位置 / 字段表 / 生命周期）
## 4. 关系建模（多对多方案对比与选型）
## 5. 文件溯源与锚点
## 6. Figure / Panel 编号与坐标
## 7. Schema 版本与迁移
## 8. 索引与检索策略
## 9. 完整性校验规则
## 10. 与 Obsidian 能力的耦合点（风险清单）
## 11. 未确认事项
```

## 6. 完成标准

- 17 个实体全部有字段表，字段表是表格形式，不得省略。
- 第 4 章给出明确选型，不是"两种都可以"。
- 第 6 章给出编号解析的具体算法（伪代码）。
- 第 9 章给出至少 10 条可执行校验规则。
- 回复中报告：研究范围、核心结论、关键取舍、技术风险、未确认事项、文件清单、最终状态。

## 7. 交付方式

简短总结（≤600 字）+ 文件路径清单。
