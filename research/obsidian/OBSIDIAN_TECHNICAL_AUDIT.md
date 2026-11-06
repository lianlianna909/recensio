# Obsidian Technical Audit

> 阶段：Phase 0 · Worker A · 唯一交付物 `research/obsidian/OBSIDIAN_TECHNICAL_AUDIT.md`
> 审计日期：2026-11-06
> 结论规则：凡标「**推测**」的条目表示没有直接证据，仅有间接推理；凡标「**社区插件能做**」的表示不属官方 API 能力。

---

## 0. 审计方法与证据基线（先读这一节，否则后面的置信度无从判断）

本报告不依赖记忆。所有 API 断言来自两个可复现的来源：

1. **`obsidian.d.ts`（权威类型定义）**
   - `obsidianmd/obsidian-api` 仓库 `master` 分支的 `obsidian.d.ts`，经 GitHub Contents API 拉取，git blob sha `10b31c4787fbc3ee4b228ca403165bbf865eb165`。
   - 与 npm 包 `obsidian@1.14.4` 内的 `obsidian.d.ts` 做 `diff`：**仅 5 处 JSDoc 措辞差异（"sidebar"→"sidedock"），所有类型签名逐字节一致**。
   - 文件指纹：11,539 行，SHA-256 `97c86417c893db691e401fdffd9026e348dc96da6bfcfa5d49a301d7fe7542a0`。
2. **官方文档（两个 Publish 站点）**
   - 开发者文档：`https://docs.obsidian.md/...`（底层 Publish 站点 uid `caa27d6312fe5c26ebc657cc609543be`）
   - 用户帮助：`https://help.obsidian.md/...`（底层 Publish 站点 uid `f786db9fac45774fa4f0d8112e232d67`）
   - 变更日志：`https://obsidian.md/changelog/...`

**环境限制（影响证据强度，必须声明）**：
- 本机 `raw.githubusercontent.com` 与 `github.com` 被阻断，`api.github.com` 有速率限制。因此**所有 GitHub 仓库文件均通过 Contents API 或镜像站点取得**，无法给出"某仓库某 commit 的 GitHub blob URL"，只能给 API URL + 本地指纹。
- 所有 Publish 文档的页面内容是通过其公开的 `access/<uid>/<path>.md` 原始 Markdown 端点取得的（这是 Obsidian Publish 的公开内容分发机制），因此引用格式统一写为官方站点 URL + 原始 Markdown 端点，便于 QA 复验。

类型定义摘录见 `research/obsidian/evidence/obsidian-dts-excerpts.md`（含行号）。

---

## 1. 结论摘要

| # | 结论 | 置信度 |
|---|---|---|
| 1 | 当前官方类型包为 `obsidian@1.14.4`；`obsidian-api` master 同时包含已发布到 1.15.x 的类型（如 `groupOrder` 标 `@since 1.14.3`），说明**类型包版本 ≠ 应用版本**，`minAppVersion` 必须按用到的每个 API 的 `@since` 逐项抬高，不能只跟包版本。 | 高 |
| 2 | `FrontMatterCache` 只有一个 `[key: string]: any` 索引签名，**官方不提供任何 frontmatter 值的类型化访问**；JSON→YAML 的语义差异、日期、wikilink 全部要插件自己归一化。 | 高 |
| 3 | Obsidian 原生的 Properties 类型集只有 7 种（Text / List / Number / Checkbox / Date / Date & time / Tags），且**全局按属性名共享类型**；"Markdown in properties" 与 "nested properties" 被官方文档明列为**不支持**。 | 高 |
| 4 | `MetadataCache` 提供 `headings / links / embeds / tags / footnotes / footnoteRefs / referenceLinks / sections / listItems / frontmatter / frontmatterPosition / frontmatterLinks / blocks`，外加 `resolvedLinks / unresolvedLinks`；**没有**反向链接查询、没有全文索引、没有跨文件聚合 API。 | 高 |
| 5 | `metadataCache.on('changed')` **在文件改名时不会触发**（类型注释明说），只能监听 `Vault.on('rename')`；缓存失效是异步的，"写完立刻读缓存"是典型竞态。 | 高 |
| 6 | Bases 在 1.10.0 起向插件开放了 `registerBasesView` + `BasesView` / `BasesQueryResult` / `Value` 体系，因此**插件可以完全自定义 Bases 的渲染**（官方 Guide 有完整示例）。 | 高 |
| 7 | 但 Bases 的**查询引擎**只暴露"结果"，不暴露"执行"：`QueryController` 在类型里是空类，`.base` 过滤语法是字符串，插件无法用官方 API 在任意上下文执行一个 Bases 查询。 | 高 |
| 8 | Bases 的结构是"**文件为行**"（`BasesEntry.file: TFile`），不是关系型。Figure/Panel/Reference 若按"一文件一实体"建模则 Bases 够用；若按"一文件多 Panel"这类内部一对多建模，**Bases 原生无法逐行展开**，必须落到自建 `BasesView` 或 `ItemView`。 | 高 |
| 9 | 自定义 `ItemView` 可以渲染任意 DOM/Canvas（`contentEl: HTMLElement`），但**没有官方 API 在自定义 View 内嵌入可编辑的 Markdown 编辑器**。 | 高 |
| 10 | CM6 集成是稳定公开 API（`registerEditorExtension(extension: Extension): void`，`@since 0.12.8`），但访问底层 `EditorView` 只能靠 `view.editor.cm`——**该字段不在类型里**，官方文档自己写了 `@ts-expect-error, not typed`。 | 高 |
| 11 | 插件运行时**没有** `fs` / `child_process` / native addon 的公开 API；移动端明确"Node.js API 和 Electron API 不可用，任何调用会让插件崩溃"。调用外部 Python 解析 DOCX **只能在桌面端**，且属于 Electron 私有能力，不属公开 API。 | 高 |
| 12 | 插件对 vault 文件的读写必须走 `Vault` / `DataAdapter`（异步、无同步 API、`process()` 保证原子读改写）；任何"边写边读"的编排都必须建立在 `process()` 之上。 | 高 |
| 13 | 自 Obsidian 1.7.2 起视图默认 **deferred**，插件遍历 leaves 时 `leaf.view` 可能不是自己的 View 实例，必须 `instanceof` 守卫或 `await leaf.loadIfDeferred()`。 | 高 |
| 14 | Bases 的原生视图（Table/Cards/List/Kanban/Map）能给 Figure 表"看"，但**不能做编号持久化、不能做冲突检测、不能生成交叉引用文本**——这些必须落在插件或外部工具。 | 高 |
| 15 | 结论：**Obsidian 是渲染与编辑宿主，不是数据仓库也不是规则引擎**。Figure 编号、审稿意见、修订轮次的权威数据必须在 Obsidian 之外或通过独立插件模块计算，Obsidian 侧只负责"呈现 + 受控写入"。 | 中 |

> 第 15 条为架构判断（置信度中），其依据是第 4/6/7/8/9/14 条的事实（置信度高）。

---

## 2. API 与版本事实

### 2.1 版本证据链

| 事实 | 证据 |
|---|---|
| npm 最新 `obsidian` 包 = `1.14.4`，发布时间 2026-10-08 | `https://registry.npmjs.org/obsidian` 的 `dist-tags.latest = 1.14.4`；`time["1.14.4"] = 2026-10-08T22:27:35.586Z` |
| 类型包内 `obsidian.d.ts` 与 `canvas.d.ts` | tarball `https://registry.npmjs.org/obsidian/-/obsidian-1.14.4.tgz`，sha1 `e4d4c91d…`，`fileCount: 7` |
| 官方 changelog 已到桌面版 1.15.1 | `https://obsidian.md/changelog/2026-11-03-desktop-v1.15.1/` |
| `obsidian-api` master 的最近提交 | `9abd9605ce08 2026-10-05 "Add FrontmatterValue."`、`40301c12bb92 2026-10-02 "Update to Obsidian 1.14.4."`（`https://api.github.com/repos/obsidianmd/obsidian-api/commits`） |
| 类型里有 `@since 1.14.3` 的字段（`BasesConfigFileView.groupOrder`） | 说明 master 类型已超前于 npm 包版本号 |

