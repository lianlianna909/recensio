#!/usr/bin/env python3
"""Executable test vectors for SCIENTIFIC_DATA_MODEL_PROPOSAL.md (revision draft-2).

Covers:
  V-G   §6.0 grammar  : ID / BLOCK_ANCHOR / TOKEN / ANCHOR_RE / INLINE_CITE / FENCE
  V-B6  §5.3 hashing  : text_hash is invariant to anchors and to anchor spelling
  V-B5  D-04 layout   : the D-04 example's frontmatter holds no object / list<object>
  V-B1/B2/B4          : authority-edge + targets declarations agree across documents

Usage (standard library only, PyYAML not required):
    python -I research/data-model/tests/run_vectors.py            # run; exit 1 on failure
    python -I research/data-model/tests/run_vectors.py --emit     # regenerate grammar_vectors.md

The regexes below are the single executable definition of the grammar; §6.0 of the
proposal quotes them verbatim (guarded by the B3-03 consistency check).
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_MODEL = HERE.parent
PROPOSAL = DATA_MODEL / "SCIENTIFIC_DATA_MODEL_PROPOSAL.md"
D04_EXAMPLE = DATA_MODEL / "schemas" / "d04-compliant.example.md"
MS_EXAMPLE = DATA_MODEL / "schemas" / "manuscript.example.md"
SCHEMA_YAML = DATA_MODEL / "schemas" / "entity-schemas.example.yaml"
VECTORS_MD = HERE / "grammar_vectors.md"
NL = chr(10)

# §6.0 grammar — single source of truth (executable copy)
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


def normalize_text(s: str) -> str:
    """§5.3 normalizeText: identical to the proposal's Python pseudocode."""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    s = re.sub(r"[ \t]+", " ", s)
    s = ANCHOR_RE.sub("", s)                 # strip block anchors (anchors are not content)
    return "\n".join(l for l in s.strip("\n").split("\n") if l.strip())


def text_hash(s: str) -> str:
    return hashlib.sha256(normalize_text(s).encode("utf-8")).hexdigest()[:16]


def tokenize(text: str) -> list[dict]:
    return [m.groupdict() for m in TOKEN_RE.finditer(text)]


def fence_blocks(markdown: str) -> list[str]:
    """Return the swp:<name> of every swp fenced YAML block in a note."""
    out = []
    for line in markdown.splitlines():
        m = FENCE_OPEN_RE.match(line)
        if m:
            out.append(m.group("block"))
    return out


def frontmatter(markdown: str) -> str:
    if not markdown.startswith("---" + NL):
        return ""
    end = markdown.find(NL + "---" + NL, 4)
    return markdown[4:end] if end > 0 else ""


def frontmatters(markdown: str) -> list[str]:
    """Every `---` … `---` pair in the file, in order (an example file may hold >1 note)."""
    lines = markdown.split(NL)
    marks = [i for i, l in enumerate(lines) if l.strip() == "---"]
    out = []
    for a, b in zip(marks[0::2], marks[1::2]):
        out.append(NL.join(lines[a + 1:b]))
    return out


def panel_scope_ok(kind: str, panel) -> bool:
    """§6.0.4 rule 1 (semantic, NOT grammar): only figref / pnl may carry #panel."""
    return panel is None or kind in ("figref", "pnl")


def frontmatter_violations(fm: str) -> list[str]:
    """D-04: no inline object, no block object, no list<object> in frontmatter."""
    bad = []
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):[ ]*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("{") or val.startswith("[{"):
            bad.append(key + ": inline object/list<object>")
            continue
        if val == "" or val == "-":
            j = i + 1
            while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
                child = lines[j].strip()
                if child:
                    if child.startswith("-"):
                        bad.append(key + ": block list<object>")
                        break
                    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", child):
                        bad.append(key + ": block object (nested mapping)")
                        break
                j += 1
    return bad


