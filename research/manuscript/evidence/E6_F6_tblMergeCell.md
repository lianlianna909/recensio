# 证据 E6: w:tblMergeCell 不是标准 OOXML 元素

## 问题 F6
原报告称 `w:tblMergeCell` 是标准 OOXML 元素，但实际为 `w:gridSpan` / `w:vMerge`。

## 正确元素名
- 跨行合并：`w:vMerge` (vertical merge)
- 跨列合并：`w:gridSpan`

## 证据来源
- OOXML Schema Part 1: https://www.ecma-international.org/publications-and-standards/standards/ecma-376/
- Open XML SDK 文档

## 结论
已更正元素名为 `w:gridSpan` / `w:vMerge`。
