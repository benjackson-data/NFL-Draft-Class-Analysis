from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ZSCORES_FILE = Path("data/processed/2026_vs_history_position_zscores.csv")
OUTDIR = Path("reports")

CLIP_MIN, CLIP_MAX = -1.5, 2.5

# Old fixed thresholds, kept only for comparison in console output
OLD_GOOD_Z = 0.75
OLD_BAD_Z = -0.75


def bucket_from_cutoffs(z, low_cutoff, high_cutoff):
    if z >= high_cutoff:
        return "good"
    elif z <= low_cutoff:
        return "bad"
    return "mid"


def z_to_color(z, low_cutoff, high_cutoff):
    bucket = bucket_from_cutoffs(z, low_cutoff, high_cutoff)
    if bucket == "good":
        return "#2ca02c"   # green
    elif bucket == "bad":
        return "#d62728"   # red
    return "#ffbf00"       # amber


def format_z(z):
    return f"{z:+.2f}"


def main():
    df = pd.read_csv(ZSCORES_FILE)
    df.columns = [c.strip().lower() for c in df.columns]

    # Sort by strength
    df = df.sort_values("z_score", ascending=False).reset_index(drop=True)

    positions = df["position"].tolist()
    raw_z = df["z_score"].to_numpy(dtype=float)
    z_plot = np.clip(raw_z, CLIP_MIN, CLIP_MAX)

    # Dynamic thresholds based on current 2026 position z-score distribution
    # Using population std since this is the full current set of positions, not a sample.
    mean_z = float(np.mean(raw_z))
    sd_z = float(np.std(raw_z, ddof=0))

    high_cutoff = mean_z + sd_z
    low_cutoff = mean_z - sd_z

    # Compare old vs new coloring logic
    old_buckets = [bucket_from_cutoffs(z, OLD_BAD_Z, OLD_GOOD_Z) for z in raw_z]
    new_buckets = [bucket_from_cutoffs(z, low_cutoff, high_cutoff) for z in raw_z]
    changed_positions = [p for p, old, new in zip(positions, old_buckets, new_buckets) if old != new]

    print(f"Mean z-score across positions: {mean_z:.4f}")
    print(f"Population std dev of z-scores: {sd_z:.4f}")
    print(f"Dynamic cutoffs -> red <= {low_cutoff:.4f}, green >= {high_cutoff:.4f}")
    print(f"Old fixed cutoffs -> red <= {OLD_BAD_Z:.2f}, green >= {OLD_GOOD_Z:.2f}")

    if changed_positions:
        print("Positions whose color bucket changed vs fixed +/-0.75:")
        print(", ".join(changed_positions))
    else:
        print("Dynamic cutoffs do not change any color buckets vs fixed +/-0.75.")

    n = len(positions)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)

    OUTDIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8.5, 8.5))
    ax = plt.subplot(111, polar=True)

    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)

    # Outer boundary
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(theta, np.full_like(theta, CLIP_MAX), linewidth=2.0, color="black")

    # Zero ring
    ax.plot(theta, np.zeros_like(theta), linewidth=1.4, color="black")

    # Light neutral open line (does not close QB back to LB)
    ax.plot(angles, z_plot, linewidth=1.5, color="gray", alpha=0.8)

    # Colored points
    point_colors = [z_to_color(z, low_cutoff, high_cutoff) for z in raw_z]
    for ang, val, color in zip(angles, z_plot, point_colors):
        ax.scatter(ang, val, s=60, color=color, zorder=3)

    # Axis labels
    ax.set_xticks(angles)
    ax.set_xticklabels(positions, fontsize=10)

    ax.set_ylim(CLIP_MIN, CLIP_MAX)
    ax.set_yticks([-1.5, -1, 0, 1, 2, 2.5])
    ax.set_yticklabels(["-1.5", "-1", "0", "+1", "+2", "+2.5"], fontsize=9)

    # Custom z-score label placement by position
    # values are: (x offset, y offset, horizontalalignment, verticalalignment)
    label_offsets = {
        "LB":   (0, -12, "center", "top"),
        "WR":   (0, 8,   "center", "bottom"),
        "S":    (0, 8,   "center", "bottom"),
        "OT":   (0, 8,   "center", "bottom"),
        "EDGE": (-8, 8,  "right",  "bottom"),
        "TE":   (-8, 0,  "right",  "center"),
        "RB":   (-8, 0,  "right",  "center"),
        "IOL":  (0, -12, "center", "top"),
        "CB":   (0, -12, "center", "top"),
        "DT":   (0, -12, "center", "top"),
        "QB":   (-8, 0,  "right",  "center"),
    }

    # Add numeric z-score labels near points
    for pos, ang, raw_val, plot_val, color in zip(positions, angles, raw_z, z_plot, point_colors):
        dx, dy, ha, va = label_offsets.get(pos, (0, 8, "center", "bottom"))
        ax.annotate(
            format_z(raw_val),
            (ang, plot_val),
            textcoords="offset points",
            xytext=(dx, dy),
            ha=ha,
            va=va,
            fontsize=9,
            color=color
        )

    ax.set_title(
        "2026 Draft Class Strength by Position\n(Z-scores vs 2016–2025)",
        pad=24
    )

    plt.tight_layout()
    outpath = OUTDIR / "2026_position_strength_radar_zscores.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main()