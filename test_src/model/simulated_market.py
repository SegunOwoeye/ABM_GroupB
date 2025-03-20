from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
import random

# Doesn't Work
class Simulated_Market(Model):
    """ [1] - Initialising Variables """
    def __init__(self, trader_ID, model, initial_price=100, initial_liquidity: int=10000):
        super().__init__(trader_ID, model)
        self.price = initial_price  # Initial stock price
        self.liquidity = initial_liquidity
        self.order_book = []  # (Side, Quantity, Trader)
        
    
    """ [2] Match Buy/Sell Orders and adjust price based on order imbalance"""
    def execute_orders(self):
        # Initialising total buy and sell
        total_buys = 0
        total_sells = 0
        
        # Obtaining total stocks bought and sold
        for side, qty, trader in self.order_book:
            if side == 'buy':
                total_buys += qty
            elif side == "sell":
                total_sells += qty

        # Adjust price based on demand/supply
        order_imbalance = total_buys - total_sells

        if abs(order_imbalance) > 0:
            impact_coefficient = 0.02
            market_impact = np.sqrt(order_imbalance/self.liquidity)
            price_change = market_impact * self.price * impact_coefficient

            if order_imbalance > 0: # More Buyers than sellers
                self.price += price_change # Price Increases
            elif order_imbalance < 0: # More sellers than buyers
                self.price -= price_change # Price Decreases
        
        # Clear order book after execution
        self.order_book = []



    """ [] Process all orders by agent and adjust stock price based on supply vs demand """
    def step(self):
        self.execute_orders()
    



class Trader(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cash = 1000  # Initial cash
        self.shares = 0  # Initially holds no stock
    
    def step(self):
        """Trader makes a buy or sell decision each step."""
        decision = random.choice(['buy', 'sell', 'hold'])
        if decision == 'buy' and self.cash >= self.model.price:
            self.model.order_book.append('buy')
            self.cash -= self.model.price
            self.shares += 1
        elif decision == 'sell' and self.shares > 0:
            self.model.order_book.append('sell')
            self.cash += self.model.price
            self.shares -= 1

# Run the simulation
market = Simulated_Market(num_traders=10, initial_price=100)
for _ in range(100):  # Simulate 100 time steps
    market.step()
    print(f"Time {_}: Price = {market.price:.2f}")
