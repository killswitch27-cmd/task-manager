import { expect } from 'playwright/test';

export class ShopPage {
  constructor(page) {
    this.page = page;
    this.productCards = page.locator('.product-card');
  }

  async open() {
    await this.page.goto('shop.html', { waitUntil: 'networkidle' });
    await expect(this.productCards.first()).toBeVisible();
  }

  async selectCategory(category) {
    const filter = this.page.getByLabel('Category', { exact: true });
    await expect(filter).toHaveCount(1);
    await expect(filter.locator('option').first()).toHaveText('All Categories');
    await filter.selectOption({ label: category });
  }

  async search(query) {
    await this.page.getByRole('searchbox', { name: 'Search products' }).fill(query);
  }

  async selectPriceRange(priceRange) {
    await this.page.locator('#price-filter').selectOption({ label: priceRange });
  }

  async sortBy(sortOrder) {
    await this.page.locator('#sort-select').selectOption({ label: sortOrder });
  }

  productCard(productName) {
    return this.productCards.filter({
      has: this.page.getByRole('heading', { name: productName, exact: true }),
    });
  }

  async visibleProductNames() {
    return this.productCards.locator('.product-name').allTextContents();
  }
}
