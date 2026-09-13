// Optional browser-only proof; run from the repository root after installing
// playwright and @sparticuz/chromium in .cache/reader-proof. Extract the latter's
// bin/al2023.tar.br to .cache/reader-proof/libs for its shared libraries.
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const root=process.cwd();
const cache=path.join(root,'.cache/reader-proof');
const {chromium:playwright}=require(path.join(cache,'node_modules/playwright'));
process.env.LD_LIBRARY_PATH=path.join(cache,'libs/lib');
(async()=>{
 const {default:chromium}=await import(pathToFileURL(path.join(cache,'node_modules/@sparticuz/chromium/build/index.js')));
 const browser=await playwright.launch({executablePath:await chromium.executablePath(),args:[...chromium.args.filter(a=>a!=='--single-process'),'--allow-file-access-from-files'],headless:true});
 const results=[];
 for(const width of [390,800]){
  const page=await browser.newPage({viewport:{width,height:1000}});const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  await page.goto(pathToFileURL(path.join(root,'work_epub/OEBPS/text/ch304.xhtml')).href);
  await page.evaluate(()=>document.fonts.ready);
  const metrics=await page.evaluate(()=>({
   viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,
   titleFont:getComputedStyle(document.querySelector('.chapter-title')).fontFamily,
   dossierAlign:[...document.querySelectorAll('.dg-value')].map(e=>getComputedStyle(e).textAlign),
   loadedFonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),
   blocks:[...document.querySelectorAll('.page-wrapper > div')].map(e=>({class:e.className,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth})),
   images:[...document.images].map(i=>({src:i.src,loaded:i.complete&&i.naturalWidth>0}))
  }));
  await page.screenshot({path:path.join(cache,`ch304-title-${width}.png`)});
  for(const [name,selector,index] of [['acting','.acting-block',2],['performance','.performance-block',0],['lesson','.lesson-block',0],['whisper','.whisper-block',1]])
   await page.locator(selector).nth(index).screenshot({path:path.join(cache,`ch304-${name}-${width}.png`)});
  results.push({width,errors,...metrics});
 }
 fs.writeFileSync('reports/ch304/browser_proof.json',JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify(results.map(r=>({width:r.width,errors:r.errors,scrollWidth:r.scrollWidth,overflowing:r.blocks.filter(b=>b.scrollWidth>b.clientWidth+1)})),null,2));
 await browser.close();
 if(results.some(r=>r.errors.length||r.scrollWidth>r.width||r.blocks.some(b=>b.scrollWidth>b.clientWidth+1)))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
