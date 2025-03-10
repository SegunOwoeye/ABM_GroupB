from enum import Enum
import math
import mesa
from mesa import Model
from mesa.discrete_space import CellCollection
from src.model.network_space import (
    NetworkSpace
)

# State class to indicate the state of each trader agent. "Broke" or "with some money".
class TraderState(Enum):
    ZERO_CAPITAL = 0
    HAS_CAPITAL = 1


# Helper functions that calculates the trader agents' state at each time step
def number_state(model, state):
    return sum(1 for a in model.grid.all_cells.agents if a.state is state)


def number_of_zero_capital(model):
    return number_state(model, TraderState.ZERO_CAPITAL)


def number_of_with_capital(model):
    return number_state(model, TraderState.HAS_CAPITAL)


class TraderNetwork(Model):
    # The Trader Network Model containing the Network grid space and the Trader Agents
    def __init__(
        self,
        num_nodes=10,
        avg_node_degree=3,
        initial_outbreak_size=1,
        seed=None,
    ):
        super().__init__(seed=seed)

        # Create the network space and store it in the grid attribute of the Trader model class
        network_space = NetworkSpace(num_nodes, avg_node_degree, self.random)
        self.grid = network_space.get_network()


        # The variables that will be calculated with each step and stored within the model for later visualisation
        self.datacollector = mesa.DataCollector(
            {
                "Zero_Capital": number_of_zero_capital,
                "With_Capital": number_of_with_capital
            }
        )

        # Create Trader Agents
        """
        TraderAgent.create_agents(
            self,
            num_nodes,
            State.HAS_CAPITAL,
            list(self.grid.all_cells),
        )
        """

        # Implement Capital sharing between nodes and agents
        """
        self.initial_outbreak_size = (
            initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes
        )

        infected_nodes = CellCollection(
            self.random.sample(list(self.grid.all_cells), self.initial_outbreak_size),
            random=self.random,
        )
        for a in infected_nodes.agents:
            a.state = State.INFECTED

        """

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        self.agents.shuffle_do("step")
        # collect data after each step
        self.datacollector.collect(self)


# Testing the model (currently just tests the stepping function and the grid attribute)
"""
test_model = TraderNetwork()
for _ in range(2):  
    test_model.step()
    print(f"Time {_}: Grid = {test_model.grid}")"
"""
