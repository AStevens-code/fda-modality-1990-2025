# FDA Novel Drug Approvals by Therapeutic Modality, 1990-2025

**36 years. 1,246 novel active substances. 1,232 approval events.**

Extension of the original 2006-2025 analysis back to 1990. The modern era is unchanged:
all 766 previously validated classifications were carried over verbatim and re-verified
identical. 491 newly admitted substances were classified with the same three-signal method.

---

# READ THIS FIRST: the two eras are not equally reliable

| | 1990-2005 | 2006-2025 |
|---|---|---|
| Mean abs. deviation vs FDA published counts | **2.25** | **0.30** |
| Max deviation | 6 | 1 |
| Years matching exactly | 2 / 16 | 14 / 20 |
| Correlation | 0.958 | 0.999 |

**Per-year counts for 1990-2005 are roughly seven times less precise than for
2006-2025.** The class-*share* trend is robust in both eras; the per-year *counts*
are not. Cite era-level shares for the older period, not individual years.

## Why the older era is worse

### 1. Withdrawn drugs are purged from the source (dominant cause)

Drugs@FDA is a *current-state* database. Products withdrawn from marketing are
removed entirely, not archived. I probed 20 well-known withdrawn drugs of the era;
**4 are absent from the corpus completely**:

| Drug | Approved | Withdrawn |
|---|---|---|
| Terfenadine (Seldane) | 1985 | 1998 |
| Astemizole (Hismanal) | 1988 | 1999 |
| Dexfenfluramine (Redux) | 1996 | 1997 |
| Mibefradil (Posicor) | 1997 | 1998 |

**The purge is inconsistent, which is what makes it uncorrectable.** Vioxx, Rezulin,
Baycol, Trovan, Raxar, Propulsid and Raplon all survive in the database despite equally
prominent withdrawals. There is no rule that predicts which records persist, so no
systematic correction is possible. The 1990s had a high withdrawal rate, so the loss
concentrates exactly in the era being added. This is also why Pepaxto (2021) is missing
from the modern era - the same mechanism, just rarer.

### 2. Formulation components listed as active ingredients

Older records more often list excipients and delivery vehicles in the active-ingredient
field. Exosurf Neonatal (1990) contributes cetyl alcohol and tyloxapol as apparent novel
moieties. Handled with an explicit 24-term excipient exclusion list; 4 cases pre-2006
vs 1 post-2006.

### 3. Pre-INN-standardization naming

Older substances predate consistent INN stem conventions, so the stem-based rule engine
is less reliable. Mitigated by ChEMBL cross-check (99% coverage on older substances -
actually *better* than modern, since old compounds have accumulated more literature)
and hand adjudication.

## What I tested and ruled out

**Hypothesis: the era's published NME lists excluded biologics (CBER reported separately
until the 2003 center transfer), so I should compare NDA-only.** Tested and rejected -
NDA-only agreement is *worse* (mean abs. deviation 2.38 vs 2.25). The residual is
intrinsic to the records, not a definitional mismatch.

**Hypothesis: biologics are truncated before the 2003 CDER/CBER transfer.** Rejected.
The transfer carried historical records with it. Rituximab appears at 1997, trastuzumab
and infliximab at 1998, etanercept 1998, epoetin 1989, imiglucerase 1994, palivizumab
1998, abciximab 1994. 56 BLA approval events sit in 1990-2005.

**Hypothesis: novelty class codes don't exist pre-2006.** Rejected. Coverage of the
`Type 1 - New Molecular Entity` code averages **99.6%** for 1990-2005, slightly better
than the 97.2% of the modern window. The corpus itself reaches back to 1939.

---

# Findings

## Biologic share rose monotonically across all four eras

| Era | Small molecule | Antibody | ADC | Peptide | Protein/Enzyme | Oligonucleotide | Other | **Biologics total** |
|---|---|---|---|---|---|---|---|---|
| 1990-1999 | 87.4% | 2.2% | 0.0% | 3.1% | 5.2% | 0.3% | 1.8% | **10.8%** |
| 2000-2009 | 76.9% | 6.1% | 0.0% | 6.5% | 9.3% | 0.4% | 0.8% | **22.3%** |
| 2010-2019 | 66.8% | 14.2% | 1.8% | 5.3% | 7.4% | 2.1% | 2.4% | **30.8%** |
| 2020-2025 | 59.5% | 20.7% | 2.4% | 4.4% | 6.8% | 4.8% | 1.4% | **39.1%** |

