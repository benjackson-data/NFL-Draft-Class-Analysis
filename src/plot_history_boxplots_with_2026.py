from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HIST_FILE = Path("data/processed/position_value_summary_2016_2025.csv")
Y2026_FILE = Path("data/processed/2026_position_value_summary.csv")
OUTDIR = Path("reports")

EXCLUDE = {"K", "P", "LS"}

def main():
    hist = pd.read_csv(HIST_FILE)
    y26 = pd.read_csv(Y2026_FILE)

    # normalize column names
    hist.columns = [c.strip().lower() for c in hist.columns]
    y26.columns = [c.strip().lower() for c in y26.columns]

    # filter out specialists
    hist = hist[~hist["position"].isin(EXCLUDE)].copy()
    y26 = y26[~y26["position"].isin(EXCLUDE)].copy()

    # ensure we have the needed columns
    if "cumulative_value" not in hist.columns:
        raise ValueError("History file must have 'cumulative_value' column.")
    if "cumulative_value" not in y26.columns:
        raise ValueError("2026 file must have 'cumulative_value' column.")

    # Decide position order: sort by 2026 value
    pos_order = (
    y26.sort_values("cumulative_value", ascending=False)["position"]
    .tolist()
)


    # Build boxplot data (list of arrays in position order)
    box_data = [hist.loc[hist["position"] == p, "cumulative_value"].values for p in pos_order]

    # Map 2026 values for overlay (missing positions -> 0)
    y26_map = dict(zip(y26["position"], y26["cumulative_value"]))
    y26_vals = [y26_map.get(p, 0) for p in pos_order]

    OUTDIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 7))

    # Boxplot (matplotlib default styling)
    plt.boxplot(
        box_data,
        labels=pos_order,
        showfliers=True
    )

    # Overlay 2026 as dots
    x = list(range(1, len(pos_order) + 1))  # boxplot positions are 1-indexed
    plt.scatter(x, y26_vals, zorder=3, label="2026")

    plt.ylabel("Cumulative Rich Hill draft value (top picks cap by year)")
    plt.title("Position Strength Distribution (2016–2025) with 2026 Overlay")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    outpath = OUTDIR / "history_boxplots_with_2026_overlay.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()
