import { WebSocket } from 'ws';

const url = process.env.REALTIME_URL;
if (!url) {
  console.error('REALTIME_URL is required');
  process.exit(1);
}

const ws = new WebSocket(url);
const timer = setTimeout(() => {
  console.error(`no greeting within 60s from ${url}`);
  process.exit(1);
}, 60000);

ws.on('message', (data) => {
  let msg;
  try {
    msg = JSON.parse(data.toString());
  } catch {
    console.error('non-json frame:', data.toString());
    process.exit(1);
  }
  if (msg.type !== 'connected') {
    console.error('unexpected first frame:', msg);
    process.exit(1);
  }
  console.log('connected:', JSON.stringify(msg));
  clearTimeout(timer);
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => {
  console.error('socket error:', err.message);
  process.exit(1);
});
