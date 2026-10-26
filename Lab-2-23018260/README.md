The initial Pylint run first exposed a Windows application-control block on
the compiled `isort` dependency. Installing compatible pure-Python isort
5.13.2 allowed Pylint to run. This is an environment/tooling note, not a
finding in the application code.

# COMP 441 Lab 2: Static Analysis, Metrics & AI Code Review

## Scope and method

Pylint 4.1.3 analyzed `app` and `tests`; Radon 6.0.1 analyzed application
modules in `app`. A default Pylint configuration is included as `.pylintrc`.
The before report was captured before the changes in `changes.patch`; the
after report was captured afterward.

Pre-existing workspace edits in `app/tasks.py` and `app/storage.py` were
preserved and not modified for these labs. The before/after comparison isolates
the import-only changes listed in `changes.patch`.

## Results

- Before: Pylint reported 29 messages, including three unused-import warnings;
  score 8.57/10.
- After: Pylint reported 26 messages; the three unused-import warnings are
  absent; score 8.71/10.
- The three fixes remove unused `save_tasks` and `add_task` imports from
  `app/cli.py` and unused `pytest` from `tests/test_lab6_ai.py`. No runtime
  behavior is changed.
- `pylint-before.txt` and `pylint-after.txt` contain the captured reports.
- `radon-report.txt` contains the complexity and maintainability output.
  `complexity-top-five.csv` lists the five highest-complexity functions.
- `triage.csv` ranks ten representative original findings. The three
  highest-severity findings are the three unused imports (Pylint warning
  category W0611); they are fixed and verified absent from the after report.

Pylint's full-repository output still contains lower-severity conventions
(primarily missing docstrings in existing tests). These are not necessary for
the three selected fixes and were left unchanged.

## Complexity

Radon reported 13 functions, average cyclomatic complexity A (2.08). The five
highest-scoring functions are all in risk band A; the maximum complexity was
3. Every analyzed function was band A. Maintainability index was also band A
for the analyzed modules.

## AI-assisted review comparison

Two code-review snippets were evaluated:

1. `app/storage.py:17-22` (`days_until_due`): A date parsed at midnight is
   compared with the current time. Depending on time of day, a due-today date
   can yield `-1` and tomorrow can yield `0`, which conflicts with a
   calendar-day interpretation. Pylint did not flag this behavioral boundary.
2. `app/storage.py:25-28` (`build_query`): The function manually escapes
   apostrophes and concatenates SQL text. That addresses ordinary quoted
   string input for common SQL dialects, but bound parameters are preferable
   when a database execution layer exists. No SQL execution path is present,
   so this review does not claim a demonstrated injection vulnerability.

See `ai-review-comparison.csv`. Pylint caught mechanical quality issues;
semantic expectations, date-boundary behavior, and persistence/query design
require review against requirements and call-site context.

## Validation

The linter after-report confirms the three selected W0611 messages are
resolved. The app's existing tracked task tests and the Lab 4 suite passed
when run in the targeted combined check. The newly added Lab 3 tests include
10 expected failures for invalid-input assumptions not implemented by
`calculate_discount`; they are intentionally not counted as regressions
caused by these import-only edits. The repository-wide pytest run remains
blocked by duplicate test module names; details are in the Lab 1 report.