# ---------------------------------------------------------------------------
# Vectors
# ---------------------------------------------------------------------------
ID_CASES = [
    ("G1-01", "fig_7K3M9Q2P", True, ""),
    ("G1-02", "par_9QK2M4XZ", True, ""),
    ("G1-03", "tab_4XQ7NWKB", True, "新增 Table 实体前缀（B3）"),
    ("G1-04", "eqn_2VH8RTMW", True, "新增 Equation 实体前缀（B3）"),
    ("G1-05", "eq_2VH8RTMW", False, "两字母前缀不合法；Equation 固定用 eqn_（audit B3）"),
    ("G1-06", "tab_4XQ7NWK", False, "长度不足 8"),
    ("G1-07", "fig_7k3m9q2p", False, "小写不在 Crockford 字母表"),
    ("G1-08", "fig_7K3M9Q2I", False, "Crockford 剔除 I L O U"),
    ("G1-09", "doc_7K3M9Q2P", False, "前缀不在 §6.0 注册表"),
]

ANCHOR_ID_CASES = [
    ("G2-01", "sec_4M2P8QKT", True, ""),
    ("G2-02", "par_9QK2M4XZ", True, ""),
    ("G2-03", "par-9QK2M4XZ", False, "连字符是锚点写法，不是 ID 写法"),
    ("G2-04", "fig_7K3M9Q2P", False, "图/表为独立文件，不得用块锚点"),
    ("G2-05", "eqn_2VH8RTMW", True, "Equation 是内联弱实体，用块锚点承载 ID"),
]

TOKEN_CASES = [
    ("G3-01", "{{fig:fig_7K3M9Q2P}}", {"kind": "fig", "id": "fig_7K3M9Q2P", "panel": None, "opts": None}, ""),
    ("G3-02", "{{tab:tab_4XQ7NWKB}}", {"kind": "tab", "id": "tab_4XQ7NWKB", "panel": None, "opts": None}, "Table 定义点"),
    ("G3-03", "{{eq:eqn_2VH8RTMW}}", {"kind": "eq", "id": "eqn_2VH8RTMW", "panel": None, "opts": None}, "Equation 定义点"),
    ("G3-04", "{{figref:fig_7K3M9Q2P}}", {"kind": "figref", "id": "fig_7K3M9Q2P", "panel": None, "opts": None}, "渲染 Figure 3"),
    ("G3-05", "{{figref:fig_7K3M9Q2P#B}}", {"kind": "figref", "id": "fig_7K3M9Q2P", "panel": "B", "opts": None}, "面板引用（audit B3 的具体报错用例）→ Figure 3B"),
    ("G3-06", "{{pnl:pnl_4ZQ7NWKB}}", {"kind": "pnl", "id": "pnl_4ZQ7NWKB", "panel": None, "opts": None}, "保留于词汇表（自有 ID，仍需身份）"),
    ("G3-07", "{{tabref:tab_4XQ7NWKB}}", {"kind": "tabref", "id": "tab_4XQ7NWKB", "panel": None, "opts": None}, "Table 引用点"),
    ("G3-08", "{{eqref:eqn_2VH8RTMW}}", {"kind": "eqref", "id": "eqn_2VH8RTMW", "panel": None, "opts": None}, "Equation 引用点"),
    ("G3-09", "{{res:res_5RTV2WQK|fmt=31.0}}", {"kind": "res", "id": "res_5RTV2WQK", "panel": None, "opts": "fmt=31.0"}, "数值注入"),
    ("G3-10", "{{pat:pat_8KHJ3MNQ}}", {"kind": "pat", "id": "pat_8KHJ3MNQ", "panel": None, "opts": None}, "修订引用"),
    ("G3-11", "{{figref:fig_a,fig_b}}", None, "多目标须写并列 token：{{figref:fig_a}}–{{figref:fig_b}}（§6.7）"),
    ("G3-12", "{{figref:fig_7K3M9Q2P#BC}}", None, "面板字母=1 位大写 + 可选 1 位数字"),
    ("G3-13", "{{figref:fig_7K3M9Q2P#}}", None, "# 后必须跟合法面板字母"),
    ("G3-14", "{{eqref:eq_2VH8RTMW}}", None, "Equation 前缀固定 eqn_"),
    ("G3-15", "{{fig:fig_7K3M9Q2P#B}}", {"kind": "fig", "id": "fig_7K3M9Q2P", "panel": "B", "opts": None}, "语法接受；语义上 fig 定义点不得带 #panel（G3-15b）"),
    ("G3-16", "{{pnl:pnl_4ZQ7NWKB#A}}", {"kind": "pnl", "id": "pnl_4ZQ7NWKB", "panel": "A", "opts": None}, "pnl 允许 #panel（§6.0.4 规则 1）"),
    ("G3-17", "{{pnl:pnl_4ZQ7NWKB|style=raw}}", {"kind": "pnl", "id": "pnl_4ZQ7NWKB", "panel": None, "opts": "style=raw"}, "opts 透传"),
]

