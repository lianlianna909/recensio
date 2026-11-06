# TASK: Worker A - Obsidian Architect

## 0. 角色与项目背景

你是 ScientificWritingProject 的 Obsidian Architect。项目目标是在 Obsidian 之上构建一套"科学写作系统"（Scientific Writing System）：把科研原稿（DOCX / LaTeX / PDF）导入为结构化 Markdown，用 YAML Properties 承载可查询的科研元数据，并在 Obsidian 内完成 Figure/Panel 编号、引用管理、修订轮次与审稿意见追踪。

本阶段（Phase 0）只做技术审计与设计，不写产品代码。

## 1. 唯一交付物

在工作区根目录创建：

`research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md`

允许在该目录下附带少量辅助文件（如 `evidence/` 下的 API 类型定义摘录）。除此之外不得写任何文件。

## 2. 研究范围（必须逐项覆盖）

1. **官方 Plugin API 现状**
   - 当前 Obsidian 插件 API 版本（manifest 的 `minAppVersion` 现状、API changelog 最近若干版本的关键变化）。
   - 从 `obsidian-api` 官方 TypeScript 定义（obsidianmd/obsidian-api 仓库的 `obsidian.d.ts`）核实每个你要用到的类/方法是否真实存在、签名如何。
   - 明确区分：稳定公开 API / 未文档化但类型里存在 / 完全不可用（需要私有 hack）。
2. **Vault 与 Markdown Properties 设计**
   - Properties（frontmatter）的类型系统：支持的 YAML 类型、Obsidian 对列表/链接/日期的解析行为。
   - frontmatter 中 wikilink 与 list 的写法在 Dataview / Bases / 原生搜索中的可见性差异。
   - 大规模 vault（>10k notes）下 frontmatter 的解析与索引开销。
3. **MetadataCache**
   - `app.metadataCache` 能拿到什么（headings、links、embeddings、listItems、frontmatter、sections），拿不到什么。
   - 增量更新语义、`resolved` 事件、缓存失效时机；插件读取缓存时的常见竞态。
4. **Workspace / Views / Commands**
   - 自定义 View（ItemView）的能力边界：能否嵌入编辑器、能否渲染任意 HTML/Canvas。
   - 与 Markdown 编辑器（CodeMirror 6）扩展的集成方式与稳定性风险。
5. **Bases 能力评估（重点）**
   - Bases 当前是什么、能查询什么、与 Dataview 的差异。
   - 是否支持：按 frontmatter 过滤/排序/分组、展示关系型数据、自定义列渲染、跨文件聚合。
   - 明确回答：Bases 能否承担"Figure/Panel/Reference 的结构化数据展示"，还是必须自建 View。
6. **插件与第三方依赖边界**
   - 插件打包约束（单文件 main.js、无 node_modules 运行时、移动端限制）。
   - 哪些依赖可用（纯 JS、无 native binding），哪些不可用（Node fs / child_process / native addon / worker）。
   - 外部进程调用（如调用 Python 做 DOCX 解析）在桌面端与移动端的可行性差异。
7. **推荐系统模块划分**
   - 给出 Obsidian 侧应承担的职责与不应承担的职责，明确"宿主边界"。

## 3. 硬性约束

- 只做只读研究。**不得**修改 `AGENTS.md`、不得修改任何其他 Worker 的目录、不得修改项目级规范、不得安装依赖、不得写产品代码。
- 每条关键结论必须给出证据：官方文档 URL，或 `obsidian.d.ts` 的具体类型/方法名与签名，或官方 changelog 版本号。没有证据的判断必须标为「推测」。
- 禁止夸大 Obsidian 原生能力。凡属"社区插件能做"而非"官方 API 支持"的，必须显式标注。
- 不确定的地方写进"未确认事项"，不要用模糊措辞掩盖。

## 4. 交付文件结构（必须遵守）

```
# Obsidian Technical Audit
## 1. 结论摘要（不超过 15 条，每条一句话 + 置信度 高/中/低）
## 2. API 与版本事实
## 3. Vault / Properties / MetadataCache
## 4. Views / Commands / 编辑器集成
## 5. Bases 能力边界
## 6. 依赖与运行时约束
## 7. 系统模块划分建议（Obsidian 侧职责 / 非 Obsidian 侧职责）
## 8. 技术风险
## 9. 未确认事项
## 10. 证据清单（URL + 类型定义摘录）
```

## 5. 完成标准（Definition of Done）

- 上述 10 个章节齐全且非空。
- "结论摘要"中每条都可在正文找到对应证据。
- "Bases 能力边界"给出明确的可/不可结论，而不是"视情况而定"。
- 明确列出至少 5 条技术风险。
- 在回复中报告：研究范围、核心结论、证据来源、技术风险、未确认事项、文件清单、最终状态。

## 6. 交付方式

文件写完后，用一段简短总结回复（不超过 600 字）+ 文件路径清单。不要粘贴整篇报告。
