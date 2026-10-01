# AROTA-FL: Federated Learning over Over-the-Air Computation (AirComp) with Reconfigurable Intelligent Surfaces (RIS)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/AROTA-FL/blob/main/Run_on_Colab.ipynb)

This repository contains the source code for simulating Federated Learning (FL) via Over-the-Air Computation (AirComp) assisted by a Reconfigurable Intelligent Surface (RIS). 

## Running on Google Colab

For journal reproducibility, the computationally heavy simulations (e.g., CIFAR-10) can be executed easily using Google Colab's free GPUs. 

Click the **Open In Colab** badge above to launch the simulation environment directly in your browser. The notebook automatically clones this repository, installs dependencies, and runs the required experiments.

## Local Setup

If you prefer to run the code locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AROTA-FL.git
   cd AROTA-FL
   ```
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the experiments (e.g., MNIST sweeps):
   ```bash
   python -m experiments.run_fl_sweeps
   ```

## Repository Structure
- `src/`: Contains the core FL algorithms, AirComp models, and RIS logic.
- `experiments/`: Scripts for executing various simulation scenarios.
- `docs/` & `theory/`: Documentation and mathematical models.
- `tests/`: Unit tests.
