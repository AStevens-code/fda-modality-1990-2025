# FDA Novel Drug Approvals by Therapeutic Modality, 2006-2025

## What was counted

**Universe: novel active substances.** One row per active moiety on its first US
approval. Source: Drugs@FDA (openFDA), all original NDA and BLA submissions with
approval status, 87120 submission records across 5983 applications.

- **766 novel active substances** across 755 approval events, 2006-2025.
- Inclusion: FDA submission class "Type 1 - New Molecular Entity", plus 2 substances
  adjudicated in individually (below).
- A moiety can be counted **once only**, in its earliest year. New combinations,
  new formulations, new indications, new dosage forms, biosimilars and generics
  are excluded by construction.

## Errors found and corrected during review

| # | Error | Effect if uncorrected | Fix |
|---|-------|----------------------|-----|
| 1 | `"Type 1"` matched as bare substring | `"Type 10 - New Indication"` absorbed; Wegovy, Zepbound, Saxenda counted as novel | anchored regex `Type\s*1\s*-\s*New Molecular Entity` |
| 2 | Multi-substance ingredient strings unsplit | combination products treated as one novel moiety | split on `,` and ` AND ` in addition to `\|` |
| 3 | Salt/hydrate/ester forms not normalized | same moiety recounted as new (e.g. sodium/hydrochloride variants) | 61-token salt-stripping normalizer |
| 4 | Suffix codes on biologic INNs (`-jsgr`, `-blmf`) | each biologic counted twice | strip trailing 4-letter code |
| 5 | FDA source typo `ISLELIZUMAB-JSGR` (Tevimbra) | phantom novel moiety in 2025 | typo correction map |
| 6 | Hyaluronidase co-formulant counted as novel | subcutaneous co-formulations inflated counts | delivery-enzyme exclusion |
| 7 | Claim order not prioritised by class code | Ryzodeg (combination) claimed insulin degludec before Tresiba (the NME) | Type-1 records claim moieties first within a date |
| 8 | `-otide` stem matched as oligonucleotide | lanreotide, abaloparatide, Ga-68 dotatate misclassified | curated peptide lexicon overrides stem |
| 9 | `-cept`/`-catib` stem false positives | Tc-99m tilmanocept -> "protein"; brensocatib -> "protein" | curated overrides |
| 10 | ChEMBL has no "peptide" molecule_type | 27 peptides would be reported as proteins | rule+model agreement overrides ChEMBL for this axis |

## Assumptions made explicit

- **ADC is scored as its own class, never double-counted as Antibody.** All 14 ADCs
  carry an antibody-plus-payload INN (vedotin, deruxtecan, emtansine, govitecan,
  ozogamicin, tesirine, mafodotin, soravtansine, pasudotox).
- **Peptide vs Protein/Enzyme** is drawn at roughly 50 residues and by manufacturing
  route: synthetic peptides (semaglutide, tirzepatide) are Peptide; recombinant
  fusions (dulaglutide, albiglutide - GLP-1 fused to albumin or Fc) are Protein/Enzyme.
- **Peptidic natural products** conventionally handled as small molecules
  (echinocandins, lipoglycopeptides, romidepsin, carfilzomib) are Small molecule.
- **PSMA radioligands** (Ga-68 gozetotide, Lu-177 vipivotide) are small-molecule
  Glu-urea-Lys ligands, not peptides; somatostatin analogues (DOTATATE, DOTATOC) are peptides.
- Bispecific and trispecific antibodies are Antibody; Fc-only fusions without an
  antigen-binding domain (efgartigimod alfa) are Protein/Enzyme.
- **Other** (14) = polymers, oligosaccharides, botanical mixtures, imaging
  colloids, gas microspheres, surfactant mixtures.

## Three-signal reconciliation

Each substance was classified three independent ways: INN-stem rule engine,
ChEMBL `molecule_type` (742/766 matched, 97%), and a blind
reasoning-model pass with a fixed rubric.

| Agreement basis | n |
|---|---|
| Unanimous, all 3 signals | 676 |
| Unanimous, 2 available signals | 26 |
| Rule+model agree, ChEMBL taxonomy lacks peptide type | 27 |
| Rule+model agree, ChEMBL differs | 2 |
| Hand-adjudicated against chemistry | 35 |
| **Unresolved** | **0** |

## External validation: 24/24 checks pass

- **Per-year totals vs published CDER novel-drug counts (2006-2024): r = 0.9979**,
  maximum yearly deviation 2, 7 years exact. Totals 718 (this analysis) vs 713 (CDER).
- **ChEMBL `first_approval` year agreement**: 92.3% within +/-1 year (n=653).
  All 39 outliers run one direction - ChEMBL earlier, never later - because ChEMBL
  records first *global* approval (e.g. amisulpride: EU 1986, US 2020). Expected signature.
- 14 landmark drugs spot-checked for correct year and class: all pass.
- Structural invariants: no duplicate moiety, one class per moiety, ADC/Antibody
  disjoint, class totals sum to universe, no nulls.

## Limitations

