# TASK: Phase 1 门禁 — Manuscript 证据可达性与描述纠正

## 0. 背景

复审 `reports/qa/PHASE_0_RECHECK.md` 把放行条件 7 判为 PARTIAL（RISK），并单列 N3/N4 两条新问题。核心风险是：**这份报告的对比表会被 D-03（python-docx vs docx4j）当作出题依据**，而它现在有两处会污染选型基线的错误。

## 1. 交付物

1. `research/manuscript/MANUSCRIPT_TECHNICAL_AUDIT.md` — 就地修订
2. `research/manuscript/evidence/` — 更新受影响的证据文件
3. `research/manuscript/EVIDENCE_FIX_LOG.md` — 追加本轮记录（不要覆盖上轮）

## 2. 必须关闭的条目

### G2-1（N3）三处出处不可达 / 张冠李戴
复审实测：Microsoft Learn 404 ×2、e-iceblue 返回 000、docx4j 的 URL 指向 **e-iceblue 商业产品站**（不是 Plutext 的 docx4j）。
**要求**：逐条替换为可访问的一手 URL 并**自己 curl 验证 HTTP 200**，把「URL + HTTP 状态 + 访问日期」写进证据文件。优先目标：
- python-docx：`python-openxml/python-docx` 仓库与官方文档
- docx4j：Plutext 的 docx4j 仓库/文档
- OOXML 类型：ECMA-376 / Microsoft Learn 的有效页面

若某条确实找不到有效页面，删除该断言，不要保留死链。

### G2-2（N4）E1 对 python-docx 能力的描述过头且自相矛盾
E1 称 python-docx「**不能**…直接操作 OOXML 层」，但库实际通过 `.element` 暴露 lxml 元素，且同报告 §3.2 又写「需手工解析 oxml 层」。
**要求**：改为准确表述——python-docx 的公开 API 无修订标记接口，但可通过 `.element` / `oxml` 访问底层 `w:ins`/`w:del`。给出能证明这一点的最小代码片段（读 `document.xml` 里 `w:ins` 的示例），并在 evidence 中附运行输出。

### G2-3 明确 D-03 的判据结论
报告必须能直接回答：**python-docx 路线做 Track Changes 的代价是什么**（手工 oxml 层、无类型安全、无批注 API、需自己维护 schema 校验）。写成一张「能力 / 代价 / 是否可接受」表，作为 D-03 的输入。

### G2-4（可选但建议）删掉仍然「不可核验」的实测数字
复审指出「实测产物」项仍全部为「不可核验」。若 `evidence/` 里的探针脚本已有可复现输出，补上；没有的，删除数字并列入未确认事项。**不要保留无产物的百分比。**

## 3. 硬性约束

- 只改 `research/manuscript/` 下文件。
- **不得编造 URL、不得编造 HTTP 状态。** 每条 URL 必须实际访问过；失败就如实写。
- 不得修改 `reports/qa/`、`research/architecture/`、`decisions/`、其他 Worker 目录、`AGENTS.md`。
- 结论若因证据不足需要下调置信度，必须显式下调。

## 4. 完成标准

- 报告与 evidence 中**零死链**（每条 URL 有 HTTP 状态记录）
- E1 与 §3.2 不再互相矛盾
- D-03 判据表可直接用于选型评审
- 无产物的「实测」数字已删除

## 5. 交付方式

≤500 字总结 + 文件清单 + 一句话结论：python-docx 做 Track Changes 的代价。
