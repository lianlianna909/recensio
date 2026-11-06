# TASK: 修订轮 — 跨审计确认记录

## 0. 背景

数据模型提案（§11.1 U1–U5）与 Manuscript 报告（§12）都向 Obsidian 审计提出了若干必须确认的问题，但 Phase 0 的 Obsidian 报告未逐项回应，导致块锚点语法至今悬空。QA 将此列为遗漏项。

你的任务：**只做这 6 项的定向确认**，不重做审计。

## 1. 交付物

`research/obsidian/CROSS_CONFIRMATION.md`

## 2. 必须回答的 6 项

每项给出：**是 / 否 / 部分** + 证据（`obsidian.d.ts` 行号或官方文档 URL）+ 对数据模型的影响 + 若不成立时的退路。

| # | 问题 |
|---|---|
| C1 | 块 ID（`^par_9QK2M4XZ`）的**合法字符集**是什么？下划线是否允许？大小写敏感吗？ |
| C2 | 块 ID 能否挂在**标题行**上（`## Introduction ^sec_4M2P8QKT`）？挂上后能否被 `[[#^id]]` 引用？ |
| C3 | `CachedMetadata.blocks` 是否返回文件中**全部**块 ID（含标题上的）？块 ID 有无长度或数量限制？ |
| C4 | Obsidian 是否会**改写正文中的 fenced code block**（如 ```yaml swp:citation```）？这是 D-04 裁决（结构化子对象放正文 YAML 块）成立的前提，必须有证据或明确标为未验证。 |
| C5 | 自定义语法 `{{figref:fig_XXXX}}` 能否被 Markdown post-processor 安全处理？是否与 Obsidian 原生语法（`{{...}}`、嵌入、模板变量）冲突？ |
| C6 | Obsidian 是否有**原生批注**能力（非插件）？若无，插件能否在编辑器内做行内批注 UI？ |

## 3. 不在范围内

- Pandoc REF 域支持 → 属 Manuscript / Phase 1 实测，不在本任务
- 重新审计 Bases、MetadataCache、Properties 整体能力 → 已有结论，不重复

## 4. 硬性约束

- 只写 `research/obsidian/CROSS_CONFIRMATION.md`。不得修改 `OBSIDIAN_TECHNICAL_AUDIT.md`，不得碰其他目录。
- 证据标准与 Phase 0 审计一致：类型定义给行号，文档给 URL。
- 无法确认的，写「未能确认」并说明尝试方式。**禁止用推测填空。**

## 5. 完成标准

- 6 项全部有判定，无一项留空
- 每项都有「对数据模型的影响」一句话
- C4 必须给出明确结论或明确标注未验证（这是 D-04 的存亡前提）

## 6. 交付方式

≤500 字总结 + 6 项判定表（一行一项）。
