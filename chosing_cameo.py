import datetime
import os
import pandas as pd

data_CAMEO = pd.read_csv("CAMEO.csv", names=["CAMEO", "Description"], delimiter=";", header=1)

def cameo_contains_name(name):
    name = name.lower()
    #filter1 = (data_CAMEO["Description"].str.lower().contains(name)) | False

    df = data_CAMEO

    return df[df["Description"].str.lower().str.contains(name)]

def search_cameo(name):

    searchRes = cameo_contains_name(name)

    print(searchRes.head(20))
    print("Chose index: \n")
    index = int(input())

    return searchRes.values[index]

def search():
    print(data_CAMEO["Description"])
    value = None
    print("Insert name, or 'return' to return value: ", value)
    name = input()
    while(name != "return"):
        value = search_cameo(name)
        print("Output value: ", value)
        print("Insert name, or 'return' to return value: ", value)
        name = input()
    return value



if __name__ == '__main__':
    print("Returned: ", search())


