# 证据 E7: 批注 XML 示例不规范

## 问题 F7
原报告批注 XML 示例中 `w:commentRangeStart` 使用 `w:ref` 而非 `w:id`，且无 `w:type="range"`。

## 正确示例（符合 OOXML 规范）
```xml
<w:comment w:id="1" w:author="Reviewer1" w:initials="R1">
  <w:r><w:t>请检查此数据</w:t></w:r>
</w:comment>
<!-- 批注范围应锚定到具体元素，使用 w:id 而非 w:ref -->
<!-- 正确示例：
<w:commentRangeStart w:id="crs_1"/>
<w:commentRangeEnd w:id="cre_1"/>
-->
```

## 结论
已更正为符合 OOXML 规范的批注示例。
