# How Strong Is This Draft Class?  
### A Position-by-Position NFL Draft Analysis

This project answers a simple question:

> **“How good is this year’s group of QBs, WRs, EDGE rushers, etc., compared to other draft classes?”**

To do that, it builds a visual, data-driven comparison of NFL draft classes by position using historical consensus big boards and draft value modeling.

---

## The Core Idea (TL;DR)

Every draft class has strengths and weaknesses by position.

Some years are:
- QB-heavy
- Deep at WR
- Weak at OT
- Loaded with defensive linemen

This project quantifies that by:
1. Taking **consensus pre-draft rankings**
2. Converting rankings into **draft pick value**
3. Summing that value **by position**
4. Comparing each position group to history

The result:  
👉 A clear picture of **which positions are strong or weak in a given draft class**, including the upcoming **2026 NFL Draft**.

---

## What “Strength” Means Here

For each position (QB, WR, EDGE, etc.), the project calculates:

### 1. Cumulative Draft Value (most important)
- How much total draft capital exists at that position in a given year
- Answers: *“How much value is there overall?”*

### 2. Number of Draft-Worthy Players
- How many players at that position appear within the total number of draft picks that year
- Answers: *“Is this position deep?”*

### 3. Average Draft Value per Player
- Cumulative value ÷ number of players
- Answers: *“Is this top-heavy or evenly strong?”*

---

## Why This Is Useful

This framework helps answer questions like:
- “Is this a good year to need a quarterback?”
- “Should teams prioritize WR in this draft?”
- “Is this EDGE class unusually strong or just average?”
- “How does the 2026 class compare to the last 10 years?”

It’s designed to support **contextual, comparative draft evaluation**, not hot takes.

---

## Data & Method (High Level)

- Uses **consensus big boards** to reduce individual evaluator bias
- Converts rank → draft pick → draft value (Rich Hill chart)
- Caps each year to the **actual number of draft picks**
- Aggregates value by position
- Visualizes each position against historical baselines
- Consensus big boards list DL; these are treated as DT for analysis.

Raw ranking data is not redistributed; the focus is on **derived metrics and visual analysis**.

---

## Current Status

- Historical boards (2016–2025) prepared locally
- Reference draft value tables committed
- First aggregation scripts in progress
- Visualization design underway
- 2026 class will be tracked dynamically as rankings change

---

## End Goal

A simple, repeatable way to generate a report like:

> “Here’s how strong the 2026 QB class is compared to the last decade.”

With charts that make the answer obvious at a glance.
