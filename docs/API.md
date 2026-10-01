# API integration

The tool sends GET requests to `https://api.github.com/users/{username}/repos`, requesting 100 repositories per page in full-name order. It uses the GitHub JSON media type, API version 2026-03-10, and an identifying User-Agent.

Pagination ends at the first page with fewer than 100 records. Repository IDs are deduplicated across pages. If 100 full pages are reached, the tool fails rather than silently returning a partial report. A report is not an atomic snapshot: repositories can change while pages are fetched.

Each request has a 20-second timeout. Requests are unauthenticated and share GitHub's public API rate allowance for the source IP. HTTP 403 or 429 produces an error with the reset timestamp when supplied; the tool does not automatically retry.

References: [repository endpoint](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), [rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).
