# obsidian.d.ts 关键类型定义摘录

## 来源与指纹

| 来源 | 说明 | 指纹 |
|---|---|---|
| `obsidianmd/obsidian-api` `master` 分支 `obsidian.d.ts` | GitHub Contents API 拉取（`?ref=master`），git blob sha `10b31c4787fbc3ee4b228ca403165bbf865eb165` | 文件 11,539 行；SHA-256 `97c86417c893db691e401fdffd9026e348dc96da6bfcfa5d49a301d7fe7542a0`；SHA-1 `6748f9476590f14d76d20792ac233e827e337cbf` |
| npm `obsidian@1.14.4` (`https://registry.npmjs.org/obsidian/-/obsidian-1.14.4.tgz`) | tarball `fileCount: 7`，`unpackedSize: 344637` | tarball SHA-1 `e4d4c91df3184c6d8cd0ecccc0a6565c0ada99bb`；内含 `obsidian.d.ts` SHA-1 `232da70b867460d0158742bdbcd861c9975fb992` |
| npm `obsidian@1.14.4` `canvas.d.ts` | 与 master 版本逐字节一致 | SHA-1 `5141e786d6b9191916e43627577eafa03f5f0bea` |

**master 与 npm 1.14.4 的差异**：`diff` 结果仅 5 处，全部是 JSDoc 注释里 "sidebar" → "sidedock" 的措辞改动（第 10899/10907/10914/10964/10986 行）。**类型签名完全一致**。

---

## 1. 版本与 API 版本

`obsidian.d.ts:1312-1319`

```ts
/**
 * This is the API version of the app, which follows the release cycle of the desktop app.
 * Example: '0.13.21'
 * @public
 */
export let apiVersion: string;
```

`obsidian.d.ts:7376-7425`（`PluginManifest`）

```ts
export interface PluginManifest {
    dir?: string;
    id: string;
    name: string;
    author: string;
    version: string;
    /** The minimum required Obsidian version to run this plugin. */
    minAppVersion: string;
    description: string;
    authorUrl?: string;
    /** Whether the plugin can be used only on desktop. */
    isDesktopOnly?: boolean;
}
```

`obsidian.d.ts:1-8`（imports，证明 Obsidian 内置 CodeMirror 6 与 moment 的版本约束）

```ts
import { Extension, StateField } from '@codemirror/state';
import { EditorView, ViewPlugin } from '@codemirror/view';
import * as Moment from 'moment';
```

`npm obsidian@1.14.4 package.json` 的 peerDependencies：

```json
"dependencies": { "@types/codemirror": "5.60.8", "moment": "2.31.0" },
"peerDependencies": { "@codemirror/state": "6.7.6", "@codemirror/view": "6.43.13" }
```

> 这组 peerDependency 是**裸 semver**，不是 `^` 范围——`npm i obsidian` 要求宿主项目自带与之兼容（通常是同版本）的 `@codemirror/state` / `@codemirror/view`，否则 `npm install` 会报 peer 冲突（ERESOLVE）。这一点决定了插件项目必须固定 CM6 版本。

---

## 2. Vault / 文件读写

`obsidian.d.ts:10188`（`Vault.adapter`）

```ts
    adapter: DataAdapter;
```

`obsidian.d.ts:10290 / 10297 / 10382`

```ts
    cachedRead(file: TFile): Promise<string>;
    readBinary(file: TFile): Promise<ArrayBuffer>;
    process(file: TFile, fn: (data: string) => string, options?: DataWriteOptions): Promise<string>;
```

`obsidian.d.ts:3181` 起 `DataAdapter` 的方法清单（仅接口，无实现）：

```ts
export interface DataAdapter {
    getName(): string;
    exists(normalizedPath: string, sensitive?: boolean): Promise<boolean>;
    stat(normalizedPath: string): Promise<Stat | null>;
    list(normalizedPath: string): Promise<ListedFiles>;
    read(normalizedPath: string): Promise<string>;
    readBinary(normalizedPath: string): Promise<ArrayBuffer>;
    write(normalizedPath: string, data: string, options?: DataWriteOptions): Promise<void>;
    writeBinary(normalizedPath: string, data: ArrayBuffer, options?: DataWriteOptions): Promise<void>;
    append(normalizedPath: string, data: string, options?: DataWriteOptions): Promise<void>;
    appendBinary(normalizedPath: string, data: ArrayBuffer, options?: DataWriteOptions): Promise<void>;
    process(normalizedPath: string, fn: (data: string) => string, options?: DataWriteOptions): Promise<string>;
    getResourcePath(normalizedPath: string): string;
    mkdir(normalizedPath: string): Promise<void>;
    trashSystem(normalizedPath: string): Promise<boolean>;
    trashLocal(normalizedPath: string): Promise<void>;
    rmdir(normalizedPath: string, recursive: boolean): Promise<void>;
}
```

