# COMP 441 Lab 1: Environment Setup & Manual Defect Hunting

## Environment and sample application

The project is Python-based. The verified local versions are recorded in
`toolchain-capture.txt`. Running `python -m app.cli` succeeded and printed an
empty-task summary.

The default `pytest` shell command was not on `PATH`; invoking it as
`python -m pytest` works. The full repository test attempt stopped during
collection because duplicate Lab 6 test module names are present under
`mutants/`, `tests/`, and `Lab_6_Deliverables/`. Pytest reported 36 tests
collected and four import-file-mismatch collection errors; it did not execute
that full suite. See `existing-test-results.txt`.

## Manual defect log

`manual-defect-log.csv` records suspected defects from source review, before
using the Lab 2 linter. Severity is a preliminary assessment. Some entries
were later corroborated by test cases or direct behavior; others remain
suspicions requiring an authoritative specification or malformed-data
scenario. The log intentionally retains this distinction.

## AI assistant and reflection

The coding question asked was: “What does `load_tasks` return when no
`tasks.json` exists?” The answer is an empty list: the function checks
`os.path.exists` and falls through to `return []`.

The assistant used for this work is Copilot SDK in VS Code. No separately
configured Claude/ChatGPT free-tier account or local Ollama installation
could be verified from this environment, so that prerequisite is not claimed
as complete.

Linting is likely to expose unused imports and some other mechanically
checkable issues. Tests readily catch the discount and date-boundary behaviors
once expected behavior is specified. Issues involving unclear requirements,
such as whether missing task fields should be tolerated, need careful review
and product clarification.
