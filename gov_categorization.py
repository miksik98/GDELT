import pandas as pd
import gdelt
import numpy as np
import csv


class Country:
    def __init__(self, gdeltCode, domain):
        self.gdeltCode = gdeltCode
        self.urlPart = '.' + domain

    @staticmethod
    def __get_media_names(series):
        return np.vectorize(lambda serie: serie.split('/')[2])(series['SOURCEURL'].values)

    def get_media_names(self, dataset):
        series = dataset[dataset['SOURCEURL'].str.contains(self.urlPart)]
        return [x for x in np.unique(self.__get_media_names(series)) if np.char.endswith(x, self.urlPart)]

    def get_tone_to_gov(self, dataset, media_addr):
        res = dataset[(dataset['Actor1Code'] == 'GOV') & (dataset['Actor1Geo_CountryCode'] == self.gdeltCode) & (
            dataset['SOURCEURL'].str.contains(media_addr))]
        return np.sum(res['AvgTone'])


    def __str__(self):
        return self.gdeltCode


poland = Country('PL', 'pl')
russia = Country('RU', 'ru')
china = Country('CH', 'cn')
japan = Country('JP', 'jp')
germany = Country('DE', 'de')
india = Country('IN', 'in')
brazil = Country('BR', 'br')
usa = Country('US', 'us')

countries = [poland, russia, china, japan, germany, india, brazil, usa]


def categorization_by_government_attitude(csv_name, date_range):
    with open(csv_name, 'w', newline='') as f:
        fieldnames = ['media', 'government_attitude']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        pd.set_option('max_columns', None)

        gd1 = gdelt.gdelt(version=1)
        dataset = gd1.Search(date_range,
                             table='events', output='pd')

        for country in countries:
            for mediaAddr in country.get_media_names(dataset):
                tone = country.get_tone_to_gov(dataset, mediaAddr)
                gov_attitude = 'neutral'
                if tone > 0:
                    gov_attitude = 'pro'
                elif tone < 0:
                    gov_attitude = 'anti'
                writer.writerow({'media': mediaAddr, 'government_attitude': gov_attitude})
            print(f"Country {country} loaded!")
        print("Done!")


if __name__ == '__main__':
    categorization_by_government_attitude("media.csv", ['2021 Mar 1', '2021 Apr 17'])
