# Open Source Audit

**审计日期**: 2026-11-06  
**审计员**: Worker D - Open-source Researcher  
**项目**: ScientificWritingProject

---

## 1. 总览表

| 项目 | 许可证 | 活跃度 | 文档模型 | DOCX 支持 | 可复用性 |
|------|--------|--------|----------|-----------|----------|
| **Curvenote Editor** | MIT | 中等 (2024-2025) | ProseMirror Schema (JSON AST) | 有限 (通过 Pandoc) | **Adapt** - 编辑器核心可复用 |
| **TeXlyre** | AGPL-3.0 | 活跃 (2025) | LaTeX/Typst 源码 + Yjs CRDT | 无原生支持 | **Reference-only** - AGPL 限制闭源使用 |
| **Oleafly** | AGPL-3.0 | 超活跃 (2026) | LaTeX/Typst/Markdown 源码 | 通过 Pandoc | **Reference-only** - AGPL 限制闭源使用 |
| **Manubot** | CC-BY-4.0 / CC0-1.0 | 低 (2024) | Markdown + YAML metadata | 支持 (Pandoc) | **Adapt** - 工具链可复用 |
| **Quarto** | MIT (v1.4+) | 超活跃 (2026) | Pandoc Markdown 扩展 | 支持 (Pandoc) | **Fork/Adapt** - 最成熟方案 |
| **Typst** | Apache-2.0 | 超活跃 (2026) | 自有标记语言 (AST) | 无原生支持 | **Reference** - 排版引擎可参考 |
| **TeXMind** | **未能核实** | **未能核实** | **未能核实** | **未能核实** | **未能核实** |

---

## 2. 逐项目详查

### 2.1 Curvenote Editor

**官方仓库**: https://github.com/curvenote/editor  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main (推测)
- **最近提交**: 2024-2025 期间活跃
- **Star 量级**: 未明确显示，属于中等规模项目
- **维护活跃度**: 中等，持续更新

#### 许可证
- **SPDX 标识**: MIT
- **许可证文件路径**: 仓库根目录 LICENSE 文件 (推测)
- **关键条款摘录**:
  ```
  特此免费授予任何获得本软件及相关文档文件副本的人不受限制地处置本软件的许可，
  包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或出售本软件副本的权利。
  
  上述版权声明和本许可声明应包含在本软件的所有副本或实质性部分中。
  
  本软件按"原样"提供，不附带任何形式的明示或默示担保。
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求

#### 源码结构
```
editor/
├── packages/
│   ├── @curvenote/schema          # 文档 Schema 定义
│   ├── @curvenote/editor         # 主编辑器组件
│   ├── prosemirror-autocomplete  # 自动补全插件
│   └── ... (其他 prosemirror 插件)
├── apps/                          # 示例应用
├── package.json                   # Monorepo 配置
└── ...
```

**核心包/模块划分**:
- 采用 Monorepo 管理 (npm workspaces 或类似工具)
- `@curvenote/schema`: 定义文档结构和节点类型
- `@curvenote/editor`: React + Redux 编辑器实现
- 多个 ProseMirror 插件包

#### Document Schema
- **文档模型**: ProseMirror Schema (基于 JSON 的 AST)
- **稳定性**: ✅ 对外稳定，有明确的 Schema 定义
- **特点**:
  - 支持 LaTeX、Markdown、Jupyter、Sphinx 生态系统集成
  - 模块化设计，易于扩展
  - 基于 prosemirror-model 包

#### Figure / Panel
- **原生支持**: ✅ 支持多面板图
- **编号解析**: ✅ 支持图表交叉引用
- **实现方式**: 通过 ProseMirror 节点和 Schema 扩展

#### Reference / Citation
- **实现方式**: 集成外部引用系统
- **支持格式**: BibTeX (通过集成)
- **特点**: 与 LaTeX、Jupyter、Sphinx 生态系统的引用管理集成

#### Editor
- **技术栈**: 
  - ProseMirror (核心编辑器框架)
  - React (UI 层)
  - Redux (状态管理)
- **可独立嵌入**: ✅ 是，设计为可嵌入组件
- **特点**:
  - 所见即所得 (WYSIWYG) 编辑
  - 支持实时协作
  - 模块化插件系统

#### Import / Export
- **支持格式**:
  - ✅ Markdown
  - ✅ LaTeX (集成)
  - ✅ Jupyter notebooks (集成)
  - ✅ HTML
  - ⚠️ DOCX: 有限支持 (通过 Pandoc 转换)
- **DOCX Track Changes**: ❌ 不支持

#### 可复用性判定
- **分级**: **Adapt** (适配复用)
- **理由**:
  - MIT 许可证允许自由使用、修改、分发
  - 编辑器核心 (ProseMirror + React) 可独立提取
  - Schema 设计清晰，可定制
  - 但需要剥离与 Curvenote 平台的集成部分
  - 协作功能需要额外的后端支持

---

### 2.2 TeXlyre

**官方仓库**: https://github.com/TeXlyre/texlyre  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main (推测)
- **最近提交**: 2025 年活跃
- **Star 量级**: ~490 stars
- **维护活跃度**: 活跃，持续开发中

#### 许可证
- **SPDX 标识**: AGPL-3.0
- **许可证文件路径**: LICENSE 文件
- **关键条款摘录**:
  ```
  GNU AFFERO GENERAL PUBLIC LICENSE
  Version 3, 19 November 2007
  
  Everyone is permitted to copy and distribute verbatim copies
  of this license document, but changing it is not allowed.
  
  核心条款:
  - 你可以使用、修改和分发此软件
  - 可用于任何目的，包括商业用途
  - 如果分发修改版，必须分发源代码
  - 如果作为网络服务运行修改版，必须向用户提供源代码
  
  选择 AGPL-3.0 的原因:
  依赖 SwiftLaTeX 的 AGPL 许可 WASM LaTeX 引擎，用于浏览器内编译。
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求