ANCHOR_CASES = [
    ("G4-01", "text ^par_9QK2M4XZ", "text", "下划线写法被剥离"),
    ("G4-02", "text ^par-9QK2M4XZ", "text", "连字符写法被剥离"),
    ("G4-03", "## Introduction ^sec_4M2P8QKT", "## Introduction", "标题行锚点"),
    ("G4-04", "## Introduction ^sec-4M2P8QKT", "## Introduction", "标题行连字符写法"),
    ("G4-05", "text ^fig_7K3M9Q2P", "text ^fig_7K3M9Q2P", "非锚点，原样保留"),
    ("G4-06", "text ^par_9QK2M4XZ trailing", "text ^par_9QK2M4XZ trailing", "锚点必须在行尾"),
    ("G4-07", "text ^par_9qk2m4xz", "text ^par_9qk2m4xz", "小写 body 不合法"),
    ("G4-09", "  $$ x = 1 $$ ^eqn_2VH8RTMW", "  $$ x = 1 $$", "公式块锚点同样被剥离"),
    ("G4-10", "text ^par_9QK2M4XZ  ", "text", "尾随空白并入锚点一起剥离"),
    ("G4-08", "text" + NL + "^par_9QK2M4XZ", "text", "锚点独占下一行也应剥离"),
]

CITE_CASES = [
    ("G5-01", "[[ref_2ABCDEFG#locator=p42|role=support]]",
     {"ref": "ref_2ABCDEFG", "locator": "p42", "role": "support"}, ""),
    ("G5-02", "[[ref_2ABCDEFG]]", {"ref": "ref_2ABCDEFG", "locator": None, "role": None}, ""),
    ("G5-03", "[[ref_2ABCDEFG#locator=fig2|role=locus]]", None, "role 必须在枚举内，否则不是引文标记"),
]

B6_BASE = ("The initial dose of 10 mg/kg produced a "
           "{{res:res_5RTV2WQK|fmt=31.0}} reduction in tumour volume")
B6_CASES = [
    ("B6-01", B6_BASE, "无锚点（基准）"),
    ("B6-02", B6_BASE + " ^par_9QK2M4XZ", "下划线锚点"),
    ("B6-03", B6_BASE + " ^par-9QK2M4XZ", "连字符锚点"),
    ("B6-04", B6_BASE + "   ^par_9QK2M4XZ  ", "锚点 + 行尾空白"),
    ("B6-05", B6_BASE + NL, "CRLF/尾换行"),
    ("B6-06", "The initial dose of 10 mg/kg produced a  reduction in tumour volume ^par_9QK2M4XZ",
     "内容已变（数值占位被删）→ 哈希必须不同"),
]


