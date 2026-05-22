import pandas as pd

df = pd.DataFrame({
    "position": [0,0,1,1,1,0,0,1]
}, index=pd.date_range("2025-01-01", periods=8))

changes = df["position"] != df["position"].shift(1)

changes_df = df[changes].iloc[1:]

print(changes_df)