# Scientific Writing System — System Architecture (Phase 0)

> 版本：v0.1 · 2026-11-06
> 状态：**草案，待用户批准**
> 来源：`research/obsidian`、`research/manuscript`、`research/data-model`、`research/open-source-audit` 四份 Phase 0 报告的统一结论。本文不是四份报告的拼接，凡与单份报告冲突处，以 `decisions/ARCHITECTURE_DECISIONS.md` 的裁决为准。

---

## 1. 一句话架构

**Obsidian 是编辑与呈现宿主，文件系统是唯一事实来源，所有"重活"在一个独立的本地引擎进程里完成，两者通过一个受控的本地桥通信。**

Obsidian 不承担：DOCX 解析、Track Changes 还原、编号计算、全库索引、格式导出。
本地引擎不承担：编辑体验、链接跳转、图谱、主题。

---

## 2. 分层

```
┌──────────────────────────────────────────────────────────┐
│ L4  Obsidian Plugin (TypeScript)                         │
│     命令 / 视图 / 装饰器 / 校验提示 / 桥客户端            │
├──────────────────────────────────────────────────────────┤
│ L3  Local Bridge  (127.0.0.1:random port, 一次性 token)   │
│     JSON-RPC over HTTP；桌面端 only                       │
├──────────────────────────────────────────────────────────┤
│ L2  SWP Engine  (独立进程, Python 或 Node)                │
│     ingest / export / index / validate / numbering        │
├──────────────────────────────────────────────────────────┤
│ L1  Schema  (YAML frontmatter + 正文 YAML 块 + _maps/)     │
├──────────────────────────────────────────────────────────┤
│ L0  Vault  (Markdown 文件 + Assets 内容寻址, 只读原件)     │
└──────────────────────────────────────────────────────────┘
```

**关键约束**：L1 必须自足。把 L2 和 L4 全部删除后，L0+L1 仍然是一份人类可读、可 Git 管理、可被任何编辑器打开的科研稿件。这是"文件即真"的可验证形式。

---

## 3. 各层职责与边界

### L0 Vault

| 目录 | 内容 | 可变性 |
|---|---|---|
| `Manuscripts/` | 正文 Markdown（一篇稿件一个主文件） | 可编辑 |
| `Figures/` | Figure / Panel 实体文件 | 可编辑 |
| `Results/` `Methods/` `Experiments/` `Claims/` | 结构化实体 | 可编辑 |
| `References/` | 文献条目 | 可编辑（可由 BibTeX 生成） |
| `Assets/` | 原始 DOCX / PDF / 图片，按 `sha256` 命名 | **只读，永不改写** |
| `_maps/` | 段落锚点映射表 | 引擎写，人只读 |
| `_index/` | 派生索引 | 可随时删除重建 |

原始件保护是硬规则：`Assets/` 下的文件只允许新增，不允许修改或删除；引擎在每次 ingest 前校验 `sha256`，不匹配即中止并告警。

### L1 Schema

由 Worker C 的 17 实体模型定义，但按 §4 的裁决做了三处修正。

### L2 Engine

单一可执行程序，四个子命令：

- `ingest` — DOCX / LaTeX / PDF → Markdown + `_maps/` + sidecar
- `export` — Markdown → DOCX（Pandoc + reference.docx 模板）
- `index` — 构建反向索引与断链检查（可选 SQLite）
- `validate` — 执行 schema 与完整性规则

引擎必须是**可独立运行的 CLI**，不依赖插件存在。这样 CI 与批处理可用，插件挂了数据也不会锁死。

### L3 Bridge

- 仅监听 `127.0.0.1`，端口随机，启动时写入插件目录的 token 文件
- 请求/响应 JSON，长任务返回 job id + 轮询
- **移动端不存在这一层**：移动端只读

### L4 Plugin

只做四件事：触发引擎、渲染派生结果、展示校验告警、提供导航。**不实现任何转换逻辑**。

