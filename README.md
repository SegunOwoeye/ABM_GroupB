
# Agent-Based Modelling – Group B

This repository contains the agent-based model (ABM) developed for the 7CCSMAMF coursework at King's College London. The model simulates capital dynamics within a networked financial system to explore emergent behaviors such as wealth inequality, systemic risk, and the effects of network topology.

## Project Structure

- **`test_src/`**  
  The core simulation engine. All experiments and analyses were conducted using the code in this directory.

- **`src/`**  
  Initial prototypes and legacy code.

- **`data/`**  
  Contains input datasets and output results from simulation runs.

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SegunOwoeye/ABM_GroupB.git
   cd ABM_GroupB/test_src
   ```


2. **Run simulations:**

   Execute the main simulation script:

   ```bash 
   solara run test_src/app/app.py
   ```


## Key Findings

- **Capital Convergence:** A subset of agents consistently amass capital, dominating the system.

- **Leader-Follower Clusters:** Dominant agents attract capital and influence from neighboring agents, resembling herding behavior.

- **Wealth Inequality:** Significant disparities emerge despite uniform initial conditions and strategies.

- **Network Density Effects:**
  - *Sparse networks* lead to isolated agent failures.
  - *Dense networks* result in synchronized collapses due to high interconnectivity.

- **Redistribution Dynamics:** Targeted redistribution can mitigate collapse risks and inequality, but excessive redistribution dampens performance differentiation.


```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
