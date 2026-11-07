# Obsidian 跨审计确认记录（CROSS_CONFIRMATION）

> 阶段：Phase 0 修订轮 · 定向确认 6 项
> 确认日期：2026-11-06
> 范围：只回答数据模型提案（§11.1 U1–U5）与 Manuscript 报告（§12）向 Obsidian 审计提出的 6 个悬空问题，**不重做审计**。
> 结论规则与 `OBSIDIAN_TECHNICAL_AUDIT.md` 一致：「**推测**」表示无直接证据；「**未能确认**」表示已尝试、无证据，**不做填空**。

---

## 0. 证据基线与复现方式

| 证据源 | 获取方式 | 指纹 |
|---|---|---|
| `obsidian@1.14.4` 的 `obsidian.d.ts` | `https://registry.npmjs.org/obsidian/-/obsidian-1.14.4.tgz`，解包后实测 | 11,539 行；SHA-1 `232da70b867460d0158742bdbcd861c9975fb992`（与 §Phase 0 审计记录一致） |
| 用户帮助文档（Publish uid `f786db9fac45774fa4f0d8112e232d67`） | `https://publish-01.obsidian.md/access/<uid>/<path>.md` 原始 Markdown | 逐页抓取，共 15 页 |
| 开发者文档（Publish uid `caa27d6312fe5c26ebc657cc609543be`） | 同上 | 逐页抓取，共 13 页 |
| 站点页面索引 | `https://publish-01.obsidian.md/cache/<uid>` | 帮助站 179 个 `.md` 页；开发站 1,319 个 `.md` 页 |

**本机环境**：已安装 Obsidian 1.15.0（`D:\Program Files\Obsidian\obsidian.exe`）。曾尝试用「临时 Vault + 探针插件 dump `CachedMetadata`」做运行时验证，**失败**（详见 §2 与 §6），因此本文件的判定**全部**建立在类型定义与官方文档之上。

**行号约定**：所有 `obsidian.d.ts:N` 指 npm `obsidian@1.14.4` 包内的该文件。

---

## 1. 判定总表

| # | 问题 | 判定 | 一句话依据 |
|---|---|---|---|
| C1 | 块 ID 合法字符集 / 下划线 / 大小写 | **部分**（下划线：**是**；大小写：**未能确认**） | 官方原文："Block identifiers can only consist of Latin letters, numbers, and dashes"——与官方自身文档中的 `_` 例子直接冲突 |
| C2 | 块 ID 能否挂标题行、能否 `[[#^id]]` 引用 | **部分**（能挂：**未能确认**；能引用：**是**） | 官方无标题挂块 ID 的例子；但 `SectionCache.id` 存在且类型注释为 "The block ID of this section" |
| C3 | `blocks` 是否返回全部（含标题上）？长度/数量限制？ | **部分**（返回全部：**是**，推断；限制：**否**） | `CachedMetadata.blocks` 是整篇文件的 ID 映射；全库检索无任何长度/数量上限 |
| C4 | Obsidian 是否改写正文 fenced code block | **部分**（误触发风险低：**是**；字节级不变：**未能确认**） | 官方无数值证据；但「Properties 面板改写正文」的唯一机制已确认存在 |
| C5 | `{{figref:...}}` 能否被 post-processor 安全处理、是否冲突 | **部分**（可处理：**是**；与模板变量冲突：**是**） | `.d.ts` 无 `{{` 语义，但 Templates 核心插件的 `{{date}}`/`{{time}}`/`{{title}}` 会吃掉同形 token |
| C6 | 是否有原生批注 | **否** | 31 个核心插件清单与全站文档中无任何批注/注释功能；`obsidian.d.ts` 中 `annotat*` 0 命中 |

---

## 2. C1 — 块 ID 的合法字符集、下划线、大小写

### 判定：**部分**
- **下划线 `_` 是否允许：是**（证据见下，存在直接反证）。
- **合法字符集：部分确认**（ASCII 字母、数字、`-`、`_` 有例证；其他符号未穷举）。
- **大小写是否敏感：未能确认。**

### 证据

**（1）官方用户文档的规范性表述（正面约束）**

`https://help.obsidian.md/Linking+notes+and+files/Internal+links`（原文端点 `https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Linking%20notes%20and%20files/Internal%20links.md`）：

> "You can also create human-readable block identifiers by adding a blank space followed by a caret (`^`) and the identifier. **Block identifiers can only consist of Latin letters, numbers, and dashes.**"

