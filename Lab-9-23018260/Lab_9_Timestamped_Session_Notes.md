# Lab 9 Timestamped Session Notes

Target: <https://alexou8.github.io/shop-demo/>  
Date: 2026-10-26  
Timezone: local time, UTC+02:00 (browser timestamps were UTC and converted by adding two hours)  
Planned time-box: 45 minutes  
Actual session: 00:53:20–00:57:15 +02:00 (about 3:56; incomplete)

**Timestamp limitation:** The browser/session start time and later browser action timestamps were available, but the earlier exploratory actions were not individually timestamped when performed. Those first observations are grouped into the bounded interval below instead of assigning them invented exact times.

| Time (+02:00) | Source | Area / action | Observation, question, or idea |
|---|---|---|---|
| 00:53:20–00:55:50 (interval; individual event times not retained) | AI-suggested | Price and category filters | “Under $50” returned one product at $45. Combining Home with “Under $50” returned zero products. These outcomes were observed; filter reset/recovery was not fully verified. |
| 00:53:20–00:55:50 (interval; individual event times not retained) | AI-suggested | Rating filter | “4.5+” showed three products. The observed review-count labels were 156, 201, and 112. |
| 00:53:20–00:55:50 (interval; individual event times not retained) | AI-suggested | Search no-result case | Query `zzzxqv-no-match` produced zero products. Clearing the search through browser automation did not reliably change the input; this may be an automation interaction problem. **Question left open:** Does clearing the search through ordinary user input restore the filtered results? Not counted as a confirmed defect. |
| 00:53:20–00:55:50 (interval; individual event times not retained) | AI-suggested | Cart arithmetic | Added the Minimalist Leather Tote until the cart showed quantity 3. At $189 each, subtotal was $567.00, tax at 8% was $45.36, and total was $612.36. No checkout was submitted. |
| 00:55:51 | AI-suggested | Cart decrement | Decremented the tote from quantity 3 to 2. Cart showed quantity 2, subtotal $378.00, tax $30.24, and total $408.24; arithmetic was consistent. |
| 00:55:51 | Self-found | Promo code | Applied `NOPE123`; the page displayed “Invalid promo code” and kept the total at $408.24. No unexpected behavior observed. |
| 00:55:52–00:57:03 (interval; exact event time not retained) | AI-suggested | Category deep link | Opened `shop.html?category=Accessories`. The Accessories filter was selected and three products were shown. The URL parameter and visible state agreed. |
| 00:57:04 | AI-suggested | Price sort | Price ascending produced the sequence $45, $52, $58, $68, $98, $129, $135, $145, $149, $168, $179, $189. The numeric ordering invariant passed. |
| 00:57:14 | Self-found | Cart remove / empty state | Removing the remaining item prompted for confirmation. After confirmation, the cart was empty and displayed “Your cart is empty.” The test-created cart was cleared. |
| 00:57:15 | AI-suggested | Responsive navigation | At the browser-reported CSS viewport width of 312 px, navigation collapsed to the menu button and document width was 300 px; no horizontal overflow was reported. The requested emulated width did not match the reported effective width, so this is a limited observation. |
| 00:57:15 | Self-found | Checkout form | Checkout showed 12 required fields; the untouched form failed native validity checks. No personal/payment information was entered and no order was submitted. |
| 00:57:15 | Self-found | Cleanup | Removed only the test-created `cart` localStorage key; confirmed it was absent afterward. |

## Defects, questions, and follow-up

- **Confirmed defects:** None.
- **Unresolved question:** Search clear/recovery needs a manual or stable end-to-end retest; current automation interactions were unreliable.
- **Tooling note:** A browser automation navigation helper initially raised a JavaScript `URL is not defined` error. This was a test-script error, not an application failure.
- **Safety boundary:** Checkout was inspected read-only; no order, payment, newsletter subscription, or personal-data submission occurred.
