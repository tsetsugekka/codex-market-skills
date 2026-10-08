# Plugin 构建与维护

## 现行契约

- `skills/`：唯一运行源码，十项 Skill、公开 Reference、采集/计算/绘图脚本。
- `.codex-plugin/plugin.json`、`assets/logo.svg`：唯一插件清单及图标。
- `plugin/README.md`：插件介绍和主 Skill 链接，不存运行副本。
- `build_plugin.py`：只读取 Git 已跟踪的上述发布文件；新增文件先纳入 Git 审查范围。排除测试，拒绝私密目录、索引、符号链接和敏感内容模式。原文字节进入 ZIP，不裁剪能力、不重写链接。
- `tests/`：包一致性、隐私边界和离线评论筛选验证。

每项 Skill 单独下载时也须完整。公共双读契约、运行能力及发布隐私规则以 `shared/references/` 为底稿，由 `python3 sync_skill_references.py` 同步到十项 Skill 的 `references/`；修改底稿后先同步，再运行 `python3 sync_skill_references.py --check`。各 Skill 的必读文件链接只指向自身目录，不能依赖相邻 Skill。跨 Skill 的可选调用仍要求对应 Skill 已安装且可用；实际私人索引和正文不在同步范围。

输出放仓库外：`python3 build_plugin.py /tmp/daytrading-monster-0.2.0.zip`。验证：`python3 -m unittest discover -s tests`。

Private Reference 位于仓库外，不能打包；只有公共读取规则进入包。发布前检查实际 ZIP 的文件列表、内容和相对链接。外部 SDK、账户权限和联网能力由宿主提供，完整脚本随包不代表所有宿主均可执行。

GitHub 推送、ZIP验证、平台扫描、提交审核和正式发布是不同状态，不相互替代。运行环境使用[共同能力规则](../skills/market-daily-strategist/references/runtime-capabilities.md)。

## 升级已有插件

在已公开插件的管理页使用 `Upload new version`，上传前后核对插件 ID 与既有安装链接一致；同名和更高版本号不能证明是同一插件。不要从新建插件入口发布更新。正式发布前保留当前线上版本；误建的独立草稿先备份并核对源码，再按平台删除确认流程清理。
