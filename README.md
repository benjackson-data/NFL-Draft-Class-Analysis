# NFL Draft Class Position & Value Analysis

A data analytics project that aggregates and evaluates NFL draft classes over the last 10+ years, quantifying positional strength and visualizing historical trends. The project also tracks the 2026 class in real time using consensus pre-draft big boards.

---

## Motivation

Evaluating NFL draft classes is a complex task: multiple mock boards exist, player names and positions are inconsistent, and historical comparisons require standardization. Doing this manually is slow and error-prone.  

The goal of this project is to **automate the process**, provide clear insights into positional draft class strength, and create a framework for ongoing evaluation of future drafts.

---

## The Challenge

Key challenges included:

- **Inconsistent player names**: Jr./Sr. suffixes, nicknames, and spelling variations  
- **Duplicate names**: Multiple players sharing first + last names  
- **Position standardization**: EDGE vs DE, OT vs T, IOL vs G/C  
- **Data access**: Historical big boards and PFR data in multiple formats  
- **Automation**: Avoiding blocked redirects and scraping pitfalls  

---

## Approach / Solution

The project evolved in several iterations:

1. **Initial Approach**:  
   - Attempted direct searches on Pro-Football-Reference via Google Apps Script  
   - Encountered errors and blocked redirects → needed a more reliable source  

2. **Refinement 1**:  
   - Scraped **player index pages by last-name letter**  
   - Automated **position lookups** into Google Sheets while preserving existing data  
   - Added logging and error handling for reliability  

3. **Refinement 2**:  
   - Introduced **college validation** to resolve duplicates and flag mismatches  
   - Ensured higher accuracy for players with identical names  

4. **Draft Value Metrics**:  
   - Calculated **cumulative draft value** per position using Rich Hill’s trade value chart  
   - Counted **draft-worthy players** per position (capped by total draft picks per year)  
   - Computed **average draft value per player** (`cumulative ÷ # of players`)  

---

## Tech Stack & Skills

- **Google Sheets & Apps Script** for automation and data aggregation  
- **Regex & HTML parsing** for structured scraping  
- **Error handling & rate limiting** for robustness  
- **Data analysis**: aggregation, metrics, and basic statistics  
- **Visualization planning**: box-and-whisker plots for positional strength  

This project demonstrates **real-world data cleaning, automation, and iterative problem-solving** skills.

---

## Results (Current Status)

- Fully automated **historical position lookups** (~250 players per year)  
- Column E in Google Sheets populated with verified positions  
- College validation reduces mismatches and ensures accurate mapping  
- Draft value calculations completed for historical data  
- Ready to integrate the **2026 draft class** for ongoing updates  

---

## Next Steps

- Pull full consensus big boards for 2026 automatically  
- Map all historical positions to canonical positions (QB, RB, WR, TE, OT, IOL, DT, EDGE, LB, CB, S)  
- Generate visualizations:
  - **Box-and-whisker plots** for historical positional draft value ±1 SD  
  - Overlay 2026 class for comparative context  
- Implement **fuzzy name matching** for Jr./Sr./nickname variants  
- Optionally create an **interactive dashboard** for dynamic mock board updates  

---

## Example Output

| Player Name      | Your Pos | College   | Draft Yr | PFR Pos |
|-----------------|----------|-----------|----------|---------|
| Micah Parsons    | LB       | Penn St.  | 2021     | LB      |
| Tom Brady        | QB       | Michigan  | 2000     | QB      |
| Chase Young      | EDGE     | Ohio St.  | 2020     | EDGE    |
| Tristan Wirfs    | OT       | Iowa      | 2020     | OT      |

*Sample output from the position lookup and validation pipeline.*

---

## Visualization Concept (Planned)

- **Box-and-whisker plots** per position to show historical draft value spread  
- **Overlay 2026 class** for each position to provide context  
- Optional interactive charts to dynamically track changes as mocks update  

