import datetime
import os
import pandas as pd
from statsmodels.tsa.api import VAR
import networkx as nx
import gdelt
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import geopandas as gpd
import plotly.graph_objects as go


pd.set_option('max_columns', None)

countries = pd.read_csv('country_codes.csv', delimiter=',')


gd1 = gdelt.gdelt(version=1)
times_series = [['2016 Oct 31', '2016 Nov 6'], ['2016 Nov 7', '2016 Nov 14'], [
    '2016 Nov 15', '2016 Nov 22'], ['2016 Nov 23', '2016 Nov 30']]
graphs = []
i = 0


class MyGraph:
    def __init__(self, G, title):
        self.G = G
        self.title = title
        self.pos = nx.spring_layout(G)


def fig_graph(fig, source_to_dest, title):
    for c1, c2, slat, dlat, slon, dlon, count in source_to_dest:
        fig.add_trace(go.Scattergeo(
            lat=[float(slat), float(dlat)],
            lon=[float(slon), float(dlon)],
            mode='lines',
            text=[c1, c2],
            line=dict(width=min(count/300, 4), color="red")
        ))

    fig.update_layout(title_text=title,
                      height=700, width=900,
                      showlegend=False)


for time in times_series:
    res = gd1.Search(time,
                         table='events', output='pd')
    listToStr = ' '.join([str(elem) for elem in time])
    # res.to_csv('{}.csv'.format(listToStr))
    # res = pd.read_csv('{}.csv'.format(listToStr))
    res = res.loc[res['Actor1Code'] == 'REF']

    # print(res.head(15))
    res = res[res['Actor1Geo_CountryCode'] != res['Actor2Geo_CountryCode']]

    res = res.groupby(['Actor1Geo_CountryCode', 'Actor2Geo_CountryCode']).agg(
        {'NumArticles': 'sum'}).sort_values('NumArticles', ascending=False).reset_index()

    res = res.head(20)
    # print(res.head(15))

    res['country1'] = res['Actor1Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['name'].iloc[0])

    res['country2'] = res['Actor2Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['name'].iloc[0])

    res['Actor1Geo_Lat'] = res['Actor1Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['lat'].iloc[0])

    res['Actor2Geo_Lat'] = res['Actor2Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['lat'].iloc[0])

    res['Actor1Geo_Long'] = res['Actor1Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['long'].iloc[0])

    res['Actor2Geo_Long'] = res['Actor2Geo_CountryCode'].apply(
        lambda code: countries.loc[countries['code'] == code]['long'].iloc[0])

    source_to_dest = zip(res['country1'], res['country2'], res['Actor1Geo_Lat'], res['Actor2Geo_Lat'], res['Actor1Geo_Long'],
                         res['Actor2Geo_Long'], res['NumArticles'])

    fig = go.Figure()
    fig_graph(fig, source_to_dest, " - ".join(time))
    # fig.canvas.mpl_connect('button_press_event', lambda event: onclick1(fig))

    fig.show()


def onclick1(fig):
    global i
    fig.clear()
    i += 1
    i = i % len(times_series)
    fig_graph(fig, graphs[i])
    plt.draw()


# fig = go.Figure()
# fig_graph(fig, graphs[0])
# # fig.canvas.mpl_connect('button_press_event', lambda event: onclick1(fig))

# fig.show()
