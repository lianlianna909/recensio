# Third-Party Dependencies

> 本文件是第三方依赖的**唯一登记处**。未在此登记的依赖不得引入。
> 规则见 `decisions/ADR-LIC-001-003.md` ADR-LIC-003。

---

## 1. 当前状态

**已登记的第三方依赖：1 个**（均为开发期工具，不随发行包分发）。

本仓库的产品代码尚未开始（Phase 1 未启动），当前无运行时依赖；
无任何包管理器清单（无 `package.json` / `pyproject.toml` / `requirements.txt` / `Cargo.toml` / `go.mod`）。

---

## 2. 登记表

每个新依赖必须填写**全部**字段，缺一不得合并。

| 名称 | 精确版本 | 来源仓库 | 许可证 SPDX | 用途 | 分类 | 随发行包分发 | 含 NOTICE | 审查结论 |
|---|---|---|---|---|---|---|---|---|
| `reuse` | `6.3.0` | https://codeberg.org/fsfe/reuse-tool | `Apache-2.0 AND CC0-1.0 AND CC-BY-SA-4.0 AND GPL-3.0-or-later` | SPDX header 与许可证合规检查（`reuse lint`） | Development | 否 | 否 | **需人工批准 → 已批准**（含 GPL-3.0-or-later，见 §5 例外 `EX-001`） |

### 2.1 `reuse` 的传递依赖（均为 Development，均不随发行包分发）

安装于仓库内 `.venv`（已在 `.gitignore` 中）。全部仅在开发期与 CI 以独立进程调用，不链接进产品。

| 名称 | 精确版本 | 许可证 SPDX | 用途 |
|---|---|---|---|
| `attrs` | `26.1.0` | MIT | reuse 的传递依赖 |
| `boolean.py` | `5.0` | BSD-2-Clause | reuse 的传递依赖 |
| `charset-normalizer` | `3.5.2` | MIT | reuse 的编码检测（Windows 无 `file` 命令时的必需 extra） |
| `click` | `8.5.1` | BSD-3-Clause | reuse 的 CLI 框架 |
| `Jinja2` | `3.1.6` | BSD-3-Clause | reuse 的模板渲染 |
| `license-expression` | `30.4.4` | Apache-2.0 | reuse 的许可证表达式解析 |
| `MarkupSafe` | `3.0.4` | BSD-3-Clause | Jinja2 的传递依赖 |
| `python-debian` | `1.1.1` | **GPL-2.0-or-later** | reuse 解析 Debian `dep5` 格式（**见 EX-002**） |
| `python-magic` | `0.4.27` | MIT | reuse 的文件类型探测 |
| `tomlkit` | `0.15.2` | MIT | reuse 读写 TOML 配置 |

> `pip` / `setuptools` / `wheel` 属虚拟环境自带工具，不计入项目依赖。

**字段约束**

| 字段 | 约束 |
|---|---|
| 精确版本 | 锁定版本号。不接受 `^1.2`、`~1.2`、`latest`、版本区间 |
| 来源仓库 | 官方仓库 URL；不得填镜像或第三方转载站 |
| 许可证 SPDX | 必须用 SPDX 标识符；无法确定时写 `NOASSERTION` 并进入人工审查 |
| 分类 | `Runtime` / `Development` / `Test` 三者之一 |
| 随发行包分发 | `是` / `否`。`是` 则触发发行时的许可证义务 |
| 含 NOTICE | `是` / `否`。`是` 则须同时登记其 NOTICE 内容的存放位置 |
| 审查结论 | `允许` / `需人工批准` / `禁止`，附一句依据 |

---

## 3. 外部工具依赖（非发行物）

以下工具由**用户自行安装**，不随本项目分发。它们不受上述登记表约束，
但必须在此列出，以便使用者知道运行时依赖及其许可证。

| 工具 | 版本 | 许可证 | 用途 | 调用方式 | 本项目是否分发 |
|---|---|---|---|---|---|
| Pandoc | 待 Phase 1 锁定 | GPL-2.0-or-later | Markdown → DOCX 导出 | 独立进程（`fork/exec`），不链接 | **否**，由用户安装 |

**为什么单列**：ADR-LIC-003 要求登记「是否随发行包分发」。Pandoc 采用
「用户自行安装」模式（P6 决策），本项目不承担其 GPL 分发义务；但若日后改为
随产品分发二进制，必须移入 §2 登记表，并在发行时履行 GPL 义务（随附源码或书面要约）。

**Phase 1 待办**：锁定实际使用的 Pandoc 版本并填入上表。

---

## 4. 放行规则

| 许可证 | 处理 |
|---|---|
| MIT / BSD-2-Clause / BSD-3-Clause / ISC / Apache-2.0 | 自动通过，但仍须检查附加条款（BSD-4 广告条款、MIT 变体措辞、Apache NOTICE） |
| MPL-2.0 / LGPL-2.1 / LGPL-3.0 / EPL-2.0 / CDDL-1.0 | 警告 + **需人工批准** |
| GPL-2.0 / GPL-3.0 / AGPL-3.0 | **禁止**，例外需书面批准 |
| 未知 / 无许可证 / 自定义条款 | **禁止** |

---

## 5. 例外流程

任何「需人工批准」或「禁止」项的例外，必须写入 `compliance/exceptions.yaml`：

```yaml
- package: example-lib
  version: 1.4.2
  license: LGPL-3.0
  reason: "仅用于测试夹具，不进入发行包"
  approved_by: <姓名>
  approved_at: 2026-11-07
  review_by: 2027-05-07
```

无此记录一律视为**未批准**。`review_by` 到期未复审的例外自动失效。

---

## 6. 变更流程

1. 在 PR 中新增/修改依赖
2. 同步更新本文件的 §2 表
3. PR 描述勾选「已登记 THIRD-PARTY.md」
4. review 时核对：版本是否为精确值、许可证是否与登记一致、是否随发行包分发

每次依赖变更都必须更新本文件——**包括版本升级**。
