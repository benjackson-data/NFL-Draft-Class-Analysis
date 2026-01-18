from pathlib import Path
import numpy as np
import pandas as pd

HIST_FILE = Path("data/processed/position_value_summary_2016_2025.csv")
Y2026_FILE = Path("data/processed/2026_position_value_summary.csv")
OUTDIR = Path("data/processed")

EXCLUDE = {"K", "P", "LS"}

def main():
    hist = pd.read_csv(HIST_FILE)
    y26 = pd.read_csv(Y2026_FILE)

    # normalize column names
    hist.columns = [c.strip().lower() for c in hist.columns]
    y26.columns = [c.strip().lower() for c in y26.columns]

    # safety: ensure column is 'position'
    if "position" not in y26.columns and "pos" in y26.columns:
        y26 = y26.rename(columns={"pos": "position"})

    hist = hist[~hist["position"].isin(EXCLUDE)].copy()
    y26 = y26[~y26["position"].isin(EXCLUDE)].copy()

    # baseline distribution across years for each position
    stats = (
        hist.groupby("position")["cumulative_value"]
        .agg(hist_mean="mean", hist_std="std", hist_min="min", hist_max="max", n_years="count")
        .reset_index()
    )

    y26 = y26[["position", "cumulative_value"]].rename(columns={"cumulative_value": "y2026"})

    merged = pd.merge(stats, y26, on="position", how="outer")

    # If a position is missing in 2026, treat as 0
    merged["y2026"] = merged["y2026"].fillna(0)

    # If std is 0 or NaN (shouldn't happen often), set z to 0 to avoid inf
    merged["hist_std"] = merged["hist_std"].replace(0, np.nan)
    merged["z_score"] = (merged["y2026"] - merged["hist_mean"]) / merged["hist_std"]
    merged["z_score"] = merged["z_score"].fillna(0)

    # nice extra columns
    merged["delta_vs_mean"] = merged["y2026"] - merged["hist_mean"]

    # sort by strongest vs history
    merged = merged.sort_values("z_score", ascending=False)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out_csv = OUTDIR / "2026_vs_history_position_zscores.csv"
    merged.to_csv(out_csv, index=False)
    print(f"Wrote: {out_csv}")

    # quick console view (top/bottom)
    print("\nTop 5 positions by z-score:")
    print(merged[["position", "y2026", "hist_mean", "hist_std", "z_score"]].head(5).to_string(index=False))

    print("\nBottom 5 positions by z-score:")
    print(merged[["position", "y2026", "hist_mean", "hist_std", "z_score"]].tail(5).to_string(index=False))

if __name__ == "__main__":
    main()
