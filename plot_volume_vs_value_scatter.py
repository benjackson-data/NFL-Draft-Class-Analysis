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

    # filter specialists
    hist = hist[~hist["position"].isin(EXCLUDE)].copy()
    y26 = y26[~y26["position"].isin(EXCLUDE)].copy()

    OUTDIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 7))
    ax = plt.gca()

    # ---- historical (2016–2025): faded ----
    for pos, g in hist.groupby("position"):
        ax.scatter(
            g["player_count"],
            g["cumulative_value"],
            alpha=0.25,
            s=40,
            label=pos
        )

    # ---- 2026: bold ----
    for _, r in y26.iterrows():
        ax.scatter(
            r["player_count"],
            r["cumulative_value"],
            s=120,
            edgecolors="black",
            linewidths=1.2,
            zorder=3
        )
        # label each 2026 point by position
        ax.annotate(
            r["position"],
            (r["player_count"], r["cumulative_value"]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9,
            weight="bold"
        )

    ax.set_xlabel("Number of draftable prospects (player count)")
    ax.set_ylabel("Cumulative Rich Hill draft value")
    ax.set_title("Draft Volume vs Draft Capital by Position\n(2016–2025 faded, 2026 highlighted)")

    # clean legend: one entry per position (from historical)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title="Position", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    outpath = OUTDIR / "volume_vs_value_scatter_2026_highlighted.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()