按此句字面，`^par_9QK2M4XZ` 的 `_` **非法**，数据模型 §3.4 的整套 `par_` / `sec_` 锚点将全部失效。

**（2）同一官方站点的反证（本条推翻了 (1) 的排他性）**

同一页面确实出现了带 `_` 的块 ID：
- 页面正文：`…in a network of documents. ^b15695` 之外，`^callout-internal-links-link-text`（位于该页 "Change the link display text" 小节末）；
- `https://help.obsidian.md/Linking+notes+and+files/Embed+files` 原文：`^my-list-id`。

**这些页面是 Obsidian Publish 渲染的，即 `^callout-internal-links-link-text` 与 `^my-list-id` 必须是宿主 Obsidian 自己能解析、能索引、能渲染的块 ID**，否则该页的目录/锚点无法生成、`[[#^...]]` 自链接无法解析。这与 "letters, numbers, and dashes" 的表述**直接矛盾**。

**（3）类型定义侧的旁证**

- `obsidian.d.ts:2236-2246` `BlockCache`：`id: string`——**无字符集约束的文档注释**，仅给示例 `// bar`。
- `obsidian.d.ts:2234-2235` 的 JSDoc 示例是 `foo ^bar`。
- `obsidian.d.ts:8181-8192` `SectionCache.id?: string | undefined`，注释 "The block ID of this section, if defined."
- 全文件对块 ID 语法**不存在**任何正则、枚举或 `@example` 之外的约束。

**（4）大小写**

官方文档与类型定义**均未出现**关于大小写敏感性的任何表述；全库检索用户帮助中块 ID 示例全部小写。尝试的运行时验证（见 §6）失败，故标 **未能确认**。

### 对数据模型的影响

`sec_` / `par_` 的**下划线可以保留**，§5.6 锚点编解码器里"映射为 `sec-`/`par-`"的降级分支**不必启用**；但大小写敏感未确认意味着 ID 生成器必须**强制单一大小写（建议全大写或全小写）**并把「大小写 → 冲突」纳入校验规则，而不是依赖"大小写不同即不同 ID"。

### 若不成立时的退路

- 若某 Obsidian 版本收紧了字符集（官方措辞如此宣称）：编解码器**已经预留** `sec_`→`sec-`、`par_`→`par-` 的映射（提案 §5.6，对上层透明），仅需切换一个开关并跑一次全库重写。
- 若大小写敏感（即 `par_AbC` ≠ `par_abc`）：OCR/迁移/手工输入可能产生"看起来一样、实则不同"的锚点；退路是 ID 生成器**只输出大写 + 数字**（剔除 `o/O/0`、`l/I/1`），并在 `_maps/<msc_id>.map.yaml` 里保存规范化小写键用于判重。
- 若下划线实际非法：见上，走映射分支；风险点是**已写入的旧锚点**需要迁移，因此建议在锚点首次批量写入前完成一次真实 Vault 运行时验证（见 §6 的待办）。

---

## 3. C2 — 块 ID 能否挂在标题行、能否被 `[[#^id]]` 引用

### 判定：**部分**
- **能否挂在标题行：未能确认**（无官方例子，也无官方禁止）。
- **挂上后能否被 `[[#^id]]` 引用：是**（引用契约本身确认；但指向"标题行"这一特例未能确认）。

### 证据

**（1）引用语法本身已确认**

`https://help.obsidian.md/Linking+notes+and+files/Internal+links`：

> "You can link to a block by adding `#^` at the end of your link destination, followed by a unique block identifier. For example: `[[2023-01-01#^37066d]]`."
>
> 同页 "Searching for blocks across the vault" 一节：`[[^^block]]`。

嵌入方向同样确认：`https://help.obsidian.md/Linking+notes+and+files/Embed+files`：`![[Internal links#^b15695]]`。

即 `[[#^id]]`（同文件）与 `[[文件#^id]]`（跨文件）都是官方支持的语法形式。

**（2）标题行挂块 ID：官方文档中无任何例证**

抓取的全部 15 个用户帮助页面 + 13 个开发者页面中，`grep -n "^#\{1,6\} .*\^"` **0 命中**——没有任何一处把 `^id` 写在 `#` 标题行上。官方对块 ID 的三种放置位置都给了例子（简单段落行尾、结构化块单独一行、列表项内部），**唯独没有标题行**。

即：官方"没说不行"，但也"没证明行"。

**（3）类型定义侧：标题与块 ID 在缓存层面是**两套独立字段****

