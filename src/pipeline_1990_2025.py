"""Classification pipeline for the 1990-2025 FDA novel-approval modality analysis.

FROZEN SOURCE RECORD, captured 2026-09-15. This is the code that produced
data/approvals_substance_level.csv from snapshot/drugs_at_fda_snapshot.json.gz.

Read this as the authoritative statement of what the pipeline did. It is NOT a
turnkey script:

  * it expects the Drugs@FDA snapshot to be loaded into a dataframe, not a path;
  * the ChEMBL cross-reference step queries the EBI API live. Use
    validation/chembl_crosswalk.csv for exact reproduction;
  * the adjudication step calls a language model and is not deterministic across
    model versions. All 54 model-deciding and 41 hand-adjudicated outcomes are
    frozen in the `final_basis` column of the published table.

Five defects found after this code ran are corrected in the published tables but
NOT in this file, so that the record stays faithful to what was actually executed.
They are listed in docs/KNOWN_ISSUES.md under "found and fixed" and each carries a
`final_basis` string beginning "restored:" or "hand-adjudicated:" in the published
data. Anyone re-running this source will reproduce the pre-correction numbers
(1243 substances, not 1246).
"""

import json, re, os
import pandas as pd
import numpy as np
import requests
import concurrent.futures as cf

# Load raw data
raw = json.load(open('/Users/astevens/.claude-science/orgs/65b6af00-8713-49d7-be9a-f4694c1514f5/artifacts/proj_c83caf7e4580/9e8b5704-0b13-48ab-9acb-97f8778a5dc8/v790b2022_raw_nda_bla.json'))

# Load previously validated 2006-2025 classifications
OLD = pd.read_csv('/Users/astevens/.claude-science/orgs/65b6af00-8713-49d7-be9a-f4694c1514f5/artifacts/proj_c83caf7e4580/b6714639-709a-49f4-95c3-71881aabfcb6/v036ea935_fda_novel_approvals_classified.csv')

# Build submission dataframe
rows = []
for pref, recs in raw.items():
    for rec in recs:
        an = rec["application_number"]
        ings = set(); brands = set()
        for p in rec.get("products") or []:
            for ai in p.get("active_ingredients") or []:
                if ai.get("name"): ings.add(ai["name"].upper())
            if p.get("brand_name"): brands.add(p["brand_name"].upper())
        for s in rec.get("submissions") or []:
            rows.append(dict(app=an, pref=pref, sub_type=s.get("submission_type"),
                status=s.get("submission_status"), date=s.get("submission_status_date"),
                cls_desc=s.get("submission_class_code_description"),
                ingredients="|".join(sorted(ings)), brands="|".join(sorted(brands)),
                sponsor=(rec.get("sponsor_name") or "").upper()))

sub = pd.DataFrame(rows)
sub["date"] = pd.to_datetime(sub.date, errors="coerce")
sub["year"] = sub.date.dt.year
oa = sub[(sub.sub_type == "ORIG") & (sub.status == "AP")].copy()

RE_T1 = re.compile(r'Type\s*1\s*-\s*New Molecular Entity')

SALTS = ["HYDROCHLORIDE","HYDROBROMIDE","SULFATE","SULPHATE","SODIUM","POTASSIUM","CALCIUM","MAGNESIUM",
 "MESYLATE","MESILATE","TOSYLATE","BESYLATE","MALEATE","FUMARATE","TARTRATE","CITRATE","ACETATE",
 "PHOSPHATE","NITRATE","BROMIDE","CHLORIDE","IODIDE","OXALATE","SUCCINATE","LACTATE","GLUCONATE",
 "STEARATE","PALMITATE","PAMOATE","MALATE","ASPARTATE","GLUTAMATE","BENZOATE","SALICYLATE",
 "MONOHYDRATE","DIHYDRATE","TRIHYDRATE","HYDRATE","ANHYDROUS","HEMIHYDRATE","SESQUIHYDRATE",
 "DIHYDROCHLORIDE","MONOHYDROCHLORIDE","HCL","ARGININE","LYSINE","MEGLUMINE","TROMETHAMINE",
 "OLAMINE","DIOLAMINE","ETHANOLAMINE","CHOLINE","ZINC","ALUMINUM","BISMUTH SUBCITRATE",
 "PROTAMINE","RECOMBINANT","LAURYL","SORBITEX","XINAFOATE","EMBONATE","EDISYLATE","ISETHIONATE",
 "NAPSYLATE","TEOCLATE","VALERATE","PROPIONATE","DIPROPIONATE","ETABONATE","ETZADROXIL",
 "TRIFENATATE","SUBCITRATE","BITARTRATE","CARBONATE","BORATE","THIOCYANATE","SUCROFERRIC",
 "DISODIUM","HEMIFUMARATE","DIPHOSPHATE","ADIPATE","SUBSALICYLATE"]

