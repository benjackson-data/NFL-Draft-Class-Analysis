from pathlib import Path
import pandas as pd

def normalize_position(pos):
    if str(pos).strip().upper() == "DL":
        return "DT"
    return str(pos).strip().upper()

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
REF_DIR = REPO_ROOT / "data" / "reference"
OUT_DIR = REPO_ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def read_board(path: Path) -> pd.DataFrame:
    # Auto-detect delimiter (handles TSV pretending to be CSV)
    df = pd.read_csv(path, sep=None, engine="python")

    df["raw_position"] = df["Position"]
    df["Position"] = df["Position"].apply(normalize_position)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Expect these (based on your header)
    needed = {"rank", "player_name", "position", "college"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"{path.name}: missing columns {missing}. Found: {list(df.columns)}")

    # Basic cleanup
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
    df = df.dropna(subset=["rank"])
    df["rank"] = df["rank"].astype(int)

    for col in ["player_name", "position", "college"]:
        df[col] = df[col].astype(str).str.strip()

    return df

def main(year: int):
    # Reference: pick -> value
    values = pd.read_csv(REF_DIR / "rich_hill_values.csv")
    values.columns = [c.strip().lower() for c in values.columns]
    if not {"pick", "value"}.issubset(values.columns):
        raise ValueError("rich_hill_values.csv must have columns: pick,value")
    values["pick"] = pd.to_numeric(values["pick"], errors="coerce").astype("Int64")
    values["value"] = pd.to_numeric(values["value"], errors="coerce")

    # Reference: year -> total_picks
    picks_by_year = pd.read_csv(REF_DIR / "picks_by_year.csv")
    picks_by_year.columns = [c.strip().lower() for c in picks_by_year.columns]
    if not {"year", "total_picks"}.issubset(picks_by_year.columns):
        raise ValueError("picks_by_year.csv must have columns: year,total_picks")

    row = picks_by_year.loc[picks_by_year["year"] == year]
    if row.empty:
        raise ValueError(f"No total_picks entry for year={year} in picks_by_year.csv")
    total_picks = int(row["total_picks"].iloc[0])

    # Read board
    board_path = RAW_DIR / f"{year}.csv"
    board = read_board(board_path)

    # Cap to total picks for that year
    board = board.sort_values("rank").head(total_picks).copy()
    board["pick"] = board["rank"]

    # Join value
    merged = board.merge(values, on="pick", how="left")
    if merged["value"].isna().any():
        # Not fatal, but indicates your rich_hill_values table doesn't cover enough picks
        missing_picks = merged.loc[merged["value"].isna(), "pick"].unique()
        raise ValueError(
            f"Missing Rich Hill values for picks: {missing_picks[:10]} "
            f"(and {max(0, len(missing_picks)-10)} more). Extend rich_hill_values.csv."
        )

    # Aggregate by position (source position for now; later we map to canonical positions)
    summary = (merged
               .groupby("position", as_index=False)
               .agg(
                   cumulative_value=("value", "sum"),
                   player_count=("player_name", "count"),
               ))
    summary["avg_value_per_player"] = summary["cumulative_value"] / summary["player_count"]
    summary = summary.sort_values("cumulative_value", ascending=False)

    out_path = OUT_DIR / f"{year}_position_value_summary.csv"
    summary.to_csv(out_path, index=False)
    print(f"Wrote: {out_path}")
    print(summary.head(12).to_string(index=False))

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, required=True)
    args = p.parse_args()
    main(args.year)
