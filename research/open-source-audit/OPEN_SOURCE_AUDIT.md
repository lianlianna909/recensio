# Open Source Audit (修订版)

**审计日期**: 2026-11-06  
**修订日期**: 2026-11-06  
**审计员**: Worker D - Open-source Researcher  
**项目**: ScientificWritingProject  
**修订原因**: 独立 QA 审计判定原报告为 RISK，需修复 G1–G6 六项问题

---

## 0. 分发形态前提声明

> **关键前提**: 本报告的许可证兼容性分析与可复用性判定均基于以下假设：
>
> **本项目可能以闭源形式分发（包括商业 SaaS 或私有部署）。**
>
> 此前提来源于项目需求文档中对"可复用性"的强调，以及对 AGPL/GPL 项目标记为 "Reference-only" 的判定逻辑。

### 若前提变更

| 分发形态 | 对结论的影响 |
|----------|-------------|
| **闭源分发**（当前假设） | AGPL 项目 (TeXlyre, Oleafly) 不可直接使用；GPL-2.0 历史版本 (Quarto ≤v1.3) 不可链接；宽松许可证项目均可使用 |
| **MIT 开源分发** | 所有项目均可使用，包括 AGPL 项目（但 AGPL 的 copyleft 会传染至整个项目）；GPL-2.0 历史版本可使用（但 GPL copyleft 传染） |
| **GPL-3.0 开源分发** | AGPL-3.0 项目可兼容使用；GPL-2.0-only 项目不兼容（除非标注 "or later"）；Apache-2.0 与 GPL-3.0 单向兼容 |

**建议**: 项目决策层应明确分发形态后再做最终选型。本报告以"闭源分发"为默认前提。

---

## 1. 总览表

| 项目 | 许可证 | 活跃度 | 文档模型 | DOCX 支持 | 可复用性 |
|------|--------|--------|----------|-----------|----------|
| **Curvenote Editor** | MIT | 中等 (2024-2025) | ProseMirror Schema (JSON AST) | 有限 (通过 Pandoc) | **Adapt** - 编辑器核心可复用 |
| **TeXlyre** | AGPL-3.0 | 活跃 (2025) | LaTeX/Typst 源码 + Yjs CRDT | 无原生支持 | **Reference-only** - AGPL 限制闭源使用 |
| **Oleafly** | AGPL-3.0 | 超活跃 (2026) | LaTeX/Typst/Markdown 源码 | 通过 Pandoc | **Reference-only** - AGPL 限制闭源使用 |
| **Manubot** | **BSD-2-Clause-Patent** | 低 (2024) | Markdown + YAML metadata | 支持 (Pandoc) | **Adapt** - 工具链可复用 |
| **Quarto** | MIT (v1.4+) / GPL-2.0 (v1.3 及更早) | 超活跃 (2026) | Pandoc Markdown 扩展 | 支持 (Pandoc) | **Fork/Adapt** - 最成熟方案 |
| **Typst** | Apache-2.0 | 超活跃 (2026) | 自有标记语言 (AST) | 无原生支持 | **Reference** - 排版引擎可参考 |
| **TeXMind** | **未能核实** | **未能核实** | **未能核实** | **未能核实** | **未能核实** |

> **G1 修正**: Manubot 许可证由原报告的 "CC-BY-4.0 / CC0-1.0" 更正为 **BSD-2-Clause-Patent**。依据：GitHub API 直接获取的 LICENSE.md 原文。

---

## 2. 逐项目详查

### 2.1 Curvenote Editor

