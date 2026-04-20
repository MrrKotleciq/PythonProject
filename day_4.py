import pandas as pd

dane = {
    "Data" : ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
    "Cena" : [100, 92, 105, 100, 103],
    "Wolumen" : [7000,6000,5000,2000,3500]
}

df = pd.DataFrame(dane)
#print(df)

#df.to_excel("test.xlsx")

#print(df[["Cena"]])

srednia, maksimum, minimum = df["Cena"].mean(), df["Cena"].max(), df["Cena"].min()

print("\nŚrednia jest równa ", srednia, ". Maksimum jest równe ", maksimum, " Minimum jest równe ", minimum, "\n")

df["Zmiana %"] = df["Cena"].pct_change() * 100

#print(df)

#print(df[df["Cena"] > 102])

print(df[df["Zmiana %"]>0])