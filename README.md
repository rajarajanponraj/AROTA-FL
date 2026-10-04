# Convergence-Aware Active RIS for AirComp-Based Federated Learning

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/AROTA-FL/blob/main/Run_on_Colab.ipynb)

This repository contains the source code for simulating **Convergence-Aware Active Reconfigurable Intelligent Surfaces (RIS)** for **Over-the-Air Computation (AirComp)** based **Federated Learning (FL)**. 

The project investigates a novel convergence-aware optimization scheme for Active RIS-assisted AirComp, comparing it against traditional MSE-Minimization and standard baselines (No-RIS, Passive-RIS).

## Features

- **Channel Models:** Distance-dependent path loss and realistic Rician/Rayleigh fading, handling imperfect Channel State Information (CSI).
- **RIS Configurations:** Supports both Passive RIS and Active RIS (including thermal noise and total power budget constraints).
- **AirComp Integration:** Full signal generation, transmission beamforming, scaling, and analytical vs. empirical Mean Squared Error (MSE) validation.
- **Optimization Baselines:**
  - No-RIS, Passive-RIS, and Fixed Active-RIS baselines.
  - Naive Instantaneous MSE-Minimization.
  - Proposed Convergence-Aware controller that optimizes expected MSE to guarantee FL convergence.
- **Federated Learning Simulator:**  
  - Built with PyTorch.
  - Supported datasets: MNIST, Fashion-MNIST, and CIFAR-10.
  - Supports both IID and Non-IID data partitioning.

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

## Running Experiments

The `experiments/` directory contains several scripts for executing the simulation scenarios:

- **Wireless and Optimization Sweeps:**
  Run MSE vs SNR, MSE vs Amplification, CSI error sweeps, etc.
  ```bash
  python -m experiments.run_wireless_sweeps
  ```

- **Federated Learning Sweeps:**
  Run FL convergence simulations under various channel conditions (MNIST/Fashion-MNIST).
  ```bash
  python -m experiments.run_fl_sweeps
  python -m experiments.run_fl_extra_sweeps
  ```

- **CIFAR-10 Experiments:**
  Run intensive FL convergence simulations on CIFAR-10.
  ```bash
  python -m experiments.run_cifar10_exp10
  ```

## Repository Structure

- `src/channels/`: Channel simulators (Rician fading, path loss, CSI estimation).
- `src/ris/`: Active and Passive RIS modeling (phase control, power constraints).
- `src/aircomp/`: AirComp transmission, beamforming, and MSE calculation.
- `src/optimization/`: Optimization controllers (MSE-minimization, Convergence-aware, Baselines).
- `src/federated_learning/`: FL simulator (PyTorch models, partition logic, client/server steps).
- `experiments/`: Scripts for executing various wireless and FL simulation scenarios.
- `docs/` & `theory/`: Documentation, assumptions, and mathematical models.
- `tests/`: Unit tests ensuring the correctness of the analytical models and simulators.
