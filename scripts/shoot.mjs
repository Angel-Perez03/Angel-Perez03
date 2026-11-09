// Screenshots of the live sites, used as frames on the profile.
// Run: node scripts/shoot.mjs  (needs playwright-core from ../portafolio and Edge)
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(here, "../../portafolio/package.json"));
const { chromium } = require("playwright-core");

const OUT = path.join(here, "../.preview/shots");
const TARGETS = [
  ["crea-home", "https://crea.virtual.uniandes.edu.co/"],
  ["crea-talleres", "https://crea.virtual.uniandes.edu.co/talleres"],
  ["crea-proyectos", "https://crea.virtual.uniandes.edu.co/proyectos"],
  ["crea-equipo", "https://crea.virtual.uniandes.edu.co/equipo"],
  ["beania", "https://unaiapordia.vercel.app/"],
  ["secrelogic-live", "https://secre-logic.vercel.app/"],
  ["creaspider-live", "https://creaspider.vercel.app/"],
  ["recrea-live", "https://recrea-pi.vercel.app/"],
];

const only = process.argv.slice(2);
const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
for (const [name, url] of TARGETS) {
  if (only.length && !only.includes(name)) continue;
  try {
    await page.goto(url, { waitUntil: "load", timeout: 30000 });
    await page.waitForTimeout(3500);
    await page.screenshot({ path: path.join(OUT, `${name}.png`), timeout: 15000 });
    console.log("ok", name);
  } catch (e) {
    console.log("fail", name, e.message.split("\n")[0]);
  }
}
await browser.close();
