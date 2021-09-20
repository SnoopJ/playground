import pandas as pd
import numpy as np
import re

from pandas import DataFrame

NWR = pd.read_excel('NWR_ALDT.xls', sheet_name='ICT')

# these will save us some typing
col1 = "(1) ROUTE"
col2 = "(21) ROUTES LOCKED"

df = NWR.copy()  # make a copy that we will change one step at a time
df[col1] = "ASSIGN " + df[col1] + ".TCS.SI"  # change the first column in-place
df[col2] = df[col2].str.replace(",", ".JK + ~")  # replace commas

# now, build a Series object by joining these columns (which are also Series)
assign = df[col1] + df[col2] + " TO " + NWR[col1] + "JK;"

print(assign.iloc[0])  # show the first row, which should be the first statement
