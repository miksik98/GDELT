import datetime
import os
import pandas as pd
from statsmodels.tsa.api import VAR
import gdelt

pd.set_option('max_columns', None)
gd1 = gdelt.gdelt(version=1)

def actors_contains_name(dataa: pd.DataFrame, name):
    name = name.upper()
    results = dataa[["Actor1Name"]]
    #filter1 = (name in results["Actor1Name"]) | (name in results["Actor2Name"])
    filter1 = (results["Actor1Name"].str.contains(name)) | False
    
    return results[filter1].drop_duplicates()

def work():

    data = gd1.Search(['2016 Nov 1', '2016 Nov 5'],
                     table='events', output='pd')

    searchRes = actors_contains_name(data, 'biden')                     

    print(searchRes.head(15))

if __name__ == '__main__':
    work()


