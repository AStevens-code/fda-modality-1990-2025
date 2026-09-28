# Changelog

## 1.0.0 - 2026-09-15

First public release.

- 1,246 novel active substances, 1990-2025, classified into seven modalities
- 45 curated US market withdrawals on the same scheme
- Approvals reconciled against FDA published novel-drug counts for 2006-2025 (r = 0.9992)
- Frozen Drugs@FDA snapshot shipped so the pipeline is re-runnable despite source mutation
- Corrections applied before release: prodrug-ester salt-stripping fix (tenofovir alafenamide
  and fluticasone furoate restored as distinct substances); FDA novelty class code substring
  match fixed; glycan misclassifications hand-adjudicated
- Late corrections from a pre-release audit of the full-period rebuild (+3 substances, one
  reclassification, two name fixes; 1243 -> 1246). All are recorded per-row in `final_basis`
  and tabulated in `docs/REPRODUCIBILITY.md`:
  - restored `BENZYL ALCOHOL` (Ulesfia, 2009), wrongly filtered as an excipient
  - restored `BISMUTH SUBCITRATE POTASSIUM` (Pylera, 2006), wrongly stripped as a counterion
  - restored `PENTETATE ZINC TRISODIUM` (2004), collapsed onto pentetate calcium trisodium
  - renamed `PENTETATE TRISODIUM` -> `PENTETATE CALCIUM TRISODIUM` and `C 11` -> `CHOLINE C 11`
  - `PATIROMER` moved `Small molecule` -> `Other`, restoring the hand adjudication it had
    regressed out of and making it consistent with zirconium cyclosilicate
- After these corrections the modern era reconciles exactly against the previously validated
  2006-2025 set (767 vs 767; 766/766 classifications identical), which the earlier +/-3
  tolerance had masked
- Added `src/pipeline_1990_2025.py`, the frozen pipeline source, so the Tier 2 claim in
  `docs/REPRODUCIBILITY.md` is backed by shipped code
- Added authorship metadata: `CITATION.cff`, `datapackage.json` contributor block and the
  MIT copyright line completed (all four had shipped with placeholder values)
- Added distribution scaffolding ahead of first deposit: pinned `requirements.txt`
  (pandas 2.3.3 / numpy 2.4.6 / matplotlib 3.11.1, Python 3.11), `.binder/` for one-click
  execution, `.zenodo.json` deposit metadata, `CONTRIBUTING.md` correction policy,
  `.github/` issue templates and a reproducibility workflow, and
  `scripts/check_reproduction.py` which fails CI if any validation check regresses
- Fixed two broken documentation references to a non-existent
  `fda_reconciliation_by_year.csv`, now pointing at
  `validation/reconciliation_vs_fda_published.csv`; surfaced by a link scan widened to
  catch bare filenames, which the earlier path-only scan had missed
- Fixed a truncated MIT licence: `LICENSE-code.txt` ended at "EXPRESS OR IMPLIED" and
  omitted the limitation-of-liability clause entirely, so it disclaimed warranty without
  disclaiming liability. Replaced with the complete MIT text. Surfaced by GitHub reporting
  the repository licence as NOASSERTION, which prompted a look at why the text would not
  match
- Added the CC BY 4.0 legal code as the root `LICENSE` (canonical text, retrieved rather
  than transcribed) so the licence is machine-detectable and the archive is self-contained;
  `LICENSE-data.txt` retained as the scope and third-party provenance note
- Added author ORCID 0009-0004-6011-8585 to `CITATION.cff`, `.zenodo.json` and `datapackage.json`
- Wired the reserved Zenodo DOI 10.5281/zenodo.23017496 into `CITATION.cff`, `README.md` (citation line
  and badge) and `datapackage.json` before publishing, so the archived v1.0.0 cites itself
- Narrowed the MIT copyright line to the author personally; the institutional string in
  `CITATION.cff`, `.zenodo.json` and `datapackage.json` is an affiliation, not an
  ownership claim, and is unchanged
- Corrected the README citation line: publisher is Zenodo, not the author's institution,
  matching DataCite practice and the citation Zenodo itself renders on the record page
- Recorded the Zenodo concept DOI 10.5281/zenodo.23017495 in `CITATION.cff` (as an additional
  identifier) and the README, so the archived package distinguishes the always-latest
  identifier from the version-pinned one
