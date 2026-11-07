"""G2-2 探针：python-docx 无公开修订 API，但可经 `.element`（lxml）读写 `w:ins`/`w:del`。

运行: python research/manuscript/evidence/probe_pythondocx_trackchanges.py
依赖: python-docx 1.2.0, lxml（本机已装，无需联网）。
产物: 标准输出（落盘见 probe_pythondocx_trackchanges_output.txt）。
"""

import io
import zipfile

import docx
import lxml.etree as etree
from docx import Document

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def qn(tag):
    return f"{{{W}}}{tag}"


def make_revision_docx():
    """构造一个正文含 w:ins / w:del 的最小 DOCX（内存中，不落盘）。"""
    seed = Document()
    seed.add_paragraph("BASE TEXT")
    buf = io.BytesIO()
    seed.save(buf)
    buf.seek(0)
    with zipfile.ZipFile(buf) as src:
        root = etree.fromstring(src.read("word/document.xml"))
        para = root.find(f"{qn('body')}/{qn('p')}")
        ins = etree.SubElement(para, qn("ins"))
        ins.set(qn("id"), "1")
        ins.set(qn("author"), "probe")
        ins.set(qn("date"), "2026-11-07T00:00:00Z")
        etree.SubElement(etree.SubElement(ins, qn("r")), qn("t")).text = "INSERTED-VIA-W-INS"
        dele = etree.SubElement(para, qn("del"))
        dele.set(qn("id"), "2")
        dele.set(qn("author"), "probe")
        dele.set(qn("date"), "2026-11-07T00:00:00Z")
        etree.SubElement(etree.SubElement(dele, qn("r")), qn("delText")).text = "DELETED-VIA-W-DEL"
        patched = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data = patched if item.filename == "word/document.xml" else src.read(item.filename)
                dst.writestr(item, data)
    out.seek(0)
    return out


def main():
    print(f"python-docx version: {docx.__version__}")
    print(f"lxml version: {etree.LXML_VERSION}")

    document = Document(make_revision_docx())

    print("\n[1] 公开 API 视角（Document.paragraphs / Paragraph.text）")
    print(f"paragraph texts: {[p.text for p in document.paragraphs]}")
    print("-> 修订标记内的文本不在公开 API 的段落/运行视图中（静默不可见）")

    print("\n[2] `.element` 暴露 lxml 元素，可 xpath 读取 w:ins / w:del")
    element = document.element
    print(f"type(document.element): {type(element).__module__}.{type(element).__name__}")
    print(f"isinstance lxml.etree._Element: {isinstance(element, etree._Element)}")
    for tag in ("ins", "del"):
        for node in element.xpath(f"//w:{tag}"):
            text = "".join(node.xpath(".//w:t/text() | .//w:delText/text()", namespaces=NS))
            print(
                f"w:{tag} id={node.get(qn('id'))} author={node.get(qn('author'))} "
                f"date={node.get(qn('date'))} text={text!r} node_type={type(node).__name__}"
            )

    print("\n[3] 经 `.element` 写入新的 w:ins 并保存，重开验证持久化")
    body = element.find(qn("body"))
    new_para = etree.SubElement(body, qn("p"))
    ins = etree.SubElement(new_para, qn("ins"))
    ins.set(qn("id"), "3")
    ins.set(qn("author"), "probe-writer")
    ins.set(qn("date"), "2026-11-07T00:00:00Z")
    etree.SubElement(etree.SubElement(ins, qn("r")), qn("t")).text = "WRITTEN-VIA-ELEMENT"
    saved = io.BytesIO()
    document.save(saved)
    saved.seek(0)
    with zipfile.ZipFile(saved) as check:
        xml = check.read("word/document.xml").decode("utf-8")
    print(f"saved document.xml contains WRITTEN-VIA-ELEMENT: {'WRITTEN-VIA-ELEMENT' in xml}")
    print(f"saved document.xml contains w:ins author=probe-writer: {'probe-writer' in xml}")

    print("\n[4] 批注 API 存在性（1.2.0 起，纠正『无批注 API』的旧断言）")
    print(f"hasattr(Document, 'add_comment'): {hasattr(document, 'add_comment')}")
    print(f"hasattr(Document, 'comments'): {hasattr(document, 'comments')}")

    print("\n[5] 公开修订 API 存在性")
    for name in ("track_changes", "revisions", "accept_changes", "insertions"):
        print(f"hasattr(Document, {name!r}): {hasattr(document, name)}")


if __name__ == "__main__":
    main()
