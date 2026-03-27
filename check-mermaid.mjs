import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

const errors = [];
page.on('console', msg => {
  if (msg.type() === 'error') {
    errors.push(msg.text());
  }
});

page.on('pageerror', error => {
  errors.push(`Page Error: ${error.message}`);
});

await page.goto('http://localhost:8080/linear-algebra-vectors-matrices/01-introduction.html');
await page.waitForTimeout(3000);

const mermaidInfo = await page.evaluate(() => {
  const mermaids = document.querySelectorAll('.mermaid');
  const results = [];
  mermaids.forEach((el, i) => {
    results.push({
      index: i,
      hasSvg: !!el.querySelector('svg'),
      text: el.textContent?.substring(0, 100)
    });
  });
  return results;
});

console.log('=== Mermaid Elements ===');
console.log(JSON.stringify(mermaidInfo, null, 2));

console.log('\n=== Console Errors ===');
errors.forEach(e => console.log(e));

await browser.close();
