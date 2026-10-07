# Contributing

Part of [OwlGuild](https://github.com/OwlGuild).

## Ground rules

- Small pull requests; one concern per commit.
- English commit messages in the imperative mood ("Fail build when checks drop").
- A check that cannot fail does not belong in the suite.
- CI must be green before review.

## Local checks

```bash
pip install -r requirements.txt
pytest -q
```

Against a running target (defaults to the local fixture server):

```bash
BASE_URL=http://localhost:8000 pytest -q
```

Load profile (requires [k6](https://k6.io/docs/get-started/installation/)):

```bash
BASE_URL=http://localhost:8000 k6 run load/health.js
```

The live smoke matrix (four services plus the WebSocket handshake and landing-page content)
is the `smoke.yml` workflow, dispatched from the Actions tab.

## Review

Both maintainers review before merge. Keep discussion in the PR, keep scope in the diff.
