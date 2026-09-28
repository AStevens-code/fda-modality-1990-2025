# US Drug Withdrawals by Modality, 1990-2025

**45 curated US market withdrawals**, classified on the same seven-modality scheme and
colour scheme as the approvals analysis, plotted on a negative axis for direct visual
pairing.

---

# CRITICAL: this series is NOT of the same evidential class as the approvals series

The approvals series is **data-derived and benchmarked** (r = 0.999 vs FDA's published
novel-drug counts for 2006-2025). This withdrawals series is **curated and
un-benchmarkable**. They are plotted together because that is the useful comparison, but
they should not be cited with equal confidence.

## Why no data-derived route exists

I tested four sources before resorting to curation.

| Source | Withdrawal year? | US-specific? | Recall on 25 known withdrawals | Verdict |
|---|---|---|---|---|
| Drugs@FDA `marketing_status` | **No date field at all** | - | - | "Discontinued" spans 6,056 products and is overwhelmingly commercial. Atorvastatin (never withdrawn) shows 4 Discontinued products. |
| openFDA `enforcement` endpoint | Yes | Yes | - | Lot-level recalls (contamination, labeling), not market withdrawals. |
| ChEMBL `withdrawn_flag` | **No year** | No | - | Boolean only. |
| ChEMBL `drug_warning` | Yes | Partially | **8/25 (32%)** | See below. |

**ChEMBL `drug_warning` fails on three counts.** (1) It collapses a multi-country
withdrawal into a single row with a single year: troglitazone reads **1997**
(UK/Peru) when the US withdrawal was **2000** - the same ex-US bias found earlier in
`first_approval`. 67% of its US-relevant records are multi-country and therefore
year-ambiguous. (2) Recall is 32% - it misses propoxyphene, lorcaserin, efalizumab,
ranitidine, drotrecogin alfa, pergolide, natalizumab, ponatinib and more.
(3) It shows 26 withdrawals in 1990-2001 against 7 in 2014-2025; the true US withdrawal
rate did not fall four-fold, so recent events are simply under-curated.

**The decisive problem was modality coverage.** Because Drugs@FDA purges withdrawn
products, only **21 of 45** withdrawn drugs still have an FDA record to classify from.
The loss is worst exactly where the signal matters most - in a first pass, the 1990s
returned **1 classifiable withdrawal out of 10**. A chart built that way would have
drawn the 1990s as a safe decade and the 2000s as a risky one, which is backwards, and
it would have inherited false authority from sitting directly beneath a validated series.

**Resolution.** Modality classification does not require an FDA record - fenfluramine is
a small molecule and efalizumab is an antibody whether or not Drugs@FDA still lists them.
So all 45 are classified. What cannot be validated is *completeness of the list itself*.

## What I could validate

- **Modality: 21/21 agreement.** For every withdrawal still present in the approval
  universe, my hand-assigned modality matches the independently-derived pipeline
  classification. Zero disagreements.
- **Chronology: 20/21 correct.** Approval precedes withdrawal in all cases except
  belantamab mafodotin, where the 2022 withdrawal precedes the 2025 *re*-approval
  now recorded in Drugs@FDA - the original 2020 BLA was purged. This is the documented
  purge mechanism, not an error.
- **Year: 12/16 exact** against ChEMBL where it has a record. Of the 4 disagreements,
  2 are ChEMBL reporting the earlier ex-US withdrawal (troglitazone 1997 vs US 2000;
  trovafloxacin 1999 EU restriction vs US 2001) and 2 are ChEMBL later.

## Limitations

- **Completeness is not benchmarked and cannot be.** There is no published, machine-
  readable, complete registry of US market withdrawals. The list is likely to miss
  obscure withdrawals, particularly older ones and non-safety commercial exits.
- **"Withdrawal" is a boundary judgement.** I count removal of a product from the US
  market for safety or failed-efficacy reasons. I exclude purely commercial
  discontinuations, generic exits, and manufacturing shutdowns. Reasonable analysts
  would draw this line differently.
- **6 of 45 later returned to market** (marked with a triangle): alosetron, natalizumab,
  tegaserod, ponatinib, gemtuzumab ozogamicin, belantamab mafodotin. They are charted as
  withdrawal events because the event occurred; if you want permanent withdrawals only,
  the count drops to 39 and ADCs fall to zero.
- **4 of 45 are formulation-specific**, not moiety-wide: hydromorphone (Palladone ER
  only), bromfenac (oral only), gatifloxacin (systemic only), sodium phenylbutyrate
  (Relyvrio combination only). Flagged in `scope` in the detail table.
- **Small-number statistics.** Median 1 withdrawal per year, max 4, and 13 of 36 years
  are zero. Single-year comparisons are meaningless; read eras.

---

# Findings

## Withdrawals run 28:1 behind approvals

1,246 approvals against 45 withdrawals over 36 years.

## The withdrawal rate peaked in the 2000s, not the 1990s

| Era | Approvals | Withdrawals | Rate |
|---|---|---|---|
| 1990-1999 | 325 | 11 | 3.4% |
| 2000-2009 | 247 | 17 | **6.9%** |
| 2010-2019 | 380 | 9 | 2.4% |
| 2020-2025 | 294 | 8 | 2.7% |

The 2000s peak is driven by the COX-2 reckoning (rofecoxib 2004, valdecoxib 2005),
the QT-prolongation cohort, and the fluoroquinolone hepatotoxicity cases. The post-2010
decline to ~2.5% is consistent with REMS programmes, mandatory CV outcome trials, and
tighter accelerated-approval confirmatory requirements - though part of it may be
censoring, since drugs approved recently have had less time to be withdrawn.

## Withdrawals are disproportionately small molecules

| Modality | Withdrawn | Approved | Withdrawal rate |
|---|---|---|---|
| Small molecule | 35 (78%) | 903 | 3.9% |
| Antibody | 4 | 137 | 2.9% |
| ADC | 2 | 14 | **14.3%** |
| Protein/Enzyme | 2 | 88 | 2.3% |
| Peptide | 1 | 59 | 1.7% |
| Oligonucleotide | 1 | 24 | 4.2% |
| Other | 0 | 21 | 0.0% |

Small molecules are 78% of withdrawals against 72% of approvals - modestly
over-represented. **The ADC rate of 14.3% is the outlier, but it rests on 2 events out
of 14 approvals and both drugs later returned to market** at adjusted doses. Treat it as
a hypothesis about payload-driven toxicity in a young class, not an established rate.

## Reasons

37 of 45 were safety withdrawals; 5 were efficacy failures (mostly accelerated-approval
confirmatory trials); 2 combined; 1 was safety plus commercial. The efficacy-failure
group is entirely post-2010, reflecting the growth of accelerated approval and its
confirmatory-trial requirement.
