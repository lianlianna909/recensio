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