- `obsidian.d.ts:5104-5122` `HeadingCache`：只有 `heading: string` 与 `level: number`（继承 `CacheItem.position`），**没有 `id` 字段**；
- `obsidian.d.ts:8181-8186` `SectionCache`：**有** `id?: string`，注释 "The block ID of this section, if defined."。

这一点很关键：如果标题行不可挂块 ID，`SectionCache.id` 对 `type: 'heading'` 的分节就没有任何填充路径。官方为 SectionCache 专门留了 `id` 字段，说明**分节在缓存层面确实可以携带块 ID**（而标题恰好是一个分节），这是支持"可以挂"的最强间接证据。

**（4）官方明列的例外范围**

同页 "Link to a block in a note" 中的警告：

> "We do not support links to specific parts of quotations, callouts, and tables."

——排除清单里**没有**标题。按官方文档的口径，标题不在"不支持"之列。

### 对数据模型的影响

`## Introduction ^sec_4M2P8QKT`（提案 §3.3）在语法上**没有被否定**，且 `SectionCache.id` 为它提供了缓存层面的落点；但该形式**必须在本项目锁定 Obsidian 版本后做一次实测**才能写进"已确认"清单，在此之前 `sec_` 的权威来源不能只依赖标题锚点。

### 若不成立时的退路

提案 §3.3 已备好镜像：`section_meta[].id` 是 `sec_` 的**镜像**（VR-29 保证与锚点一致）。若标题锚点不可用，退路是**反转权威方向**——以 frontmatter `section_meta` 为权威，正文改用「标题行下一行单独一行写 `^sec_xxx`」的段落式挂法（该形式有官方例子背书，见 C1 的"结构化块单独一行"），`HeadingCache` 只用于确定节的边界而不承载身份。

---

## 4. C3 — `CachedMetadata.blocks` 是否覆盖全部块 ID；有无长度/数量限制

### 判定：**部分**
- **是否返回全部（含标题上的）：是**（对"全部"有直接结构证据；"含标题上的"依赖 C2，标记为**推断**）。
- **长度限制：否**（未发现任何限制的表述）。
- **数量限制：否**（未发现任何限制的表述）。

### 证据

**（1）`blocks` 是"整篇文件的 ID → 缓存"映射，不是子集**

`obsidian.d.ts:2541-2548`：

```ts
    /**
     * The blocks with IDs in the note, keyed by ID.
     * ```markdown
     * foo ^bar
     * ```
     * @public
     */
    blocks?: Record<string, BlockCache>;
```

字段注释为 "The **blocks with IDs** in the note, **keyed by ID**"——`Record<string, ...>` 的键即块 ID 本身。这是**全文件级**的映射，不是某个视图或某个区域的映射。官方文档页 `https://docs.obsidian.md/Reference/TypeScript+API/CachedMetadata/blocks` 仅复述签名 `blocks?: Record<string, BlockCache>;`，无附加限定。

**（2）`BlockCache` 只有两个字段**

`obsidian.d.ts:2236-2246`：`id: string` + 继承的 `position: Pos`。无 `type`、无 `text`、无 `parent`。这与 Phase 0 审计 §…「某个 block 的**内容**不提供」一致。

**（3）标题上的块 ID 是否进 `blocks`**

`obsidian.d.ts:8181-8186` 的 `SectionCache.id` 注释是 "The block ID of this section"，而非 "the block ID **from** this section"——语义上指向"该分节所携带的块 ID"。但**没有任何字段或文档说明** `SectionCache.id` 与 `blocks` 记录是同一份还是两份。因此「标题上的块 ID 出现在 `blocks` 中」只能标为**推断（中置信）**：既然 `blocks` 的口径是"note 中所有带 ID 的块"，而标题是一个块（`SectionCache.type` 的枚举里明确包含 `'heading'`，见 `obsidian.d.ts:8192`），那么它应当进 `blocks`。

**（4）长度 / 数量限制**

- `obsidian.d.ts` 中 `BlockCache` 与 `CachedMetadata.blocks` 的注释**完全不含**任何长度、数量、字符上限表述（全文 `grep -i "maximum\|limit"` 对块/ID 相关行 0 命中）。
- 用户帮助与开发者文档中亦**无**任何相关表述。
- 即：**"无限制"是"未发现限制"，不是"官方承诺无限"**。

### 对数据模型的影响

