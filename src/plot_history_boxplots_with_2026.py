from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HIST_FILE = Path("data/processed/position_value_summary_2016_2025.csv")
Y2026_FILE = Path("data/processed/2026_position_value_summary.csv")
PREV_FILE = Path("data/processed/2026_position_value_summary_prev.csv")
OUTDIR = Path("reports")

EXCLUDE = {"K", "P", "LS"}

def main():
    hist = pd.read_csv(HIST_FILE)
    y26 = pd.read_csv(Y2026_FILE)
    prev = pd.read_csv(PREV_FILE)

    # Normalize column names
    hist.columns = [c.strip().lower() for c in hist.columns]
    y26.columns = [c.strip().lower() for c in y26.columns]
    prev.columns = [c.strip().lower() for c in prev.columns]

    # Filter out specialists
    hist = hist[~hist["position"].isin(EXCLUDE)].copy()
    y26 = y26[~y26["position"].isin(EXCLUDE)].copy()
    prev = prev[~prev["position"].isin(EXCLUDE)].copy()

    # Ensure needed columns exist
    if "cumulative_value" not in hist.columns:
        raise ValueError("History file must have 'cumulative_value' column.")
    if "cumulative_value" not in y26.columns:
        raise ValueError("2026 file must have 'cumulative_value' column.")
    if "cumulative_value" not in prev.columns:
        raise ValueError("Previous 2026 file must have 'cumulative_value' column.")
    if "player_count" not in y26.columns:
        raise ValueError("2026 file must have 'player_count' column.")
    if "player_count" not in prev.columns:
        raise ValueError("Previous 2026 file must have 'player_count' column.")

    # Sort positions by current 2026 cumulative value
    pos_order = (
        y26.sort_values("cumulative_value", ascending=False)["position"]
        .tolist()
    )

    # Keep only positions that exist in history
    pos_order = [p for p in pos_order if (hist["position"] == p).any()]

    # Build boxplot data
    box_data = [
        hist.loc[hist["position"] == p, "cumulative_value"].values
        for p in pos_order
    ]

    # Value maps
    y26_map = dict(zip(y26["position"], y26["cumulative_value"]))
    prev_map = dict(zip(prev["position"], prev["cumulative_value"]))

    y26_vals = [y26_map.get(p, 0) for p in pos_order]
    prev_vals = [prev_map.get(p, 0) for p in pos_order]
    deltas = [y26_map.get(p, 0) - prev_map.get(p, 0) for p in pos_order]

    # Count maps
    y26_count_map = dict(zip(y26["position"], y26["player_count"]))
    prev_count_map = dict(zip(prev["position"], prev["player_count"]))
    count_deltas = [y26_count_map.get(p, 0) - prev_count_map.get(p, 0) for p in pos_order]

    OUTDIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 7))

    plt.boxplot(
        box_data,
        tick_labels=pos_order,
        showfliers=True
    )

    x = list(range(1, len(pos_order) + 1))  # boxplot positions are 1-indexed

    # Previous 2026 overlay
    plt.scatter(x, prev_vals, zorder=3, label="Previous 2026", marker="x")

    # Current 2026 overlay
    plt.scatter(x, y26_vals, zorder=4, label="Current 2026")

    # Split labels: value delta and count delta colored separately
    for xi, yi, d, cd in zip(x, y26_vals, deltas, count_deltas):
        if d > 0:
            value_color = "green"
        elif d < 0:
            value_color = "red"
        else:
            value_color = "black"

        if cd > 0:
            count_color = "green"
        elif cd < 0:
            count_color = "red"
        else:
            count_color = "black"

        # Value change
        plt.annotate(
            f"{d:+.0f}",
            (xi, yi),
            textcoords="offset points",
            xytext=(22, 0),
            ha="left",
            va="center",
            fontsize=8,
            color=value_color
        )

        # Count change
        plt.annotate(
            f" ({cd:+d})",
            (xi, yi),
            textcoords="offset points",
            xytext=(42, 0),
            ha="left",
            va="center",
            fontsize=8,
            color=count_color
        )

    plt.ylabel("Cumulative Rich Hill draft value (top picks cap by year)")
    plt.title("Position Strength Distribution (2016–2025) with 2026 Movement Overlay")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    outpath = OUTDIR / "history_boxplots_with_2026_movement.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()