def run() -> tuple[int, list[list[str]]]:
    rows: list[list[str]] = []
    failures = 0

    def rec(cid, kind, inp, expected, actual, ok, note=""):
        nonlocal failures
        if not ok:
            failures += 1
        safe = inp.replace("`", "'").replace("|", "\\|")
        rows.append([cid, kind, "`" + safe + "`", expected, actual,
                     "PASS" if ok else "**FAIL**", note])

    for cid, s, want, note in ID_CASES:
        got = ID_RE.fullmatch(s) is not None
        rec(cid, "ID_RE.fullmatch", s, "match" if want else "no match",
            "match" if got else "no match", got == want, note)

    for cid, s, want, note in ANCHOR_ID_CASES:
        got = BLOCK_ANCHOR_RE.fullmatch(s) is not None
        rec(cid, "BLOCK_ANCHOR_RE.fullmatch", s, "match" if want else "no match",
            "match" if got else "no match", got == want, note)

    # semantic rule (§6.0.4 rule 1): only figref / pnl may carry #panel
    for kind, base in (("fig", "fig_7K3M9Q2P"), ("tab", "tab_4XQ7NWKB"), ("tabref", "tab_4XQ7NWKB"),
                       ("eq", "eqn_2VH8RTMW"), ("eqref", "eqn_2VH8RTMW"), ("sec", "sec_4M2P8QKT"),
                       ("res", "res_5RTV2WQK"), ("pat", "pat_8KHJ3MNQ")):
        src = "{{" + kind + ":" + base + "#B}}"
        ms = tokenize(src)
        ok = bool(ms) and not panel_scope_ok(kind, ms[0]["panel"])
        rec("G3-15b", "TOKEN + semantic(no #panel)", src, "matched, semantic reject",
            ("panel=" + str(ms[0]["panel"])) if ms else "no match", ok,
            "语法接受、语义拒绝（语法层不拦，渲染器入口按 §6.0.4 规则 1 丢弃 panel 并报 VR-06）")

    for cid, s, want, note in TOKEN_CASES:
        ms = tokenize(s)
        if want is None:
            rec(cid, "TOKEN_RE.finditer", s, "no match", "match" if ms else "no match",
                not ms, note)
        else:
            got = {k: ms[0][k] for k in ("kind", "id", "panel", "opts")} if ms else None
            rec(cid, "TOKEN_RE.finditer", s, str(want), str(got),
                got == want and len(ms) == 1, note)

    for cid, src, want_rest, note in ANCHOR_CASES:
        rest = ANCHOR_RE.sub("", src)
        rec(cid, "ANCHOR_RE.sub", src, "rest=" + want_rest, "rest=" + rest,
            rest == want_rest, note)

    for cid, src, want, note in CITE_CASES:
        m = INLINE_CITE_RE.search(src)
        got = {k: m.group(k) for k in ("ref", "locator", "role")} if m else None
        rec(cid, "INLINE_CITE_RE", src, str(want), str(got), got == want, note)

    hashes: dict[str, str] = {}
    for cid, src, note in B6_CASES:
        hashes[cid] = text_hash(src)
        safe = src.replace("|", "\\|")
        rows.append([cid, "text_hash", "`" + safe + "`", "见判定", hashes[cid], "", note])
    for i, (cid, _s, _n) in enumerate(B6_CASES):
        idx = next(j for j, r in enumerate(rows) if r[0] == cid)
        if cid == "B6-06":
            ok = hashes[cid] != hashes["B6-01"]
            rows[idx][5] = "PASS" if ok else "**FAIL**"
            rows[idx][6] = _n + "（与 B6-01 不同才算正确）"
        else:
            ok = hashes[cid] == hashes["B6-01"]
            rows[idx][5] = "PASS" if ok else "**FAIL**"
            rows[idx][6] = _n + "（必须与 B6-01 全等）"
        failures += (not ok)

    # ---- B5: D-04 example frontmatter must be flat
    md = D04_EXAMPLE.read_text(encoding="utf-8") if D04_EXAMPLE.exists() else ""
    fm_blocks = frontmatters(md)
    viol: list[str] = []
    for i, fm in enumerate(fm_blocks, 1):
        viol += ["#%d %s" % (i, v) for v in frontmatter_violations(fm)]
    failures += (not fm_blocks) or bool(viol)
    rows.append(["B5-01", "frontmatter_flatten", "`schemas/d04-compliant.example.md` 全部 frontmatter 块",
                 ">=1 block, 0 violations",
                 str(len(fm_blocks)) + " blocks, " + str(len(viol)) + " violations",
                 "PASS" if fm_blocks and not viol else "**FAIL**",
                 "D-04：禁止 object / list<object>  " + "; ".join(viol)])
    blocks = fence_blocks(md)
    for name in ("meta", "sections", "equations", "citations", "targets"):
        ok = name in blocks
        failures += (not ok)
        rows.append(["B5-02", "fence_blocks(swp:" + name + ")", "`schemas/d04-compliant.example.md`",
                     "present", "present" if ok else "missing", "PASS" if ok else "**FAIL**",
                     "blocks=" + str(blocks)])

    # ---- Cross-document consistency (P2 table / field tables / schema)
    prop = PROPOSAL.read_text(encoding="utf-8")
    checks = [
        ("B1-01", "P2 表：Panel.figure 为唯一权威边",
         "| Figure ↔ Panel | `Panel.figure` |" in prop),
        ("B1-02", "Panel 字段表：derived_from 降为纯血缘",
         "| `derived_from` | list<wikilink> | 否 | `[]` | 纯血缘" in prop),
        ("B1-03", "Panel 字段表：figure 行标注唯一权威边",
         "**唯一权威边**（P2 表决）" in prop),
        ("B4-01", "P2 表：Figure.result_refs[] 为唯一权威边",
         "| Result ↔ Figure | `Figure.result_refs[]` |" in prop),
        ("B4-02", "Result.figures 标注派生缓存 + 权威指向",
         ("| `figures` | list<wikilink> | 否 | `[]` | **派生缓存**（B4）" in prop
          and "权威来源是 `Figure.result_refs`" in prop)),
        ("B2-01", "targets 单一形态 {par, manuscript, section?, quote_hint?, patch?}",
         "{par, manuscript, section?, quote_hint?, patch?}" in prop),
        ("B2-02", "§4.6 引用同一形态（不再各写一套）",
         "唯一形态见 §3.15" in prop),
        ("B3-00", "实体总数 19，且全文无「17 个实体」",
         "19 个实体" in prop and "17 个实体" not in prop),
        ("B3-01", "§6.0 声明为文法唯一定义",
         "唯一权威定义" in prop),
        ("B3-02", "§3.18 词汇表引用 §6.0（不再自带正则）",
         "词汇表不重复定义文法" in prop),
        ("B3-03", "#panel 片段已在 §6.0 / §3.18 出现",
         "{{figref:fig_7K3M9Q2P#B}}" in prop),
        ("B3-04", "ANCHOR_RE 修正版写入 §5.3",
         "ANCHOR_RE = re.compile(rf" in prop),
        ("B5-02", "落位映射表存在（含 x_ext → swp:meta）",
         "`x_ext`" in prop and "swp:meta" in prop),
        ("B5-03", "示例 frontmatter 按 VR-53/VR-54 校验（19 前缀 / 禁嵌套）",
         "VR-53" in prop and "VR-54" in prop),
        ("B6-00", "§6.0.5 与 §5.3 引用同一 ANCHOR_RE（含 [_-] 与 eqn）",
         "ANCHOR_RE = re.compile(rf\"\\s+\\^(?:sec|par|eqn)[_-]{B32}{{8}}\\s*$\")" in prop),
        ("B3-05", "§6.0.8 可执行定义与本脚本 grammar_source() 逐字一致（无漂移）",
         proposal_grammar_block(prop) == grammar_source()),
        ("B3-06", "schema 的 id_pattern 含 tab/eqn 且计数 19（§6.0.2 同步）",
         schema_sync_ok()),
        ("B5-04", "manuscript.example.md frontmatter 亦为零嵌套（D-04）",
         bool(frontmatters(MS_EXAMPLE.read_text(encoding="utf-8")))
         and not any(frontmatter_violations(fm)
                     for fm in frontmatters(MS_EXAMPLE.read_text(encoding="utf-8")))),
    ]
    for cid, label, ok in checks:
        failures += (not ok)
        rows.append([cid, "cross-document", label, "present",
                     "present" if ok else "missing", "PASS" if ok else "**FAIL**", ""])
    return failures, rows


