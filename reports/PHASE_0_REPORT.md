# Phase 0 报告 — ScientificWritingProject Technical Audit

> 2026-11-06 · Technical Lead (ORCA-LEAD)
> 验收状态：**FAIL**
> 结论依据：独立 QA 报告 `reports/qa/PHASE_0_AUDIT_REPORT.md`（总体判定 FAIL，6 个阻断级缺陷）

---

## 1. 验收状态：FAIL

**FAIL 的范围是"数据模型文档 + 两份报告的证据质量"，不是"技术方向"。**

架构方向（Obsidian 宿主 + 外部引擎 + 文件即真）没有被证伪；被证伪的是**当前这版数据模型文档的内部一致性**，以及 Manuscript / Open-source 两份报告的部分证据。

按放行条件，6 个阻断项全部关闭前不得进入 Phase 1 实现。

---

## 2. 环境状态

| 项 | 结果 |
|---|---|
| Orca CLI | v1.4.250，runtime ready / connected |
| Orchestration | 启用 |
| 项目仓库 | `E:\ScientificWritingProject`，git 初始化于本次会话，分支 `main` |
| 初始提交 | `e0e9af6` |
| 文档提交 | `b531b74` |
| Orca 注册 | `kind=git`，repo id `56e55e0f-49db-4f85-bddc-39986f890c15` |

---

## 3. Run 与 Task 状态

Run：`run_c3ec9d828744` — ScientificWritingProject - Phase 0 Technical Audit

| Task | Worker | Agent | 状态 |
|---|---|---|---|
| A Obsidian Architect | worker-a-obsidian | claude | completed |
| B Manuscript Specialist | worker-b-manuscript | pi | completed |
| C Scientific Modeler | worker-c-datamodel | claude | completed |
| D Open-source Researcher | worker-d-opensource | qoder-cn | completed |
| QA Phase 0 Audit | qa-phase0-hermes | hermes | completed |

### Agent 替换记录（如实记录，不掩盖）

| 尝试 | Agent | 结果 | 原因 |
|---|---|---|---|
| 1 | codebuddy | 失败 | terminal 模式，CLI 裸启动，任务规格未注入，空转 |
| 2 | codex | 失败 | structured 模式，读到第 2 份文档后停止，无产出 |
| 3 | dsh | 失败 | 免费模型 `qiniu/conatus-free` 触发 429 限流 |
| 4 | hermes | 成功 | 完成全部审计，产出 30 KB 报告 |

---

## 4. Worker 交付与质量

| 交付物 | 大小 | QA 判定 |
|---|---|---|
| `research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md` | 59 KB | 证据链外部复核**逐字节吻合**，10/10 抽查可核验 |
| `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` | 24 KB | 3 条来源与结论不符、5 条不可核验、§9 统计错误 |
| `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` | 150 KB | **FAIL**，6 个阻断级内部矛盾 |
| `research/open-source-audit/OPEN_SOURCE_AUDIT.md` | 41 KB | 2 条来源与结论不符（Manubot 许可证、Quarto 历史版本） |

### 已知过程缺陷

- **Worker B 越界写入**：交付文件写到了四个 worktree 的公共父目录，而非自己的 worktree。已由 Lead 手工收回。隔离机制本身有效，是 Worker 未遵守路径约定。

---

## 5. QA 结果摘要

必审 9 项：**5 PASS / 3 RISK / 1 FAIL**。

PASS：原始文件保护、DOCX 导入失败与信息丢失、WritingLab Core 依赖边界、Obsidian 能力未夸大、Revision Engine 闭环。
RISK：来源可追溯、技术判断证据、许可证。
FAIL：数据模型内部一致性。

### 6 个阻断级缺陷（数据模型）

| ID | 缺陷 | 状态 |
|---|---|---|
| B1 | `Panel.figure` 与 `Panel.derived_from` 同时自称权威边，违反自身 P2 | 已独立复核确认 |
| B2 | `RevisionIssue.targets[]` 在 §3.15 与 §4.6 是两种不兼容形态 | 已确认 |
| B3 | 编号 token 体系三处矛盾；Table/Equation 无实体却存在 `{{tab:}}`/`{{eq:}}` | 已确认 |
| B4 | Result↔Figure 边归属互指，无权威方 | 已确认 |
| B5 | 已 ACCEPTED 的 D-04（禁嵌套 frontmatter）与 17 张字段表未对齐 | 已确认 |
| B6 | `ANCHOR_RE` 只匹配 `^par-…`，主语法是 `^par_…`，哈希确定性失效 | **Lead 已独立复现** |

