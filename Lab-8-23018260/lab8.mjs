import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import axeCore from 'axe-core';
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';

const directory = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://alexou8.github.io/shop-demo/';
const pages = ['index.html', 'shop.html', 'about.html', 'cart.html'];
const wcagTags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];
const visualScenarios = [
  { name: 'desktop', width: 1280, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
];
const fixes = await readFile(path.join(directory, 'accessibility-fixes.css'), 'utf8');
const visualChange = await readFile(path.join(directory, 'visual-regression-change.css'), 'utf8');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await context.newPage();

async function scanCurrentPage(theme, applyFixes) {
  if (applyFixes) {
    await page.addStyleTag({ content: fixes });
  }

  const result = await new AxeBuilder({ page }).withTags(wcagTags).analyze();
  return {
    url: page.url(),
    title: await page.title(),
    theme,
    passes: result.passes.length,
    incomplete: result.incomplete.length,
    violations: result.violations,
  };
}

async function scanAllPages(applyFixes) {
  const results = [];
  await page.addInitScript(() => localStorage.setItem('darkMode', 'false'));

  for (const route of pages) {
    await page.goto(new URL(route, baseUrl).href, { waitUntil: 'networkidle' });
    results.push(await scanCurrentPage('light', applyFixes));
  }

  await page.setViewportSize({ width: 1024, height: 720 });
  await page.goto(new URL('shop.html', baseUrl).href, { waitUntil: 'networkidle' });
  await page.getByRole('button', { name: 'Toggle dark mode' }).click();
  await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
  results.push(await scanCurrentPage('dark', applyFixes));
  return results;
}

try {
  const before = await scanAllPages(false);
  const after = await scanAllPages(true);
  await writeFile(path.join(directory, 'axe-before.json'), `${JSON.stringify({
    tool: 'axe-core via @axe-core/playwright',
    version: axeCore.version,
    tags: wcagTags,
    results: before,
  }, null, 2)}\n`);
  await writeFile(path.join(directory, 'axe-after.json'), `${JSON.stringify({
    tool: 'axe-core via @axe-core/playwright',
    version: axeCore.version,
    tags: wcagTags,
    results: after,
  }, null, 2)}\n`);

  const visualResults = [];
  for (const scenario of visualScenarios) {
    await page.setViewportSize({ width: scenario.width, height: scenario.height });
    await page.goto(new URL('shop.html', baseUrl).href, { waitUntil: 'networkidle' });
    const baselinePath = path.join(directory, `visual-${scenario.name}-baseline.png`);
    const changedPath = path.join(directory, `visual-${scenario.name}-change.png`);
    const diffPath = path.join(directory, `visual-${scenario.name}-diff.png`);
    await page.screenshot({ path: baselinePath });
    await page.addStyleTag({ content: visualChange });
    await page.screenshot({ path: changedPath });

    const baseline = PNG.sync.read(await readFile(baselinePath));
    const changed = PNG.sync.read(await readFile(changedPath));
    if (baseline.width !== changed.width || baseline.height !== changed.height) {
      throw new Error(`Visual screenshots must have matching dimensions for ${scenario.name}.`);
    }
    const diff = new PNG({ width: baseline.width, height: baseline.height });
    const changedPixels = pixelmatch(
      baseline.data,
      changed.data,
      diff.data,
      baseline.width,
      baseline.height,
      { threshold: 0.1 },
    );
    await writeFile(diffPath, PNG.sync.write(diff));
    visualResults.push({
      name: scenario.name,
      viewport: { width: scenario.width, height: scenario.height },
      changedPixels,
      totalPixels: baseline.width * baseline.height,
      changedPercent: Number((changedPixels * 100 / (baseline.width * baseline.height)).toFixed(4)),
    });
  }
  await writeFile(path.join(directory, 'visual-diff-report.json'), `${JSON.stringify({
    route: new URL('shop.html', baseUrl).href,
    change: 'main h1 margin-top changed to 48px',
    threshold: 0.1,
    scenarios: visualResults,
  }, null, 2)}\n`);

  const summaries = { before, after };
  console.log(JSON.stringify(Object.entries(summaries).map(([name, group]) => ({
    name,
    results: group.map((result) => ({
      url: result.url,
      theme: result.theme,
      passes: result.passes,
      violations: result.violations.length,
      nodes: result.violations.reduce((total, violation) => total + violation.nodes.length, 0),
    })),
  })), null, 2));
} finally {
  await browser.close();
}
