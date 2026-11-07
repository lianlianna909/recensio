# Grammar & Hashing Test Vectors (B3 / B6 + B1/B2/B4/B5 consistency)

> 生成者：`research/data-model/tests/run_vectors.py --emit`（正则与结果均由脚本产出，勿手改）
> 被测文档：`../SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §6.0（文法唯一定义）、§5.3（哈希契约）、§3.0.6（D-04 落位）、§2.2（实体清单）
> 执行：`python -I research/data-model/tests/run_vectors.py`；全部 PASS 时退出码 0

## 0. 被测正则（= §6.0 的可执行副本，与提案 §6.0 逐字一致）

```python
ID_PREFIX = (
    r"prj|msc|sec|par|fig|pnl|res|mth|exp|ref|cit|clm|ast|rnd|iss|pat|rsp|tab|eqn"
)
B32 = r"[0-9A-HJKMNP-TV-Z]"          # Crockford Base32 body alphabet (I L O U excluded)
PANEL_LETTER = r"[A-Z][0-9]?"        # A .. Z, or two-level A1 .. Z9

ID_PATTERN = rf"(?:{ID_PREFIX})_{B32}{{8}}"          # 供 VR-20 使用（^…$ 由调用方加）
ID_RE = re.compile(ID_PATTERN)
BLOCK_ANCHOR_RE = re.compile(rf"(?:sec|par|eqn)_{B32}{{8}}")
TOKEN_KINDS = "fig|figref|tab|tabref|eq|eqref|sec|pnl|res|pat"
TOKEN_RE = re.compile(
    r"\{\{(?P<kind>" + TOKEN_KINDS + r")"
    rf":(?P<id>(?:{ID_PREFIX})_{B32}{{8}})"
    rf"(?:\#(?P<panel>{PANEL_LETTER}))?"
    r"(?:\|(?P<opts>[^}|\s][^}|]*))?\}\}"
)
ANCHOR_RE = re.compile(rf"\s+\^(?:sec|par|eqn)[_-]{B32}{{8}}\s*$")
INLINE_CITE_ROLES = "support|contrast|method_source|background|refute|data_source"
INLINE_CITE_RE = re.compile(
    rf"\[\[(?P<ref>ref_{B32}{{8}})"
    r"(?:\#locator=(?P<locator>[^|\]]+))?"
    rf"(?:\|role=(?P<role>{INLINE_CITE_ROLES}))?\]\]"
)
FENCE_OPEN_RE = re.compile(r"^ {0,3}```yaml[ ]+swp:(?P<block>[a-z][a-z0-9-]*)[ ]*$")
```

## 1. 结果表

| # | 被测对象 | 输入 | 期望 | 实际 | 判定 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| G1-01 | ID_RE.fullmatch | `fig_7K3M9Q2P` | match | match | PASS |  |
| G1-02 | ID_RE.fullmatch | `par_9QK2M4XZ` | match | match | PASS |  |
| G1-03 | ID_RE.fullmatch | `tab_4XQ7NWKB` | match | match | PASS | 新增 Table 实体前缀（B3） |
| G1-04 | ID_RE.fullmatch | `eqn_2VH8RTMW` | match | match | PASS | 新增 Equation 实体前缀（B3） |
| G1-05 | ID_RE.fullmatch | `eq_2VH8RTMW` | no match | no match | PASS | 两字母前缀不合法；Equation 固定用 eqn_（audit B3） |
| G1-06 | ID_RE.fullmatch | `tab_4XQ7NWK` | no match | no match | PASS | 长度不足 8 |
| G1-07 | ID_RE.fullmatch | `fig_7k3m9q2p` | no match | no match | PASS | 小写不在 Crockford 字母表 |
| G1-08 | ID_RE.fullmatch | `fig_7K3M9Q2I` | no match | no match | PASS | Crockford 剔除 I L O U |
| G1-09 | ID_RE.fullmatch | `doc_7K3M9Q2P` | no match | no match | PASS | 前缀不在 §6.0 注册表 |
| G2-01 | BLOCK_ANCHOR_RE.fullmatch | `sec_4M2P8QKT` | match | match | PASS |  |
| G2-02 | BLOCK_ANCHOR_RE.fullmatch | `par_9QK2M4XZ` | match | match | PASS |  |
| G2-03 | BLOCK_ANCHOR_RE.fullmatch | `par-9QK2M4XZ` | no match | no match | PASS | 连字符是锚点写法，不是 ID 写法 |
| G2-04 | BLOCK_ANCHOR_RE.fullmatch | `fig_7K3M9Q2P` | no match | no match | PASS | 图/表为独立文件，不得用块锚点 |
| G2-05 | BLOCK_ANCHOR_RE.fullmatch | `eqn_2VH8RTMW` | match | match | PASS | Equation 是内联弱实体，用块锚点承载 ID |
| G3-15b | TOKEN + semantic(no #panel) | `{{fig:fig_7K3M9Q2P#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{tab:tab_4XQ7NWKB#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{tabref:tab_4XQ7NWKB#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{eq:eqn_2VH8RTMW#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{eqref:eqn_2VH8RTMW#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{sec:sec_4M2P8QKT#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{res:res_5RTV2WQK#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-15b | TOKEN + semantic(no #panel) | `{{pat:pat_8KHJ3MNQ#B}}` | matched, semantic reject | panel=B | PASS | 语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06） |
| G3-01 | TOKEN_RE.finditer | `{{fig:fig_7K3M9Q2P}}` | {'kind': 'fig', 'id': 'fig_7K3M9Q2P', 'panel': None, 'opts': None} | {'kind': 'fig', 'id': 'fig_7K3M9Q2P', 'panel': None, 'opts': None} | PASS |  |
| G3-02 | TOKEN_RE.finditer | `{{tab:tab_4XQ7NWKB}}` | {'kind': 'tab', 'id': 'tab_4XQ7NWKB', 'panel': None, 'opts': None} | {'kind': 'tab', 'id': 'tab_4XQ7NWKB', 'panel': None, 'opts': None} | PASS | Table 定义点 |
| G3-03 | TOKEN_RE.finditer | `{{eq:eqn_2VH8RTMW}}` | {'kind': 'eq', 'id': 'eqn_2VH8RTMW', 'panel': None, 'opts': None} | {'kind': 'eq', 'id': 'eqn_2VH8RTMW', 'panel': None, 'opts': None} | PASS | Equation 定义点 |
| G3-04 | TOKEN_RE.finditer | `{{figref:fig_7K3M9Q2P}}` | {'kind': 'figref', 'id': 'fig_7K3M9Q2P', 'panel': None, 'opts': None} | {'kind': 'figref', 'id': 'fig_7K3M9Q2P', 'panel': None, 'opts': None} | PASS | 渲染 Figure 3 |
| G3-05 | TOKEN_RE.finditer | `{{figref:fig_7K3M9Q2P#B}}` | {'kind': 'figref', 'id': 'fig_7K3M9Q2P', 'panel': 'B', 'opts': None} | {'kind': 'figref', 'id': 'fig_7K3M9Q2P', 'panel': 'B', 'opts': None} | PASS | 面板引用（audit B3 的具体报错用例）→ Figure 3B |
| G3-06 | TOKEN_RE.finditer | `{{pnl:pnl_4ZQ7NWKB}}` | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': None, 'opts': None} | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': None, 'opts': None} | PASS | 保留于词汇表（自有 ID，仍需身份） |
| G3-07 | TOKEN_RE.finditer | `{{tabref:tab_4XQ7NWKB}}` | {'kind': 'tabref', 'id': 'tab_4XQ7NWKB', 'panel': None, 'opts': None} | {'kind': 'tabref', 'id': 'tab_4XQ7NWKB', 'panel': None, 'opts': None} | PASS | Table 引用点 |
| G3-08 | TOKEN_RE.finditer | `{{eqref:eqn_2VH8RTMW}}` | {'kind': 'eqref', 'id': 'eqn_2VH8RTMW', 'panel': None, 'opts': None} | {'kind': 'eqref', 'id': 'eqn_2VH8RTMW', 'panel': None, 'opts': None} | PASS | Equation 引用点 |
| G3-09 | TOKEN_RE.finditer | `{{res:res_5RTV2WQK\|fmt=31.0}}` | {'kind': 'res', 'id': 'res_5RTV2WQK', 'panel': None, 'opts': 'fmt=31.0'} | {'kind': 'res', 'id': 'res_5RTV2WQK', 'panel': None, 'opts': 'fmt=31.0'} | PASS | 数值注入 |
| G3-10 | TOKEN_RE.finditer | `{{pat:pat_8KHJ3MNQ}}` | {'kind': 'pat', 'id': 'pat_8KHJ3MNQ', 'panel': None, 'opts': None} | {'kind': 'pat', 'id': 'pat_8KHJ3MNQ', 'panel': None, 'opts': None} | PASS | 修订引用 |
| G3-11 | TOKEN_RE.finditer | `{{figref:fig_a,fig_b}}` | no match | no match | PASS | 多目标须写并列 token：{{figref:fig_a}}–{{figref:fig_b}}（§6.7） |
| G3-12 | TOKEN_RE.finditer | `{{figref:fig_7K3M9Q2P#BC}}` | no match | no match | PASS | 面板字母=1 位大写 + 可选 1 位数字 |
| G3-13 | TOKEN_RE.finditer | `{{figref:fig_7K3M9Q2P#}}` | no match | no match | PASS | # 后必须跟合法面板字母 |
| G3-14 | TOKEN_RE.finditer | `{{eqref:eq_2VH8RTMW}}` | no match | no match | PASS | Equation 前缀固定 eqn_ |
| G3-15 | TOKEN_RE.finditer | `{{fig:fig_7K3M9Q2P#B}}` | {'kind': 'fig', 'id': 'fig_7K3M9Q2P', 'panel': 'B', 'opts': None} | {'kind': 'fig', 'id': 'fig_7K3M9Q2P', 'panel': 'B', 'opts': None} | PASS | 语法接受；语义上 fig 定义点不得带 #panel（G3-15b） |
| G3-16 | TOKEN_RE.finditer | `{{pnl:pnl_4ZQ7NWKB#A}}` | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': 'A', 'opts': None} | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': 'A', 'opts': None} | PASS | pnl 允许 #panel（§6.0.4 规则 1） |
| G3-17 | TOKEN_RE.finditer | `{{pnl:pnl_4ZQ7NWKB\|style=raw}}` | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': None, 'opts': 'style=raw'} | {'kind': 'pnl', 'id': 'pnl_4ZQ7NWKB', 'panel': None, 'opts': 'style=raw'} | PASS | opts 透传 |
| G4-01 | ANCHOR_RE.sub | `text ^par_9QK2M4XZ` | rest=text | rest=text | PASS | 下划线写法被剥离 |
| G4-02 | ANCHOR_RE.sub | `text ^par-9QK2M4XZ` | rest=text | rest=text | PASS | 连字符写法被剥离 |
| G4-03 | ANCHOR_RE.sub | `## Introduction ^sec_4M2P8QKT` | rest=## Introduction | rest=## Introduction | PASS | 标题行锚点 |
| G4-04 | ANCHOR_RE.sub | `## Introduction ^sec-4M2P8QKT` | rest=## Introduction | rest=## Introduction | PASS | 标题行连字符写法 |
| G4-05 | ANCHOR_RE.sub | `text ^fig_7K3M9Q2P` | rest=text ^fig_7K3M9Q2P | rest=text ^fig_7K3M9Q2P | PASS | 非锚点，原样保留 |
| G4-06 | ANCHOR_RE.sub | `text ^par_9QK2M4XZ trailing` | rest=text ^par_9QK2M4XZ trailing | rest=text ^par_9QK2M4XZ trailing | PASS | 锚点必须在行尾 |
| G4-07 | ANCHOR_RE.sub | `text ^par_9qk2m4xz` | rest=text ^par_9qk2m4xz | rest=text ^par_9qk2m4xz | PASS | 小写 body 不合法 |
| G4-09 | ANCHOR_RE.sub | `  $$ x = 1 $$ ^eqn_2VH8RTMW` | rest=  $$ x = 1 $$ | rest=  $$ x = 1 $$ | PASS | 公式块锚点同样被剥离 |
| G4-10 | ANCHOR_RE.sub | `text ^par_9QK2M4XZ  ` | rest=text | rest=text | PASS | 尾随空白并入锚点一起剥离 |
| G4-08 | ANCHOR_RE.sub | `text
^par_9QK2M4XZ` | rest=text | rest=text | PASS | 锚点独占下一行也应剥离 |
| G5-01 | INLINE_CITE_RE | `[[ref_2ABCDEFG#locator=p42\|role=support]]` | {'ref': 'ref_2ABCDEFG', 'locator': 'p42', 'role': 'support'} | {'ref': 'ref_2ABCDEFG', 'locator': 'p42', 'role': 'support'} | PASS |  |
| G5-02 | INLINE_CITE_RE | `[[ref_2ABCDEFG]]` | {'ref': 'ref_2ABCDEFG', 'locator': None, 'role': None} | {'ref': 'ref_2ABCDEFG', 'locator': None, 'role': None} | PASS |  |
| G5-03 | INLINE_CITE_RE | `[[ref_2ABCDEFG#locator=fig2\|role=locus]]` | None | None | PASS | role 必须在枚举内，否则不是引文标记 |
| B6-01 | text_hash | `The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK\|fmt=31.0}} reduction in tumour volume` | 见判定 | b61d80e882d0b66f | PASS | 无锚点（基准）（必须与 B6-01 全等） |
| B6-02 | text_hash | `The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK\|fmt=31.0}} reduction in tumour volume ^par_9QK2M4XZ` | 见判定 | b61d80e882d0b66f | PASS | 下划线锚点（必须与 B6-01 全等） |
| B6-03 | text_hash | `The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK\|fmt=31.0}} reduction in tumour volume ^par-9QK2M4XZ` | 见判定 | b61d80e882d0b66f | PASS | 连字符锚点（必须与 B6-01 全等） |
| B6-04 | text_hash | `The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK\|fmt=31.0}} reduction in tumour volume   ^par_9QK2M4XZ  ` | 见判定 | b61d80e882d0b66f | PASS | 锚点 + 行尾空白（必须与 B6-01 全等） |
| B6-05 | text_hash | `The initial dose of 10 mg/kg produced a {{res:res_5RTV2WQK\|fmt=31.0}} reduction in tumour volume
` | 见判定 | b61d80e882d0b66f | PASS | CRLF/尾换行（必须与 B6-01 全等） |
| B6-06 | text_hash | `The initial dose of 10 mg/kg produced a  reduction in tumour volume ^par_9QK2M4XZ` | 见判定 | 19a0d16d7aa79946 | PASS | 内容已变（数值占位被删）→ 哈希必须不同（与 B6-01 不同才算正确） |
| B5-01 | frontmatter_flatten | `schemas/d04-compliant.example.md` 全部 frontmatter 块 | >=1 block, 0 violations | 2 blocks, 0 violations | PASS | D-04：禁止 object / list<object>   |
| B5-02 | fence_blocks(swp:meta) | `schemas/d04-compliant.example.md` | present | present | PASS | blocks=['meta', 'sections', 'equations', 'citations', 'targets'] |
| B5-02 | fence_blocks(swp:sections) | `schemas/d04-compliant.example.md` | present | present | PASS | blocks=['meta', 'sections', 'equations', 'citations', 'targets'] |
| B5-02 | fence_blocks(swp:equations) | `schemas/d04-compliant.example.md` | present | present | PASS | blocks=['meta', 'sections', 'equations', 'citations', 'targets'] |
| B5-02 | fence_blocks(swp:citations) | `schemas/d04-compliant.example.md` | present | present | PASS | blocks=['meta', 'sections', 'equations', 'citations', 'targets'] |
| B5-02 | fence_blocks(swp:targets) | `schemas/d04-compliant.example.md` | present | present | PASS | blocks=['meta', 'sections', 'equations', 'citations', 'targets'] |
| B1-01 | cross-document | P2 表：Panel.figure 为唯一权威边 | present | present | PASS |  |
| B1-02 | cross-document | Panel 字段表：derived_from 降为纯血缘 | present | present | PASS |  |
| B1-03 | cross-document | Panel 字段表：figure 行标注唯一权威边 | present | present | PASS |  |
| B4-01 | cross-document | P2 表：Figure.result_refs[] 为唯一权威边 | present | present | PASS |  |
| B4-02 | cross-document | Result.figures 标注派生缓存 + 权威指向 | present | present | PASS |  |
| B2-01 | cross-document | targets 单一形态 {par, manuscript, section?, quote_hint?, patch?} | present | present | PASS |  |
| B2-02 | cross-document | §4.6 引用同一形态（不再各写一套） | present | present | PASS |  |
| B3-00 | cross-document | 实体总数 19，且全文无「17 个实体」 | present | present | PASS |  |
| B3-01 | cross-document | §6.0 声明为文法唯一定义 | present | present | PASS |  |
| B3-02 | cross-document | §3.18 词汇表引用 §6.0（不再自带正则） | present | present | PASS |  |
| B3-03 | cross-document | #panel 片段已在 §6.0 / §3.18 出现 | present | present | PASS |  |
| B3-04 | cross-document | ANCHOR_RE 修正版写入 §5.3 | present | present | PASS |  |
| B5-02 | cross-document | 落位映射表存在（含 x_ext → swp:meta） | present | present | PASS |  |
| B5-03 | cross-document | 示例 frontmatter 按 VR-53/VR-54 校验（19 前缀 / 禁嵌套） | present | present | PASS |  |
| B6-00 | cross-document | §6.0.5 与 §5.3 引用同一 ANCHOR_RE（含 [_-] 与 eqn） | present | present | PASS |  |
| B3-05 | cross-document | §6.0.8 可执行定义与本脚本 grammar_source() 逐字一致（无漂移） | present | present | PASS |  |
| B3-06 | cross-document | schema 的 id_pattern 含 tab/eqn 且计数 19（§6.0.2 同步） | present | present | PASS |  |
| B5-04 | cross-document | manuscript.example.md frontmatter 亦为零嵌套（D-04） | present | present | PASS |  |