`obsidian.d.ts:4492-4510`（桌面适配器，**仅类型存在**）

```ts
export class FileSystemAdapter implements DataAdapter {
    getName(): string;
    /** Get the absolute path to the vault. */
    getBasePath(): string;
    ...
}
```

> `getBasePath()` 的文档原文只写了 "Get the absolute path to the vault."，**没有**任何关于移动端行为的说明；在移动端 `adapter` 不是 `FileSystemAdapter`（见 `CapacitorAdapter`：`obsidian.d.ts` 中有该类的类型条目，官方文档站也有同名 API 页）。因此任何依赖 `getBasePath()` 的代码必须用 `instanceof FileSystemAdapter` 守卫。

---

## 3. MetadataCache

`obsidian.d.ts:6440-6535`

```ts
/**
 * Provides access to the cached metadata of the files in the vault.
 * Linktext is any internal link that is composed of a path and a subpath, such as 'My note#Heading'
 * Linkpath (or path) is the path part of a linktext
 * Subpath is the heading/block ID part of a linktext.
 * @public
 */
export class MetadataCache extends Events {

    getFirstLinkpathDest(linkpath: string, sourcePath: string): TFile | null;
    getFileCache(file: TFile): CachedMetadata | null;
    getCache(path: string): CachedMetadata | null;
    fileToLinktext(file: TFile, sourcePath: string, omitMdExtension?: boolean): string;

    resolvedLinks: Record<string, Record<string, number>>;
    unresolvedLinks: Record<string, Record<string, number>>;

    /** Called when a file has been indexed, and its (updated) cache is now available.
     *  Note: This is not called when a file is renamed for performance reasons.
     *  You must hook the {@link Vault.on | Vault.on(name: 'rename')} event for those. */
    on(name: 'changed', callback: (file: TFile, data: string, cache: CachedMetadata) => any, ctx?: any): EventRef;
    on(name: 'deleted', callback: (file: TFile, prevCache: CachedMetadata | null) => any, ctx?: any): EventRef;
    /** Called when a file has been resolved for resolvedLinks and unresolvedLinks.
     *  This happens sometimes after a file has been indexed. */
    on(name: 'resolve', callback: (file: TFile) => any, ctx?: any): EventRef;
    /** Called when all files have been resolved. This will be fired each time files get modified after the initial load. */
    on(name: 'resolved', callback: () => any, ctx?: any): EventRef;
}
```

### CachedMetadata 的完整字段（`obsidian.d.ts:2391-2550`）

| 字段 | 类型 | `@since` |
|---|---|---|
| `links` | `LinkCache[]` | — |
| `embeds` | `EmbedCache[]` | — |
| `tags` | `TagCache[]` | — |
| `headings` | `HeadingCache[]` | — |
| `footnotes` | `FootnoteCache[]` | 1.6.6 |
| `footnoteRefs` | `FootnoteRefCache[]` | 1.8.7 |
| `referenceLinks` | `ReferenceLinkCache[]` | 1.8.7 |
| `sections` | `SectionCache[]` | — |
| `listItems` | `ListItemCache[]` | — |
| `frontmatter` | `FrontMatterCache` | — |
| `frontmatterPosition` | `Pos` | — |
| `frontmatterLinks` | `FrontmatterLinkCache[]` | — |
| `blocks` | `Record<string, BlockCache>` | — |

### FrontMatterCache（`obsidian.d.ts:4832-4843`）

```ts
export interface FrontMatterCache {
    /**
     * The frontmatter properties.
     * @example
     * console.log(frontmatterCache['key1']); // value1
     * console.log(frontmatterCache['key2']); // 42
     * @public
     */
    [key: string]: any;
}
```

> 关键点：**`FrontMatterCache` 只有字符串索引签名，值类型是 `any`。** 没有任何类型层面的 YAML→TS 类型映射。null、日期、wikilink、嵌套对象在类型上都不可区分。

### FrontmatterValue（`obsidian.d.ts` 中 1.14 新增）

```ts
export type FrontmatterValue = string | number | boolean | undefined | null | {
    /** @public */
    [key: string]: FrontmatterValue;
} | Array<FrontmatterValue>;
```