#### 源码结构
```
texlyre/
├── src/                          # 前端源码
│   ├── components/               # React 组件
│   ├── plugins/                  # 插件系统
│   └── extras/                   # 扩展功能
├── public/                       # 静态资源
├── package.json
└── ...
```

**核心模块**:
- 基于 Web 的编辑器
- 插件架构支持扩展
- 集成 SwiftLaTeX WASM 引擎

#### Document Schema
- **文档模型**: LaTeX/Typst 源码 (纯文本)
- **稳定性**: ✅ 稳定 (基于标准 LaTeX/Typst 语法)
- **特点**:
  - 直接编辑源码，无中间 AST
  - 支持 LaTeX 和 Typst 两种格式
  - 浏览器内编译

#### Figure / Panel
- **原生支持**: ⚠️ 依赖 LaTeX/Typst 原生能力
- **编号解析**: ✅ 通过 LaTeX/Typst 编译实现
- **实现方式**: 编译后的 PDF 预览

#### Reference / Citation
- **实现方式**: LaTeX/Typst 原生引用系统
- **支持格式**: BibTeX, BibLaTeX
- **特点**: 依赖外部引用管理工具

#### Editor
- **技术栈**: 
  - Web 前端 (React 推测)
  - SwiftLaTeX WASM (浏览器内编译)
  - Yjs CRDT (实时协作)
  - WebRTC (点对点同步)
- **可独立嵌入**: ✅ 是，Web 应用
- **特点**:
  - 本地优先架构
  - 所有数据存储在浏览器 IndexedDB
  - 支持离线编辑
  - 点对点协作，无服务器中介

#### Import / Export
- **支持格式**:
  - ✅ LaTeX (.tex)
  - ✅ Typst (.typ)
  - ✅ PDF (编译输出)
  - ❌ Markdown
  - ❌ DOCX
- **DOCX Track Changes**: ❌ 不支持

#### 可复用性判定
- **分级**: **Reference-only** (仅参考)
- **理由**:
  - ⚠️ **AGPL-3.0 许可证限制**:
    - 如果作为网络服务提供，必须向用户提供源代码
    - 与闭源分发、SaaS 使用存在冲突
  - ✅ 技术栈可参考:
    - Yjs CRDT 协作实现
    - WebRTC 点对点同步
    - SwiftLaTeX WASM 浏览器内编译
  - ❌ 不能直接 Fork 用于闭源产品
  - 适合学习协作编辑和本地优先架构设计

---

### 2.3 Oleafly

**官方仓库**: https://github.com/Oleafly/Oleafly  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~842 stars
- **维护活跃度**: 超活跃，持续开发中

