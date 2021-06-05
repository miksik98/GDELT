import gdelt
import pandas as pd
import csv


class Edge:
    def __init__(self, value, node1, node2):
        self.value = value
        self.node1 = node1
        self.node2 = node2

    def is_equal(self, other):
        return (self.node1 == other.node1 and self.node2 == other.node2) or (
                self.node1 == other.node2 and self.node2 == other.node1)

    def print(self):
        print(f"{self.value} |  {self.node1} | {self.node2}")

    def to_csv(self):
        return f"{self.node1},{self.node2},{self.value}"


class Edges:
    def __init__(self):
        self.list = []

    def add_edge(self, edge):
        for e in self.list:
            if e.is_equal(edge):
                e.value += edge.value
                return False
        self.list.append(edge)
        return True

    def print(self):
        for e in self.list:
            print(e.to_csv())

    def to_csv(self, csv_name):
        with open(csv_name, 'w', newline='') as f:
            fieldnames = ['Source', 'Target', 'num_mentions']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in self.list:
                writer.writerow({'Source': e.node1, 'Target': e.node2, 'num_mentions': e.value})


data = None
edges = Edges()


def prepare_graph(given_country, depth, current_depth=0):
    if depth != 'max' and current_depth >= depth:
        return
    results = data.loc[(data['EventRootCode'] == "03") & (data['Actor1CountryCode'] == given_country)]
    results = zip(results["Actor2CountryCode"], results["NumMentions"])
    m = {}
    for x in results:
        country = x[0]
        if country != given_country:
            if not pd.isna(country):
                if m.get(country) is None:
                    m[country] = x[1]
                else:
                    m[country] += x[1]
    countries = []
    for country in m:
        if edges.add_edge(Edge(m[country], given_country, country)):
            countries.append(country)
    for country in countries:
        prepare_graph(country, depth, current_depth + 1)


def load_data(time_range):
    return gdelt.gdelt(version=1).Search([time_range[0], time_range[1]],
                                         table='events', output='pd')


if __name__ == '__main__':
    data = load_data(['2021 Jun 1', '2021 Jun 2'])
    given_country = "USA"
    depth = 'max'
    csv_name = "cooperation_graph1.csv"
    prepare_graph(given_country, depth)
    edges.to_csv(csv_name)
