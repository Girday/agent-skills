# Contributing

Add a skill under `skills/<lowercase-hyphenated-name>/`, then add its catalog entry to both READMEs. Explain the concrete task it handles and provide a realistic usage example.

Keep `SKILL.md` focused on decisions and workflow. Place detailed references, reusable scripts, and templates in separate resources when they help. Make required dependencies explicit and provide a usable fallback for optional agent-specific tools.

Include material you are entitled to publish. Cite external sources, preserve their licensing requirements, and distinguish original analysis from authoritative source text. Do not include private infrastructure details, personal document data, credentials, local machine paths, or proprietary reference files.

For executable changes, add tests that exercise observable behavior, especially overwrite protection, reported failures, and representative outputs. Record what was actually tested and what still requires manual review. Do not describe a successful script run as a full correctness or compliance guarantee.

Before opening a pull request, run the development checks in the README. If LaTeX behavior changes, compile the affected example and inspect its PDF pages as well. Keep generated build files out of Git; deliberately published examples belong under `examples/` with their sources and a short description.
