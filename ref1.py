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

country_codes = d = {line[0:2]: line[3:]
                     for line in open("country_codes.txt")}


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


def fig_graph(fig, graph):
    ax = fig.add_subplot(111)
    ax.title.set_text(graph.title)
    G = graph.G

    counts = [i['count'] for i in dict(G.edges).values()]
    labels = [i for i in dict(G.nodes).keys()]
    labels = {i: i for i in dict(G.nodes).keys()}

    pos = graph.pos
    nx.draw_networkx_nodes(G, pos, ax=ax, labels=True)
    nx.draw_networkx_edges(G, pos, width=counts, ax=ax)
    _ = nx.draw_networkx_labels(G, pos, labels, ax=ax)


for time in times_series:
    # res = gd1.Search(time,
    #                      table='events', output='pd')
    listToStr = ' '.join([str(elem) for elem in time])
    # res.to_csv('{}.csv'.format(listToStr))
    res = pd.read_csv('{}.csv'.format(listToStr))
    res = res.loc[res['Actor1Code'] == 'REF']

    # print(res.head(15))
    res = res[res['Actor1Geo_CountryCode'] != res['Actor2Geo_CountryCode']]

    res = res.groupby(['Actor1Geo_CountryCode', 'Actor2Geo_CountryCode', 'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor2Geo_Lat', 'Actor2Geo_Long']).agg(
        {'NumArticles': 'sum'}).sort_values('NumArticles', ascending=False).reset_index()

    res = res.head(20)
    print(res.head(15))

    res.rename(columns={res.columns[6]: "count"}, inplace=True)

    res['country1'] = res['Actor1Geo_CountryCode'].apply(
        lambda code: country_codes[code])

    res['country2'] = res['Actor2Geo_CountryCode'].apply(
        lambda code: country_codes[code])

    

    G = nx.from_pandas_edgelist(
        res, 'country1', 'country2', edge_attr='count')

    graph = MyGraph(G, " - ".join(time))

    graphs.append(graph)


def onclick1(fig):
    global i
    fig.clear()
    i += 1
    i = i % len(times_series)
    fig_graph(fig, graphs[i])
    plt.draw()


fig = go.Figure()
fig_graph(fig, graphs[0])
fig.canvas.mpl_connect('button_press_event', lambda event: onclick1(fig))

plt.show()


plt.show()
