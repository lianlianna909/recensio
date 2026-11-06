# TASK: Worker D - Open-source Researcher

## 0. 角色与项目背景

你是 ScientificWritingProject 的 Open-source Researcher。项目要决定"从哪些开源项目借鉴、复用、Fork 或仅作参考"。本任务只做证据调查，不做选型承诺。

## 1. 唯一交付物

在工作区根目录创建：

`research/open-source-audit/OPEN_SOURCE_AUDIT.md`

允许在同目录附带证据材料（如许可证原文摘录）。除此之外不得写任何文件。

## 2. 必查项目（7 个，一个不能少）

1. Curvenote Editor
2. TeXlyre
3. Oleafly
4. TeXMind
5. Manubot
6. Quarto
7. Typst

对每个项目必须核查并记录：
- **官方仓库**：真实 URL、默认分支、最近一次提交时间、star 量级、维护活跃度（近 6 个月提交频率）。
- **许可证**：SPDX 标识、许可证文件路径、是否存在双许可 / 附加条款 / CLA。**必须引用许可证文件原文关键段落**，不能只写"MIT"。
- **源码结构**：顶层目录职责，核心包/模块划分。
- **Document Schema**：它的文档模型是什么（AST / JSON schema / Markdown 扩展语法），是否对外稳定。
- **Figure / Panel**：是否原生支持多面板图与编号解析。
- **Reference / Citation**：引用实现方式（CSL？bibtex？自有格式）。
- **Editor**：编辑器技术栈（ProseMirror / CodeMirror / 自研），是否可独立嵌入。
- **Import / Export**：支持哪些格式，DOCX 支持程度（尤其 Track Changes）。
- **可复用性判定**：Fork / Adapt / Reference-only / 不可用，并给出理由。

## 3. 硬性约束

- **必须基于真实访问结果**。无法访问或无法核实的项目，明确写"未能核实"并说明尝试方式，不得编造 URL、许可证或功能。
- 许可证判断必须保守：GPL/AGPL 与闭源分发、SaaS 使用的冲突要写清。不得给出"应该没问题"这类模糊结论。
- 不得修改 `AGENTS.md`、不得碰其他 Worker 目录、不得 clone 大型仓库到项目目录（需要看源码时用临时目录并说明）、不得安装依赖。
- 不得替项目做最终选型决定——你只提供事实与可复用性判断。

## 4. 交付文件结构（必须遵守）

```
# Open Source Audit
## 1. 总览表（项目 / 许可证 / 活跃度 / 文档模型 / DOCX / 可复用性）
## 2. 逐项目详查（每个项目一节，含上述全部字段）
## 3. 许可证风险汇总
## 4. 可复用性分级（Fork / Adapt / Reference-only / 不可用）
## 5. 与本项目的匹配度分析
## 6. 未能核实的事项
## 7. 证据清单（URL + 访问日期）
```

## 5. 完成标准

- 7 个项目全部覆盖，总览表信息与详查章节一致。
- 每个项目的许可证有原文摘录，不是仅写名称。
- 每个项目都给出可复用性分级与理由。
- 明确区分"我核实过"与"我推测"。
- 回复中报告：研究范围、核心结论、证据来源、许可证风险、未确认事项、文件清单、最终状态。

## 6. 交付方式

简短总结（≤600 字）+ 文件路径清单。
