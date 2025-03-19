from enum import Enum
import mesa
import numpy as np
from mesa import Model
from mesa.discrete_space import CellCollection
from src.model.network_space import (
    NetworkSpace
)
from src.agent.trader import (
    TraderState
)

# Helper function to generate random prices that follow a geometric brownian motion
def generate_prices(start_price, num_days, volatility, drift=0):
  dt = 1 / 252  # 252 trading day assumption
  sqrt_dt = np.sqrt(dt)
  random_returns = np.random.normal(loc=0, scale=sqrt_dt, size=num_days)
  returns = (drift - 0.5 * volatility ** 2) * dt + volatility * random_returns

  prices = np.zeros(num_days + 1)
  prices[0] = start_price
  for i in range(1, num_days + 1):
    prices[i] = prices[i - 1] * np.exp(returns[i - 1])

  return prices



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
        prices = generate_prices(100, 100, 0.01),
        seed=None,
    ):
        super().__init__(seed=seed)
        
        self.prices = prices
        self.market_date = 0 #simulating the date that we are going to use to iterate through the market prices and provide the price information to the trader agents

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
        TraderAgent.create_agents(
            self,
            num_nodes,
            100,
            trader_strategy,
            0.01,
            self.prices,
            0.5,
            list(self.grid.all_cells),
        )

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        if len(self.prices) > 1:
            self.agents.shuffle_do("step")
            self.market_date+=1
            self.prices = np.delete(self.prices, 0)
            self.agents.set("price_memory", self.prices[0])
            self.agents.set("market_prices", self.prices)
            # collect data after each step
            self.datacollector.collect(self)
        else:
            print("market price data is too low")


# Testing the model (currently just tests the stepping function and the grid attribute)
"""
test_model = TraderNetwork()
for _ in range(4):  
    test_model.step()
    print(f"Time {_}: Grid = {test_model.grid}")"
    print()
"""
