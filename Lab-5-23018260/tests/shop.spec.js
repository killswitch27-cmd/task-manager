import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { expect, test } from 'playwright/test';
import { ShopPage } from '../pages/ShopPage.js';

const dataDirectory = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'data');
const testCases = JSON.parse(
  await readFile(path.join(dataDirectory, 'test-cases.json'), 'utf8'),
);

for (const testCase of testCases) {
  test(testCase.name, async ({ page }) => {
    const shop = new ShopPage(page);
    await shop.open();

    if (testCase.action === 'search') {
      await shop.search(testCase.value);
    } else if (testCase.action === 'category') {
      await shop.selectCategory(testCase.value);
    } else if (testCase.action === 'price') {
      await shop.selectPriceRange(testCase.value);
    } else if (testCase.action === 'sort') {
      await shop.sortBy(testCase.value);
    } else if (testCase.action === 'cart') {
      await shop.productCard(testCase.value).getByRole('button', { name: 'Add to Cart' }).click();
      await expect(shop.page.getByLabel('Shopping cart').locator('.cart-badge')).toHaveText('1');
      await shop.page.getByLabel('Shopping cart').click();
      await expect(shop.page.getByText(testCase.value, { exact: true })).toBeVisible();
      return;
    } else {
      throw new Error(`Unknown test action: ${testCase.action}`);
    }

    if (testCase.expectedProducts) {
      await expect(shop.productCards).toHaveCount(testCase.expectedProducts.length);
      expect(await shop.visibleProductNames()).toEqual(testCase.expectedProducts);
    }

    if (testCase.expectedFirstProduct) {
      await expect(shop.productCards.first().getByRole('heading')).toHaveText(
        testCase.expectedFirstProduct,
      );
    }
  });
}
