import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dane = {
    "Dzień": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    "Cena" : [100,102,101,104,107,106,109,111,110,114,123,132,110,104,103,106,109,111,110,114]
}

df = pd.DataFrame(dane)
df["return %"] = df["Cena"].pct_change() * 100

srednia = df["Cena"].mean()
zmiennosc = df["Cena"].std()

df["SMA3"] = df["Cena"].rolling(5).mean()

df["signal"] = np.where(df["Cena"] > df["SMA3"], 1, 0)

print(df)
print("Średnia: ", srednia)
print("STD: ", zmiennosc)

plt.plot(df["Dzień"], df["Cena"], marker = "o", label = "Cena")
plt.plot(df["Dzień"], df["SMA3"], label = "SMA3")

plt.title("MiniTrading System")
plt.xlabel("Dzień")
plt.ylabel("Cena")
plt.legend()
plt.show()