---

## 4. 对 Worker 报告的三处架构裁决

### 4.1 嵌套 frontmatter：否决

Worker C 的模型在 `Citation`、`Issue.targets`、`section_meta` 上使用了 `list<object>`。Worker A 的官方证据表明 Obsidian 明列 **Nested properties 不支持**，且 Properties 面板会重写 frontmatter。

裁决：
- frontmatter 只允许 **标量 / 标量列表 / wikilink 列表**。
- 结构化子对象放**正文的 fenced YAML 块**（```yaml swp:citation```），Obsidian 不改写正文代码块。
- 高频小结构（如 `Citation`）用平行列表平铺：`cit_ref[] / cit_locator[] / cit_role[]`，由引擎保证等长。

代价：Properties 面板里看不到引用详情，只能看计数。可接受——引用详情本来就该在正文里被读到。

### 4.2 Bases：只做浏览，不做查询引擎

Worker A 证明 Bases 的查询引擎不对外暴露执行接口，且模型是"文件为行"。Worker C 需要反向关系查询。

裁决：
- Bases 仅用于"一文件一实体"的只读表（Figure 表、Reference 表）。
- 反向关系（"这个 Reference 被哪些 Claim 引用"）由 L2 `index` 生成 JSON，插件用 `ItemView` 渲染。
- 不把任何业务规则写进 `.base` 文件。

### 4.3 DOCX：必须外置进程

Worker B 推荐 docx4j / python-docx，Worker A 证明插件无 `fs` / `child_process`、移动端直接崩溃。

裁决：
- DOCX 导入导出全部在 L2 引擎，插件不碰 OOXML。
- 移动端明确不提供导入导出。
- 不承诺"插件内一键导入"；用户体验是"命令 → 引擎任务 → 进度 → 结果"，与 IDE 的重构操作同构。

---

## 5. 数据流

### 5.1 导入

```
DOCX ──sha256──► Assets/ (只读)
      │
      ├─► Engine.ingest ──► Manuscripts/xxx.md  (正文)
      │                 ──► _maps/xxx.map.yaml  (段落锚点)
      │                 ──► Manuscripts/xxx.revisions.json (Track Changes sidecar)
      │                 ──► Assets/xxx.media/    (抽出的图片)
      └─► Engine.index  ──► _index/*.json
```

失败语义：ingest 是全或无。任一步失败，删除本次产生的所有新文件，原稿不受影响，向用户报告失败阶段与原因。**不存在"导入了一半"的状态。**

### 5.2 导出

```
Manuscripts/xxx.md ──► Engine.export ──► out/xxx.docx
                        │  1. 固化编号（Figure 3 写死）
                        │  2. 剥离 ^block-id 与 {{token}}
                        │  3. 套 reference.docx 模板
                        │  4. 从 sidecar 重建 Track Changes（可选）
                        └─► out/xxx.report.json（丢失项清单）
```

导出必须产出**丢失项报告**：哪些格式在往返中损失。这是产品的一部分，不是调试信息。

### 5.3 编辑期

插件监听 `metadataCache.on('changed')`，只跑**单文件**校验规则；全库校验由引擎在空闲时执行，结果写入 `_index/validation.json`，插件只读展示。避免 Worker A 指出的 `resolved` 反复触发与全量扫描竞态。

---

## 6. 编号系统

- 文件里只存 `{{figref:fig_7K3M9Q}}`，不存 `Figure 3`。
- 编辑期：插件 post-processor + CM6 装饰器渲染为 `Figure 3`（只读呈现）。
- 导出期：引擎固化。
- 校验规则 VR-07 拦截正文中的字面量 `Figure N`。

风险：渲染期解析依赖 CM6 装饰 API，Worker A 标注其为稳定公开 API，但底层 `EditorView` 访问需 `@ts-expect-error`。若失效，降级为"写入时固化 + 手动重排命令"。

---

## 7. 修订系统