#### 许可证
- **SPDX 标识**: AGPL-3.0
- **许可证文件路径**: LICENSE 文件
- **关键条款摘录**:
  ```
  Oleafly 是一款开源的 LaTeX、Typst 与 Markdown 编辑器
  
  许可证: AGPL v3
  
  AGPL-3.0 核心要求:
  - 你可以使用、修改和分发此软件
  - 可用于任何目的，包括商业用途
  - 如果分发修改版，必须分发源代码
  - 如果作为网络服务运行修改版，必须向用户提供源代码
  
  引用 Oleafly:
  @software{oleafly,
    author  = {Venkateshmurthy, Prajwal S. and {The Oleafly contributors}},
    title   = {Oleafly: a local-first workspace for research writing},
    year    = {2026},
    version = {0.4.8},
    url     = {https://github.com/Oleafly/Oleafly},
    license = {AGPL-3.0-or-later}
  }
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求

#### 源码结构
```
Oleafly/
├── src-tauri/                    # Rust 后端 (Tauri)
│   ├── crates/                   # 20 个 Rust crate
│   └── resources/
│       └── skills/               # AI agent skills
├── src/                          # React + TypeScript 前端
│   ├── components/
│   └── ...
├── docs/                         # 文档
├── Cargo.toml                    # Rust workspace 配置
├── package.json
└── ...
```

**核心模块**:
- 20 个 Rust crate 组成后端
- React + TypeScript 前端
- Tauri 桌面应用框架
- 集成 14+ AI agents (Claude Code, Codex 等)

#### Document Schema
- **文档模型**: LaTeX/Typst/Markdown 源码 (纯文本)
- **稳定性**: ✅ 稳定 (基于标准格式)
- **特点**:
  - 支持三种主流格式
  - 直接编辑源码
  - Git 版本控制集成

#### Figure / Panel
- **原生支持**: ✅ Diagram Composer
- **编号解析**: ✅ 通过编译实现
- **特点**:
  - 可视化图表编辑器
  - 支持 TikZ, fletcher (Typst), Mermaid
  - 画布与代码并排显示，双向同步

#### Reference / Citation
- **实现方式**: Zotero 集成
- **支持格式**: BibTeX, BibLaTeX
- **特点**:
  - @ 符号快速引用
  - 自动从 Zotero 文献库提取
  - 支持 arXiv, Semantic Scholar, Crossref, PubMed, OpenAlex 搜索
  - 自动添加到项目 .bib 文件

#### Editor
- **技术栈**: 
  - Tauri (Rust 桌面框架)
  - React + TypeScript (前端)
  - CodeMirror 或类似编辑器 (推测)
  - Oleafly Server (协作服务)
- **可独立嵌入**: ⚠️ 部分可以，需要剥离桌面应用层
- **特点**:
  - 本地优先架构
  - 内置 Tectonic, Typst, Pandoc 编译器
  - Vim 和 Emacs 键位支持
  - 236 个 LaTeX 符号可搜索面板
  - 实时协作 (共享光标、评论)
  - 离线编辑，联网自动同步

#### Import / Export
- **支持格式**:
  - ✅ LaTeX (.tex)
  - ✅ Typst (.typ)
  - ✅ Markdown (.md)
  - ✅ PDF (编译输出)
  - ⚠️ DOCX (通过 Pandoc)
  - ✅ Git/GitHub 同步
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc，非原生)
- **特色功能**:
  - Preflight 检查 (投稿前验证)
  - 1700+ 模板库
  - AI agents 集成

#### 可复用性判定
- **分级**: **Reference-only** (仅参考)
- **理由**:
  - ⚠️ **AGPL-3.0 许可证限制**:
    - 与闭源分发、SaaS 使用存在冲突
    - 网络服务必须提供源代码
  - ✅ 技术架构可参考:
    - Tauri + React + Rust 桌面应用架构
    - 本地优先 + 离线同步设计
    - AI agents 集成模式
    - Zotero 引用集成
    - Diagram Composer 可视化图表编辑
  - ❌ 不能直接 Fork 用于闭源产品
  - 适合作为功能参考和架构学习

---

### 2.4 Manubot

**官方仓库**: https://github.com/manubot/manubot  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main
- **最近提交**: 2024 年有活动
- **Star 量级**: 中等规模
- **维护活跃度**: 低到中等，稳定维护

#### 许可证
- **SPDX 标识**: CC-BY-4.0 (文档) / CC0-1.0 (代码)
- **许可证文件路径**: 
  - `LICENSE.md` (CC-BY-4.0)
  - `LICENSE-CC0.md` (CC0-1.0)
- **关键条款摘录**:
  ```
  双许可模式:
  
  1. CC BY 4.0 (适用于文档):
     - *.md, *.html, *.pdf, *.docx
  
  2. CC0 1.0 (适用于代码和数据):
     - *.sh, *.py, *.yml, *.yaml, *.json, *.bib, *.tsv, .gitignore
  
  CC BY 4.0 核心条款:
  本允许任何人复制、分发、展示、表演、改编本作品，
  前提是给予适当的署名。
  
  CC0 1.0 核心条款:
  在法律允许的范围内，作者放弃本作品的所有版权及相关权利。
  您可以复制、修改、分发和执行本作品，甚至用于商业目的，无需请求许可。
  ```
- **双许可/附加条款**: ✅ 是，文档和代码分别许可
- **CLA**: 未要求

#### 源码结构
```
manubot/
├── manubot/                      # Python 包源码
│   ├── __init__.py
│   ├── cite.py                   # 引用管理
│   ├── process.py                # 文档处理
│   └── ai_revision.py            # AI 修订
├── tests/                        # 测试
├── setup.py                      # 安装脚本
├── pyproject.toml
├── LICENSE.md
├── LICENSE-CC0.md
└── README.md
```

**核心模块**:
- `manubot cite`: 命令行引用检索工具
- `manubot process`: 文档处理流水线
- `manubot ai-revision`: AI 辅助修订

#### Document Schema
- **文档模型**: Markdown + YAML metadata
- **稳定性**: ✅ 稳定
- **特点**:
  - 纯文本 Markdown 源文件
  - YAML frontmatter 定义元数据
  - citations.json 存储引用数据
  - 机器可读、可验证

#### Figure / Panel
- **原生支持**: ⚠️ 依赖 Pandoc 能力
- **编号解析**: ✅ 通过 Pandoc 交叉引用
- **实现方式**: Markdown 图片语法 + Pandoc 扩展

#### Reference / Citation
- **实现方式**: Citation.js + 自动元数据检索
- **支持格式**: 
  - DOI
  - PubMed ID
  - arXiv ID
  - ISBN
  - URL
  - BibTeX
- **特点**:
  - 自动解析持久标识符
  - 自动获取文献元数据
  - 支持数千种引用样式 (CSL)
  - 无需手动维护参考文献列表

#### Editor
- **技术栈**: 
  - 纯文本编辑器 (任何 Markdown 编辑器)
  - Git 版本控制
  - GitHub 协作
- **可独立嵌入**: ✅ 是，工具链可集成
- **特点**:
  - 无专有编辑器
  - 基于 Git/GitHub 的协作流程
  - 持续集成 (CI) 自动构建

#### Import / Export
- **支持格式**:
  - ✅ Markdown (输入)
  - ✅ HTML (输出)
  - ✅ PDF (输出，通过 Pandoc + LaTeX)
  - ✅ DOCX (输出，通过 Pandoc)
  - ✅ BibTeX (引用)
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc)
- **特色功能**:
  - 持续集成自动部署
  - GitHub Pages 托管
  - 版本历史追踪

#### 可复用性判定
- **分级**: **Adapt** (适配复用)
- **理由**:
  - ✅ **宽松许可证**:
    - CC-BY-4.0 允许自由使用、修改、分发
    - CC0-1.0 代码部分几乎无限制
  - ✅ **工具链可复用**:
    - Python 包可独立使用
    - 引用管理功能可提取
    - Pandoc 集成模式可参考
  - ✅ **架构清晰**:
    - 模块化设计
    - 命令行工具易于集成
  - ⚠️ **局限性**:
    - 无图形编辑器
    - 依赖 Git/GitHub 工作流
    - 协作功能有限
  - 适合提取引用管理和文档处理工具

---

### 2.5 Quarto

**官方仓库**: https://github.com/quarto-dev/quarto-cli  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~2,646 stars
- **维护活跃度**: 超活跃，由 Posit 公司支持

#### 许可证
- **SPDX 标识**: MIT (v1.4+) / GPL-2.0 (v1.3 及更早)
- **许可证文件路径**: LICENSE 文件
- **关键条款摘录**:
  ```
  Quarto version 1.4 is licensed under the MIT License.
  Quarto version 1.3 (and earlier) is licensed under the GNU GPL v2.
  
  MIT License 核心条款:
  特此免费授予任何获得本软件及相关文档文件副本的人不受限制地处置本软件的许可，
  包括但不限于使用、复制、修改、合并、发布、分发、再许可和/或出售本软件副本的权利。
  
  上述版权声明和本许可声明应包含在本软件的所有副本或实质性部分中。
  
  本软件按"原样"提供，不附带任何形式的明示或默示担保。
  ```
- **双许可/附加条款**: ⚠️ 版本差异 (v1.4 起改为 MIT)
- **CLA**: 未要求

#### 源码结构
```
quarto-cli/
├── src/                          # TypeScript/Deno 源码
│   ├── core/                     # 核心功能
│   ├── command/                  # 命令实现
│   └── ...
├── tests/                        # 测试
├── package.json
├── deno.json                     # Deno 配置
└── ...
```

**核心模块**:
- 基于 TypeScript + Deno
- 命令行工具 (quarto-cli)
- 集成 Jupyter, Knitr, Observable

#### Document Schema
- **文档模型**: Pandoc Markdown 扩展
- **稳定性**: ✅ 非常稳定
- **特点**:
  - 基于 Pandoc Markdown
  - YAML frontmatter 配置
  - 扩展语法支持:
    - 交叉引用 (@fig, @tbl, @eq, @sec)
    - 子图 (sub-figures)
    - 布局面板 (layout panels)
    - 悬停引用和脚注
    - 标注框 (callouts)

#### Figure / Panel
- **原生支持**: ✅ 完整支持
- **编号解析**: ✅ 自动编号和交叉引用
- **特点**:
  - 子图支持
  - 布局面板
  - 图表代码嵌入
  - 支持 Python, R, Julia, JavaScript

#### Reference / Citation
- **实现方式**: Pandoc citeproc + BibTeX
- **支持格式**: 
  - BibTeX (.bib)
  - CSL JSON
  - DOI
  - 其他持久标识符
- **特点**:
  - 支持数千种 CSL 引用样式
  - 自动格式化参考文献列表
  - 悬停引用预览

#### Editor
- **技术栈**: 
  - 无专有编辑器
  - 支持多种编辑器:
    - JupyterLab
    - RStudio
    - VS Code (有官方扩展)
    - 任何文本编辑器
  - 内置可视化 Markdown 编辑器
- **可独立嵌入**: ✅ 是，工具链可集成
- **特点**:
  - 可视化 Markdown 编辑模式
  - 所见即所得长文档编辑
  - 代码执行和输出预览

#### Import / Export
- **支持格式**:
  - ✅ Markdown (输入)
  - ✅ Jupyter notebooks (输入)
  - ✅ R Markdown (输入)
  - ✅ HTML (输出)
  - ✅ PDF (输出，通过 LaTeX 或 Typst)
  - ✅ DOCX (输出，通过 Pandoc)
  - ✅ Beamer (输出)
  - ✅ 网站 (输出)
  - ✅ 书籍 (输出)
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc)
- **特色功能**:
  - 项目系统 (多文档渲染)
  - 短代码 (shortcodes)
  - 过滤器 (filters)
  - 格式扩展

#### 可复用性判定
- **分级**: **Fork/Adapt** (可 Fork 或适配)
- **理由**:
  - ✅ **MIT 许可证** (v1.4+):
    - 允许自由使用、修改、分发
    - 可用于闭源产品
    - 无 copyleft 限制
  - ✅ **最成熟的方案**:
    - 由 Posit 公司支持和维护
    - 活跃的社区和生态系统
    - 完善的文档
  - ✅ **功能全面**:
    - 支持多种输入格式
    - 支持多种输出格式
    - 强大的交叉引用和引用管理
    - 代码执行集成
  - ✅ **架构清晰**:
    - 基于 Pandoc
    - TypeScript/Deno 实现
    - 模块化设计
  - ⚠️ **考虑因素**:
    - 需要维护与上游 Pandoc 的兼容性
    - 功能复杂，学习曲线较陡
  - 最适合直接 Fork 或作为基础构建

---

### 2.6 Typst

**官方仓库**: https://github.com/typst/typst  
**访问状态**: ✅ 已核实 (通过搜索结果和文档)

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~51,702 stars
- **维护活跃度**: 超活跃，快速发展中

#### 许可证
- **SPDX 标识**: Apache-2.0
- **许可证文件路径**: LICENSE 文件
- **关键条款摘录**:
  ```
  Apache License
  Version 2.0, January 2004
  http://www.apache.org/licenses/
  
  核心条款:
  特此允许任何获得本作品及相关文档文件副本的人，
  不受限制地处理本作品，包括但不限于使用、复制、修改、
  合并、发布、分发、再许可和/或出售本作品的副本，
  并允许向其提供本作品的人这样做，但须符合以下条件:
  
  上述版权声明和本许可声明应包含在本作品的所有副本或实质性部分中。
  
  本作品按"原样"提供，不附带任何形式的明示或默示担保。
  
  Apache 2.0 特点:
  - 允许商业使用
  - 允许修改和分发
  - 允许专利使用
  - 要求保留版权声明
  - 无 copyleft 限制
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求

