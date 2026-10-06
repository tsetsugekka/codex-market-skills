# Codex Market Skills maintenance

## 目录职责与版本边界

- 根 `skills/` 是独立安装和 Plugin 共用的唯一 Skill 源码；不得在 `plugin/` 维护副本或能力缩减版。
- `plugin/` 仅放说明和根 Skill 链接；根 `.codex-plugin/plugin.json`、`assets/logo.svg`、`build_plugin.py` 负责插件分发。
- 按运行时实际能力和授权选择工具，不按 ChatGPT/Codex 名称限制方法。
- Private Reference 正文和索引保存在仓库外，按公共双读契约读取，不发布或打包。
- 每个独立 Skill 的必读公共 Reference 必须包含在自身目录，不能靠另一个 Skill 或仓库根目录补齐。公共契约唯一底稿在 `shared/references/`；运行 `python3 sync_skill_references.py` 同步各 Skill 内的普通文件，提交前用 `--check` 核验。实际私人正文仍在仓库外。
- 独立安装与插件安装会提供同名 Skill；不得为清理重复入口擅自卸载整个插件。

## Maintenance

- This checkout tracks the public GitHub main branch and is the source of the linked local skills. Before edits, inspect branch, index and worktree and fetch the current origin/main. Reconcile baseline/local/upstream intent through `shared/references/release-and-privacy.md` before publishing; a unique local difference may already be superseded upstream. Preserve recovery evidence and never overwrite work blindly.
- Keep reusable source changes in reviewed commits on main. Before commit/push, inspect only the intended diff and apply `shared/references/release-and-privacy.md`. Do not accumulate a private variant as long-lived uncommitted changes to public tracked files.
- Private RAG, account data and personal defaults stay outside the public source. Local handoffs, release receipts, packages and recovery snapshots use ignored `.local/`; current handoff is `.local/TASK.md`. Never stage that directory. This AGENTS.md is tracked and published with the repository.
- Global skill links may point into `skills/`; preserve these paths and update the source once. Do not treat plugin-cache installations or temporary release copies as authoritative.
- GitHub source synchronization does not publish a marketplace/plugin version. Follow the existing release workflow only within the requested scope.
