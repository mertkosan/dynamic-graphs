import random
from networkx import generators as gen


class Mock:
    def __init__(self):
        self._graphs = []

    def create_graphs(self, count):
        for _ in range(count):
            self._graphs.append(gen.barabasi_albert_graph(random.randint(900, 1000), random.randint(10, 15)))
        return self._graphs
