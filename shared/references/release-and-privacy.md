# Release And Privacy Policy

This reference governs public source maintenance and release privacy. Runtime use of public and local private research follows the [public + private reference contract](../../skills/market-daily-strategist/references/reference-layers.md).

## Reference Layers And Updates

- The tracked Skill and its public references remain the public source. A local private index adds task-scoped references; it does not replace the public Skill or grant permissions.
- Keep private indexes and content outside this repository and plugin package. Do not automatically copy a local lesson into public experience files. Update public material only when the user explicitly requests it and the proposed text is independently checked for privacy, evidence, and scope.
- Public rules and local private revisions may each change with evidence. Record the local revision's public section, scope, reason, and date in the private index; report unresolved conflicts instead of silently choosing one layer.

Before reconciling an older checkout, fetch the public history and compare the common baseline A, local edits B, and later upstream changes C by topic and intent. A different local patch or conflict-free merge does not prove that B is still valid: C may replace or withdraw it. Use dated commits and relevant release records to classify each difference as already absorbed, superseded, complementary, or unresolved; file timestamps and channel version numbers alone do not establish precedence. Preserve C when it supersedes B, merge only compatible useful changes, and keep uncertain/private material in local recovery evidence until resolved. Verify the combined behavior and contracts, including changes across different files. Do not maintain private variants as an indefinitely dirty public checkout. A GitHub commit alone does not update a separately published plugin or marketplace package.

## GitHub Upload Rule

When preparing anything for GitHub, use only the tracked public source as the release input. Before staging or pushing, run a privacy check appropriate to the repository, including searches for:

- personal paths such as `/Users/...`;
- API keys, tokens, `.env`, credentials, account numbers, cookies;
- private RAG folders, `.ftindex`, screenshots, raw PDFs/PPTs, private notes;
- private strategy names, memorable private labels, private person names/handles;
- copied raw source text from private materials.

Also confirm `.gitignore` excludes private folders such as `private-rag/`, `RAG_INDEX/`, `.env*`, logs, caches, and index files.

### Branch Discipline

- Do not create, switch to, or push a new working branch for a GitHub release unless the user explicitly asks for a branch, PR, draft PR, or experimental branch.
- Default to the repository's intended target branch, usually `main`, for direct publish requests such as "commit", "push", "publish to GitHub", or "update GitHub".
- Before staging or committing, run `git branch --show-current` and confirm it is the intended target branch. If it is not, switch or fast-forward to the target branch before committing.
- If a temporary branch already exists from earlier work, do not keep using it by inertia. Either merge/fast-forward the target branch when safe, or ask the user before publishing from that branch.
- After a temporary branch has been merged into the target branch and is no longer needed, delete the local and remote temporary branch.

## Local RAG Index Rule

It is public-safe to teach the technique of building a local private RAG/index. Private RAG can support sentiment analysis, technical patterns, gamma/option structure, market calendar heuristics, and other user study materials. The public skill may say how to create an index with aliases, topics, page/slide ranges, keywords, categories such as `sentiment`, `technical`, `gamma`, and short public-safe summaries. The index content stays outside the public repository; a generalized public rule is written only when the user explicitly requests a public Skill update and the text passes privacy review.
