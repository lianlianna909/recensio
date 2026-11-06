# TASK: Worker B - Manuscript Specialist

## 0. 角色与项目背景

你是 ScientificWritingProject 的 Manuscript Specialist，负责"科研原稿 ↔ 结构化 Markdown"之间的转换可行性审计。项目要把作者已有的 Word 原稿导入成可结构化编辑的 Markdown，并支持导出回 DOCX，同时保留修订与批注语义。

本阶段（Phase 0）只做技术审计，不写产品代码、不安装依赖。

## 1. 唯一交付物

在工作区根目录创建：

`research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md`

允许在同目录附带少量辅助材料。除此之外不得写任何文件。

## 2. 研究范围（必须逐项覆盖）

1. **DOCX 导入**
   - DOCX 的 OOXML 结构（`word/document.xml`、`styles.xml`、`numbering.xml`、`footnotes.xml`、`comments.xml`、`settings.xml`）。
   - 可用的解析路径对比：Pandoc、mammoth.js、docx4j / python-docx、直接解析 OOXML。各自在"样式保留 / 表格 / 公式 / 图片 / 脚注 / 批注"上的能力与损失。
   - 样式映射策略：Word 的 Heading 样式 → Markdown 标题；自定义样式 → 语义标签的可行性与失败模式。
2. **DOCX 导出**
   - Markdown → DOCX 的可行路径（Pandoc reference.docx 模板机制、docx 生成库）。
   - 编号、交叉引用、图表题注、参考文献域（field code）能否在导出后仍被 Word 识别为"域"。
3. **Word Track Changes 与批注**
   - `w:ins` / `w:del` / `w:rPrChange` / `w:pPrChange` 的语义。
   - `comments.xml` + `commentRangeStart/End` 的锚定方式。
   - 明确回答：**Markdown 侧能否无损承载 Track Changes？** 如果不能，退路是什么（sidecar 文件 / 修订轮次快照 / 仅导出时重建）。
4. **表格、公式、图片、引用**
   - 合并单元格、嵌套表格、表注在 Markdown 中的表达损失。
   - OMML（Word 公式）与 LaTeX 的双向转换现状与保真度。
   - 图片：嵌入方式、相对路径、`alt text`、DPI/尺寸信息保留。
   - 域代码引用（`REF`、`SEQ`、`CITATION`）与 Markdown 链接/引用的映射。
5. **LaTeX 导入**
   - `.tex` 结构（preamble、\section、\begin{figure}、\label/\ref、\cite、bib）。
   - 导入时哪些信息必须保留（label、cite key、figure 环境边界）。
6. **PDF 提取与 OCR**
   - 文本层 PDF vs 扫描件；版面分析（双栏、脚注、图表混排）的现实准确率。
   - 明确结论：PDF 路径应定位为"辅助录入"还是"可靠导入"。
7. **Markdown 与 DOCX 的结构映射**
   - 给出映射表：DOCX 元素 → Markdown 表示 → 是否可逆。
   - 标注每一行的可逆性等级：完全可逆 / 单向可逆 / 有损 / 不可行。
8. **原稿段落与结构化数据的映射策略**
   - 段落稳定 ID 如何与原始 DOCX 段落对应（原文锚点、内容哈希、顺序索引的取舍）。
   - 重新导入同一稿件时如何避免重复建实体、如何检测漂移。

## 3. 硬性约束

- 只做只读研究。不得修改 `AGENTS.md`、不得碰其他 Worker 目录、不得安装依赖、不得写产品代码。
- 每条关键结论必须有证据：官方文档、源码文件与行号、或实测（若实测，写清版本与命令）。
- **禁止做出不可实现的承诺**。凡"可以无损转换"的说法必须给出机制说明；做不到就明确写"有损"。
- 必须显式讨论"导入失败"与"信息丢失"的场景，这是本项目的核心风险。

## 4. 交付文件结构（必须遵守）

```
# Manuscript Technical Audit
## 1. 结论摘要（≤15 条，每条含置信度）
## 2. DOCX 结构事实
## 3. 导入路径对比（含选型建议）
## 4. 导出路径与保真度
## 5. Track Changes / 批注 承载能力（重点结论）
## 6. 表格 / 公式 / 图片 / 引用
## 7. LaTeX 导入
## 8. PDF / OCR 定位
## 9. 结构映射表（含可逆性等级）
## 10. 原稿段落锚定与重导入策略
## 11. 技术风险
## 12. 未确认事项
## 13. 证据清单
```

## 5. 完成标准

- 第 9 章映射表至少覆盖 20 个 DOCX 元素，每行都有可逆性等级。
- 第 5 章给出明确的"能/不能/部分能"结论与替代方案。
- 至少列出 6 条技术风险，其中至少 2 条关于"信息丢失"。
- 回复中报告：研究范围、核心结论、证据来源、技术风险、未确认事项、文件清单、最终状态。

## 6. 交付方式

简短总结（≤600 字）+ 文件路径清单，不要粘贴全文。