> 该类型在 `obsidian.d.ts` 中仅被 Bases 的 `groupOrder?: FrontmatterValue[]` 使用（`BasesConfigFileView`，`@since 1.14.3`），**没有**任何 API 方法把它用于 `processFrontMatter` 或 `getFileCache`。它的存在说明官方承认 frontmatter 允许嵌套对象（与 `FrontMatterCache` 的 `any` 对应）。

### FrontmatterLinkCache（`obsidian.d.ts:4887-4900`）

```ts
/**
 * A link in the frontmatter.
 * ```markdown
 * ---
 * key1: "[[wikilink]]"
 * key2: "[[wikilink|alias]]"
 * ---
 * ```
 * @public
 */
export interface FrontmatterLinkCache extends Reference {
    key: string;
}
```

> 注意示例里 wikilink **带双引号**。且仅在值为合法链接（可达）时才被缓存为 `frontmatterLinks` 条目。

### FileManager.processFrontMatter（`obsidian.d.ts:4432-4450`）

```ts
    /**
     * await fileManager.processFrontMatter(file, (frontmatter) => {
     * ...
     * @public
     * @since 0.13.24
     */
    processFrontMatter(file: TFile, fn: (frontmatter: any) => void, options?: DataWriteOptions): Promise<void>;
```

### getFrontMatterInfo（`obsidian.d.ts:5060`）

```ts
export function getFrontMatterInfo(content: string): FrontMatterInfo;

export interface FrontMatterInfo {
    exists: boolean;
    frontmatter: string;
    from: number;
    to: number;
    contentStart: number;
}
```

---

## 4. Views / ItemView / Commands

`obsidian.d.ts:10460` 起 `View`

```ts
export abstract class View extends Component {
    containerEl: HTMLElement;
    scope: Scope | null;            // @since 1.5.7 起公开
    protected onOpen(): Promise<void>;
    protected onClose(): Promise<void>;
    abstract getViewType(): string;
    abstract getDisplayText(): string;
    onPaneMenu(menu: Menu, source: 'more-options' | 'tab-header' | string): void;  // @since 0.15.3
}
```

`obsidian.d.ts:5391-5416` `ItemView`

```ts
export abstract class ItemView extends View {
    /** The content element. */
    contentEl: HTMLElement;

    constructor(leaf: WorkspaceLeaf);
    addAction(icon: IconName, title: string, callback: (evt: MouseEvent) => any): HTMLElement;
}
```

`obsidian.d.ts:7219 / 7257 / 7299`

```ts
registerView(type: string, viewCreator: ViewCreator): void;
registerMarkdownPostProcessor(postProcessor: MarkdownPostProcessor, sortOrder?: number): MarkdownPostProcessor;
registerEditorExtension(extension: Extension): void;
```

> `Extension` 来自 `@codemirror/state`（见文件第 6 行 import）。

`obsidian.d.ts:7283`（Bases）

```ts
    /**
     * Register a Base view handler that can be used to render data from property queries.
     * @returns false if bases are not enabled in this vault.
     * @public
     * @since 1.10.0
     */
    registerBasesView(viewId: string, registration: BasesViewRegistration): boolean;
```

`obsidian.d.ts:3930-3940`（编辑器互操作的两把钥匙）

```ts
export const editorEditorField: StateField<EditorView>;
export const editorInfoField: StateField<MarkdownFileInfo>;
export const editorLivePreviewField: StateField<boolean>;
```

> 在 `obsidian.d.ts` 中**不存在** `Editor.cm`。`grep -n "cm:" obsidian.d.ts` 无结果。而 `Editor` 是 `export abstract class Editor`（`obsidian.d.ts:3652`），只有 `getValue/setValue/getLine/posToOffset/transaction/processLines` 等抽象方法。访问 `view.editor.cm` 属于**类型里没有、运行时才有的私有字段**。

---

## 5. Bases API 全貌（`obsidian.d.ts:1459-2290`）

可区分的事实：

