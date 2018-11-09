"""
most function takes a graph as a parameter like below format:
graph:
{
    1: [2, 3, 4],
    2: [1, 3],
    3: [1, 2],
    4: [1]
}
"""


def is_graph_connected(graph):
    """
    Decide whether the graph is connected or not
    :param graph: dict
    :return: True if graph is connected, False if graph is not connected
    """
    pass


def how_many_unconnected_graph(graph):
    """
    Decide how many unconnected graph exists
    :param graph: dict
    :return: integer n where n is the number of graphs which are unconnected
    """
    pass


def find_max_degree(graph):
    """
    Decide maximum degree node in given graph
    :param graph: dict
    :return: integer n where n is the maximum degree in the graph
    """
    pass


def average_degree(graph):
    """
    Decide average degree of nodes in given graph
    :param graph: dict
    :return: integer n where n is the average degree in the graph
    """
    pass


def global_min_cut_size(graph):
    """
    Decide global min-cut size in the graph
    :param graph: dict
    :return: integer n where n is the global min-cut size in the graph.
    """
    pass


def centrality(graph):
    # There are many centrality parametrics in the graphs, decide which one to choose
    pass


def density(graph):
    """
    Decide the density of the graph with number of edges and vertices in the graph.
    :param graph: dict
    :return: integer n where n is a density in the graph
    """
    pass


def diameter(graph):
    """
    Decide the diameter of the graph, the length of the longest shortest path
    :param graph: dict
    :return: integer n where n is the diameter of the graph
    """
    pass


def edge_number(graph):
    """
    Decide the number of edges in the graph
    :param graph: dict
    :return: integer n where n is the number of edges in the graph.
    """
    pass


def node_number(graph):
    """
    Decide the number of nodes in the graph
    :param graph: dict
    :return: integer n where n is the number of nodes in the graph.
    """
    pass
