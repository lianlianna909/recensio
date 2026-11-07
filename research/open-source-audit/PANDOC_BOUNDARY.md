# Pandoc 调用边界合规说明（PANDOC_BOUNDARY.md）

**创建日期**: 2026-11-07
**背景**: Phase 1 门禁条目 G3-3。本项目计划以**独立进程**调用 Pandoc 做文档导出（Markdown → DOCX 等）。
**本文性质**: 仅陈述事实、官方来源与条件，**不给出法律结论**（如「应该没问题」）；所有涉及解释空间的判定均标注「需法务确认」。

---

## 0. Pandoc 的许可证（事实）

- **许可证**: GPL-2.0-or-later（"GPL, version 2 or greater"）
- **来源（一手）**: Pandoc 官方手册 Authors 节，声明 "Released under the GPL, version 2 or greater" — https://pandoc.org/MANUAL.html （访问日期 2026-11-07）
- **许可文本**: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html （GPL-2.0 原文）；"or later" 意味着使用者可按 GPL-3.0 选择适用版本，GPL-3.0 原文见 https://www.gnu.org/licenses/gpl-3.0.en.html
- **同仓库 COPYING.md 链接**: https://github.com/jgm/pandoc/blob/master/COPYING.md （2026-11-07 经 pandoc.org/MANUAL.html 与仓库 COPYING.md 页面交叉确认；当日 GitHub API 匿名请求已达速率上限，未重新抓取原文）

> **注意**: 本项目原审计报告中将 Pandoc 标为 "GPL-2.0"，未体现 "or later"。**应更正为 GPL-2.0-or-later。**

---

## 1. 进程级调用 vs 链接/嵌入：法律差异与 FSF 立场

### 1.1 链接/嵌入（高风险路径）

**事实**：
- 将 GPL 代码以静态链接、动态链接、或作为库（Haskell library API，如 pandoc-types）嵌入自己的程序，FSF 的立场是：这使两者构成一个「组合程序」（combined program / derivative work），整个程序必须以 GPL 分发。
- FSF GPL FAQ 原文（访问日期 2026-11-07）：
  - "I'd like to incorporate GPL-covered software in my proprietary system. Can I do this?" → **"You cannot incorporate GPL-covered software in a proprietary system."** — https://www.gnu.org/licenses/gpl-faq.en.html#GPLInProprietarySystem
  - 库以 GPL 发布时，「使用该库的程序」是否必须为 GPL：https://www.gnu.org/licenses/gpl-faq.en.html#IfLibraryIsGPL

### 1.2 独立进程调用（争议较小路径）

**事实**：
- FSF GPL FAQ 对「聚合」（aggregate）与「组合程序」的区分：**"What is the difference between an 'aggregate' and other kinds of 'modified versions'?"** — https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation
  - 要点：两个独立程序通过 exec/pipes/sockets 等「恰当的通信方式」（suitable for communication at arm's length）交换数据，通常被视为两个独立程序；通信细节越「亲密」（共享复杂数据结构、内部状态），越可能被判定为组合程序。
- FSF GPL FAQ 对 fork/exec 插件：**"When is a program and its plug-ins considered a single combined program?"** — https://www.gnu.org/licenses/gpl-faq.en.html#GPLPlugins
  - 要点：主程序若以 fork and exec 调用插件，且通信是「arm's length」（如命令行参数、标准输入输出、临时文件），通常视为独立程序；若共享复杂数据结构或紧密耦合，则可能视为组合程序。
- FSF GPL FAQ 对非自由程序加载 GPL 插件：https://www.gnu.org/licenses/gpl-faq.en.html#NFUseGPLPlugins

**本项目的对应关系（事实映射，非结论）**：
- 本项目计划以 fork/exec 方式调用 pandoc 独立二进制，通过命令行参数与文件/stdin/stdout 交换数据——这正落在 FSF 所述「arm's length」通信的典型情形，按 FSF 立场通常被视为两个独立程序。
- 「通常被视为」≠ 法律定论。最终判定取决于整体架构的耦合程度（例如是否依赖 pandoc 内部结构、是否修改 pandoc、是否通过定制 Lua filter 让 pandoc 与宿主共享专有逻辑），此边界**需法务确认**。

