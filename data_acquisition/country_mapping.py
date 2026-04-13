import csv 
from pathlib import Path
import pycountry 

BASE_DIR = Path(__file__).parent.parent  
CSV_PATH = BASE_DIR / "data" / "processed" / "precious_metals_trade_inflation.csv"

with open(CSV_PATH) as f:
    reader = csv.DictReader(f)
    laender = set() # Duplikate entfernen
    for row in reader:
        laender.add(row['country'])

print(len(laender)) #check 

gefunden = {}
nicht_gefunden = []

for name in laender:
    ergebnis = pycountry.countries.get(name=name)
    if ergebnis:
        gefunden[name] = ergebnis.alpha_2
    else:
        nicht_gefunden.append(name)