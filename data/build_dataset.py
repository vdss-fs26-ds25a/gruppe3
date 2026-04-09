import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data_acquisition"
OUT = ROOT / "data_acquisition"
OUT.mkdir(exist_ok=True)

PRECIOUS_KEYWORDS = [
    "Gold",
    "Silver",
    "Platinum",
    "Precious metal",
    "precious metal",
]

trade_raw = pd.read_csv(RAW / "commodity_trade_statistics_data.csv", low_memory=False)

mask = trade_raw["commodity"].str.contains(
    "|".join(PRECIOUS_KEYWORDS), case=False, na=False
)
trade = trade_raw[mask].copy()

def classify_metal(commodity: str) -> str:
    c = commodity.lower()
    if "gold" in c:
        return "Gold"
    if "silver" in c:
        return "Silver"
    if "platinum" in c:
        return "Platinum"
    return "Other precious"

trade["metal_group"] = trade["commodity"].apply(classify_metal)

trade = trade.rename(columns={
    "country_or_area": "country",
    "trade_usd": "trade_value_usd",
})

trade = trade[
    ["country", "year", "commodity", "metal_group", "flow",
     "trade_value_usd", "weight_kg", "category"]
]

print(f"Trade data filtered: {len(trade):,} rows, {trade['country'].nunique()} countries")


INFLATION_SHEETS = {
    "hcpi_a": "Headline CPI",
    "fcpi_a": "Food CPI",
    "ecpi_a": "Energy CPI",
    "ccpi_a": "Core CPI",
}

inflation_frames = []

for sheet, label in INFLATION_SHEETS.items():
    df = pd.read_excel(RAW / "Inflation-data.xlsx", sheet_name=sheet, header=None)

    # Row 0 is the header: Country Code | IMF Code | Country | Indicator Type | Series Name | 1970 | 1971 | ...
    header = df.iloc[0].tolist()
    df = df.iloc[1:]  # drop header row
    df.columns = header

    # Year columns are floats like 1970.0
    year_cols = [c for c in df.columns if isinstance(c, (int, float)) and 1900 < c < 2100]

    melted = df.melt(
        id_vars=["Country"],
        value_vars=year_cols,
        var_name="year",
        value_name="inflation_rate",
    )
    melted = melted.rename(columns={"Country": "country"})
    melted["year"] = melted["year"].astype(int)
    melted["inflation_rate"] = pd.to_numeric(melted["inflation_rate"], errors="coerce")
    melted["inflation_type"] = label
    melted = melted.dropna(subset=["inflation_rate"])

    inflation_frames.append(melted[["country", "year", "inflation_type", "inflation_rate"]])

inflation = pd.concat(inflation_frames, ignore_index=True)
print(f"Inflation data: {len(inflation):,} rows")


# Map common mismatches between the two datasets
COUNTRY_MAP = {
    "Bolivia (Plurinational State of)": "Bolivia",
    "Cabo Verde": "Cape Verde",
    "China, Hong Kong SAR": "Hong Kong SAR, China",
    "China, Macao SAR": "Macao SAR, China",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Czechia": "Czech Republic",
    "Dominican Rep.": "Dominican Republic",
    "Dem. Rep. of the Congo": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Fmr Sudan": "Sudan",
    "FS Micronesia": "Micronesia, Fed. Sts.",
    "Gambia": "Gambia, The",
    "Iran (Islamic Rep. of)": "Iran, Islamic Rep.",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Lao People's Dem. Rep.": "Lao PDR",
    "North Macedonia": "Macedonia, FYR",
    "Rep. of Korea": "Korea, Rep.",
    "Rep. of Moldova": "Moldova",
    "Russian Federation": "Russia",
    "Saint Kitts and Nevis": "St. Kitts and Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
    "Slovakia": "Slovak Republic",
    "State of Palestine": "West Bank and Gaza",
    "Syria": "Syrian Arab Republic",
    "TFYR of Macedonia": "Macedonia, FYR",
    "United Rep. of Tanzania": "Tanzania",
    "United States": "United States of America",
    "Venezuela": "Venezuela, RB",
    "Viet Nam": "Vietnam",
    "Yemen": "Yemen, Rep.",
}

trade["country"] = trade["country"].replace(COUNTRY_MAP)
inflation["country"] = inflation["country"].replace(
    {v: k for k, v in COUNTRY_MAP.items()}  # reverse: map inflation names → trade names
)


# Pivot inflation so each type becomes its own column
inflation_wide = inflation.pivot_table(
    index=["country", "year"],
    columns="inflation_type",
    values="inflation_rate",
    aggfunc="first",
).reset_index()

inflation_wide.columns.name = None  # clean up multi-index name

combined = trade.merge(inflation_wide, on=["country", "year"], how="left")

print(f"\nCombined dataset: {len(combined):,} rows")
print(f"  Countries: {combined['country'].nunique()}")
print(f"  Years: {combined['year'].min()} – {combined['year'].max()}")
print(f"  Inflation match rate: {combined['Headline CPI'].notna().mean():.1%}")
print(f"\nColumns: {combined.columns.tolist()}")


out_path = OUT / "precious_metals_trade_inflation.csv"
combined.to_csv(out_path, index=False)
print(f"\nSaved to {out_path} ({out_path.stat().st_size / 1e6:.1f} MB)")
