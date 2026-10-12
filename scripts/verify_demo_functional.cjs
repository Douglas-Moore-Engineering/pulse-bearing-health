// Offline functional check, not a browser rendering or accessibility audit.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const html = fs.readFileSync('customer/benchmark-demo.html', 'utf8');
const elements = {};
function element() { return {textContent:'',innerHTML:'',children:[],value:'B04',
 addEventListener(name, fn){this[name]=fn;},append(child){this.children.push(child);},
 replaceChildren(...children){this.children=children;}}; }
const document = {getElementById(id){return elements[id] ||= element();},createElement:element};
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length,1);
const context = vm.createContext({document});
vm.runInContext(scripts[0][1],context,{timeout:5000});
const runs=[];
for(const [run, raw] of [['B04',3],['B12',26],['B17',9]]) {
 elements.run.value=run;elements.run.change();
 assert.equal(Number(elements.raw.textContent),raw);
 assert.equal(Number(elements.stable.textContent),1);
 assert.equal(elements.queue.children.length,1);
 assert.ok(elements.chart.innerHTML.includes('<path'));
 assert.ok(elements.first.textContent.includes('yes'));
 runs.push({run,original_episodes:raw,grouped_episodes:1,queue_rows:1});
}
const report={result:'PASS',scope:'Node VM DOM-stub functional check; not visual/browser validation',
 observed_at:new Date().toISOString(),html_sha256:crypto.createHash('sha256').update(html).digest('hex'),runs};
fs.writeFileSync('governance/evidence/phase10-demo-functional.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
