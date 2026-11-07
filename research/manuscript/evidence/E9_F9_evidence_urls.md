# 证据 E9: URL 可达性台账（v0.3 重写，关闭 N3/G2-1）

> 访问日期: **2026-11-07**（Asia/Shanghai）· 方法: `curl.exe -sS -L --max-time 30~60 -w "%{http_code} -> %{url_effective}"`
> 规则: 报告与本目录只引用下表「采用」区（HTTP 200）的 URL；失败 URL 仅作为处置记录保留，不再被任何断言依赖。

## 1. 采用（HTTP 200，全部实测）

| # | URL | HTTP | 用于 | 内容核验 |
|---|-----|------|------|----------|
| 1 | https://github.com/python-openxml/python-docx | 200 | E1/E5 | 真实仓库，组织 python-openxml |
| 2 | https://python-docx.readthedocs.io/en/latest/ | 200 | E1/E5 | 官方文档站 |
| 3 | https://python-docx.readthedocs.io/en/latest/api/document.html | 200 | E1/E5 | 含「paragraphs within revision marks such as `<w:ins>` or `<w:del>` do not appear」原文 |
| 4 | https://github.com/python-openxml/python-docx/blob/master/src/docx/document.py | 200 | E1 | `Document(ElementProxy)`、`add_comment`、`comments` 源码可见 |
| 5 | https://github.com/Plutext/docx4j | 200 | E4 | Plutext 官方仓库；HTML 内 defaultBranch=`VERSION_17_3_6` |
| 6 | https://javadoc.io/doc/org.docx4j/docx4j-openxml-objects/latest/org/docx4j/wml/RunIns.html | 200 | E4 | 解析到 11.5.14 |
| 7 | https://javadoc.io/static/org.docx4j/docx4j-openxml-objects/11.5.14/org/docx4j/wml/RunIns.html | 200 | E4 | 「Inserted Run Content … Java class for ins element declaration」 |
| 8 | https://javadoc.io/static/org.docx4j/docx4j-openxml-objects/11.5.14/org/docx4j/wml/RunDel.html | 200 | E4 | 「Deleted Run Content … Java class for del element declaration」 |
| 9 | https://ecma-international.org/publications-and-standards/standards/ecma-376/ | 200 | E6/E11 | ECMA-376 标准页 |
| 10 | https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.insertedrun?view=openxml-3.0.1 | 200 | E1/E2 | 标题 InsertedRun Class；qualified name = w:ins |
| 11 | https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.deletedrun?view=openxml-3.0.1 | 200 | E1/E2 | 标题 DeletedRun Class；qualified name = w:del |
| 12 | https://pandoc.org/MANUAL.html#option--from | 200 | E2（清单行） | 锚点 `id="option--from"` 实测存在，附近文本含 docx |
| 13 | https://pandoc.org/MANUAL.html#option--reference-doc | 200 | E7 | 锚点实测存在 |
| 14 | https://pandoc.org/MANUAL.html#latex | 200 | E9 | 锚点 `id="latex"` 实测存在（复审称未检出，本轮复核为存在） |
| 15 | https://github.github.com/gfm/#tables-extension- | 200 | E6 | 锚点 `id="tables-extension-"` 实测存在 |
| 16 | https://commonmark.org/help/ | 200 | （备查） | 可达，但 CommonMark 本身不含表格，E6 改引 GFM Spec |
| 17 | https://github.com/mwilliamson/mammoth.js | 200 | E3 | 仓库主页 |
| 18 | https://github.com/mwilliamson/mammoth.js/blob/master/README.md | 200 | E3 | 「using semantic information … ignoring other details」原文 |

## 2. 失败 / 弃用（实测记录，断言已删除或替换）

| URL | HTTP | 处置 |
|-----|------|------|
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packageword.insertion?view=openxml-2.8.1 | 404 | 删除，替换为 #10 |
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packageword.deletion?view=openxml-2.8.1 | 404 | 删除，替换为 #11 |
| https://www.e-iceblue.io/docx4j/api/ | 000（DNS 解析失败） | 删除；该站属 e-iceblue 商业产品，与 docx4j（Plutext）无关，替换为 #5–#8 |
| https://github.com/python-docx/python-docx | 404 | 删除，替换为 #1 |
| https://www.docx4java.org/trac/docx4j | 403 | 不采用 |
| https://www.docx4j.org/ | 000（连接超时） | 不采用 |
| https://python-openxml.readthedocs.io/en/latest/ | 404 | 不采用；官方文档站在 python-docx.readthedocs.io（#2） |
| https://python-docx.readthedocs.io/en/latest/dev/analysis/schema.html | 404 | 不采用 |
| https://raw.githubusercontent.com/python-openxml/python-docx/master/src/docx/document.py | 000（连接被重置） | 本机网络限制；改用 GitHub blob 页 #4 |
| https://raw.githubusercontent.com/Plutext/docx4j/master/docx4j-core/src/main/java/org/docx4j/wml/RunIns.java | 000（连接被重置） | 同上；且路径/分支不存在（blob 页 404），改用 javadoc #7 |
| https://github.com/Plutext/docx4j/blob/master/docx4j-core/src/main/java/org/docx4j/wml/RunIns.java | 404 | 默认分支非 master；类型化对象证据改用 javadoc #7/#8 |
| https://api.github.com/repos/Plutext/docx4j | 403（rate limit exceeded，IP 级） | 不采用；分支信息改从仓库 HTML（#5）提取 |
| https://pandoc.org/MANUAL.html#input-MS-Word-documents | 200（页面可达，锚点不存在） | 页面 HTML 中无 `id="input-MS-Word-documents"`，旧引用不切题，替换为 #12 |

## 3. 无 URL 的未确认项（不保留死链，不编造出处）

- E8 LibreOffice Markdown 转换：未实测 → 报告 §12-11。
- E10 PDF/OCR 准确率：无产物，数字已删 → 报告 §12-9。
- docx4j 接受/拒绝修订端到端语义：未实测 → 报告 §12-10。

## 结论

报告 §13 与本目录所有被依赖 URL 均在上表「采用」区且有 HTTP 200 记录；零死链。
