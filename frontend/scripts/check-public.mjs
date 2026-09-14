import { access, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = await readFile(path.join(root, 'index.html'), 'utf8');
const scannableHtml = html.replace(/data:[^"']+/gi, 'data:embedded-asset');

const required = [
  '<symbol id="i-chat"',
  '<symbol id="i-home"',
  'seongnam-ai-characters.png',
  'seongnam-ai-icon.png',
  'new-chat-forum.svg',
  '예시 데이터',
  '실제 분석을 수행하지 않습니다.',
];

const forbidden = [
  /api[_-]?key/i,
  /password/i,
  /authorization/i,
  /bearer\s/i,
  /nvidia/i,
  /postgres/i,
  /jdbc/i,
  /fetch\s*\(/i,
  /xmlhttprequest/i,
  /websocket/i,
  /eventsource/i,
  /document\.modelContext/i,
  /registerTool/i,
  /AGENTS\.md/i,
  /Data Tools/i,
  /ML Tool/i,
];

const missing = required.filter((value) => !html.includes(value));
const exposed = forbidden.filter((pattern) => pattern.test(scannableHtml)).map(String);

await Promise.all([
  'public/new-chat-forum.svg',
  'public/seongnam-ai-characters.png',
  'public/seongnam-ai-icon.png',
].map((asset) => access(path.join(root, asset))));

if (missing.length || exposed.length) {
  if (missing.length) console.error(`필수 목업 요소 누락: ${missing.join(', ')}`);
  if (exposed.length) console.error(`공개 금지 패턴 발견: ${exposed.join(', ')}`);
  process.exitCode = 1;
} else {
  console.log('공개 데모 구조 및 안전 패턴 검사를 통과했습니다.');
}
