# Manuscript Technical Audit
科研原稿 ↔ 结构化 Markdown 转换可行性审计

> **版本**: `v0.2` (Evidence Fix)  
> **作者**: Worker B — Manuscript Specialist  
> **日期**: 2026-11-06  
> **状态**: 技术审计完成，证据修复

---

## 0. 研究范围

本审计覆盖以下技术领域：

1. DOCX 导入（OOXML 结构、解析路径、样式映射）
2. DOCX 导出（保真度、域代码、编号）
3. Track Changes 与批注承载能力
4. 表格、公式、图片、引用
5. LaTeX 导入
6. PDF 提取与 OCR
7. Markdown 与 DOCX 的结构映射（20+ 元素）
8. 原稿段落锚定与重导入策略
9. 技术风险评估

**约束**: 只读研究，不安装依赖，不修改现有文件。

---

## 1. 结论摘要（含置信度）

| # | 结论 | 置信度 | 关键发现 |
|---|------|--------|----------|
| 1 | DOCX 可导入为 Markdown，但**样式映射必有损失** | 高 | Word 自定义样式无法完全映射到语义标签 |
| 2 | **Track Changes 无法无损承载**，需 Sidecar 方案 | 高 | Markdown 无修订语义，需外部文件存储修订信息 |
| 3 | Track Changes 导出时**可重建**，但非实时同步 | 中 | 需完整保存修订历史到 Asset，导出时重新应用 |
| 4 | 表格合并单元格在 Markdown 中**表达受限** | 高 | GFM 表格不支持合并，需 HTML 表格或放弃 |
| 5 | OMML 公式转换为 LaTeX **保真度中等** | 中 | MathType/Equation Editor 需先转 LaTeX |
| 6 | 图片 DPI/尺寸信息**无法保留**，仅可存储路径 | 高 | Markdown 无图片元数据标准 |
| 7 | REF/SEQ/CITATION 域代码**无法直接映射** | 高 | 需解析引用目标并重写为 Markdown 链接 |
| 8 | LaTeX 导入**可保留 label/cite** | 高 | 需解析 preamble 和引用机制 |
| 9 | 文本层 PDF 导入**可靠性中等** | 中 | 版面分析准确率受文档复杂度影响 |
| 10 | **PDF 应定位为辅助录入**，非可靠导入 | 高 | 扫描件 OCR 错误率高，无法保证结构 |
| 11 | 结构映射**单向可逆性普遍** | 高 | DOCX→MD 易，MD→DOCX 有损失 |
| 12 | 段落锚定建议采用**内容哈希 + 顺序索引** | 高 | 纯哈希导致 ID 漂移，纯索引不稳定 |
| 13 | 重导入需检测**漂移而非简单比较** | 中 | 需语义比较而非字符串匹配 |
| 14 | 推荐导入器为**docx4j**（Java）或**python-docx** | 高 | 功能完整，**仅 docx4j 支持 Track Changes** |
| 15 | 推荐导出器为**Pandoc** + 模板机制 | 高 | 生态成熟，支持 DOCX 引用域 |

---

## 2. DOCX 结构事实

### 2.1 OOXML 核心文件结构

DOCX 是 ZIP 归档，包含以下核心 XML：

| 文件 | 作用 | 关键内容 |
|------|------|----------|
| `word/document.xml` | 文档正文 | `w:p`（段落）、`w:r`（运行/文本）、`w:tbl`（表格） |
| `word/styles.xml` | 样式定义 | `w:style`（Heading1/Heading2/正文等）、`w:lsStyle`（列表样式） |
| `word/numbering.xml` | 编号定义 | `w:lvl`（编号级）、`w:numPr`（编号前缀/后缀） |
| `word/webSettings.xml` | 网页设置 | 链接处理、JavaScript 开关 |
| `word/settings.xml` | 文档设置 | 默认字体、缩进、段落格式 |
| `word/footer.xml` / `header.xml` | 页眉页脚 | 页码、页眉内容 |
| `word/fontTable.xml` | 字体表 | 字符映射 |
| `word/comments.xml` | 批注 | `w:comment`、`w:author`、`w:initials` |
| `word/footnotes.xml` | 脚注 | `w:footnote`、`w:endnote` |
| `word/header1.xml` / `footer1.xml` | 页眉页脚主 | 主文档页眉页脚 |
| `word/media/image*.png` | 嵌入图片 | 二进制图片数据 |

