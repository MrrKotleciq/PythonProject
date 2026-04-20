import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dane = {
    "Dzień" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Cena" : np.ceil(np.random.normal(100, 10, 10))
}

df = pd.DataFrame(dane)
df["SMA3"] = df["Cena"].rolling(3).mean()



'''plt.plot(df["Dzień"],df["Cena"], marker="o", linestyle="--")

plt.title("Cena akcji")
plt.xlabel("Dzień")
plt.ylabel("Cena")

plt.show()'''

df["Zwrot %"] = df["Cena"].pct_change() * 100

print(df)

plt.hist(df["Zwrot %"].dropna(), bins = 7)
plt.title("Histogram Zwrotów")
plt.show()

plt.plot(df["Dzień"], df["Cena"], label= "cena")
plt.plot(df["Dzień"], df["SMA3"], label= "SMA 3")

plt.legend()
plt.show()