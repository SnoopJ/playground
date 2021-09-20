"""
Select the previous row based on a predicate. Based on a freenode #python
question from Nov 2, 2018
"""

import pandas as pd

df = pd.DataFrame(
    {
        "first_name": ["Jason", "Molly", "Tina", "Jake", "Amy"],
        "last_name": ["Miller", "Jacobson", "Ali", "Milner", "Cooze"],
        "age": [42, 52, 36, 24, 73],
        "preTestScore": [4, 24, 31, 2, 3],
        "postTestScore": [25, 94, 57, 62, 70],
    }
)

print(df)

print("Selecting rows where the next entry is older than 40")
idx = df[df["age"] > 40].index  # rows matching predicate
idx -= 1  # select previous row
idx = idx[idx >= 0]  # ensure we don't select backwards

sel = df.iloc[idx, :]
print(f"Selection:\n{sel}")
