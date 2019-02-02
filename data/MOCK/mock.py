import numpy as np
import networkx as nx


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


drg = DynamicRandomGraph2(100)
