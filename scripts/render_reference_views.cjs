// Canonical Mermaid sources -> transparent SVG/PNG + light-surface inspection PNG.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const toolsRoot = process.argv[2];
if (!toolsRoot) throw new Error('Supply temporary Mermaid installation directory');
const renderConfig = process.env.DME_MERMAID_CONFIG;
if (!renderConfig || !path.isAbsolute(renderConfig) || !fs.existsSync(renderConfig)) {
  throw new Error('Set DME_MERMAID_CONFIG to the approved external diagram skill mermaid-config.json');
}
const puppeteer = require(path.join(toolsRoot, 'node_modules', 'puppeteer'));
const cli = path.join(toolsRoot, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');
const executablePath = process.env.PULSE_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const browserConfig = path.join(root,'outputs/reference-v0.4/puppeteer.json');
fs.mkdirSync(path.dirname(browserConfig), {recursive:true});
fs.writeFileSync(browserConfig,JSON.stringify({executablePath,headless:true}));
const palette = [
  ['source','Blue','Sources','#EAF3F8','#356079'], ['data','Teal','Data foundation','#E5F4F2','#32746E'],
  ['model','Indigo','Analytics','#EDF0FA','#42558B'], ['policy','Gold','Policy','#F8F2E4','#876A2D'],
  ['human','Green','Human authority','#EFF6EB','#4C713E'], ['evidence','Purple','Evidence','#F3F0F8','#6E5B85'],
  ['security','Rose','Security','#FBEFED','#9B534C']
];
const views = JSON.parse(fs.readFileSync(path.join(root,'docs/diagrams/view_metadata.json'),'utf8')).filter(v=>/^1[1-7]_/.test(v.name) && (!process.argv[3] || v.name===process.argv[3]));
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
(async()=>{
  const browser = await puppeteer.launch({headless:true,executablePath});
  try {
    for (const view of views) {
      const base = path.join(root,'docs/diagrams',view.name);
      execFileSync(process.execPath,[cli,'-i',base+'.mmd','-o',base+'.svg','-c',renderConfig,'-p',browserConfig,'-b','transparent'],{stdio:'pipe',windowsHide:true});
      let svg = fs.readFileSync(base+'.svg','utf8');
      const svgId = svg.match(/<svg[^>]*\bid="([^"]+)"/)[1];
      const bounds = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
      const source = fs.readFileSync(base+'.mmd','utf8');
      const used = palette.filter(([role])=>new RegExp('^class .+ '+role+'$','m').test(source));
      const legend = used.map(([role,name,meaning,fill,stroke],i)=>{
        const x = 30 + (i%3)*325, y=1170+Math.floor(i/3)*34;
        return `<rect x="${x}" y="${y-15}" width="16" height="16" fill="${fill}" stroke="${stroke}"/><text x="${x+24}" y="${y}" font-size="16">${name}: ${meaning}</text>`;
      }).join('');
      const scale = Math.min(940/bounds[2],1010/bounds[3]);
      const tx = (1000-bounds[2]*scale)/2 - bounds[0]*scale;
      const ty = 125-bounds[1]*scale;
      const body = svg.replace(/^<svg[^>]*>/,'').replace(/<\/svg>\s*$/,'');
      svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1294" viewBox="0 0 1000 1294" style="background:transparent;font-family:Arial,sans-serif;color:#111111"><title>${escape(view.title)}</title><g fill="#111111"><text x="30" y="38" font-size="27" font-weight="bold">${escape(view.title)}</text><text x="30" y="70" font-size="16">${escape(view.purpose)}</text><text x="30" y="99" font-size="16">${escape(view.status)}</text></g><g id="${svgId}" transform="translate(${tx},${ty}) scale(${scale})">${body}</g><g fill="#111111">${legend}<text x="30" y="1270" font-size="15">${escape(view.footer || 'PULSE reference | No site validation')}</text></g></svg>`;
      fs.writeFileSync(base+'.svg',svg);
      const page = await browser.newPage();
      await page.setViewport({width:1000,height:1294,deviceScaleFactor:1});
      await page.setContent(`<html><style>html,body{margin:0;background:transparent}</style>${svg}</html>`);
      await page.screenshot({path:base+'.png',omitBackground:true});
      await page.addStyleTag({content:'html,body{background:white}'});
      await page.screenshot({path:path.join(root,'outputs/reference-v0.4',view.name+'-inspection.png')});
      await page.close();
      console.log(view.name);
    }
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
