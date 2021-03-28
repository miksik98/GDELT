import datetime
import os
import pandas as pd
from statsmodels.tsa.api import VAR
import gdelt

pd.set_option('max_columns', None)

gd1 = gdelt.gdelt(version=1)


results = gd1.Search(['2016 Oct 31', '2016 Nov 20'],
                     table='events', output='pd')
res = results.loc[results['Actor1Code'] == 'REF']
print(res.head(15))