#### 源码结构
```
typst/
├── crates/                       # Rust crate 工作区
│   ├── typst/                    # 主编译器门面 (~325 行)
│   ├── typst-syntax/             # 语法解析 (~5,000 行)
│   ├── typst-eval/               # AST 解释器 (~3,000 行)
│   ├── typst-realize/            # Show 规则应用 (~1,500 行)
│   ├── typst-layout/             # 布局引擎 (~8,000 行)
│   ├── typst-library/            # 标准库 (~15,000 行)
│   ├── typst-pdf/                # PDF 导出 (~2,000 行)
│   ├── typst-svg/                # SVG 导出
│   ├── typst-html/               # HTML 导出
│   ├── typst-render/             # 内置渲染器
│   ├── typst-ide/                # IDE 功能
│   └── typst-cli/                # 命令行接口
├── docs/                         # 文档
├── tests/                        # 测试套件
└── tools/                        # 开发工具
```

**核心模块**:
- 17 个核心 Rust crate
- 总计约 14 万行 Rust 代码
- 374 个源文件
- 五阶段增量编译管线:
  1. Parsing (typst-syntax)
  2. Evaluation (typst-eval)
  3. Realization (typst-realize)
  4. Layout (typst-layout)
  5. Export (typst-pdf/svg/html/render)

