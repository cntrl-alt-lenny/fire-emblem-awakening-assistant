// Visual QA only; use supplied local runtime modules and installed Chrome.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL, fileURLToPath} from 'node:url';
const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../../../..');
const {marked} = await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES, 'marked/lib/marked.esm.js')));
const {chromium} = await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES, 'playwright/index.js')));
const source = path.join(root, 'docs/play-briefing.md');
const markdown = fs.readFileSync(source, 'utf8');
let count = 0;
for (const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
  const target = match[1];
  if (/^[a-z]+:/i.test(target) || target.startsWith('#')) continue;
  if (!fs.existsSync(path.resolve(path.dirname(source), target.split('#')[0]))) throw Error('Unresolved local link: ' + target);
  count++;
}
const body = marked.parse(markdown).replace(/href="(?![a-z]+:|#)([^"]+)"/gi, 'href="../../../$1"');
const html = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Current-map play briefing</title>' +
  '<style>body{margin:0;background:#eef2f5;color:#182330;font:17px/1.5 system-ui}article{max-width:1000px;margin:24px auto;padding:30px;background:white;border-radius:12px}h1,h2{line-height:1.2;color:#163f61}h2{margin-top:32px}pre{padding:14px;background:#f3f6f8;border-radius:6px;white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 ui-monospace}code{font-family:ui-monospace}a{color:#17649b}</style><article>' + body + '</article></html>';
const artifact = path.join(directory, 'reference.html');
fs.writeFileSync(artifact, html);
const browser = await chromium.launch({headless:true, executablePath:process.env.FEA_CHROME});
try {
  const page = await browser.newPage({viewport:{width:1120,height:1000},deviceScaleFactor:1});
  await page.goto(pathToFileURL(artifact).href);
  const dimensions = await page.evaluate(() => ({height:document.body.scrollHeight, width:document.documentElement.scrollWidth, viewport:innerWidth}));
  if (dimensions.width > dimensions.viewport) throw Error('Horizontal overflow');
  await page.screenshot({path:'/tmp/awakening-12-reference.png',fullPage:true});
  console.log('docs/play-briefing.md rendered; ' + count + ' local links resolve; horizontal overflow: 0; dimensions: ' + dimensions.width + 'x' + dimensions.height);
} finally {
  await browser.close();
}
