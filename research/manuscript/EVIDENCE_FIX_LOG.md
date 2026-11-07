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

---

# 第二轮：Phase 1 门禁 G2（2026-11-07）

> 依据: `reports/qa/PHASE_0_RECHECK.md` 放行条件 7（PARTIAL/RISK）与新问题 N3/N4。
> 本轮只改 `research/manuscript/`；所有 URL 均本机 curl 实测，台账见 `evidence/E9_F9_evidence_urls.md`。

## G2-1（N3）：三处出处不可达 / 张冠李戴 → 已关闭

- **问题**: Microsoft Learn 404 ×2、e-iceblue 000 且非 docx4j 官方、python-docx GitHub 组织名错误。
- **修改**:
  - Learn 旧 `packageword.insertion/deletion` URL（复测仍 404）→ 替换为
    `wordprocessing.insertedrun` / `wordprocessing.deletedrun`（view=openxml-3.0.1，实测 200）。
  - e-iceblue URL（复测 DNS 失败 000）→ 替换为 Plutext 仓库（200）+
    docx4j-openxml-objects 11.5.14 javadoc `RunIns`/`RunDel`（200，页面原文核验）。
  - `github.com/python-docx/python-docx`（复测 404）→ `github.com/python-openxml/python-docx`（200）。
  - Pandoc 旧锚点 `#input-MS-Word-documents`/`#reference-documents` 不存在 →
    `#option--from` / `#option--reference-doc`（锚点实测存在）；`#latex` 复核为存在，保留。
  - E6 改引 GFM Spec 表格扩展（200，锚点存在）；ECMA-376 页 200。
- **附带发现**: 上一轮把 SDK 类名写成 `Insertion`/`Deletion` 也不准确，正确为
  `InsertedRun`/`DeletedRun`（Learn 页面原文：qualified name = w:ins/w:del），报告与 E2 一并更正。
- **证据**: `evidence/E2_F2_wDocumentChange_class.md`、`evidence/E9_F9_evidence_urls.md`（含失败 URL 处置记录）。

## G2-2（N4）：E1 对 python-docx 能力描述过头且自相矛盾 → 已关闭

- **问题**: E1 称「不能直接操作 OOXML 层」，与 `.element` 设计及 §3.2 矛盾。
- **修改**: E1 重写为「公开 API 无修订接口，但可经 `.element`/oxml 读写 `w:ins`/`w:del`」；
  报告 §3.1/§3.2 同步；新增最小代码片段与可复现探针。
- **产物**: `evidence/probe_pythondocx_trackchanges.py` + `probe_pythondocx_trackchanges_output.txt`
  （Python 3.14.4 / python-docx 1.2.0 / lxml 6.1.0，EXIT=0；读、写、持久化均验证）。
- **附带发现（纠正任务前提）**: python-docx **1.2.0 起有批注公开 API**（`add_comment`/`comments`，
  探针 [4] 与 master 源码 blob 页双重验证）。任务书中「无批注 API」仅对 <1.2.0 成立；
  D-03 判据表按实测事实书写并显式标注该纠正。

## G2-3：D-03 判据结论 → 已交付

- 报告新增 **§3.3「D-03 判据表：python-docx 路线做 Track Changes 的代价」**
  （能力 / 代价 / 是否可接受，6 行，全部挂探针或已核验 URL）。
- 结论 14 置信度 **高 → 中**（显式下调）：docx4j 仅核验类型化对象存在，接受/拒绝端到端未实测。

## G2-4：无产物的「实测」数字 → 已关闭

- §8.2 改写为「工具实测：未执行（无样本、无脚本、无产物）」，定性表标注为经验估计；
  百分比数字维持删除状态（第一轮已删，本轮全文复查无残留）。
- E8/E10 无 URL、无产物，列入 §12-9/11；docx4j 端到端列入 §12-10。

## 本轮文件清单

- 修订: `MANUSCRIPT_TECHNICAL_AUDIT.md`（v0.3）
- 重写: `evidence/E1_F1_F2_python-docx_TrackChanges.md`、`evidence/E2_F2_wDocumentChange_class.md`、`evidence/E9_F9_evidence_urls.md`
- 补充: `evidence/E3_F3_mammoth_issues.md`、`evidence/E4_F4_tool_test_data.md`、`evidence/E6_F6_tblMergeCell.md`
- 新增: `evidence/probe_pythondocx_trackchanges.py`、`evidence/probe_pythondocx_trackchanges_output.txt`
- 追加: `EVIDENCE_FIX_LOG.md`（本节）

## 一句话结论（D-03 输入）

python-docx 做 Track Changes 的代价 = 在 lxml/oxml 层手工实现 `w:ins`/`w:del` 的解析、生成与
接受/拒绝语义，无类型安全、需自维护 ECMA-376 schema 校验；批注自 1.2.0 已有公开 API，不构成代价。