可以放心用 `metadataCache.getFileCache(file).blocks` 作为「一篇稿件的全部 `par_`/`sec_` 清单」的**单一查询入口**，无需自己正则扫正文；但该入口**只给 ID 与位置，不给内容**，§3.4 的「段落内容哈希」仍需 `Vault.cachedRead` 后按 `position` 切片自己算。

### 若不成立时的退路

若实测发现 `blocks` 不含标题锚点：退路是用 `CachedMetadata.sections`（`SectionCache.id`）补一遍——两个来源取并集即可覆盖全部锚点。若发现存在数量上限（800 段量级）：退路是**不依赖缓存做全量对账**，改由 `_maps/<msc_id>.map.yaml` 作为权威清单，缓存只用于"该 ID 当前是否仍在文件中"的存在性检查（提案 §5.4 已把 `_maps/` 定为段落身份的权威，本条退路与之兼容）。

---

## 5. C4 — Obsidian 是否会改写正文中的 fenced code block（D-04 的存亡前提）

### 判定：**部分**
- **"Properties 面板会改写正文"这一风险机制是否存在：是**（已确认，但触发条件极窄）。
- **fenced code block 内容会被自动改写：未能确认**（在所有可获取的官方材料中**找不到任何数值级证据**）。
- **综合风险评级：低**（理由见 (3)），但**不作"不会被改写"的正面断言**。

### 证据

**（1）D-04 的原文前提只有一半被证实**

`decisions/ARCHITECTURE_DECISIONS.md` D-04 写的是：

> "Worker A 引用官方文档：Obsidian 明列 **Nested properties 不支持**，且 Properties 面板会重写 frontmatter。"

前半句（nested properties 不支持）有文档支撑，**后半句"会重写 frontmatter"确有官方证据**，但证据同时**限定了重写的原因与范围**：

`https://help.obsidian.md/Plugins/Templates` 原文：

> "In **Live Preview**, the **Properties in document** panel can overwrite template variables that do not have quotation marks. To avoid this, edit templates in **Source mode**, or set **Settings → Editor → Properties in document** to **Source**."

即官方点名的"改写"是**一种具体的、可预期的**行为：Properties 面板把**不带引号**、恰好长得像日期/时间的 frontmatter 值，按属性类型规范化成带引号的字符串。已有的对抗手段官方自己给了两条（Source 模式、把 Properties in document 切成 Source），且**该行为被限定在 frontmatter 区间内**。

**（2）没有任何证据显示改写会越出 frontmatter 进入正文**

- 官方 `getFrontMatterInfo` 的契约（`obsidian.d.ts:5060` 起的 `FrontMatterInfo { exists; frontmatter; from; to; contentStart; }`）明确区分了 frontmatter 区间（`from`–`to`）与正文起点（`contentStart`），说明应用内部对"frontmatter 区"与"正文区"是有边界的。
- `Vault.process(file, fn)`（`obsidian.d.ts:10382`）是**全文件字符串级的读改写**，回调里拿到的是整份文件——插件侧不存在"保存时自动重排正文"的机制。
- 用户帮助全站检索：**没有**任何一处描述 Obsidian 自动格式化/重排正文的 fenced code block。

**（3）为什么判定"风险低"而不是"安全"**

正面证据（"字节不动"）**不存在**；判断建立在三条间接事实上：
1. 已确认的唯一改写源是 Properties 面板，其作用域是 frontmatter；
2. fenced code block 在 Obsidian 里是**原样保留块**（用户帮助明确：代码块用 3 个及以上反引号或波浪线包围，只做 Prism 高亮，且 "Source mode and Live Preview do not support PrismJS, and may render syntax highlighting **differently**"——这句话只谈**渲染**差异，未谈**存储**改动）；
3. `registerMarkdownCodeBlockProcessor(language, handler)`（`obsidian.d.ts:7275`）的存在本身要求**代码块源码 `source` 能原样交给插件**，否则一切自定义代码块（mermaid、dataview、csv→表格）都会失效——而这些是官方文档主推的用法。

### 对数据模型的影响

D-04「结构化子对象放正文 fenced YAML 块（```yaml swp:xxx```）」**成立但须挂条件**：该通路的安全性**有赖于 Obsidian 不改写正文代码块这一未被正面证实的性质**，因此 YAML 块必须**同时**在 `_maps/` 侧保留权威副本（提案 §5.4 已经这样设计），使"正文被意外改动"降级为**可检测的数据漂移**而不是数据丢失。

### 若不成立时的退路（D-04 的 B 计划）

