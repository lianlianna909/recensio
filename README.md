# Recensio

**在 Obsidian 之上构建的科研写作系统。**

Recensio 把作者的原始稿件（DOCX / LaTeX / PDF）导入为结构化 Markdown，用 YAML Properties
承载可查询的科研元数据，并在 Obsidian 内完成图表面板编号、引用管理、修订轮次与审稿意见追踪。

> 名字取自校勘学：`recensio` 指对各版本／见证本做系统比对以确定其谱系关系。
> 这与本系统的核心对象——修订轮次、版本谱系、审稿意见追溯——是同一件事。

---

## 当前状态

**Phase 0（技术审计）已完成，Phase 1（实现）尚未启动。本仓库目前没有产品代码。**

| 阶段 | 状态 |
|---|---|
| Phase 0 · 技术审计与架构决策 | 完成（PASS WITH RISKS） |
| Phase 1 · 竖切验证（引擎 + 单篇稿件） | 未启动，等待架构决策批准 |

Phase 0 的三轮独立 QA 结论、6 个阻断级缺陷的关闭过程、以及一次被交叉验证推翻的
复审降级，都完整记录在仓库里——包括失败与返工。

---

## 架构（一句话）

**Obsidian 是编辑与呈现宿主，文件系统是唯一事实来源，所有"重活"在一个独立的本地引擎进程里完成。**

```
L4  Obsidian Plugin (TypeScript)   命令 / 视图 / 装饰器 / 校验提示
L3  Local Bridge                   127.0.0.1 + 随机端口 + 一次性 token
L2  Engine (Python)                ingest / export / index / validate
L1  Schema                         YAML frontmatter + 正文 YAML 块
L0  Vault                          Markdown + Assets（只读原件，sha256 寻址）
```

**关键约束**：L1 必须自足。删除 L2–L4 后，L0 + L1 仍是一份人类可读、可 Git 管理、
可被任何编辑器打开的科研稿件。

Obsidian 不承担：DOCX 解析、Track Changes 还原、编号计算、全库索引、格式导出。
本地引擎不承担：编辑体验、链接跳转、图谱、主题。

---

## 文档

| 文档 | 内容 |
|---|---|
| [`research/architecture/SYSTEM_ARCHITECTURE.md`](research/architecture/SYSTEM_ARCHITECTURE.md) | 五层架构与边界 |
| [`research/architecture/DEVELOPMENT_ROADMAP.md`](research/architecture/DEVELOPMENT_ROADMAP.md) | Phase 1–5 路线图与退出条件 |
| [`decisions/ARCHITECTURE_DECISIONS.md`](decisions/ARCHITECTURE_DECISIONS.md) | 架构决策索引 |
| [`decisions/ADR-LIC-001-003.md`](decisions/ADR-LIC-001-003.md) | 许可证、贡献者协议、依赖治理 |
| [`research/obsidian/`](research/obsidian/) | Obsidian 能力审计 |
| [`research/manuscript/`](research/manuscript/) | DOCX / LaTeX / PDF 转换可行性 |
| [`research/data-model/`](research/data-model/) | 19 实体数据模型与文法定义 |
| [`research/open-source-audit/`](research/open-source-audit/) | 7 个开源项目的许可证与复用性核查 |
| [`reports/PHASE_0_REPORT.md`](reports/PHASE_0_REPORT.md) | Phase 0 总报告 |
| [`reports/qa/`](reports/qa/) | 三轮独立 QA 报告 |

---

## 已知限制

- **Markdown 无法无损承载 Word Track Changes。** 修订语义存于 sidecar JSON，导出时重建。
- **移动端只读。** Obsidian 移动端无 Node/Electron API，插件调用 `fs`/`child_process` 会崩溃。
- **PDF 只作辅助录入**，不是可靠导入路径。
- **不 Fork 任何开源项目。** AGPL（TeXlyre、Oleafly）与 GPL 代码均不合入。

---

## 许可证

[Apache License 2.0](LICENSE)。第三方依赖登记见 [`THIRD-PARTY.md`](THIRD-PARTY.md)，
例外记录见 [`compliance/exceptions.yaml`](compliance/exceptions.yaml)。

## 贡献

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。本项目采用 **DCO 1.1**（`git commit -s`），暂不采用 CLA。
新增依赖必须先登记 [`THIRD-PARTY.md`](THIRD-PARTY.md)。

## 开发环境

```bash
python -m venv .venv
.venv/Scripts/python -m pip install "reuse[charset-normalizer]==6.3.0"   # Windows
.venv/Scripts/reuse lint                                                # 许可证合规检查
```
