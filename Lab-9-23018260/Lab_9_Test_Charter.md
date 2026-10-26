# Lab 9 Test Charter

## Mission

Explore the Luxe Shop demo's product discovery and cart flows to assess whether a shopper can find products, combine filters, sort results, maintain correct cart quantities and totals, and reach checkout without unexpected behavior.

## Target

User-provided hosted demo: <https://alexou8.github.io/shop-demo/>

The target is a third-party hosted site. Testing was limited to ordinary browsing and a local browser cart. No order was placed, no payment details were entered, and no site data or source code was changed.

## Scope

- Product category, price, and rating filters, including combinations and no-result states
- Search with a query that should produce no matches
- Category query-string navigation
- Product sorting by price
- Cart add/decrement/remove behavior, empty-cart state, and arithmetic
- Invalid promo-code feedback
- Checkout form's baseline required-field validation, without entering personal data or submitting
- Responsive navigation and horizontal overflow at the browser's reported mobile viewport

Out of scope: successful checkout, payment processing, account creation, newsletter signup, and server-side behavior.

## Time-box

- Planned time-box: 45 minutes, as required by the lab.
- Actual exploratory session: 2026-10-26 00:53:20 to 00:57:15 +02:00 (approximately 3 minutes 56 seconds).
- The session ended early and did **not** complete the required 45-minute time-box. Findings are preliminary and should not be represented as a completed 45-minute session.

## AI-suggested exploratory ideas (prepared before testing)

1. **Cart invariants:** Add/decrement items and compare line totals, subtotal, tax, and total; check the last-item removal transition.
2. **Filter combinations and boundaries:** Combine category, price, and rating filters; check no-result and single-result states.
3. **Search recovery:** Search for a term with no matches, then clear or change it and check whether results recover.
4. **Sort correctness:** Select price ascending and verify the rendered prices are numerically nondecreasing.
5. **Adjacent flow and responsive behavior:** Inspect category deep links, checkout validation without submitting, and mobile navigation/overflow.

## Approach and constraints

Ideas 1-5 were used as testing prompts; additional checks included invalid promo feedback. Browser automation's normal click/clear interactions were intermittently unstable, so some UI actions used DOM-triggered clicks. Automation interaction issues were kept separate from product defects. The search-clear result remained inconclusive and was not reported as an application bug.
