import argparse
import io
import json
import unittest
from urllib.error import HTTPError, URLError
from unittest.mock import Mock
import repo_summary as app


def response(data):
    return io.StringIO(json.dumps(data))


class RepositorySummaryTests(unittest.TestCase):
    def test_username_rejects_path_injection(self):
        for value in ["../users", "a?x=1", "", "-abc", "abc-", "a" * 40]:
            with self.assertRaises(argparse.ArgumentTypeError):
                app.validate_username(value)

    def test_username_accepts_normal_accounts(self):
        self.assertEqual(app.validate_username("IbrahimXXs"), "IbrahimXXs")
        self.assertEqual(app.validate_username("a"), "a")

    def test_pagination_collects_more_than_one_page(self):
        opener = Mock(side_effect=[response([{"id": i} for i in range(100)]), response([{"id": 100}])])
        self.assertEqual(len(app.fetch_repositories("octocat", opener)), 101)
        self.assertIn("page=2", opener.call_args.args[0].full_url)

    def test_pagination_deduplicates_ids(self):
        opener = Mock(side_effect=[response([{"id": i} for i in range(100)]), response([{"id": 99}])])
        self.assertEqual(len(app.fetch_repositories("octocat", opener)), 100)

    def test_not_found_has_actionable_error(self):
        opener = Mock(side_effect=HTTPError("https://api.github.com", 404, "Missing", {}, None))
        with self.assertRaisesRegex(RuntimeError, "not found"):
            app.fetch_repositories("missing", opener)

    def test_rate_limit_has_actionable_error(self):
        opener = Mock(side_effect=HTTPError("https://api.github.com", 429, "Limited", {"X-RateLimit-Reset": "123"}, None))
        with self.assertRaisesRegex(RuntimeError, "123"):
            app.fetch_repositories("octocat", opener)

    def test_network_failure_is_wrapped(self):
        with self.assertRaisesRegex(RuntimeError, "Could not reach"):
            app.fetch_repositories("octocat", Mock(side_effect=URLError("offline")))

    def test_invalid_json_and_shape_are_rejected(self):
        for stream in [io.StringIO("not json"), response({"message": "error"}), response([{}])]:
            with self.assertRaises(RuntimeError):
                app.fetch_repositories("octocat", Mock(return_value=stream))

    def test_default_filters_exclude_forks_and_archived(self):
        repos = [
            {"id": 1, "name": "source", "language": "Python", "stargazers_count": 2, "forks_count": 1},
            {"id": 2, "fork": True, "stargazers_count": 100},
            {"id": 3, "archived": True, "stargazers_count": 100},
        ]
        report = app.summarize("demo", repos)
        self.assertEqual((report["repositories_fetched"], report["repositories_included"], report["stars"]), (3, 1, 2))
        self.assertEqual(report["languages"], {"Python": 1})
        self.assertEqual(app.summarize("demo", repos, True, True)["stars"], 202)

    def test_top_repositories_are_sorted_and_limited(self):
        repos = [{"id": i, "name": str(i), "stargazers_count": i} for i in range(7)]
        report = app.summarize("demo", repos)
        self.assertEqual([r["stars"] for r in report["top_repositories"]], [6, 5, 4, 3, 2])

    def test_empty_account_renders(self):
        report = app.summarize("demo", [])
        self.assertEqual(report["stars"], 0)
        self.assertIn("Primary languages: none", app.render_text(report))


if __name__ == "__main__":
    unittest.main()
