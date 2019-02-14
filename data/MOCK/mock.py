import numpy as np
import networkx as nx
import os
import csv
from time import asctime
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from processing.features import features as feature_functions

class Mock:
    def __init__(self):
        self._graphs = []

    def create_graphs(self, count):
        for _ in range(count):
            self._graphs.append(nx.barabasi_albert_graph(np.random.randint(900, 1001), np.random.randint(10, 16)))
        return self._graphs


class DynamicRandomGraph:
    def __init__(self, count):
        self._graph_count = count  # Number of graph in dynamic graph

        self._graphs = []  # All graphs
        self._n = 1000  # Initial number of nodes
        self._p = 0.001  # Initial probability of each edge
        self._event_trigger = 0.07  # How much increase in # edges will result in an event.
        self._p_next = self._p / 20 / (1 - self._p)  # Probability of edge creation for the next generation.
        self._p_increase = 0.5  # Max percentage increase of p_next for the next generation.

        # Initialize with the first graph
        first_graph = nx.erdos_renyi_graph(self._n, self._p)
        self._graphs.append(first_graph)

        # Create dynamic graph with events
        self._event_information = [0]
        current_graph = first_graph
        for _ in range(1, count):
            next_graph = self._find_next_graph(current_graph)
            if self._is_event(next_graph, current_graph):
                self._event_information.append(1)
                self._reset_p_next(current_graph_density=nx.density(next_graph))
            else:
                self._event_information.append(0)
                self._next_p_next()
            current_graph = next_graph
            print(self._p_next, nx.density(current_graph))

    # reset to p value to approximately %5 increase edge number
    def _reset_p_next(self, current_graph_density):
        self._p_next = current_graph_density / 20 / (1 - current_graph_density)

    # increase the probability of edge creation
    def _next_p_next(self):
        self._p_next += self._p_next * np.random.uniform(0, self._p_increase)

    def _find_next_graph(self, current_graph):
        next_graph = current_graph.copy()
        for edge in nx.non_edges(next_graph):
            if np.random.binomial(1, self._p_next) == 1:
                next_graph.add_edge(edge[0], edge[1])
        self._graphs.append(next_graph)
        return next_graph

    def _get_graphs(self):
        return self._graphs

    def _get_event_info(self):
        return self._event_information

    def _is_event(self, next_graph, current_graph):
        return len(next_graph.edges) / len(current_graph.edges) >= 1 + self._event_trigger


class DynamicRandomGraph2:
    def __init__(self, count):
        self._graph_count = count  # Number of graph in dynamic graph

        self._graphs = []  # All graphs.
        self._n = 1000  # Initial number of nodes.
        self._p = 0.01  # Initial probability of each edge.
        self._p_next = 0.01  # Probability of an edge for next time.
        self._event_trigger = 0.5  # How much increase density will be enough for an event.
        self._p_change = 1  # Max percentage change of p_next for the next generation.

        increase = True
        self._event_information = []
        for _ in range(0, count):
            graph = nx.erdos_renyi_graph(self._n, self._p_next)
            self._graphs.append(graph)
            if self._is_event(graph):
                self._event_information.append(1)
                increase = False
            else:
                self._event_information.append(0)
                if self._p_next <= self._p:
                    increase = True
            self._next_p_next(increase)

    # reset p to default
    def _reset_p_next(self):
        self._p_next = self._p

    # increase the probability of edge creation
    def _next_p_next(self, increase=True):
        if increase:
            self._p_next += self._p_next * np.random.uniform(0, self._p_change)
        else:
            self._p_next -= self._p_next * np.random.uniform(0, self._p_change)

    def _get_graphs(self):
        return self._graphs

    def _get_event_info(self):
        return self._event_information

    def _is_event(self, graph):
        return nx.density(graph) >= self._event_trigger


class ClusteredDynamicRandomGraph:
    def __init__(self, graph_count, n=100, p=0.1, threshold=0.2, seed=None, is_chain=False):
        self._graphs = []  # graphs
        self._labels = []  # labels (event or not)
        self._features = []  # feature vectors for each graph
        self._clusters = None  # cluster object after training

        self._n = n  # number of nodes
        self._p = p  # edge probability
        self._threshold = threshold  # threshold value that p will be stable
        self._is_chain = is_chain  # is the dynamic graph chain?

        self._seed = seed

        self._construct_graphs(graph_count)
        self._generate_features()
        # self._normalize_features()
        self._cluster_features()
        # self._write_data()

    def get_graphs(self):
        return self._graphs

    def _next_parameters(self):
        if not self._is_chain:
            self._n += int(np.round(np.random.exponential(1)))
            if self._p > self._threshold:
                self._p += np.random.normal(0, 0.01)
            else:
                self._p += np.random.normal(0.01, 0.01)
        # TODO : elif self.chain...

    def _construct_graphs(self, graph_count):
        for i in range(graph_count):
            gi = nx.erdos_renyi_graph(n=self._n, p=self._p, seed=self._seed)
            self._graphs.append(gi)
            self._next_parameters()
            print(self._n, self._p)

    def _generate_features(self):
        for subgraph in self._graphs:
            graph_features = []
            for func in feature_functions:
                graph_features.append(func(subgraph))
            self._features.append(graph_features)

    def _cluster_features(self):
        x = np.array(self._features)
        good_k = 0
        max_score = -1
        for k in range(3, 11):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(x)
            score = silhouette_score(x, kmeans.labels_)
            if score > max_score:
                max_score = score
                good_k = k
        print(max_score)
        self._clusters = KMeans(n_clusters=good_k, random_state=0).fit(x)

    def _determine_labels(self):
        # TODO: choose random cluster as an event
        self._labels = list(self._clusters.labels_)

    def _write_data(self):
        if len(self._graphs) != len(self._labels):
            raise Exception("The number of graphs should be equal to the number of labels!")

        if len(self._graphs) <= 0 or len(self._labels) <= 0:
            raise Exception("The size of the graph/labels should be bigger than 0!")

        _dump_time = asctime()
        with open("data/%s_edges.csv" % str(_dump_time), "w") as _csv_file:
            _field_names = ['timestamp', 'source', 'target']
            _writer = csv.DictWriter(_csv_file, fieldnames=_field_names)
            _writer.writeheader()

            for timestamp, graph in enumerate(self._graphs):
                for edges in graph.edges:
                    _writer.writerow({'timestamp': timestamp, 'source': edges[0], 'target': edges[1]})

        with open("data/%s_labels.csv" % str(_dump_time), "w") as _csv_file:
            _field_names = ['timestamp', 'is_event']
            _writer = csv.DictWriter(_csv_file, fieldnames=_field_names)
            _writer.writeheader()

            for timestamp, label in enumerate(self._labels):
                _writer.writerow({'timestamp': timestamp, 'is_event': label})


cdrg = ClusteredDynamicRandomGraph(100)