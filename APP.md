# GitHub Repository Summary

A dependency-free Python command-line tool that uses GitHub's REST API to summarize an account's public repositories.

## Run

Requires Python 3.10 or newer. From this repository:

```sh
python3 repo_summary.py IbrahimXXs
python3 repo_summary.py IbrahimXXs --json
python3 repo_summary.py IbrahimXXs --include-forks --include-archived
```

No token, installation, or GitHub account login is needed. Forked and archived repositories are excluded by default. Reports include repository counts, stars, forks, primary languages, and the five most-starred repositories.

## Verify

```sh
python3 -m unittest -v
```

See [API behavior](docs/API.md), [output fields](docs/OUTPUT.md), [examples](docs/EXAMPLES.md), [privacy](docs/PRIVACY.md), and [troubleshooting](docs/TROUBLESHOOTING.md).

Support: ibrahimsarraj1@gmail.com
