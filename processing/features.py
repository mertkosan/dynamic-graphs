import networkx
import utils


# one feature value for series of graphs, last feature value is for the current graph
def weighted_average_based_history_function(feature_arr, decimal_places=4):
    diff_arr = [feature_arr[i + 1] - feature_arr[i] for i in range(len(feature_arr) - 1)]
    history = diff_arr[:-1]
    return round(utils.weighted_average_based_on_index(history) + diff_arr[-1], decimal_places)


def average_degree(graph, decimal_place=4):
    degrees = networkx.degree(graph)
    total_degree = 0
    for node in degrees:
        total_degree += node[1]
    return round(total_degree / networkx.number_of_nodes(graph), decimal_place)


def max_degree(graph):
    degrees = networkx.degree(graph)
    _max = 0
    for node in degrees:
        if node[1] > _max:
            _max = node[1]
    return _max


features = [
    networkx.number_of_edges,
    networkx.number_of_nodes,
    average_degree,
    max_degree,
    networkx.density,
    networkx.is_connected,
    networkx.algorithms.shortest_paths.average_shortest_path_length
]
