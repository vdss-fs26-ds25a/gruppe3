# Aisosa — Project Notes

## Phase 1 (until 13. April)
- [x] Download World Bank Inflation Excel and push to repo
- [x] Reshape inflation data with pd.melt() from wide to long
- [x] Background research: Geopolitics and Gold, BRICS vs. Dollar

## Phase 2 (14.–20. April)

### 16. April 2026
- [x] Git pull, created branch `aisosa/eda`
- [x] Data quality analysis (`eda/aisosa_eda.ipynb`)

#### Key Findings
- Dataset: 83765 rows, 12 columns, 198 countries, 1988–2016
- Missing values: weight_kg 5.6%, Headline CPI 19.6%, Core CPI 46.9%
- Outliers: 2779 entries under $100, 16765 entries with weight_kg = 0
- **Switzerland only has Silver data → problem for Chapter 4 Sankey**
- **Dataset ends 2016 → 2022 inflation wave not covered**
- Gold dominates trade value with $3.8 trillion

## TODO
- [ ] Tell team about Switzerland problem
- [ ] Bar Chart: Gold vs. Silver vs. Platinum (Chapter 3)
- [ ] Sankey diagram Switzerland (Chapter 4) — needs new data source?