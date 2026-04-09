<h1>
<p align="center">
  <br> Is Gold Really the Safe Haven?
</p>
</h1>

<h4>
<p align="center"
<br> Global Precious Metals Trade and Inflation — An Interactive Data Story
</p>
</h4>

An interactive scrollytelling website exploring whether gold truly functions as an inflation hedge by analyzing physical trade flows of gold, silver, and platinum against country-level inflation data.

---

**Live app:** https://gold-flows.streamlit.app/
**Documentation:** https://vdss-fs26-ds25a.github.io/gruppe3/

---

## What This Project Does

When inflation rises, the advice is always the same: *buy gold*. But what actually happens to physical gold trade flows when inflation spikes? This project investigates:

1. Where does gold flow during high-inflation periods — and do those flows change direction?
2. Do high-inflation countries consistently import more gold?
3. Is gold special, or do silver and platinum show the same patterns?
4. What role does Switzerland play as a refining hub during global economic stress?
5. Which type of inflation — food, energy, or core CPI — has the strongest link to gold trade activity?

The final product is a 5-chapter Streamlit scrollytelling app with interactive charts (choropleth map, scatter plot, grouped bar chart, Sankey diagram, and summary metric cards).

---

## Data Sources

| Dataset | Source | Coverage |
|---|---|---|
| UN Global Commodity Trade Statistics | Kaggle (filtered to HS codes 7106–7112) | 1988–2016, ~10,000–50,000 rows after filtering |
| World Bank Global Inflation Database | Ha, Kose & Ohnsorge (2023) | 1970–2025, 209 countries × 6 inflation types |

---

## Project Structure

```
gruppe3/
├── data/              # Raw and processed datasets
│   ├── raw/
│   └── processed/
├── eda/               # Exploratory data analysis scripts
├── deployment/        # Streamlit app (app.py)
├── evaluation/        # Evaluation artefacts
├── viz_design/        # Visual encoding and design explorations
└── docs/              # Quarto documentation website
    ├── project_charta.qmd
    ├── data_report.qmd
    ├── viz_design_report.qmd
    ├── evaluation.qmd
    └── deployment.qmd
```

---

## Setup

**Requirements:** [uv](https://docs.astral.sh/uv/getting-started/installation/), [Quarto](https://quarto.org/docs/get-started/)

```bash
# Clone the repo and install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run deployment/app.py

# Preview the documentation website
cd docs && uv run quarto preview
```

To add or remove packages:
```bash
uv add <package>
uv remove <package>
```

---

## Documentation (Quarto)

Source files are in `docs/`. To build and deploy:

```bash
cd docs
uv run quarto render    # builds to docs/build/, updates docs/_freeze
```

The documentation is deployed to GitHub Pages via GitHub Actions on every push to `main`. Python computations are cached in `docs/_freeze` (checked in), so the Actions runner does not need Python.

**Initial setup (once):** Go to **Settings > Pages** in the GitHub repo and set the source to **GitHub Actions**.

---

## Team

| Name | Role | Contact |
|---|---|---|
| Valentin Schwarz | Data Engineering — pipeline, repo structure | vschwarz@ik.me |
| Aisosa Omokaro | App Infrastructure — inflation data, Streamlit deployment | aisosashina@gmail.com |
| Thiveja Thirukumar | Documentation — research, data report, project charter | thiveja.thirukumar@gmail.com |

---

## License

See [LICENSE](LICENSE).
