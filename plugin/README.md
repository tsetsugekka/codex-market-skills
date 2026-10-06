# DayTrading.Monster Plugin

[安装插件](https://chatgpt.com/plugins/plugins_6aa415f8252481919a6ac03e2072381b) · [网站](https://daytrading.monster/) · [仓库说明](../README.md)

插件直接使用根目录 `skills/` 的完整 Skill、公开 Reference 和脚本，不维护能力缩减版。独立安装和 Plugin 只是分发方式不同，方法正文只有一份；通常选择一种安装方式，避免重复显示。

本目录只提供说明。发布清单在根 `.codex-plugin/plugin.json`，图标在 `assets/logo.svg`，构建入口为 `build_plugin.py`。生成的 ZIP 包含根目录 Skill 的原文，不改写或裁剪。

## Skill 入口

- [cn-market-tape](../skills/cn-market-tape/SKILL.md)
- [cn-stock-move-reason](../skills/cn-stock-move-reason/SKILL.md)
- [jp-stock-move-reason](../skills/jp-stock-move-reason/SKILL.md)
- [macro-news-check](../skills/macro-news-check/SKILL.md)
- [market-calendar-google](../skills/market-calendar-google/SKILL.md)
- [market-daily-strategist](../skills/market-daily-strategist/SKILL.md)
- [stock-sentiment-analysis](../skills/stock-sentiment-analysis/SKILL.md)
- [stock-technical-analysis](../skills/stock-technical-analysis/SKILL.md)
- [us-stock-gamma-moomoo](../skills/us-stock-gamma-moomoo/SKILL.md)
- [us-stock-move-reason](../skills/us-stock-move-reason/SKILL.md)

## 能力与私密资料

按[当前环境能力](../skills/market-daily-strategist/references/runtime-capabilities.md)调用实际可用工具，本地能力可用就使用；没有工具时说明缺口。主 Skill 的研究方法不因此删减。

[Private Reference 规则](../skills/market-daily-strategist/references/reference-layers.md)允许读取获授权的仓库外资料；私密索引和正文不打包、不提交 GitHub。

## 构建

```sh
python3 build_plugin.py /tmp/daytrading-monster-0.2.0.zip
python3 -m unittest discover -s tests
```

[构建与发布约定](../docs/plugin-maintenance.md)。GitHub 更新不代表商店新版已发布。