```ts
// 1.10.0
export interface BasesConfigFile {
    filters?: BasesConfigFileFilter;
    properties?: Record<string, Record<string, any>>;   // 注释：当前合法键只有 displayName
    formulas?: Record<string, string>;
    summaries?: Record<string, string>;
    views?: BasesConfigFileView[];
}

export type BasesConfigFileFilter =
    | string
    | { and: BasesConfigFileFilter[] }
    | { or: BasesConfigFileFilter[] }
    | { not: BasesConfigFileFilter[] };

export interface BasesConfigFileView {
    type: string;
    name: string;
    filters?: BasesConfigFileFilter;
    groupBy?: { };                       // 1.10.0，空对象类型，字段未公开
    groupOrder?: FrontmatterValue[];     // 1.14.3
    order?: string[];                    // 可见属性列表
    summaries?: Record<string, string>;
}

// 1.10.0
export class BasesEntry implements FormulaContext {
    file: TFile;
    getValue(propertyId: BasesPropertyId): Value | null;
}

export class BasesEntryGroup {
    key?: Value;
    entries: BasesEntry[];
    hasKey(): boolean;
}

export class BasesQueryResult {
    data: BasesEntry[];                          // 已按用户配置排序+限量
    get groupedData(): BasesEntryGroup[];        // 按 groupBy 分组
    get properties(): BasesPropertyId[];
    getSummaryValue(queryController, entries, prop, summaryKey): Value;
}

export type BasesPropertyId = `${BasesPropertyType}.${string}`;
export type BasesPropertyType = 'note' | 'formula' | 'file';

export abstract class BasesView extends Component {
    abstract type: string;
    app: App;
    config: BasesViewConfig;
    allProperties: BasesPropertyId[];
    data: BasesQueryResult;
    protected constructor(controller: QueryController);
    abstract onDataUpdated(): void;
    createFileForView(baseFileName?: string, frontmatterProcessor?: (frontmatter: any, file: TFile) => void): Promise<void>;  // 1.10.2
}

export class BasesViewConfig {
    name: string;
    get(key: string): unknown;
    getAsPropertyId(key: string): BasesPropertyId | null;
    getEvaluatedFormula(view: BasesView, key: string): Value;   // 1.10.2
    set(key: string, value: any | null): void;
    getOrder(): BasesPropertyId[];
    getSort(): BasesSortConfig[];
    getDisplayName(propertyId: BasesPropertyId): string;
}

export type BasesViewFactory = (controller: QueryController, containerEl: HTMLElement) => BasesView;

export interface BasesViewRegistration {
    name: string;
    icon: IconName;
    factory: BasesViewFactory;
    options?: (config: BasesViewConfig) => BasesAllOptions[];
}

// 关键：QueryController 是空壳
export class QueryController extends Component { }
```

Value 体系（`obsidian.d.ts:10092` 起）

```ts
export abstract class Value {
    static type: string;
    static equals(a: Value | null, b: Value | null): boolean;
    static looseEquals(a: Value | null, b: Value | null): boolean;
    abstract toString(): string;
    abstract isTruthy(): boolean;
    equals(other: this): boolean;
    looseEquals(other: Value): boolean;
    renderTo(el: HTMLElement, ctx: RenderContext): void;   // @since 1.10.0
}
```

具体 `Value` 子类（证明 Bases 内置了一套独立类型系统）：
`BooleanValue`、`NumberValue`、`StringValue`、`DateValue`、`DurationValue`、`FileValue`、`LinkValue`、`ListValue`、`ObjectValue`、`NullValue`、`RegExpValue`、`RelativeDateValue`、`TagValue`、`UrlValue`、`HTMLValue`、`IconValue`、`ImageValue`、`PrimitiveValue<T>`、`NotNullValue`。

---

## 6. Platform（`obsidian.d.ts:7041` 起）

```ts
export const Platform: {
    isDesktop: boolean;
    isMobile: boolean;
    isDesktopApp: boolean;
    isMobileApp: boolean;
    isIosApp: boolean;
    isAndroidApp: boolean;
    isPhone: boolean;
    isMacOS: boolean;
    ...
};   // 其余字段见原文件：isWin / isLinux / isSafari / resourcePathPrefix 等
```

---

## 7. 在 `obsidian.d.ts` 中**不存在**的符号（grep 全文件 0 命中）

以下是我在设计中会用到、但官方类型定义里**没有**的：

| 符号 | grep 结果 | 影响 |
|---|---|---|
| 任何 `child_process` / `require(...)` / `electron` 的导出 | 0 命中 | 外部进程调用不在公开 API 内 |
| `MetadataCache.getBacklinks()` 之类的反向索引 API | 0 命中 | 反向链接只能通过 `resolvedLinks` 自己反查 |
| `Bases` 查询的公开执行入口（如 `app.bases.executeQuery()`） | 0 命中 | 查询只能通过 `.base` 文件或 `BasesView` 间接触发 |
| `ItemView` 的编辑器嵌入 API | 0 命中 | 自定义 View 内没有官方「嵌入 Markdown 编辑器」的方法 |
| `Editor.cm` | 0 命中 | 见 §4 |