B6 复现：`ANCHOR_RE = r"\s+\^[a-z]{3}-?[0-9A-HJKMNP-TV-Z]{8}\s*$"`，对 `^par_9QK2M4XZ` 不匹配（下划线不被 `-?` 覆盖）。`Patch.before_hash`、漂移检测、VR-29/VR-45 全部建立在该哈希上。

---

## 6. 架构建议（不被 FAIL 推翻的部分）

统一架构见 `research/architecture/SYSTEM_ARCHITECTURE.md`，核心五层：

```
Vault(文件即真) → Schema → Engine(外部进程) → Bridge(127.0.0.1) → Plugin(宿主)
```

三处关键裁决：

1. **禁止嵌套 frontmatter** — Obsidian 官方明列不支持，且属性面板会重写。结构化子对象进正文 fenced YAML 块。
2. **Bases 只作浏览层** — `QueryController` 是空类，插件无法执行查询；反向关系由引擎生成 JSON。
3. **转换必须外置** — 插件无 `fs`/`child_process`，移动端调用即崩溃；DOCX 全部在引擎侧。

开源策略：**不 Fork 任何项目**，Reference-only 为主，Manubot 有限 Adapt。理由见 `decisions/ARCHITECTURE_DECISIONS.md` D-09。

---

## 7. 证据链接

- Obsidian：`research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md` + `evidence/obsidian-dts-excerpts.md`（含 `obsidian.d.ts` blob sha、SHA-256、逐条行号）
- Manuscript：`research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md`（证据清单需补 URL，见放行条件 7）
- Data model：`research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` + `schemas/`
- Open source：`research/open-source-audit/OPEN_SOURCE_AUDIT.md`（无 evidence 目录，需补）
- QA：`reports/qa/PHASE_0_AUDIT_REPORT.md`

---

## 8. 风险清单

| # | 风险 | 级别 | 来源 |
|---|---|---|---|
| R-01 | 数据模型 6 处阻断缺陷若带入实现，会产生分歧实现与静默数据损坏 | 阻断 | QA B1–B6 |
| R-02 | `python-docx` 修订能力被高估，D-03 选型基线可能错误 | 高 | QA B1(§3) |
| R-03 | 渲染期编号依赖 CM6 未类型化 API | 高 | Worker A §4.3 |
| R-04 | `_maps/` 是"文件即真"的唯一例外，备份策略未定义 | 高 | 数据模型 W1 |
| R-05 | 跨审计确认闭环缺失，块锚点语法至今悬空 | 中 | QA §5-7 |
| R-06 | 开源报告证据为二手来源，无证据快照 | 中 | QA §9-9 |
| R-07 | 大 Vault 全量扫描卡顿 | 中 | Worker A §3.3 |
| R-08 | Pandoc 为 GPL，引擎分发方式的合规边界未定 | 中 | QA §9-10 |

---

## 9. 需要你批准的决策

### 9.1 Phase 0 修复（必须先做）

- **是否启动一轮修订**：把 6 个阻断项交给 Worker C 修复，Manuscript 与 Open-source 的证据问题交给 B / D 补证，再由 QA 复审。

### 9.2 架构决策（原 7 条，仍待批）

| ID | 决策 | 建议 |
|---|---|---|
| D-05 | 文件名策略 | 混合：机器实体用 ID，人类实体用可读名 |
| D-09 | 开源复用 | 不 Fork，Reference-only |
| D-10 | WritingLab Core | 可选 Adapter，Phase 4 后再评估 |
| D-11 | 移动端定位 | 只读 |
| D-12 | Vault 目录结构 | 按架构文档 §3 |
| D-13 | 技术栈 | Python 引擎 + Pandoc + TypeScript 插件 |
| D-03 | DOCX 导入器 | Phase 1 第 1 周实测对比（须含 python-docx 修订 API 实测） |

---

## 10. 下一阶段任务

1. **修订轮（阻断）**：关闭 B1–B6，产出修订后字段表 + diff + 测试向量
2. **补证轮**：Manuscript 证据清单补 URL/版本/产物；Open-source 更正 Manubot 许可证、重做兼容矩阵、复核 Quarto 历史版本
3. **交叉确认**：Worker A 对块 ID 字符集、`{{...}}` 语法、批注支持、blocks 索引逐项答复
4. **QA 复审**：仅针对关闭项复审，通过后升级为 PASS WITH RISKS
5. 决策批准后进入 Phase 1

---

## 11. 本阶段未做的事（按约束）

- 未开始功能开发
- 未安装项目依赖
- 未修改 WritingLab Core
- 未修改任何科研资料或 Obsidian Vault
- 未自动合并 Worker 分支（四份报告由 Lead 读取后手工汇总）
- 未自动进入下一阶段

---

**停止，等待批准。**
