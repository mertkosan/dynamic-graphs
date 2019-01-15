#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt

nodes = pd.read_csv('data/Madrid/Madrid_Nodes_Public_Version2.csv')
relations = pd.read_csv('data/Madrid/Madrid_Relations_Public_Version2.csv')


# union of dynamic graph to one static graph
graph = relations.groupby('ID')['Tie_ID'].apply(list).to_dict()
freqs = [len(graph[node]) for node in graph]

histogram = plt.hist(freqs, bins=max(freqs))

# Build a dynamic graph from Madrid data. Examine how did they change across time?
dynamic_graph = []
periods = relations.columns[7:] # We have timeline after index 7
for period in periods:
    current_graph = relations[["ID", "Tie_ID", period]].dropna().groupby("ID")["Tie_ID"].apply(list).to_dict()
    dynamic_graph.append((period, current_graph))  # for each graph, first index is period, second index is data

# Calculate average number of neighbors for each graph
average_neighbour_counts = {}
for d_graph in dynamic_graph:
    d_graph_period = d_graph[0]
    d_graph_data = d_graph[1]
    person_count, neighbour_count = 0, 0
    for person in d_graph_data:
        person_count += 1
        neighbour_count += len(d_graph_data[person])
    if person_count != 0:
        average_neighbour_counts[d_graph_period] = neighbour_count / person_count

# plot average neighbour count
lists = sorted(average_neighbour_counts.items())
x, y = zip(*lists)
plt.cla()
plt.plot(x, y)
plt.xticks(rotation=90)
plt.show()
