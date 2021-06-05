import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import preprocessing
import graphviz
from sklearn.model_selection import GridSearchCV
# DOT data

le = preprocessing.LabelEncoder()

dataset = pd.read_csv('media5.csv')
dataset['government_attitude'] = le.fit_transform(
    dataset['government_attitude'])

clf = DecisionTreeClassifier(random_state=1234, max_depth=3, criterion='entropy')

X = dataset.loc[:, dataset.columns.isin(
    ['root_events', 'num_sources', 'government_attitude'])]
y = dataset.loc[:, dataset.columns == 'reliability']
model = clf.fit(X, y)

text_representation = tree.export_text(clf)
print(text_representation)

dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=[
                                    'root_events', 'num_sources', 'government_attitude'],
                                class_names=['not_reliable', 'reliable'],
                                filled=True)
graph = graphviz.Source(dot_data, format="png")
graph.render("decision_tree_graphivz")

parameters = {'max_depth': range(2, 20), 'criterion': ['entropy']}
clf = GridSearchCV(DecisionTreeClassifier(), parameters, n_jobs=4)
clf.fit(X=X, y=y)
tree_model = clf.best_estimator_
print(clf.best_score_, clf.best_params_)
