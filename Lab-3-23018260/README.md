# COMP 441 Lab 3: Dynamic Analysis & Test Design

## Target and specification basis

The target is `app.tasks.calculate_discount`. The sample repository contains
no separate function specification, so this exercise uses the function's
docstring and an explicitly stated, testable contract: a premium user receives
20% off; a regular user pays the original price. To make equivalence classes
and invalid-input boundaries testable, the following additional assumptions
are declared rather than presented as supplied requirements:

- `price` is a finite built-in `int` or `float`, not a `bool`, and is
  nonnegative.
- `is_premium` is exactly `True` or `False`, not another truthy or falsy value.
- No maximum price or currency rounding rule is specified. The expected
  result is the mathematical multiplier without rounding.

Confirm these assumptions against an authoritative function specification
before treating invalid-input failures as contractual bugs.

## Equivalence partitions and boundaries

See `equivalence-partitions.csv` for valid and invalid classes for both
inputs. `boundary-values.csv` covers the price lower boundary at zero, a
negative just-outside value, a small positive just-inside value, finite-number
edges, and the categorical/type boundary of the boolean flag.

## Executable tests and observed defects

`test-cases.csv` contains 18 cases and their actual outcomes against the
current implementation. Run the focused suite from the repository root:

```powershell
python -m pytest Lab_3_Deliverables\test_lab3_discount.py -q
```

Observed result: **8 passed, 10 failed**. The eight valid cases pass and
confirm the 20% premium calculation, regular-price pass-through, zero price,
small positive values, and lack of implicit cent-rounding. The ten invalid
input cases expose missing validation:

| Finding | Cases | Observation |
|---|---|---|
| Negative prices are accepted | TC-09 | Returns a negative discounted amount instead of raising `ValueError`. |
| Non-finite prices are accepted | TC-10–TC-12 | NaN and infinities propagate into the result instead of raising `ValueError`. |
| Invalid price types are accepted or propagated | TC-13–TC-14 | A regular string is returned unchanged and a boolean is treated as a price. |
| Non-boolean flags are accepted by truthiness | TC-15–TC-18 | Integers, `None`, and strings select a discount branch instead of raising `TypeError`. |

These are failures relative to the explicit assumptions above; the absent
authoritative specification means the invalid-input expectations still need
confirmation. The application code was not changed for this test-design lab.

## AI-generated comparison and reflection

`ai-generated-cases.csv` records a separate AI-style draft against the same
declared contract, with overlaps, omissions, and incorrect suggestions
flagged. Of the three manually selected price lower-bound values (−0.01,
0, and +0.01), the draft reproduced all three: **3/3 (100%)**. It also
reproduced important invalid types and non-finite values.

The draft additionally suggested a $50 eligibility threshold and mandatory
two-decimal rounding. Neither follows from the function's docstring or this
exercise's stated contract, and current code supplies no evidence for either.
They are marked as hallucinated assumptions, not included as expected
behavior. The invalid-input suite is deliberately broader than the visible
implementation so that missing input checks are measurable.

The manual requires attempting the repository-wide test suite too. In this
workspace, `pytest --collect-only -q` encountered four pre-existing import
file mismatch errors caused by duplicate Lab 6 test modules under `mutants/`,
`tests/`, and `Lab_6_Deliverables/`. Use the focused command above to run the
Lab 3 cases independently.
