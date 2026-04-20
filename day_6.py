import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## Zwrot z inwestycji (ROI)
'''
dane = {
    "start" : [200,500],
    "koniec" : [250,450]
}

df = pd.DataFrame(dane)

df["ROI"] = (df["koniec"] - df["start"]) / df["start"] * 100

print(df[["ROI"]], "%")
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



