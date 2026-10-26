# COMP 441 Lab 4: Requirements Traceability & Test Management

## Requirements basis and assumptions

The lab manual refers to a supplied requirements document, but none was
present in the repository. The eight functional requirements in
`requirements-traceability-matrix.csv` are therefore an explicit, testable
reconstruction from the current task-manager API in `app/tasks.py`. They are
not presented as requirements from a missing external specification.

The manual test cases in `test-cases.csv` have unique IDs and are implemented
as pytest tests in `test_lab4_rtm.py`. The matrix status reflects the latest
run of that suite.

## Requirements traceability matrix

See `requirements-traceability-matrix.csv` for the requested columns:
Requirement ID, Requirement Description, Test Case ID(s), Test Level, and
Status. Each functional requirement maps to at least one unit-level test.

## Mini test plan (IEEE 829-style): FR-05, pending-task retrieval

**Test item:** `app.tasks.get_pending_tasks`

**Scope:** Verify that the function returns every unfinished task in the
original order, including the first list item, and excludes tasks explicitly
marked done. For compatibility, a task without a `done` key is considered
pending.

**Features to be tested:** Inclusion of unfinished tasks, exclusion of
completed tasks, first-item handling, stable order, and the documented default
for a missing `done` key.

**Features not to be tested:** Persistence, task creation, completion side
effects, priority calculations, and CLI output; these are covered by other
requirements or are outside this unit's scope.

**Approach:** Run isolated pytest unit tests with in-memory task dictionaries.
Use a mixed list containing an unfinished first task, a completed task, and an
unfinished task without a `done` field. Compare the returned tasks and their
order to the expected result. The regression case for a pending first item is
`TC-08`.

**Entry criteria:** Python and pytest are available; the task-manager package
imports; the test data are local and isolated from persistent user data.

**Exit criteria:** All FR-05 cases pass, including the first-item regression
case; no test mutates the input list or writes outside pytest's temporary
directory.

## Defect log and lifecycle

`defect-lifecycle.csv` records two seeded defects in the repository's original
`HEAD:app/tasks.py`: the pending-task loop skipped the first task, and
averaging an empty task list raised `ZeroDivisionError`. The original
`tests/test_tasks.py` contains assertions that explicitly identify these
failures. The current workspace already contains corrections; this lab does
not change the application implementation.

The CSV records each defect through New → Triaged → Assigned → Fixed →
Verified → Closed. These are sample lifecycle records for the lab exercise,
not issues filed in an external tracker. Severity and priority are assigned
at triage. Verification is linked to regression cases `TC-08` and `TC-09`.
The lifecycle is illustrative; the available repository evidence does not
establish real historical assignment or closure events.

## AI-generated draft comparison

`ai-draft-traceability-matrix.csv` is an assistant-generated first draft
derived from the same reconstructed requirements above. It intentionally
starts with one representative test per requirement; it is a draft, not the
audited final matrix. The comparison below checks requirement coverage,
granularity, and correctness against the final, executable test set.

| Area | AI draft | Audited matrix and test set | Assessment |
|---|---|---|---|
| Requirement coverage | Maps all eight reconstructed requirements to one test each. | Maps all eight requirements to 15 uniquely identified tests. | No requirement omitted; final set covers additional conditions. |
| Loading tasks | Covers a missing file only. | Also verifies reading an existing JSON file (`TC-02`). | Draft misses the successful read path. |
| Saving tasks | Covers save/load round-trip. | Preserves round-trip coverage (`TC-03`). | Correct, but the draft does not separately exercise both loader branches. |
| Adding tasks | Covers default field values. | Also checks supplied priority/tags and that tags are copied (`TC-05`). | Draft omits custom-input and mutable-alias behavior. |
| Completing tasks | Covers a matching task. | Also checks an unknown ID returns `False` without changing tasks (`TC-07`). | Draft omits the negative path. |
| Pending tasks | Covers a mixed list. | Explicitly asserts the first unfinished item is retained, completed tasks are excluded, and a missing `done` field defaults to pending (`TC-08`). | Draft is underspecified around the known first-item boundary. |
| Average priority | Covers a nonempty list. | Covers both the arithmetic mean and empty-list result (`TC-09`–`TC-10`). | Draft misses the empty-list regression. |
| Title lookup | Covers a match. | Also covers no match and duplicate titles returning the first match (`TC-11`–`TC-13`). | Draft omits two useful edge cases. |
| Removal | Covers removing a matching task. | Also checks an unknown ID leaves the list unchanged (`TC-15`). | Draft omits the no-op case. |
| Hallucinated behavior | Adds no requirement beyond the source API. | Checks only behaviors supported by the current implementation and documented tests. | No incorrect requirement identified; requirements themselves remain inferred until confirmed against an authoritative specification. |

The final matrix is the better audit artifact because every row maps to
executable, uniquely named cases and its status comes from a recorded test
run. The missing source requirements document remains an audit limitation:
the matrix should be reconciled with the authoritative specification before
being treated as a contractual traceability record.

## Run and verify

From the repository root:

```powershell
python -m pytest Lab_4_Deliverables/test_lab4_rtm.py -q
```
