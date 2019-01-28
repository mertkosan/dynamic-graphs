from random import randint


class TimeSeries:
    def __init__(self, graph):
        # graph variable is NetworkX instance
        self._graph = graph
        self._feature_functions = list()
        self._features = list()
        self._has_event = list()
        self._history_func = self.empty_history
        self._series = list()

    # without any history information
    def empty_history(self, feature_arr, decimal_places=4):
        return round(feature_arr[-1] - feature_arr[-2], decimal_places)

    def set_feature_functions(self, feature_functions):
        self._feature_functions = feature_functions

    def set_history_function(self, history_function):
        self._history_func = history_function

    # learns features for each feature and graph from feature functions
    def learn_features(self):
        for func in self._feature_functions:
            graph_features = []
            for subgraph in self._graph:
                graph_features.append(func(subgraph))
            self._features.append(graph_features)
            self._has_event.append(randint(0, 1))  # TODO: event happened or not, it will not be random

    def create_time_series(self):
        for time in range(len(self._graph)-1):
            series = list()
            for feature in self._features:
                series.append(self._history_func(feature_arr=feature[:time+2]))
            self._series.append(series)

