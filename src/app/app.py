# Created in Mesa 3.2.0.dev0| Python 3.13.2

# Run by Typing "solara run src/app/app.py" into the terminal

# Importing Libraries 
import numpy as np
## Local Agent Library
from mesa.examples.basic.boltzmann_wealth_model.model import BoltzmannWealth # Replace with our model
from src.model import model as AgentPortfolioModel

## Data Logging and Visualisation Libraries
from mesa.mesa_logging import INFO, log_to_stderr
from mesa.visualization.utils import update_counter
from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component,
)
import solara
from matplotlib.figure import Figure



"""[0] Setting Up Environment"""

# [0.1] Logging Events to Terminal
log_to_stderr(INFO)

# [0.2] -> [1] Demo | [0] Custom
custom_env = 1


"""[1] Gathering Data for Visualisation""" # -> Turn into a class
# [1.1] Gathering Agent Capital Data
def get_agent_capital(model):
    # Testing [1]
    if custom_env == 1:
        wealth_list = []
        for agent in model.agents:
            wealth_list.append(agent.wealth)

        return wealth_list
    
    # Custom [0]
    elif custom_env == 0:
        capital_list = []
        for agent in model.agents:
            capital_list.append(agent.capital)

        return capital_list

# [1.2] Gathering Asset Price Data


# [1.3] Visual representation of Agent in the Simulation
def agent_representation(agent): # WIP
    """ 
    A Colourmap will be used to translate an agent feature into colour. This could be
    one of the following:
    - Agent's portfolio (Capital)
    - Agent's Capital State
    - Agent's Wealth

    """

    colour = agent.wealth # CHANGE FOR OUR AGENT
    # colour = agent.capital  
    return {"colour": colour}


# Model Parameters
model_params = {
    "seed": {
        "type": "InputText",
        "value": 1,
        "label": "Random Seed",
    },

    "n": {
        "type": "SliderInt",
        "value": 300,
        "label": "Number of agents:",
        "min": 30,
        "max": 3000,
        "step": 30,
    },
    
    "width": 10,
    "height": 10,
}


""" Reprogram from here"""

def post_process(ax):
    ax.get_figure().colorbar(ax.collections[0], label="Capital Value", ax=ax)


# Create initial model instance with Initial Paramters
model = BoltzmannWealth(10, 10, 10)

# Custom Model
if custom_env == 0:
    model = AgentPortfolioModel(
        n=300,
        seed=1
    )

""" [3] Create visualization """
class visuals:
    # [3.1] Initialising Variables
    def __init__(self, model):
        self.model = model

    # [3.2] Create Capital Histagram Component
    @solara.component
    def CapitalHistogram(model):
        # Update the agent counter
        update_counter.get() 

        # Initialise Figure
        fig = Figure()
        ax = fig.subplots()
        capital_values = get_agent_capital(model)
        ax.hist(capital_values, bins=10, color='blue')
        
        # Labeling Chart and Axis
        ax.set_title("Agent Capital Histogram")
        ax.set_xlabel("Capital Ranges")
        ax.set_ylabel("Number of Agents")
        
        # Simulate
        solara.FigureMatplotlib(fig)

    # [3.3] Create Capital Yield Component
    agent_capital_history = {}
    @solara.component
    def CapitalYield(model):
        # Reactive state for capital history and reset trigger
        reset_key, set_reset_key = solara.use_state(0)
        visuals.agent_capital_history, set_agent_capital_history = solara.use_state({})

        # Automatically reset agent_capital_history when model changes
        solara.use_effect(lambda: set_agent_capital_history({}), [model])    

        # Update the agent counter
        update_counter.get() 

        # Initialise Figure
        fig = Figure()
        ax = fig.subplots()

        # Get capital values for all agents at the current timestep
        capital_values = get_agent_capital(model)

        # Ensure each agent has a history storage
        for agent_id in range(len(capital_values)):
            if agent_id not in visuals.agent_capital_history:
                visuals.agent_capital_history[agent_id] = []  # Initialize empty list for new agents

        # Append the current timestep's capital value for each agent
        for agent_id, capital in enumerate(capital_values):
            visuals.agent_capital_history[agent_id].append(capital)


        # Plot each agent's capital over time
        for agent_id, capital_series in visuals.agent_capital_history.items():
            ax.plot(range(len(capital_series)), capital_series, linestyle="-", alpha=0.5)


        # Labeling Chart and Axis
        ax.set_title("Agent Capital Over Time")
        ax.set_xlabel("Timesteps")
        ax.set_ylabel("Capital")
        ax.grid(True, linestyle="-", alpha=0.3)

        # Show plot in Solara
        solara.FigureMatplotlib(fig)





# SpaceGraph shows the spatial distribution of agents based on their portfolio values.
SpaceGraph = make_space_component(
    agent_representation, cmap="viridis", vmin=0, vmax=10, post_process=post_process
)
# PortfolioPlot shows how the distribution of portfolio values evolves over time.
#PortfolioPlot = make_plot_component("Portfolio Distribution")

GiniPlot = make_plot_component("Gini")

# Create the SolaraViz page to serve the interactive visualizations.e
page = SolaraViz(
    model,
    components=[visuals.CapitalHistogram, visuals.CapitalYield, SpaceGraph, GiniPlot],
    model_params=model_params,
    name="Agent Portfolio Optimisation",
)
page