def schema_sync_ok() -> bool:
    """schema 副本与 §6.0 同步：id_pattern 前缀集 == ID_PREFIX，kind_to_prefix 键集 == token kinds。"""
    if not SCHEMA_YAML.exists():
        return False
    y = SCHEMA_YAML.read_text(encoding="utf-8")
    prefixes = ID_PREFIX.split("|")
    kinds = TOKEN_KINDS.split("|")
    m = re.search(r"^id_pattern: \"\^\(([^)]+)\)_", y, re.M)
    if not m:
        return False
    have = m.group(1).split("|")
    k2p = dict(re.findall(r"(\w+): (\w+)", y.split("kind_to_prefix:", 1)[1].split("}", 1)[0]))
    return (have == prefixes
            and sorted(k2p) == sorted(kinds)
            and all(k2p[k] in prefixes for k in kinds))


def proposal_grammar_block(prop: str) -> str:
    """The ```python block under §6.0.8 of the proposal, fences and marker comment stripped."""
    i = prop.index("#### 6.0.8")
    j = prop.index("#### 6.0.9")
    seg = prop[i:j]
    fence = "`" * 3
    a = seg.index(fence + "python") + len(fence + "python")
    b = seg.index(NL + fence, a + 1)          # closing fence at line start
    lines = seg[a:b].strip(NL).split(NL)
    while lines and lines[0].startswith("# §6.0 grammar"):
        lines = lines[1:]
    return NL.join(lines).rstrip()


