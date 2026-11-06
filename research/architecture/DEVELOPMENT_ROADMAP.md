# Development Roadmap (Phase 0 → Phase 5)

> 版本：v0.1 · 2026-11-06 · 草案，待批准
> 前置：`SYSTEM_ARCHITECTURE.md` 与 `decisions/ARCHITECTURE_DECISIONS.md` 中被批准的决策。

## 0. 路线图原则

1. **先打通一条竖切，再横向铺开。** 第一个可交付版本必须能"导入一篇真实 DOCX → 在 Obsidian 里看到结构化结果 → 导出回 DOCX"，而不是先做完整数据模型。
2. **每个 Phase 有可验证的退出条件。** 不写"基本完成"。
3. **引擎先于插件。** 引擎可以用 CLI 独立验收，插件只是它的界面。
4. **风险前置。** 三个最高风险（DOCX 保真度、CM6 装饰稳定性、段落锚点稳定性）在 Phase 1 内必须被证伪或证实。

---

## Phase 1 — 竖切验证（Engine + 单篇稿件）

**目标**：证明"导入一篇真实论文 → 结构化 → 导出"这条链路在保真度上可接受。

| 交付 | 说明 |
|---|---|
| `swp-engine` CLI 骨架 | `ingest` / `export` / `validate` 三个子命令，Python |
| Schema v1 | 只实现 Manuscript / Section / Paragraph / Figure / Panel / Asset 六个实体 |
| DOCX ingest | python-docx + lxml；产出 MD + `_maps/` + media + revisions sidecar |
| DOCX export | Pandoc + reference.docx；产出丢失项报告 |
| 保真度基准 | 5 篇真实论文，逐项记录损失 |

**退出条件**
- 5 篇论文导入后，正文文字 100% 一致（不含格式）
- 段落锚点在两次导入同一文件后完全一致
- 导出的 DOCX 能被 Word 打开，标题层级、图注、表格数量正确
- 丢失项报告覆盖全部已知损失类型

**不做的**：Obsidian 插件、编号渲染、修订 UI、引用管理。

**决策依赖**：D-03（导入器选型）必须在 Phase 1 第 1 周内定。

---

## Phase 2 — Obsidian 宿主（只读优先）

**目标**：在 Obsidian 里"看见"Phase 1 的产物。

| 交付 | 说明 |
|---|---|
| 插件骨架 | 命令注册、设置页、桥客户端 |
| 只读视图 | Figure 表（Bases 或 ItemView）、实体详情面板 |
| 校验告警 | 读取 `_index/validation.json`，侧栏展示 |
| 编号渲染 | post-processor 只读渲染 `{{figref}}` |

**退出条件**
- 打开 vault 不产生可感知卡顿（10k 文件基准）
- 校验结果与 CLI `validate` 输出一致
- 编号渲染在 reading view 与 live preview 下一致

**风险前置**：CM6 装饰器若不可用，立即触发 D-06 降级方案。

---

## Phase 3 — 修订闭环

**目标**：审稿意见 → 定位 → 修改 → 回复。

| 交付 | 说明 |
|---|---|
| RevisionRound / RevisionIssue / Patch / Response 实体 | 按 C 的模型，去掉嵌套 frontmatter |
| Sidecar 重建 | 导出时把 sidecar 还原为 `w:ins`/`w:del` |
| 回复信生成 | 从 Response 实体生成 Markdown → DOCX |
| 快照与回滚 | `Assets/snapshots/` |

**退出条件**
- 一轮真实审稿：导入带 Track Changes 的 DOCX，导出后修订标记仍在
- 每条 Issue 能定位到具体段落且锚点不漂移
- 回滚到任意轮次后，文件逐字节一致

---

## Phase 4 — 引用与编号完备

- Reference / Citation 实体，BibTeX 导入
- 交叉引用（`{{figref}}`、`{{tabref}}`、`{{citeref}}`）全类型
- 反向索引视图（引擎生成 JSON + ItemView）

**退出条件**：一篇 50 条参考文献的稿件，改序后全部引用自动更新，导出后编号连续。

---

## Phase 5 — 规模化与硬化

- 索引持久化（SQLite）
- 增量校验
- 错误恢复与降级路径全覆盖
- 性能基准与回归

---

## 里程碑与依赖

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
   │           │
   └─ D-03     └─ D-06（CM6 降级判定）
```

Phase 2 可与 Phase 1 后半并行（插件只依赖 CLI 输出格式，不依赖其实现）。

---

## 明确不排期

| 项 | 原因 |
|---|---|
| 云端协作 | 与本地优先冲突 |
| 移动端写入 | Obsidian 移动端无 Node 能力 |
| 自有文献管理器 | 接 Zotero |
| WritingLab Core 集成 | 待用户单独批准 |
| Fork 任何开源项目 | 见架构文档 §9 |