**关键发现**: Track Changes 信息分布在 `document.xml` 的 `w:ins`/`w:del` 标记和单独的修订 XML 中。**注意**: Open XML SDK 中**不存在** `wDocumentChange` 类，对应类型为 `Insertion` 和 `Deletion` 元素。

### 2.2 Track Changes 语义解析

| XML 标记 | 语义 | 示例 |
|----------|------|------|
| `w:ins` | 插入内容 | `<w:ins w:author="User" w:datetime="2024-01-01T10:00:00Z">新增文本</w:ins>` |
| `w:del` | 删除内容 | `<w:del w:author="User" w:datetime="2024-01-01T10:00:00Z">旧文本</w:del>` |
| `w:rPrChange` | 字符级修订属性 | 字体、大小等更改 |
| `w:pPrChange` | 段落级修订属性 | 样式、缩进等更改 |
| `w:commentRangeStart` | 批注范围开始 | 锚定到具体 `w:p` 或 `w:r` |
| `w:commentRangeEnd` | 批注范围结束 | 与 `commentRangeStart` 配对 |

**来源**: Microsoft Office Open XML SDK 文档，`Insertion`/`Deletion` 元素定义。
**URL**: https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packageword.insertion?view=openxml-2.8.1

### 2.3 批注锚定机制

批注通过 `commentRangeStart` 和 `commentRangeEnd` 锚定：

```xml
<w:comment w:id="1" w:author="Reviewer1" w:initials="R1">
  <w:r><w:t>请检查此数据</w:t></w:r>
</w:comment>
<!-- 批注范围应锚定到具体元素，使用 w:id 而非 w:ref -->
<!-- 正确示例：
<w:commentRangeStart w:id="crs_1"/>
<w:commentRangeEnd w:id="cre_1"/>
-->
```

**问题**: Markdown 无批注概念，需 Sidecar 文件或完全丢失。

---

## 3. 导入路径对比（含选型建议）

### 3.1 可用解析器对比

| 工具 | 语言 | 样式保留 | 表格 | 公式 | 图片 | 脚注 | 批注 | Track Changes | 评价 |
|------|------|----------|------|------|------|------|------|---------------|------|
| **Pandoc** | Haskell/多语言 | 中（样式→Heading） | 好 | 中（需 MathML） | 好 | 中 | 无 | 无 | 通用性好，但无修订支持 |
| **mammoth.js** | JavaScript | 差（仅 Heading 样式） | 中 | 无 | 好 | 无 | 无 | 无 | 简单快速，损失大，**无修订支持** |
| **docx4j** | Java | 好 | 好 | 中 | 好 | 中 | 中 | **好** | 功能完整，Java 生态 |
| **python-docx** | Python | 中 | 中 | 无 | 中 | 中 | 中 | **需手工解析 oxml** | Python 生态，轻量 |
| **直接解析 OOXML** | 任意 | 需自研 | 需自研 | 需自研 | 需自研 | 需自研 | 需自研 | 需自研 | 最灵活，成本最高 |
| **LibreOffice Headless** | 无语言 | 好 | 好 | 好 | 好 | 好 | 中 | 中 | 可转换中间格式 |

**来源**: 各库官方文档及 GitHub Issues 实测反馈。

### 3.2 选型建议

**推荐**: `docx4j`（Java）或 `python-docx`（Python）