**结论**：`npm view obsidian version` 给出的数字**不是**应用版本，只是"类型定义快照"的版本。真正的版本约束来自每个 API 上的 `@since X.Y.Z` 注释 + `apiVersion` 常量（`obsidian.d.ts:1319`，注释说明 "follows the release cycle of the desktop app"）。

### 2.2 `manifest.json` 与 `minAppVersion`

`PluginManifest`（`obsidian.d.ts:7376`）字段：`dir?`、`id`、`name`、`author`、`version`、`minAppVersion`、`description`、`authorUrl?`、`isDesktopOnly?`。

官方 `Reference/Manifest`（`https://docs.obsidian.md/Reference/Manifest`）明确：
- `minAppVersion`、`version`、`name`、`author` 必填；
- 插件额外必填 `id`、`description`、`isDesktopOnly`（**注意：类型定义里 `isDesktopOnly?` 是可选的，文档说必填——两者不一致，以文档为准**）；
- `id` 只能含小写字母和连字符，不能以 `plugin` 结尾，不能含 `obsidian`。

`Reference/Versions`（`https://docs.obsidian.md/Reference/Versions`）：`versions.json` 把"插件版本"映射到"该版本要求的 minAppVersion"，让低于 minAppVersion 的用户拿到旧版插件。

> **对本项目的含义**：如果本系统用到 Bases API（`@since 1.10.0`）、`groupOrder`（`@since 1.14.3`）、deferred views（`@since 1.7.2`），`minAppVersion` 至少要 `1.14.3`，并且必须配 `versions.json`。

### 2.3 近期 API changelog 关键变化

来源：`https://obsidian.md/changelog/2026-09-02-desktop-v1.14.0/`、`.../2026-10-05-desktop-v1.14.4/`、`.../2026-10-22-desktop-v1.15.0/`，以及 npm 包内 `CHANGELOG.md`（仅覆盖到 1.7.2）。

| 版本 | 变化 | 对本项目的影响 |
|---|---|---|
| 1.15.0 | **关闭格式标记 token 的 syntax-tree 节点名改为 `formatting_*-end`**；"Plugins that match full node names like `formatting-code_inline-code` will miss closing tokens; match `formatting-code` instead." | 任何基于 CM6 语法树做内联装饰（如给 Figure 引用上色）的扩展必须按新节点名匹配 |
| 1.15.0 | Obsidian 不再内置 Mermaid，改用 Pele；`loadMermaid()` 仍可用但渲染类名不同 | 不影响本项目，但说明"内置库"会变 |
| 1.14.4 | Bases 新增 **Kanban 视图** 与 **Group 菜单**（分组属性、顺序、隐藏） | Figure 面板的看板式追踪可直接用 Kanban，无需自研 |
| 1.14.4 | "Fixed periodic input lag in large vaults caused by **properties getting recomputed** in the background." | 官方承认大 vault 下 frontmatter 重算有性能问题；1.14.4 只是修复 |
| 1.14.x | 支持打开 vault 外的单个 Markdown 文件 | 对"导入原稿"路径有影响（可以在 vault 外预览） |
| （类型层）1.14.3 | `BasesConfigFileView.groupOrder?: FrontmatterValue[]` | 可程序化控制分组顺序 |
| （类型层）1.14.4/master | 新增 `export type FrontmatterValue` | 官方首次给出 frontmatter 的联合类型，但**未被任何方法签名使用** |
| 1.7.2 | `Plugin#onUserEnable`、`Workspace#ensureSideLeaf`、`WorkspaceLeaf#isDeferred/loadIfDeferred`；移除 `prepareQuery`/`fuzzySearch`/`PreparedQuery` | deferred view 处理是必做项 |
| 1.5.7 | `Plugin#onExternalSettingsChange`、`Vault#getFileByPath`、`View.scope` 公开、`getFrontMatterInfo`、`FileManager#getAvailablePathForAttachment` | 外部同步导致设置变化时需重载 |
| 1.4.0 | **Properties 正式化**：`FrontMatterCache` 不再是 `CacheItem`（无 position），frontmatter 支持 wikilink 并缓存到 `frontmatterLinks` | 所有 frontmatter 代码必须以 1.4+ 语义为准 |

### 2.4 三类 API 的明确划分

| 类别 | 定义 | 本项目会用到的典型符号 | 判定依据 |
|---|---|---|---|
| **A. 稳定公开 API** | `obsidian.d.ts` 中带 `@public` 且有 `@since`，且官方文档站有对应页面 | `Vault`、`DataAdapter`、`MetadataCache.getFileCache`、`FileManager.processFrontMatter`、`getFrontMatterInfo`、`ItemView`、`registerView`、`registerMarkdownPostProcessor`、`registerEditorExtension`、`registerBasesView`、`BasesView`、`BasesEntry.getValue`、`Value.renderTo`、`Platform`、`requestUrl`、`normalizePath` | 类型 + 文档双证 |
| **B. 未文档化但类型里存在** | `obsidian.d.ts` 里存在，但官方文档站没有页面，或注释自相矛盾/废弃 | `iterateCacheRefs`（标 `@deprecated`）、`CachedMetadata.referenceLinks`/`footnoteRefs`（有 `@since` 但指南未覆盖）、`BasesView.config.getEvaluatedFormula`（`@since 1.10.2`，仅在类型）| 类型有、文档无 |
| **B'. 类型里存在但语义空洞** | 类存在但无任何公开成员——等于"已知的不透明句柄" | **`QueryController`**（`export class QueryController extends Component { }`，零成员） | `obsidian.d.ts:7643` |
| **C. 完全不可用（需私有 hack）** | 类型里没有，只能靠运行时对象形状 + `as any` | `view.editor.cm`（官方文档明写 `@ts-expect-error, not typed`）、Electron `require('electron')`、`window.require('fs'/'child_process')`、`app.metadataCache.getBacklinks()` 之类的内部方法 | 类型 0 命中 + 官方文档明确"not typed" |

> **C 类才是真正的风险点**：C 类 API 的破坏性变更不会出现在 changelog 的 "Developers" 段，也不会在类型层报错。本项目的设计原则是**C 类调用必须收敛到单点适配层并带降级**。

---

## 3. Vault / Properties / MetadataCache

### 3.1 Properties 的类型系统（官方事实）

来源：`https://help.obsidian.md/properties`（原始 Markdown：`https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Editing%20and%20formatting/Properties.md`）

官方定义的 7 种属性类型：

| 类型 | 存储形态（官方示例） | 原样解析出的 YAML 值 |
|---|---|---|
| Text | `title: A New Hope` | string |
| List | `cast:\n  - Mark Hamill\n  - Harrison Ford` | array of string |
| Number | `year: 1977` / `pie: 3.14` | number |
| Checkbox | `favorite: true` / `last:`（空值，"often treated as false"） | boolean / null |
| Date | `date: 2020-08-21` | **YAML 里是 string**（Obsidian 内部按属性类型解释） |
| Date & time | `time: 2020-08-21T10:30:00` | string |
| Tags | 只有 `tags` 属性能用，list 形态 | array of string |

**必须注意的官方原文**：
- "Once a property type is assigned to a property name, **all properties with that name across your vault will use the same type**." → 属性类型是 **vault 全局**的，不是按文件、不是按目录。这对"同一字段在不同稿件里语义不同"的科学写作场景是一个硬约束。
- Text 属性里：**"Markdown formatting is not rendered"**，**"Hashtags do not create tags"**。
- 内部链接："**must be surrounded with quotes**"，例：`link: "[[Episode IV]]"`。
- List 属性里的内部链接："**surround them with quotes**"，例：`- "[[Link]]"`。
- 明列 **不支持**（原文小标题 "Not supported"）：**Nested properties**、**Bulk-editing properties**、**Markdown in properties**。
- 支持 JSON 块（`---` 里放 JSON），但 "the JSON block will be read, interpreted, and **saved as YAML**"。
- 每个属性名在单个笔记内必须唯一。
- 1.4 起 `tag` / `alias` / `cssclass`（单数）废弃，**1.9 起彻底不再作为默认属性**。

**类型层对应**：`FrontMatterCache` 只有一个 `[key: string]: any`。也就是说 **YAML 的日期、链接、null、嵌套对象在 `app.metadataCache.getFileCache(file).frontmatter` 里全部是 `any`**，Obsidian 不会替你把 `date: 2020-08-21` 变成 `Date` 对象。属性"类型"只决定 UI 呈现与搜索/查询语义，不改变 `FrontMatterCache` 的结构。