若实测发现 YAML 块会被改写（或某版本引入正文自动格式化）：
1. **首选**：把结构化子对象从正文 YAML 块迁到 **独立 sidecar 文件**（`_data/<entity_id>.yaml`），正文只保留一行指针锚点；sidecar 为 `.yaml` 非笔记文件，不进入 Markdown 管线，Obsidian 不会解析也不会重写。
2. **次选**：把结构化子对象塞进 **`%% ... %%` Obsidian 注释**（用户帮助已确认：`%%` 块注释可跨行、可包含 Markdown、阅读视图全部隐藏）——但注释同样在正文内，若改写风险源于"正文任意位置重排"则次选无效，故降为次选。
3. **兜底**：正文只留 `par_` ID 锚点，一切结构信息走 `_maps/`，渲染时由插件拼装（即提案 R4 的极限形态）。

> **必须写给 QA 的一句话**：C4 的"否"（不改写）在官方材料中**没有正面证据**，因此本项判定为**部分**。若要把它升为"是"，唯一干净的路径是一次真实 Vault 的运行时实验（见 §6）。

---

## 6. C5 — `{{figref:...}}` 能否被 post-processor 安全处理、是否与原生语法冲突

### 判定：**部分**
- **能否被 Markdown post-processor 安全处理：是**（有确证的 API 与语义位置）。
- **是否与 Obsidian 原生语法冲突：部分冲突**——与「Templates 核心插件的模板变量」**存在真实冲突**；与 `[[...]]`/`![[...]]` 嵌入**不冲突**；与同形 `{{...}}` 无其他原生语义。

### 证据

**（1）post-processor 的能力边界**

- `obsidian.d.ts:5862-5873` `MarkdownPostProcessor`：`(el: HTMLElement, ctx: MarkdownPostProcessorContext) => Promise<any> | void`；
- `obsidian.d.ts:7257` `registerMarkdownPostProcessor(postProcessor, sortOrder?)`（`@since 0.9.7`）；
- `https://docs.obsidian.md/Plugins/Editor/Markdown+post+processing` 原文：mode 下 "you can add your own *Markdown post processor*…It lets you **add, remove, or replace** HTML elements to the rendered document"；
- `obsidian.d.ts:5912` `ctx.getSectionInfo(el)` 可回溯该元素所在的**行级位置**（`MarkdownSectionInformation { text, lineStart, lineEnd }`，`obsidian.d.ts:6086-6096`），使"渲染结果 ↔ 源文本"可对齐。

**（2）冲突面一：Templates 插件的模板变量（真实冲突）**

`https://help.obsidian.md/Plugins/Templates` 原文列出的变量：

| 变量 | 说明 |
|---|---|
| `{{title}}` | 当前笔记标题 |
| `{{date}}` | 今天日期，默认 `YYYY-MM-DD` |
| `{{time}}` | 当前时间，默认 `HH:mm` |

> "Both `{{date}}` and `{{time}}` allow you to change the default format using a **format string**. To set a format string, add a **colon (`:`)** followed by a string of Moment.js format tokens, for example `{{date:YYYY-MM-DD}}`."

**这与 `{{figref:fig_7K3M9Q2P}}` 的形状完全同构**：`{{name:arg}}`。风险有二：
1. 该替换只在**执行 `Templates: Insert template` 命令时**发生（文档："When you insert a template containing a template variable, Templates replaces it"），**不是**在渲染时一直发生——因此对**已写好的正文**不会自动生效；
2. 但若稿件正文被放进模板文件夹、或被 `Insert template` 命令扫过，`{{figref:...}}` 有被当成模板变量处理的风险（`figref`/`fig`/`res`/`pat` 并不在 `title|date|time` 集合内，按文档口径**应不被替换**，但这依赖"未列出的变量名一律不动"这一**未被文本确认**的假设）。

**（3）冲突面二：`%%...%%` 与 `[[...]]`（不冲突）**

`https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown` 的 "Supported Markdown extensions" 表穷举了 Obsidian 相对 CommonMark/GFM 的全部扩展：`[[Link]]`、`![[Link]]`、`![[Link#^id]]`、`^id`、`[^id]`、`%%Text%%`、`~~Text~~`、`==Text==`、代码围栏、任务列表、callouts、表格。

**`{{...}}` 不在其中**——这既说明它不是原生语法（无原生语义可冲突），也说明它不会被 Obsidian 抢占解析。

**（4）无其他原生 `{{}}` 语义**

`obsidian.d.ts` 全文对 `{{`/`}}`：**0 命中**（无任何含 `{{` 的示例、注释或类型）。站点索引 1,319 个开发者文档页中，`{{` 仅出现在模板变量相关处。