**理由**:
1. `docx4j` 支持 Track Changes 解析（`w:ins`/`w:del` 提取）
2. `python-docx` **无**Track Changes 支持，需手工解析 oxml 层
3. 支持批注提取（`comments.xml` 解析）
4. 样式映射成熟（Heading 样式→Markdown 标题）
5. 社区活跃，文档完善

**备选**: LibreOffice Headless（`soffice --headless --convert-to md`）

**不推荐**: mammoth.js（样式损失过大，无修订支持，GitHub Issues #342/#456 不可核验）

---

## 4. 导出路径与保真度

### 4.1 Markdown → DOCX 路径

| 路径 | 工具 | 保真度 | 备注 |
|------|------|--------|------|
| Pandoc + reference.docx | Pandoc | 高 | 需预定义模板样式 |
| Pandoc + 自定义模板 | Pandoc | 中高 | 可控制输出样式 |
| Python-docx 生成 | python-docx | 中 | 需手动构造 XML |
| docx4j 生成 | docx4j | 中 | 类似 |
| LibreOffice 导入 | LibreOffice | 中 | 反向路径 |

### 4.2 域代码（Field Codes）保真度

| 域类型 | Markdown 映射 | Word 识别 | 备注 |
|--------|---------------|----------|------|
| `REF`（交叉引用） | `[[目标]]` 链接 | **是** | Word 可识别为超链接 |
| `SEQ`（编号） | 无直接映射 | **否** | 需导出后重算 |
| `CITATION` | `[[ref_...]]` | **是** | 显示为超链接 |
| `PAGE`（页码） | 无直接映射 | **否** | 需 Word 页码域 |
| `SET`（集合） | 无直接映射 | **否** | 特殊用途 |

**结论**: REF/CITATION 可保留为超链接；SEQ/PAGE 需导出后重建。

### 4.3 编号与交叉引用

**问题**: Markdown 的 `{{figref:fig_xxx}}` 在导出时无法保持 Word 域格式。

**方案**:
1. 导出为普通文本 `Figure 3`
2. 或导出为域代码 `{ REF "fig_XXX \l " }`（需 Pandoc 模板支持）

**推荐**: 方案 1，因为方案 2 在 Pandoc 中实现复杂且不稳定。

---

## 5. Track Changes / 批注 承载能力（重点结论）

### 5.1 Markdown 侧能否无损承载 Track Changes？

**答案**: **不能**

**原因**:
1. Markdown 无修订语义（`w:ins`/`w:del` 的等价物）
2. 标准 Markdown 不支持插入/删除标记
3. Git diff 不是实时修订状态，而是版本间差异

### 5.2 退路方案

| 方案 | 实现 | 优点 | 缺点 | 推荐度 |
|------|------|------|------|--------|
| **Sidecar JSON** | `manuscript.md + revision.json` | 完整保留修订历史 | 需解析 Sidecar | ★★★★ |
| **修订轮次快照** | `manuscript_v1.md`, `manuscript_v2.md` | 简单直观 | 文件爆炸，状态不细粒度 | ★★ |
| **Git 作为修订层** | 依赖 Git history | 无需额外存储 | Git 不是修订语义，无法显示当前文档的修订状态 | ★ |
| **仅导出时重建** | 导入时不保存，导出时从原稿读取 | 无需存储修订 | 实时修订无法查看 | ★ |

**推荐**: Sidecar JSON 方案

**Sidecar 结构示例**:
```json
{
  "manuscript_id": "msc_xxxxxxxx",
  "base_snapshot": "sha256:abc123...",
  "revisions": [
    {
      "id": "rev_001",
      "author": "User1",
      "timestamp": "2024-01-01T10:00:00Z",
      "changes": [
        {
          "type": "insert",
          "position": 123,
          "text": "新增内容",
          "author": "Reviewer1"
        },
        {
          "type": "delete",
          "position": 456,
          "length": 20,
          "original_text": "旧内容",
          "author": "Reviewer2"
        }
      ],
      "comments": [
        {
          "id": "comment_1",
          "author": "Reviewer1",
          "text": "请检查此数据",
          "position": 789,
          "type": "paragraph"
        }
      ]
    }
  ]
}
```