**官方仓库**: https://github.com/curvenote/editor  
**许可证文件**: LICENSE (仓库根目录)  
**证据文件**: `evidence/CURVENOTE_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API 核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2024-2025 期间活跃
- **Star 量级**: 中等规模项目
- **维护活跃度**: 中等，持续更新

#### 许可证
- **SPDX 标识**: MIT（GitHub API 确认 spdx_id: "MIT"）
- **许可证文件路径**: `LICENSE`
- **Copyright**: Copyright (c) 2022 Curvenote Inc.
- **关键条款摘录**:
  ```
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software...
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求
- **来源**: 一手来源 — GitHub API 直接获取

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
- 采用 Monorepo 管理 (npm workspaces)
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
**许可证文件**: LICENSE (仓库根目录)  
**证据文件**: `evidence/TEXLYRE_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API 核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2025 年活跃
- **Star 量级**: ~490 stars
- **维护活跃度**: 活跃，持续开发中

#### 许可证
- **SPDX 标识**: AGPL-3.0（GitHub API 确认 spdx_id: "AGPL-3.0"）
- **许可证文件路径**: `LICENSE`
- **关键条款摘录**:
  ```
  GNU AFFERO GENERAL PUBLIC LICENSE
  Version 3, 19 November 2007
  
  Everyone is permitted to copy and distribute verbatim copies
  of this license document, but changing it is not allowed.
  ```
- **双许可/附加条款**: 无
- **CLA**: 未要求
- **来源**: 一手来源 — GitHub API 直接获取

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

#### Figure / Panel
- **原生支持**: ⚠️ 依赖 LaTeX/Typst 原生能力
- **编号解析**: ✅ 通过 LaTeX/Typst 编译实现

#### Reference / Citation
- **实现方式**: LaTeX/Typst 原生引用系统
- **支持格式**: BibTeX, BibLaTeX

#### Editor
- **技术栈**: 
  - Web 前端 (React)
  - SwiftLaTeX WASM (浏览器内编译)
  - Yjs CRDT (实时协作)
  - WebRTC (点对点同步)
- **可独立嵌入**: ✅ 是，Web 应用

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
  - ✅ 技术栈可参考: Yjs CRDT、WebRTC、SwiftLaTeX WASM
  - ❌ 不能直接 Fork 用于闭源产品

---

### 2.3 Oleafly

**官方仓库**: https://github.com/Oleafly/Oleafly  
**许可证文件**: LICENSE (仓库根目录)  
**证据文件**: `evidence/OLEAFLY_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API 核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~842 stars
- **维护活跃度**: 超活跃，持续开发中

#### 许可证
- **SPDX 标识**: AGPL-3.0（GitHub API 确认 spdx_id: "AGPL-3.0"）
- **许可证文件路径**: `LICENSE`
- **双许可/附加条款**: 无
- **CLA**: 未要求
- **来源**: 一手来源 — GitHub API 直接获取

#### 源码结构
```
Oleafly/
├── src-tauri/                    # Rust 后端 (Tauri)
│   ├── crates/                   # 20 个 Rust crate
│   └── resources/
├── src/                          # React + TypeScript 前端
├── docs/
├── Cargo.toml
├── package.json
└── ...
```

#### Document Schema
- **文档模型**: LaTeX/Typst/Markdown 源码 (纯文本)
- **稳定性**: ✅ 稳定

#### Figure / Panel
- **原生支持**: ✅ Diagram Composer
- **特点**: 可视化图表编辑器，支持 TikZ, fletcher (Typst), Mermaid

#### Reference / Citation
- **实现方式**: Zotero 集成
- **支持格式**: BibTeX, BibLaTeX
- **特点**: 支持 arXiv, Semantic Scholar, Crossref, PubMed, OpenAlex 搜索

#### Editor
- **技术栈**: Tauri (Rust) + React + TypeScript
- **可独立嵌入**: ⚠️ 部分可以，需要剥离桌面应用层

#### Import / Export
- **支持格式**: LaTeX, Typst, Markdown, PDF, DOCX (通过 Pandoc)
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc，非原生)
- **特色功能**: Preflight 检查, 1700+ 模板库, AI agents 集成