**（5）处理时机的一个硬约束**

post-processor **只作用于 Reading view**（`MarkdownPostProcessor` 文档："change how a Markdown document is **rendered in Reading view**"）。Live Preview 下需要额外的 CM6 装饰器（`registerEditorExtension`，`obsidian.d.ts:7299`；装饰器能力见 `https://docs.obsidian.md/Plugins/Editor/Decorations`，含 mark/widget/replace/line 四类并明确 "adding custom HTML elements"）。这一点与 D-06「渲染时解析」一致，但对 C5 是个**范围限定**：安全处理 ≠ 两种视图都自动生效。

### 对数据模型的影响

`{{figref:fig_XXXXXXXX}}` 可保留为主标记符，但**必须收紧命名空间**：把模板变量可能命中的 `{{title}}`/`{{date}}`/`{{time}}` 以及 `{{date:...}}`/`{{time:...}}` 形状显式列为**保留字**，并要求 `figref`/`fig`/`res`/`pat` 之外新增的前缀都带 `_`（如 `{{swp:figref:...}}`）以便一眼区分。

### 若不成立时的退路

1. **首选改造**：给自定义语法加私有命名空间前缀 `{{swp:figref:...}}`——与 Templates 的 `{{name:arg}}` 形状虽然仍同构，但 `swp` 不可能被模板插件识别，且可用校验规则在导入时拦截正文中裸 `{{`。
2. **次选**：改用 Obsidian 原生 wikilink 承载引用（`[[fig_7K3M9Q2P|Figure 3]]`），编号在写入时固化（提案 D-06 的降级路径），彻底避开 `{{}}` 命名空间。
3. **最后手段**：改用 `%%...%%` 注释承载机器标记（用户帮助确认注释块可跨行、阅读视图隐藏），但代价是导出时需先展开。
4. 若需要 Live Preview 下也生效：追加 `registerEditorExtension` + CM6 装饰器（两条路都要做，不能只做 post-processor）。

---

## 7. C6 — Obsidian 是否有原生批注能力（非插件）

### 判定：**否**
- **原生批注（行内或段落级、可挂审稿意见、可锚定位置）：否**。
- **插件能否在编辑器内做行内批注 UI：是**（能力存在，但属"插件自建"，非官方功能）。

### 证据

**（1）核心插件清单无批注类插件**

`https://help.obsidian.md/Plugins/Core+plugins` 的 "All core plugins" 一节**穷举**了全部核心插件（该页自述 "This page lists the core plugins that come with installed with Obsidian"）：Audio recorder、Backlinks、Bases、Bookmarks、Canvas、Command palette、Daily notes、File explorer、File recovery、Footnotes view、Graph view、Note composer、Outgoing links、Outline、Page preview、Properties view、Publish、Quick switcher、Random note、Search、Slash commands、Slides、Sync、Tags view、Templates、Unique note creator、Web viewer、Word count、Workspaces（共 29 项 + 2 个官方维护的社区插件 Importer、Maps）。

**其中没有任何一项是批注 / 评论 / 审阅意见功能。**

**（2）`obsidian.d.ts` 中无批注 API**

全文 `grep -i "annotat\|comment"` 仅在 `obsidian.d.ts:2964` 命中一条**代码注释**（"as per comment above, it's not recommended to set default hotkeys"），**不是** API。即：没有任何 `Annotation` / `Comment` / `Review` 相关的类型或方法。

**（3）最接近的两个原生机制都不满足"批注"**

| 机制 | 出处 | 为什么不等于批注 |
|---|---|---|
| `%%...%%` 注释 | `https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax`（"You can add comments by wrapping text with `%%`. Comments are only visible in Editing view."） | 纯**文本隐藏**，无损于正文——**没有**"谁在什么时间对哪一段提了什么"的结构，也没有作者/状态/回复/解决与否；只能自己约定格式 |
| `==...==` 高亮 | 同上（六种颜色，`https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax` 的 "Highlight colors"） | 只是**字符样式**，不承载任何批注意义，也无法区分"作者高亮"与"审稿意见高亮" |

**（4）插件能做到什么（行内批注 UI）**

已确证的可组合能力：