RE_SALT = re.compile(r'\b(' + "|".join(sorted(SALTS, key=len, reverse=True)) + r')\b')

TYPO_FIX = {"ISLELIZUMAB": "TISLELIZUMAB", "AZELASTINE HYDROCHRLORIDE": "AZELASTINE",
            "CARBON DIOIDE": "CARBON DIOXIDE", "OMEGA 3ACID ETHYL ESTERS": "OMEGA 3 ACID ETHYL ESTERS"}

def norm3(name):
    n = str(name).strip().upper()
    n = re.sub(r'-[A-Z]{4}$', '', n)
    n = re.sub(r'\s*\(.*?\)\s*', ' ', n)
    n = RE_SALT.sub(' ', n)
    n = re.sub(r'[^A-Z0-9 ]', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    for k, v in TYPO_FIX.items():
        if n == k or n.startswith(k + " "): n = n.replace(k, v, 1)
    return n

def split3(s):
    if not isinstance(s, str): return []
    parts = []
    for chunk in re.split(r'\||,| AND ', s):
        c = norm3(chunk)
        if c and len(c) > 2: parts.append(c)
    return sorted(set(parts))

oa["moi"] = oa.ingredients.apply(split3)

fs = {}
for _, r in oa.sort_values(["date", "app"]).iterrows():
    for m in r["moi"]: fs.setdefault(m, r["year"])

HYAL = re.compile(r'HYALURONIDASE')
MANUAL_EXCLUDE = {"BLA761060": "Mylotarg 2017 re-approval; original 2000 BLA absent",
                  "BLA125291": "Lumizyme 2010 same moiety as Myozyme 2006"}
ADJUDICATED_IN = {"BLA125399", "BLA761440"}

appl = oa.sort_values(["date", "app"]).groupby("app", as_index=False).first()
grp = oa.groupby("app")
appl["cls_all"] = grp.cls_desc.apply(lambda s: " ; ".join(sorted(set(s.dropna())))).reindex(appl.app).values
appl["moi"] = grp.moi.apply(lambda s: sorted(set().union(*s))).reindex(appl.app).values
appl["is_t1"] = appl.cls_all.fillna("").str.contains(RE_T1)
appl = appl.sort_values(["date", "is_t1", "app"], ascending=[True, False, True])

EXCIPIENT = {
    "CETYL ALCOHOL", "TYLOXAPOL", "POLYSORBATE 80", "POLYSORBATE 20", "BENZYL ALCOHOL", "GLYCERIN",
    "MANNITOL", "SORBITOL", "POVIDONE", "EDETATE", "PHENOL", "PURIFIED WATER", "STARCH", "GELATIN",
    "SUCROSE", "LACTOSE", "DIMYRISTOYL LECITHIN", "DIPALMITOYLPHOSPHATIDYLCHOLINE", "HEXADECANOL",
    "SODIUM CHLORIDE", "DEXTROSE", "POLOXAMER 188", "TROMETHAMINE",
}
COFORMULANT = re.compile(r'HYALURONIDASE')

claimed = set(); rows2 = []
for _, r in appl.iterrows():
    new = [m for m in r["moi"] if fs.get(m) == r["year"] and m not in claimed]
    ther = [m for m in new if not COFORMULANT.search(m) and m not in EXCIPIENT]
    keep = (r["is_t1"] and bool(ther)) or (r["app"] in ADJUDICATED_IN)
    reason = None
    if keep and "Medical Gas" in (r["cls_all"] or ""): keep, reason = False, "medical gas"
    if r["app"] in MANUAL_EXCLUDE: keep, reason = False, MANUAL_EXCLUDE[r["app"]]
    if keep:
        claimed.update(new)
        rows2.append(dict(app=r["app"], pref=r["pref"], year=int(r["year"]), date=r["date"],
            new_moieties="|".join(ther) if ther else "|".join(r["moi"]), brands=r["brands"],
            sponsor=r["sponsor"], ingredients=r["ingredients"], cls=r["cls_all"],
            dropped="|".join([m for m in new if m not in ther])))
    else:
        claimed.update(new)

UNI = pd.DataFrame(rows2)
W = UNI[(UNI.year >= 1990) & (UNI.year <= 2025)].reset_index(drop=True)
M = W.assign(moiety=W.new_moieties.str.split("|")).explode("moiety")
M = M[M.moiety.notna() & (M.moiety.str.len() > 0)].reset_index(drop=True)

OLDMAP = OLD.set_index("moiety")

ADC_PAYLOAD = ["VEDOTIN", "DERUXTECAN", "EMTANSINE", "GOVITECAN", "OZOGAMICIN", "TESIRINE", "MAFODOTIN",
               "SORAVTANSINE", "PASUDOTOX", "EJETERAN", "TIRUMOTECAN", "NADOTOTUG", "BRIXAFUSP"]
AB_STEM = re.compile(r'(MAB|MAB [A-Z]+)$|(ZUMAB|XIMAB|MUMAB|OMAB|UMAB|XIZUMAB)$')
OLIGO = re.compile(r'(SEN|MERSEN|RSEN|VIRSEN|NUCLEOTIDE|SIRAN|GENE)$|MERSEN|^(NUSINERSEN|INOTERSEN|VOLANESORSEN|PATISIRAN|GIVOSIRAN|LUMASIRAN|INCLISIRAN|VUTRISIRAN|NEDOSIRAN|ETEPLIRSEN|GOLODIRSEN|VILTOLARSEN|CASIMERSEN|TOFERSEN|ELADOCAGENE|OLEZARSEN|DONIDALORSEN|FOMIVIRSEN|PEGAPTANIB|DEFIBROTIDE|MIPOMERSEN|IMETELSTAT|AVACINCAPTAD)$')
PEPT_SUF = re.compile(r'(TIDE|RELIN|ACTIDE|PRESSIN|TOCIN|CALCIN|GLUTIDE|ATIDE)$')
PROT_SUF = re.compile(r'(ASE|POETIN|STIM|TROPIN|KINASE|ERCEPT|MOD ALFA|ALFA|BETA|GAMMA|EPOETIN)$|\b(ALFA|BETA|GAMMA)\b')

CURATED = {
    "LANREOTIDE": "Peptide", "GALLIUM GA 68 EDOTREOTIDE": "Peptide", "GALLIUM GA 68 DOTATATE": "Peptide",
    "LUTETIUM LU 177 DOTATATE": "Peptide", "COPPER CU 64 DOTATATE": "Peptide", "ABALOPARATIDE": "Peptide",
    "TERIPARATIDE": "Peptide", "OCTREOTIDE": "Peptide", "PASIREOTIDE": "Peptide", "VAPREOTIDE": "Peptide",
    "DESMOPRESSIN": "Peptide", "CALCITONIN SALMON": "Peptide", "EPTIFIBATIDE": "Peptide",
    "BIVALIRUDIN": "Peptide", "ENFUVIRTIDE": "Peptide", "ZICONOTIDE": "Peptide", "PRAMLINTIDE": "Peptide",
    "NESIRITIDE": "Peptide", "EXENATIDE": "Peptide", "LIRAGLUTIDE": "Peptide", "SEMAGLUTIDE": "Peptide",
    "TIRZEPATIDE": "Peptide", "ICATIBANT": "Peptide", "LINACLOTIDE": "Peptide", "PLECANATIDE": "Peptide",
    "AFAMELANOTIDE": "Peptide", "SETMELANOTIDE": "Peptide", "BREMELANOTIDE": "Peptide",
    "ANGIOTENSIN II": "Peptide", "VASOPRESSIN": "Peptide", "OXYTOCIN": "Peptide", "CORTICORELIN": "Peptide",
    "SECRETIN": "Peptide", "GLUCAGON": "Peptide", "DASIGLUCAGON": "Peptide", "PEGCETACOPLAN": "Peptide",
    "CETRORELIX": "Peptide", "DEGARELIX": "Peptide", "NAFARELIN": "Peptide", "HISTRELIN": "Peptide",
    "GOSERELIN": "Peptide", "LEUPROLIDE": "Peptide", "TRIPTORELIN": "Peptide", "ATOSIBAN": "Peptide",
    "GALLIUM GA 68 GOZETOTIDE": "Small molecule", "LUTETIUM LU 177 VIPIVOTIDE TETRAXETAN": "Small molecule",
    "PIFLUFOLASTAT F 18": "Small molecule", "FLOTUFOLASTAT F 18": "Small molecule",
    "CASPOFUNGIN": "Small molecule", "MICAFUNGIN": "Small molecule", "ANIDULAFUNGIN": "Small molecule",
    "REZAFUNGIN": "Small molecule", "DAPTOMYCIN": "Small molecule", "ORITAVANCIN": "Small molecule",
    "DALBAVANCIN": "Small molecule", "TELAVANCIN": "Small molecule", "ROMIDEPSIN": "Small molecule",
    "CARFILZOMIB": "Small molecule", "BORTEZOMIB": "Small molecule", "IXAZOMIB": "Small molecule",
    "TELITHROMYCIN": "Small molecule", "TIGECYCLINE": "Small molecule", "ERAVACYCLINE": "Small molecule",
    "TECHNETIUM TC 99M TILMANOCEPT": "Other", "BRENSOCATIB": "Small molecule",
    "ETANERCEPT": "Protein/Enzyme", "ABATACEPT": "Protein/Enzyme", "BELATACEPT": "Protein/Enzyme",
    "AFLIBERCEPT": "Protein/Enzyme", "ZIV AFLIBERCEPT": "Protein/Enzyme", "RILONACEPT": "Protein/Enzyme",
    "ROMIPLOSTIM": "Protein/Enzyme", "EFGARTIGIMOD ALFA": "Protein/Enzyme", "LUSPATERCEPT": "Protein/Enzyme",
    "SOTATERCEPT": "Protein/Enzyme", "DULAGLUTIDE": "Protein/Enzyme", "ALBIGLUTIDE": "Protein/Enzyme",
    "OCRIPLASMIN": "Protein/Enzyme", "DORNASE ALFA": "Protein/Enzyme", "BECAPLERMIN": "Protein/Enzyme",
    "PEGADEMASE BOVINE": "Protein/Enzyme", "DENILEUKIN DIFTITOX": "Protein/Enzyme",
    "ALDESLEUKIN": "Protein/Enzyme", "OPRELVEKIN": "Protein/Enzyme", "PALIFERMIN": "Protein/Enzyme",
    "ANAKINRA": "Protein/Enzyme", "METRELEPTIN": "Protein/Enzyme", "PEGLOTICASE": "Protein/Enzyme",
    "RASBURICASE": "Protein/Enzyme", "AGALSIDASE BETA": "Protein/Enzyme", "LARONIDASE": "Protein/Enzyme",
    "DROTRECOGIN ALFA": "Protein/Enzyme", "TENECTEPLASE": "Protein/Enzyme", "RETEPLASE": "Protein/Enzyme",
    "ALTEPLASE": "Protein/Enzyme", "SOMATROPIN": "Protein/Enzyme", "SOMAPACITAN": "Protein/Enzyme",
    "PEGVISOMANT": "Protein/Enzyme", "MECASERMIN": "Protein/Enzyme", "THYROTROPIN ALFA": "Protein/Enzyme",
    "FOLLITROPIN ALFA": "Protein/Enzyme", "FOLLITROPIN BETA": "Protein/Enzyme", "LUTROPIN ALFA": "Protein/Enzyme",
    "CHORIOGONADOTROPIN ALFA": "Protein/Enzyme", "INSULIN GLARGINE": "Peptide", "INSULIN ASPART": "Peptide",
    "INSULIN LISPRO": "Peptide", "INSULIN DETEMIR": "Peptide", "INSULIN DEGLUDEC": "Peptide",
    "INSULIN GLULISINE": "Peptide", "INSULIN HUMAN": "Peptide", "INSULIN ICODEC": "Peptide",
    "BERACTANT": "Other", "CALFACTANT": "Other", "PORACTANT ALFA": "Other", "COLFOSCERIL": "Other",
    "ONABOTULINUMTOXINA": "Protein/Enzyme", "BOTULINUM TOXIN TYPE B": "Protein/Enzyme",
    "RIMABOTULINUMTOXINB": "Protein/Enzyme", "ABOBOTULINUMTOXINA": "Protein/Enzyme",
    "INCOBOTULINUMTOXINA": "Protein/Enzyme", "PRABOTULINUMTOXINA": "Protein/Enzyme",
    "DAXIBOTULINUMTOXINA": "Protein/Enzyme", "APROTININ": "Protein/Enzyme",
    "CORTICORELIN OVINE TRIFLUTATE": "Peptide", "MECASERMIN RINFABATE": "Protein/Enzyme",
}

def rule_classify(m):
    if m in CURATED: return CURATED[m], "curated lexicon"
    for p in ADC_PAYLOAD:
        if m.endswith(p) or (" " + p) in m: return "ADC", f"ADC payload stem '{p}'"
    if AB_STEM.search(m): return "Antibody", "antibody -mab stem"
    if OLIGO.search(m): return "Oligonucleotide", "oligonucleotide stem"
    if PEPT_SUF.search(m): return "Peptide", "peptide stem"
    if PROT_SUF.search(m): return "Protein/Enzyme", "protein/enzyme stem"
    return "Small molecule", "residual (no biologic stem)"

NEW = M[~M.moiety.isin(OLDMAP.index)].drop_duplicates("moiety").copy()
NEW["rule_class"], NEW["rule_evidence"] = zip(*NEW.moiety.map(rule_classify))

# ChEMBL lookup for new moieties
S = requests.Session()
BASE = "https://www.ebi.ac.uk/chembl/api/data/molecule.json"

def q3(m):
    for field in ("pref_name__iexact", "molecule_synonyms__molecule_synonym__iexact"):
        try:
            r = S.get(BASE, params={field: m, "limit": 1}, timeout=25)
            if r.ok:
                ms = r.json().get("molecules") or []
                if ms:
                    d = ms[0]
                    return m, d.get("molecule_chembl_id"), d.get("molecule_type"), d.get("first_approval"), field
        except Exception:
            pass
    return m, None, None, None, None

with cf.ThreadPoolExecutor(8) as ex:
    chres = list(ex.map(q3, NEW.moiety.tolist()))

CHN = pd.DataFrame(chres, columns=["moiety", "chembl_id", "chembl_type", "chembl_first_approval", "matched_on"])
NEW = NEW.merge(CHN, on="moiety", how="left")

CH_MAP = {"Small molecule": "Small molecule", "Antibody": "Antibody", "Protein": "Protein/Enzyme",
          "Enzyme": "Protein/Enzyme", "Oligonucleotide": "Oligonucleotide", "Oligosaccharide": "Other",
          "Cell": "Other", "Gene": "Other", "Unknown": None, None: None}
NEW["chembl_class"] = NEW.chembl_type.map(lambda t: CH_MAP.get(t))

both = NEW[NEW.chembl_class.notna()]
D_disc = both[both.rule_class != both.chembl_class].copy()

ORDER = ["Small molecule", "Antibody", "ADC", "Peptide", "Protein/Enzyme", "Oligonucleotide", "Other"]
VALID = set(ORDER)

SYS = ("You classify approved drug active substances into exactly one therapeutic modality. "
       "Allowed labels: Small molecule, Peptide, Protein/Enzyme, Antibody, ADC, Oligonucleotide, Other. "
       "Conventions: (a) chains under ~50 residues made by synthesis = Peptide, including insulins; "
       "(b) recombinant enzymes, cytokines, growth factors, Fc-fusion -cept proteins, toxins = Protein/Enzyme; "
       "(c) cyclic/nonribosomal peptide natural products used as conventional drugs (daptomycin, echinocandins, "
       "vancomycin-class, proteasome inhibitors) = Small molecule; (d) pulmonary surfactants and other complex "
       "biological mixtures with no single active moiety = Other; (e) radiolabelled peptide conjugates = Peptide "
       "only if the targeting vector is a genuine peptide chain. "
       "Reply with ONLY the label, nothing else.")

reqs = [dict(prompt=f"Active substance: {r.moiety}\nBrand: {(r.brands or '').split('|')[0]}\n"
                    f"US approval year: {int(r.year)}\nApplication type: {r.pref}\n"
                    f"Rule-engine says: {r.rule_class}. ChEMBL says: {r.chembl_class}.\nLabel:",
             system=SYS, model=host.reasoning_model(), max_tokens=12)
        for r in D_disc.itertuples()]
out_llm = host.llm(reqs, max_concurrency=8)

D_disc = D_disc.copy()
D_disc["llm_class"] = [(o.get("text", "").strip() if isinstance(o, dict) else "") for o in out_llm]
D_disc["llm_class"] = D_disc.llm_class.apply(lambda t: t if t in VALID else None)

retry = D_disc[D_disc.llm_class.isna()]
POLYSACC = {"ENOXAPARIN": "Other", "DALTEPARIN": "Other", "TINZAPARIN": "Other",
            "FONDAPARINUX": "Small molecule", "ACARBOSE": "Small molecule"}

if len(retry) > 0:
    rq = [dict(prompt=f"Active substance: {r.moiety}\nBrand: {(r.brands or '').split('|')[0]}\n"
                      f"US approval year: {int(r.year)}\nApplication type: {r.pref}\n"
                      f"Rule-engine says: {r.rule_class}. ChEMBL says: {r.chembl_class}.\nLabel:",
               system=SYS, model=host.reasoning_model(), max_tokens=300) for r in retry.itertuples()]
    ro = host.llm(rq, max_concurrency=6)
    fixed = {}
    for m, o in zip(retry.moiety, ro):
        t = (o.get("text", "") if isinstance(o, dict) else "").strip()
        lab = next((v for v in VALID if t == v), None) or next(
            (v for v in sorted(VALID, key=len, reverse=True) if v.lower() in t.lower()), None)
        fixed[m] = lab
    D_disc["llm_class"] = D_disc.apply(lambda r: fixed.get(r.moiety) or r.llm_class, axis=1)

D_disc["final_class"] = np.where(D_disc.moiety.isin(POLYSACC), D_disc.moiety.map(POLYSACC),
                         np.where(D_disc.llm_class == D_disc.rule_class, D_disc.rule_class,
                          np.where(D_disc.llm_class == D_disc.chembl_class, D_disc.chembl_class,
                                   D_disc.llm_class.fillna(D_disc.rule_class))))
D_disc["final_basis"] = np.where(D_disc.moiety.isin(POLYSACC), "hand-adjudicated (glycan)",
                         np.where(D_disc.llm_class == D_disc.rule_class, "rule+model (2 of 3)",
                          np.where(D_disc.llm_class == D_disc.chembl_class, "chembl+model (2 of 3)",
                                   "model tiebreak")))

NEW = NEW.set_index("moiety")
NEW["final_class"] = NEW.rule_class
NEW["final_basis"] = "rule+chembl concordant"
conc = NEW.index.isin(both[both.rule_class == both.chembl_class].moiety)
NEW.loc[~conc, "final_basis"] = "rule only (no ChEMBL match)"
NEW.loc[conc, "final_basis"] = "rule+chembl concordant"
for r in D_disc.itertuples():
    NEW.loc[r.moiety, ["final_class", "final_basis"]] = [r.final_class, r.final_basis]
NEW = NEW.reset_index()

CAR = M[M.moiety.isin(OLDMAP.index)].drop_duplicates("moiety").copy()
CAR["final_class"] = CAR.moiety.map(OLDMAP.final_class)
CAR["final_basis"] = "carried from validated 2006-2025 set"

keep = ["moiety", "app", "pref", "year", "date", "brands", "sponsor", "cls", "final_class", "final_basis"]
ALL = pd.concat([CAR[keep], NEW[keep]], ignore_index=True).sort_values(["year", "moiety"])

ALL_out = ALL.copy()
ALL_out["era_confidence"] = np.where(ALL_out.year < 2006, "lower", "validated")
ALL_out.to_csv("fda_novel_substances_1990_2025.csv", index=False)
print("Saved fda_novel_substances_1990_2025.csv with", len(ALL_out), "rows")