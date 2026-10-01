# Examples

Run these commands from the repository directory.

## Human-readable summary

```sh
python3 repo_summary.py IbrahimXXs
```

## Include forks and archived projects

```sh
python3 repo_summary.py IbrahimXXs --include-forks --include-archived
```

## Export JSON

```sh
python3 repo_summary.py IbrahimXXs --json > report.json
```

Check the command's exit status before using the file: shell redirection can create an empty report even when the command fails. This command replaces an existing `report.json`.

## Read the star total

```sh
python3 -c 'import json; print(json.load(open("report.json"))["stars"])'
```

Results change as GitHub repositories change. No API token is required.
