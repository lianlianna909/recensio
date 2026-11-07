# 证据 E1: python-docx Track Changes 能力（v0.3 重写，关闭 N4/G2-2）

> 修订日期: 2026-11-07 · 本轮推翻上一版「不能直接操作 OOXML 层」的过头表述。

## 准确描述

1. **公开 API 无修订标记接口**：`Document` 无 `track_changes`/`revisions`/`accept_changes` 等属性
   （探针 [5] 实测均为 False）；官方文档明确「paragraphs within revision marks such as
   `<w:ins>` or `<w:del>` do not appear in this list」。
2. **但可经 `.element` / oxml 访问底层 OOXML**：`document.element` 返回 lxml 元素
   `docx.oxml.document.CT_Document`（`isinstance(..., lxml.etree._Element)` = True），
   可 xpath 读取并按 lxml 方式写入 `w:ins`/`w:del`，保存后持久化（探针 [2][3]）。
3. 因此正确表述是「**需手工实现 oxml 层**」，与报告 §3.2/§3.3 一致；
   旧表述「不能直接操作 OOXML 层」错误，已删除。
4. **批注**：1.2.0 起有公开 API `Document.add_comment()` / `Document.comments`
   （探针 [4] = True）。旧断言「无批注 API」仅对 <1.2.0 成立，已纠正。

## 最小代码片段（读 `document.xml` 里的 `w:ins`）

```python
from docx import Document

document = Document("with_revisions.docx")
print([p.text for p in document.paragraphs])   # 修订标记内文本不可见（静默）

element = document.element                      # lxml CT_Document
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
for ins in element.xpath("//w:ins"):            # oxml 层自带 w 前缀 nsmap
    print(ins.get(f"{{{W}}}author"),
          "".join(ins.xpath(".//w:t/text()", namespaces={"w": W})))
```

完整可复现探针（自构造含 `w:ins`/`w:del` 的 DOCX，无需外部样张）：
`probe_pythondocx_trackchanges.py`；运行输出：`probe_pythondocx_trackchanges_output.txt`
（2026-11-07，Python 3.14.4 / python-docx 1.2.0 / lxml 6.1.0，EXIT=0）。

关键输出摘录：

```text
paragraph texts: ['BASE TEXT']
type(document.element): docx.oxml.document.CT_Document
isinstance lxml.etree._Element: True
w:ins id=1 author=probe date=2026-11-07T00:00:00Z text='INSERTED-VIA-W-INS' node_type=_Element
w:del id=2 author=probe date=2026-11-07T00:00:00Z text='DELETED-VIA-W-DEL' node_type=_Element
saved document.xml contains WRITTEN-VIA-ELEMENT: True
hasattr(Document, 'add_comment'): True
hasattr(Document, 'track_changes'): False
```

注意 `node_type=_Element`：python-docx 未给 `w:ins`/`w:del` 注册定制元素类，
修订节点是**原生 lxml 元素，无类型安全**——这是 §3.3 D-03 判据表的直接依据。

## 证据来源（2026-11-07 curl 实测）

| URL | HTTP | 说明 |
|-----|------|------|
| https://github.com/python-openxml/python-docx | 200 | 真实仓库（组织 python-openxml） |
| https://python-docx.readthedocs.io/en/latest/api/document.html | 200 | 修订视图限制原文 |
| https://github.com/python-openxml/python-docx/blob/master/src/docx/document.py | 200 | `Document(ElementProxy)`、`add_comment`、`comments` 源码 |
| https://github.com/python-docx/python-docx | 404 | 旧错误 URL，已删除 |
| https://python-openxml.readthedocs.io/en/latest/ | 404 | 文档站仍在 python-docx.readthedocs.io，此 URL 弃用 |

## 结论

python-docx 做 Track Changes：公开 API 缺位，但 oxml 层完全可达；代价是手工解析/生成、
无类型安全、需自维护 schema 校验（详见报告 §3.3 D-03 判据表）。
