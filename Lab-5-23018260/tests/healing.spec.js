import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { expect, test } from 'playwright/test';
import { ShopPage } from '../pages/ShopPage.js';

test('label-based category locator recovers after the element id changes', async ({ page }) => {
  const fixtureDirectory = path.resolve(
    path.dirname(fileURLToPath(import.meta.url)),
    '..',
    'fixtures',
  );
  await page.goto(pathToFileURL(path.join(fixtureDirectory, 'category-before-drift.html')).href);
  await expect(page.locator('#category-filter')).toHaveCount(1);
  const shop = new ShopPage(page);
  await shop.selectCategory('Tech');
  await expect(page.getByLabel('Category')).toHaveValue('tech');

  await page.goto(pathToFileURL(path.join(fixtureDirectory, 'category-after-drift.html')).href);
  await expect(page.locator('#category-filter')).toHaveCount(0);
  await shop.selectCategory('Tech');
  await expect(page.getByLabel('Category')).toHaveValue('tech');
});
