import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## return z inwestycji (ROI)
'''
dane = {
    "start" : [200,500],
    "koniec" : [250,450]
}

asset1 = pd.DataFrame(dane)

asset1["ROI"] = (asset1["koniec"] - asset1["start"]) / asset1["start"] * 100

print(asset1[["ROI"]], "%")
'''


# CAGR - średni roczny wzrost
'''
pv = 1000   #wartość początkowa
fv = 2000   #wartość końcowa
n = 5       #liczba lat

cagr = (fv/pv)**(1/n) - 1 #średni roczny wzrost

print(cagr * 100, "%")
'''

# Średnia
'''
dane = [1,2,3,4,5]
print(np.mean(dane))
'''

# Wariacja i odchylenie standardowe
'''
ceny = [100,102,92,104]

print(np.mean(ceny))
print(np.var(ceny))
print(np.std(ceny))
'''

# Korelacja
'''
a = [1,2,3,4,5,6]
b = [2,4,6,8,10,12]


print(np.corrcoef(a,b))
'''

# Covariance
'''
a = [1,2,3,4,5,6]
b = [2,4,6,8,10,12]

print(np.cov(a,b))
'''

dane1 = {
    "Dzień" : [1,2,3,4,5,6,7,8,9,10],
    "Cena" : np.random.normal(100,10,10)
}

dane2 = {
    "Dzień" : [1,2,3,4,5,6,7,8,9,10],
    "Cena" : np.random.normal(100,10,10)
}

asset1 = pd.DataFrame(dane1)
asset2 = pd.DataFrame(dane2)

asset1["return %"] = asset1["Cena"].pct_change() * 100
ROI = (asset1["Cena"][len(asset1["Cena"])-1] - asset1["Cena"][0]) / asset1["Cena"][0] * 100
mean = asset1["Cena"].mean()



print("ROI: ", ROI, ", średnia: ", mean)
print("\nVariacia: " ,np.var(asset1["Cena"]))
print("\nOdchylenie standardowe: ", np.std(asset1["Cena"]))
print("\nCorelation: ", np.corrcoef(asset1["Cena"], asset2["Cena"]))