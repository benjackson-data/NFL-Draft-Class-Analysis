from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ZSCORES_FILE = Path("data/processed/2026_vs_history_position_zscores.csv")
OUTDIR = Path("reports")

CLIP_MIN, CLIP_MAX = -2.0, 2.0

# Color thresholds
GOOD_Z = 0.75
BAD_Z = -0.75

def z_to_color(z):
    if z >= GOOD_Z:
        return "#2ca02c"   # green
    elif z <= BAD_Z:
        return "#d62728"   # red
    else:
        return "#ffbf00"   # yellow (amber, easier on eyes than pure yellow)

def main():
    df = pd.read_csv(ZSCORES_FILE)
    df.columns = [c.strip().lower() for c in df.columns]

    # Sort by strength (max at 0° / east, CCW descending)
    df = df.sort_values("z_score", ascending=False)

    positions = df["position"].tolist()
    z = np.clip(df["z_score"].to_numpy(dtype=float), CLIP_MIN, CLIP_MAX)

    n = len(positions)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    angles_closed = np.append(angles, angles[0])
    values_closed = np.append(z, z[0])

    OUTDIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)

    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)

    # ---- Draw outer boundary thicker ----
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(theta, np.full_like(theta, CLIP_MAX), linewidth=2.5, color="black")

    # ---- Draw slightly bolded zero ring ----
    ax.plot(theta, np.zeros_like(theta), linewidth=1.6, color="black")

    # ---- Plot colored segments ----
    for i in range(n):
        a = [angles[i], angles[(i + 1) % n]]
        v = [z[i], z[(i + 1) % n]]
        color = z_to_color(z[i])
        ax.plot(a, v, linewidth=2.5, color=color)

    # ---- Fill polygon (neutral alpha so colors stay legible) ----
    ax.fill(angles_closed, values_closed, alpha=0.12, color="black")

    # ---- Scatter points for clarity ----
    for ang, val in zip(angles, z):
        ax.scatter(ang, val, s=45, color=z_to_color(val), zorder=3)

    # Labels
    ax.set_xticks(angles)
    ax.set_xticklabels(positions)

    ax.set_ylim(CLIP_MIN, CLIP_MAX)
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_yticklabels(["-2", "-1", "0", "+1", "+2"])

    ax.set_title(
        "2026 Draft Class Strength by Position\n(Z-scores vs 2016–2025)",
        pad=22
    )

    plt.tight_layout()
    outpath = OUTDIR / "2026_position_strength_radar_zscores.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()
