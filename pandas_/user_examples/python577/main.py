import pandas as pd
import numpy as np
import re

from pandas import DataFrame

NWR = pd.read_excel('NWR_ALDT.xls', sheet_name='ICT')
# print(NWR.columns)
# con=(NWR['(1) ROUTE', '(21) ROUTES LOCKED'])
a: DataFrame = pd.DataFrame(NWR[['(1) ROUTE', '(21) ROUTES LOCKED']])
b = pd.DataFrame(NWR['(1) ROUTE'])
e= pd.DataFrame('ASSIGN ' + b + '.TCS.SI')
c = pd.DataFrame(NWR['(21) ROUTES LOCKED'])
d = pd.DataFrame(c.stack().str.replace(',', '.JK + ~').unstack())
assign = 'ASSIGN ' + b +'.TCS.SI' + d + '  TO ' + b + 'JK;'