Small molecules fell 27.9 points. Antibodies grew roughly ten-fold as a share.
Oligonucleotides went from 0.3% to 4.8% - almost entirely a post-2016 phenomenon.
ADCs did not exist as an approved class until 2011.

First approval in each class: antibody **1994** (abciximab), oligonucleotide **1998**
(fomivirsen), ADC **2011** (brentuximab vedotin).

## Class totals, 36 years

| Class | 1990-2005 | 2006-2025 | Total |
|---|---|---|---|
| Small molecule | 399 | 504 | 903 |
| Antibody | 14 | 123 | 137 |
| Protein/Enzyme | 33 | 55 | 88 |
| Peptide | 24 | 35 | 59 |
| Oligonucleotide | 2 | 22 | 24 |
| Other | 7 | 14 | 21 |
| ADC | 0 | 14 | 14 |

---

# Method for the newly added substances

Same three-signal approach as the original analysis: INN-stem rule engine, ChEMBL
`molecule_type` cross-check, and a reasoning-model pass, with disagreements adjudicated
individually.

- 491 new substances classified
- ChEMBL matched **466 / 491 (95%)**
- Rule-vs-ChEMBL concordance **93.4%** (423/453 comparable)
- 30 discordant cases adjudicated to zero unresolved

## Errors found and corrected during this extension

1. **Seven biologics fell to the small-molecule residual** - beractant, calfactant,
   onabotulinumtoxinA, botulinum toxin type B, aprotinin, corticorelin, mecasermin
   rinfabate. Caught by an audit asserting no BLA-prefix substance may be classified
   Small molecule. Added to the curated lexicon; surfactants routed to Other as
   complex biological mixtures with no single active moiety.
2. **`max_tokens=12` truncated 6 model responses to empty strings**, which silently
   fell back to the rule class. Caught by counting parsed labels. Re-run at 300 tokens;
   all 6 resolved (and 5 of 6 changed the answer).
3. **Fondaparinux labelled Oligonucleotide** by the model - it is a synthetic
   pentasaccharide, not a nucleic acid. The heparins (enoxaparin, dalteparin,
   tinzaparin) were also inconsistently split between Small molecule and Other.
   All 5 glycans hand-adjudicated: heparins to Other (polydisperse polysaccharide
   mixtures), fondaparinux and acarbose to Small molecule (single defined structures).
4. **A mis-citation in the previous session's report**: I had attributed BLA761232 to
   Blenrep. It is Tevimbra (tislelizumab, 2024). Blenrep is BLA761440 (2025), and it
   carries a `Type 2 - New Active Ingredient` code rather than Type 1, so it needs
   explicit admission. Corrected.
5. **Reconstructed salt-token list was incomplete** - missing DISODIUM, HEMIFUMARATE,
   DIPHOSPHATE, ADIPATE. Produced 6 label variants (e.g. `GADOXETATE DISODIUM` vs
   `GADOXETATE`). Fixed. One substantive improvement fell out: bismuth now correctly
   traces to Helidac (1996) rather than Pylera (2006).

## Validation

13/13 structural checks pass, including: all 766 carried-over classifications identical
to the validated set; no BLA substance classified as a small molecule; 12/12 landmark
approval years correct; no ADC before 2000; antibodies present pre-2000; excipients
excluded.

## Limitations

- **Per-year counts pre-2006 carry roughly 2-3 drugs of uncertainty.** Use era shares.
- **Withdrawn drugs are systematically missing**, non-uniformly, unfixably.
- CBER-only classes remain out of scope throughout: vaccines, blood and plasma products,
  allergenics, cell and gene therapy. Therapeutic proteins and monoclonal antibodies
  ARE included, because they transferred to CDER in 2003 and their historical records
  came with them.
- The peptide/protein boundary is a convention, not a fact. I place synthetic chains
  under ~50 residues (including insulins) in Peptide and recombinant enzymes, cytokines
  and Fc-fusion proteins in Protein/Enzyme. Cyclic peptide natural products used as
  conventional drugs (daptomycin, echinocandins) are Small molecule by convention.
  Reasonable people draw these lines differently.
- Counting basis here is **novel active moieties**, not products. See
  `validation/reconciliation_vs_fda_published.csv` for the product-basis bridge to FDA's published headline.
