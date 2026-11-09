// Screenshots every page in .preview/render into assets/ at 2x.
// Run after compose.py: node scripts/render.mjs
import { createRequire } from "node:module";
import { readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(here, "../../portafolio/package.json"));
const { chromium } = require("playwright-core");

const RENDER = path.join(here, "../.preview/render");
const OUT = path.join(here, "../assets");

const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1000, height: 800 }, deviceScaleFactor: 2 });
for (const file of readdirSync(RENDER).filter((f) => f.endsWith(".html"))) {
  await page.goto(pathToFileURL(path.join(RENDER, file)).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const font = await page.evaluate(() => document.fonts.check("500 20px 'Hanken Grotesk'"));
  const out = path.join(OUT, file.replace(".html", ".jpg"));
  await page.locator(".frame").screenshot({ path: out, type: "jpeg", quality: 88 });
  console.log(font ? "ok  " : "NOFONT", path.basename(out));
}
await browser.close();
