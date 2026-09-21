---
name: jp-stock-move-reason
description: 分析日本股票上涨下跌、财报反应和PTS异动，核验公司披露、预期差、量价及市场背景。
---

# Jp Stock Move Reason

## 可用资料与边界

使用本轮实际可用的网页、连接工具和用户资料；有本机执行能力时，也按需使用已安装且可用的研究 Skill。先读取所需页面正文，核对代码、市场日期、行情时间与交易阶段；只搜索到标题不算取得数据。价格、新闻、讨论各有用途，未知字段保持未知，单点行情不能证明持续承接或完整分钟路径。入口失败时说明具体缺口，换用可读的公开来源；遇限流或拒绝访问停止请求该来源，不尝试绕过。

需要补充数据时先按[环境能力路由](../market-daily-strategist/references/runtime-capabilities.md)发现并使用相关 Skill，包括可用的 OpenD、MX 和同花顺；未加载或未调用成功就不要声称使用。插件本身不新增行情工具或权限。报告与交易执行分开，不凭研究结论声称下单。自动任务遵守自身 Prompt 的输出、归档与模拟账本合同，本插件不修改任务或自身规则。


## 公司事件、期待差与资本政策

先确认股票代码、市场、交易日和常规盘/PTS；优先公司 IR、TDnet/法定披露，再用 Yahoo、Kabutan、Traders 等发现和交叉核对。掲示板负责揭示市场在讨论什么，不证明消息为真。

财报应拆分本期成绩与全年指引、上修/下修、利润率、订单/积压订单、汇率假设、一次性收益、进度率和公司历史保守程度。对照市场此前期待，而不只对照去年或公司旧指引。财报“好”但未达到期待、兑现更慢或确定性下降，可能引发利好出尽。

资本政策逐项核实：增配/特别股息、回购金额与期限及股数比例、拆股、增发、可转债、限售或大股东减持。拆股不创造企业价值，回购宣布不等于完成，融资要考虑稀释和实际资金用途。

将日经/TOPIX、对应 JPX 行业、同业、USD/JPY、JGB 收益率和海外同行作为对照。出口商、银行、成长、REIT 等受汇率/利率影响不同；先拆公司催化，再判断市场放大。海外题材传导需要业务映射和本地价格确认。

掲示板只读取适度近期样本，去重并保留时间；过滤口号和无来源断言，挑有具体公司材料的讨论再核验。高赞与高频是情绪强度，不是事实置信度。报价是当前而帖子很旧时，不能将旧讨论解释为新催化。

## PTS 与涨跌榜的完整口径

使用 DTM 三个 PTS model 时，只分析它实际提供的时段、方向和排序；其上涨名单不能称完整涨跌 Top10。需要自建推定成交额排行时，按当前 JST 与交易日选择普通盘或 PTS：普通盘 09:00–11:30、12:30–15:30；盘前/午间/收盘后早段使用相应白天 PTS，其余使用对应夜间 PTS，并核对节假日和来源标记。

先在实际获得的候选中按用户范围筛选；原工作流默认绝对涨跌幅≥3%、成交量>2,000，再按现价×成交量（PTS 则 PTS 价×PTS 量）降序。某一方向不足五只时，仅该方向可扩至≥1%，明确放宽口径。涨、跌分别排名，成交量只是筛选项；用户明确要求成交量榜时尊重该排序。

价格×成交量是推定成交额，不是逐笔成交累积。价格与量若延迟不同必须说明；无法取得完整候选时只称已取得样本排行。保留时段、价、涨跌幅、量、推定成交额及原因。除用户只要数字外，入选股票逐一解释催化；可复用任务包已有可追溯原因，不无差别逐股重抓。无材料时标未确认，不能根据行业标签编原因。

## 估值与后续验证

合理估值用指引 EPS×PE、ROE/PBR、现金流、净现金/债务、股东回报与同业作为情景锚；检查股数口径及可转债稀释。区分基本面公允价值、题材溢价和短期期待差。盈利上修与 PE 扩张可叠加，盈利下修与估值压缩也可叠加；不能只看历史低 PER。

输出最有力理由、补助理由、量价与板块共振、期待差/情绪、确定度和反证。涉及买点或关键位时读取技术 Skill，涉及周期/领导地位时读取情绪 Skill，涉及大盘/汇率/利率时读取宏观 Skill。分别判断逻辑能否持续、盘面能否延续、当前位置能否执行。



