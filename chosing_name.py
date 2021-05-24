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

def search_name(dataa: pd.DataFrame, name):

    searchRes = actors_contains_name(dataa, name)

    print(searchRes.head(20))
    print("Chose index: \n")
    index = int(input())

    return searchRes.values[index][0]

def search():
    value = None
    tmpData = gd1.Search(['2016 Nov 1', '2016 Nov 2'],
                     table='events', output='pd')
    print("Insert name, or 'return' to return value: ", value)
    name = input()
    while(name != "return"):
        value = search_name(tmpData, name)
        print("Output value: ", value)
        print("Insert name, or 'return' to return value: ", value)
        name = input()
    return value



if __name__ == '__main__':
    print("Returned: ", search())


