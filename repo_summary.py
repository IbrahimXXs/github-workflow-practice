#!/usr/bin/env python3
"""Summarize public GitHub repositories without credentials or dependencies."""
import argparse
from collections import Counter
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"


def validate_username(value):
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", value):
        raise argparse.ArgumentTypeError("Use a GitHub username (1-39 letters, numbers or internal hyphens).")
    return value


def fetch_repositories(username, opener=urlopen):
    validate_username(username)
    repositories = {}
    for page in range(1, 101):
        url = f"{API_ROOT}/users/{username}/repos?per_page=100&page={page}&sort=full_name&direction=asc"
        request = Request(url, headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "IbrahimXXs-repository-summary",
        })
        try:
            with opener(request, timeout=20) as response:
                batch = json.load(response)
        except HTTPError as exc:
            if exc.code == 404:
                raise RuntimeError("GitHub user not found.") from exc
            if exc.code in (403, 429):
                reset = exc.headers.get("X-RateLimit-Reset", "unknown")
                raise RuntimeError(f"GitHub denied or rate-limited the request (HTTP {exc.code}); reset Unix timestamp: {reset}. Retry later.") from exc
            raise RuntimeError(f"GitHub returned HTTP {exc.code}.") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"Could not reach GitHub: {exc}") from exc
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError("GitHub returned invalid JSON.") from exc
        if not isinstance(batch, list) or any(not isinstance(repo, dict) or "id" not in repo for repo in batch):
            raise RuntimeError("Unexpected repository response from GitHub.")
        for repo in batch:
            repositories[repo["id"]] = repo
        if len(batch) < 100:
            return list(repositories.values())
    raise RuntimeError("Pagination exceeded 100 pages; refusing to return a partial report.")


def summarize(username, repositories, include_forks=False, include_archived=False):
    selected = [
        repo for repo in repositories
        if (include_forks or not repo.get("fork"))
        and (include_archived or not repo.get("archived"))
    ]
    languages = Counter(repo.get("language") or "Unspecified" for repo in selected)
    ranked = sorted(selected, key=lambda repo: (-repo.get("stargazers_count", 0), repo.get("name", "")))
    return {
        "username": username,
        "repositories_fetched": len(repositories),
        "repositories_included": len(selected),
        "include_forks": include_forks,
        "include_archived": include_archived,
        "stars": sum(repo.get("stargazers_count", 0) for repo in selected),
        "forks": sum(repo.get("forks_count", 0) for repo in selected),
        "languages": dict(sorted(languages.items())),
        "top_repositories": [
            {"name": repo.get("name", ""), "stars": repo.get("stargazers_count", 0),
             "url": repo.get("html_url", "")}
            for repo in ranked[:5]
        ],
    }


def render_text(report):
    lines = [
        f"Public repository summary: {report['username']}",
        f"Repositories included: {report['repositories_included']} / {report['repositories_fetched']}",
        f"Stars: {report['stars']} | Forks: {report['forks']}",
        "Primary languages: " + (", ".join(f"{name}: {count}" for name, count in report["languages"].items()) or "none"),
        "Top repositories:",
    ]
    lines.extend(f"  {repo['name']} ({repo['stars']} stars) {repo['url']}" for repo in report["top_repositories"])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username", type=validate_username)
    parser.add_argument("--include-forks", action="store_true")
    parser.add_argument("--include-archived", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print structured JSON.")
    args = parser.parse_args(argv)
    try:
        report = summarize(args.username, fetch_repositories(args.username),
                           args.include_forks, args.include_archived)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
