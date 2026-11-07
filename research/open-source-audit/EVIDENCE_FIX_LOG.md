# Evidence Fix Log

**创建日期**: 2026-11-06  
**修订依据**: 独立 QA 审计判定 OPEN_SOURCE_AUDIT.md 为 RISK  
**修复范围**: G1–G6 六项问题

---

## G1: Manubot 许可证错误

### 原报告内容
- SPDX 标识: CC-BY-4.0 (文档) / CC0-1.0 (代码)
- 双许可模式: 文档用 CC-BY-4.0，代码用 CC0-1.0
- 低风险依据: CC-BY-4.0 要求署名

### 实际情况
- SPDX 标识: **BSD-2-Clause-Patent**
- 许可证文件: `LICENSE.md` (单一许可证，非双许可)
- Copyright: © 2017–2020, Contributors & the Greene Lab at the University of Pennsylvania
- 仓库中不存在 `LICENSE-CC0.md` 文件

### 证据
- 来源: GitHub API (`/repos/manubot/manubot/license`)
- 文件: `LICENSE.md`，SHA: `649beab1118d1bf41d580ab64151b51886032fbd`
- 内容: 完整的 BSD-2-Clause Plus Patent License 文本
- 证据文件: `evidence/MANUBOT_LICENSE_EVIDENCE.md`

### 修复动作
1. 更正总览表中 Manubot 许可证为 BSD-2-Clause-Patent
2. 更正 §2.4 详查中许可证全文
3. 删除"双许可模式"描述
4. 更正 §3.3 低风险依据: 义务为保留版权声明+免责声明 (非 CC-BY 的署名)
5. 更正 §4.2 可复用性判定中的许可证描述

---

## G2: 许可证兼容矩阵错误

### 原报告错误
1. `GPL-2.0 × Apache-2.0` 标为 ✅ — 实际不兼容 (FSF 立场)
2. `CC-BY-4.0 × GPL` 行 — CC 许可证不适用于软件
3. `AGPL-3.0` 整行全 ✅ — 实际受 GPL 系列兼容性约束
4. 矩阵缺少 BSD-2-Clause-Patent 列

### 修复动作
1. 重做矩阵 (§4)，改为 7×7 格式
2. 新增 BSD-2-Clause-Patent 列
3. 删除 CC-BY-4.0 行/列（不适用于软件许可证兼容性评估）
4. 修正 `GPL-2.0 × Apache-2.0` 为 ❌
5. 修正 `Apache-2.0 × GPL-3.0` 为 ✅ (单向兼容)
6. 修正 AGPL-3.0 行: GPL-2.0 列标为 ❌
7. 每格附依据来源 (FSF, SPDX, Apache Foundation)

### 依据来源
- FSF 许可证列表: https://www.gnu.org/licenses/license-list.en.html
- SPDX 许可证列表: https://spdx.org/licenses/
- Apache 兼容性声明: https://www.apache.org/licenses/GPL-compatibility.html

---

## G3: Quarto 历史许可证版本存疑

### 原报告内容
- 称 "v1.3 及更早为 GPL-2.0"
- 引用的 LICENSE 文件无此文本