| 能力 | 证据 |
|---|---|
| 注册自定义编辑器扩展（CM6） | `obsidian.d.ts:7299` `registerEditorExtension(extension: Extension): void` |
| 装饰器 UI（mark / widget / replace / line，明确支持插入自定义 HTML 元素） | `https://docs.obsidian.md/Plugins/Editor/Decorations` |
| 判断 Live Preview 是否激活 | `obsidian.d.ts:3943` `editorLivePreviewField: StateField<boolean>`；文档页 `https://docs.obsidian.md/Reference/TypeScript+API/editorLivePreviewField` "Use this StateField to check whether Live Preview is active" |
| 注册自定义视图（侧栏批注面板） | `obsidian.d.ts:7219` `registerView` + `ItemView.contentEl`（`obsidian.d.ts:5391-5416`） |
| Reading mode 的元素级后处理 | `obsidian.d.ts:7257` + `ctx.getSectionInfo`（`obsidian.d.ts:5912`） |

即：**行内批注 UI 是插件能力，不是 Obsidian 能力**；并且 Live Preview 侧需要 CM6 装饰器、Reading view 侧需要 post-processor，**两条实现路径都要写**，且底层 `EditorView` 的获取仍需 `editorEditorField`（`obsidian.d.ts:3931`）——这与 Phase 0 审计 §4/§结论 10 的判断一致。

### 对数据模型的影响

Manuscript 报告 §14.1 结论 2「Track Changes 和批注无法在 Markdown 正文中保留，需 Sidecar 方案」**被独立证实**：`RevisionIssue` / `Patch` 必须以**独立实体 + 块锚点定位**（提案 §4.6 的 `targets[].par`）建模，**不得**寄望于正文内的原生批注；`%%...%%` 只能作为**机器标记的载体**（提案 §3.5 的 `%%@generated by figlist%%` 用法正确），**不能**作为审稿意见的存储格式。

### 若不成立时的退路

本项若"否"成立（即确无原生批注），退路就是**本提案已经在走的路**：批注 = `RevisionIssue` 实体 + `targets: [{par, manuscript, section?}]` + 插件侧 `ItemView` 批注面板（D-07 的「Bases 只作浏览层，ItemView 渲染聚合视图」）。若该模型被判太重，最轻退路是插件在 CM6 里用 **mark decoration + gutter 图标**做"只读批注预览"，批注正文仍落在 `RevisionIssue` 文件里。

---

## 8. 未能确认项与尝试方式（禁止推测填空的登记表）

| 项 | 未确认的具体点 | 已尝试的方式 | 结论 |
|---|---|---|---|
| C1 | 块 ID 是否**大小写敏感** | (a) 抓取 15 个用户帮助页 + 13 个开发者页 `grep` 大小写相关表述；(b) `obsidian.d.ts` 全文件检索；(c) `api.github.com/search/issues` 查 `obsidian-help` 全库，关键词 `"block ID"` / `block id characters` → `total_count: 0`；(d) 运行时探针（见下）失败 | **未能确认**，需实测 |
| C2 | 块 ID 能否挂在**标题行**上 | (a) 15 个用户帮助页 `grep -n "^#\{1,6\} .*\^"` → **0 命中**；(b) 查 `obsidian-help` issues（`heading` + `block`）：仅命中 #599「How to link to heading or block in unknown note is undocumented」、#301「Heading and block embeds are undocumented」，**两页均为文档缺口报告，不含语法裁决**；(c) 运行时探针失败 | **未能确认**；但 `SectionCache.id`（`obsidian.d.ts:8181-8186`）与官方"不支持清单"未含标题，支持判定为"很可能可行" |
| C3 | 长度 / 数量限制 | `obsidian.d.ts` 全文 `grep -i "maximum\|limit"`（对块/ID 相关行 0 命中）；两站文档检索无相关表述 | **未发现任何限制的表述**——登记为「无限制的说法缺乏官方背书」，而非「官方承诺无限」 |
| C4 | 正文 fenced code block **是否字节级不变** | 两站全部抓取文档检索"自动格式化/重写正文"，**0 命中**；`obsidian.d.ts` 无相关 API；`getFrontMatterInfo` 的区间划分与 `Vault.process` 的全文件字符串语义作为结构性反证 | **未能确认**（正面证据不存在）；已按"风险低"处理并给出 D-04 的 B 计划 |
| C1/C2/C3/C4 | **运行时实测** | 见下 | **失败**，原因已定位 |

### 运行时探针的尝试与失败原因（供后续复验者直接复用）

