from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HIST_FILE = Path("data/processed/position_value_summary_2016_2025.csv")
Y2026_FILE = Path("data/processed/2026_position_value_summary.csv")
OUTDIR = Path("reports")

# keep your main buckets; exclude specialists by default
EXCLUDE = {"K", "P", "LS"}

def main():
    hist = pd.read_csv(HIST_FILE)
    y26 = pd.read_csv(Y2026_FILE)

    # Normalize col names
    hist.columns = [c.strip().lower() for c in hist.columns]
    y26.columns = [c.strip().lower() for c in y26.columns]

    if "position" not in y26.columns and "pos" in y26.columns:
        y26 = y26.rename(columns={"pos": "position"})

    # Filter
    hist = hist[~hist["position"].isin(EXCLUDE)]
    y26 = y26[~y26["position"].isin(EXCLUDE)]

    # Historical baseline: mean cumulative value by position (2016–2025)
    baseline = (
        hist.groupby("position", as_index=False)["cumulative_value"]
        .mean()
        .rename(columns={"cumulative_value": "hist_mean"})
    )

    # 2026 actuals
    y26 = y26[["position", "cumulative_value"]].rename(columns={"cumulative_value": "y2026"})

    # Merge and fill missing with 0 (in case a position doesn't appear)
    merged = pd.merge(baseline, y26, on="position", how="outer").fillna(0)

    # Sort by 2026 value (most readable)
    merged = merged.sort_values("y2026", ascending=False)

    # Plot: two bars per position
    OUTDIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 6))
    x = range(len(merged))

    plt.bar([i - 0.2 for i in x], merged["hist_mean"], width=0.4, label="2016–2025 mean")
    plt.bar([i + 0.2 for i in x], merged["y2026"], width=0.4, label="2026")

    plt.xticks(list(x), merged["position"], rotation=45, ha="right")
    plt.ylabel("Cumulative Rich Hill draft value")
    plt.title("2026 Draft Class Strength by Position vs 2016–2025 Average")
    plt.legend()
    plt.tight_layout()

    outpath = OUTDIR / "2026_vs_history_mean_cumulative_value_by_position.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()
