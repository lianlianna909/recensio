# TASK: 修订轮 — 开源审计证据与许可证修复

## 0. 背景

独立 QA 判定 `research/open-source-audit/OPEN_SOURCE_AUDIT.md` 为 RISK：Manubot 许可证识别错误、兼容矩阵存在事实错误、Quarto 历史许可证引文不可核验、全篇无证据快照。

## 1. 交付物

1. `research/open-source-audit/OPEN_SOURCE_AUDIT.md` — 就地修订
2. `research/open-source-audit/evidence/` — 每个项目的许可证原文摘录 + 仓库 URL + 访问日期 + commit SHA（若能取得）
3. `research/open-source-audit/EVIDENCE_FIX_LOG.md` — 逐条修复记录

## 2. 必须修复的具体问题

### G1 Manubot 许可证错误
现写「CC-BY-4.0 / CC0-1.0」，QA 外部复核为 **BSD-2-Clause Plus Patent**。
**要求**：核实并更正；同时修正「低风险」一节的依据（BSD 的义务是保留版权声明与免责声明，不是 CC-BY 的署名）。

### G2 许可证兼容矩阵错误
现矩阵把 `GPL-2.0 × Apache-2.0` 标为 ✅（业界公认不兼容，Apache-2.0 仅与 GPL-3.0 单向兼容），`CC-BY-4.0 × GPL` 同样存疑，AGPL 整行全 ✅。
**要求**：重做矩阵，逐格给出依据；无法确定的格子标「需法务确认」，不得臆断。

### G3 Quarto 历史许可证版本存疑
现称「v1.3 及更早为 GPL-2.0」，但所引 LICENSE 无此文本，仓库历史线索指向 GPL v3。
**要求**：给出 commit 级证据（commit SHA + 文件路径）；拿不到就删除版本号断言，只保留「旧版本曾为 copyleft」这一方向性结论并标注不可核验。

### G4 全篇无证据快照
Obsidian 报告有 `evidence/` 目录与文件指纹，本报告没有。
**要求**：建立 `evidence/`，每个项目至少一份：LICENSE 原文关键段落、仓库 URL、访问日期。

### G5 「闭源」前提未声明
兼容矩阵与可复用性判定都建立在「本项目可能闭源分发」上，但没有任何决策文档确立该前提。
**要求**：在报告开头显式声明前提，并说明若改为开源（如 MIT）结论会如何变化。

### G6 来源多为二手
现报告多处引用 CSDN / 微博 / 博客。
**要求**：一手来源（官方仓库、LICENSE、官方文档）优先；确实只能二手的，标注「二手来源」。

## 3. 硬性约束

- 只改 `research/open-source-audit/` 下文件。
- 不得修改其他 Worker 目录、`research/architecture/`、`decisions/`、`AGENTS.md`。
- **不得编造仓库 URL、许可证或 commit SHA。** 拿不到证据就写「未能核实」。
- 不得替项目做最终选型。

## 4. 完成标准

- G1–G6 全部有处理记录
- 兼容矩阵每格有依据或标「需法务确认」
- 7 个项目均有 evidence 文件
- 报告开头有明确的分发形态前提声明

## 5. 交付方式

≤600 字总结 + 文件清单 + Manubot 与 Quarto 两条的最终结论。
