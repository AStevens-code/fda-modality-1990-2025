# Data dictionary

Field-level definitions for every table shipped in `data/` and `validation/`.
Row and column counts are as-shipped.


## `data/`

### `approvals_by_era.csv`

-  4 rows x 8 cols

| field | type | description |
|---|---|---|
| `era` | string | Decade grouping: 1990-1999, 2000-2009, 2010-2019, 2020-2025. |
| `small_molecule` | integer | Count (or share, in share tables) of novel approvals classified as Small molecule. |
| `antibody` | integer | Count (or share, in share tables) of novel approvals classified as Antibody. |
| `adc` | integer | Count (or share, in share tables) of novel approvals classified as ADC. |
| `peptide` | integer | Count (or share, in share tables) of novel approvals classified as Peptide. |
| `protein_enzyme` | integer | Count (or share, in share tables) of novel approvals classified as Protein/Enzyme. |
| `oligonucleotide` | integer | Count (or share, in share tables) of novel approvals classified as Oligonucleotide. |
| `other` | integer | Count (or share, in share tables) of novel approvals classified as Other. |

### `approvals_by_year.csv`

-  36 rows x 10 cols

| field | type | description |
|---|---|---|
| `year` | integer | Calendar year of first US approval. |
| `small_molecule` | integer | Count (or share, in share tables) of novel approvals classified as Small molecule. |
| `antibody` | integer | Count (or share, in share tables) of novel approvals classified as Antibody. |
| `adc` | integer | Count (or share, in share tables) of novel approvals classified as ADC. |
| `peptide` | integer | Count (or share, in share tables) of novel approvals classified as Peptide. |
| `protein_enzyme` | integer | Count (or share, in share tables) of novel approvals classified as Protein/Enzyme. |
| `oligonucleotide` | integer | Count (or share, in share tables) of novel approvals classified as Oligonucleotide. |
| `other` | integer | Count (or share, in share tables) of novel approvals classified as Other. |
| `total` | integer | Sum across the seven modality columns for that year. |
| `confidence` | string | Evidential tier for the row: validated (2006-2025) or lower (1990-2005). See README. |

### `approvals_share_by_year.csv`

-  36 rows x 9 cols

| field | type | description |
|---|---|---|
| `year` | integer | Calendar year of first US approval. |
| `small_molecule` | number | Count (or share, in share tables) of novel approvals classified as Small molecule. |
| `antibody` | number | Count (or share, in share tables) of novel approvals classified as Antibody. |
| `adc` | number | Count (or share, in share tables) of novel approvals classified as ADC. |
| `peptide` | number | Count (or share, in share tables) of novel approvals classified as Peptide. |
| `protein_enzyme` | number | Count (or share, in share tables) of novel approvals classified as Protein/Enzyme. |
| `oligonucleotide` | number | Count (or share, in share tables) of novel approvals classified as Oligonucleotide. |
| `other` | number | Count (or share, in share tables) of novel approvals classified as Other. |
| `confidence` | string | Evidential tier for the row: validated (2006-2025) or lower (1990-2005). See README. |

### `approvals_substance_level.csv`

-  1246 rows x 11 cols

| field | type | description |
|---|---|---|
| `moiety` | string | Normalised active moiety name, uppercase. Salts/hydrates stripped to parent; distinct prodrug esters retained. |
| `application_number` | string | FDA application number, prefix included (e.g. NDA021436, BLA125057). |
| `application_prefix` | string | NDA or BLA. |
| `approval_year` | integer | Calendar year of first US approval of this moiety. |
| `approval_date` | string | FDA submission status date for the approval action (ISO date). |
| `brands` | string | Pipe-delimited brand name(s) recorded on the application. |
| `sponsor` | string | Applicant/sponsor as recorded by FDA at the time of the pull. |
| `fda_submission_class` | string | FDA submission class code description for the original submission (e.g. 'Type 1 - New Molecular Entity'). |
| `final_class` | string | Assigned therapeutic modality. One of: Small molecule, Antibody, ADC, Peptide, Protein/Enzyme, Oligonucleotide, Other. |
| `final_basis` | string | How the modality was decided: rule engine, ChEMBL concordance, model vote, or a written per-case adjudication. |
| `era_confidence` | string | Per-row evidential tier, matching the `confidence` column of the aggregate tables. |

