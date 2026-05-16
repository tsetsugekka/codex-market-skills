# Release And Privacy Policy

这是给 GitHub 用户阅读的公开摘要。Codex runtime 读取的详细规则位于 `shared/references/release-and-privacy.md`；更新发布/隐私规则时，两处应保持一致，runtime 规则以 `shared/` 下的 reference 为准。

本仓库公开版 skill 可以说明如何使用私有版和本地 RAG，但不能包含私有材料本身。私有 RAG 可服务情绪面、技术分析、gamma/期权结构和其他市场研究流程。

核心规则：

- 本地分析：如果同名私密版可用且用户允许，优先用私密版。
- 更新 skill：公开安全的通用规则要同步到公开版；私有规则只留在私密版或私有 RAG。
- 上传 GitHub：只用公开版作为来源，提交前检查个人路径、API key、`.env`、`Stocks/`、私有 RAG、`.ftindex`、截图、原始 PDF/PPT、私有标签和个人信息。
- GitHub 发布分支：除非用户明确要求新分支、PR、draft PR 或实验分支，否则不要擅自创建、切换或推送临时分支；默认发布到仓库目标分支，通常是 `main`。提交前先确认当前分支，若不在目标分支，先切回并快进目标分支。
- 本地 RAG 索引技巧可以公开：可以教用户建立只含来源别名、页码/slide 范围、关键词和公开安全摘要的索引；索引内容本身不公开。
