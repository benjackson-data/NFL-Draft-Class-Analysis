from pathlib import Path
import pandas as pd

OLD_FILE = Path("data/processed/2026_position_value_summary_prev.csv")
NEW_FILE = Path("data/processed/2026_position_value_summary.csv")
OUT_FILE = Path("data/processed/2026_position_value_movement.csv")

EXCLUDE = {"K", "P", "LS"}

def prep(df):
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    if "pos" in df.columns and "position" not in df.columns:
        df = df.rename(columns={"pos": "position"})
    df["position"] = df["position"].astype(str).str.strip().str.upper()
    df = df[~df["position"].isin(EXCLUDE)].copy()
    return df

def main():
    old = prep(pd.read_csv(OLD_FILE))
    new = prep(pd.read_csv(NEW_FILE))

    old = old[["position", "cumulative_value", "player_count"]].rename(
        columns={
            "cumulative_value": "old_value",
            "player_count": "old_count"
        }
    )

    new = new[["position", "cumulative_value", "player_count"]].rename(
        columns={
            "cumulative_value": "new_value",
            "player_count": "new_count"
        }
    )

    merged = old.merge(new, on="position", how="outer").fillna(0)

    merged["value_change"] = merged["new_value"] - merged["old_value"]
    merged["count_change"] = merged["new_count"] - merged["old_count"]

    merged = merged.sort_values("value_change", ascending=False).reset_index(drop=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_FILE, index=False)

    print(f"Saved: {OUT_FILE}")
    print(merged.to_string(index=False))

if __name__ == "__main__":
    main()