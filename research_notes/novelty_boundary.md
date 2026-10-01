# Novelty Boundary

## What is NOT Novel
1. **Active RIS:** The general concept of an Active RIS, its hardware architectures, and reflection-amplification models are already established in the literature.
2. **Over-the-Air Computation (AirComp):** Analog aggregation of superimposed signals over multiple access channels is a well-known concept for fast aggregation.
3. **Wireless Federated Learning (AirFL):** Performing Federated Learning over AirComp has been heavily studied as a promising solution for massive IoT systems.
4. **Active-RIS AirComp / AirFL:** Recent contemporary works have proposed integrating an active RIS to assist AirComp or AirFL to mitigate the "multiplicative fading" (double-fading) attenuation problem typical of passive RIS structures.

## What IS Novel (The Scope of this Project)
This research strictly isolates its novelty to the **control strategy under imperfect CSI**.

- Existing Active-RIS AirFL investigations traditionally design their transmit scalars, receive scalars, and active-RIS amplification/phase shifts to minimize the instantaneous estimated AirComp MSE, broadly operating under the assumption of perfect Channel State Information (CSI).
- **Our Hypothesis:** Under imperfect CSI compounded with active-RIS amplification noise, the configuration that minimizes the *estimated* instantaneous AirComp MSE is not necessarily the identical configuration that minimizes the degradation of the end-to-end FL convergence. 
- **Proposed Objective:** We design a **Convergence-Aware Joint Active-RIS and Transceiver Optimization** scheme that inherently accounts for statistical CSI uncertainty. We hypothesize (and intend to demonstrate via simulation) that penalizing extreme active-RIS amplification when CSI uncertainty is high prevents severe instantaneous aggregation errors, yielding a demonstrably superior end-to-end FL convergence compared to naive MSE-minimization.

We explicitly do not claim that the combination of Active RIS and AirFL is novel. We assert that *convergence-aware control of Active RIS AirFL under imperfect CSI* presents a critical divergence from the standard MSE-minimizing control, and this project aims to quantify and statistically validate that distinction.
