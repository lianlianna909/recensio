# D-04 合规样例（B5 验收件）

> 用途：证明「frontmatter 只放标量 / 标量列表 / wikilink 列表」这一裁决在本模型上**可以完整落地** —— 原本需要嵌套对象/`list<object>` 的字段，全部搬进正文 `swp:` 块或拆成等长平行列表。
> 依据：`decisions/ARCHITECTURE_DECISIONS.md` D-04；提案 §3.0.6（落位规则 + 块名注册表）、§3.0.7（逐字段落位映射表）。
> 自动化校验：`python -I research/data-model/tests/run_vectors.py` 的 **B5-01**（本文件每个 frontmatter 块零嵌套）与 **B5-02**（`swp:meta` / `swp:sections` / `swp:citations` / `swp:targets` 齐备）。
> 本文件包含**两个示例笔记**（示例 1 = Manuscript，示例 2 = RevisionIssue），每个示例各自是一份合法的单文件笔记。

## 示例 1：Manuscript（`msc_5TQ8WZRK`）—— 文件：`Manuscripts/msc_5TQ8WZRK.md`

```markdown
---
id: msc_5TQ8WZRK
type: manuscript
schema_version: "1.0"
project: "[[prj_2N7B4XQM]]"
title: "Dose-dependent tumour growth inhibition by compound X in a murine model"
aliases: [MS-2024-01, "Compound X paper"]
tags: [oncology, in-vivo]
created: 2026-03-02T09:14:00+08:00
updated: 2026-11-06T10:22:31+08:00
status: revision
supersedes:
notes: ""
review_state: in_review
frozen: false
visibility: internal
x_ext: ""                                  # ← D-04：只能是标量；结构化扩展见下方 swp:meta
source_asset: "[[ast_J8KP2NRT]]"
source_sha256: "3f9a1c0e77b2d4e6a8c1f0b2938d5e4716a9b3c2d0e8f7a6b5c4d3e2f1a0b9c8"
source_anchor: "docx:3f9a1c0e#whole"
source_locator_hint: "Original Word submission, 2026-03"
derived_from: []
content_hash: "b4e1f09c22d7a365"
journal: "Example Oncology Journal"
article_type: research_article
target_length_words: 4500
numbering_figure: arabic                   # ┐
numbering_table: arabic                    # │ 平行列表（原 numbering_scheme 对象，6 列）
numbering_equation: arabic                 # │
numbering_supplementary_prefix: "S"        # │
numbering_continue_across_sections: true   # │
numbering_locale: inherit                  # ┘
supplementary_of:
current_round: "[[rnd_Q3F7KM2P]]"
claims: ["[[clm_3XB8NRT5]]", "[[clm_9WD4PKMR]]"]
figures: ["[[fig_7K3M9Q2P]]"]
section_order: ["[[sec_4M2P8QKT]]", "[[sec_7B3N5RTW]]", "[[sec_2JX9KQMW]]"]
reference_style_note: "Vancouver, as per author guidelines §4.2"
---

```yaml swp:meta
# 该实体的结构化扩展（D-04 落位 B(swp:meta)）
x_ext:
  legacy:
    caption_html: "<b>Dose–response</b> of tumour volume"
  reviewer_portal_id: "EOJ-2026-0871"
```

```yaml swp:sections
# Section 弱实体元数据（§3.3）；title/level 以正文标题为准，不在此重复
- {id: sec_4M2P8QKT, role: body,       status: draft, frozen: false, acronyms_defined: [TGI, MTD], notes: ""}
- {id: sec_7B3N5RTW, role: results,    status: draft, frozen: false, acronyms_defined: [],        notes: ""}
- {id: sec_2JX9KQMW, role: discussion, status: draft, frozen: false, acronyms_defined: [],        notes: "待补 limitations"}
```

```yaml swp:equations
- {id: eqn_2VH8RTMW, caption: "where k is the decay constant", number_mode: arabic, label_prefix: equation, source: "adapted from Smith 2023, Eq. 2"}
- {id: eqn_7QMP2XKD, number_mode: none}
```

```yaml swp:citations
# 段落 par_9QK2M4XZ 的引文（弱 Citation，§3.11）
par: par_9QK2M4XZ
entries:
  - {ref: ref_2ABCDEFG, locator: "p42", role: background, verified: true}
  - {ref: ref_8KD2MQRV, locator: "Fig. 2", role: contrast, verified: false}
