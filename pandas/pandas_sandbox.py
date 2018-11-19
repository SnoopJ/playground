"""
  Load pandas and some sample data. Aliased to `pandas` for quick exploration:
    
    alias pandas='python -i ~/playground/pandas/pandas_sandbox.py'
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "first_name": ["Jason", "Molly", "Tina", "Jake", "Amy"],
        "last_name": ["Miller", "Jacobson", "Ali", "Milner", "Cooze"],
        "age": [42, 52, 36, 24, 73],
        "preTestScore": [4, 24, 31, 2, 3],
        "postTestScore": [25, 94, 57, 62, 70],
    }
)

print("pandas loaded as `pd`, example DataFrame initialized as `df`")
