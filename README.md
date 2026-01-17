# NFL Draft Class Visual Analysis (Positional Strength Tracker)

This project builds a **visual, position-by-position analysis of NFL draft class strength** using historical consensus big boards (10+ years) and draft value modeling. The end goal is a set of clear visuals that let you compare any upcoming class (starting with **2026**) against historical context as the consensus board changes over time.

> Note: A small supporting component of this project is position/college standardization (e.g., using Pro-Football-Reference labels) to make historical comparisons consistent. The visuals and draft class evaluation are the primary objective.

---

## Goal

Create an analytics workflow that:

- Ingests **pre-draft consensus big boards** by year (historical + ongoing 2026 updates)
- Standardizes players into canonical positions:
  **QB, RB, WR, TE, OT, IOL, DT, EDGE, LB, CB, S**
- Converts board rank → **draft pick** (capped to total picks in that year)
- Applies a **draft value chart** (Rich Hill baseline; may compare alternatives)
- Produces visuals that communicate **positional strength** across years and for 2026 in context

---

## Core Metrics (per position, per year)

1. **Cumulative Draft Value** (primary)
   - Sum of pick-values for the top N “draft-worthy” players at a position (N capped by total picks that year)

2. **# Draft-Worthy Players**
   - Count of players at that position within the top N overall players for that year (N = total draft picks)

3. **Average Draft Value per Player**
   - `Cumulative Draft Value ÷ # Draft-Worthy Players`

Working theory: **cumulative value** best captures “how strong is this position group overall?”

---

## Visualization Plan

Primary idea (initial prototype):

- For each position:
  - Show historical distribution (e.g., **box-and-whisker** or similar)
  - Include **mean** and a variability indicator (e.g., ±1 standard deviation or quartiles)
  - Overlay the **2026** class value as a point/marker as it evolves

This may evolve into clearer visuals (e.g., rank-ordered bars, ridgeline distributions, or small multiples) depending on readability.

---

## Supporting Pipeline Work (Secondary)

To make historical comparisons reliable, the project includes automation and validation steps such as:

- Standardizing position labels across sources (e.g., DE vs EDGE, OT vs T, IOL vs G/C)
- Handling naming inconsistencies (Jr./Sr., nicknames, punctuation)
- Disambiguating duplicate names using college as a tiebreaker
- Rate limiting + error handling for reliable enrichment workflows

---

## Approach / Iterations So Far

1. **Automation prototyping**
   - Early attempts at direct lookups ran into redirect/method limitations in Apps Script.

2. **Reliable enrichment**
   - Switched to Pro-Football-Reference player index pages to support repeatable position lookups in Google Sheets while preserving original data.

3. **Accuracy improvements**
   - Added college-based validation to reduce mis-matches and handle same-name collisions.

These steps support the bigger goal: **clean, consistent historical datasets to power the draft class visuals.**

---

## Tech Stack

- Google Sheets & Apps Script (automation + enrichment)
- Regex & HTML parsing
- Data aggregation + custom metric modeling
- Visualization tooling planned (Python/Plotly/matplotlib or Google-native charts)

---

## Status

- Position enrichment workflow working and scalable to a full draft class size (250–265)
- Historical big board ingestion is the next major automation piece
- Draft value modeling and visuals are the primary deliverables in progress

---

## Next Steps

- Automate importing consensus big boards for 10+ years and ongoing 2026 snapshots
- Canonical position mapping (QB/RB/WR/TE/OT/IOL/DT/EDGE/LB/CB/S)
- Implement Rich Hill value mapping and compute yearly positional metrics
- Build the first visualization set and iterate for clarity
- Add fuzzy matching for name variants and better duplicate handling
