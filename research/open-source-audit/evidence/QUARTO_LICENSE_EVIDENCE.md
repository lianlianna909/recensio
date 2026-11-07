# Quarto License Evidence

**Project**: Quarto CLI  
**Repository**: https://github.com/quarto-dev/quarto-cli  
**Access Date**: 2026-11-06  
**License File**: COPYING.md  
**Source**: GitHub API (primary source) + Official website (primary source)

## Current License (v1.4+)
**SPDX Identifier**: MIT

## Historical License (v1.3 and earlier)
**SPDX Identifier**: GPL-2.0-only (GNU GPL v2)

## Official Statement

From https://quarto.org/license.html (accessed 2026-11-06):

> The Quarto CLI is licensed under the MIT License (version 1.4 and later) or the GNU GPL v2 (version 1.3 and earlier).

## Current License Text (MIT, from COPYING.md)

```
MIT License

Copyright (c) 2020-2024 Posit Software, PBC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Historical License (GPL-2.0)

**注意**: v1.3 及更早版本使用 GPL-2.0，这是 copyleft 许可证。  
**变更时间**: v1.4 起改为 MIT  

### G3-1 核实结果（2026-11-07 更新）

- **GPL v2 时期证据（已核实）**:
  - Commit SHA: `6582777c9d22eb08440ab188ddcbd3d1dca07ec4`（2021-02-22，作者 JJ Allaire，消息 "run deno fmt"）
  - 文件路径: `COPYING.md`
  - 核实方式: GitHub API 按 ref 获取原文（`/repos/quarto-dev/quarto-cli/contents/COPYING.md?ref=6582777c9d...`），文件开头为 "### GNU GENERAL PUBLIC LICENSE / Version 2, June 1991"
  - Commit 页面: https://github.com/quarto-dev/quarto-cli/commit/6582777c9d22eb08440ab188ddcbd3d1dca07ec4
- **改用 MIT 的 commit（已核实）**:
  - Commit SHA: `28cdb28f990afa3abdd2aa21f4fde9c1190eb3cb`（2023-11-15，消息 "mit license"）
  - 文件路径: `COPYING.md`（同时修改 COPYRIGHT、README.md 等）
  - 核实方式: GitHub API 按 ref 获取原文，文件开头为 "MIT License / Copyright (c) 2023 Posit Software, PBC"
  - Commit 页面: https://github.com/quarto-dev/quarto-cli/commit/28cdb28f990afa3abdd2aa21f4fde9c1190eb3cb
- **仍未落实（单独标注，非「不可核验」）**:
  - 「改用 MIT 的**具体发布 tag**」：抽样核验 tag v1.4.498 / v1.4.499 / v1.4.500 / v1.4.501 / v1.4.502 / v1.4.503 的 COPYING.md 均仍为 GPL v2 文本；受 GitHub API 速率限制（未认证 60 次/小时），改 MIT 后的首个发布 tag 未逐个核验完毕。API 本身可查，后续可补验。
  - 注：commit `28cdb28f`（2023-11-15）晚于 v1.3 系列的发布期，与官方「v1.3 及更早为 GPL v2，v1.4 为 MIT」的声明一致；但 v1.4 早期 tag 的 COPYING.md 状态与该 commit 的关系需后续核验。

## Key Obligations (MIT)

- **保留版权声明**: Must include copyright notice
- **无 copyleft**: Permissive, allows proprietary derivatives
- **专利条款**: No explicit patent grant (unlike Apache-2.0)

## Dependencies with Different Licenses

From official license page:
- Pandoc: GPL-2.0
- Bootstrap 5: MIT
- Deno: MIT
- esbuild: MIT
- Dart Sass: MIT
- Typst: Apache-2.0

## Verification Status
✅ 已通过 GitHub API 获取 COPYING.md 原文  
✅ 已通过官方网站 https://quarto.org/license.html 验证许可证历史  
✅ G3-1（2026-11-07）: commit `6582777c9d`（GPL v2）与 commit `28cdb28f`（改 MIT）均已按 ref 核实原文  
⚠️ 改用 MIT 后的首个发布 tag 未逐个核验（API 速率限制，非不可核验）
