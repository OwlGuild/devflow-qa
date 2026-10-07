# devflow-qa

Contract, load and coverage checks across the DevFlow stack. This repository exists because
"it works locally" is not a claim — it is a hypothesis.

[![k6](https://img.shields.io/badge/load-k6-d01010.svg)](https://k6.io/)
[![pytest](https://img.shields.io/badge/tests-pytest-555555.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-enforced-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Why this exists

Four repositories ship one product. Individually each can pass its tests while the whole thing
still breaks. This repo tests the seams: the API contract, the realtime protocol, and the
behaviour under load.

## What runs

| Suite | Tool | What it proves |
|---|---|---|
| Contract | pytest + schemas | the API responses still match what `devflow-web` expects |
| Protocol | pytest | `devflow-realtime` events match the declared types |
| Load | k6 | p95 latency and error rate stay inside budget at target concurrency |
| Coverage | pytest-cov | project-wide coverage never drops below the enforced floor |

## Quickstart

```bash
git clone https://github.com/OwlGuild/devflow-qa.git
cd devflow-qa
cp .env.example .env
docker compose up -d        # start the stack under test
pip install -r requirements.txt
pytest                      # contract and protocol suites
k6 run load/smoke.js        # smoke load profile
```

## Thresholds

```js
// load/baseline.js
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<400'],
    http_req_failed: ['rate<0.01'],
  },
};
```

Thresholds are assertions, not charts. If they fail, the build fails.

## How contract tests stay honest

Responses are checked against JSON Schemas that both the API and this repository read. When the
API changes a field, either the schema is updated deliberately or the test fails — there is no
third option where the client silently breaks in production.

## Ownership

Both maintainers of [OwlGuild](https://github.com/OwlGuild) commit here.

| Area | Maintainer |
|---|---|
| Contract suites and schemas | shared |
| Load profiles and thresholds | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Protocol checks | [@AhmadGolbooee](https://github.com/AhmadGolbooee) |
| Coverage gate in CI | shared |
| Triaging failures | shared |

## License

[MIT](LICENSE).