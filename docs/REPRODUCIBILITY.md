# Reproducibility

This analysis has **three tiers of reproducibility**. We state them separately because a
single "run this to reproduce" claim would be false for two of the three.

---

## Tier 1 - Fully reproducible, offline, deterministic

**Every figure and every headline number, regenerated from `data/`.**

```bash
jupyter lab notebooks/01_reproduce_figures.ipynb   # Run All
```

No network, no API keys, no hidden state. If a number in the README or in
`docs/METHODOLOGY_approvals.md` cannot be reproduced by this notebook, that is a bug -
please open an issue.

This is the tier that matters for checking our arithmetic and for building on the results.

## Tier 2 - Reproducible from the frozen snapshot, with two non-deterministic steps

**The classification pipeline (`src/pipeline_1990_2025.py`), re-run over
`snapshot/drugs_at_fda_snapshot.json.gz`.**

`src/pipeline_1990_2025.py` is a frozen record of the code as executed, not a turnkey
script - see its module docstring for the three reasons why, and note that it reproduces
the *pre-correction* numbers (1243 substances) because five defects found afterwards were
fixed in the published tables rather than retrofitted into the source.

The snapshot is the exact Drugs@FDA pull the analysis was built on. We ship it because
**Drugs@FDA is a current-state database, not an archive** - it purges withdrawn products.
Re-pulling it today gives a different corpus, so without this snapshot Tier 2 would be
impossible, not merely awkward. Anyone re-running against a live pull should expect
different numbers and should not treat the difference as an error in either result.

Two steps inside the pipeline do not reproduce bit-for-bit:

1. **ChEMBL cross-reference.** Queried live. ChEMBL is re-curated between releases, so
   molecule types and identifiers can change. Our resolved values are frozen in
   `validation/chembl_crosswalk.csv` - use that file for exact reproduction and query
   ChEMBL live only if you want to refresh it.
2. **LLM adjudication of 30 discordant cases.** Where the rule engine and ChEMBL
   disagreed, a language model cast a third vote. This is not deterministic across
   model versions. All 30 decisions, with the reasoning, are frozen in
   `data/approvals_substance_level.csv` (`final_basis`, and the `llm_*` columns in
   `validation/` for the 2006-2025 subset). **They are auditable but not re-derivable.**
   Across both eras, **54 of 1246 substances (4.3%)** carry a classification in which a
   model vote was one of the deciding signals, and a further **41** were individually
   adjudicated with a written rationale recorded verbatim in `final_basis` (5 of those
   after the model erred on glycan chemistry). The remaining **1151 (92.4%)** were settled
   by the rule engine and ChEMBL alone and are fully deterministic. Filter `final_basis`
   in `data/approvals_substance_level.csv` to isolate each group.

## Tier 3 - Not reproducible, by nature

1. **The original corpus pull.** See above: the source database mutates and purges.
   Only the snapshot is reproducible, not the act of obtaining it.
2. **The withdrawal list.** 45 entries assembled by hand from regulatory history,
   because no machine-readable registry exists. Four candidate sources were tested and
   each failed for a recorded reason (`validation/withdrawal_source_assessment.csv`).
   The list is **individually checkable but not benchmarkable**: any reader can verify
   that fenfluramine was withdrawn in 1997, but nobody - including us - can verify that
   the list is complete.

---

## How to check our work

Ranked by value per unit effort:

1. **`validation/validation_checks_approvals.csv`** - 13 internal consistency
   checks, all passing. Cheap to re-run from the notebook.
2. **`validation/reconciliation_vs_fda_published.csv`** - the external benchmark.
   Our counts against FDA's published novel-drug counts, per year, 2006-2025, with a
   per-year note explaining every non-zero difference by mechanism. We did not tune our
   pipeline to force agreement; the residual differences are real and explained.
3. **`data/withdrawals_substance_level.csv`** - the weakest part of the release. Scan it
   for withdrawals we missed. `modality_crosscheck` records, for each of the 21 entries
   still present in the approval corpus, whether our hand-assigned modality matched the
   independently-derived pipeline classification (it did, 21/21).
4. **`validation/exclusion_log_full.csv`** - every application the pipeline dropped, with
   a reason. If you think something belongs in the universe that isn't, look here first.
5. **`validation/other_class_breakdown.csv`** - all members of the residual "Other" class
   with subcategory and confidence, so you can re-bin them under a different scheme.

## Known defects that were found and fixed

Documented for the benefit of anyone building a similar pipeline; each of these produced
a wrong number before it was caught.

| Defect | Effect | How it surfaced |
|---|---|---|
| Prodrug-ester tokens in the salt-stripping list | Tenofovir alafenamide and fluticasone furoate collapsed onto earlier siblings, losing 2 substances | Year-level disagreement with published counts |
| Substring match on FDA novelty class codes | "Type 10 - New Indication" matched the "Type 1" pattern | Universe size implausibly large |
| Silent date-parse failure | All approval dates null | Coverage table came back empty for every year |
| Token budget too low for the adjudicating model | 6 responses returned empty and silently fell back to the rule class | Parse-failure count checked explicitly |
| Wrong column name assumed for ChEMBL identifiers | Lookup appeared to match nothing while returning populated types | Null-rate check on a column that should have been dense |
| Synthetic pentasaccharide classified as an oligonucleotide | Fondaparinux mis-binned; heparins inconsistent | Manual review of adjudicated cases |
| `BENZYL ALCOHOL` on the excipient exclusion list | Ulesfia (2009) dropped entirely - benzyl alcohol is its active ingredient | Substance present in the 2006-2025 set but absent from the 1990-2025 rebuild |
| `BISMUTH SUBCITRATE` on the counterion list | Pylera (2006) dropped - bismuth subcitrate potassium is the new active moiety | Same comparison |
| `CHOLINE` on the counterion list | Choline C 11 (2012) had its name corrupted to `C 11`; choline is the active moiety of the tracer | Same comparison |
| `ZINC` and `CALCIUM` both stripped as counterions | Pentetate zinc trisodium collapsed onto pentetate calcium trisodium - two distinct 2004 NMEs merged into one | Corpus-wide audit for applications contributing no new moiety |
| Carry-over of validated classifications keyed on substance name | Patiromer was renamed by salt-stripping, missed the carry-over, was re-matched to ChEMBL and typed `Small molecule` - contradicting the hand adjudication that put this non-absorbed polymer in `Other`, and inconsistent with zirconium cyclosilicate | Comparing the 2006-2025 set against the full-period rebuild name by name |

The general lesson: **all but one of these were caught by a check that compared against
something external, not by internal consistency.** Internal consistency was high
throughout, including while the numbers were wrong.
