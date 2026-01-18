from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INFILE = Path("data/processed/2026_vs_history_position_zscores.csv")
OUTDIR = Path("reports")

def main():
    df = pd.read_csv(INFILE)

    # order strongest -> weakest
    df = df.sort_values("z_score", ascending=False)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 6))
    plt.bar(df["position"], df["z_score"])
    plt.axhline(0, linewidth=1)

    plt.ylabel("Z-score vs 2016–2025 (std devs from mean)")
    plt.title("2026 Draft Class Strength by Position (Standardized vs History)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    outpath = OUTDIR / "2026_position_strength_zscores.png"
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    main()