### 1.3 Pandoc 官方对两种用法的区分（事实）

- Pandoc 官方手册区分两种用法：**"If you are using pandoc as a Haskell library (rather than shelling out to the executable)"** — 即官方自身也区分「以库方式使用」与「以可执行程序方式调用」，并以可执行程序方式为默认推荐（含 +RTS 内存限制等面向独立进程调用的说明）。来源：https://pandoc.org/MANUAL.html （访问日期 2026-11-07）

---

## 2. 三种分发情形的义务

### 情形 1：用户自装 Pandoc（本项目不随产品分发 Pandoc 二进制）

- **架构**: 本项目文档导出功能检测系统 PATH 中的 pandoc；未安装时提示用户自行安装（如 `apt install pandoc`、官方安装包）。
- **义务**:
  - 本项目不分发 Pandoc，故**不触发** GPL 对「拷贝/分发」的义务条款；GPL 的核心义务（提供源码、保留声明）由 Pandoc 的分发者（如发行版打包方、pandoc 官方）履行。
  - 本项目仍需在自己的文档中注明「导出功能依赖 Pandoc（GPL-2.0-or-later）」，避免误导（good practice；是否为强制义务需法务确认）。
  - GPL 的「组合程序」风险在进程边界清晰的前提下最小，但**不等于零**，见 §1.2。
- **对闭源分发的兼容性**: 三种情形中约束最少的一种。

### 情形 2：随产品分发 Pandoc 二进制

- **架构**: 本项目安装包内捆绑 pandoc 独立二进制（Windows/Linux/macOS 桌面分发）。
- **义务（事实，源自 GPL-2.0 条文 https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html ）**:
  - **分发即触发 GPL**: 第 1–3 条要求向每个接收者提供 GPL 许可证副本、源代码（或书面获取源码的承诺），且不得对接收者施加超出 GPL 的限制。
  - **保留声明**: 不得移除 pandoc 二进制中的版权与许可声明。
  - **无附加限制**: 不能用最终用户协议禁止接收者行使 GPL 授予的权利。
  - **「聚合」问题**: 与独立第三方程序捆绑分发（即使同一介质），FSF 立场是只要两者是独立程序且通信方式得当，各自许可证独立适用（GPL FAQ #MereAggregation）。但安装包的耦合方式（如是否让宿主程序唯一地依赖捆绑的 pandoc、是否共享私有接口）会影响此判定，**需法务确认**。
  - **版本选择**: GPL-2.0-or-later 允许本项目在 GPL-2.0 或 GPL-3.0 下转发 pandoc；转发时遵循所择版本条款即可。
- **对闭源分发的兼容性**: 可以与闭源宿主并存（FSF 的 aggregate 立场下），但安装包合规细节需逐项审查。**需法务确认**。

### 情形 3：SaaS 调用（服务端运行 pandoc，用户通过 Web 访问）

- **架构**: pandoc 仅运行在本项目服务器上，用户上传 Markdown、下载 DOCX，用户从未收到 pandoc 二进制。
- **义务（事实）**:
  - **GPL（不含 AGPL）的源码义务由「分发」触发**。FSF 立场：在服务器上运行程序、让用户通过网络交互，**不构成 GPL 意义上的分发**，故不触发 GPL 的源码提供义务。FSF 对此的表达见其 SaaS 相关论述 "Who's Afraid of SaaS?"（作为 S：https://www.gnu.org/philosophy/who-does-that-server-really-serve.en.html 讨论网络服务不触发 GPL 分发义务的立场）。
  - **但注意**: 2026-11-07 抽查发现 FSF GPL FAQ 中曾列的 "MoneyGig"/"ServiceProviders" 条目在当前版本未命中（锚点不存在），相关论述可能已迁移或重组；引用前应以 FAQ 当前内容为准。
  - **风险边界**: 若未来将 pandoc 输出/交互包装成向外部用户「分发」的行为（如允许用户下载含 pandoc 派生内容的可执行产物），性质可能变化；自定义 Lua filter 等与宿主逻辑深度耦合的做法也会增加「组合程序」判定风险。**需法务确认**。
  - 若采用用户自装/自托管 pandoc 的混合架构，则回到情形 1 的义务结构。
