import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const projectRoot = process.cwd();
const workspaceRoot = path.resolve(projectRoot, '..');
const manifestPath = path.join(workspaceRoot, 'DAM_ANALYSIS_READY_2026', '11_manifest', 'sha256_checksums.txt');
const masterRoot = path.join(workspaceRoot, 'dam_output', 'master');

const expected = new Map();
for (const line of fs.readFileSync(manifestPath, 'utf8').split(/\r?\n/)) {
  const match = line.match(/^([a-f0-9]{64})\s+(.+)$/i);
  if (!match) continue;
  const relativePath = match[2].replace(/\\/g, '/');
  if (relativePath.startsWith('dam_output/master/')) expected.set(path.basename(relativePath), match[1].toLowerCase());
}

const files = fs.readdirSync(masterRoot).filter((name) => name.toLowerCase().endsWith('.csv')).sort();
const failures = [];
for (const fileName of files) {
  const actual = crypto.createHash('sha256').update(fs.readFileSync(path.join(masterRoot, fileName))).digest('hex');
  const wanted = expected.get(fileName);
  if (!wanted || wanted !== actual) failures.push({ fileName, expected: wanted ?? 'missing', actual });
}

for (const fileName of expected.keys()) {
  if (!files.includes(fileName)) failures.push({ fileName, expected: expected.get(fileName), actual: 'missing' });
}

if (files.length !== 12 || expected.size !== 12 || failures.length > 0) {
  console.error(JSON.stringify({ ok: false, fileCount: files.length, manifestCount: expected.size, failures }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ ok: true, fileCount: files.length, manifestCount: expected.size }, null, 2));