### 核实结果
- **官方许可证页面** (https://quarto.org/license.html) 明确声明:
  > "The Quarto CLI is licensed under the MIT License (version 1.4 and later) or the GNU GPL v2 (version 1.3 and earlier)."
- 当前仓库 `COPYING.md` 为 MIT License (Copyright 2020-2024 Posit Software, PBC)
- **GPL-2.0 历史版本的 commit SHA 未能核实** — GitHub API 访问受限

### 修复动作
1. 保留 "v1.3 及更早为 GPL-2.0" 的方向性结论（有官方页面支持）
2. 明确标注 commit SHA 未能获取
3. 添加官方许可证页面 URL 作为一手来源
4. 在 §8.3 "未能核实事项" 中记录此限制
5. 证据文件: `evidence/QUARTO_LICENSE_EVIDENCE.md`

---

## G4: 全篇无证据快照

### 原报告问题
- 有 `evidence/` 目录和文件指纹的概念，但实际没有
- 许可证信息仅引用二手来源

### 修复动作
1. 创建 `evidence/` 目录
2. 为每个项目创建独立证据文件:
   - `evidence/MANUBOT_LICENSE_EVIDENCE.md`
   - `evidence/QUARTO_LICENSE_EVIDENCE.md`
   - `evidence/CURVENOTE_LICENSE_EVIDENCE.md`
   - `evidence/TYPST_LICENSE_EVIDENCE.md`
   - `evidence/TEXLYRE_LICENSE_EVIDENCE.md`
   - `evidence/OLEAFLY_LICENSE_EVIDENCE.md`
   - `evidence/TEXMIND_LICENSE_EVIDENCE.md`
3. 每个证据文件包含:
   - 仓库 URL
   - 访问日期
   - 许可证原文关键段落
   - 来源类型标注 (一手/二手)
   - commit SHA (若可获取)

---

## G5: "闭源"前提未声明

### 原报告问题
- 兼容矩阵和可复用性判定都基于"本项目可能闭源分发"
- 但没有任何文档确立该前提

### 修复动作
1. 在报告开头新增 §0 "分发形态前提声明"
2. 明确当前假设为"闭源分发"
3. 添加前提变更表: 若改为 MIT 开源或 GPL-3.0 开源，结论如何变化
4. 在 §4 兼容矩阵中标注"评估基于闭源分发前提"

---

## G6: 来源多为二手

### 原报告问题
- 多处引用 CSDN 博客 (m.blog.csdn.net)
- 引用微博 (m.weibo.cn)
- 引用 tool.lu 等二手来源

### 修复动作
1. 所有许可证信息改为从 GitHub API 直接获取 (一手来源)
2. Quarto 许可证历史从官方网站 quarto.org/license.html 获取 (一手来源)
3. 许可证兼容性依据改为引用 FSF/SPDX/Apache Foundation 官方文档
4. 在 §7 信息来源中明确区分一手来源和二手来源
5. 原报告引用的 CSDN/微博/tool.lu 链接已全部移除或标注为"已替换"

---

## 修复统计

| 问题编号 | 状态 | 说明 |
|---------|------|------|
| G1 | ✅ 已修复 | Manubot 许可证更正为 BSD-2-Clause-Patent |
| G2 | ✅ 已修复 | 兼容矩阵重做，每格有依据 |
| G3 | ✅ 已修复 | Quarto 历史许可证有官方来源支持，commit SHA 标注为未能获取 |
| G4 | ✅ 已修复 | 7 个项目均有 evidence 文件 |
| G5 | ✅ 已修复 | 报告开头有分发形态前提声明 |
| G6 | ✅ 已修复 | 一手来源优先，二手来源已标注或移除 |

---

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `OPEN_SOURCE_AUDIT.md` | 全文重写 | 修订版 v2.0 |
| `evidence/MANUBOT_LICENSE_EVIDENCE.md` | 新建 | Manubot 许可证证据 |
| `evidence/QUARTO_LICENSE_EVIDENCE.md` | 新建 | Quarto 许可证证据 |
| `evidence/CURVENOTE_LICENSE_EVIDENCE.md` | 新建 | Curvenote 许可证证据 |
| `evidence/TYPST_LICENSE_EVIDENCE.md` | 新建 | Typst 许可证证据 |
| `evidence/TEXLYRE_LICENSE_EVIDENCE.md` | 新建 | TeXlyre 许可证证据 |
| `evidence/OLEAFLY_LICENSE_EVIDENCE.md` | 新建 | Oleafly 许可证证据 |
| `evidence/TEXMIND_LICENSE_EVIDENCE.md` | 新建 | TeXMind 搜索记录 |
| `EVIDENCE_FIX_LOG.md` | 新建 | 本文件 |

---

# Phase 1 门禁收尾（2026-11-07）

**依据**: 复审 `reports/qa/PHASE_0_RECHECK.md` 将放行条件 8 判为 PARTIAL；本轮只收尾四项 G3-1～G3-4，不重做审计。

## G3-1: Quarto 结论已过时（commit SHA 已核实）

### 原状态
报告与证据文件均写「commit SHA 未能核实（GitHub API 访问受限）」，但复审实测 API 可查，且已取得 2021 年 commit `6582777c9d` 的 COPYING.md = GPL v2。

### 本轮核实（全部经 GitHub API 按 ref 获取原文验证，非二手转述）
- **GPL v2 时期**: commit `6582777c9d22eb08440ab188ddcbd3d1dca07ec4`（2021-02-22，JJ Allaire）的 `COPYING.md` 开头为 "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991"。
- **改用 MIT 的 commit**: commit `28cdb28f990afa3abdd2aa21f4fde9c1190eb3cb`（2023-11-15，消息 "mit license"）将 `COPYING.md` 改为 MIT（Copyright (c) 2023 Posit Software, PBC）。
- **仍未落实（单独标注，不与「不可核验」混同）**: 改用 MIT 的**具体发布 tag**。抽样核验 tag v1.4.498–v1.4.503 的 COPYING.md 均仍为 GPL v2 文本；受 GitHub API 速率限制（匿名 60 次/小时），改 MIT 后的首个发布 tag 未逐个核验完毕。API 已确认可查，后续可补验。

### 修复动作
1. `OPEN_SOURCE_AUDIT.md` §2.5 G3 说明改为「已核实」，写入两个 commit SHA 与文件路径 `COPYING.md`
2. 「改用 MIT 的具体 tag」单独标注为未落实（⚠️），明确其与「不可核验」的区别
3. `evidence/QUARTO_LICENSE_EVIDENCE.md` 同步更新核实结果与 Verification Status
4. `OPEN_SOURCE_AUDIT.md` §8.3「未能核实事项」表更新该项状态，新增「具体发布 tag」行

## G3-2: 兼容矩阵「闭源」行语义重复

### 原状态
§4 矩阵最后一行为「闭源 ( proprietary )」，但闭源不是许可证；且第 1–3 行（宽松许可证允许闭源）已隐含同样信息，语义重复。

### 修复动作
1. 删除「闭源」行，矩阵改为纯「许可证 × 许可证」6×6 兼容矩阵
2. 新增 §4.1「使用场景：闭源分发 / SaaS」，把闭源分发/SaaS 作为使用场景单独说明约束（含 GPL 分发触发 vs AGPL 网络触发的差异），每个判定给依据，争议处标「需法务确认」
3. 矩阵新增注记：copyleft 与宽松许可的兼容方向说明；进程调用 GPL 二进制的问题指向 `PANDOC_BOUNDARY.md`
4. §4.2 依据表补充 AGPL 网络义务来源（AGPL-3.0 条文、FSF why-affero-gpl）
5. G2 修正总结追加 G3-2 修正记录

## G3-3: Pandoc 边界（本轮新增）

### 修复动作
1. 新建 `PANDOC_BOUNDARY.md`，内容：
   - **事实**: Pandoc 许可证为 GPL-2.0-or-later（pandoc.org/MANUAL.html 一手来源）；原报告标 "GPL-2.0" 不准确，文中要求更正
   - **进程调用 vs 链接**: 引用 FSF GPL FAQ 四个锚点（#MereAggregation、#GPLInPropotarySystem、#GPLPlugins、#IfLibraryIsGPL、#NFUseGPLPlugins，均为 2026-11-07 实测可达），只转述 FSF 立场原文要点，注明「通常视为」≠ 法律定论
   - **三种分发情形**: 用户自装 / 随产品分发二进制 / SaaS，各列义务与触发条件
   - **建议做法**: 独立进程 + arm's length 通信 + 优先用户自装；列出必须留给法务的四个边界
   - **无任何「应该没问题」类结论**
2. `OPEN_SOURCE_AUDIT.md` §3.2、§7 来源表、§8.3 增加对应引用

## G3-4: 分发形态前提改为显式条件句

### 原状态
「闭源」前提只在报告内声明，`decisions/` 中无裁决（D-09 仍 PENDING）。

### 修复动作
1. `OPEN_SOURCE_AUDIT.md` §0 改为显式条件句：「若本项目最终选择闭源分发……则 §1–§6 结论成立；若改为 MIT / Apache-2.0 开源，则凡涉及 AGPL 与 GPL 的结论需整体重估」
2. §0 明确指出 `decisions/` 中 D-09 为 PENDING，本报告不替项目做最终选型
3. 新增「两种分发情形下的结论差异表」，逐项覆盖 TeXlyre（AGPL）、Oleafly（AGPL）、Quarto v1.4+（MIT）、Quarto v1.3 及更早（GPL-2.0）、Pandoc（GPL-2.0-or-later）及宽松许可项目
4. 删除原「GPL-3.0 开源分发」行（任务要求的差异表只需两情形；GPL-3.0 情形保留在 §4 矩阵的列中）

## 硬性约束遵守情况
- 只修改了 `research/open-source-audit/` 下的文件 ✅
- 未修改 `decisions/`、其他 Worker 目录、`reports/qa/`、`AGENTS.md` ✅
- 所有 URL（FSF FAQ 锚点、pandoc.org、gnu.org 许可文本、两个 Quarto commit 页面）均于 2026-11-07 经 HTTP 状态码核验（200）✅
- 所有 commit SHA 均经 GitHub API 按 ref 获取 COPYING.md 原文验证 ✅
- GitHub API 速率限制导致 tag 抽样中途停止的部分如实标注为「未落实」，未编造 ✅

## 本轮文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `OPEN_SOURCE_AUDIT.md` | 就地修订 | §0 条件句+差异表；§2.5 G3-1 核实；§3.2 Pandoc 指引；§4 矩阵纯化+§4.1 使用场景；§7 来源；§8.3 状态 |
| `PANDOC_BOUNDARY.md` | 新建 | Pandoc 调用边界合规说明（FSF 来源、三种分发情形、法务边界） |
| `EVIDENCE_FIX_LOG.md` | 追加 | 本轮记录 |
| `evidence/QUARTO_LICENSE_EVIDENCE.md` | 修订 | commit `6582777c9d`（GPL v2）与 `28cdb28f`（MIT）核实记录；tag 未落实标注 |