#### 可复用性判定
- **分级**: **Reference-only** (仅参考)
- **理由**:
  - ❌ AGPL-3.0 与闭源分发不兼容
  - ✅ 技术架构可参考: Tauri + React + Rust, 本地优先, AI agents 集成

---

### 2.4 Manubot

**官方仓库**: https://github.com/manubot/manubot  
**许可证文件**: LICENSE.md (仓库根目录)  
**证据文件**: `evidence/MANUBOT_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API 核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2024 年有活动
- **Star 量级**: 中等规模
- **维护活跃度**: 低到中等，稳定维护

#### 许可证
- **SPDX 标识**: **BSD-2-Clause-Patent**
- **许可证文件路径**: `LICENSE.md`
- **Copyright**: Copyright © 2017–2020, Contributors & the Greene Lab at the University of Pennsylvania
- **关键条款摘录**:
  ```
  # BSD-2-Clause Plus Patent License
  
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
  
  1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  
  2. Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
  
  Subject to the terms and conditions of this license, each copyright holder
  and contributor hereby grants... a perpetual, worldwide, non-exclusive,
  no-charge, royalty-free, irrevocable... patent license...
  ```
- **双许可/附加条款**: ❌ 无（原报告称有 CC-BY-4.0/CC0-1.0 双许可，系错误）
- **CLA**: 未要求
- **来源**: 一手来源 — GitHub API 直接获取 LICENSE.md 原文

> **G1 修正说明**: 原报告将 Manubot 许可证误标为 "CC-BY-4.0 (文档) / CC0-1.0 (代码)" 双许可模式。经 GitHub API 获取的 LICENSE.md 原文确认，实际许可证为 **BSD-2-Clause Plus Patent License**。仓库中不存在 LICENSE-CC0.md 文件。

#### 源码结构
```
manubot/
├── manubot/                      # Python 包源码
│   ├── __init__.py
│   ├── cite.py                   # 引用管理
│   ├── process.py                # 文档处理
│   └── ai_revision.py            # AI 修订
├── tests/
├── setup.py
├── pyproject.toml
├── LICENSE.md                    # BSD-2-Clause-Patent
└── README.md
```

#### Document Schema
- **文档模型**: Markdown + YAML metadata
- **稳定性**: ✅ 稳定

#### Figure / Panel
- **原生支持**: ⚠️ 依赖 Pandoc 能力
- **编号解析**: ✅ 通过 Pandoc 交叉引用

#### Reference / Citation
- **实现方式**: Citation.js + 自动元数据检索
- **支持格式**: DOI, PubMed ID, arXiv ID, ISBN, URL, BibTeX
- **特点**: 自动解析持久标识符，支持数千种引用样式 (CSL)

#### Editor
- **技术栈**: 纯文本编辑器 + Git/GitHub
- **可独立嵌入**: ✅ 是，工具链可集成

#### Import / Export
- **支持格式**: Markdown (输入), HTML/PDF/DOCX (输出), BibTeX
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc)

#### 可复用性判定
- **分级**: **Adapt** (适配复用)
- **理由**:
  - ✅ **BSD-2-Clause-Patent 许可证**:
    - 允许商业使用、修改、分发
    - 允许闭源衍生作品
    - 义务仅为保留版权声明和免责声明
    - 包含明确的专利授权条款
  - ✅ **工具链可复用**: Python 包可独立使用，引用管理功能成熟
  - ⚠️ **局限性**: 无图形编辑器，依赖 Git/GitHub 工作流

> **G1 对低风险判定的影响**: BSD-2-Clause-Patent 的义务是保留版权声明与免责声明，比 CC-BY-4.0 的署名要求更轻量（无需标注作者姓名的特定方式），且额外提供专利授权。对闭源分发仍然友好。

---

### 2.5 Quarto

**官方仓库**: https://github.com/quarto-dev/quarto-cli  
**许可证文件**: COPYING.md (仓库根目录)  
**官方许可证页面**: https://quarto.org/license.html  
**证据文件**: `evidence/QUARTO_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API + 官方网站核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~2,646 stars
- **维护活跃度**: 超活跃，由 Posit 公司支持

