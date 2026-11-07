# TASK: Phase 1 门禁 — 开源审计收尾（条件 8）

## 0. 背景

复审 `reports/qa/PHASE_0_RECHECK.md` 把放行条件 8 判为 PARTIAL：Manubot 许可证、兼容矩阵、Quarto 版本三项已实质达成，但仍有四处未闭环。本轮只收尾，不重做审计。

## 1. 交付物

1. `research/open-source-audit/OPEN_SOURCE_AUDIT.md` — 就地修订
2. `research/open-source-audit/PANDOC_BOUNDARY.md` — Pandoc 调用边界的合规说明
3. `research/open-source-audit/EVIDENCE_FIX_LOG.md` — 追加本轮记录

## 2. 必须关闭的条目

### G3-1 Quarto 结论已过时
报告与证据文件仍写「commit SHA 未能核实（API 访问受限）」，但复审实测 API 可查，且已取得 2021 年 commit `6582777c9d` 的 COPYING.md = GPL **v2**。
**要求**：更新为「已核实」并写入 commit SHA 与文件路径；仍缺的「改用 MIT 的具体 tag」单独标注为未落实，不要与「不可核验」混为一谈。

### G3-2 兼容矩阵的「闭源」行语义重复
§3.4 矩阵把「闭源」当作行/列标签，但闭源不是许可证；第 1–3 行与最后一行语义重复。
**要求**：把矩阵改为「许可证 × 许可证」的纯兼容矩阵，把「闭源分发 / SaaS」作为**使用场景**另设一节说明其约束，不要在矩阵里当许可证用。每个格子给依据，拿不准的标「需法务确认」。

### G3-3 Pandoc 边界（本轮新增，必须做）
Pandoc 是 GPL-2.0-or-later。本项目计划以**独立进程**调用它做导出。
**要求**：写 `PANDOC_BOUNDARY.md`，明确：
1. 进程级调用（fork/exec 独立二进制）与链接/嵌入的法律差异，引用 FSF 的官方立场来源（URL）；
2. 分发形态的三种情形（用户自装 / 随产品分发二进制 / SaaS 调用）各自的义务；
3. 本项目建议的做法与「需法务确认」的边界。
**不得**给出「应该没问题」这类结论；只给事实、来源、条件。

### G3-4 分发形态前提
复审指出「闭源」前提只在报告内声明，`decisions/` 中无裁决（D-09 仍 PENDING）。
**要求**：在报告开头把该前提改为**显式条件句**——「若最终选择闭源分发，则以下结论成立；若改为 MIT/Apache 开源，则 AGPL 项的结论需整体重估，具体变化为……」。给出两种情形下结论的差异表（至少覆盖 TeXlyre/Oleafly 的 AGPL、Quarto 的 GPL、Pandoc 的 GPL）。

## 3. 硬性约束

- 只改 `research/open-source-audit/` 下文件。
- 不得编造 URL / commit SHA / 许可证。拿不到就写「未能核实」。
- 不得替项目做最终选型；不得修改 `decisions/`。
- 不得修改其他 Worker 目录、`reports/qa/`、`AGENTS.md`。

## 4. 完成标准

- G3-1…G3-4 全部有处理记录
- 矩阵中不再有非许可证标签
- `PANDOC_BOUNDARY.md` 有 FSF 来源 URL 与三种分发情形的义务说明
- 开头有条件句与两情形差异表

## 5. 交付方式

≤500 字总结 + 文件清单 + Pandoc 结论一句话。
