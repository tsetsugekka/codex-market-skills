---
name: stock-technical-analysis
description: 分析股票与指数的趋势、支撑压力、量价动能、突破回踩和有条件的入场止损退出计划。
---

# Stock Technical Analysis

## 可用资料与边界

使用本轮实际可用的网页、连接工具和用户资料；有本机执行能力时，也按需使用已安装且可用的研究 Skill。先读取所需页面正文，核对代码、市场日期、行情时间与交易阶段；只搜索到标题不算取得数据。价格、新闻、讨论各有用途，未知字段保持未知，单点行情不能证明持续承接或完整分钟路径。入口失败时说明具体缺口，换用可读的公开来源；遇限流或拒绝访问停止请求该来源，不尝试绕过。

需要补充数据时先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现并使用相关 Skill，包括可用的 OpenD、MX 和同花顺；未加载或未调用成功就不要声称使用。插件本身不新增行情工具或权限。报告与交易执行分开，不凭研究结论声称下单。自动任务遵守自身 Prompt 的输出、归档与模拟账本合同，本插件不修改任务或自身规则。


## 必读深度与执行顺序

涉及日内、分时、买卖点、支撑压力、突破回踩、指标、图表或交易计划时，先读取[完整技术分析手册](../../../skills/stock-technical-analysis/references/technical-analysis-playbook.md)对应章节；复杂多周期问题读完整手册。补齐手册的结构、指标、背离、FVG/Vegas、图表读取与策略一致性方法，不以入口短文代替。

先判断收益逻辑和持有期，再判断周期、价格位置、量价、动能、结构、市场/行业背景，最后给触发与失效。只给图表时，可以论证执行失效，不能凭图证明长期基本面。分析 1 小时以上波段或事件行情，要结合相关新闻与情绪，避免纯图形自循环。

K线先核对标的、市场、复权、时区、周期及最新完整 bar。可用本机行情时优先真实序列；只有截图时说明可读区间，不填补不可见历史。美股 1 分钟数据、指数不支持、跨市场无权限等均按实际返回处理，不能为了套流程把 ETF 直接称作指数。

## 关键判断

- 突破需站稳与量价支持；一次触价或瞬时越线不是可成交确认。
- 放量不涨可提示派发，但需位置与后续结构支持；缩量回调只有守住支持才可能健康。
- 第一次碰压力回落不自动是顶部。若回收支持守住、低点抬高、缩量整理后再攻，可能是压力消化或第二次攻击。
- 陡峭但有序的趋势中，超买是热度警示，不能单独推导必须卖出。优先看更高低点、支撑转换和回撤深度。
- 利好后上影、连续更低高点、失去事件日收盘/关键位，属于事件溢价回吐候选；故事仍好不能取消短线失效。
- 指标冲突时用价格、成交及大盘/板块验证：跌破支撑后的金叉可能只是反抽，强趋势回踩守位的死叉可能只是整理。
- 技术背离需同周期真实价格与指标序列；无法计算时只能描述价格结构，不能声称 MACD/RSI 背离。

## 可执行性与计划一致性

当前距离阻力的剩余空间、合理止损距离、成交量/点差、交易单位及事件风险共同决定可行性。不能用事后最低价“证明”机会优秀，不能建议已过去的买点仍可成交。区分日内止盈与趋势持有，两种目标可对应不同处理，但每种都需自洽。

对齐收益来源、入场、执行止损、逻辑失效、时间止损和退出。执行失效关注近端结构；长期逻辑失效需业绩/现金流/竞争力证据。不得用一种策略入场、另一种策略延长亏损持有。A 股新买股票不能默认当日卖出；其他限制按标的核验。

价格代理换算需同时间锚、基差和比例。场外成交区只作为潜在流动性位置，确认支撑/压力仍需后续价格接受。多轮复核比较真正迁移的关键位、路径和成交条件，不保留已经失效的第一次压力位。



## 核心方法

确认代码、价格时间、复权口径与图表周期；读取公开图表/数据或用户提供的图像，不假设能看到用户的桌面。以实际可得序列分析，不从单点推断VWAP、指标值或分钟先后。

1. 明确收益逻辑与持有期：事件重定价、危机修复、质量成长、价值、股息或纯技术交易。图表不能证明基本面逻辑。
2. 比较现价、开盘、昨收、前高低、可得均线/VWAP及缺口，先定位再看信号。
3. 量价确认：放量突破还需站稳；量增价滞可能派发；缩量回踩仅在支撑保持时才健康。
4. 在真实指标/序列存在时读KDJ、MACD、RSI和动能背离；区分延续、空中加油、回踩确认、破位反抽和冲高回落。
5. 结合行业、同业、宏观与情绪核对叙事。A股/日股催化优先相应个股方法；美股期权位置不能替代价格确认。
6. 同一收益逻辑推导触发、执行止损、逻辑失效、时间止损与退出。没有可观察条件时说明限制，不虚构精确概率。

美股场外成交/暗池价位仅是候选流动性区，方向须价格确认；短成交量不等于空头持仓。A股和日股不套用此层。SPY换算SPX使用同一时点比值，注明代理与期货基差，不固定乘10。

## DTM Index And Theme Context

For DTM data, use the canonical JSON interfaces in `https://daytrading.monster/api-docs/`. When relevant to the target index, read `https://daytrading.monster/api/gamma/` for SPX/SPXW structure and SPX Camarilla, `https://daytrading.monster/api/camarilla/nikkei` for Nikkei, or `https://daytrading.monster/api/camarilla/sse` for Shanghai Composite. Use the returned session and timestamps; Japan/A-share premarket analysis skips the corresponding Camarilla snapshot rather than treating an old session as current. These fixed-index snapshots are context, not arbitrary-stock K-lines or a complete option chain. For theme context, select `https://daytrading.monster/api/themes?market=us`, `https://daytrading.monster/api/themes?market=jp`, or `https://daytrading.monster/api/themes?market=cn`; use members and completed-session performance, not assumed live intraday strength. Parse these `text/plain` bodies as JSON and reuse relevant data already obtained upstream.

## Output Style

Reply in Chinese unless the user asks otherwise. Be decisive but conditional.

Use this compact structure when useful:

1. `结论`: state whether the setup is strong, weak, or only a candidate, and name the key confirmation level.
2. `技术结构`: trend, support/resistance, moving averages, and K-line pattern.
3. `量价/动能`: volume, KDJ/MACD/RSI, divergence, and funding/order-flow clues if available.
4. `触发条件`: what must happen for the bullish or bearish scenario to confirm.
5. `失效条件`: the level or signal that invalidates the read.
6. `计划一致性`: when a trade plan is requested, distinguish execution invalidation from thesis invalidation and state the exit/time-stop condition derived from the same thesis.

Avoid giving direct trading instructions. Use probability bands only when the evidence supports them, and explain what would change the probability.

需要深入应用此方法时读取 [研究细则](../../../skills/stock-technical-analysis/references/technical-analysis-playbook.md)。