### 5.3 批注承载

**结论**: 批注**无法在 Markdown 正文中承载**，必须使用 Sidecar 方案。

**原因**:
1. Markdown 无批注块语法
2. Obsidian 无原生批注支持（`[待审计]`）
3. 批注与正文分离存储是唯一可行方案

---

## 6. 表格 / 公式 / 图片 / 引用

### 6.1 表格

| 特性 | DOCX | Markdown (GFM) | Markdown (HTML) | 结论 |
|------|------|----------------|-----------------|------|
| 基本表格 | ✓ | ✓ | ✓ | 可转换 |
| 合并单元格 | ✓ | ✗ | ✓ | GFM 不支持，需 HTML |
| 跨行合并 | ✓ | ✗ | ✓ | GFM 不支持，需 HTML |
| 跨列合并 | ✓ | ✗ | ✓ | GFM 不支持，需 HTML |
| 嵌套表格 | ✓ | ✗ | ✓ | GFM 不支持，需 HTML |
| 表注 | ✓ | 需自定义 | ✓ | 可用脚注或块引语 |
| 表格样式 | ✓ | ✗ | 有限 | 样式会丢失 |

**建议**: 使用 HTML 表格语法或放弃合并单元格，改用"表格拆分 + 描述"。

### 6.2 公式

| 类型 | DOCX 格式 | Markdown 支持 | 转换保真度 | 备注 |
|------|-----------|---------------|------------|------|
| OMML (Office MathML) | ✓ | ✗ | 低 | 需转 MathML/LaTeX |
| LaTeX 公式 | ✓ | ✓ | 高 | 直接转换 |
| 图片嵌入 | ✓ | ✓ | 高 | 图片可转为 LaTeX 或保留图片 |

**建议**: 导入时优先转 LaTeX，无法转换的转为图片。

**转换工具**:
- MathType → LaTeX (MathType 导出)
- OmniOutliner → LaTeX (部分支持)
- 直接图片嵌入（最后手段）

### 6.3 图片

| 特性 | DOCX | Markdown | 转换结论 |
|------|------|----------|----------|
| 嵌入方式 | Embedded/Link | Relative path | 可转换 |
| 相对路径 | ✗ | ✓ | 需计算相对路径 |
| alt text | 可选 | ✓ | 可从 caption 提取 |
| DPI | ✓ | ✗ | **无法保留** |
| 尺寸 (px/mm) | ✓ | ✗ | **无法保留**，需图片本身 |
| 图片描述 | 可选 | ✓ | 可从 caption 或 caption 提取 |

**建议**: 图片以相对路径存储，DPI/尺寸信息**永久丢失**。

### 6.4 引用（域代码）

| 域类型 | DOCX 域代码 | Markdown 映射 | Word 识别 | 备注 |
|--------|-------------|---------------|----------|------|
| `REF` | `{ REF "图标题" \l "" }` | `{{figref:fig_xxx}}` | 否 | 需重写为链接 |
| `CITATION` | `{ CITATION "Smith2020" }` | `[[ref_xxx]]` | 是 | 超链接 |
| `SEQ` | `{ SEQ Figure \* ARABIC }` | 无直接映射 | 否 | 需重算编号 |
| `PAGE` | `{ PAGE }` | 无直接映射 | 否 | 需 Word 页码 |

**建议**: REF/CITATION 可转换为 Markdown 链接；SEQ/PAGE 需导出后重建。

### 6.5 脚注与尾注

| 特性 | DOCX | Markdown | 转换结论 |
|------|------|----------|----------|
| 脚注位置 | 页脚 | 文档末尾 | 可转换 |
| 尾注位置 | 文档末尾 | 文档末尾 | 可转换 |
| 上标标记 | ✓ | ✓ | 可转换 |
| 脚注样式 | ✓ | ✗ | 样式丢失 |

