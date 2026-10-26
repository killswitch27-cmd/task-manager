import { defineConfig } from 'playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.js',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  timeout: 60_000,
  use: {
    baseURL: 'https://alexou8.github.io/shop-demo/',
    browserName: 'chromium',
    headless: true,
    trace: 'retain-on-failure',
  },
});
