export default {
  thresholds: {
    http_req_duration: ['p(95)<250'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};
