import options from './config.js';

export const options = {
  ...options,
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
  const res = http.get(${__ENV.BASE_URL}/health/);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'latency < 200ms': (r) => r.timings.duration < 200,
  });
}