### `withdrawal_rate_by_era.csv`

-  4 rows x 4 cols

| field | type | description |
|---|---|---|
| `era` | string | Decade grouping: 1990-1999, 2000-2009, 2010-2019, 2020-2025. |
| `approvals` | integer | Count of novel approvals in the era. |
| `withdrawals` | integer | Count of withdrawal events in the era. |
| `withdrawal_rate_pct` | number | withdrawals / approvals x 100 for the era. Not a per-drug hazard; see KNOWN_ISSUES. |

### `withdrawals_by_year.csv`

-  36 rows x 9 cols

| field | type | description |
|---|---|---|
| `withdrawal_year` | integer | Calendar year the product was withdrawn from the US market. |
| `small_molecule` | integer | Count (or share, in share tables) of novel approvals classified as Small molecule. |
| `antibody` | integer | Count (or share, in share tables) of novel approvals classified as Antibody. |
| `adc` | integer | Count (or share, in share tables) of novel approvals classified as ADC. |
| `peptide` | integer | Count (or share, in share tables) of novel approvals classified as Peptide. |
| `protein_enzyme` | integer | Count (or share, in share tables) of novel approvals classified as Protein/Enzyme. |
| `oligonucleotide` | integer | Count (or share, in share tables) of novel approvals classified as Oligonucleotide. |
| `other` | integer | Count (or share, in share tables) of novel approvals classified as Other. |
| `total` | integer | Sum across the seven modality columns for that year. |

### `withdrawals_substance_level.csv`

-  45 rows x 13 cols

| field | type | description |
|---|---|---|
| `moiety` | string | Normalised active moiety name, uppercase. Salts/hydrates stripped to parent; distinct prodrug esters retained. |
| `withdrawal_year` | integer | Calendar year the product was withdrawn from the US market. |
| `final_class` | string | Assigned therapeutic modality. One of: Small molecule, Antibody, ADC, Peptide, Protein/Enzyme, Oligonucleotide, Other. |
| `withdrawal_basis` | string | safety, efficacy, or a combination. |
| `withdrawal_reason` | string | Short description of the withdrawal trigger. |
| `returned` | boolean | True if the drug later returned to the US market. |
| `return_note` | string | Circumstances of return, where applicable. |
| `scope` | string | 'moiety-wide' or 'formulation' - whether the whole moiety or only one formulation was withdrawn. |
| `scope_note` | string | Which formulation, for formulation-scoped withdrawals. |
| `pipeline_class` | string | Modality independently derived by the approvals pipeline, where the drug survives in Drugs@FDA. Blank if purged. |
| `approval_year` | number | Calendar year of first US approval of this moiety. |
| `modality_crosscheck` | string | Whether the hand-assigned modality agreed with `pipeline_class`. |
| `chembl_withdrawal_year` | number | ChEMBL drug_warning year, where present. First GLOBAL withdrawal, not necessarily US. |


## `validation/`

### `chembl_crosswalk.csv`

-  766 rows x 6 cols

| field | type | description |
|---|---|---|
| `moiety` | string | Normalised active moiety name, uppercase. Salts/hydrates stripped to parent; distinct prodrug esters retained. |
| `chembl_id` | string | ChEMBL molecule identifier, where matched. |
| `chembl_name` | string | ChEMBL preferred name. |
| `chembl_type` | string | ChEMBL `molecule_type` value. |
| `chembl_first_approval` | number | ChEMBL `first_approval` year. Note: this is first GLOBAL approval, not US. |
| `matched_on` | string | Which ChEMBL field the moiety name matched (preferred name or synonym). |

### `exclusion_log_full.csv`

-  1554 rows x 6 cols

| field | type | description |
|---|---|---|
| `app` | string | FDA application number. |
| `year` | integer | Calendar year of first US approval. |
| `brands` | string | Pipe-delimited brand name(s) recorded on the application. |
| `ingredients` | string | Active ingredient string as recorded by FDA. |
| `cls` | string | FDA submission class code description. |
| `reason` | string | Why the application was excluded from the universe. |