- **对闭源分发的兼容性**: GPL 在纯 SaaS 场景下义务最少（这正是 AGPL-3.0 立法要堵的缺口；AGPL 对本项目无关——pandoc 是 GPL-2.0-or-later，不是 AGPL）。

---

## 3. 本项目建议的做法（非法律结论）

**建议路径（事实依据最充分的组合）**：

1. **以独立进程调用**: fork/exec 独立 pandoc 二进制，仅通过命令行参数、文件、stdin/stdout 交换数据；不使用 pandoc 的 Haskell 库 API，不嵌入其代码。依据：FSF FAQ #MereAggregation / #GPLPlugins 的 arm's length 判定标准（§1.2）。
2. **优先选择「用户自装」**: 若产品形态允许，让用户自行安装 pandoc（情形 1），本项目不捆绑、不分发，义务面最小。
3. **若必须捆绑**: 按 §2 情形 2 的义务清单逐项履行（提供源码链接、保留声明、不附加限制），并审查安装包耦合方式。
4. **SaaS 形态**: 若以 SaaS 交付，pandoc 仅服务端运行即可，不触发 GPL 分发义务（§2 情形 3），但仍需注意导出功能不构成「分发」的架构边界。

**必须留给法务确认的边界（不可由本报告代替判定）**：
- 独立进程 + arm's length 通信在具体架构下是否一定不构成衍生作品（§1.2 的「通常视为」存在解释空间）；
- 自定义 Lua filter / 模板的归属与耦合程度对组合程序判定的影响；
- 情形 2 安装包的聚合判定；
- 情形 3 中任何可能被视为「分发」的交互形态。

**不得由本文做出的判定**: 本文不给「合规」「没问题」的结论；上述任一情形的最终判定均需具备资格的法律意见。

---

## 4. 来源清单

| # | 来源 | URL | 类型 | 访问日期 |
|---|------|-----|------|---------|
| 1 | Pandoc 官方手册（许可证声明、库/可执行区分） | https://pandoc.org/MANUAL.html | 一手 | 2026-11-07 |
| 2 | GPL-2.0 许可文本 | https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html | 一手 | 2026-11-07 |
| 3 | GPL-3.0 许可文本 | https://www.gnu.org/licenses/gpl-3.0.en.html | 一手 | 2026-11-07 |
| 4 | FSF GPL FAQ: 聚合 vs 修改版本 | https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation | 一手 | 2026-11-07 |
| 5 | FSF GPL FAQ: GPL 软件嵌入专有系统 | https://www.gnu.org/licenses/gpl-faq.en.html#GPLInProprietarySystem | 一手 | 2026-11-07 |
| 6 | FSF GPL FAQ: 插件与组合程序判定 | https://www.gnu.org/licenses/gpl-faq.en.html#GPLPlugins | 一手 | 2026-11-07 |
| 7 | FSF GPL FAQ: GPL 库使用 | https://www.gnu.org/licenses/gpl-faq.en.html#IfLibraryIsGPL | 一手 | 2026-11-07 |
| 8 | FSF GPL FAQ: 非自由程序加载 GPL 插件 | https://www.gnu.org/licenses/gpl-faq.en.html#NFUseGPLPlugins | 一手 | 2026-11-07 |
| 9 | Pandoc 仓库 COPYING.md | https://github.com/jgm/pandoc/blob/master/COPYING.md | 一手 | 2026-11-07 |
| 10 | FSF: 网络服务与 GPL（背景立场） | https://www.gnu.org/philosophy/who-does-that-server-really-serve.en.html | 一手 | 2026-11-07 |

> 以上 URL 均于 2026-11-07 经 HTTP 状态码核验可达（200）。未编造任何 URL 或条款内容。
