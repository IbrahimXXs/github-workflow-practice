# Output reference

Use `--json` to emit one JSON object to stdout. Errors go to stderr and return exit code 1; invalid command-line arguments return 2.

| Field | Meaning |
| --- | --- |
| username | Requested GitHub account |
| repositories_fetched | Number of unique public repositories fetched |
| repositories_included | Number remaining after filters |
| include_forks / include_archived | Applied inclusion options |
| stars / forks | Sums for included repositories |
| languages | Count of repositories per primary language, not lines of code |
| top_repositories | Up to five included repositories ordered by stars descending, then name |

Each top repository has `name`, `stars`, and `url`. Missing primary languages are represented as `Unspecified`. An empty account produces zero totals and empty collections.

Counts are a snapshot of public API data, not a measure of skill, code quality, or achievement eligibility.
