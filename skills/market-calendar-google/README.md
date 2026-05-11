# Market Calendar Google

`market-calendar-google` 是一个用于 Codex 的市场日历 skill。它把美股财报、日股财报、中美日宏观数据、央行事件、美债拍卖和其他重要市场事件整理成 Google Calendar 日程。

这个目录里的 `SKILL.md` 是给 Codex 执行时读取的规则文件；本 `README.md` 是给 GitHub 用户阅读的公开说明。

## 能做什么

- 整理指定周的 Earnings Whispers 美股财报日历。
- 根据用户提供的美股或日股关注列表筛选重点财报。
- 整理中美日重要宏观数据、央行事件、拍卖和财经事件。
- 按日本时间写入 Google Calendar。
- 自动合并同一 30 分钟时间段内的多个事件。
- 为五星事件设置醒目的 Google Calendar 颜色。

## 典型请求

```text
整理下周 Earnings Whispers 财报图，并添加到 Google Calendar。
```

```text
整理本周中美日四星以上财经事件，加入 Google Calendar。
```

```text
根据这个 CSV 关注列表，整理下周日股财报。
```

## 需要的权限和来源

- 需要 Codex 的 Google Calendar 连接器来创建或更新日历事件。
- 会在需要当前事件、财报或共识数据时读取公开网页或公开日历来源。
- 不需要本地 API token。
- 不会自动读取 `.env` 或其他凭据文件。

## 输出和写入规则

- 默认用中文写日程详情。
- 默认时区为 `Asia/Tokyo`。
- 写入日历前应先搜索同一周已有事件，避免重复。
- 只在用户明确要求写入 Google Calendar 时创建或更新日程。

## 公开安全说明

这个 skill 可以放在公开仓库中。请不要把个人关注列表、Google Calendar 私有输出、浏览器缓存、`.env`、token 或其他私密文件提交进来。

本 skill 生成的市场事件说明仅用于个人研究和日程管理，不构成投资建议。
