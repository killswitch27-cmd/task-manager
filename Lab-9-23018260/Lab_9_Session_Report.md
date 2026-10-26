# Lab 9 Session Report: Exploratory Testing with an AI Co-Pilot

## Summary

I explored product discovery, cart behavior, and adjacent checkout/navigation states on the user-provided Luxe Shop demo. The planned charter was 45 minutes, but the recorded session lasted approximately 3 minutes 56 seconds (2026-10-26 00:53:20–00:57:15 +02:00). This is a preliminary, incomplete session and does not satisfy the lab's full 45-minute time-box.

The session confirmed the observed price-filter results, category deep-link state, ascending price order, cart quantity arithmetic, invalid-promo feedback, empty-cart transition, and basic untouched-checkout validation. No confirmed application defects were found. One search recovery question remains open because browser automation could not reliably clear the search field.

## Charter and coverage

The mission was to check whether a shopper can find products, combine filters, sort the catalog, maintain correct cart quantities/totals, and reach checkout without unexpected behavior. Areas exercised:

- Price/category/rating filtering and a no-result search
- Accessories category query-string navigation
- Ascending price sort
- Cart quantity decrement, total arithmetic, item removal, and empty state
- Invalid promo code
- Checkout required-field baseline validation without submitting
- Responsive navigation and horizontal overflow at the browser-reported viewport

The hosted site was not modified. No personal information or payment data was entered, and no order or newsletter signup was submitted. The test-created cart was cleared at the end.

## Results

| Check | Result |
|---|---|
| Under $50 filter | One product at $45 |
| Home + Under $50 | Zero products |
| Rating 4.5+ | Three products; review counts 156, 201, 112 |
| Search `zzzxqv-no-match` | Zero products |
| Accessories deep link | Filter selected; three products |
| Price ascending | $45, $52, $58, $68, $98, $129, $135, $145, $149, $168, $179, $189 |
| Tote quantity 3 | Subtotal $567.00; tax $45.36; total $612.36 |
| Tote quantity 2 | Subtotal $378.00; tax $30.24; total $408.24 |
| Invalid promo `NOPE123` | “Invalid promo code”; total unchanged |
| Remove final item | Confirmation shown; empty-cart message displayed |
| Checkout baseline | 12 required fields; untouched form invalid; no submission |
| Responsive check | Browser reported 312px viewport and 300px document width; no horizontal overflow |

## Bug list and AI-vs-manual source breakdown

| ID | Severity | Finding | Source |
|---|---|---|---|
| — | — | No confirmed defects found during this preliminary session. | — |

Confirmed bugs: **0**. The required source percentages are **not applicable** because there were no confirmed bugs to classify (AI-suggested: 0 bugs; self-found: 0 bugs). This is not a 0%/100% split.

The search-clear behavior is an unresolved question, not a confirmed defect: automation did not reliably clear the field, and the result needs a stable manual retest. Browser click/clear instability and a `URL is not defined` error in a test helper were treated as tooling issues rather than product defects.

## Reflection

AI-suggested ideas gave the session a repeatable structure around filter combinations, numeric sorting, cart invariants, recovery states, and checkout boundaries. They overlapped with ordinary tester instincts, but helped make arithmetic and ordering explicit pass/fail checks. No bug was confirmed, so this short session cannot establish that AI uncovered defects that would otherwise have been missed. The search-recovery question is the most useful follow-up and should be retested with direct user input during a full-length session.

## Limitations and completion status

- The lab requires a 45-minute session; only about 3:56 was completed. This report does not claim compliance with the full duration.
- Early observations were not individually timestamped when first made; the notes preserve their order and use honest time intervals rather than invented exact times.
- Browser automation interaction instability limited conclusions about clearing search and the exact responsive viewport.
- The hosted demo is outside this repository and was not modified.

## Deliverables

- [Test charter](./Lab_9_Test_Charter.md)
- [Timestamped session notes](./Lab_9_Timestamped_Session_Notes.md)
- This session report
