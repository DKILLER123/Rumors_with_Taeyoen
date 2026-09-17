const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const root=process.cwd(),cache=path.join(root,'.cache/reader-proof'),report=path.join(root,'reports/ch307_308_revision');
const {chromium:pw}=require(path.join(cache,'node_modules/playwright'));
process.env.LD_LIBRARY_PATH=path.join(cache,'libs/lib');
(async()=>{
 const {default:chromium}=await import(pathToFileURL(path.join(cache,'node_modules/@sparticuz/chromium/build/index.js')));
 const browser=await pw.launch({executablePath:await chromium.executablePath(),args:[...chromium.args.filter(a=>a!=='--single-process'),'--allow-file-access-from-files'],headless:true});
 const results=[];
 for(const chapter of [307,308])for(const width of [390,800]){
  const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  await page.goto(pathToFileURL(path.join(root,`work_epub/OEBPS/text/ch${chapter}.xhtml`)).href);await page.evaluate(()=>document.fonts.ready);
  const metrics=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,loadedFonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.src})),panels:[...document.querySelectorAll('.system-block,.phone-call,.dev-quest,.wardrobe-block')].map(e=>({class:e.className,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth})),plainParagraphs:document.querySelectorAll('.page-wrapper > p:not(.scene-break)').length}));
  await page.screenshot({path:path.join(report,`ch${chapter}-opening-${width}.png`)});
  if(chapter===307){await page.locator('.scene-break').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(report,`ch307-dialogue-${width}.png`)});}
  else {await page.locator('.dev-quest').screenshot({path:path.join(report,`ch308-quest-${width}.png`)});}
  results.push({chapter,width,errors,...metrics});await page.close();
 }
 fs.writeFileSync(path.join(report,'browser_proof.json'),JSON.stringify(results,null,2)+'\n');
 console.log(JSON.stringify(results.map(r=>({chapter:r.chapter,width:r.width,errors:r.errors,scrollWidth:r.scrollWidth,panels:r.panels.length,plainParagraphs:r.plainParagraphs})),null,2));
 await browser.close();if(results.some(r=>r.errors.length||r.scrollWidth>r.width||r.images.some(i=>!i.loaded)||r.panels.some(b=>b.scrollWidth>b.clientWidth+1)))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
