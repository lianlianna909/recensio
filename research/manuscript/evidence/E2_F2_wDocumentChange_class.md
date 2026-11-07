# 证据 E2: wDocumentChange 类不存在；正确类名为 InsertedRun / DeletedRun（v0.3 重写）

> 修订日期: 2026-11-07 · 关闭 N3 的 Microsoft Learn 404 ×2，并纠正上一轮的类名。

## 事实

- Open XML SDK 中**不存在** `wDocumentChange` 类（原报告错误，F2）。
- 上一轮改写为 `Insertion`/`Deletion` **亦不准确**：SDK 的实际类是
  `DocumentFormat.OpenXml.Wordprocessing.InsertedRun` 与 `DeletedRun`。
- Microsoft Learn 页面原文（本轮抓取核验）：
  - InsertedRun: "Inserted Run Content. … When the object is serialized out as xml,
    it's qualified name is **w:ins**."
  - DeletedRun: "Deleted Run Content. … qualified name is **w:del**."

## URL 可达性（2026-11-07 curl 实测）

| URL | HTTP | 处置 |
|-----|------|------|
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.insertedrun?view=openxml-3.0.1 | 200 | 采用（不带 view 的请求亦 200，重定向到该 view） |
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.deletedrun?view=openxml-3.0.1 | 200 | 采用 |
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packageword.insertion?view=openxml-2.8.1 | 404 | 旧 URL，删除 |
| https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packageword.deletion?view=openxml-2.8.1 | 404 | 旧 URL，删除 |

## 结论

报告 §2.1/§2.2/§13 已统一改为 `InsertedRun`/`DeletedRun` + 上表 200 的 URL；零死链。
