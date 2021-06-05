import pandas as pd
import gdelt
import numpy as np
import csv
from sklearn.tree import DecisionTreeClassifier


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
        tone = np.sum(res['AvgTone'])
        gov_attitude = 'neutral'
        if tone > 0:
            gov_attitude = 'pro'
        elif tone < 0:
            gov_attitude = 'anti'
        return gov_attitude

    def get_avg_tone(self, dataset, media_addr):
        res = dataset[(dataset['Actor1Code'] == 'GOV') & (dataset['Actor1Geo_CountryCode'] == self.gdeltCode) & (
            dataset['SOURCEURL'].str.contains(media_addr))]
        tone = np.sum(res['AvgTone'])
        return tone

    def get_num_sources(self, dataset, media_addr):
        res = dataset[(dataset['Actor1Code'] == 'GOV') & (dataset['Actor1Geo_CountryCode'] == self.gdeltCode) & (
            dataset['SOURCEURL'].str.contains(media_addr))]
        return np.sum(res['NumSources'])

    def get_root_events(self, dataset, media_addr):
        res = dataset[(dataset['Actor1Code'] == 'GOV') & (dataset['Actor1Geo_CountryCode'] == self.gdeltCode) & (
            dataset['SOURCEURL'].str.contains(media_addr))]
        return len(res[res['IsRootEvent'] == 1])

    def get_reliability(self, dataset, media_addr):
        res = dataset[dataset['SOURCEURL'].str.contains(media_addr)]
        if len(res) == 0:
            return 1.0
        notRootNumber = len(
            res[(res['NumSources'] < 4) & (res['IsRootEvent'] == 0)])
        rootNumber = len(res[(res['NumSources'] < 4)
                             & (res['IsRootEvent'] == 1)])
        notReliableArticlesNumber = 0.5 * notRootNumber + rootNumber
        if notReliableArticlesNumber / len(res) > 0.75:
            return 'not_reliable'
        else:
            return 'reliable'

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
# usa1 = Country('US', 'com')

countries = [poland, russia, china, japan, germany, india, brazil, usa]
# countries = [usa]


def media_categorization(csv_name, date_range):
    with open(csv_name, 'w', newline='') as f:
        fieldnames = ['media', 'government_attitude',
                      'reliability', 'avg_tone', 'root_events', 'num_sources']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        pd.set_option('max_columns', None)

        gd1 = gdelt.gdelt(version=1)
        dataset = gd1.Search(date_range,
                             table='events', output='pd')
        print(dataset.columns)

        for country in countries:
            for mediaAddr in country.get_media_names(dataset):
                if mediaAddr in ['www.bbc.com', 'www.cnn.com', 'www.foxnews.com'] or True:
                    gov_attitude = country.get_tone_to_gov(dataset, mediaAddr)
                    reliability = country.get_reliability(dataset, mediaAddr)
                    avg_tone = country.get_avg_tone(dataset, mediaAddr)
                    root_events = country.get_root_events(
                        dataset, mediaAddr)
                    num_sources = country.get_num_sources(dataset, mediaAddr)
                    writer.writerow({'media': mediaAddr, 'government_attitude': gov_attitude,
                                     'reliability': reliability, 'avg_tone': avg_tone, 'root_events': root_events, 'num_sources': num_sources})
            print(f"Country {country} loaded!")
        print("Done!")


if __name__ == '__main__':
    media_categorization("media5.csv", ['2020 Jan 6', '2020 Feb 6'])
