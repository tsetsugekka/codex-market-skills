# stock-sentiment-analysis

`stock-sentiment-analysis` 是给其他股票 skill 复用的情绪面框架。它不主动抓取行情，而是解释来自新闻、公告、股吧/掲示板、板块广度、期权 gamma、图表和用户私有 RAG 的证据。

## 能力

- 判断 A 股七阶段情绪周期：冰点、修复/潜伏、启动、加速、高潮、高位分歧/分化、退潮。
- 区分情绪票、趋势票和 hybrid。
- 分析主线、跟随、旧龙反抽、防御轮动和噪声。
- 做预期差分析：原来预期、实际落地、超预期/符合/不及预期。
- 与 `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo` 协同。
- A 股板块/题材成分、相关股、概念股、龙头股问题可用 `mx-xuangu` 做可选增强，再结合行情和资讯判断纯度、热度和催化。

## 【依赖】

- 可选：`mx-data`、`mx-search`、`mx-xuangu`，用于 A 股行情、资讯、题材成分和条件筛选增强。
- 可选：`mx-zixuan`，仅在用户明确要求东方财富自选股查询、筛选、添加或删除时使用。

## 【协同调用】

- `cn-stock-move-reason`、`jp-stock-move-reason`、`stock-technical-analysis`、`us-stock-gamma-moomoo`。

## 私有 RAG

该 skill 支持用户指定自己的私有 RAG 或索引目录，也可以帮助用户在本地建立轻量索引，记录主题、来源别名、页码/slide 范围、关键词和公开安全摘要。公开仓库不包含任何私有资料、路径、截图、API key、交易日志或专有标签。只允许在用户明确要求时，把通用、公开安全的规则摘要写回 skill。
