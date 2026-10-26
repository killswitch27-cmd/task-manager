# COMP 441 Lab 8 Deliverables

This folder contains the Lab 8 visual-regression and accessibility results for
the user-provided Luxe Shop demo: <https://alexou8.github.io/shop-demo/>.

## Run the checks

```powershell
npm install
npx playwright install chromium
npm test
```

The Playwright harness scans the home, shop, about, and cart pages in light
mode, and the shop page in dark mode. It writes the before/after axe results
to `axe-before.json` and `axe-after.json`. It also captures desktop and mobile
shop screenshots and writes pixel-difference measurements to
`visual-diff-report.json`.

## Results

- Baseline: serious WCAG 2.1 AA contrast failures in light-mode product prices
  and dark-mode review counts.
- After local CSS overrides: zero axe violations across all five scan states.
- Deliberate visual change: increase the shop heading's top margin to 48px.
  Pixelmatch reports the desktop and mobile changed-pixel percentages in
  `visual-diff-report.json`.

The demo is hosted by a third party, so the CSS fixes are injected by the
Playwright test harness and are not deployed to or written into the live site.
`accessibility-fixes.css` contains those local overrides.