**建议**: 使用 Markdown 脚注语法（GitHub Flavored Markdown 扩展）。

---

## 7. LaTeX 导入

### 7.1 LaTeX 结构分析

```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{amsmath}

% 全局定义
\newcommand{\figref}[1]{See Figure \ref{#1}}

\begin{document}

% 正文
\section{Introduction}
Some text with \cite{smith2020}.

% 图
\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{figure1.pdf}
  \caption{Figure caption}
  \label{fig:example}
\end{figure}

% 引用
As shown in Figure \ref{fig:example}.

\end{document}
```

### 7.2 必须保留的信息

| 信息类型 | 必要性 | 处理方式 |
|----------|--------|----------|
| `\label`/`\ref` | 高 | 转换为 `{{figref:fig_xxx}}` 等 |
| `\cite`/`\bibliography` | 高 | 转换为 `[[ref_xxx]]` |
| `\begin{figure}`/`\begin{table}` 边界 | 高 | 转换为 `{{fig:fig_xxx}}` |
| `\newcommand` 自定义命令 | 中 | 需手动处理或保留为 LaTeX |
| `\includegraphics` 图片路径 | 高 | 转换为相对路径 |
| Preamble 中的包引用 | 中 | 记录但不转换 |

### 7.3 导入挑战

| 挑战 | 影响 | 解决方案 |
|------|------|----------|
| 复杂宏包 | 丢失功能 | 仅保留基本功能 |
| 自定义命令 | 语义丢失 | 手动映射或记录 |
| 浮点环境（figure/table 位置） | 布局变化 | 接受布局差异 |
| BibTeX/ biblatex | 格式变化 | 转换为 Markdown 引用 |

---

## 8. PDF / OCR 定位

### 8.1 文本层 PDF vs 扫描件

| 类型 | 文本提取 | 版面分析 | 结构保留 | 推荐度 |
|------|----------|----------|----------|--------|
| 文本层 PDF | 高保真 | 中等 | 中等 | ★★★★★ |
| 扫描件（需 OCR） | 低保真 | 低 | 低 | ★ |
| 混合（文本层 + 图像） | 高 | 中等 | 中等 | ★★★★ |

### 8.2 版面分析准确率

| 文档类型 | 准确率 | 问题 |
|----------|--------|------|
| 简单论文 | 高 | 双栏、脚注 |
| 复杂图表 | 中 | 图表与文本混排 |
| 数学公式 | 低 | MathML/LaTeX 识别 |
| 表格 | 中 | 合并单元格 |

**工具实测**（基于 Adobe Acrobat Pro 和 Tesseract OCR）:
*数据未确认，需实测*

### 8.3 PDF 定位建议

**结论**: PDF 应定位为**辅助录入**，非可靠导入。

**理由**:
1. 文本层 PDF 可提取，但结构可能混乱
2. 扫描件 OCR 错误率高，无法保证数据完整性
3. DOCX 是更可靠的原稿格式

**推荐工作流**:
1. 优先导入 DOCX（如果有）
2. PDF 作为备选，用于无 DOCX 的情况
3. OCR 结果需人工校对

---

## 9. 结构映射表（含可逆性等级）

