# COMP 441 Lab 5: Test Automation Framework & Self-Healing Locators

This deliverable uses Playwright's test runner and a Page Object Model against
the Luxe Shop demo already used in this repository's Lab 8 work. Test inputs
and expected results are stored in `data/test-cases.json`; the suite contains
five data-driven UI tests.

## Run the suite

From this directory:

```powershell
npm install
npx playwright install chromium
npm test
```

The live demo must be reachable. Tests run serially to avoid concurrent
interference with its shared backend.

## Verification

The suite passed against the live demo: five functional UI cases and one local
locator-drift recovery case (6 passed).

## Page Object and test data

- `pages/ShopPage.js` contains shop navigation, filters, search, and product
  card access.
- `tests/shop.spec.js` runs the five scenarios loaded from the JSON data file.
- `tests/healing.spec.js` checks the intentional category-filter id change in
  local fixtures. It verifies that the original id locator fails after drift
  and that the Page Object's accessible-label locator still selects the
  expected category.

## Drift result and limitation

The local drift demonstration has one affected locator: the original id
selector fails after the change, while the accessible-label fallback succeeds
(1/1 recovery). The result is recorded in `healing-report.json`. This is a
small, deterministic Playwright fallback demonstration; it is **not** a
Healenium run, and no Healenium dashboard evidence is claimed. Docker was not
available in the environment, and the third-party demo cannot be modified to
introduce DOM drift. To complete the Healenium-specific portion, run a
Selenium/Healenium setup against an application whose DOM you control, then
record its proxy and dashboard results separately.