1. **CBER products are absent.** Drugs@FDA covers CDER drugs and therapeutic
   biologics only. **No vaccines, cell therapies (CAR-T), or gene therapies** -
   Kymriah, Yescarta, Zolgensma, Luxturna, Comirnaty are all outside this dataset.
   Verified directly: their BLA numbers return no records. Roughly 5-10 CBER
   approvals per year in recent years are therefore not represented, and the
   "Other" class does **not** stand in for them.
2. **2025 is partial** - the corpus was retrieved mid-August 2026, so late-2025
   approvals may be incomplete relative to the final published figure.
3. **Withdrawn-and-reapproved products** anchor to the year present in Drugs@FDA.
   Blenrep appears at 2025 (re-approval) because its 2020 original BLA is absent
   from the corpus; Mylotarg's 2017 re-approval was excluded for the same reason
   with its original 2000 BLA missing.
4. **Peptide/protein boundary is a convention, not a fact.** The ~50-residue cut
   is defensible but arbitrary; ~30 substances sit near it. Reclassifying all
   Fc/albumin fusions as Peptide would move ~5 substances.
5. Two substances lacked a parseable model vote; both were resolved by rule+ChEMBL agreement.


---

# Addendum: reconciliation against FDA's published Novel Drug Approvals list

The user compared 2021, 2024 and 2025 against FDA's published counts (50, 50, 46)
and found differences. Diagnosis below. **The deltas run in both directions, which
ruled out a systematic error and pointed at definitional boundaries.**

## Cause 1 (dominant): counting unit — moieties vs drugs

FDA counts **approved drug products**. I counted **novel active moieties**. These
diverge whenever one approval carries two or more new molecular entities. Ten such
applications exist in the window:

| Year | Application | Brand | New moieties |
|---|---|---|---|
| 2006 | NDA021502 | Anthelios SX | 2 |
| 2009 | NDA022268 | Coartem | 2 |
| 2012 | NDA203100 | Stribild | 2 |
| 2014 | NDA206619 | Viekira Pak | 3 |
| 2016 | NDA208261 | Zepatier | 2 |
| 2017 | NDA209394 | Mavyret | 2 |
| 2020 | BLA761169 | Inmazeb | 3 |
| 2024 | NDA218730 | Alyftrek | 2 |
| 2025 | NDA219616 | Avmapki Fakzynja | 2 |
| 2025 | NDA219792 | Kygevvi | 2 |

This fully explains 2024 (+1) and 2025 (+2). Counting on the drug basis reproduces
FDA's 2024 = 50 and 2025 = 46 exactly.

## Cause 2: a genuine error in my normalizer (now fixed)

My salt-stripping token list wrongly included **ALAFENAMIDE**, **DISOPROXIL** and
**FUROATE**. These are distinct prodrug esters, not salt counterions. The effect:

- **Tenofovir alafenamide** (Genvoya, 2015) was collapsed onto tenofovir disoproxil
  (2001) and dropped from the universe. FDA treats TAF as a separate NME. **Corrected
  — 2015 now matches exactly at 45.**
- Fluticasone furoate (2007) was collapsed onto fluticasone propionate (1990); outside
  the Type-1 set so it did not change a count, but the token was removed regardless.

Universe: 766 -> **767 moieties**, 755 -> **756 approval events**. Class totals move by
one (Small molecule 503 -> 504). No trend claim changes.

## Cause 3: withdrawn products purged from Drugs@FDA

**Melphalan flufenamide** (Pepaxto, 2021) returns no records at all — withdrawn 2024
and removed from the database. This is the whole of the 2021 delta. Same mechanism
already documented for Blenrep and Mylotarg. Drugs@FDA is a *current* database, not
an archival one, so retrospective counts from it systematically under-count
withdrawn products.

## Cause 4: Lumizyme (2010)

Excluded by design as the same active moiety as Myozyme (alglucosidase alfa, 2006).
FDA's list counts the new BLA. A defensible difference in unit, not an error: on a
moiety basis it is the same substance.

## Residual after correction

| Basis | Exact-match years | Mean abs. deviation | Max deviation |
|---|---|---|---|
| Moiety count | 7 / 20 | 0.75 | 3 |
| **Drug count** | **14 / 20** | **0.35** | **1** |

Correlation on the drug basis: **r = 0.9992**, totals 755 vs 759 over 2006-2025.
Remaining deltas are all exactly +/-1, in 2008 (+1), 2010, 2011, 2012, 2020, 2021 (-1 each).
2010 and 2021 have identified causes above. The other four are single-drug boundary
cases — most plausibly approvals near a 31 December / 1 January edge that FDA assigns
to the adjacent year's report (2012 alone has 8 December approvals, including one on
31 December), or a product FDA's list treats differently. I did not force these to
match, since fabricating agreement would defeat the point of an independent count.

## Which number should you use?

- **For matching FDA's published headline**: use the drug count in
  `validation/reconciliation_vs_fda_published.csv`.
- **For modality analysis** (the purpose here): the moiety count is the right unit.
  Alyftrek contributes two distinct small molecules; Inmazeb contributes three distinct
  antibodies. Collapsing them to one product would understate the chemistry.

Both are now published side by side so either can be cited.