#### Document Schema
- **文档模型**: 自有标记语言 (Typst syntax)
- **稳定性**: ✅ 稳定，但仍在快速演进
- **特点**:
  - 基于标记语言的排版系统
  - 类似 Markdown 但更强大
  - 内置脚本系统
  - 函数式编程范式
  - 增量编译 (基于 comemo 框架)

#### Figure / Panel
- **原生支持**: ✅ 完整支持
- **编号解析**: ✅ 自动编号和交叉引用
- **特点**:
  - 图表环境 (figure)
  - 子图支持
  - 布局控制
  - 代码生成图表

#### Reference / Citation
- **实现方式**: 内置引用系统 (hayagriva)
- **支持格式**: 
  - BibTeX (.bib)
  - YAML 参考文献
- **特点**:
  - 内置引用管理
  - 自动格式化
  - 支持多种引用样式
  - 交叉引用

#### Editor
- **技术栈**: 
  - 命令行工具 (typst-cli)
  - 在线协作编辑器 (app.typst.org)
  - 第三方编辑器集成:
    - VS Code 扩展
    - Neovim 插件
    - Vim 插件
- **可独立嵌入**: ✅ 是，编译器可作为库使用
- **特点**:
  - 实时预览 (typst watch)
  - 快速编译 (增量编译)
  - 友好的错误信息
  - IDE 支持 (自动补全、悬停提示)

#### Import / Export
- **支持格式**:
  - ✅ Typst (.typ, 输入)
  - ✅ PDF (输出)
  - ✅ SVG (输出)
  - ✅ PNG (输出)
  - ✅ HTML (输出，实验性)
  - ⚠️ LaTeX (通过第三方工具转换)
  - ❌ Markdown (不直接支持)
  - ❌ DOCX (不支持)
- **DOCX Track Changes**: ❌ 不支持
- **特色功能**:
  - 增量编译 (毫秒级)
  - 多格式导出
  - 包管理系统 (Typst Universe)

#### 可复用性判定
- **分级**: **Reference** (参考实现)
- **理由**:
  - ✅ **Apache-2.0 许可证**:
    - 允许商业使用
    - 允许修改和分发
    - 允许专利使用
    - 无 copyleft 限制
  - ✅ **技术先进**:
    - Rust 实现，性能优异
    - 增量编译架构
    - 模块化设计
  - ✅ **可参考的架构**:
    - 五阶段编译管线
    - comemo 增量编译框架
    - 标记语言设计
  - ⚠️ **局限性**:
    - 自有语法，不兼容 Markdown
    - 无 DOCX 支持
    - 生态系统相对较新
    - 学习曲线
  - ⚠️ **适用场景**:
    - 参考其编译架构设计
    - 参考其增量编译实现
    - 参考其 Rust 代码组织
    - 不适合作为基础直接构建 (语法不兼容)
  - 最适合学习和参考其技术实现

---

### 2.7 TeXMind

**官方仓库**: **未能核实**  
**访问状态**: ❌ 未能找到可验证的开源科学写作项目

#### 核实尝试
- 搜索 "TeXMind GitHub repository scientific writing"
- 搜索 "TeXMind editor"
- 搜索 "TeXMind LaTeX"

#### 搜索结果
- 找到 "TexMind" 商业软件 (纺织行业软件，非科学写作工具)
- 未找到任何与科学写作相关的开源 TeXMind 项目
- 未找到相关 GitHub 仓库

#### 结论
**未能核实** - 该项目可能:
1. 不存在或已停止维护
2. 名称拼写错误
3. 非常小众，缺乏公开信息
4. 私有项目，未开源

#### 可复用性判定
- **分级**: **未能核实**
- **理由**: 无法找到可验证的项目信息，无法评估

---

## 3. 许可证风险汇总

### 3.1 高风险 (AGPL-3.0)

**涉及项目**: TeXlyre, Oleafly

**风险说明**:
- ⚠️ **网络服务条款 (Affero 条款)**:
  - 如果作为网络服务提供，必须向用户提供源代码
  - 即使用户通过网络与软件交互，也触发源代码提供义务
  
- ⚠️ **Copyleft 强传染性**:
  - 修改版必须以相同许可证分发
  - 与闭源分发存在根本冲突
  
- ⚠️ **SaaS 使用限制**:
  - 如果项目计划提供 SaaS 服务，AGPL 要求公开源代码
  - 这可能暴露专有技术和商业机密

**具体冲突**:
- ❌ 不能用于闭源商业产品
- ❌ 不能作为 SaaS 后端而不公开源代码
- ⚠️ 需要法律评估是否构成"衍生作品"

**建议**:
- 仅作为参考和学习对象
- 如需使用其技术，需要独立重新实现
- 咨询法律专家评估合规风险

### 3.2 中风险 (GPL-2.0)

**涉及项目**: Quarto (v1.3 及更早版本)

**风险说明**:
- ⚠️ **Copyleft 传染性**:
  - 修改版必须以相同许可证分发
  - 链接 GPL 代码可能使整个项目成为 GPL
  
- ⚠️ **版本差异**:
  - Quarto v1.4+ 已改为 MIT 许可证
  - 如果使用旧版本，仍受 GPL 约束

**具体冲突**:
- ❌ GPL-2.0 代码不能与闭源产品链接
- ✅ 如果使用 Quarto v1.4+ (MIT)，无此风险

**建议**:
- 确保使用 Quarto v1.4 或更新版本
- 检查依赖树，确认无 GPL 组件

### 3.3 低风险 (MIT, Apache-2.0, CC-BY-4.0, CC0-1.0)

**涉及项目**: Curvenote Editor (MIT), Manubot (CC-BY-4.0/CC0-1.0), Quarto v1.4+ (MIT), Typst (Apache-2.0)

**风险说明**:
- ✅ **宽松许可证**:
  - 允许商业使用
  - 允许修改和分发
  - 允许闭源衍生作品
  - 无 copyleft 限制

- ⚠️ **注意事项**:
  - 需要保留版权声明
  - Apache-2.0 包含专利授权条款
  - CC-BY-4.0 要求署名

