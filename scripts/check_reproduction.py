#!/usr/bin/env python3
"""Post-execution gate for the reproducibility workflow.

Run from the repository root AFTER executing notebooks/01_reproduce_figures.ipynb.
Exits non-zero with a specific message on the first failure, so a red build says what
broke rather than just that something did.
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIGURES = [
    "approvals_by_modality_1990_2025.png",
    "approvals_by_modality_2006_2025.png",
    "approvals_withdrawals_mirror_1990_2025.png",
    "withdrawals_by_modality_1990_2025.png",
]
failures = []

checks = pd.read_csv(ROOT / "validation" / "validation_checks_approvals.csv")
bad = checks[checks["result"] != "PASS"]
if len(bad):
    failures.append(f"{len(bad)} validation check(s) not PASS: "
                    + "; ".join(bad["check"].astype(str)))
if len(checks) == 0:
    failures.append("validation_checks_approvals.csv is empty")

for name in FIGURES:
    p = ROOT / "figures" / name
    if not p.exists():
        failures.append(f"figure not regenerated: {name}")
    elif p.stat().st_size < 10_000:
        failures.append(f"figure suspiciously small ({p.stat().st_size} bytes): {name}")

recon = pd.read_csv(ROOT / "validation" / "reconciliation_vs_fda_published.csv")
r = recon["my_drug_count"].corr(recon["fda_published_novel"])
if not (r > 0.99):
    failures.append(f"reconciliation against FDA published counts degraded: r = {r:.4f}")
if int(recon["delta_drugs"].abs().max()) > 2:
    failures.append("a reconciliation year now differs from FDA's published count by "
                    f"more than 2 (max |delta| = {int(recon['delta_drugs'].abs().max())})")

sub = pd.read_csv(ROOT / "data" / "approvals_substance_level.csv")
if sub["moiety"].duplicated().any():
    failures.append("duplicate moieties in approvals_substance_level.csv")

if failures:
    print("REPRODUCTION CHECK FAILED")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print(f"REPRODUCTION CHECK PASSED - {len(checks)} validation checks, "
      f"{len(FIGURES)} figures, r = {r:.4f}, {len(sub)} substances")
