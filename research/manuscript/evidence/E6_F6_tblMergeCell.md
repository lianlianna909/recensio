# 证据 E6: w:tblMergeCell 不是标准 OOXML 元素

## 问题 F6
原报告称 `w:tblMergeCell` 是标准 OOXML 元素，但实际为 `w:gridSpan` / `w:vMerge`。

## 正确元素名
- 跨行合并：`w:vMerge` (vertical merge)
- 跨列合并：`w:gridSpan`

## 证据来源
- OOXML Schema Part 1（ECMA-376）: https://ecma-international.org/publications-and-standards/standards/ecma-376/
  — 2026-11-07 curl 实测 **HTTP 200**（`www.ecma-international.org` 同路径亦 200，重定向至无 www 主机）
- Open XML SDK 文档（`w:gridSpan`/`w:vMerge` 对应 `GridSpan`/`VerticalMerge` 类型，见 E2 的 Learn API 站）

## 结论
已更正元素名为 `w:gridSpan` / `w:vMerge`。