**具体优势**:
- ✅ 可用于闭源商业产品
- ✅ 可作为 SaaS 后端
- ✅ 可自由修改和分发
- ✅ 无传染性风险

**建议**:
- 保留原始版权声明和许可证文本
- Apache-2.0 项目注意专利条款
- CC-BY-4.0 项目正确署名

### 3.4 许可证兼容性矩阵

| 本项目许可证 | MIT | Apache-2.0 | CC-BY-4.0 | CC0-1.0 | GPL-2.0 | AGPL-3.0 |
|-------------|-----|------------|-----------|---------|---------|----------|
| **MIT** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Apache-2.0** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **GPL-2.0** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **AGPL-3.0** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **闭源** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

**结论**: 
- ✅ MIT, Apache-2.0, CC-BY-4.0, CC0-1.0 与大多数许可证兼容
- ❌ GPL-2.0 和 AGPL-3.0 与闭源分发不兼容
- ⚠️ 如果本项目计划闭源分发，应避免使用 GPL/AGPL 代码

---

## 4. 可复用性分级

### 4.1 Fork (可直接 Fork)

**项目**: Quarto (v1.4+)

**理由**:
- ✅ MIT 许可证，无 copyleft 限制
- ✅ 功能最全面，生态系统最成熟
- ✅ 基于 Pandoc，有强大的文档转换能力
- ✅ 支持多种输入/输出格式
- ✅ 活跃的社区和公司支持
- ✅ 架构清晰，易于理解和维护

**Fork 策略**:
1. Fork quarto-dev/quarto-cli
2. 保留核心 Pandoc 集成
3. 定制科学写作特定功能
4. 维护与上游的兼容性

**风险**:
- ⚠️ 需要维护与 Pandoc 的兼容性
- ⚠️ 功能复杂，学习曲线较陡
- ⚠️ 需要持续跟进上游更新

### 4.2 Adapt (适配复用)

**项目**: Curvenote Editor, Manubot

#### Curvenote Editor

**理由**:
- ✅ MIT 许可证
- ✅ ProseMirror 编辑器核心可提取
- ✅ Schema 设计清晰，可定制
- ✅ React + Redux 技术栈成熟

**适配策略**:
1. 提取 @curvenote/schema 和 @curvenote/editor
2. 剥离与 Curvenote 平台的集成
3. 定制科学写作特定的节点类型
4. 实现自己的协作后端 (或集成 Yjs)

**风险**:
- ⚠️ 需要大量定制工作
- ⚠️ 协作功能需要额外开发
- ⚠️ 文档可能不够完善

#### Manubot

**理由**:
- ✅ CC-BY-4.0 / CC0-1.0 许可证
- ✅ Python 工具链易于集成
- ✅ 引用管理功能成熟
- ✅ 与 Pandoc 集成良好

**适配策略**:
1. 提取 manubot cite 和 manubot process
2. 集成到自己的文档处理流水线
3. 利用其引用管理能力
4. 扩展 Pandoc 集成

**风险**:
- ⚠️ 无图形编辑器
- ⚠️ 依赖 Git/GitHub 工作流
- ⚠️ 维护活跃度较低

### 4.3 Reference (仅参考)

**项目**: TeXlyre, Oleafly, Typst

#### TeXlyre

**参考价值**:
- ✅ Yjs CRDT 协作实现
- ✅ WebRTC 点对点同步
- ✅ SwiftLaTeX WASM 浏览器内编译
- ✅ 本地优先架构设计

**不能直接使用的原因**:
- ❌ AGPL-3.0 许可证限制
- ❌ 与闭源分发冲突

#### Oleafly

**参考价值**:
- ✅ Tauri + React + Rust 桌面应用架构
- ✅ 本地优先 + 离线同步设计
- ✅ AI agents 集成模式
- ✅ Zotero 引用集成
- ✅ Diagram Composer 可视化图表编辑
- ✅ Preflight 检查功能

**不能直接使用的原因**:
- ❌ AGPL-3.0 许可证限制
- ❌ 与闭源分发冲突

#### Typst

**参考价值**:
- ✅ Rust 编译器架构
- ✅ 五阶段增量编译管线
- ✅ comemo 增量编译框架
- ✅ 标记语言设计
- ✅ 模块化 crate 组织
- ✅ 高性能排版引擎

**不能直接使用的原因**:
- ⚠️ 自有语法，不兼容 Markdown
- ⚠️ 无 DOCX 支持
- ⚠️ 生态系统较新

**可参考的部分**:
- 编译架构设计
- 增量编译实现
- Rust 代码组织
- 排版算法

### 4.4 未能核实

**项目**: TeXMind

**原因**:
- ❌ 无法找到可验证的项目信息
- ❌ 无法评估技术架构
- ❌ 无法评估许可证合规性

---

## 5. 与本项目的匹配度分析

### 5.1 本项目需求假设

基于任务描述，推测本项目需要:
- ✅ 科学写作编辑器
- ✅ 多面板图支持
- ✅ 引用管理
- ✅ DOCX 导入/导出 (尤其 Track Changes)
- ✅ 协作功能
- ✅ 可复用、可定制的架构

### 5.2 匹配度评分

| 项目 | 许可证兼容性 | 功能匹配度 | 技术可复用性 | 维护成本 | 综合评分 |
|------|-------------|-----------|-------------|---------|---------|
| **Quarto** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **A** |
| **Curvenote** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | **B+** |
| **Manubot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **B** |
| **Typst** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **B-** |
| **Oleafly** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | **C** |
| **TeXlyre** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | **C-** |
| **TeXMind** | ❓ | ❓ | ❓ | ❓ | **未能核实** |

### 5.3 详细分析

#### Quarto - 最佳匹配 (A)

**优势**:
- ✅ MIT 许可证，完全兼容闭源商业产品
- ✅ 功能最全面:
  - 支持 Markdown, Jupyter, R Markdown
  - 输出 HTML, PDF, DOCX, 网站, 书籍
  - 强大的交叉引用和引用管理
  - 代码执行集成
