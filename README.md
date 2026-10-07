# devflow-qa

Contract and load checks across the DevFlow stack. This repository exists because "it works
locally" is not a claim — it is a hypothesis.

[![CI](https://github.com/OwlGuild/devflow-qa/actions/workflows/ci.yml/badge.svg)](https://github.com/OwlGuild/devflow-qa/actions/workflows/ci.yml)
[![k6](https://img.shields.io/badge/load-k6-d01010.svg)](https://k6.io/)
[![pytest](https://img.shields.io/badge/tests-pytest-555555.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Why this exists

Four repositories ship one product. Individually each can pass its tests while the whole thing
still breaks. This repo tests the seams: HTTP contracts and behaviour under load.

## What runs

| Suite | Tool | What it proves |
|---|---|---|
| Contract | pytest | status codes, response shape and routing stay stable |
| Load | k6 | p95 latency and error rate stay inside budget at target concurrency |

Both run without external dependencies: the contract suite boots its own fixture server, so it
is green in CI before any service is deployed.

## Quickstart

```bash
git clone https://github.com/OwlGuild/devflow-qa.git
cd devflow-qa
pip install -r requirements.txt
pytest -q            # contract suite
k6 run load/health.js   # load profile, needs BASE_URL
```

To point the suite at a real deployment instead of the fixture:

```bash
BASE_URL=https://api.example.com pytest -q
```

## Thresholds

```js
// load/config.js
export default {
  thresholds: {
    http_req_duration: ['p(95)<250'],
    http_req_failed: ['rate<0.01'],
  },
};
```

Thresholds are assertions, not charts. If they fail, the build fails.

## Testing

```bash
pytest -q
# 3 passed
```

CI runs the contract suite on every push; the load profile runs against a deployed target.

## Roadmap

- JSON Schemas shared with `devflow-api`, so a field change fails here instead of in production
- Protocol checks against `devflow-realtime` event frames
- Coverage gate with `pytest-cov`
- Load profiles for board and search endpoints

## Ownership

Both maintainers of [OwlGuild](https://github.com/OwlGuild) commit here.

| Area | Maintainer |
|---|---|
| Contract suites | shared |
| Load profiles and thresholds | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Protocol checks | [@AhmadGolbooee](https://github.com/AhmadGolbooee) |
| Triaging failures | shared |

## License

[MIT](LICENSE).
