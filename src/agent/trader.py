from mesa import Agent, Model
from mesa.time import RandomActivation
import random
import numpy as np

# -	Simulate traders with different trading strategies for portfolio optimisation

class Traders(Agent):
    """ [1] - Initialising Variables """
    def __init__(self, trader_ID: int, model: str, strategy: str, initial_funds: float = 10000, 
                 initial_shares: float = 0):
        super().__init__(trader_ID, model)
        self.strategy = strategy # Trading Strategy
        self.funds = initial_funds # Initial Money for Investment
        self.shares = initial_shares # Initially holds no stock

        # Initial Portfolio Value
        self.portfolio_value = self.funds 
    
    
    """ [2] - Trading Strategies"""
    # Random Trading
    def random_trade(self):
        # Agent Randomly chooses to buy, hold or sell a stock
        trade_decisions = ["buy", "hold", "sell"] 
        agents_decision = random.choice(trade_decisions)

        #if agents_decision == "buy" and self.funds >=
    
    # SMA Trading
    def sma_trade(self):
        pass
    
    # Machine Learning Trading
    def ml_trade(self):
        pass
    
    """ [3] - Updating the Value of the Portfolio """
    def update_portfolio(self):
        self.portfolio_value = self.funds + (self.shares * self.model.market.price)
    


    """ [3] Execute a step for the agent """
    def step(self):
        """Agent makes a buy/sell decision based on their strategy to optimise their portfolio """

        # Random Strategy
        if self.strategy.lower() == "random":
            self.random_trade()

        # SMA Strategy
        elif self.strategy.lower() == "sma":
            self.sma_trade()

        # Machine Learning Strategy
        elif self.strategy.lower() == "ml":
            self.ml_trade()

        # Updates Portfolio Value
        