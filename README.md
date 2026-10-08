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
| Load | k6 | p95 latency, error rate and check rate stay inside budget |
| Live smoke | GitHub Actions | the four deployed services, the WebSocket handshake and the landing page still answer |

The contract suite runs against the deployed `devflow-api` in CI — with retries, so a
cold-starting instance is waited out rather than failed. Without `BASE_URL` it boots its own
fixture server, so it stays green locally before any service is deployed. Point it at any
other deployment with `BASE_URL` to run the same assertions elsewhere. The live smoke matrix
runs on demand and daily against the Render URLs.

## Quickstart

```bash
git clone https://github.com/OwlGuild/devflow-qa.git
cd devflow-qa
pip install -r requirements.txt
pytest -q            # contract suite against the fixture server
k6 run -e BASE_URL=http://localhost:8000 load/health.js   # load profile
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
    checks: ['rate>0.99'],
  },
};
```

Thresholds are assertions, not charts: when a run breaches one, k6 exits non-zero, so a
`latency < 250ms` check that stops passing cannot come back green. CI bundles and inspects
the scripts on every push — it does not run the profile — so a broken script fails the build
before anyone puts load on a service.

## Testing

```bash
pytest -q
# 3 passed
```

CI runs the contract suite on every push and bundles the k6 scripts, so a broken import fails
here instead of during a load run. Running the profile itself is manual — k6 is an external
tool — and targets whatever you pass:

```bash
k6 run -e BASE_URL=https://devflow-api-jtmi.onrender.com load/health.js
```

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