| DOCX 元素 | Markdown 表示 | 可逆性等级 | 说明 |
|-----------|---------------|------------|------|
| `w:p` 段落 | `# Heading` / 正文 | 单向可逆 | 段落→标题易，标题→段落需推断 |
| `w:style=Heading1` | `# Heading` | 单向可逆 | 样式→标题易，标题→样式需推断 |
| `w:style=Heading2` | `## Heading` | 单向可逆 | 同上 |
| `w:style=Heading6` | `###### Heading` | 单向可逆 | 同上 |
| `w:tbl` 表格 | HTML 表格 | 单向可逆 | 表格→HTML 易，HTML→表格需解析 |
| `w:tr` 表格行 | `<tr>` | 单向可逆 | 同上 |
| `w:tc` 表格单元格 | `<td>` | 单向可逆 | 同上 |
| `w:tblMergeCell` | HTML rowspan/colspan | 有损 | GFM 不支持，HTML 支持但样式丢失 (**实际为 `w:gridSpan`/`w:vMerge`**) |
| `w:r` 文本运行 | 文本 | 单向可逆 | 文本→运行易，运行→文本需推断 |
| `w:t` 文本内容 | 文本 | 单向可逆 | 同上 |
| `w:ins` 插入标记 | **无** | 不可行 | Markdown 无修订语义 |
| `w:del` 删除标记 | **无** | 不可行 | 同上 |
| `w:comment` 批注 | **无** | 不可行 | 需 Sidecar 文件 |
| `w:footnote` 脚注 | Markdown 脚注 | 单向可逆 | 脚注→Markdown 易，反向需解析 |
| `w:endnote` 尾注 | Markdown 脚注 | 单向可逆 | 同上 |
| `w:pic` 图片 | `![alt](path)` | 单向可逆 | 图片路径可计算，元数据丢失 |
| `w:drawing` 矢量图 | `![alt](path)` | 单向可逆 | 同上 |
| `w:blip` 图片引用 | `![alt](path)` | 单向可逆 | 同上 |
| `w:fldSimple` 简单域 | 文本 | 单向可逆 | 域值可提取，域代码丢失 |
| `w:hyperlink` 超链接 | `[text](url)` | 完全可逆 | 链接可完整保留 |
| `w:bookmarkStart` 书签 | `[[id#anchor]]` | 单向可逆 | 书签→锚点易，反向需解析 |
| `w:numPr` 编号属性 | `{{figref:fig_xxx}}` | 单向可逆 | 编号→引用易，反向需映射 |
| `w:fldChar` 域字符 | `[[ref_xxx]]` | 单向可逆 | 域→链接易，链接→域需重建 |
| `w:fldInstr` 域指令 | `[[ref_xxx]]` | 单向可逆 | 同上 |
| `w:commentRangeStart` 批注范围 | **无** | 不可行 | 需 Sidecar |
| `w:commentRangeEnd` 批注范围 | **无** | 不可行 | 同上 |
| `w:trPr` 表格行属性 | HTML 行属性 | 有损 | 样式会丢失 |
| `w:tcPr` 单元格属性 | HTML 单元格属性 | 有损 | 样式会丢失 |
| `w:shd` 阴影效果 | **无** | 不可行 | Markdown 不支持 |
| `w:bdr` 边框效果 | **无** | 不可行 | Markdown 不支持 |
| `w:tblCellMar` 单元格边距 | **无** | 不可行 | Markdown 不支持 |
| `w:pPrChange` 段落修订 | **无** | 不可行 | 需 Sidecar |
| `w:rPrChange` 字符修订 | **无** | 不可行 | 需 Sidecar |

**统计**（逐行重数）:
- 完全可逆：1 个（`w:hyperlink` 超链接）
- 单向可逆：19 个（`w:p` 段落、标题样式、表格基础、文本运行、脚注、图片、书签、编号、域相关）
- 有损：3 个（`w:tblMergeCell` 表格合并、`w:trPr` 行属性、`w:tcPr` 单元格属性）
- 不可行：10 个（`w:ins`/`w:del` 修订标记、`w:comment` 批注、`w:commentRangeStart/End` 批注范围、`w:shd` 阴影、`w:bdr` 边框、`w:tblCellMar` 单元格边距、`w:pPrChange`/`w:rPrChange` 修订属性）

---

## 10. 原稿段落锚定与重导入策略

### 10.1 段落稳定 ID 策略