### `exclusion_log_manual.csv`

-  21 rows x 5 cols

| field | type | description |
|---|---|---|
| `app` | string | FDA application number. |
| `year` | number | Calendar year of first US approval. |
| `brands` | string | Pipe-delimited brand name(s) recorded on the application. |
| `ingredients` | string | Active ingredient string as recorded by FDA. |
| `reason` | string | Why the application was excluded from the universe. |

### `other_class_breakdown.csv`

-  21 rows x 9 cols

| field | type | description |
|---|---|---|
| `moiety` | string | Normalised active moiety name, uppercase. Salts/hydrates stripped to parent; distinct prodrug esters retained. |
| `brands` | string | Pipe-delimited brand name(s) recorded on the application. |
| `approval_year` | integer | Calendar year of first US approval of this moiety. |
| `application_number` | string | FDA application number, prefix included (e.g. NDA021436, BLA125057). |
| `subcategory` | string | Sub-grouping within the residual 'Other' class. |
| `why_other` | string | Why this substance is not one of the six named modalities. |
| `era_confidence` | string | Per-row evidential tier, matching the `confidence` column of the aggregate tables. |
| `sponsor` | string | Applicant/sponsor as recorded by FDA at the time of the pull. |
| `final_basis` | string | How the modality was decided: rule engine, ChEMBL concordance, model vote, or a written per-case adjudication. |

### `pre2006_feasibility.csv`

-  36 rows x 8 cols

| field | type | description |
|---|---|---|
| `year` | integer | Calendar year of first US approval. |
| `orig_approvals_in_corpus` | integer | Original NDA/BLA approvals present in the corpus for that year. |
| `pct_with_novelty_class_code` | number | Share of that year's originals carrying an FDA novelty class code. |
| `type1_apps` | integer | Applications flagged Type 1 - New Molecular Entity. |
| `my_universe_events` | integer | Novel-substance events our pipeline identifies for that year. |
| `published_nme_benchmark` | integer | Published NME/novel count for that year, where available. |
| `delta` | integer | my_universe_events minus published_nme_benchmark. |
| `era` | string | Decade grouping: 1990-1999, 2000-2009, 2010-2019, 2020-2025. |

### `reconciliation_vs_fda_published.csv`

-  20 rows x 7 cols

| field | type | description |
|---|---|---|
| `year` | integer | Calendar year of first US approval. |
| `my_drug_count` | integer | Our count on a product basis, for comparison with FDA's published list. |
| `my_moiety_count` | integer | Our count on a moiety basis (the basis used throughout `data/`). |
| `fda_published_novel` | integer | FDA's published novel drug approval count for that year. |
| `delta_drugs` | integer | my_drug_count minus fda_published_novel. |
| `delta_moieties` | integer | my_moiety_count minus fda_published_novel. |
| `note` | string | Mechanism explaining a non-zero delta for that year. |

### `validation_checks_2006_2025_detailed.csv`

-  24 rows x 3 cols

| field | type | description |
|---|---|---|
| `check` | string | Name of the internal consistency check. |
| `result` | string | PASS or FAIL. |
| `detail` | string | Observed values behind the check. |

### `validation_checks_approvals.csv`

-  13 rows x 3 cols

| field | type | description |
|---|---|---|
| `check` | string | Name of the internal consistency check. |
| `result` | string | PASS or FAIL. |
| `detail` | string | Observed values behind the check. |

### `withdrawal_source_assessment.csv`

-  5 rows x 5 cols

| field | type | description |
|---|---|---|
| `source` | string | Candidate withdrawal data source evaluated. |
| `has_year` | boolean | Whether the source carries a withdrawal year. |
| `us_specific` | string | Whether the source's year is US-specific. |
| `recall_on_known` | string | Measured recall against a hand-assembled list of known withdrawals. |
| `verdict` | string | Why the source was accepted or rejected. |

### `withdrawn_drug_purge_probe.csv`

-  20 rows x 3 cols

| field | type | description |
|---|---|---|
| `drug` | string | Well-known withdrawn drug used to probe source coverage. |
| `note` | string | Mechanism explaining a non-zero delta for that year. |
| `status` | string | Whether a Drugs@FDA record survives for it. |