### 3.2 能在哪些地方"看见" frontmatter

| 消费方 | 能否看见 frontmatter 字段 | 能否看见字段里的 wikilink | 证据 |
|---|---|---|---|
| 原生搜索 | 能：`[property]` / `[property:value]` / `[property:null]`、`[a:b OR c]`、`[duration:<5]` | 值按文本匹配（可搜 `[[...]]` 字面） | `https://help.obsidian.md/plugins/search` → `## Search properties` |
| `MetadataCache` | 能：`frontmatter`（`any` 字典） | 能：`frontmatterLinks: FrontmatterLinkCache[]`，每项有 `key` 字段 | `obsidian.d.ts:2510` 附近 |
| Bases | 能：`note.*` 属性；wikilink 值被解析为 `LinkValue` | 能：官方说明 "Wikilinks in frontmatter properties are **automatically recognized as Link objects**" | `https://help.obsidian.md/bases/syntax` → `### Files and links` |
| Dataview（社区插件） | 能：所有 YAML frontmatter 自动成为字段 | 能（但需 `[[...]]` 且带引号） | `https://blacksmithgu.github.io/obsidian-dataview/annotation/add-metadata/` → `## Frontmatter` |

> **关键差异（重要）**：
> - **Bases**：wikilink 被类型化成 `Link` 对象，可以做 `link.asFile()`、`file.hasLink(other)`、`authors.contains(this)` 这类**关系操作**。
> - **Dataview**：frontmatter 自动成为字段，类型按 "wrapped in quotes → text"、"ISO 日期格式 → date"、"YAML object 语法 → object" 推断（Dataview 官方文档原文）。所以 **Dataview 的类型推断规则与 Obsidian/Bases 不一致**（例如 `date: 2020-08-21` 在 Dataview 里是 date，在 `FrontMatterCache` 里是 string）。
> - **原生搜索**：完全不做类型化，是文本匹配。
>
> 三者对同一个 frontmatter 的"解释"不同，是本项目最容易出错的地方之一。

### 3.3 大规模 vault（>10k notes）的解析与索引开销

**已证事实**：
- Obsidian 1.14.4 changelog 原文："Fixed periodic input lag in large vaults caused by **properties getting recomputed in the background**." → 官方确认 frontmatter 重算在大 vault 会造成输入卡顿，直到 1.14.4 才缓解。
- Obsidian 1.14.4 changelog："Fixed the app freezing when searching headings across all notes (`[[##`) in large vaults."
- Bases 官方 Guide 原文："An unfiltered Base will provide an entry for every file in the vault, so your view should be able to handle **thousands of entries**, reuse DOM elements, and avoid rendering off screen where appropriate."
- `MetadataCache` 注释：文件被**重命名**时**不会**触发 `changed` 事件（性能原因）。

**判断**：
- frontmatter 的**解析**由 Obsidian 核心完成并缓存，插件拿缓存是 O(1) 级访问，**不需要也不应该**自己解析全部文件的 frontmatter。
- 真正的开销在于**插件的全量遍历**：`vault.getMarkdownFiles()` + `metadataCache.getFileCache()` × 10k 次，加上随后对 `frontmatter` 字段的读写，是一次 O(N) 的同步循环。在 1.14.4 之前还会与 Obsidian 的后台重算叠加。
- **推测**：对 10k–50k 笔记，只要全量扫描放在 `workspace.onLayoutReady` 之后、并做增量（`metadataCache.on('changed')` 只处理单个文件），可接受；但对 >50k 或单文件 frontmatter 很大的 vault，需要自建持久化索引（放在 `.obsidian/plugins/<id>/` 或独立外部文件），不能每次启动全扫。

> 注意：`Vault.getMarkdownFiles()` 本身要遍历全部文件；`MetadataCache.resolvedLinks` 在所有文件都解析完之前是不完整的——见 §3.4。

### 3.4 MetadataCache 能力边界

**能拿到**（`CachedMetadata`，13 个字段，全部可选）：

```
links, embeds, tags, headings, footnotes, footnoteRefs, referenceLinks,
sections, listItems, frontmatter, frontmatterPosition, frontmatterLinks, blocks
```

以及 `MetadataCache` 本身的两张全 vault 表：

```ts
resolvedLinks:   Record<string, Record<string, number>>;   // 源路径 → 目标路径 → 链接次数
unresolvedLinks: Record<string, Record<string, number>>;   // 源路径 → 未解析目标 → 次数
```

**拿不到**（本设计中需要的、但官方没有的）：

| 需要的能力 | MetadataCache 是否提供 | 替代方案 |
|---|---|---|
| 某个文件的反向链接（谁链接到我） | **不提供** | 自建反向索引：遍历 `resolvedLinks`（O(N) 建一次，之后增量维护） |
| 某个 block 的**内容** | 不提供（`BlockCache` 只有 `id` 与位置） | `Vault.cachedRead` + 按位置切片 |
| Frontmatter 值的语义类型（date vs string） | 不提供（`any`） | 自行按 schema 归一化 |
| 表格 / 任务的内部结构 | **不提供**（`listItems` 只有位置和父子关系，`TaskList` 结构不在 SDK 里） | 自行解析文本 |
| 标题的编号（1.2.3） | 不提供（只有 heading 文本与 level） | 自行计算 |
| 全文检索 / 分词索引 | 不提供 | 用原生 Search 的 UI，或外部工具 |

> 关于列表：`ListItemCache` 只有位置（`position`、`parent`、`children` 等索引），**不含任务勾选状态、不含内联字段**。想在 frontmatter 之外承载 Panel 级元数据，MetadataCache 帮不上忙。

### 3.5 增量更新语义与竞态

**已证事实**（全部来自 `obsidian.d.ts` 的 `MetadataCache` 注释）：

| 事件 | 签名 | 语义（官方原文要点） |
|---|---|---|
| `changed` | `(file: TFile, data: string, cache: CachedMetadata)` | 文件被索引、更新后的缓存可用时触发。**文件重命名时不触发** |
| `deleted` | `(file: TFile, prevCache: CachedMetadata \| null)` | 文件删除；`prevCache` 是尽力而为的旧缓存，可能为 `null` |
| `resolve` | `(file: TFile)` | 该文件的链接被解析进 `resolvedLinks / unresolvedLinks`，"This happens **sometimes after** a file has been indexed" |
| `resolved` | `()` | 所有文件都已解析。**"will be fired each time files get modified after the initial load"** |

**四个必然的竞态**（均为由上述语义直接推出，非推测）：

1. **写后读竞态**：`await fileManager.processFrontMatter(file, fn)` 返回后，`metadataCache.getFileCache(file)` **不保证**已更新——索引是异步的。必须 `await` `changed` 事件（带超时降级）。
2. **rename 不触发 `changed`**：`Vault.on('rename')` 之后元数据缓存不会发 `changed`，任何"按路径缓存 frontmatter"的自有索引会与真实状态错位，必须在 rename 里**重映射 key**。
3. **`resolved` 反复触发**：它不是"加载完成一次"的信号，初始加载后每次文件修改都会再触发。用它做"首次全量建索引用"必须自带 only-once 守卫，否则会反复全量重建。
4. **启动窗口期**：在 `workspace.onLayoutReady` 之前 `vault.on('create')` 会为**每个文件**各触发一次（官方 Guide《Optimize plugin load time》原文："it will call `create` for every file"），此时注册的 handler 会把整个 vault 当成"新增文件"处理。

**官方推荐的做法**（《Optimize plugin load time》）：
- `onload` 只做注册（commands / views / post-processors），不做数据拉取；
- vault 事件注册放在 `workspace.onLayoutReady(...)` 内；
- 或者用 `this.app.workspace.layoutReady`（`obsidian.d.ts:10718` 确认存在）守卫。

---

## 4. Views / Commands / 编辑器集成

### 4.1 自定义 View 的能力边界