## 查询与判断

确认代码、东京市场日期和交易阶段。已有Drive事件或异动原因时先复用，再补量价验证；只在原因不清、冲突或关键决策需要时补查披露。从本轮可读公开行情补查现价、涨跌幅和行情时点；日线不能替代实时分时，读取失败时只说明实际缺口。

可先读 Yahoo Japan 个股页 `https://finance.yahoo.co.jp/quote/7203.T`，按实际上市地替换代码与后缀。从页面带标签的株価詳細値读取现价、昨收、开高低、成交量额及各自时间，并查单元株数；区分东证与夜间PTS栏，财务指标另核对应期间。整页可读不代表有连续分时，掲示板及AI値動き解説也不等同公司披露。

用公司IR、TDnet披露、决算说明资料、补充资料和Q&A解释业务变化，而不仅是财报标题。核验指引、订单兑现、利润率、现金流、融资稀释和客户集中度。

评级仅在精确代码与日期匹配时引用 `https://daytrading.monster/api/ratings-jp`，写明机构、评级/目标价变化及主催化或辅助作用；目标价不替代自主估值。主题映射读取 `https://daytrading.monster/api/themes` 并核对成分日期。

东京正常交易时优先现货；盘后可看 Kabutan 个股PTS块并注明延迟，或按对应日/盘后/夜间时段读取 `https://daytrading.monster/api/pts/model1`、`https://daytrading.monster/api/pts/model2`、`https://daytrading.monster/api/pts/model3`。这些是上涨发现来源，不称完整下跌榜。小成交的跳价低置信，不能当作次日成交价。

需要估计成交额榜时仅在价格与成交量、单位和时间均可核验后计算并注明估计，实际成交额优先；不把单笔最新价×全日量当精确成交额。Yahoo掲示板只评估零售讨论热度与传闻风险，买卖情绪比例不证明催化或方向。公开页拒绝访问或限流即停止该来源。

先完成披露和新闻核验，再按需加入宏观、情绪与技术确认。比较原预期、实际新增信息及价格接受/拒绝；新反馈出现时重新评估，不为维护旧结论忽略新证据。

## Output Style


For every stock analyzed, always use these five numbered sections in this exact order:

1. `最有力理由`: the most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme buying, short-term speculation, or market-cap/liquidity context.
3. `掲示板温度`: summarize heat level, recent post volume, high-like comments, expectation gap, and crowding risk.
4. `确定度`: high / medium / low, with one sentence explaining why.
5. `注意点`: what remains unconfirmed or what could invalidate the read.

When the user gives multiple stocks, write the five numbered sections separately for each stock first. After all individual stock sections, add a final comparison section such as `两只对比` or `多只对比`, covering common drivers, differences in catalyst quality, sentiment heat, and relative risk. You may add extra sections when useful, but the five required sections and the final comparison for multi-stock requests must remain present.

If the evidence is weak, say so plainly and use wording like `思惑`, `期待`, `传闻`, or `确认待ち`. Do not invent catalysts absent from the collected news/comments.

When explaining a catalyst, always check the expectation gap: `市场原来预期什么` -> `实际消息落地什么` -> `超预期 / 符合预期或只是落地 / 不及预期`. This applies to numeric news such as guidance, earnings, orders, dividends, and buybacks, and to qualitative news such as wording strength, timing, certainty, management confidence, regulatory tone, and whether the news solves the market's real concern.

## Valuation Requests

When the user asks for `合理估值`, `目标价`, `估值`, `贵不贵`, `空间`, `fair value`, or similar:

- Still collect current quote/news materials first, then add financial guidance, EPS/share-count, capital policy, and peer/sector context when available.
- Provide scenario ranges rather than one exact target: conservative / base / bull.
- State the anchors used, such as forward EPS/PER, operating or recurring profit, ROE/PBR, EV/EBITDA, orders/backlog, buyback/CB dilution, and peer multiples.
- When using EPS/PER, explicitly decompose price into `EPS x PER`: judge whether the setup is a Davis double play (`EPS upgrades + PER expansion` from better growth/certainty/theme premium) or Davis double kill (`EPS downgrades + PER contraction` from weaker guidance/cycle reversal/expectation miss). Do not call a stock cheap from PER alone if EPS or the deserved multiple is falling.
- Explicitly say what the current price already prices in, what must happen to justify upside, and what would invalidate the valuation.