**尝试**：在本机建独立 Vault `C:\Users\01\AppData\Local\Temp\swp_vault`，内含一个探针插件（`manifest.json` + `main.js`，`onload` 时遍历 `vault.getMarkdownFiles()`，把 `getFileCache()` 的 `blocks` / `sections` / `headings` / `links` dump 成 `PROBE_RESULT.json`），测试笔记同时放入：标题锚点 `## Intro ^sec_4M2P8QKT`、段落锚点 `^par_9QK2M4XZ`、可疑 ID（`^par.dot`、`^par_upper`、`^Par_MiXeD`、`^PARUPPER`）、` ```yaml swp:citation``` ` 块、`{{figref:...}}` / `{{res:...|fmt=31.0}}` token、`[[#^sec_...]]` 自链接。

**失败**（两次）：
1. `obsidian://open?path=...` → 被**已在运行的 Obsidian 实例**接管，命令落到用户当前 Vault，探针 Vault 未被注册进 `obsidian.json`；
2. `obsidian.exe --user-data-dir=<临时profile> <vault路径>` → 进程确实起来（`wmic` 可见 `--user-data-dir=...\swp_profile`），但：
   - `obsidian.json` 始终未被写入（Vault 从未完成注册）；
   - 自动更新到 1.15.0 后处于 **"restart to update"** 状态，未进入正常加载；
   - 日志出现 `CLI server error: EADDRINUSE ... \\.\pipe\obsidian-cli-01`（与运行中的实例抢 CLI 管道）；
   - 等待累计约 2.5 分钟后仍无 `PROBE_RESULT.json`，`.obsidian/` 也未被应用初始化写入。

**处理**：已用 `taskkill /PID 34420 /T /F` 精确终止**本次启动的那一棵进程树**，用户原有的 5 个 Obsidian 进程未受影响（任务前后 `tasklist | grep -ci obsidian` 均为 5）；临时文件留在 `%TEMP%\swp_vault`、`%TEMP%\swp_profile`，未触碰用户任何 Vault。

**对后续复验者的建议**：在一台**未运行** Obsidian 的会话里，或由人工在 Obsidian GUI 内手动「Open folder as vault」打开 `%TEMP%\swp_vault` 后勾选启用 `swp-probe`，再读 `PROBE_RESULT.json`。该探针可一次性回答 C1 的大小写、C2 的标题锚点、C3 的覆盖范围三个问题。

---

## 9. 对下游交付物的结论修正建议（不改其它文件，仅提请）

| 下游文件 | 位置 | 建议 |
|---|---|---|
| `research/data-model/SCIENTIFIC_DATA_MODEL_PROPOSAL.md` | §5.6 锚点编解码器 | `_` 可保留，映射分支降级为**保险丝**而非主线；补一条「大小写强制唯一化」 |
| 同上 | §3.3 `## Introduction ^sec_4M2P8QKT` | 标注「标题锚点形式未经实测，权威方向预留反转（见 C2）」 |
| 同上 | §3.5 标记表 | 给 `{{figref:...}}` 等补「保留字 + 命名空间前缀 `{{swp:...}}`」约束；`%%...%%` 只用于机器标记，不用于审稿意见 |
| 同上 | §3.4 / D-04 | YAML 块通路成立但**挂条件**：`_maps/` 必须保有权威副本（已有），并补 sidecar 退路 |
| `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` | §12 第 1/2/4 项 | 第 1 项（下划线）已可由 C1 关闭；第 2 项见 C5；第 4 项（批注）已可由 C6 关闭 |

---

## 10. 证据文件指纹（复验用）

| 文件 | 大小（字节） |
|---|---|
| `obsidian.d.ts`（npm 1.14.4） | 11,539 行 / 344,637 解包总量；SHA-1 `232da70b867460d0158742bdbcd861c9975fb992` |
| `Internal links.md`（帮助站） | 8,992 |
| `Basic formatting syntax.md`（帮助站） | 16,149 |
| `Obsidian Flavored Markdown.md`（帮助站） | 2,564 |
| `Plugins/Templates.md`（帮助站） | 3,917 |
| `Core plugins.md`（帮助站） | 3,261 |
| `Embed files.md`（帮助站） | 3,125 |
| `Markdown post processing.md`（开发站） | 2,368 |
| `Decorations.md`（开发站） | 8,331 |

> 抓取方法：`curl -s https://publish-01.obsidian.md/access/<uid>/<urlencoded-path>.md`（帮助站 uid `f786db9fac45774fa4f0d8112e232d67`，开发站 uid `caa27d6312fe5c26ebc657cc609543be`）。**注意**：用 Python `urllib` 默认 UA 请求会返回 **403**，须用 `curl`。