**能做**：
- `ItemView` 提供 `contentEl: HTMLElement`（`obsidian.d.ts:5398`），可以往里渲染任意 DOM、SVG、`<canvas>`、WebGL。**因此"渲染任意 HTML/Canvas"是成立的**——因为 `contentEl` 就是一个普通 DOM 节点，Electron/WebView 能渲染什么它就能渲染什么。
- `addAction(icon, title, callback)` 向视图头添加按钮（`@since 1.1.0`）。
- `View.scope: Scope | null`（1.5.7 起公开），能给本视图绑定快捷键。
- `registerView(type, creator)` 注册视图类型；`workspace.getRightLeaf(false).setViewState({ type, active: true })` 打开。

**不能做 / 无官方支持**：
- **没有官方 API 在自定义 `ItemView` 内嵌入可编辑的 Markdown 编辑器**。任务书问"能否嵌入编辑器"——答案是**否**（就公开 API 而言）。
  - 证据：`obsidian.d.ts` 中没有 "embed editor" 之类的导出；`ItemView` 只有 `contentEl`；`TextFileView` / `MarkdownView` / `MarkdownEditView` 是具体实现类，不是"可嵌入组件"。
  - 社区插件常用的做法是 `workspace.openLinkText` 打开侧边编辑，或直接给 `contentEl` 挂一个自建的 CM6 `EditorView`——**后者需要自己处理保存、主题、快捷键、撤销栈，属于社区实践而非官方能力。**
- **没有**官方 API 让插件"注册一个新的 Markdown 渲染容器"供别的 View 复用。

**deferred views（必读）**：自 1.7.2 起，Obsidian 启动时所有视图都是 `DeferredView`，直到该 tab 第一次可见。官方 Guide《Understanding deferred views》给出的规则：
- 遍历 leaves 时**必须** `leaf.view instanceof MyView`，不能 `getViewType()` + cast；
- 需要访问视图实例时 `await workspace.revealLeaf(leaf)`；
- 或在确有必要时 `await leaf.loadIfDeferred()`（性能警告：会取消该视图的延迟加载优化）。

**官方另一条硬性要求**（《Views》指南原文警告）："**Never manage references to views in your plugin. Obsidian may call the view factory function multiple times.**" 必须每次用 `getLeavesOfType()` 现查。

### 4.2 Commands

`addCommand` 支持 `callback` / `checkCallback` / `editorCallback` / `editorCheckCallback`（`obsidian.d.ts:2928`、`2955`）。`editorCallback` 的签名是：

```ts
editorCallback?: (editor: Editor, ctx: MarkdownView | MarkdownFileInfo) => any;
```

`removeCommand(commandId)` 在 1.7.2 起公开，用于动态生成命令（比如"跳转到 Figure 3"这类）。

### 4.3 CodeMirror 6 集成：稳定性评估

**稳定的一面**：
- `Plugin.registerEditorExtension(extension: Extension): void`（`@since 0.12.8`）是**公开稳定 API**，参数类型 `Extension` 直接来自 `@codemirror/state`。
- Obsidian 官方文档《Editor extensions》明确："Obsidian **uses CodeMirror 6 (CM6)** to power the Markdown editor" 且 "an Obsidian editor extension is the same thing as a CodeMirror 6 extension"。
- 两把官方钥匙：`editorEditorField: StateField<EditorView>`、`editorInfoField: StateField<MarkdownFileInfo>`、`editorLivePreviewField: StateField<boolean>`。

**不稳定的一面**（这是风险核心）：

| 风险 | 证据 |
|---|---|
| 拿到底层 `EditorView` 要走私有字段 | 官方《Communicating with editor extensions》原文：`// @ts-expect-error, not typed` + `const editorView = view.editor.cm as EditorView;`。`grep "cm:" obsidian.d.ts` = 0 命中 |
| CM6 版本被 Obsidian 锁定、且 npm peer 依赖是**精确版本** | `obsidian@1.14.4` 的 `peerDependencies`：`@codemirror/state: "6.7.6"`、`@codemirror/view: "6.43.13"`（无 `^`）。插件若自带另一份 CM6，会得到两份实例、`instanceof` 失效 |
| Live Preview 的渲染由 Obsidian 内部扩展掌管，扩展顺序/优先级无公开契约 | 官方《Decorations》/《State fields》指南只给了扩展写法，没有给"与其他插件扩展的相对顺序保证" |
| 语法树节点名会变 | 1.15.0 changelog 明确改了 closing token 的节点名，并点名"Plugins that match full node names … will miss closing tokens" |
| 扩展只能影响编辑体验，**不能作为数据源** | 扩展是视图层；要落盘必须走 `Vault.process()` |

**判断**：CM6 扩展适合做**编辑态的视觉增强**（如给 `[@fig:3]` 上色、提供引用自动补全的 `EditorSuggest`），**不适合**作为编号/引用正确性的唯一实现——正确性必须由可独立测试的纯函数模块承担（见 §7）。

### 4.4 其他渲染入口

| 入口 | 适用场景 | 依据 |
|---|---|---|
| `registerMarkdownPostProcessor` | 阅读视图的后处理 | `obsidian.d.ts:7257`；官方《Markdown post processing》 |
| `registerMarkdownCodeBlockProcessor(language, handler)` | 自定义代码块（如 ```fig-panel```） | `obsidian.d.ts:7277` |
| `Base` 代码块（```` ```base ````） | 内嵌一个 Bases 查询 | `https://help.obsidian.md/bases/create-a-base` 原文："Bases can also embedded directly into a note using a `base` code block" |
| `![[File.base#View]]` | 内嵌 `.base` 文件的某个视图 | 同上 |

---

## 5. Bases 能力边界（重点）

### 5.1 Bases 是什么

- **核心插件**（core plugin），非社区插件。原文："Bases is a [[Core plugins|core plugin]] that lets you create database-like views of your notes."（`https://help.obsidian.md/bases`）
- 数据**只**来自本地 Markdown 文件 + 其 properties。没有独立数据库。
- 一个 `.base` 文件 = 一份 schema（filters/formulas/properties/summaries/views），可内嵌为 ```` ```base ```` 代码块。
- 布局（官方与版本）：Table（1.9）、Cards（1.9）、List（1.10）、Kanban（1.14）、Map（1.10，需 Maps 插件）。
- **每行 = 一个文件**：`export class BasesEntry { file: TFile; getValue(propertyId): Value | null; }`。

### 5.2 逐项回答任务书中的四个问题

| 问题 | 结论 | 证据 |
|---|---|---|
| 按 frontmatter 过滤/排序/分组 | **可以**。过滤：`filters`（`and`/`or`/`not` 嵌套）；排序：`getSort(): BasesSortConfig[]`，`direction: 'ASC' \| 'DESC'`，多键；分组：`groupBy` + `groupOrder`（1.14.3），**但每个视图只能按一个属性分组** | `BasesConfigFile`、`BasesViewConfig.getSort()`；帮助文档《Views》原文 "Each view can have several sorts, but can group results by only one property." |
| 展示关系型数据 | **部分可以，且只是"单跳链接"。** wikilink 值被解析为 `Link`，支持 `link.asFile()`、`link.linksTo(file)`、`file.hasLink(other)`、`authors.contains(this)`、`file.backlinks`。**没有** join、没有反向遍历的多跳查询、`file.backlinks` 被官方标为 "performance heavy"，且 "Does not automatically refresh results when the vault is changed" | `https://help.obsidian.md/bases/functions`（Link 类型 / File 类型）；`https://help.obsidian.md/bases/syntax` 的 `### File properties` 表格 |
| 自定义列渲染 | **可以，但必须写插件。** 原生只有"属性列"（属性值按 `Value.renderTo(el, ctx)` 渲染）+ 汇总行 + 分组。要在列里画进度条、编号徽章、diff 视图，必须 `registerBasesView` 自己实现整个 `BasesView.onDataUpdated()` | `BasesView` / `Value.renderTo`；`https://docs.obsidian.md/plugins/guides/bases-view` |
| 跨文件聚合 | **可以做"汇总"，不做"关联聚合"。** 聚合手段：`formulas`、`summaries`（内置 Sum/Avg/Median/Stddev/Earliest/Latest 等 + 自定义 formula，如 `values.reduce(...)`）、`List` 类型的 `filter/map/reduce/join/unique/sort`。**但没有跨文件的"按 key 连接两张表"**——不存在 join 函数 | `https://help.obsidian.md/bases/views/table` 的 `### Built-in summaries`；`https://help.obsidian.md/bases/functions` 的 `## List type` |

