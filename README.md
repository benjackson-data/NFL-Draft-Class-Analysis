# NFL Draft Class Strength by Position (2016–2026)

## Overview

This project answers a simple but often hand-waved question:

> **How strong is a given NFL draft class by position (QB, WR, EDGE, etc.) compared to history?**

Rather than relying on narrative or isolated prospect rankings, this analysis uses **draft capital as revealed preference** — how teams actually value positions in aggregate — and compares each draft class to historical baselines.

The primary focus is on evaluating the **2026 draft class** in context, using drafts from **2016–2025** as the historical reference window.

---

## Core Idea

A draft class can be “strong” at a position in two different ways:

- **Elite talent at the top** (high-value early picks)
- **Depth throughout the draft** (many draftable players accumulating value)

This project captures *both* by aggregating **Rich Hill draft value** across positions and standardizing results relative to history.

---

## Data Sources

- **Consensus Big Boards (2016–2026)**  
  Used to rank prospects consistently across years.

- **Rich Hill Draft Value Chart**  
  Converts draft pick numbers into comparable numeric value.

- **Per-year total draft pick counts**  
  Ensures each class is capped consistently based on how many players were actually drafted.

---

## Data Availability

Raw consensus big board files are not included in this repository, as they were sourced from a premium subscription service. All analyses are fully reproducible using equivalent publicly available rankings or user-provided big board data following the same schema.

---

## Methodology (High Level)

For each draft year:

1. Read the consensus big board
2. Cap the board to that year’s total draft picks
3. Map rank → pick → Rich Hill value
4. Aggregate by position:
   - cumulative draft value
   - number of players
   - average value per player

For historical comparison (2016–2025):

5. Build per-position distributions of cumulative value
6. Compute historical mean and standard deviation
7. Score the 2026 class using **z-scores**:
   - how many standard deviations above or below historical average

---

## Position Normalization

- Consensus big boards label some prospects as **DL**
- For consistency, **DL is treated as DT**
- All other position labels are passed through unchanged

This preserves **draft-era positional intent** rather than reclassifying players based on NFL usage, which would introduce hindsight bias.

---

## Key Findings (2026 Draft Class)

### Strongest Positions (vs history)
- **EDGE**
- **WR**
- **LB**

These positions are not just strong in absolute terms — they are **meaningfully above historical norms**, indicating either premium talent, unusual depth, or both.

### Weakest Positions (vs history)
- **RB**
- **QB**
- **IOL**  
  *(DT is also below average, though not as extreme)*

While the 2026 class includes a projected top-of-the-draft quarterback and another potential first-round selection, it remains below historical averages in cumulative draft value. This reflects a **top-heavy quarterback class** rather than one defined by depth, with fewer draftable QBs contributing value beyond the early rounds.

---

## Visualizations

The project includes multiple complementary views of the same underlying data:

- **Bar charts** comparing 2026 vs historical averages
- **Boxplots** showing historical distributions with 2026 overlaid
- **Radar chart (z-scores)** summarizing positional strengths and weaknesses at a glance

The radar chart uses:
- standardized z-scores
- capped ranges for readability
- semantic color coding:
  - green = strong vs history
  - yellow = near average
  - red = weak vs history

---

## Why This Approach Works

- Uses **draft capital**, not opinion, as the valuation signal
- Separates **depth** from top-heavy hype
- Controls for positional inflation and deflation over time
- Makes historical context explicit rather than implied

---

## Limitations & Design Choices

- Positions reflect **pre-draft evaluation**, not NFL career outcomes
- DL → DT normalization simplifies older board conventions
- Results describe **class composition**, not individual player success
- Rich Hill values approximate draft behavior, not surplus value

These tradeoffs are intentional and documented to preserve analytical clarity and reproducibility.

---

## Project Structure

```text
nfl-draft-analytics/
  data/
    raw/            # consensus big boards (2016–2026)
    reference/      # draft value charts, pick counts
    processed/      # per-year + historical summaries
  src/
    make_position_summary.py
    combine_position_summaries.py
    score_2026_vs_history.py
    plot_*.py
  reports/
    *.png           # generated charts

```
---

## Possible Extensions

- Position-by-position time series trends
- Alternative draft value models
- NFL outcome overlays (snap counts, WAR, PFF grades)
- Team-level exploitation of strong/weak positional classes

---

## Bottom Line

This project provides a **transparent, repeatable way** to evaluate how and why a draft class is strong or weak at specific positions, grounding conclusions in explicit historical context rather than subjective narrative.
