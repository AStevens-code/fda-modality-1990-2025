# Known issues and limitations

## Scope boundaries (deliberate, but they will not suit every use)

- **Moiety basis, not product basis.** See README. Convert via
  `validation/reconciliation_vs_fda_published.csv`.
- **CDER-reviewed drugs and therapeutic biologics only.** Vaccines, blood products,
  allergenics, and cell and gene therapies are reviewed by a different FDA centre and are
  absent from the source corpus. A modality breakdown of *all* FDA-regulated therapeutics
  would need a second data source and would add classes not present here.
- **First US approval only.** A drug approved in 1995, withdrawn, and re-approved in 2018
  appears once, in 1995 - except where the original application was purged from the
  source, in which case it appears at the re-approval date. Belantamab mafodotin is the
  known instance (45-entry withdrawal table, `approval_year` 2025 against
  `withdrawal_year` 2022).

## Classification boundaries that reasonable people draw differently

- **Peptide vs Protein/Enzyme.** We cut at roughly 40 residues with attention to whether
  the molecule is chemically synthesised or recombinantly expressed. ChEMBL types many
  short peptides as "Protein"; this accounted for most of the 19 rule-vs-ChEMBL
  disagreements. Insulins and their analogues are the most consequential judgement call.
- **ADC as its own class.** Antibody-drug conjugates are counted separately rather than
  as antibodies. Fold them back in if you want a simple biologic/small-molecule split.
- **Five defects were found in a pre-release audit** and are corrected in the shipped tables
  (+3 substances, one reclassification, two name fixes). Each corrected row carries its reason
  in `final_basis`; the mechanisms are tabulated in `docs/REPRODUCIBILITY.md`. The frozen
  pipeline source in `src/` still contains the defects, deliberately, so the record matches
  what was executed.
- **"Other"** holds 21 substances that are genuinely none of the six - polysaccharides,
  the low-molecular-weight heparins, radiopharmaceuticals, oligosaccharide and complex
  natural-product mixtures. Enumerated with subcategory in
  `validation/other_class_breakdown.csv`. It is a residual, not a modality.

## Data-quality limitations inherited from the source

- **Withdrawn products are purged from Drugs@FDA, inconsistently.** This is the dominant
  source of error in 1990-2005 and the reason that period carries a lower confidence flag.
  `validation/withdrawn_drug_purge_probe.csv` records the probe: well-known withdrawn
  drugs of the period, and whether a record survives.
- **Typographic errors in FDA ingredient fields.** A small number were corrected by hand;
  the corrections are visible in the pipeline's normalisation map.
- **Older records sometimes list formulation components in the active-ingredient field**,
  which required an excipient/co-formulant filter. Over-filtering would drop real
  substances; the filter is deliberately conservative and the dropped rows are logged.

## Withdrawal-series limitations

- **Completeness is not benchmarked and cannot be.** Most important caveat in the package.
- **"Withdrawal" is a judgement.** We count removal from the US market for safety or
  failed-efficacy reasons, and exclude purely commercial discontinuations, generic exits
  and manufacturing shutdowns.
- **6 of 45 later returned to market**, flagged in `returned`. Restricting to permanent
  withdrawals gives 39 and drops ADCs to zero.
- **4 of 45 are formulation-specific**, not moiety-wide, flagged in `scope`.
- **Small numbers.** Median 1 withdrawal per year; 13 of 36 years are zero. Single-year
  comparisons are not meaningful. The ADC withdrawal rate of 14.3% rests on 2 events out
  of 14 approvals and should be read as a hypothesis, not a rate.
- **Right-censoring.** Recently approved drugs have had less time to be withdrawn, so the
  2020-2025 rate is a floor.

## Things we would do differently with more time

- Cross-check 1990-2005 against an archived Drugs@FDA snapshot or the printed *Approved
  Drug Products* annual editions, which would likely recover most of the purged records
  and let that era be validated rather than flagged.
- Seek a second opinion on the ~35 peptide/protein boundary cases from a structural
  definition (residue count and disulfide topology) rather than a name-stem heuristic.
- Add an explicit `is_first_in_class` flag, which is the question most readers ask next.