## 2. 可直接粘贴执行的等价断言

```python
from run_vectors import ID_RE, TOKEN_RE, ANCHOR_RE, text_hash

assert ID_RE.fullmatch("tab_4XQ7NWKB")
assert ID_RE.fullmatch("eqn_2VH8RTMW")
assert not ID_RE.fullmatch("eq_2VH8RTMW")            # 审计 B3：两字母前缀
m = TOKEN_RE.fullmatch("{{figref:fig_7K3M9Q2P#B}}")   # 审计 B3：# 片段
assert m and m.group("panel") == "B"
assert not TOKEN_RE.fullmatch("{{figref:fig_a,fig_b}}")
assert ANCHOR_RE.sub("", "Paragraph text ^par_9QK2M4XZ") == "Paragraph text"
assert ANCHOR_RE.sub("", "Paragraph text ^par-9QK2M4XZ") == "Paragraph text"
assert text_hash("P text ^par_9QK2M4XZ") == text_hash("P text ^par-9QK2M4XZ") == text_hash("P text")
```

## 3. 判定语义

- `text_hash`：B6-01…B6-05 必须**全等**（同一段落，有/无锚点、`_`/`-` 两种写法、行尾空白、尾换行）；B6-06 必须**不同**（文本内容真的变了，哈希须反映）。
- `#panel` 的归属是**语义规则**而非文法规则：`TOKEN_RE` 对所有 kind 都接受 `#A`…`#Z9`；`fig`/`tab`/`eq`/`sec`/`res`/`pat` 带上 `#panel` 时由渲染器入口丢弃该片段并报 VR-06（G3-15b），`figref`/`pnl` 才解释它。
- `B1/B2/B3/B4/B5` 行是跨文件一致性断言（P2 表 ↔ 字段表 ↔ schema ↔ 示例文件），任何文档改动后必须重跑。
