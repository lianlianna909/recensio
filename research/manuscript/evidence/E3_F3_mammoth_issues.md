# 证据 E3: mammoth.js GitHub Issues 不可核验（v0.3 补充可核验一手来源）

> 修订日期: 2026-11-07

## 问题 F3
原报告引用 mammoth.js GitHub Issues #342/#456 但无法核实。

## 问题
- 无法访问 Issues #342 和 #456 的具体内容
- 无法确认这些 issue 是否关于样式支持限制

## 处理
删除该引用，改用可核验来源或标注"不可核验"。

## 结论
mammoth.js Issues #342/#456 **不可核验**，已从结论依赖中移除。

## v0.3 补充：可核验的替代来源（2026-11-07 curl 实测）

| URL | HTTP | 内容 |
|-----|------|------|
| https://github.com/mwilliamson/mammoth.js | 200 | 仓库主页 |
| https://github.com/mwilliamson/mammoth.js/blob/master/README.md | 200 | README 原文：「Mammoth aims to produce simple and clean HTML by using semantic information in the document, and ignoring other details.」 |

「样式损失大」的结论现依赖 README 的设计自述（语义优先、忽略其余细节），不再依赖不可核验的 Issues。
注：README 未逐字声明 Track Changes 支持与否，报告 §3.1 中 mammoth「无修订支持」一项维持为
基于公开文档未见修订 API 的推断，未单独实测。
