# License Policy — Header 规范与检查方案

> 配套决策：`decisions/ADR-LIC-001-003.md`
> 适用范围：本仓库全部自有内容

---

## 1. 先分清两件事

| 类别 | 内容 | 性质 |
|---|---|---|
| **Apache-2.0 的法律要求** | 分发时附许可证副本；修改过的文件显著标注；分发物含 `NOTICE` 时须一并传递且不得改写其归属（§4） | 法律义务 |
| **本项目的自律规范** | 每文件加 SPDX 标识与版权头；维护 `THIRD-PARTY.md`；CI 检查；SBOM | 工程规范，**Apache-2.0 不强制** |

本文档描述的是**第二类**。不要把自律规范说成法定义务。

---

## 2. Header 模板

### 2.1 Python

```python
# Copyright 2026 马蕾娜 (Leina Ma)
# SPDX-License-Identifier: Apache-2.0
```

放在 shebang（如有）之后、模块 docstring 之前：

```python
#!/usr/bin/env python3
# Copyright 2026 马蕾娜 (Leina Ma)
# SPDX-License-Identifier: Apache-2.0
"""Module docstring."""
```

### 2.2 TypeScript / JavaScript

```typescript
// Copyright 2026 马蕾娜 (Leina Ma)
// SPDX-License-Identifier: Apache-2.0
```

### 2.3 YAML / TOML / Shell

```yaml
# Copyright 2026 马蕾娜 (Leina Ma)
# SPDX-License-Identifier: Apache-2.0
```

### 2.4 Markdown（仅限**新增的**规范类文档）

```markdown
<!--
Copyright 2026 马蕾娜 (Leina Ma)
SPDX-License-Identifier: Apache-2.0
-->
```

---

## 3. 适用范围

| 类型 | 是否加 Header | 理由 |
|---|---|---|
| 自有源码（`.py` / `.ts` / `.js` / `.sh`） | **加** | 主要分发单元 |
| 配置文件（`.yaml` / `.toml` / `.json`） | 视情况 | 有注释语法的加；纯 JSON 不加 |
| 文档（`.md`） | **不加** | 见下条 |
| `research/` 下的审计与证据文件 | **不加** | 会改变文件字节，破坏已记录的 SHA-256 指纹与行号引用 |
| 第三方代码 | **不加**，且不改其原有声明 | 加本项目头会造成归属错误 |
| 自动生成的文件 | 由生成器负责，不手改 | 手改会在下次生成时丢失 |

> `research/` 的例外是硬约束：Phase 0 的证据链以文件字节指纹为依据，
> 加 Header 等于篡改证据。这类文件的许可证归属由根目录 `LICENSE` 与 `NOTICE` 覆盖。

---

## 4. 检查方案

### 阶段一：人工 + `reuse`（Phase 1）

| 项 | 做法 |
|---|---|
| 依赖登记 | 手工维护 `THIRD-PARTY.md`（Phase 1 依赖数预期 < 10） |
| Header 校验 | FSFE `reuse` 的 `reuse lint` |
| 引入审批 | PR 模板勾选「是否新增依赖」 |

**前置条件**：`reuse lint` 需先在本仓库实测通过。若其对 `research/` 的豁免规则
需要额外配置，必须提交 `.reuse/dep5` 说明豁免依据，不得靠"视而不见"绕过。

### 阶段二：自动化扫描（首个外部依赖落地时）

| 生态 | 候选工具 | 状态 |
|---|---|---|
| Python | `pip-licenses` / `licensecheck` | 待实测 |
| Node | `license-checker-rseidelsohn` | 待实测 |
| 通用 | `reuse` | 待实测 |
| SBOM | CycloneDX（`cyclonedx-py` 等） | 待实测 |

> 以上均为候选，**未在本机验证**。采用前须逐个实测其对当前技术栈的支持度。

### 阶段三：CI 门禁（Phase 2 起）

```
1. reuse lint                  → SPDX header 缺失即失败
2. 依赖许可证扫描              → 检出 GPL/AGPL/未知即失败
3. THIRD-PARTY.md 一致性检查   → 清单与登记表不一致即失败
4. SBOM 生成并归档
```

托管平台为 GitHub，上述步骤以 GitHub Actions 实现。

---

## 5. 例外

- 依赖类例外 → `compliance/exceptions.yaml`（见 `THIRD-PARTY.md` §5）
- Header 类例外 → 在 `.reuse/dep5` 中按路径声明，并注明理由
- 两类例外都必须有**批准人**与**复审日期**

---

## 6. 已知待办

- [ ] 在本地实测 `reuse lint`，确认对 `research/` 的豁免可配置
- [ ] 决定 CI 上 DCO 检查方式（`dcoapp` GitHub App 或自建 Actions job）
- [ ] Phase 1 锁定 Pandoc 版本，填入 `THIRD-PARTY.md` §3