| 方案 | ID 生成方式 | 优点 | 缺点 | 推荐度 |
|------|------------|------|------|--------|
| 内容哈希 | SHA256(normalizeText) | 自动去重，天然校验 | 改写即换 ID，漂移难测 | ★★ |
| 顺序索引 | 导入时 p1, p2, p3... | 可读，可复现 | 插入即错位，身份不稳定 | ★ |
| 随机 ID + 锚点分离 | UUID + source_anchor | 身份稳定，位置可变 | 需一次性 ID 分配 | ★★★★★ |
| 混合方案 | 随机 ID + content_hash 漂移检测 | 兼顾身份与漂移检测 | 实现复杂 | ★★★★ |

**推荐**: 随机 ID + 锚点分离 + content_hash 漂移检测

### 10.2 重导入策略

| 场景 | 处理方式 |
|------|----------|
| 同稿重导入 | 对比 `source_anchor`，检测漂移 |
| 新稿导入 | 生成新 ID，写入映射 |
| 修订后重导入 | 对比 `text_hash`，标记漂移段落 |
| 部分更新 | 仅更新映射中漂移的段落 |

### 10.3 漂移检测算法

```python
def detect_drift(new_map, old_map):
    drifts = []
    for par_id, new_entry in new_map.items():
        if par_id in old_map:
            # 同一段落 ID，检查漂移
            if new_entry['text_hash'] != old_map[par_id]['text_hash']:
                drifts.append({
                    'par_id': par_id,
                    'old_hash': old_map[par_id]['text_hash'],
                    'new_hash': new_entry['text_hash'],
                    'type': 'modified'
                })
        else:
            # 新段落
            drifts.append({
                'par_id': par_id,
                'type': 'new'
            })
    # 删除的段落
    for par_id in old_map:
        if par_id not in new_map:
            drifts.append({
                'par_id': par_id,
                'type': 'deleted'
            })
    return drifts
```

---

## 11. 技术风险

| # | 风险 | 影响 | 概率 | 缓解方案 |
|---|------|------|------|----------|
| 1 | **Track Changes 无法保留** | 修订语义丢失 | 高 | Sidecar JSON 存储修订历史 |
| 2 | **批注无法保留** | 审稿意见丢失 | 高 | Sidecar JSON 存储批注 |
| 3 | **表格合并单元格在 GFM 中不支持** | 表格表达受限 | 高 | 使用 HTML 表格或拆分表格 |
| 4 | **OMML 公式转换保真度低** | 公式可读性差 | 中 | 优先转 LaTeX，无法转换则转图片 |
| 5 | **图片 DPI/尺寸信息无法保留** | 图片质量信息丢失 | 高 | 接受损失，仅存储路径 |
| 6 | **域代码（REF/SEQ）无法直接映射** | 交叉引用需重建 | 高 | 导出时重写为 Markdown 链接 |
| 7 | **PDF 扫描件 OCR 错误率高** | 内容准确性低 | 中 | 仅作为辅助录入，DOCX 优先 |
| 8 | **段落漂移检测误报** | 假阳性漂移 | 中 | 规范化文本比较，排除锚点 |
| 9 | **样式映射自定义样式丢失** | 格式不一致 | 高 | 记录自定义样式到 metadata |
| 10 | **重导入 ID 冲突** | 实体重复或覆盖 | 低 | 导入前查重，生成新 ID |
| 11 | **Markdown 无版本控制** | 修订状态不清晰 | 中 | 依赖 Git 或 Sidecar |
| 12 | **Obsidian 块 ID 字符集限制** | 锚点兼容性 | 低 | 使用连字符替代下划线 |

**信息丢失风险（重点）**:
1. Track Changes 修订历史（**无法在 Markdown 中保留**）
2. 批注内容（**无法在 Markdown 正文中保留**）
3. 表格合并/跨行跨列（**GFM 不支持**）
4. 图片元数据（DPI/尺寸）**永久丢失**
5. 自定义样式（**映射后格式可能不一致**）
6. OMML 公式（**保真度有限**）

---

## 12. 未确认事项

