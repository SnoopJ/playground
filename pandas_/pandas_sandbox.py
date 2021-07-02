"""
  Load pandas and some sample data. Aliased to `pandas` for quick exploration:
    
    alias pandas='python -i ~/playground/pandas/pandas_sandbox.py'
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "ID": [1000, 1001, 1005, 1337, 1578],
        "first_name": ["Jason", "Molly", "Tina", "Jake", "Amy"],
        "last_name": ["Miller", "Jacobson", "Ali", "Milner", "Cooze"],
        "age": [42, 52, 36, 24, 73],
        "preTestScore": [4, 24, 31, 2, 3],
        "postTestScore": [25, 94, 57, 62, 70],
    }
)

df2 = pd.DataFrame(
    {
        "ID": [1000, 1001, 1005, 1337, 1578, 1298],
        "first_name": ["Jason", "Molly", "Tina", "Jake", "Amy", "Robert"],
        "last_name": ["Miller", "Jacobson", "Ali", "Milner", "Cooze", "'); DROP TABLE Students;"],
        "remarks": ["cool", "very cool", "chill", "definitely not a shark", "finite entity", "what's up with that name?!"]
    }
)

print("pandas loaded as `pd`, example DataFrames initialized as `df` and `df2`")
