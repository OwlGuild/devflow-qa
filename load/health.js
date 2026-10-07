import config from './config.js';

export const options = {
  ...config,
  scenarios: {
    health_check: {
      executor: 'constant-arrival-rate',
      rate: 20,
      duration: '30s',
      timeUnit: '1s',
      preAllocatedVUs: 10,
      maxVUs: 50,
    },
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL;
  if (!baseUrl) {
    throw new Error('BASE_URL is required: k6 run -e BASE_URL=https://host load/health.js');
  }

  const res = http.get(`${baseUrl}/health/`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'latency < 250ms': (r) => r.timings.duration < 250,
  });
}
