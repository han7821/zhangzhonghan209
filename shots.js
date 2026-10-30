/* shots.js —— 使用本机 Edge/Chrome 无头浏览器按移动设备模拟截图
   用法: node shots.js */
const puppeteer = require('puppeteer-core');
const path = require('path');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const CHROME = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe';
const BASE = 'http://127.0.0.1:8765';
const OUT = path.join(__dirname, 'docs');

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function shoot(browser, opts) {
  const { file, url, w, h, dsf = 2, mobile = true, fullPage = false, click = null } = opts;
  const page = await browser.newPage();
  await page.emulate({
    viewport: { width: w, height: h, deviceScaleFactor: dsf, isMobile: mobile, hasTouch: mobile },
    userAgent: 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36',
  });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  if (click) {
    await page.evaluate((sel) => document.querySelector(sel).click(), click);
    await sleep(400);
  }
  await sleep(300);
  await page.screenshot({ path: path.join(OUT, file), fullPage });
  await page.close();
  console.log('OK', file);
}

(async () => {
  const jobs = JSON.parse(process.argv[2] || '[]');
  const exe = process.argv[3] === 'chrome' ? CHROME : EDGE;
  const tag = process.argv[3] === 'chrome' ? '_chrome' : '';
  const browser = await puppeteer.launch({ executablePath: exe, headless: 'new' });
  for (const j of jobs) {
    j.file = j.file.replace('.png', tag + '.png');
    await shoot(browser, j);
  }
  await browser.close();
})();
