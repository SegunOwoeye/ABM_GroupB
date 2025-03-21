from mesa.discrete_space import FixedAgent
import random
from enum import Enum
import numpy as np


# State class to indicate the state of each trader agent. "Broke" or "with some money".
class TraderState(Enum):
    ZERO_CAPITAL = 0
    HAS_CAPITAL = 1

""" Trade Strategies"""
# Random Strategy
def random_strategy():
    # randomly chooses True (Buy Signal) or False (Sell Signal)
    return random.choice([True, False])

# RSI Strategy
def rsi_strategy(prices, period=14, lower_threshold=30, upper_threshold=70):
    # Checks to see if there is enough data to compute RSI
    if len(prices) < period + 1:
        return None 

    deltas = np.diff(prices[-(period+1):])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    
    # Signals
    if rsi < lower_threshold:
        return True  # Buy
    elif rsi > upper_threshold:
        return False  # Sell
    else:
        return None  # Hold


# SMA Strategy
def sma_strategy(prices, period=28):
    # Checks to see if there is enough data to compute SMA
    if len(prices) < period + 1:
        return None  

    sma = np.mean(prices[-(period+1):-1])  # Compute SMA from previous N prices
    current_price = prices[-1]
    
    # Signals
    if current_price > sma:
        return True  # Buy
    elif current_price < sma:
        return False  # Sell
    else:
        return None  # Hold

# Bollinger Band Strategy -> Mean Reverting
def bollinger_strategy(prices, period=20, num_std_dev=2):
    # Checks to see if there is enough data to compute Bollinger Bands
    if len(prices) < period:
        return None  

    recent_prices = prices[-period:]
    sma = np.mean(recent_prices)
    std = np.std(recent_prices)

    upper_band = sma + num_std_dev * std
    lower_band = sma - num_std_dev * std
    current_price = prices[-1]
    
    # Signal
    if current_price < lower_band:
        return True  # Buy
    elif current_price > upper_band:
        return False  # Sell
    else:
        return None  # Hold



# Strategy Selector
def trader_strategy(price_history=None, strategy_type="random", **kwargs):
    if strategy_type == "random":
        return random_strategy()
    elif strategy_type == "rsi":
        return rsi_strategy(price_history, **kwargs)
    elif strategy_type == "sma":
        return sma_strategy(price_history, **kwargs)
    elif strategy_type == "bollinger":
        return bollinger_strategy(price_history, **kwargs)


class TraderAgent(FixedAgent):
    def __init__(self, model, capital, strategy_type, win_rate, market_prices, generocity_rate, cell, strategy_params=None):
        super().__init__(model)
        self.capital = capital
        self.strategy_type = strategy_type  # Callable strategy function
        self.strategy_params = strategy_params or {}
        self.win_rate = win_rate  # Float (0 to 1)
        self.market_prices = market_prices
        self.price_memory = self.market_prices[0]
        self.generocity_rate = generocity_rate
        self.cell = cell
        self.state = TraderState.HAS_CAPITAL if round(capital) >= 0 else TraderState.ZERO_CAPITAL

    def trade_action(self):
        """
        Executes a trade action based on strategy decision.
        """
        # Prevent agent from trading if out of capital
        if self.state == TraderState.ZERO_CAPITAL:
            return


        # Strategy decides Buy (True) or Sell (False)
        decision = trader_strategy(self.market_prices, self.strategy_type, **self.strategy_params)
        
        # Hold - no action
        if decision is None:
            return  

        index = 0
        continue_flag = True

        while index < len(self.market_prices) and continue_flag:
            if decision:
                if self.price_memory*1.001 <= self.market_prices[index]:
                    self.capital += (self.market_prices[index] - self.price_memory)
                    self.win_rate += 1
                    continue_flag = False

                elif self.price_memory*0.0090 >= self.market_prices[index]:
                    self.capital -= (self.price_memory - self.market_prices[index])
                    continue_flag = False

            else:
                if self.price_memory*1.001 <= self.market_prices[index]:
                    self.capital -= (self.market_prices[index] - self.price_memory)
                    continue_flag = False

                elif self.price_memory*0.0090 >= self.market_prices[index]:
                    self.capital += (self.price_memory - self.market_prices[index])
                    self.win_rate += 1
                    continue_flag = False

            index += 1
            
        # Update state
        self.state = TraderState.HAS_CAPITAL if self.capital > 0 else TraderState.ZERO_CAPITAL


    # Change function below to randomly give capital to the agent with the highest winrate
    def try_to_share_capital(self):
        successful_agent = None
        max_winrate = 0

        for agent in self.cell.neighborhood.agents:
            if agent.win_rate > max_winrate:
                max_winrate = agent.win_rate
                successful_agent = agent

        if successful_agent is not None and successful_agent is not self:
            if self.random.random() < self.generocity_rate:
                if self.capital <= 1:
                    successful_agent.capital += self.capital
                    self.capital -= self.capital
                    print(f"Agent {self.unique_id} just gave {self.capital} capital to {successful_agent.unique_id} with winrate: {successful_agent.win_rate}.")
                else:
                    successful_agent.capital += self.capital*0.01
                    self.capital -= self.capital*0.01
                    print(f"Agent {self.unique_id} just gave {self.capital*0.01} capital to {successful_agent.unique_id} with winrate: {successful_agent.win_rate}.")

        self.state = TraderState.HAS_CAPITAL if self.capital > 0 else TraderState.ZERO_CAPITAL
            

        

    def adjust_capital(self, amount):
        """
        Adjusts capital directly (e.g., for sharing mechanisms).
        """
        self.capital += amount
        self.state = TraderState.HAS_CAPITAL if self.capital > 0 else TraderState.ZERO_CAPITAL

    def get_capital(self):
        return self.capital

    def get_state(self):
        return self.state

    def step(self):
        """
        Step function called by scheduler each time step.
        """  
        # Skip step if agent has zero capital
        if self.state == TraderState.ZERO_CAPITAL:
            # A debug print (optional, can be commented out)
            print(f"Agent {self.unique_id} is out of capital and has stopped trading.")
            return

        self.trade_action()

        if self.state is TraderState.HAS_CAPITAL:
            self.try_to_share_capital()

        # A debug print (optional, can be commented out)
        print(f"Agent {self.unique_id}: Capital = {self.capital}, State = {self.state}, Price Memory = {self.price_memory}")



