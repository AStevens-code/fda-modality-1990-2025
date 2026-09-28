# Contributing

This is a published dataset with a DOI, not a software project, so "contributing" mostly
means **reporting errors**. That is actively wanted: the package documents its own weak
points in `docs/KNOWN_ISSUES.md`, and the withdrawals series in particular was curated by
hand against no authoritative registry.

## The evidence bar

A correction to the data needs a **citable source** - a Federal Register notice, an FDA
communication or approval letter, a ChEMBL or Drugs@FDA record, or a peer-reviewed
citation. This is not bureaucracy: every row in the published tables is traceable to a
source, and accepting an unsourced change would break that property for all downstream
users.

Corrections *without* a source are still worth filing as questions - just expect the
answer to be "I can't change it on this basis" rather than a new release.

## What is in and out of scope

**In scope:** missing or mis-dated withdrawals; modality misclassifications; substances
wrongly included in or excluded from the novel-active-substance universe; errors in the
documentation; broken reproducibility.

**Out of scope:** extending the series before 1990 or to non-US regulators; adding
generics, biosimilars, new formulations or new combinations (the universe is deliberately
novel active substances only - see `docs/METHODOLOGY_approvals.md`); redefining the seven
modality classes, which would make the published series non-comparable with itself.

## How corrections are released

Published versions are **never edited in place.** A correction produces a new release:

1. The fix is applied to the source tables and every downstream table is regenerated, not
   hand-patched.
2. The notebook is re-executed and all validation checks must pass.
3. `CHANGELOG.md` records the defect, its effect on the published numbers, and the check
   that surfaced it.
4. A new GitHub release is tagged, which Zenodo archives under a **new version DOI**. The
   concept DOI continues to resolve to the latest version, so existing citations keep
   working and readers can see what changed.

## Code

`notebooks/01_reproduce_figures.ipynb` must keep passing the reproducibility workflow -
CI executes it and fails the build if any validation check reports anything but PASS.

`src/pipeline_1990_2025.py` is a **frozen record of the code as executed**, not maintained
code. It is shipped so the provenance of the classifications is inspectable. Please do not
send patches "fixing" it; its job is to match what actually ran, including the five defects
that were later found and corrected in the published tables (see `docs/REPRODUCIBILITY.md`).
