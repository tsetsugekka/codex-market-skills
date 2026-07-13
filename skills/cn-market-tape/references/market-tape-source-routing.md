# Market Tape Source Routing

本文件是 `cn-market-tape` 的运行时参考。公开说明只描述“MX 主源”和“聚合公开备用源”，不把具体站点写入用户默认回答。

## Source order

### Theme strength

- 题材映射：使用 skill 目录下的 `assets/themes/theme-data.json` 和 `theme-label-i18n.json`。
- 题材行情：使用 `mx-zixuan` 一次快速覆盖，再用 `mx-xuangu` 按代码批量补齐。
- 题材驱动：用户要求解释时，使用 `mx-search` 和 `cn-stock-move-reason` 的讨论发现层。

### Sector money flow

1. 先使用 `mx-data` 或其他 MX 聚合查询，要求返回板块/行业名称、主力净流入、主力净流出、数据时间和单位。
2. MX 不支持或字段不完整时，使用同花顺公开概念资金流聚合页作为备用。
3. 备用页面只请求一次并在本地解析全量板块榜；不要按板块名称逐个请求。

资金榜金额通常以亿元展示。若源返回的是“主力净流入”一列，负值可用于净流出排序，但最终表格要把符号和列名写清楚。

已验证过的聚合备用接口族：

- 板块资金流：同花顺公开概念资金流页面 `data.10jqka.com.cn/funds/gnzjl/`，一次读取整榜。
- 大盘宽度/批量快照：东方财富 `push2delay.eastmoney.com`，只做聚合或批量请求。
- 涨停池：东方财富 `push2ex.eastmoney.com/getTopicZTPool`，按交易日读取聚合池。
- `push2.eastmoney.com` 不作为默认源；若尝试后出现 502 或其他非 JSON 响应，报告 host 和 endpoint family 并停止继续重试。

### Market breadth and limit-up pool

- 大盘指数和涨跌家数优先使用单次聚合快照接口。
- 涨停池优先使用单次聚合涨停池接口，必要时再取跌停池；不要逐只股票轮询。
- 盘中返回的涨停池会随时间变化，必须保留统计时间和交易日字段。

### Institutional survey

- 当前/最近交易日：优先 `cn-institutional-survey-heat` 的低频缓存/聚合查询，或 MX 的调研记录查询。
- 历史：优先使用 `https://daytrading.monster/surveyheat/` 及其公开历史 JSON 快照；只接受能校验日期和字段的结果。
- 历史数据缺失时，输出“尚不支持该时间/数据”，不要回退到当前快照。

## Request discipline

- 能用一个聚合请求解决时，不做逐股票、逐板块、逐日期循环。
- 同一 host 连续请求达到第 4 次前，加入 8-20 秒随机等待；有多个 host 时也不要并行轰击同一站点。
- 对同一 host 连续请求之间可使用更短的正常间隔，但不得用紧密循环。
- 如果出现 HTTP 429、403、5xx、超时、DNS 失败、连接重置或返回非 JSON：立即报告 host、endpoint family、错误类型和已尝试次数，然后停止继续增加该 host 的请求量。
- 不因一次错误切换到更多高频重试；优先使用已获得的聚合快照、缓存或 MX。

## Timestamp and fallback rules

- 每个模块都记录 `data_date`、`updated_at` 或等价时间字段；没有时间字段时标记时间不确定。
- 盘中结果只能描述为“截至该时间的快照”，不能写成全天结论。
- 盘后结果必须校验目标交易日；周末和节假日使用最近交易日并明确说明。
- 公开备用源只补齐 MX 不支持的字段，不替换题材强弱的 MX 成分行情层。
- 当备用源口径与 MX 不一致时，两者分开列出，不做未经说明的加总或平均。