### 5.3 Bases vs Dataview

| 维度 | Obsidian Bases（官方核心） | Dataview（社区插件） |
|---|---|---|
| 归属 | 官方，内核内置 | 社区插件，需用户自行安装并启用 |
| 查询语言 | `.base` 文件（YAML-ish），过滤/公式用**自定义表达式语言**（`file.hasTag(...)`、`now() - "1 week"`） | DQL（`TABLE ... FROM ... WHERE ...`）+ JS API（`dataviewjs`） |
| 类型系统 | 独立的 `Value` 层级（`LinkValue`/`DateValue`/`ListValue`/…），**前端类型化**（frontmatter 的 wikilink 自动成为 `Link`） | 前端类型化，规则不同（引号→text、ISO→date、YAML object→object） |
| 视图 | Table/Cards/List/Kanban/Map，全部内核内置，**可通过 `registerBasesView` 扩展** | 表格/列表/任务/日历（靠社区或 dataviewjs 自绘） |
| 插件 API | **有**（1.10.0 起 `registerBasesView`） | 只通过 `await window.app.plugins.plugins["dataview"].api` 之类的运行时访问，**非官方契约** |
| 可用性 | 依赖 app 版本，且需用户在核心插件里启用 Bases（`registerBasesView` 在未启用时**返回 `false`**） | 依赖用户安装了该社区插件 |
| 长期维护 | 官方承诺（内核功能） | 社区维护 |

> **对本项目的意义**：Bases 是**唯一有官方插件扩展点**的结构化查询 UI。Dataview 只能作为"用户可选增强"，**绝不能作为系统依赖**。

### 5.4 明确回答：Bases 能否承担 Figure/Panel/Reference 的结构化数据展示？

**分情况，但每个情况都有明确结论：**

| 场景 | Bases 能否承担 | 必须自建的是 |
|---|---|---|
| **1. Reference 库**（每条文献一个 `.md`，frontmatter 存 `authors`、`year`、`doi`、`journal`、`cited_in` 等） | ✅ **能**。Table 视图 + 多列排序 + 分组 + 内置汇总，完全够用；`link` 值可点开文献笔记 | 不需要自建视图。需要自建的是**数据写入与校验**（DOI 去重、作者名规范化） |
| **2. Figure 清单**（每个图一个 `.md`，frontmatter 存 `figure_number`、`caption`、`panel_count`、`source_file`、`section`） | ✅ **能**（前提：一图一文件） | 编号一致性、跨文件重编号、与正文引用的双向一致性校验，**Bases 不做** |
| **3. Panel 明细**（一个 Figure 下有 4–8 个 panel，每个 panel 有 label/描述/来源图片/像素坐标） | ❌ **不能作为主视图**。Bases 的行 = 文件，Panel 若只是 Figure 文件里的一个 YAML 列表元素，Bases **无法逐 panel 出一行**。可以 `List` 展开成一格（`values.join()`），但**不能排序/筛选/选中单个 panel** | 必须自建 `BasesView`（能读 `entry.getValue('note.panels')` 得到 `ListValue` 然后自己画）或 `ItemView`；或者把 Panel 拆成独立文件（会制造大量小文件，见风险 R3） |
| **4. 交叉引用校验表**（"正文出现 `[@fig:3a]`，但 Figure 3 没有 panel a"） | ❌ **不能**。Bases 无法读正文内容做匹配，也无法执行"校验"逻辑；formula 只能基于 frontmatter 字段的算术/字符串/列表操作 | 校验逻辑必须在插件（或外部工具）里实现，结果可写回 frontmatter 供 Bases 显示 |
| **5. 审稿意见 / 修订轮次追踪**（Issue → 定位段落 → Patch → Response） | ⚠️ **部分能，不建议**。Issue 若一个文件一条，Table + Kanban（按 status 分组）可以当看板用；但"定位段落"需要稳定锚点（block id），"Patch"需要行级 diff，"Response"需要与 Issue 的多对多关系——这些 Bases 都表达不了（无 join、无多对多、无 diff） | 自建 `ItemView`（三栏：Issue 列表 / 正文定位 / Response 编辑器），或完全在 Obsidian 之外 |

**总判定**：**Bases 能承担"Figure/Reference 的只读结构化浏览"，不能承担"Panel 级明细、交叉引用校验、修订闭环"。** 后三者必须自建 View 或放到宿主之外。

---

## 6. 依赖与运行时约束

### 6.1 打包形态

**已证事实**：
- 官方《Build a plugin》：插件目录放在 `<vault>/.obsidian/plugins/<id>/`，"now has a `main.js` file that contains a compiled version of the plugin"。
- `manifest.json` 的 `isDesktopOnly`：官方 Manifest 文档原文 "Whether the plugin can only be used on the desktop app, **for example because it uses NodeJS or Electron APIs**"。
- 社区插件目录的安装形态是"下载 `main.js` + `manifest.json`（+ 可选 `styles.css`）到插件目录"。
- Obsidian 内置了 `moment`（`import * as Moment from 'moment'` 在 `obsidian.d.ts` 顶部；官方《Events》指南原文 "Obsidian uses Moment internally, so you don't need to install it yourself"）。

**推论（高置信）**：
- **单文件 `main.js`**：由 esbuild/rollup 打成单文件 IIFE/CJS，**没有 `node_modules` 运行时解析**。任何在运行时 `require('some-pkg')` 的代码都会失败，除非被打进 bundle。
- **不能有动态 chunk / code splitting**（除非自己处理加载）。
- **不能有 native addon**（`.node` 文件），因为目录里只分发 `main.js`。
- 样式放 `styles.css`，由 Obsidian 自动注入。

### 6.2 可用 / 不可用的依赖

| 类别 | 桌面端 | 移动端 | 判定依据 |
|---|---|---|---|
| 纯 JS 库（无 Node 内置模块） | ✅ | ✅ | 无 platform 依赖 |
| 依赖 Node 内置（`fs`/`path`/`crypto`/`buffer`/`stream`/`zlib`） | ⚠️ 桌面端运行时**可以** `require`（Electron 环境自带），但**不属官方 API 契约**；打包时必须把 Node 内置标为 external，且第三方库若在**模块顶层**调用它们，移动端会导致插件崩溃 | ❌ | 官方《Mobile development》原文："The Node.js API, and the Electron API aren't available on mobile devices. Any calls to these libraries made by your plugin **or it's dependencies** can cause your plugin to crash." |
| `child_process`（调用外部程序） | ⚠️ Electron 里可 `window.require('child_process')`，**非公开 API** | ❌ | 同上；且 `obsidian.d.ts` 中 0 命中 |
| native addon（`.node`、sqlite3 原生绑定、canvas 原生） | ❌（目录只分发 `main.js`，无平台二进制分发机制） | ❌ | 分发形态所限 |
| WASM（如 sql.js、pdfium-wasm） | ✅ | ✅ | 单文件内联或作为插件自带资源；**但需自行确认 Obsidian 对插件目录内资源加载的支持**（见未确认事项 U4） |
| Web Worker | ⚠️ 桌面可，移动端可用性未证 | ? | 官方《Manage plugin lifecycle》把 "web workers" 明列为"需要显式清理的资源"，说明可用；但未给出移动端保证 |
| 正则 lookbehind | ✅ | ⚠️ iOS < 16.4 不支持 | 官方《Mobile development》原文 |
| `at codemirror/*` | ✅（必须与宿主同版本） | ✅ | peerDependencies 精确版本 6.7.6 / 6.43.13 |

### 6.3 外部进程（Python 解析 DOCX）的可行性

| 维度 | 桌面端 | 移动端 |
|---|---|---|
| 技术可行性 | ✅ **推测可行**：Electron 渲染进程可通过 `window.require('child_process')` 或 `require('electron').ipcRenderer` 走主进程 exec。**属 C 类私有 hack**：不在 `obsidian.d.ts`，不在官方文档，不在 changelog 的保障范围 | ❌ **不可行**。官方明文：移动端没有 Node.js / Electron API；沙箱里没有本地进程概念 |
| 分发可行性 | ⚠️ 差。插件目录只分发 `main.js`，**无法携带 Python 解释器或已编译的 `python.exe`**；只能要求用户**自行**在系统 PATH 上装有 Python + 依赖，插件运行 `python script.py` | ❌ |
| 安全/合规 | ⚠️ 社区插件审核对"执行外部程序"极敏感，官方政策文档（Community directory / Developer policies）需要单独核对（本次未逐条审计） | ❌ |
| 稳定性 | ⚠️ 路径含空格/中文/CJK、Windows 无 Python、Conda 环境、杀软拦截，都是常见故障点 | — |

