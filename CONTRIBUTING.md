# Contributing

Keep changes focused and explain the user-visible behavior in the pull request.

1. Create a branch from main.
2. Implement the change using the Python standard library where practical.
3. Add a regression test for changed behavior. Unit tests should mock network access.
4. Run `python3 -m unittest -v` and `python3 repo_summary.py --help`.
5. Update APP.md or docs when commands or output fields change.

Avoid committing credentials or live private data. API tests should not require a personal access token. If changing pagination, verify empty, full, and partial pages as well as duplicate repository IDs.