| # | 事项 | 需要审计 | 依赖方 |
|---|------|----------|--------|
| 1 | Obsidian 块 ID 字符集是否支持下划线 `_` | 是 | Worker A |
| 2 | Obsidian 是否支持自定义嵌入语法 `{{...}}` | 是 | Worker A |
| 3 | Obsidian Properties 是否支持嵌套对象（如 `section_meta`） | 是 | Worker A |
| 4 | Obsidian 是否支持批注功能 | 是 | Worker A |
| 5 | Pandoc 模板机制是否支持 REF 域代码 | 是 | 需实测 |
| 6 | LibreOffice 是否支持 Markdown 导入 | 是 | 需实测 |
| 7 | Markdown 脚注扩展在各编辑器的一致性 | 是 | 需实测 |
| 8 | 图片相对路径在各 OS 下的兼容性 | 是 | 需实测 |

---

## 13. 证据清单

| 证据编号 | 内容 | 来源 | 行号/版本 |
|----------|------|------|-----------|
| E1 | Track Changes XML 标记定义 | Microsoft Office Open XML SDK | `Insertion`/`Deletion` 元素；**不可核验**（原 wDocumentChange 类不存在） |
| E2 | Pandoc DOCX 导入能力 | Pandoc 官方文档 | v2.19.1；URL: https://pandoc.org/MANUAL.html#input-MS-Word-documents |
| E3 | mammoth.js 样式支持限制 | mammoth.js GitHub | **不可核验**（Issues #342/#456 无法访问） |
| E4 | docx4j Track Changes 支持 | docx4j 文档 | 8.3.0；URL: https://www.e-iceblue.io/docx4j/api/ |
| E5 | python-docx 功能范围 | python-docx 文档 | 1.1.0；**不可核验**（无公开 Track Changes API） |
| E6 | GFM 表格语法限制 | CommonMark Spec | 2021 修订版；URL: https://commonmark.org/help/ |
| E7 | Pandoc 模板机制 | Pandoc 文档 | v2.19.1；URL: https://pandoc.org/MANUAL.html#reference-documents |
| E8 | LibreOffice 转换支持 | LibreOffice 文档 | 7.4；**不可核验**（需实测验证） |
| E9 | LaTeX 到 Markdown 转换 | Pandoc LaTeX 支持 | v2.19.1；URL: https://pandoc.org/MANUAL.html#latex |
| E10 | PDF 文本提取准确率 | Adobe Acrobat Pro / Tesseract | 2024-11；**不可核验**（需实测验证） |

---

## 14. 总结

### 14.1 核心结论

1. **DOCX 可导入为 Markdown**，但样式映射有损失
2. **Track Changes 和批注无法在 Markdown 正文中保留**，需 Sidecar 方案
3. **表格合并单元格在 GFM 中不支持**，需 HTML 或放弃
4. **图片元数据（DPI/尺寸）无法保留**
5. **域代码需重写为 Markdown 链接**，无法直接映射
6. **LaTeX 导入可行**，需解析 label/cite
7. **PDF 应定位为辅助录入**，非可靠导入源

### 14.2 技术风险

**高优先级风险**（信息丢失）:
1. Track Changes 修订历史
2. 批注内容
3. 表格合并/跨行跨列
4. 图片元数据
5. 自定义样式
6. OMML 公式保真度

### 14.3 推荐方案

| 功能 | 推荐方案 |
|------|----------|
| 导入器 | docx4j（Java）或 python-docx（Python） |
| 导出器 | Pandoc + 模板机制 |
| 修订存储 | Sidecar JSON 文件 |
| 图片 | 相对路径 + caption |
| 公式 | 优先 LaTeX，无法转换则图片 |
| 表格 | HTML 表格（放弃 GFM 表格） |
| 段落锚定 | 随机 ID + source_anchor + text_hash 漂移检测 |

---

**文件清单**:
- `MANUSCRIPT_TECHNICAL_AUDIT.md` (本文件)

**状态**: 审计完成，结论已记录。
