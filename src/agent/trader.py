from mesa.discrete_space import FixedAgent
from random import random
from src.model.model import TraderState  # Waiting for model implementation to import this


class TraderAgent(FixedAgent):
    def __init__(self, unique_id, model, capital, strategy, win_rate):
        super().__init__(unique_id, model)

    
        self.capital = capital
        self.strategy = strategy  # Callable strategy function
        self.win_rate = win_rate  # Float (0 to 1)
        self.state = TraderState.HAS_CAPITAL if capital > 0 else TraderState.ZERO_CAPITAL

    def trade_action(self, market_prices):
        """
        Executes a trade action based on strategy decision.
        """
        # Strategy decides Buy (True) or Sell (False)
        decision = self.strategy(market_prices)

        # Probabilistic trade outcome
        trade_success = random() < self.win_rate
        trade_amount = 10  # An example fixed trade size

        if decision:  # Buy
            self.capital += trade_amount if trade_success else -trade_amount
        else:  # Sell
            self.capital += trade_amount * 0.5 if trade_success else -trade_amount * 0.5

        # Update state
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
        market_prices = self.model.market_prices  # Expect this to be provided by the model (?)
        self.trade_action(market_prices)

        # A debug print (optional, can be commented out)
        print(f"Agent {self.unique_id}: Capital = {self.capital}, State = {self.state}")

