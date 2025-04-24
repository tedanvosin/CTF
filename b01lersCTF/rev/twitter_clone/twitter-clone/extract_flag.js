// extract_flag_puppeteer.js
const puppeteer = require('puppeteer');
const path      = require('path');

(async () => {
  // 1) Launch headless Chrome
  const browser = await puppeteer.launch();
  const page    = await browser.newPage();

  // 2) Intercept console.log from the page so we can detect "Correct!"
  let lastLog = null;
  page.on('console', msg => {
    const text = msg.text();
    lastLog = text;
  });

  // 3) Load your local file:// index.html
  const indexPath = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(indexPath);

  // 4) Initialize the obfuscated VM
  await page.evaluate(() => setup());

  // 5) Brute‑force loop
  const alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789{}_';
  let flag       = '';
  const maxLen   = 40;  // adjust if your flag is longer/shorter

  while (!flag.endsWith('}')) {
    let found = false;
    for (const c of alphabet) {
      // pad to constant length so VM always does the same number of steps
      const trial = flag + c + 'A'.repeat(maxLen - flag.length - 1);
      lastLog = null;
      // call check(trial) in the page context
      await page.evaluate(f => check(f), trial);

      if (lastLog === 'Correct!') {
        process.stdout.write(c);
        flag += c;
        found = true;
        break;
      }
    }
    if (!found) {
      console.error('\n\n✘ Failed to extend flag—maybe increase maxLen or adjust alphabet.');
      process.exit(1);
    }
  }

  console.log('\n\n🎉 FLAG:', flag);
  await browser.close();
})();
