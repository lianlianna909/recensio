# 证据 E1: python-docx Track Changes 能力

## 问题 F1
原报告称 python-docx「Track Changes：好」，但 python-docx 公开 API **没有**修订标记接口，`w:ins`/`w:del` 需手工操作 oxml 层。

## 正确描述
python-docx **只能**：
- 创建文档
- 添加文本/段落/表格
- 设置样式

**不能**：
- 直接解析/修改 `w:ins`/`w:del` 修订标记
- 直接操作 OOXML 层

## 证据来源
- python-docx 官方文档：https://python-docx.readthedocs.io/
- python-docx GitHub：https://github.com/python-docx/python-docx
- 无 Track Changes API 的确认

## 结论
python-docx **不支持** Track Changes 解析，需手工解析 oxml 层或改用 docx4j。
