# Codex Market Calendar Google

一个用于 Codex 的市场日历 skill：整理某一周的美股财报日历，或中美日重要财经数据/事件日历，并按规则写入 Google Calendar。

## 能做什么

- 查找并整理某一周的美股财报日历。
- 优先从 Reddit `r/EarningsWhisper` 找 Earnings Whispers 周度财报图，并确认周次。
- 读取用户提供的美股关注列表 CSV，用关注顺序决定日历标题里的重点 ticker。
- 整理中美日宏观数据、央行事件、美债拍卖、重要财经事件。
- 按日本时间写入 Google Calendar。
- 自动使用国旗标记国家：`🇺🇸`、`🇨🇳`、`🇯🇵`。
- 五星事件自动改为 Google Calendar 红色。
- 同一 30 分钟时间段内的多个事件自动合并。

## 安装

把仓库目录放到 Codex skills 目录下：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/tsetsugekka/codex-market-calendar-google.git ~/.codex/skills/market-calendar-google
```

重启 Codex 或开启新会话后，skill 会被自动发现。

## 示例请求

```text
整理下周 Earnings Whispers 财报图，并添加到 Google Calendar。
```

```text
整理本周中美日四星以上财经事件，加入 Google Calendar。
```

```text
用这个 CSV 里的关注顺序，整理下周美股财报日历。
```

## 财报日历规则

- 标题格式：

```text
🇺🇸 ER | TICKER TICKER TICKER
```

- 美股盘前：按美东 `08:30` 换算到日本时间，持续 30 分钟。
- 美股盘后：按美东 `16:00` 换算到日本时间，持续 30 分钟。
- 自动处理美国夏令时/冬令时；夏令时通常对应日本时间 `20:30` / 次日 `05:00`，冬令时通常对应 `22:30` / 次日 `06:00`。
- 标题只放重点 ticker。
- 详情保留该时段全部 ticker。
- 详情用中文写重点看点，不写“解析来源”或本地文件路径。

## 财经事件规则

- 四星以上、有具体发布时间的事件才默认写入日历。
- 数据发布类事件持续时间为 0 分钟。
- 讲话/发布会类事件持续时间为 30 分钟。
- 详情包含：
  - 重要度
  - 预期/前值
  - 高于预期的影响
  - 低于预期的影响
- 影响尽量写清楚利多/利空对象，例如美元、美债收益率、纳指、成长股、黄金、加密、中概、日元、日本银行股等。

## 备注

这个 skill 默认不使用 X，因为 X 经常需要登录或额外浏览器权限。默认优先使用 Reddit `r/EarningsWhisper`、Earnings Whispers 官网日历，以及其他可验证来源交叉确认。