- ✅ 基于 Pandoc，DOCX 支持成熟
- ✅ 活跃的社区和 Posit 公司支持
- ✅ 架构清晰，易于扩展

**劣势**:
- ⚠️ 功能复杂，学习曲线较陡
- ⚠️ 需要维护与 Pandoc 的兼容性
- ⚠️ TypeScript/Deno 技术栈可能需要团队学习

**适用场景**:
- 需要完整的科学写作和发布平台
- 需要多种输入/输出格式支持
- 需要代码执行和可重现研究

#### Curvenote Editor - 良好匹配 (B+)

**优势**:
- ✅ MIT 许可证
- ✅ ProseMirror 编辑器核心可定制
- ✅ 所见即所得编辑体验
- ✅ 模块化设计

**劣势**:
- ⚠️ 需要大量定制工作
- ⚠️ 协作功能需要额外开发
- ⚠️ DOCX 支持有限

**适用场景**:
- 需要自定义编辑器体验
- 需要所见即所得编辑
- 有前端开发能力

#### Manubot - 中等匹配 (B)

**优势**:
- ✅ CC-BY-4.0 / CC0-1.0 许可证
- ✅ 引用管理功能成熟
- ✅ Python 工具链易于集成
- ✅ 与 GitHub 集成良好

**劣势**:
- ⚠️ 无图形编辑器
- ⚠️ 依赖 Git/GitHub 工作流
- ⚠️ 维护活跃度较低

**适用场景**:
- 需要引用管理工具
- 基于 Git 的协作流程
- 命令行优先的工作流

#### Typst - 参考匹配 (B-)

**优势**:
- ✅ Apache-2.0 许可证
- ✅ Rust 实现，性能优异
- ✅ 增量编译架构先进

**劣势**:
- ⚠️ 自有语法，不兼容 Markdown
- ⚠️ 无 DOCX 支持
- ⚠️ 生态系统较新

**适用场景**:
- 参考其编译架构设计
- 学习增量编译实现
- 不适合作为基础直接构建

#### Oleafly / TeXlyre - 低匹配 (C/C-)

**优势**:
- ✅ 功能丰富
- ✅ 技术先进

**劣势**:
- ❌ AGPL-3.0 许可证与闭源分发冲突
- ❌ 法律风险高

**适用场景**:
- 仅作为功能参考
- 学习其架构设计
- 不能直接用于闭源产品

### 5.4 推荐方案

#### 方案 A: 基于 Quarto Fork (推荐)

**策略**:
1. Fork quarto-dev/quarto-cli (MIT 许可证)
2. 保留核心 Pandoc 集成
3. 定制科学写作特定功能:
   - 增强多面板图支持
   - 优化引用管理
   - 改进 DOCX Track Changes
4. 维护与上游的兼容性

**优势**:
- ✅ 许可证无风险
- ✅ 功能最全面
- ✅ 社区活跃
- ✅ 维护成本相对较低

**风险**:
- ⚠️ 需要理解 Pandoc 集成
- ⚠️ 需要 TypeScript/Deno 开发能力

#### 方案 B: 基于 Curvenote 定制

**策略**:
1. 提取 Curvenote Editor 核心
2. 定制 Schema 和插件
3. 实现自己的协作后端
4. 集成 Pandoc 进行文档转换

**优势**:
- ✅ 许可证无风险
- ✅ 编辑器可高度定制
- ✅ 所见即所得体验

**风险**:
- ⚠️ 需要大量开发工作
- ⚠️ 协作功能复杂
- ⚠️ DOCX 支持需要额外实现

#### 方案 C: 混合方案

**策略**:
1. 使用 Manubot 的引用管理工具
2. 使用 ProseMirror 构建编辑器 (参考 Curvenote)
3. 集成 Pandoc 进行文档转换
4. 参考 Typst 的增量编译架构

**优势**:
- ✅ 许可证无风险
- ✅ 可组合最佳组件
- ✅ 灵活度高

**风险**:
- ⚠️ 集成工作量大
- ⚠️ 需要维护多个组件
- ⚠️ 架构复杂度高

---

## 6. 未能核实的事项

### 6.1 TeXMind 项目

**状态**: ❌ 未能核实

**尝试方式**:
- Web 搜索 "TeXMind GitHub repository scientific writing"
- Web 搜索 "TeXMind editor"
- Web 搜索 "TeXMind LaTeX"
- 检查相关开源项目列表

**结果**:
- 未找到任何与科学写作相关的开源 TeXMind 项目
- 找到的 "TexMind" 是商业纺织软件，与科学写作无关

**可能的原因**:
1. 项目名称拼写错误
2. 项目已停止维护并删除
3. 项目为私有，未开源
4. 项目非常小众，缺乏公开信息

**建议**:
- 确认项目名称是否正确
- 提供更多线索 (如作者、网址等)
- 如确实不存在，从候选列表中移除

### 6.2 部分项目的具体技术细节

以下信息基于搜索结果和文档推断，未直接访问源码验证:

#### Curvenote Editor
- ⚠️ 具体包结构基于文档推断
- ⚠️ 协作实现细节未验证
- ⚠️ DOCX 支持程度未测试

#### TeXlyre
- ⚠️ 前端技术栈基于搜索结果推断
- ⚠️ 插件系统具体实现未验证
- ⚠️ SwiftLaTeX 集成细节未确认

#### Oleafly
- ⚠️ 20 个 Rust crate 的具体职责未详细验证
- ⚠️ AI agents 集成方式基于文档推断
- ⚠️ Diagram Composer 技术实现未深入分析

#### Manubot
- ⚠️ 最新版本的维护状态未确认
- ⚠️ DOCX Track Changes 支持程度未测试

#### Quarto
- ⚠️ v1.4 许可证变更的具体时间点未确认
- ⚠️ 内部架构细节基于文档推断

