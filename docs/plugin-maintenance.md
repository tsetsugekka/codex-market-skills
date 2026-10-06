# Plugin 构建与维护

## 现行契约

- `skills/`：唯一运行源码，十项 Skill、公开 Reference、采集/计算/绘图脚本。
- `.codex-plugin/plugin.json`、`assets/logo.svg`：唯一插件清单及图标。
- `plugin/README.md`：插件介绍和主 Skill 链接，不存运行副本。
- `build_plugin.py`：只读取 Git 已跟踪的上述发布文件；新增文件先纳入 Git 审查范围。排除测试，拒绝私密目录、索引、符号链接和敏感内容模式。原文字节进入 ZIP，不裁剪能力、不重写链接。
- `tests/`：包一致性、隐私边界和离线评论筛选验证。

输出放仓库外：`python3 build_plugin.py /tmp/daytrading-monster-0.2.0.zip`。验证：`python3 -m unittest discover -s tests`。

Private Reference 位于仓库外，不能打包；只有公共读取规则进入包。发布前检查实际 ZIP 的文件列表、内容和相对链接。外部 SDK、账户权限和联网能力由宿主提供，完整脚本随包不代表所有宿主均可执行。

GitHub 推送、ZIP验证、平台扫描、提交审核和正式发布是不同状态，不相互替代。运行环境使用[共同能力规则](../skills/market-daily-strategist/references/runtime-capabilities.md)。