```

## Introduction ^sec_4M2P8QKT

Compound X has shown promising anti-tumour activity in vitro [[ref_2ABCDEFG#locator=p42|role=background]], but in vivo dose–response data remain limited ^par_9QK2M4XZ

### Dose selection is critical ^sec_2JX9KQMW

Prior studies used a narrow dose range, which we extend here ^par_1A2B3C4D

## Results ^sec_7B3N5RTW

The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK|fmt=31.0}} reduction in tumour volume ^par_6YH2NQWP

{{fig:fig_7K3M9Q2P}}

As shown in {{figref:fig_7K3M9Q2P}}, the effect was dose-dependent, and in particular {{figref:fig_7K3M9Q2P#B}} shows the plateau above 20 mg/kg ^par_8RK1MTXD

$$ \Delta V = V_0 \left(1 - e^{-kt}\right) $$ ^eqn_2VH8RTMW

Raw values are listed in {{tabref:tab_4XQ7NWKB}} ^par_5KQ8NWRT

These observations support our central claim [[clm_3XB8NRT5]] ^par_3TW6PQRS

## Discussion ^sec_2JX9KQMW
```

**本示例对应的落位清单（与 §3.0.7 逐行对应）**

| draft-1 字段 | draft-1 类型 | 本例落位 | 证据 |
| --- | --- | --- | --- |
| `numbering_scheme` | object | **PL** `numbering_*`（6 列） | frontmatter 中 6 行 `numbering_*` |
| `section_meta` | list<object> | **B(`swp:sections`)** | 上方第 2 个 fenced 块 |
| `equation_meta` | list<object> | **B(`swp:equations`)** | 上方第 3 个 fenced 块 |
| `Paragraph.citations` | list<object> | **B(`swp:citations`)** | 上方第 4 个 fenced 块 |
| `x_ext` | object | **F 标量 + B(`swp:meta`)** | frontmatter `x_ext: ""` + 块内 `x_ext:` 映射 |
| `section_order` / `claims` / `figures` | list<wikilink> | **F**（不变，合法） | frontmatter |

## 示例 2：RevisionIssue（`iss_8QW3MNRT`）—— 文件：`Revisions/iss_8QW3MNRT.md`

```markdown
---
id: iss_8QW3MNRT
type: revision_issue
schema_version: "1.0"
project: "[[prj_2N7B4XQM]]"
title: "R2-3: dose–response plateau not discussed"
aliases: [R2.3]
tags: [review, results]
created: 2026-10-28T14:02:00+08:00
updated: 2026-11-06T09:41:00+08:00
status: in_progress
supersedes:
notes: ""
review_state: in_review
frozen: false
visibility: internal
x_ext: ""
derived_from: []
round: "[[rnd_Q3F7KM2P]]"
reviewer: R2
issue_label: R2.3
source_text: "The plateau above 20 mg/kg is not discussed; Fig. 3B suggests saturation."
category: science
severity: major
scope: localized
resolution_note: ""
planned_patch: "扩写 Results 末段 + 讨论饱和机制"
blocks_submission: true
patches: ["[[pat_8KHJ3MNQ]]"]
responses: ["[[rsp_5TY2QWKB]]"]
---

```yaml swp:targets
# B2：唯一形态 {par, manuscript, section?, quote_hint?, patch?}；par 与 manuscript 必填，可选键缺省即省略
- {par: par_8RK1MTXD, manuscript: msc_5TQ8WZRK, section: sec_7B3N5RTW, quote_hint: "the effect was dose-dependent", patch: "[[pat_8KHJ3MNQ]]"}
- {par: par_3TW6PQRS, manuscript: "[[msc_5TQ8WZRK]]"}
```
```

**反例（同一份数据的 draft-1 写法，本模型禁止）**

```yaml
# ✗ frontmatter 内嵌 list<object>：Obsidian Properties 面板不支持，保存时会被拍平
targets:
  - {par: par_8RK1MTXD, manuscript: "[[msc_5TQ8WZRK]]"}
# ✗ 同义异构：draft-1 另一处写作 para_ref / quote / note，键集不封闭
# ✗ x_ext 为对象：x_ext: {reviewer_portal_id: "EOJ-2026-0871"}
```

**为什么 targets 进块而不是平行列表**：`par`/`manuscript` 是必填标量，理论上可扁平为两列平行列表；但 `section`/`quote_hint`/`patch` 是**可选键**，扁平化会产生"空串占位"与"未给出"的歧义（空串到底是没写还是写空？），因此统一进 `swp:targets` 块，块内缺省即"未给出"（§3.0.6 规则 2、§4.6）。相比之下 `Project.authors` 的 4 列全部必填/可空串，故用平行列表（§3.0.7 #15）。
