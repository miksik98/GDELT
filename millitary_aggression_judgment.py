import pandas as pd
import numpy as np
import gdelt
import matplotlib.pyplot as plt


def plot_military_judgement_stats(given_country, timeSeries):
    results = gdelt.gdelt(version=1).Search([timeSeries[0], timeSeries[1]],
                                            table='events', output='pd')
    res = results.loc[(results['EventRootCode'] == "20") | (results['EventRootCode'] == "19")]
    res1 = res.loc[(results['Actor1CountryCode'] == given_country)]
    m = {}
    countries = []
    for x in zip(res1['Actor2CountryCode'], res1['AvgTone']):
        country = x[0]
        if not pd.isna(country):
            if m.get(country) is None:
                countries.append(country)
                m[country] = [x[1]]
            else:
                m[country].append(x[1])
    result = {'country': [], 'avgTone': [], 'numberOfEvents': []}
    for country in countries:
        c = country if country != given_country else 'internal'
        result['country'].append(c)
        result['avgTone'].append(np.mean(m[country]))
        result['numberOfEvents'].append(len(m[country]))
    df = pd.DataFrame(result).sort_values('numberOfEvents', ascending=False)
    plt.figure(1)
    plt.title(f'Media\'s judgement of military operations of {given_country} in other countries\n in period: {timeSeries[0]} - {timeSeries[1]}')
    plt.bar(df['country'], df['avgTone'], color='maroon', width=0.4)
    plt.xlabel(f'Country military involved by {given_country}')
    plt.ylabel('Media average judgement')
    plt.figure(2)
    plt.table(cellText=df.values, colLabels=df.columns, loc='center')
    plt.title(f'Media\'s judgement of military operations of {given_country} in other countries\nin period: {timeSeries[0]} - {timeSeries[1]}')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    given_country = "ISR"
    plot_military_judgement_stats(given_country, ['2021 Apr 1', '2021 Apr 3'])
