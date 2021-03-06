import datetime
import os
import numpy
import pandas as pd
from statsmodels.tsa.api import VAR
import gdelt
from chosing_name import search_name
from collections import defaultdict
import matplotlib.pyplot as plt

counts = defaultdict(lambda: defaultdict(int))

pd.set_option('max_columns', None)
gd1 = gdelt.gdelt(version=1)
dates = "2020 Dec 1- 2020 Dec 31"
dataaa = None

def load_data():
    data = gd1.Search(['2020 Dec 1', '2020 Dec 31'],
                    table='events', output='pd')
    return data

def filter_country(dataa: pd.DataFrame, name):
    name = name.upper()
    #results = dataa[["Actor1Name"]]
    #filter1 = (name in results["Actor1Name"]) | (name in results["Actor2Name"])
    filter1 = (dataa["Actor1Name"].str.contains(name)) | False
    
    return dataa[filter1].drop_duplicates()

def get_country_data(country, data):

    searchRes = filter_country(data, country)

    return searchRes

def count_actors(data, country):
    for index, row in data.iterrows():
        name = row["Actor2Name"]
        date = row["SQLDATE"]
        num_articles = row["NumArticles"]
        if name == name and name != country and date>=20201201 and date<=20201231:
            counts[name][date]+= num_articles
    
    return counts

def filter_actors(data):
    #print("data: ", data)
    res = sorted(data.items(), key=lambda k_v: sum(k_v[1].values()), reverse = True)[:10]
    #print("values: \n\n", res)
    
    return res

def work():
    data = load_data()

    country = None

    print("Select dates")
    dates = input()

    country = "EUROPE"

    while country == None:
        print("Select country name")
        country_name = input()

        country = search_name(data, country_name)
    
    print(country)

    res = get_country_data(country, data)
    print(res.head())

    result = count_actors(res, country)
    res = filter_actors(result)
    result = res
    #print(result)
    for key, value in result:#.items():
        print(key)
        lists = sorted(value.items()) # sorted by key, return a list of tuples
        x, y = zip(*lists) # unpack a list of pairs into two tuples
        x2 = []
        for v in x:
            x2.append(str((v//100)%100) + "-" + str(v%100))
        plt.plot(x2, y, label=key + " (" + str(sum(y)) + ")")
    plt.legend()
    plt.show()
    return result



if __name__ == '__main__':
    print("\n", "Returned: ", work())