**结论**：**"在 Obsidian 插件里调用 Python 解析 DOCX"只可能是桌面端的私有方案，且需要用户自备 Python 环境。** 正确做法是把 DOCX 解析放到 **Obsidian 之外**（独立 CLI / 本地服务），插件只消费其产出（写好的 Markdown + 附件 + 一份索引 JSON）。这也顺带解决移动端问题——移动端直接标记为不支持导入，只做查看。

### 6.4 文件 I/O 约束

- **只有异步 API**：`Vault.cachedRead/readBinary/process/modify`、`DataAdapter.read/write/readBinary/writeBinary/append/process` 全部返回 `Promise`。**没有同步读**。
- **读改写必须用 `process()`**：官方《Vault》原文 "`Vault.process()` … **guarantees that the file doesn't change between reading the current content and writing the updated content**. **Always prefer** `Vault.process()` over `Vault.read()`/`Vault.modify()` to avoid unintentional loss of data."
- **`cachedRead` vs `read`**：官方原文 "If you only want to display the content to the user, then use `cachedRead()` … If you want to read the content, change it, and then write it back to disk, then use `read()` to avoid potentially overwriting the file with a stale copy."
- **隐藏文件**：官方《Vault》原文 "The Vault API only allows access to the files visible inside the app, **files included in hidden folders can only be accessed using the Adapter API**." → 插件的私有数据放在 `.obsidian/plugins/<id>/` 时，必须走 `adapter`，不能走 `vault`。
- **移动端 `getBasePath()` 不可用**：`FileSystemAdapter.getBasePath()` 只在桌面适配器上；移动端是 `CapacitorAdapter`（类型条目存在）。**任何需要绝对路径的逻辑必须 `instanceof FileSystemAdapter` 守卫。**
- **附件路径**：`FileManager.getAvailablePathForAttachment(filename, sourcePath?)`（`@since 1.5.7`）是官方推荐的"安全占位路径"。

---

## 7. 系统模块划分建议（Obsidian 侧职责 / 非 Obsidian 侧职责）

### 7.1 划界原则

三条来自上文事实的硬边界：

1. **Obsidian 无事务、无 schema 校验、无规则引擎** → 任何"正确性"（编号唯一、引用可解析、审稿闭环完整）**不能**只存在于 Obsidian。
2. **Obsidian 无同步 I/O、无外部进程（移动端）、无 join** → 任何"重计算"（DOCX 解析、全文索引、跨表关联、diff）**不能**放在插件里跑。
3. **Bases 的行=文件** → 任何"一文件多实体"（Figure→Panels、Issue→多条 Patch）都**必须**自建视图。

### 7.2 职责分工

#### Obsidian 侧【应承担】

| 职责 | 实现手段 | 证据 |
|---|---|---|
| Markdown 的**编辑与阅读** | 内置 | — |
| frontmatter 的**受控写入**（原子读改写） | `FileManager.processFrontMatter` + `Vault.process` | `obsidian.d.ts:4450`；官方《Vault》 |
| **只读**的结构化浏览（Figure / Reference / Issue 列表） | Bases（Table / Cards / Kanban / List）+ 少量 formula | §5 |
| **展示**校验结果（"第 3 图 panel b 悬空"） | 写回 frontmatter 的 `status` 字段 + Bases 着色；或 `BasesView` 自绘 | §5.2 |
| **编辑态提示**（引用自动补全、`@fig:` 高亮、跳转） | `EditorSuggest` + `registerEditorExtension`（装饰）+ `addCommand` | §4.3 |
| **内嵌代码块**渲染（如 ```` ```panel-table ````、```` ```base ````） | `registerMarkdownCodeBlockProcessor` | §4.4 |
| **打开/跳转/悬停预览** | `workspace.openLinkText`、`registerHoverLinkSource`、`hover-link` 事件 | 官方 Bases View Guide 示例 |
| **向用户发通知** | `new Notice(...)` | `obsidian.d.ts:6728` |
| **调用本地服务的 HTTP** | `requestUrl`（绕过 CORS） | `obsidian.d.ts:7841` |
| **可选**：驱动本地服务的业务操作（点击"生成修订包"调 `requestUrl`） | `requestUrl` + `Notice` + 进度条 | — |

#### Obsidian 侧【不应承担】

| 不应承担 | 原因 | 应放在哪里 |
|---|---|---|
| DOCX / LaTeX / PDF 解析 | 移动端无 Node/进程；桌面端 `child_process` 是 C 类私有 hack；插件不能携带解析器 | 外部 CLI / 本地服务 |
| 编号分配与全局唯一性保证 | Obsidian 无事务、无锁；两个插件实例并发写会互相覆盖 | 外部工具做"分配"，插件只做"落盘" |
| 全文索引 / 语义检索 | MetadataCache 无全文索引；插件内自建索引在大 vault 会拖慢启动 | 外部服务 |
| 跨文件 join / 关系查询 | Bases 无 join；MetadataCache 只有单跳 `resolvedLinks` | 外部服务（SQLite / 内存图） |
| Markdown / DOCX 的**往返转换** | 保真度问题属于转换器职责；插件不可能同时守住两套渲染 | 外部转换器（如 Pandoc / 自研） |
| 审稿意见的**状态机与多对多关系**（Issue ↔ Patch ↔ Response） | frontmatter 是"每文件一份"的扁平字典；无 join、无多对多 | 外部数据层；Obsidian 只镜像成"每个 Issue 一个 md"用于浏览 |
| 版本快照与回滚 | 无 VCS 集成；只能靠外部 git / 文件系统快照 | 外部版本控制 |
| 移动端导入 | 移动端无进程、无 Python | 明确不支持，只做查看 |

### 7.3 推荐的内部分层（Obsidian 插件侧）

```
┌─────────────────────────────────────────────────────────┐
│  Presentation                                            │
│  - Bases 视图 (内置 Table/Cards/Kanban)                   │
│  - 自定义 BasesView (Panel 明细 / 校验面板)               │
│  - ItemView (修订三栏视图)                                │
│  - Editor extension (装饰 + 补全)                         │
│  - Code block processor                                   │
└───────────────────▲─────────────────────────────────────┘
                    │ 只读渲染契约（纯数据 → DOM）
┌───────────────────┴─────────────────────────────────────┐
│  Adapter / Ports  (C 类 hack 全部收敛于此)                │
│  - VaultPort: cachedRead / process / processFrontMatter   │
│  - MetadataPort: getFileCache + changed/resolve 事件       │
│  - ServicePort: requestUrl → 本地服务 (可选，可缺失)       │
│  - EditorPort: view.editor.cm (带能力探测 + 降级)         │
└───────────────────▲─────────────────────────────────────┘
                    │ 纯函数 / 无 DOM
┌───────────────────┴─────────────────────────────────────┐
│  Domain (可在 Node 下单元测试，不 import obsidian)        │
│  - frontmatter schema 归一化与校验                        │
│  - 编号规则 / 交叉引用解析                                │
│  - 反向链接索引推导                                       │
│  - 视图模型构建 (FigureView[], PanelView[], IssueView[])  │
└─────────────────────────────────────────────────────────┘
```

**硬性要求**：Domain 层**不允许** `import { ... } from 'obsidian'`。所有 Obsidian 能力通过 Port 注入。这样：
- Domain 可以在 Node 下用 vitest/jest 直接测；
- 同一份 Domain 可以被外部 CLI（处理 DOCX 导入）复用；
- 未来若换宿主（VS Code / 独立 App），只需重写 Adapter。

---

## 8. 技术风险

至少 5 条，按影响排序。

