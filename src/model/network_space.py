import networkx as nx
import mesa
from mesa.discrete_space import CellCollection, Network

class NetworkSpace():
    # The network space class that implements the logic behind the network grid
    def __init__(self, num_nodes, avg_node_degree, random_value):
        prob = avg_node_degree / num_nodes
        self.graph = nx.erdos_renyi_graph(n=num_nodes, p=prob)
        self.random = random_value

    def get_network(self):
        return Network(self.graph, capacity=1, random=self.random)