Markdown 无法承载 Track Changes（Worker B 明确结论）。采用三层：

1. **Sidecar JSON** — `*.revisions.json`，保存 `w:ins`/`w:del` 的作者、时间、范围，用于导出时重建。
2. **RevisionRound 快照** — 每轮修订生成 `Assets/snapshots/<round>/<file>.md`（内容寻址），用于回滚。
3. **Git** — 作为外部版本层，不作为修订语义。

三者职责不重叠：sidecar 管"Word 修订标记"，快照管"轮次回滚"，Git 管"提交历史"。

---

## 8. 索引

- 主索引由引擎生成，放 `_index/`，格式 JSON（<5k 实体）或 SQLite（>5k）。
- 插件**不建全库索引**，只读引擎产物 + 内存中维护当前文件。
- 索引可随时删除重建；重建耗时目标 < 10s（10k 文件）。

---

## 9. 开源复用策略

| 项目 | 结论 | 理由 |
|---|---|---|
| Quarto | **Reference-only** | CLI 工具而非库；Fork 后无法作为产品基础维护 |
| Curvenote Editor | **Reference-only**（原判 Adapt 下调） | ProseMirror 栈与 Obsidian 的 CM6 不兼容，只能借鉴 schema 设计 |
| Manubot | **Adapt（有限）** | 仅借鉴 citation 处理流程与 `manubot cite` 的 CLI 契约 |
| Typst | Reference-only | 排版引擎，与本项目无直接复用点 |
| TeXlyre / Oleafly | **Reference-only（法务阻断）** | AGPL-3.0；**条件性结论**——若本项目最终闭源分发或作为 SaaS 提供，AGPL 代码不可复用；若改为 AGPL 兼容的开源分发，此项需重新评估。分发形态见 D-09（PENDING） |
| TeXMind | 不可用 | 未能核实为科研写作项目 |

**没有任何 Fork。** 这是对 Worker D 建议的修正：Worker D 建议 Fork Quarto，但 Quarto 是打包好的 CLI 发行版，Fork 它等于接管一个百万行级工具的维护，与"在 Obsidian 上做科研写作"的目标不匹配。

---

## 10. WritingLab Core

定位：**可选 Adapter，不是依赖**。

- 默认架构不引用 WritingLab Core。
- 若接入，只能通过 L2 引擎的 adapter 接口，且必须满足：不修改 Core、不把 Core 的数据结构泄漏进 L1 schema、Core 缺失时系统功能不降级（除该 adapter 提供的功能外）。
- Phase 0 不评估其具体能力，只锁定边界。接入方式需用户单独批准。

---

## 11. 已识别的架构级风险

| # | 风险 | 影响 | 缓解 |
|---|---|---|---|
| R-01 | 本地桥在 Windows 上的进程管理与端口安全 | 中 | 随机端口 + token + 仅 127.0.0.1；不做远程监听 |
| R-02 | 渲染期编号依赖 CM6 装饰 API 稳定性 | 高 | 保留写入时固化降级路径 |
| R-03 | 无嵌套 frontmatter 导致引用详情不可在 Properties 中编辑 | 中 | 正文 YAML 块 + 专用编辑视图 |
| R-04 | 段落锚点 `_maps/` 是"文件即真"的唯一例外 | 高 | 随稿件进 Git；加载时执行 VR-49 |
| R-05 | 大 Vault 下插件全量扫描卡顿 | 中 | 插件不做全量扫描 |
| R-06 | 导入器选型（python-docx vs docx4j）未定 | 中 | Phase 1 第一周做对比验证 |
| R-07 | 移动端功能缺口 | 低 | 明确为只读端 |

---

## 12. 不做什么

- 不做 Obsidian 内的 DOCX 解析
- 不做云端协作
- 不做自有排版引擎
- 不做文献管理器（接 Zotero / BibTeX）
- 不 Fork 任何开源项目
- 不在 Phase 1 之前写业务代码
