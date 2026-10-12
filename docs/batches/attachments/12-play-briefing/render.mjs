// Visual QA only; use supplied local runtime modules and installed Chrome.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL, fileURLToPath} from 'node:url';
const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../../../..');
const {marked} = await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES, 'marked/lib/marked.esm.js')));
const imported = await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES, 'playwright/index.js')));
const {chromium} = imported.default || imported;
const browser = await chromium.launch({headless:true, executablePath:process.env.FEA_CHROME});
try {
  for (const [relative, stem] of [['docs/play-briefing.md','reference'], ['docs/batches/12-play-briefing.md','summary'], ['docs/batches/attachments/12-play-briefing/attempts.md','attempts']]) {
    const source = path.join(root, relative);
    const markdown = fs.readFileSync(source, 'utf8');
    let count = 0;
    for (const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
      const target = match[1];
      if (/^[a-z]+:/i.test(target) || target.startsWith('#')) continue;
      if (!fs.existsSync(path.resolve(path.dirname(source), target.split('#')[0]))) throw Error('Unresolved local link: ' + target);
      count++;
    }
    const prefix = path.relative(directory, path.dirname(source)) + '/';
    const body = marked.parse(markdown).replace(/href="(?![a-z]+:|#)([^"]+)"/gi, (_, href) => 'href="' + prefix + href + '"');
    const html = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Play briefing reference and evidence</title>' +
      '<style>body{margin:0;background:#eef2f5;color:#182330;font:17px/1.5 system-ui}article{max-width:1000px;margin:24px auto;padding:30px;background:white;border-radius:12px}h1,h2{line-height:1.2;color:#163f61}h2{margin-top:32px}pre{padding:14px;background:#f3f6f8;border-radius:6px;white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 ui-monospace,Menlo,monospace}code{font:14px/1.5 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}a{color:#17649b}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #ccd6dc;padding:8px;text-align:left}</style><article>' + body + '</article></html>';
    const artifact = path.join(directory, stem + '.html');
    fs.writeFileSync(artifact, html);
    const page = await browser.newPage({viewport:{width:1120,height:1000},deviceScaleFactor:1});
    await page.goto(pathToFileURL(artifact).href);
    const dimensions = await page.evaluate(() => ({height:document.body.scrollHeight, width:document.documentElement.scrollWidth, viewport:innerWidth}));
    if (dimensions.width > dimensions.viewport) throw Error('Horizontal overflow');
    await page.screenshot({path:'/tmp/awakening-12-' + stem + '.png',fullPage:true});
    console.log(relative + ' rendered; ' + count + ' local links resolve; horizontal overflow: 0; dimensions: ' + dimensions.width + 'x' + dimensions.height);
    await page.close();
  }
} finally {
  await browser.close();
}