def grammar_source() -> str:
    """Extract the §6.0 grammar block verbatim from this file's own source."""
    src = Path(__file__).read_text(encoding="utf-8").splitlines()
    a = next(i for i, l in enumerate(src) if l.startswith("# §6.0 grammar"))
    b = next(i for i, l in enumerate(src) if l.startswith("def normalize_text"))
    return NL.join(src[a + 1:b]).rstrip()


HEAD = [
    "# Grammar & Hashing Test Vectors (B3 / B6 + B1/B2/B4/B5 consistency)",
    "",
    "> 生成者：`research/data-model/tests/run_vectors.py --emit`（正则与结果均由脚本产出，勿手改）",
    "> 被测文档：`../SCIENTIFIC_DATA_MODEL_PROPOSAL.md` §6.0（文法唯一定义）、§5.3（哈希契约）、§3.0.6（D-04 落位）、§2.2（实体清单）",
    "> 执行：`python -I research/data-model/tests/run_vectors.py`；全部 PASS 时退出码 0",
    "",
    "## 0. 被测正则（= §6.0 的可执行副本，与提案 §6.0 逐字一致）",
    "",
    "```python",
]

MID = [
    "```",
    "",
    "## 1. 结果表",
    "",
    "| # | 被测对象 | 输入 | 期望 | 实际 | 判定 | 说明 |",
    "| --- | --- | --- | --- | --- | --- | --- |",
]

TAIL = [
    "",
    "## 2. 可直接粘贴执行的等价断言",
    "",
    "```python",
    "from run_vectors import ID_RE, TOKEN_RE, ANCHOR_RE, text_hash",
    "",
    'assert ID_RE.fullmatch("tab_4XQ7NWKB")',
    'assert ID_RE.fullmatch("eqn_2VH8RTMW")',
    'assert not ID_RE.fullmatch("eq_2VH8RTMW")            # 审计 B3：两字母前缀',
    'm = TOKEN_RE.fullmatch("{{figref:fig_7K3M9Q2P#B}}")   # 审计 B3：# 片段',
    'assert m and m.group("panel") == "B"',
    'assert not TOKEN_RE.fullmatch("{{figref:fig_a,fig_b}}")',
    'assert ANCHOR_RE.sub("", "Paragraph text ^par_9QK2M4XZ") == "Paragraph text"',
    'assert ANCHOR_RE.sub("", "Paragraph text ^par-9QK2M4XZ") == "Paragraph text"',
    'assert text_hash("P text ^par_9QK2M4XZ") == text_hash("P text ^par-9QK2M4XZ") == text_hash("P text")',
    "```",
    "",
    "## 3. 判定语义",
    "",
    "- `text_hash`：B6-01…B6-05 必须**全等**（同一段落，有/无锚点、`_`/`-` 两种写法、行尾空白、尾换行）；B6-06 必须**不同**（文本内容真的变了，哈希须反映）。",
    "- `#panel` 的归属是**语义规则**而非文法规则：`TOKEN_RE` 对所有 kind 都接受 `#A`…`#Z9`；`fig`/`tab`/`eq`/`sec`/`res`/`pat` 带上 `#panel` 时由渲染器入口丢弃该片段并报 VR-06（G3-15b），`figref`/`pnl` 才解释它。",
    "- `B1/B2/B3/B4/B5` 行是跨文件一致性断言（P2 表 ↔ 字段表 ↔ schema ↔ 示例文件），任何文档改动后必须重跑。",
]


def emit_md(rows: list[list[str]]) -> str:
    body = [("| " + " | ".join(r) + " |") for r in rows]
    out = HEAD + [grammar_source()] + MID + body + TAIL
    return NL.join(out) + NL


def main() -> int:
    failures, rows = run()
    if "--emit" in sys.argv:
        VECTORS_MD.write_text(emit_md(rows), encoding="utf-8")
        print("wrote", VECTORS_MD, "(" + str(len(rows)) + " vectors)")
    else:
        for r in rows:
            print(" | ".join(r))
    print(NL + str(len(rows)) + " checks, " + str(failures) + " failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
