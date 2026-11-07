---
# ===========================================================================
# Manuscript 示例（提案 §3.2）
# 说明：这是 *示例*，用于验证模型"落地在 Markdown + YAML 上"的可读性。
#       文件名 = 实体 ID（提案 §3.0.3）。
# ===========================================================================
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
supersedes: null
notes: ""
review_state: in_review
frozen: false
visibility: internal
x_ext: ""                            # D-04：frontmatter 只能是标量

source_asset: "[[ast_J8KP2NRT]]"
source_sha256: "3f9a1c0e77b2d4e6a8c1f0b2938d5e4716a9b3c2d0e8f7a6b5c4d3e2f1a0b9c8"
source_anchor: "docx:3f9a1c0e#whole"
source_locator_hint: "Original Word submission, 2026-03"
derived_from: []
content_hash: "b4e1f09c22d7a365"

journal: "Example Oncology Journal"
article_type: research_article
target_length_words: 4500
numbering_figure: arabic
numbering_table: arabic
numbering_equation: arabic
numbering_supplementary_prefix: "S"
numbering_continue_across_sections: true
numbering_locale: inherit
supplementary_of: null
current_round: "[[rnd_Q3F7KM2P]]"
claims: ["[[clm_3XB8NRT5]]", "[[clm_9WD4PKMR]]"]   # 派生缓存
figures: ["[[fig_7K3M9Q2P]]"]                        # 派生缓存
reference_style_note: "Vancouver, as per author guidelines §4.2"
section_order: ["[[sec_4M2P8QKT]]", "[[sec_6XW2QKMP]]", "[[sec_7B3N5RTW]]", "[[sec_2JX9KQMW]]"]  # 派生
---

```yaml swp:sections
# D-04：结构化字段进正文块（§3.0.6）；title/level 以正文标题为准
- {id: sec_4M2P8QKT, role: body,       status: draft, frozen: false, acronyms_defined: [TGI], notes: ""}
- {id: sec_6XW2QKMP, role: body,       status: draft, frozen: false, acronyms_defined: [],    notes: ""}
- {id: sec_7B3N5RTW, role: results,    status: draft, frozen: false, acronyms_defined: [],    notes: ""}
- {id: sec_2JX9KQMW, role: discussion, status: draft, frozen: false, acronyms_defined: [],    notes: ""}
```

```yaml swp:meta
x_ext: {}
```

## Introduction ^sec_4M2P8QKT

Compound X has shown promising anti-tumour activity in vitro [[ref_2ABCDEFG#locator=p42|role=background]], but in vivo dose–response data remain limited ^par_9QK2M4XZ

### Dose selection is critical ^sec_6XW2QKMP

Prior studies used a narrow dose range, which we extend here ^par_1A2B3C4D

## Results ^sec_7B3N5RTW

The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK|fmt=31.0}} reduction in tumour volume ^par_6YH2NQWP

{{fig:fig_7K3M9Q2P}}

As shown in {{figref:fig_7K3M9Q2P}}, the effect was dose-dependent, and in particular {{figref:fig_7K3M9Q2P#B}} shows the plateau above 20 mg/kg ^par_8RK1MTXD

These observations support our central claim [[clm_3XB8NRT5]] ^par_3TW6PQRS

## Discussion ^sec_2JX9KQMW

<!--
§ 阅读提示（不属于正文，导入/导出时会剥离）：

  ^sec_XXXXXXXX / ^par_XXXXXXXX   块锚点（弱实体的载体，提案 §3.3–3.4）
  [[ref_XXXXXXXX#locator=…|role=…]]  引文（弱 Citation，提案 §3.11）
  [[clm_XXXXXXXX]]                 段落表达的论断（提案 §3.12）
  {{fig:…}}                        图定义点（决定图号，提案 §6.3）
  {{figref:…}} / {{figref:…#B}}    图号引用 / 面板引用（渲染为 "Figure 3" / "Figure 3B"）
  {{tabref:…}} / {{eqref:…}}       表号 / 公式号引用（提案 §6.0.4）
  {{res:…|fmt=…}}                  数值注入（提案 §6.9）

§ 下划线合法性已由交叉确认 C1 判定为「是」（2026-11-06），^par_ 主写法保留；
   编解码器的 ^par_→^par- 映射仅为保险丝分支（未来版本收紧字符集时启用），模型语义不变。
-->

---

## 附：对应的 _maps 片段（`Manuscripts/_maps/msc_5TQ8WZRK.map.yaml`）

> 以下内容**不在**本 Markdown 文件中，而是与它并排存放于 `_maps/`。
> 此处仅作展示，说明段落身份与原稿锚点的对应关系（提案 §5.5）。

```yaml
map_version: 1
manuscript: msc_5TQ8WZRK
source_asset: ast_J8KP2NRT
source_sha256: "3f9a1c0e77b2d4e6a8c1f0b2938d5e4716a9b3c2d0e8f7a6b5c4d3e2f1a0b9c8"
generated_at: 2026-11-06T10:22:31+08:00
entries:
  - {par: par_9QK2M4XZ, order: 12, section: sec_4M2P8QKT, anchor: "docx:3f9a1c0e#p:214#hash:77e0aa11", text_hash: 77e0aa11, track_change_state: clean, tombstone: false}
  - {par: par_1A2B3C4D, order: 14, section: sec_6XW2QKMP, anchor: "docx:3f9a1c0e#p:216#hash:2c9b4e07", text_hash: 2c9b4e07, track_change_state: clean, tombstone: false}
  - {par: par_6YH2NQWP, order: 21, section: sec_7B3N5RTW, anchor: "docx:3f9a1c0e#p:241#hash:8ad31f5c", text_hash: 8ad31f5c, track_change_state: clean, tombstone: false}
  - {par: par_8RK1MTXD, order: 24, section: sec_7B3N5RTW, anchor: "docx:3f9a1c0e#p:246#hash:10ff7be2", text_hash: 10ff7be2, track_change_state: clean, tombstone: false}
  - {par: par_3TW6PQRS, order: 26, section: sec_7B3N5RTW, anchor: "docx:3f9a1c0e#p:251#hash:c4410d8e", text_hash: c4410d8e, track_change_state: clean, tombstone: false}
import_runs:
  - at: 2026-03-02T09:20:00+08:00
    tool: docx-import/0.1
    source_sha256: "3f9a1c0e77b2d4e6a8c1f0b2938d5e4716a9b3c2d0e8f7a6b5c4d3e2f1a0b9c8"
    stats: {matched: 0, inserted: 812, updated: 0, deleted: 0}
```

## 附：渲染结果预览（导出/阅读视图中的样子）

> `{{res:res_5RTV2WQK|fmt=31.0}}` → `31.0 ± 4.2 (n = 8) %`
> `{{fig:fig_7K3M9Q2P}}` → 图片 + `Figure 1. Dose–response of tumour volume to compound X.`
> `{{figref:fig_7K3M9Q2P}}` → `Figure 1`
> `{{figref:fig_7K3M9Q2P#B}}` → `Figure 1B`
> `{{pnl:pnl_4ZQ7NWKB}}` → `Figure 1B`（知道面板 ID 时的等价写法）
