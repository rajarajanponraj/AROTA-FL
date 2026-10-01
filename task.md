# Project Tasks

## Completed Tasks
- [x] **Phase 1:** Mathematical model, assumptions, and novelty boundary.
- [x] **Phase 2:** Channel simulator (`rayleigh.py`, `channel_estimation.py`, `channel_utils.py`, tests).
- [x] **Phase 3:** Active/Passive RIS models and phase control (`active_ris.py`, `passive_ris.py`, `phase_control.py`, `ris_power.py`, tests).

## Phase 3.5: Realistic Channel Models (Enhancements)
- [x] Implement distance-dependent Path Loss model.
- [x] Implement Rician Fading for LoS links (e.g., RIS-to-AP).

## Phase 4: AirComp Received Signal
- [x] Implement transmit/receive beamforming/scaling (`src/aircomp/beamforming.py`).
- [x] Implement AirComp signal generation with noise (`src/aircomp/received_signal.py`).
- [x] Add unit tests for signal generation and shapes.

## Phase 5: MSE Validation
- [x] Implement analytical MSE calculation (`src/aircomp/mse.py`).
- [x] Implement empirical Monte Carlo MSE validation.
- [x] Create `test_mse.py` to ensure analytical and empirical MSE match.

## Phase 6: Initial Baselines
- [x] Implement No-RIS baseline.
- [x] Implement Passive-RIS baseline.
- [x] Implement Fixed Active-RIS baseline.
- [x] Implement Total Power Budget constraint for fair Active vs Passive comparison.
- [x] Validate baselines (`src/optimization/baselines.py`).

## Phase 7: MSE-Minimization Baseline
- [x] Implement naive instantaneous MSE minimization (e.g., using grid search/alternating optimization) over $\{a, \Theta, b_k, c\}$ (`src/optimization/mse_minimization.py`).
- [x] Write unit tests to verify MSE-Min finds a lower MSE than a random configuration.

## Phase 8: Federated Learning Simulator
- [x] Set up PyTorch models for MNIST, Fashion-MNIST, and CIFAR-10 (`src/federated_learning/model.py`).
- [x] Implement IID/Non-IID dataset partitioning (`src/federated_learning/partition.py`).
- [x] Implement Client local training step (`src/federated_learning/client.py`).
- [x] Implement Server global update step (`src/federated_learning/server.py`).

## Phase 9: AirComp-FL Integration
- [x] Connect AirComp aggregation error model directly into FL weight updates (`src/aircomp/aggregation.py`).
- [x] Test that varying error variance appropriately degrades FL accuracy.

## Phase 10: Proposed Convergence-Aware Controller
- [x] Implement the expected-MSE objective bounding the aggregation error (`src/optimization/convergence_aware.py`).
- [x] Implement optimizer to find optimal convergence-aware configuration.
- [x] Formulate and document the optimization algorithm (e.g., AO/SCA) and analyze its Big-O complexity.

## Phase 11-13: Experiments
- [x] **Exp 1:** MSE vs Amplification ($a=1.0$ to $a_{max}$).
- [x] **Exp 2:** MSE vs SNR (0 to 30 dB).
- [x] **Exp 3:** Amplification vs SNR (compare MSE-Min vs Convergence-Aware optimal gains).
- [x] **Exp 4:** CSI Error sweep (0.0 to 0.30).
- [x] **Exp 5:** RIS Size sweep ($N \in \{16, 32, 64, 128\}$).
- [x] **Exp 6:** Client Count sweep ($K \in \{5, 10, 20\}$).
- [x] **Exp 7 & 8:** FL Convergence under IID vs Non-IID.
- [x] **Exp 9:** Monte Carlo repetitions (30+ seeds).
- [x] **Exp 10:** FL Convergence on complex datasets (Fashion-MNIST or CIFAR-10).

## Phase 14-15: Analysis and Reporting
- [x] Generate standard metrics, tables, and visualization figures (`src/metrics/`, `results/figures/`).
- [x] Compile automated research report summarizing findings.