| ID | 风险 | 触发条件 | 影响 | 缓解 | 置信度 |
|---|---|---|---|---|---|
| **R1** | **frontmatter 是无类型 `any` 字典，且属性类型 vault 全局共享** | 同一字段（如 `year`）在不同稿件里想表达"出版年"和"实验年"；或想写 `{a: {b: 1}}` 嵌套 | 数据静默错乱；Bases/Dataview/原生搜索对同一值解释不同；改一个文件的属性类型会**影响全 vault**（官方文档原文） | 强制 schema 注册表（字段名 → 类型 → 允许值域），写入前校验；禁止嵌套（官方不支持）；日期统一 ISO 字符串；链接统一加引号 | 高 |
| **R2** | **MetadataCache 竞态导致"写完即读"拿到旧数据** | `processFrontMatter` 之后立刻 `getFileCache`；rename 后按路径缓存失效；启动窗口期 `create` 风暴 | 编号重复、引用指向旧目标、启动时对全 vault 做错误的"新增"处理 | 所有写后读 await `changed`（带超时）；rename 时重映射自有索引；vault 事件注册放 `onLayoutReady` | 高 |
| **R3** | **"一文件一实体"的陷阱**：为让 Bases 能展示 Panel，把每个 Panel 拆成独立 md | >10k notes 级别的 vault + 每图 4–8 panel | 文件爆炸；`metadataCache` 压力；Obsidian 官方已承认大 vault 有 properties 重算卡顿（1.14.4 修复单例） | Panel 留在 Figure 文件的 frontmatter list 里；用自建 `BasesView` 展开渲染；只有确实需要独立生命周期时才拆文件 | 高 |
| **R4** | **依赖 C 类私有 API**（`view.editor.cm`、`child_process`、Electron） | 编辑器深度集成 / 桌面端调用 Python | 任意次要版本更新即可静默失效，且无类型报错、无 changelog 提示 | 收敛到单一 Port + 能力探测（`try/catch` + `typeof` 检查）+ 显式降级 + 启动时自检一次并在 `Notice` 中告知用户 | 高 |
| **R5** | **移动端不可用面被低估** | 插件依赖 Node 内置模块、`getBasePath()`、进程、lookbehind 正则 | Android/iOS 上插件崩溃（官方原文） | `isDesktopOnly: true`，或全链路 platform 分支；CI 里用 `app.emulateMobile(true)` 手测（官方《Mobile development》） | 高 |
| **R6** | **Bases 依赖用户启用核心插件** | 用户在核心插件里关掉 Bases | `registerBasesView(...)` **返回 `false`**，视图不出现（`obsidian.d.ts:7279` 注释） | 检查返回值并降级到 `ItemView`；不得把 Bases 作为唯一入口 | 高 |
| **R7** | **插件目录只分发 `main.js`，无法携带二进制（`.node`）或外部解释器** | 需要 Python、原生 addon、模型权重 | 功能无法分发 | 外部依赖一律放到宿主外部（本地服务 / CLI）；插件只通过 `requestUrl` 消费 | 中（"只分发 main.js/manifest.json/styles.css"是官方教程与社区目录的既有形态，但官方文档未逐字写成禁令；见 U4） |
| **R8** | **CM6 双实例** | 插件 `npm i` 了与宿主不同的 `@codemirror/*` 版本 | `StateField`/`Decoration` 在不同 realm，`instanceof` 与合并失败，编辑态异常 | 锁定 peer 版本（6.7.6 / 6.43.13），bundler 中 `external` 掉 `@codemirror/*` | 高 |
| **R9** | **插件加载阻塞启动** | `onload` 里做全 vault 扫描；自定义 View 构造函数里读数据 | 官方原文："Obsidian loads all plugins **before the user can interact with the app**"；deferred views 会被取消 | `onload` 只注册；数据加载放 `onLayoutReady`；View 构造函数零副作用 | 高 |

---

## 9. 未确认事项

以下各项**本次未取得直接证据**，不得在架构文档中当作已证事实使用。

| ID | 未确认事项 | 为什么没确认 | 建议的验证方式 |
|---|---|---|---|
| **U1** | `MetadataCache` 在 10k–50k 文件 vault 上的**具体**索引耗时、`getFileCache` 的平均延迟 | 需要实机测量；本环境无 Obsidian 运行时 | 建一个 20k 文件的合成 vault，测 `onLayoutReady` → 首个 `resolved` 的时间，以及遍历 `getFileCache` 的总耗时 |
| **U2** | `frontmatter` 里**未加引号**的 `[[Link]]` 是否被解析为 `frontmatterLinks` | 官方帮助文档要求加引号，`FrontmatterLinkCache` 示例也加引号；但未实测不加引号时的行为（YAML 里 `[[a]]` 是 flow sequence 嵌套，可能被解析成 `[['a']]`） | 实机写一个 vault 文件，`console.log(app.metadataCache.getFileCache(f))` 观察 `frontmatter` 与 `frontmatterLinks` |
| **U3** | `processFrontMatter` 对**日期、null、嵌套**字段的 round-trip 保真度（是否会把 `2020-08-21` 写回成 `"2020-08-21"`） | 官方只说明"JSON 会以 YAML 保存"，未说明类型保留 | 实机 round-trip 测试 |
| **U4** | Obsidian 插件目录内**嵌套子目录/资源文件**（如 `data/xxx.json`、`data/x.wasm`）的加载约束 | 官方文档只展示 `main.js`/`manifest.json`/`styles.css`，未说明资源目录规则 | 实机测试 + 查阅社区目录 Submission requirements |
| **U5** | Web Worker 在移动端 Obsidian 的可用性 | 官方《Manage plugin lifecycle》提到 web worker 需清理，但未讨论移动端 | `Platform.isMobileApp` 分支实测 |
| **U6** | `QueryController`（Bases）未来是否会公开成员 | 目前是空类；无路线图信息 | 跟 `obsidian-api` 仓库 changelog |
| **U7** | `BasesView` 中 `createFileForView` 的副作用边界（是否会触发 `create` 事件风暴） | 类型只有签名 | 实测 |
| **U8** | 1.15.x 的 changelog 中是否还有未进入 `obsidian.d.ts` 的 API 变更（npm 包只到 1.14.4） | 类型包滞后于 app | 待 `obsidian@1.15.x` 发布后比对 |
| **U9** | 社区插件审核政策是否允许"调用外部 Python 进程"（即使 `isDesktopOnly`） | 未逐条审计 `Community directory/Developer policies` | 审计该文档 |
| **U10** | `FileSystemAdapter.instanceType` 等运行时判型字段是否稳定 | 类型里有 `instanceType` 但文档未承诺 | 用 `adapter instanceof FileSystemAdapter` 而非 `instanceType` |
| **U11** | 自定义 `BasesView` 在**嵌入式** base（``` ```base ``` 代码块）里是否同样被调用、`containerEl` 语义是否一致 | Guide 只演示了 `.base` 文件 | 实测嵌入式 base 的 `factory` 调用 |

---

## 10. 证据清单

### 10.1 类型定义（`obsidian.d.ts`）

完整摘录见 `research/obsidian/evidence/obsidian-dts-excerpts.md`。基线：

- 文件：`obsidian-api@master/obsidian.d.ts`，git blob sha `10b31c4787fbc3ee4b228ca403165bbf865eb165`，11,539 行，SHA-256 `97c86417c893db691e401fdffd9026e348dc96da6bfcfa5d49a301d7fe7542a0`
- 包：`https://registry.npmjs.org/obsidian/-/obsidian-1.14.4.tgz`，sha1 `e4d4c91d…`，内 `obsidian.d.ts` sha1 `232da70b…`
- 二者 diff：仅 5 处 JSDoc 措辞（sidebar→sidedock），类型签名一致

关键行号 → 内容 → 本报告引用章节：

