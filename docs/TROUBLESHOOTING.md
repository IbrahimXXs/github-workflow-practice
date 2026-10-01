# Troubleshooting

- **GitHub user not found:** check the account spelling and whether the account is publicly accessible.
- **HTTP 403 or 429:** GitHub denied or limited the request. Wait before retrying. A displayed reset value is a Unix timestamp in seconds; access restrictions can also cause 403 responses.
- **Certificate verification failed:** repair the Python installation's CA certificates. On macOS, a system CA bundle can be selected with `SSL_CERT_FILE=/etc/ssl/cert.pem` if that trusted bundle exists. Never disable certificate verification.
- **Could not reach GitHub:** check network access and try again later. Do not disable TLS verification.
- **Unexpected response or invalid JSON:** a proxy or upstream service may have returned unexpected data. Retry once later and report persistent failures.
- **Fewer repositories than expected:** only public repositories are fetched. Forks and archived repositories are excluded unless their flags are supplied.
- **No language:** repositories without a primary language are grouped under Unspecified.

To report a problem, provide the command, Python version, and error text without credentials. Use a repository issue or ibrahimsarraj1@gmail.com.
