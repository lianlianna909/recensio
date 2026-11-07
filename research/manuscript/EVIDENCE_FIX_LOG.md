# Evidence Fix Log

## 问题 → 改了什么 → 新证据位置

### F1: python-docx Track Changes 能力断言错误（最严重）
- **问题**: 原报告称 python-docx「Track Changes：好」
- **事实**: python-docx 公开 API **没有**修订标记接口，`w:ins`/`w:del` 需手工操作 oxml 层
- **修改**:
  - 结论 14: 更正为「功能完整，**仅 docx4j 支持 Track Changes**」
  - python-docx 能力表：Track Changes 改为「中」，评价改为「需手工解析 oxml」
  - 选型理由：明确区分 docx4j 和 python-docx 的能力
- **新证据**: `research/manuscript/evidence/E1_F1_F2_python-docx_TrackChanges.md`

### F2: wDocumentChange 类不存在
- **问题**: Open XML SDK 没有 `wDocumentChange` 这个类
- **事实**: 对应类型是 `Insertion` / `Deletion` 等
- **修改**:
  - Track Changes 语义解析部分：删除 `wDocumentChange` 类引用
  - 添加正确类型名和文档 URL
- **新证据**: `research/manuscript/evidence/E2_F2_wDocumentChange_class.md`

### F3: mammoth.js GitHub Issues #342/#456 不可核验
- **问题**: 无法访问 Issues 内容
- **修改**:
  - 评价表：添加「**无修订支持**」说明
  - 选型建议：添加「GitHub Issues #342/#456 不可核验」标注
- **新证据**: `research/manuscript/evidence/E3_F3_mammoth_issues.md`

### F4: 「工具实测」数据无产物
- **问题**: §8.2 的 95%/85%/60-70% 等数字无样本、无脚本、无产物
- **修改**: 删除这些数字，改为「*数据未确认，需实测*」
- **新证据**: `research/manuscript/evidence/E4_F4_tool_test_data.md`

### F5: §9 映射表统计错误
- **问题**: 报告自报「完全可逆 1 / 单向可逆 19 / 有损 6 / 不可行 14」合计 40，实际表格 33 行
- **修改**: 逐行重数并更正为 1/19/3/10
- **新证据**: `research/manuscript/evidence/E5_F5_mapping_stats.md`

### F6: w:tblMergeCell 不是标准 OOXML 元素
- **问题**: 实际为 `w:gridSpan` / `w:vMerge`
- **修改**: 在表格说明中添加「(实际为 `w:gridSpan`/`w:vMerge`)」
- **新证据**: `research/manuscript/evidence/E6_F6_tblMergeCell.md`

### F7: 批注 XML 示例不规范
- **问题**: `w:commentRangeStart` 实际用 `w:id`，无 `w:ref` / `w:type="range"`
- **修改**: 添加正确示例和说明
- **新证据**: `research/manuscript/evidence/E7_F7_comment_xml.md`

### F8: 文首日期错误
- **问题**: 写成 2024-11-06
- **修改**: 更正为 2026-11-06
- **新证据**: `research/manuscript/evidence/E8_F8_date_error.md`

### F9: 证据清单缺 URL/版本
- **问题**: E1–E10 多数无 URL、无版本定位
- **修改**: 每条证据补齐「URL 或 文件 + 版本 + 章节」；确实无法定位的，明确标注「不可核验」
- **新证据**: `research/manuscript/evidence/E9_F9_evidence_urls.md`

---

## 文件清单

### 修订文件
- `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md`

### 证据快照
- `research/manuscript/evidence/E1_F1_F2_python-docx_TrackChanges.md`
- `research/manuscript/evidence/E2_F2_wDocumentChange_class.md`
- `research/manuscript/evidence/E3_F3_mammoth_issues.md`
- `research/manuscript/evidence/E4_F4_tool_test_data.md`
- `research/manuscript/evidence/E5_F5_mapping_stats.md`
- `research/manuscript/evidence/E6_F6_tblMergeCell.md`
- `research/manuscript/evidence/E7_F7_comment_xml.md`
- `research/manuscript/evidence/E8_F8_date_error.md`
- `research/manuscript/evidence/E9_F9_evidence_urls.md`

### 修复日志
- `research/manuscript/EVIDENCE_FIX_LOG.md` (本文件)
