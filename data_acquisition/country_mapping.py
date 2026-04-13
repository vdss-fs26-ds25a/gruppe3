import csv 
from pathlib import Path
import pycountry


BASE_DIR = Path(__file__).parent.parent  
CSV_PATH = BASE_DIR / "data" / "processed" / "precious_metals_trade_inflation.csv"

# Ländernamen aus CSV laden, Duplikate entfernen
with open(CSV_PATH) as f:
    reader = csv.DictReader(f)
    laender = set() 
    for row in reader:
        laender.add(row['country']) 

print(len(laender)) #check 

gefunden = {}
nicht_gefunden = []

# Manuelle Korrekturen für nicht-standardisierte Namen
korrekturen = {
    "Korea, Rep.": "KR",
    "Turkey": "TR",
    "Russia": "RU",
    "USA": "US",
    "Vietnam": "VN",
    "Iran": "IR",
    "Tanzania": "TZ",
    "Bolivia": "BO",
    "Venezuela, RB": "VE",
    "Egypt, Arab Rep.": "EG",
    "Kyrgyz Republic": "KG",
    "Lao PDR": "LA",
    "Gambia, The": "GM",
    "Yemen, Rep.": "YE",
    "Slovak Republic": "SK",
    "Czech Rep.": "CZ",
    "Central African Rep.": "CF",
    "Cote d'Ivoire": "CI",
    "Cape Verde": "CV",
    "Swaziland": "SZ",
    "Macao SAR, China": "MO",
    "Hong Kong SAR, China": "HK",
    "Macedonia, FYR": "MK",
    "Bosnia Herzegovina": "BA",
    "St. Lucia": "LC",
    "St. Kitts and Nevis": "KN",
    "St. Vincent and the Grenadines": "VC",
    "Solomon Isds": "SB",
    "Cook Isds": "CK",
    "Faeroe Isds": "FO",
    "Turks and Caicos Isds": "TC",
    "Micronesia, Fed. Sts.": "FM",
    "Neth. Antilles": "AN",
}

# Schritt 1: exakte Suche
for name in laender:
    ergebnis = pycountry.countries.get(name=name)
    if ergebnis:
        gefunden[name] = ergebnis.alpha_2
    else:
        # Schritt 2: Fuzzy Search als Backup
        try: 
            ergebnis = pycountry.countries.search_fuzzy(name)
            gefunden[name] = ergebnis[0].alpha_2
        except LookupError:
            # Schritt 3: manuelle Korrekturen
            if name in korrekturen:
                gefunden[name] = korrekturen[name]
            else:
                nicht_gefunden.append(name)

print("O Gefunden:", len(gefunden))
print("X Nicht gefunden:", nicht_gefunden)

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "country_mapping.csv"

# Ergebnis speichern
with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["country", "iso_code"])
    writer.writeheader()
    for name, code in gefunden.items():
        writer.writerow({"country": name, "iso_code": code})

print("Gespeichert!")