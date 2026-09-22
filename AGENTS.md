# Codex Market Skills maintenance

## 目录职责与版本边界

- 仓库根目录 `skills/` 是本仓库的独立 Skills，非 Plugin；`plugin/` 是 Plugin 的唯一维护入口，`plugin/skills/` 保存其适配内容。
- 独立 Skills 与 Plugin 允许存在运行适配差异；共享研究资料按现有构建流程复用，不因目录区分而删减内容或强行合并。
- 不得用插件清单版本代表独立 Skills 版本，不得将根目录独立 Skills 自动视为插件内容。版本号或同名显示名称不能作为判定目录职责的依据。
- 发现清单、marketplace 或发布配置与上述职责冲突时，明确报告配置冲突；不得据配置重新解释目录职责，也不得未经对应任务授权改变安装入口。

## Maintenance

- This checkout tracks the public GitHub main branch and is the source of the linked local skills. Before edits, inspect branch, index and worktree and fetch the current origin/main. Reconcile baseline/local/upstream intent through `shared/references/release-and-privacy.md` before publishing; a unique local difference may already be superseded upstream. Preserve recovery evidence and never overwrite work blindly.
- Keep reusable source changes in reviewed commits on main. Before commit/push, inspect only the intended diff and apply `shared/references/release-and-privacy.md`. Do not accumulate a private variant as long-lived uncommitted changes to public tracked files.
- Private RAG, account data and personal defaults stay outside the public source. Local handoffs, release receipts, packages and recovery snapshots use ignored `.local/`; current handoff is `.local/TASK.md`. Never stage that directory. This AGENTS.md is tracked and published with the repository.
- Global skill links may point into `skills/`; preserve these paths and update the source once. Do not treat plugin-cache installations or temporary release copies as authoritative.
- GitHub source synchronization does not publish a marketplace/plugin version. Follow the existing release workflow only within the requested scope.
