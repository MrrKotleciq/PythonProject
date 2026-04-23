import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

apple_data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")
tesla_data = yf.download("TSLA", start="2023-01-01", end="2024-01-01")

apple_data["Zwrot %"] = apple_data["Close"].pct_change() * 100
apple_data["SMA10"] = apple_data["Close"].rolling(10).mean()
apple_mean = apple_data["Close"].mean()
apple_std = apple_data["Close"].std()

print("\nŚrednia", apple_mean,
      "\nZmienność", apple_std)

tesla_data["Zwrot %"] = tesla_data["Close"].pct_change() * 100
tesla_data["SMA10"] = tesla_data["Close"].rolling(10).mean()
tesla_mean = tesla_data["Close"].mean()
tesla_std = tesla_data["Close"].std()

print("\nŚrednia", tesla_mean,
      "\nZmienność", tesla_std)

#print(len(apple_data["Close"]), len(tesla_data["Close"]))

plt.plot(apple_data["Close"], label="Apple", color="#181BE4")
plt.plot(apple_data["SMA10"], color="#18B4E4")
plt.plot(tesla_data["Close"], label="Tesla", color="#C58907")
plt.plot(tesla_data["SMA10"], color="#E4C518")

plt.xlabel("Dzień")
plt.ylabel("Cena")
plt.legend()
plt.show()

corr = np.corrcoef(apple_data["Zwrot %"].dropna(), tesla_data["Zwrot %"].dropna())
print("\nkorelacja pomiędzy apple i tesla \n", corr)

'''
print(apple_data.head())
print(tesla_data.head())
'''
# Wykres
'''
plt.plot(apple_data["Close"], label="Apple")
plt.plot(tesla_data["Close"], label="Tesla")
plt.title("Cena zamknięcia")
plt.xlabel("Dzień")
plt.ylabel("Cena")
plt.legend()
plt.show()
'''