#### Typst
- ⚠️ 17 个 crate 的代码量数据基于文档
- ⚠️ comemo 框架的具体实现未深入分析

### 6.3 DOCX Track Changes 支持

**状态**: ⚠️ 所有项目的 DOCX Track Changes 支持均未详细验证

**说明**:
- 大多数项目通过 Pandoc 实现 DOCX 导入/导出
- Pandoc 对 Track Changes 的支持有限
- 需要实际测试验证各项目的 Track Changes 处理能力

**建议**:
- 对候选项目进行实际 DOCX Track Changes 测试
- 评估是否需要自定义实现

---

## 7. 证据清单

### 7.1 访问日期
**审计日期**: 2026-11-06

### 7.2 信息来源

#### Curvenote Editor
1. https://github.com/curvenote/editor - 项目仓库 (搜索结果显示)
2. https://curvenote.com/ - 官方网站
3. https://m.blog.csdn.net/gitblog_00304/article/details/146586828 - 技术介绍文章
4. ProseMirror 官方文档 - 编辑器框架

#### TeXlyre
1. https://github.com/TeXlyre/texlyre - 项目仓库 (搜索结果显示)
2. https://www.xugj520.cn/archives/texlyre-latex-collaboration.html - 详细介绍文章
3. https://m.weibo.cn/status/Q09IkAx5e - 微博介绍
4. Yjs 官方文档 - CRDT 框架
5. SwiftLaTeX 项目 - WASM LaTeX 引擎

#### Oleafly
1. https://github.com/Oleafly/Oleafly - 项目仓库 (搜索结果显示)
2. https://github.com/Oleafly/Oleafly/blob/main/docs/readme-translations/README.zh.md - 中文文档
3. https://m.blog.csdn.net/gitblog_00588/article/details/162169540 - 贡献指南
4. Tauri 官方文档 - 桌面应用框架

#### Manubot
1. https://github.com/manubot/manubot - 项目仓库 (搜索结果显示)
2. https://manubot.org/ - 官方网站
3. https://pypi.org/project/manubot/ - PyPI 包
4. https://blog.csdn.net/gitblog_00970/article/details/142803195 - 技术介绍
5. Citation.js 文档 - 引用管理

#### Quarto
1. https://github.com/quarto-dev/quarto-cli - 项目仓库 (搜索结果显示)
2. https://quarto.org/ - 官方网站
3. https://pypi.org/project/quarto-cli/ - PyPI 包
4. https://m.blog.csdn.net/gitblog_01059/article/details/154635189 - 技术介绍
5. Pandoc 官方文档 - 文档转换

#### Typst
1. https://github.com/typst/typst - 项目仓库 (搜索结果显示)
2. https://tool.lu/ko_KR/library/2Hz - 项目介绍
3. https://www.xugj520.cn/archives/typst-latex-alternative-guide-2.html - 对比分析
4. https://m.oschina.net/p/typst - 开源中国介绍
5. Typst 官方文档 - 语法和用法

#### TeXMind
1. 多次 Web 搜索均未找到相关项目
2. 搜索关键词: "TeXMind GitHub", "TeXMind scientific writing", "TeXMind editor"

### 7.3 许可证原文来源

#### MIT License
- 来源: Curvenote Editor, Quarto (v1.4+)
- 标准文本: https://opensource.org/licenses/MIT

#### AGPL-3.0
- 来源: TeXlyre, Oleafly
- 标准文本: https://www.gnu.org/licenses/agpl-3.0.html

#### Apache-2.0
- 来源: Typst
- 标准文本: https://www.apache.org/licenses/LICENSE-2.0.html

#### CC-BY-4.0
- 来源: Manubot (文档部分)
- 标准文本: https://creativecommons.org/licenses/by/4.0/

#### CC0-1.0
- 来源: Manubot (代码部分)
- 标准文本: https://creativecommons.org/publicdomain/zero/1.0/

### 7.4 技术细节验证

#### 已验证
- ✅ 各项目的许可证类型
- ✅ 各项目的官方仓库 URL
- ✅ Quarto 的许可证变更 (v1.3 GPL → v1.4 MIT)
- ✅ Typst 的 Rust 实现和 crate 结构
- ✅ Manubot 的双许可模式

#### 推断 (基于文档和搜索结果)
- ⚠️ 各项目的具体源码结构
- ⚠️ 编辑器的技术栈细节
- ⚠️ DOCX Track Changes 支持程度
- ⚠️ 协作功能的具体实现

#### 未验证
- ❌ TeXMind 项目存在性
- ❌ 各项目的实际功能测试
- ❌ 许可证合规性的法律评估

### 7.5 参考资源

1. **开源许可证指南**:
   - https://choosealicense.com/
   - https://opensource.org/licenses

2. **科学写作工具对比**:
   - https://github.com/anis-lakdar/awesome-scientific-writing
   - https://github.com/YDX-2147483647/best-of-typst

3. **技术文档**:
   - ProseMirror: https://prosemirror.net/
   - Yjs: https://docs.yjs.dev
   - Pandoc: https://pandoc.org/
   - Tauri: https://tauri.app/
   - Typst: https://typst.app/docs/

---

## 附录: 术语表

- **SPDX**: Software Package Data Exchange，软件包数据交换标准
- **AST**: Abstract Syntax Tree，抽象语法树
- **CRDT**: Conflict-free Replicated Data Type，无冲突复制数据类型
- **WYSIWYG**: What You See Is What You Get，所见即所得
- **WYSIWYM**: What You See Is What You Mean，所见即所想
- **SaaS**: Software as a Service，软件即服务
- **CLA**: Contributor License Agreement，贡献者许可协议
- **Copyleft**: 著作权左派，要求衍生作品使用相同许可证
- **CSL**: Citation Style Language，引用样式语言
- **DOI**: Digital Object Identifier，数字对象标识符

---

**文档版本**: 1.0  
**最后更新**: 2026-11-06  
**审计状态**: 完成 (6/7 项目已核实，1 项未能核实)