| 行号 | 符号 | 引用章节 |
|---|---|---|
| 1319 | `export let apiVersion: string` | §2.1 |
| 7376-7425 | `PluginManifest` | §2.2 |
| 2391-2550 | `CachedMetadata`（13 字段） | §3.4, §3.5 |
| 4832-4843 | `FrontMatterCache`（仅 `[key: string]: any`） | §3.1 |
| 4887-4900 | `FrontmatterLinkCache extends Reference { key: string }` | §3.2 |
| 5060 | `getFrontMatterInfo(content): FrontMatterInfo` | §3.1 |
| 6446-6535 | `MetadataCache`（getFileCache/on changed/deleted/resolve/resolved, resolvedLinks） | §3.4, §3.5 |
| 4450 | `FileManager.processFrontMatter(file, fn: (fm: any)=>void, opts?)` | §3.1, §7.2 |
| 10382 | `Vault.process(file, fn: (data: string)=>string, opts?)` | §6.4 |
| 10188 | `Vault.adapter: DataAdapter` | §6.4 |
| 3181-3330 | `DataAdapter`（全异步） | §6.4 |
| 4492 | `FileSystemAdapter.getBasePath()` | §6.3, §6.4 |
| 10460-10600 | `View`（containerEl / scope / onPaneMenu） | §4.1 |
| 5391-5416 | `ItemView`（contentEl / addAction） | §4.1 |
| 7219 | `registerView(type, viewCreator)` | §4.1 |
| 7279-7283 | `registerBasesView(...): boolean`（未启用 Bases 返回 false） | §5.3, R6 |
| 7299 | `registerEditorExtension(extension: Extension)` | §4.3 |
| 3930-3937 | `editorEditorField` / `editorInfoField` / `editorLivePreviewField` | §4.3 |
| 3652 | `export abstract class Editor`（**无 `cm` 字段**） | §4.3, §2.4 |
| 1459-2290 | Bases 全套类型 | §5 |
| 7643 | `QueryController extends Component { }`（空类） | §5.2, §2.4 |
| 10092-10140 | `Value` 基类（`renderTo`/`isTruthy`/`toString`） | §5.2 |
| 7041+ | `Platform`（isDesktop/isMobile/isIosApp/isAndroidApp…） | §6.2 |

### 10.2 官方开发者文档

| URL | 本报告引用点 |
|---|---|
| `https://docs.obsidian.md/Reference/Manifest` | `minAppVersion` / `isDesktopOnly` 必填；`id` 命名规则 |
| `https://docs.obsidian.md/Reference/Versions` | `versions.json` 语义 |
| `https://docs.obsidian.md/plugins/guides/bases-view` | 自定义 Bases 视图的官方完整示例；"An unfiltered Base will provide an entry for every file in the vault, so your view should be able to handle thousands of entries" |
| `https://docs.obsidian.md/plugins/guides/load-time` | `onload` 只注册；`vault.on('create')` 会为每个文件触发；`onLayoutReady` |
| `https://docs.obsidian.md/plugins/guides/defer-views` | 1.7.2 deferred views；`instanceof` 守卫；`loadIfDeferred()` |
| `https://docs.obsidian.md/plugins/guides/lifecycle-management` | `Component` 生命周期；web worker 属需清理资源 |
| `https://docs.obsidian.md/plugins/editor/editor-extensions` | "Obsidian uses CodeMirror 6 (CM6)"；`registerEditorExtension` |
| `https://docs.obsidian.md/plugins/editor/communicating-with-editor-extensions` | **`view.editor.cm` 的 `@ts-expect-error, not typed`** |
| `https://docs.obsidian.md/plugins/user-interface/views` | ItemView 写法；"Never manage references to views in your plugin. Obsidian may call the view factory function multiple times." |
| `https://docs.obsidian.md/plugins/vault` | `cachedRead` vs `read`；`process()` 原子性；隐藏目录需 Adapter；`TFile`/`TFolder` 判型 |
| `https://docs.obsidian.md/plugins/events` | `registerEvent`；`moment` 内置 |
| `https://docs.obsidian.md/plugins/getting-started/build-a-plugin` | 插件目录形态、`main.js` |
| `https://docs.obsidian.md/plugins/getting-started/mobile-development` | "The Node.js API, and the Electron API aren't available on mobile devices … can cause your plugin to crash"；lookbehind；`isDesktopOnly` |
| `https://docs.obsidian.md/plugins/guides/manage-plugin-lifecycle` | 资源清理清单 |

### 10.3 官方用户文档（help.obsidian.md）

| URL | 本报告引用点 |
|---|---|
| `https://help.obsidian.md/properties` | 7 种属性类型；**属性类型 vault 全局共享**；wikilink 必须加引号；Markdown-in-properties 不支持；Nested properties 不支持；JSON→YAML；1.9 起单数别名移除 |
| `https://help.obsidian.md/bases` | Bases 是 core plugin；数据只来自本地 md + properties；视图可被社区插件扩展 |
| `https://help.obsidian.md/bases/views` | 视图布局与版本；过滤组件；**每视图只能按一个属性分组**；排序可多键 |
| `https://help.obsidian.md/bases/views/table` | 内置汇总（Sum/Avg/Median/Stddev/Earliest/Latest…）；自定义 summary 用 formula |
| `https://help.obsidian.md/bases/syntax` | `.base` 结构；`file.*` 属性表（含 `file.backlinks` 的 "performance heavy" 与 "Does not automatically refresh"）；**frontmatter 里的 wikilink 自动成为 Link 对象**；`this` 的三种语义 |
| `https://help.obsidian.md/bases/functions` | 全局函数；`link()`；Link/List/Object/File 类型函数（`filter/map/reduce/join`、`asFile`、`linksTo`、`hasLink`） |
| `https://help.obsidian.md/bases/create-a-base` | `![[File.base#View]]` 与 ```` ```base ```` 两种内嵌 |
| `https://help.obsidian.md/plugins/search` | Search properties：`[prop]` / `[prop:value]` / `[prop:null]` / OR / 比较 |
| `https://help.obsidian.md/bases/views/table` | 汇总 |

### 10.4 官方 changelog

| URL | 引用点 |
|---|---|
| `https://obsidian.md/changelog/2026-09-02-desktop-v1.14.0/` | "Fixed periodic input lag in large vaults caused by properties getting recomputed in the background." |
| `https://obsidian.md/changelog/2026-10-05-desktop-v1.14.4/` | Bases Kanban + Group 菜单；打开 vault 外文件 |
| `https://obsidian.md/changelog/2026-10-22-desktop-v1.15.0/` | 格式标记 token 节点名改变（点名会破坏匹配完整节点名的插件）；Mermaid→Pele |
| `https://obsidian.md/changelog/2026-11-03-desktop-v1.15.1/` | 最新桌面版本号 |
| npm 包内 `CHANGELOG.md`（`obsidian@1.14.4`） | 1.7.2 `onUserEnable` / `ensureSideLeaf` / deferred views；移除 `prepareQuery`/`fuzzySearch`；1.5.7 `onExternalSettingsChange` / `getFrontMatterInfo` / `View.scope`；1.4.0 Properties 化（`FrontMatterCache` 不再有 position；`frontmatterLinks`） |

### 10.5 第三方（仅用于对比，非依赖）

| URL | 引用点 |
|---|---|
| `https://blacksmithgu.github.io/obsidian-dataview/annotation/add-metadata/` | Dataview 的 frontmatter 类型推断规则（引号→text、ISO→date、YAML object→object）；"All YAML Frontmatter fields will be automatically available as Dataview fields" |

### 10.6 与任务书章节的对照（自检）

| 任务书要求 | 本报告位置 |
|---|---|
| §2.1 API 版本 / minAppVersion / changelog | 本文 §2.1–2.3 |
| §2.2 obsidian.d.ts 逐符号核实 | 本文 §2.4 表 + 证据文件逐条摘录 |
| §2.3 稳定 / 未文档化 / 不可用 三分 | 本文 §2.4 |
| §3.1 Properties 类型系统与解析行为 | 本文 §3.1 |
| §3.2 wikilink/list 在 Dataview / Bases / 原生搜索的差异 | 本文 §3.2 |
| §3.3 >10k notes 开销 | 本文 §3.3 |
| §4.1 MetadataCache 能/不能拿到什么 | 本文 §3.4 |
| §4.2 增量更新、resolved、失效、竞态 | 本文 §3.5 |
| §5.1 ItemView 边界（编辑器 / 任意 HTML / Canvas） | 本文 §4.1 |
| §5.2 CM6 集成方式与稳定性 | 本文 §4.3 |
| §6 Bases 能力评估 | 本文 §5（含 §5.4 明确结论） |
| §7 打包与依赖边界、外部进程 | 本文 §6 |
| §8 模块划分 / 宿主边界 | 本文 §7 |
