from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")
OUTFILE = PROCESSED_DIR / "position_value_summary_2016_2025.csv"

def main():
    frames = []
    for year in range(2016, 2026):  # 2016–2025
        f = PROCESSED_DIR / f"{year}_position_value_summary.csv"
        if not f.exists():
            raise FileNotFoundError(f"Missing processed file: {f}")

        df = pd.read_csv(f)

        # Normalize column names just in case
        df.columns = [c.strip() for c in df.columns]
        if "position" not in df.columns and "Position" in df.columns:
            df = df.rename(columns={"Position": "position"})

        df["year"] = year
        frames.append(df)

    all_df = pd.concat(frames, ignore_index=True)

    # Consistent column order (only keep what we need)
    keep = ["year", "position", "cumulative_value", "player_count", "avg_value_per_player"]
    all_df = all_df[keep]

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    all_df.to_csv(OUTFILE, index=False)
    print(f"Wrote {OUTFILE} ({len(all_df)} rows)")

if __name__ == "__main__":
    main()
