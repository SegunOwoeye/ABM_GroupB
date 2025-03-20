from enum import Enum
import mesa
import numpy as np
from mesa import Model
from mesa.discrete_space import CellCollection
from test_src.model.network_space import (
    NetworkSpace
)
from test_src.agent.trader import (
    TraderState,
    TraderAgent,
    trader_strategy
)

# Helper function to generate random prices that follow a geometric brownian motion
def generate_new_price(previous_price, volatility=0.01, drift=0):
    """Generate the next price using a Geometric Brownian Motion step."""
    dt = 1 / 252  # Assume 252 trading days
    sqrt_dt = np.sqrt(dt)
    random_return = np.random.normal(loc=0, scale=sqrt_dt)  # Random return

    # Applying Geometric Brownian Motion formula for a single step
    new_price = previous_price * np.exp((drift - 0.5 * volatility ** 2) * dt + volatility * random_return)

    return float(new_price) 



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
        num_nodes=3,
        avg_node_degree=3,
        start_price=100,  # Use a single starting price instead of a full array
        volatility=0.01,
        seed=None,
    ):
        super().__init__(seed=seed)

        self.current_price = float(start_price)  # Store the latest price
        self.volatility = volatility
        self.market_date = 0
        self.price_history = [self.current_price]  # Maintain full price history

        # Create the network space and store it in the grid attribute of the Trader model class
        network_space = NetworkSpace(num_nodes, avg_node_degree, self.random)
        self.grid = network_space.get_network()

        # Data Collection
        self.datacollector = mesa.DataCollector(
            {
                "Zero_Capital": number_of_zero_capital,
                "With_Capital": number_of_with_capital
            }
        )

        # Create Trader Agents
        TraderAgent.create_agents(
            self,
            num_nodes,
            100,
            trader_strategy,
            0.01,
            self.price_history,  # Pass history
            0.5,
            list(self.grid.all_cells),
        )

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """Advance simulation one step and generate a new price dynamically."""
        self.agents.shuffle_do("step")
        self.market_date += 1
        print(self.market_date)

        # Generate the next price dynamically
        self.current_price = generate_new_price(self.current_price, volatility=self.volatility)

        # Append to history for tracking
        self.price_history.append(self.current_price)

        # Update agents
        self.agents.set("price_memory", self.current_price)  # number
        self.agents.set("market_prices", self.price_history)  # List

        # Collect data
        self.datacollector.collect(self)





# Testing the model (currently just tests the stepping function and the grid attribute)

"""test_model = TraderNetwork()
for _ in range(4):  
    test_model.step()
    print(f"Time {_}: Grid = {test_model.grid}")
    print()"""