#### 许可证
- **当前版本 (v1.4+)**: MIT
- **历史版本 (v1.3 及更早)**: GPL-2.0-only (GNU GPL v2)
- **许可证文件路径**: `COPYING.md`
- **Copyright**: Copyright (c) 2020-2024 Posit Software, PBC
- **关键条款摘录 (MIT)**:
  ```
  MIT License
  
  Copyright (c) 2020-2024 Posit Software, PBC
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction...
  ```
- **双许可/附加条款**: ⚠️ 版本差异 (v1.4 起改为 MIT)
- **CLA**: 未要求
- **来源**: 一手来源 — GitHub API 获取 COPYING.md + 官方网站 license.html

> **G3 说明**: Quarto 官方许可证页面 (https://quarto.org/license.html) 明确声明 "Quarto version 1.3 (and earlier) is licensed under the GNU GPL v2. Quarto version 1.4 is licensed under the MIT License." 原报告称 "GPL-2.0" 与官方表述 "GNU GPL v2" 一致。但 **变更的具体 commit SHA 未能核实**（GitHub API 访问受限），因此无法提供 commit 级证据。方向性结论可靠：旧版本曾为 copyleft (GPL-2.0)，v1.4 起改为 MIT。

#### 源码结构
```
quarto-cli/
├── src/                          # TypeScript/Deno 源码
│   ├── core/
│   ├── command/
│   └── ...
├── tests/
├── package.json
├── deno.json
├── COPYING.md                    # MIT License
└── ...
```

#### Document Schema
- **文档模型**: Pandoc Markdown 扩展
- **稳定性**: ✅ 非常稳定

#### Figure / Panel
- **原生支持**: ✅ 完整支持（子图、布局面板、图表代码嵌入）
- **编号解析**: ✅ 自动编号和交叉引用 (@fig, @tbl, @eq, @sec)

#### Reference / Citation
- **实现方式**: Pandoc citeproc + BibTeX
- **支持格式**: BibTeX, CSL JSON, DOI

#### Editor
- **技术栈**: 无专有编辑器，支持 JupyterLab, RStudio, VS Code
- **可独立嵌入**: ✅ 是，工具链可集成

#### Import / Export
- **支持格式**: Markdown, Jupyter, R Markdown → HTML, PDF, DOCX, Beamer, 网站, 书籍
- **DOCX Track Changes**: ⚠️ 有限支持 (通过 Pandoc)

#### 依赖组件许可证

| 组件 | 许可证 | 来源 |
|------|--------|------|
| Pandoc | GPL-2.0 | https://github.com/jgm/pandoc/blob/master/COPYING.md |
| Bootstrap 5 | MIT | https://github.com/twbs/bootstrap/blob/main/LICENSE |
| Deno | MIT | https://github.com/denoland/deno/blob/main/LICENSE.md |
| esbuild | MIT | https://github.com/evanw/esbuild/blob/master/LICENSE.md |
| Typst | Apache-2.0 | https://github.com/typst/typst/blob/main/LICENSE |

> **注意**: Quarto 依赖 Pandoc (GPL-2.0)。即使 Quarto 本身为 MIT，通过 Pandoc 进行文档转换时可能触发 GPL 条款。需法务确认此依赖关系对闭源分发的影响。

#### 可复用性判定
- **分级**: **Fork/Adapt** (可 Fork 或适配)
- **理由**:
  - ✅ MIT 许可证 (v1.4+)，无 copyleft 限制
  - ✅ 功能最全面，社区最活跃
  - ⚠️ 需确认 Pandoc (GPL-2.0) 依赖对闭源分发的影响

---

### 2.6 Typst

**官方仓库**: https://github.com/typst/typst  
**许可证文件**: LICENSE (仓库根目录)  
**证据文件**: `evidence/TYPST_LICENSE_EVIDENCE.md`  
**访问状态**: ✅ 已通过 GitHub API 核实

#### 基本信息
- **默认分支**: main
- **最近提交**: 2026 年超活跃
- **Star 量级**: ~51,702 stars
- **维护活跃度**: 超活跃，快速发展中

#### 许可证
- **SPDX 标识**: Apache-2.0（GitHub API 确认 spdx_id: "Apache-2.0"）
- **许可证文件路径**: `LICENSE`
- **来源**: 一手来源 — GitHub API 直接获取

#### 源码结构
```
typst/
├── crates/
│   ├── typst/                    # 主编译器门面
│   ├── typst-syntax/             # 语法解析
│   ├── typst-eval/               # AST 解释器
│   ├── typst-realize/            # Show 规则应用
│   ├── typst-layout/             # 布局引擎
│   ├── typst-library/            # 标准库
│   ├── typst-pdf/                # PDF 导出
│   ├── typst-svg/                # SVG 导出
│   ├── typst-html/               # HTML 导出
│   ├── typst-render/             # 内置渲染器
│   ├── typst-ide/                # IDE 功能
│   └── typst-cli/                # 命令行接口
├── docs/
├── tests/
└── tools/
```

#### Document Schema
- **文档模型**: 自有标记语言 (Typst syntax)
- **稳定性**: ✅ 稳定，但仍在快速演进

#### Figure / Panel
- **原生支持**: ✅ 完整支持（图表、子图、布局控制）
- **编号解析**: ✅ 自动编号和交叉引用

#### Reference / Citation
- **实现方式**: 内置引用系统 (hayagriva)
- **支持格式**: BibTeX, YAML 参考文献

#### Import / Export
- **支持格式**: Typst (输入) → PDF, SVG, PNG, HTML (输出)
- **DOCX**: ❌ 不支持

#### 可复用性判定
- **分级**: **Reference** (参考实现)
- **理由**:
  - ✅ Apache-2.0，允许商业使用和闭源衍生
  - ✅ Rust 实现，增量编译架构先进
  - ⚠️ 自有语法，不兼容 Markdown，无 DOCX 支持

---

### 2.7 TeXMind

**官方仓库**: **未能核实**  
**证据文件**: `evidence/TEXMIND_LICENSE_EVIDENCE.md`  
**访问状态**: ❌ 未能找到可验证的开源项目

#### 核实尝试
- GitHub 搜索 "TeXMind scientific writing"
- GitHub 搜索 "TeXMind editor"
- Web 搜索 "TeXMind LaTeX"
- 结果: 仅找到 "TexMind" 商业纺织软件，与科学写作无关

#### 结论
**未能核实** - 该项目可能不存在、已删除、未开源或名称有误。

---

## 3. 许可证风险汇总

### 3.1 高风险 (AGPL-3.0)

**涉及项目**: TeXlyre, Oleafly

**风险说明**:
- ❌ 不能用于闭源商业产品
- ❌ 不能作为 SaaS 后端而不公开源代码
- ❌ 网络服务条款要求向用户提供源代码
- ⚠️ 需要法律评估是否构成"衍生作品"

**建议**: 仅作为参考和学习对象；如需使用其技术，需独立重新实现。

### 3.2 中风险 (GPL-2.0)

**涉及项目**: Quarto (v1.3 及更早版本), Pandoc (Quarto 依赖)

**风险说明**:
- ❌ GPL-2.0 代码不能与闭源产品链接
- ⚠️ Quarto v1.4+ 已改为 MIT，但依赖 Pandoc (GPL-2.0)
- ⚠️ 通过 Pandoc 进行文档转换是否触发 GPL 传染需法务确认

**建议**: 使用 Quarto v1.4+；评估 Pandoc 依赖的合规风险。

### 3.3 低风险 (MIT, Apache-2.0, BSD-2-Clause-Patent)

**涉及项目**: Curvenote Editor (MIT), Manubot (BSD-2-Clause-Patent), Quarto v1.4+ (MIT), Typst (Apache-2.0)

**风险说明**:
- ✅ 允许商业使用和闭源衍生
- ✅ 无 copyleft 限制

**义务差异**:

| 许可证 | 核心义务 | 专利条款 |
|--------|---------|---------|
| MIT | 保留版权声明 | 无 |
| BSD-2-Clause-Patent | 保留版权声明 + 免责声明 | ✅ 明确专利授权 |
| Apache-2.0 | 保留版权声明 + 声明修改 + NOTICE 文件 | ✅ 明确专利授权 |

> **G1 修正**: 原报告将 Manubot 归入 "CC-BY-4.0" 类低风险，其义务描述为"署名"。实际上 BSD-2-Clause-Patent 的义务是保留版权声明和免责声明，比 CC-BY-4.0 更轻量，且额外提供专利授权。

---

## 4. 许可证兼容矩阵

> **G2 修正**: 原矩阵存在多处事实错误。以下为修订版，逐格给出依据。

### 前提声明
- 本矩阵评估的是**单向兼容**：左侧许可证的项目能否包含/链接右侧许可证的代码
- "✅" = 兼容（有明确依据）
- "❌" = 不兼容（有明确依据）
- "⚠️ 需法务确认" = 存在争议或无定论
- 评估基于闭源分发前提

| 本项目 → 依赖 ↓ | MIT | BSD-2-Clause-Patent | Apache-2.0 | GPL-2.0-only | GPL-3.0-only | AGPL-3.0 |
|---|---|---|---|---|---|---|
| **MIT (闭源)** | ✅ 同许可 | ✅ 宽松→宽松 | ✅ 宽松→宽松 | ❌ GPL copyleft 传染 | ❌ GPL copyleft 传染 | ❌ AGPL copyleft 传染 |
| **BSD-2-Clause-Patent (闭源)** | ✅ 宽松→宽松 | ✅ 同许可 | ✅ 宽松→宽松 | ❌ GPL copyleft 传染 | ❌ GPL copyleft 传染 | ❌ AGPL copyleft 传染 |
| **Apache-2.0 (闭源)** | ✅ 宽松→宽松 | ✅ 宽松→宽松 | ✅ 同许可 | ❌ GPL-2.0 不兼容 Apache-2.0 (FSF 立场) | ✅ Apache-2.0→GPL-3.0 单向兼容 (FSF 确认) | ❌ AGPL copyleft 传染 |
| **GPL-2.0-only** | ✅ GPL 可包含宽松代码 | ✅ GPL 可包含宽松代码 | ❌ GPL-2.0 不兼容 Apache-2.0 (FSF 立场) | ✅ 同许可 | ⚠️ 需法务确认 (GPL-2.0→GPL-3.0 升级条款存在争议) | ❌ GPL-2.0 与 AGPL-3.0 不兼容 |
| **GPL-3.0-only** | ✅ GPL 可包含宽松代码 | ✅ GPL 可包含宽松代码 | ✅ Apache-2.0→GPL-3.0 单向兼容 | ⚠️ 需法务确认 | ✅ 同许可 | ✅ GPL-3.0 与 AGPL-3.0 兼容 |
| **AGPL-3.0** | ✅ AGPL 可包含宽松代码 | ✅ AGPL 可包含宽松代码 | ✅ Apache-2.0→AGPL-3.0 兼容 (通过 GPL-3.0) | ❌ GPL-2.0 与 AGPL-3.0 不兼容 | ✅ GPL-3.0 与 AGPL-3.0 兼容 | ✅ 同许可 |
| **闭源 ( proprietary )** | ✅ 宽松许可允许闭源 | ✅ 宽松许可允许闭源 | ✅ 宽松许可允许闭源 | ❌ GPL 不允许闭源 | ❌ GPL 不允许闭源 | ❌ AGPL 不允许闭源 |

### 依据来源

| 判定 | 依据 |
|------|------|
| Apache-2.0 × GPL-2.0 = ❌ | FSF 官方立场: https://www.gnu.org/licenses/license-list.en.html#apache2 — Apache 2.0 与 GPL-2.0 不兼容 |
| Apache-2.0 × GPL-3.0 = ✅ | FSF 官方立场: Apache 2.0 与 GPL-3.0 单向兼容 |
| GPL-2.0 × AGPL-3.0 = ❌ | GPL-2.0-only 与 AGPL-3.0 不兼容（不同 major 版本的 GPL 系列） |
| GPL-3.0 × AGPL-3.0 = ✅ | GPL-3.0 第13条明确允许与 AGPL-3.0 组合 |
| AGPL-3.0 行不全 ✅ | 原报告 AGPL 整行全 ✅ 系错误；AGPL 仍受 GPL 系列兼容性约束 |

> **G2 修正总结**: 
> 1. `GPL-2.0 × Apache-2.0` 由原报告的 ✅ 更正为 ❌（FSF 确认不兼容）
> 2. `AGPL-3.0` 行由原报告的全 ✅ 更正为存在 ❌ 格子
> 3. `CC-BY-4.0 × GPL` 行已删除（CC 许可证不适用于软件，不应出现在软件兼容矩阵中）
> 4. 新增 BSD-2-Clause-Patent 列

---

## 5. 可复用性分级

### 5.1 Fork (可直接 Fork)

**项目**: Quarto (v1.4+)

**理由**: MIT 许可证，功能最全面，Posit 公司支持  
**风险**: ⚠️ Pandoc (GPL-2.0) 依赖的合规性需法务确认

### 5.2 Adapt (适配复用)

**项目**: Curvenote Editor, Manubot

- **Curvenote Editor**: MIT，ProseMirror 编辑器核心可提取
- **Manubot**: BSD-2-Clause-Patent，Python 工具链和引用管理可复用

### 5.3 Reference (仅参考)

**项目**: TeXlyre, Oleafly, Typst

- **TeXlyre / Oleafly**: AGPL-3.0，与闭源分发不兼容
- **Typst**: Apache-2.0，但自有语法不兼容 Markdown

### 5.4 未能核实

**项目**: TeXMind

---

## 6. 与本项目的匹配度分析

### 6.1 匹配度评分

| 项目 | 许可证兼容性 | 功能匹配度 | 技术可复用性 | 维护成本 | 综合评分 |
|------|-------------|-----------|-------------|---------|---------|
| **Quarto** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **A-** |
| **Curvenote** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | **B+** |
| **Manubot** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **B** |
| **Typst** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **B-** |
| **Oleafly** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | **C** |
| **TeXlyre** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | **C-** |
| **TeXMind** | ❓ | ❓ | ❓ | ❓ | **未能核实** |

> **Quarto 评分由 A 降为 A-**: 因 Pandoc (GPL-2.0) 依赖的合规风险尚未确认。

---

## 7. 信息来源

> **G6 修正**: 原报告大量引用 CSDN 博客、微博等二手来源。修订版优先使用一手来源。

### 一手来源 (Primary Sources)

| 项目 | 来源 | URL |
|------|------|-----|
| Curvenote Editor | GitHub 仓库 LICENSE 文件 | https://github.com/curvenote/editor/blob/main/LICENSE |
| TeXlyre | GitHub 仓库 LICENSE 文件 | https://github.com/TeXlyre/texlyre/blob/main/LICENSE |
| Oleafly | GitHub 仓库 LICENSE 文件 | https://github.com/Oleafly/Oleafly/blob/main/LICENSE |
| Manubot | GitHub 仓库 LICENSE.md 文件 | https://github.com/manubot/manubot/blob/main/LICENSE.md |
| Quarto | GitHub 仓库 COPYING.md 文件 | https://github.com/quarto-dev/quarto-cli/blob/main/COPYING.md |
| Quarto | 官方许可证页面 | https://quarto.org/license.html |
| Typst | GitHub 仓库 LICENSE 文件 | https://github.com/typst/typst/blob/main/LICENSE |
| 许可证兼容性 | FSF 许可证列表 | https://www.gnu.org/licenses/license-list.en.html |
| 许可证兼容性 | SPDX 许可证列表 | https://spdx.org/licenses/ |
| 许可证兼容性 | Apache-2.0 与 GPL 兼容性 | https://www.apache.org/licenses/GPL-compatibility.html |

### 二手来源 (Secondary Sources)

> 以下来源仅在无法获取一手来源时引用，并已标注。

| 来源 | 类型 | 引用内容 | 标注 |
|------|------|---------|------|
| CSDN 博客 | 二手 | 已移除或替换为一手来源 | ⚠️ 原报告引用，修订版已替换 |
| 微博 | 二手 | 已移除 | ⚠️ 原报告引用，修订版已移除 |
| tool.lu | 二手 | 已移除 | ⚠️ 原报告引用，修订版已移除 |

---

## 8. 证据清单

### 8.1 证据文件

| 项目 | 证据文件 | 来源类型 |
|------|---------|---------|
| Curvenote Editor | `evidence/CURVENOTE_LICENSE_EVIDENCE.md` | GitHub API (一手) |
| TeXlyre | `evidence/TEXLYRE_LICENSE_EVIDENCE.md` | GitHub API (一手) |
| Oleafly | `evidence/OLEAFLY_LICENSE_EVIDENCE.md` | GitHub API (一手) |
| Manubot | `evidence/MANUBOT_LICENSE_EVIDENCE.md` | GitHub API (一手) |
| Quarto | `evidence/QUARTO_LICENSE_EVIDENCE.md` | GitHub API + 官方网站 (一手) |
| Typst | `evidence/TYPST_LICENSE_EVIDENCE.md` | GitHub API (一手) |
| TeXMind | `evidence/TEXMIND_LICENSE_EVIDENCE.md` | 多次搜索未果 |

### 8.2 访问日期
**审计日期**: 2026-11-06  
**修订日期**: 2026-11-06

### 8.3 未能核实事项

| 事项 | 状态 | 说明 |
|------|------|------|
| TeXMind 项目 | ❌ 未找到 | 多次搜索未果 |
| Quarto GPL→MIT 变更 commit SHA | ⚠️ 未能获取 | GitHub API 访问受限 |
| 各项目的最新 commit SHA | ⚠️ 未能获取 | GitHub API 访问受限 |
| Pandoc 依赖对 Quarto 闭源分发的影响 | ⚠️ 需法务确认 | GPL-2.0 依赖的传染范围 |
| 各项目的 DOCX Track Changes 实际测试 | ❌ 未测试 | 需实际测试验证 |

---

## 附录: 术语表

- **SPDX**: Software Package Data Exchange，软件包数据交换标准
- **AST**: Abstract Syntax Tree，抽象语法树
- **CRDT**: Conflict-free Replicated Data Type，无冲突复制数据类型
- **WYSIWYG**: What You See Is What You Get，所见即所得
- **SaaS**: Software as a Service，软件即服务
- **CLA**: Contributor License Agreement，贡献者许可协议
- **Copyleft**: 著作权左派，要求衍生作品使用相同许可证
- **CSL**: Citation Style Language，引用样式语言
- **DOI**: Digital Object Identifier，数字对象标识符
- **FSF**: Free Software Foundation，自由软件基金会

---

**文档版本**: 2.0 (修订版)  
**最后更新**: 2026-11-06  
**审计状态**: 修订完成 (6/7 项目已核实，1 项未能核实)  
**QA 修复状态**: G1-G6 全部已处理
