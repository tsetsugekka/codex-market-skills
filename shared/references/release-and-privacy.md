# Release And Privacy Policy

This reference is public-safe and applies when a skill has both a public version and a private/local version, and when private RAG materials support sentiment, technical analysis, gamma analysis, or other market workflows.

## Version Priority

- Treat the installed local skill directory as the private/local working version when the user has one, and treat the GitHub repository copy as the public release version.
- For local analysis, if a valid private version of the same skill is available and the user permits using it, prefer the private version because it may contain local RAG indexes, personal workflow defaults, and user-specific study material.
- If no private version is available, use the public version plus any user-specified private RAG/index folder.
- Never assume or hard-code a private path in public files. Discover private materials from the user's explicit instruction, local install metadata, or a local-only index outside the Git repository.

## Keeping Versions In Sync

When updating a skill that has public and private variants:

1. Make the functional change in the version that the current task actually needs.
2. Decide whether the lesson is public-safe.
3. If public-safe, port the generalized rule to the public version too.
4. If private-only, keep it only in the private version or private RAG index.
5. Update both experience files when a reusable public-safe lesson affects both variants.
6. Do not let the public version mention private labels, private paths, personal positions, raw notes, screenshots, account data, or API keys.

## GitHub Upload Rule

When preparing anything for GitHub, use only the public version of the skill as the source of truth. Before staging or pushing, run a privacy check appropriate to the repository, including searches for:

- personal paths such as `/Users/...`;
- API keys, tokens, `.env`, credentials, account numbers, cookies;
- `Stocks/`, private RAG folders, `.ftindex`, screenshots, raw PDFs/PPTs, private notes;
- private strategy names, memorable private labels, private person names/handles;
- copied raw source text from private materials.

Also confirm `.gitignore` excludes private folders such as `Stocks/`, `private-rag/`, `RAG_INDEX/`, `.env*`, logs, caches, and index files.

### Branch Discipline

- Do not create, switch to, or push a new working branch for a GitHub release unless the user explicitly asks for a branch, PR, draft PR, or experimental branch.
- Default to the repository's intended target branch, usually `main`, for direct publish requests such as "commit", "push", "publish to GitHub", or "update GitHub".
- Before staging or committing, run `git branch --show-current` and confirm it is the intended target branch. If it is not, switch or fast-forward to the target branch before committing.
- If a temporary branch already exists from earlier work, do not keep using it by inertia. Either merge/fast-forward the target branch when safe, or ask the user before publishing from that branch.
- After a temporary branch has been merged into the target branch and is no longer needed, delete the local and remote temporary branch.

## Local RAG Index Rule

It is public-safe to teach the technique of building a local private RAG/index. Private RAG can support sentiment analysis, technical patterns, gamma/option structure, market calendar heuristics, and other user study materials. The public skill may say how to create an index with aliases, topics, page/slide ranges, keywords, categories such as `sentiment`, `technical`, `gamma`, and short public-safe summaries. The index content itself stays outside the public repository unless it has been stripped to public-safe generalized rules.
