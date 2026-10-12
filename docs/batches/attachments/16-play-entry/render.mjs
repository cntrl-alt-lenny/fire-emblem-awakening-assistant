// Evidence rendering with externally supplied runtime paths; no product dependency.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const directory=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(directory,'../../../..');
const {marked}=await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES,'marked/lib/marked.esm.js')));
const {chromium}=await import(pathToFileURL(path.join(process.env.FEA_NODE_MODULES,'playwright/index.mjs')));
const browser=await chromium.launch({headless:true,executablePath:process.env.FEA_CHROME});
try {
 for (const [source,stem] of [['docs/play-entry.md','reference'],['docs/batches/16-play-entry.md','summary']]) {
  const filename=path.join(root,source);
  const markdown=fs.readFileSync(filename,'utf8');
  let links=0;
  for(const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
   if(!fs.existsSync(path.resolve(path.dirname(filename),match[1].split('#')[0])))throw Error('Missing link '+match[1]);
   links++;
  }
  const prefix=path.relative(directory,path.dirname(filename))+'/';
  const body=marked.parse(markdown).replace(/href="(?![a-z]+:|#)([^"]+)"/gi,(_,href)=>'href="'+prefix+href+'"');
  const html='<!doctype html><html lang="en"><meta charset="utf-8"><title>Play entry</title><style>body{background:#eef2f5;color:#182330;font:17px/1.5 system-ui}article{max-width:900px;margin:24px auto;padding:30px;background:white}h1,h2{line-height:1.2}pre{padding:14px;background:#f3f6f8;white-space:pre-wrap}code{overflow-wrap:anywhere}a{color:#17649b}</style><article>'+body+'</article></html>';
  const artifact=path.join(directory,stem+'.html');fs.writeFileSync(artifact,html);
  const page=await browser.newPage({viewport:{width:1120,height:1000}});
  await page.goto(pathToFileURL(artifact).href);
  const size=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth,height:document.body.scrollHeight}));
  if(size.width>size.viewport)throw Error('Horizontal overflow');
  await page.screenshot({path:'/tmp/fea16-'+stem+'.png',fullPage:true});
  console.log(source+': '+links+' local links resolve; no horizontal overflow; rendered '+size.width+'x'+size.height);
  await page.close();
 }
}finally{await browser.close();}
