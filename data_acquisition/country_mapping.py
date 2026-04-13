import csv 

with open('../data/precious_metals_trade_inflation.csv') as f:
    reader = csv.DictReader(f)
    laender = []
    for row in reader:
        laender.append(row['country'])

print(laender[:5]) #check 