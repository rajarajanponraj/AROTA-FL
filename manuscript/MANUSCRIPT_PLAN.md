  # Manuscript Plan and 5-Page IEEE Layout Budget: AROTA-FL

## 1. Publication Target and Format
- **Document Class**: `\documentclass[journal, twocolumn]{IEEEtran}` (or `lettersize, journal`)
- **Target Page Count**: Exactly 5 rendered pages, fully utilizing two columns with balanced references on Page 5.
- **Figures**: Clean vector EPS or high-resolution PNG, embedded with appropriate subfigures and explicit captions.
- **Bibliography Style**: `IEEEtran.bst` using verified entries from `references.bib`.

---

## 2. Page-by-Page Budget and Structural Blueprint

### Page 1: Motivation and Problem Statement
- **Title**: *Convergence-Aware Active RIS for AirComp-Based Federated Learning Under Imperfect CSI*
- **Author Block**: Academic presentation preserving research affiliation context.
- **Abstract** (approx. 200–250 words):
  - Context: Edge AI and communication bottleneck of Federated Learning (FL).
  - Approach: Over-the-Air Computation (AirComp) with Active Reconfigurable Intelligent Surfaces (RIS).
  - Core Issue: Active RIS amplifies thermal noise; naive instantaneous MSE minimization compounds CSI estimation errors, causing severe FL divergence.
  - Proposed Solution: Statistically derived Convergence-Aware optimization framework directly bounding FL aggregation error.
  - Key Findings: Quantified MSE reduction (~10x under high CSI uncertainty), dynamic amplification back-off, ~3x convergence speedup, and robust non-IID classification accuracy.
- **Index Terms**: Active RIS, Over-the-Air Computation, Federated Learning, Imperfect CSI, Edge Intelligence, Convergence Analysis.
- **Section I: Introduction**:
  - Subsection A: Background on Edge Intelligence and FL Communication Bottlenecks.
  - Subsection B: AirComp and the Role of RIS (Passive vs. Active).
  - Subsection C: The Imperfect CSI Dilemma in Active-RIS AirComp.
  - Subsection D: Novelty Boundary and Concrete Contributions (Mathematical derivation of expected error penalty, closed-form ZF reduction, $\mathcal{O}(N^2)$ algorithmic formulation, extensive physical + learning layer validation).
  - Subsection E: Organization of the Manuscript.

### Page 2: System Architecture and Mathematical Model
- **Section II: System Model**:
  - Subsection A: Network Architecture ($K$ clients, $N$-element Active RIS, single-antenna AP).
  - Subsection B: Federated Learning Objective and Local Gradient Computation.
  - Subsection C: Wireless Propagation and CSI Estimation Error Model ($\hat{\mathbf{h}}_k = \mathbf{h}_k + \mathbf{e}_k$, $\mathbf{e}_k \sim \mathcal{CN}(0, \sigma_e^2 \mathbf{I}_N)$).
  - Subsection D: Active RIS Reflection and Thermal Noise Model ($\mathbf{\Theta} = a \operatorname{diag}(e^{j\theta_n})$, $\mathbf{n}_R \sim \mathcal{CN}(0, \sigma_R^2 \mathbf{I}_N)$).
  - Subsection E: Over-the-Air Signal Superposition and Receive Scaling ($y, \hat{s} = c y$).
- **Visual Element**:
  - Fig. 1: System and Signal Processing Architecture of Active-RIS-assisted AirComp FL.

### Page 3: Problem Formulation, Bound Derivation, and Algorithm
- **Section III: Problem Formulation and Convergence-Aware Bound**:
  - Subsection A: True Instantaneous Mean Squared Error (MSE).
  - Subsection B: Failure of the Naive MSE-Minimizing Baseline under Channel Uncertainty.
  - Subsection C: Derivation of the Convergence-Aware Expected MSE ($J_t$).
  - Subsection D: Mathematical Linkage to Global FL Convergence ($L$-smooth descent guarantee).
- **Section IV: Joint Optimization Algorithm and Complexity**:
  - Subsection A: Closed-Form Zero-Forcing Transceiver Precoding ($b_k, c$).
  - Subsection B: Multi-Start Bound-Constrained Optimization (SLSQP / L-BFGS-B over $a$ and $\boldsymbol{\theta}$).
  - Subsection C: Computational Complexity Analysis ($\mathcal{O}(N^2)$ vs $\mathcal{O}(N^{4.5})$ for SDR).
- **Table I**: Simulation and Wireless Channel Parameters.

### Page 4: Experimental Performance Evaluation
- **Section V: Numerical Results and Discussion**:
  - Subsection A: Physical-Layer Communication Performance:
    - Exp 1: Expected MSE vs. Amplification Factor $a_{\max}$ (Trade-off and sweet-spot clamping).
    - Exp 2 & 3: Transmit Power Budget ($P_{\max}$) and Dynamic Amplification Back-off ($a^*$).
    - Exp 4: CSI Estimation Uncertainty Sweep ($\sigma_e^2 \in [0, 0.30]$).
    - Exp 5 & 6: Impact of RIS Elements ($N$) and Multi-User Scalability ($K$).
- **Visual Elements**:
  - Multi-panel figure or side-by-side plots:
    - Fig. 2: Aggregation MSE vs. Amplification Factor and CSI Error Variance.
    - Fig. 3: Optimal Amplification Factor vs. Transmit Power Budget ($P_{\max}$).

### Page 5: Federated Learning Validation, Conclusion, and References
- **Section V (Continued): End-to-End Learning Performance**:
  - Subsection B: Federated Learning Convergence and Accuracy:
    - Exp 7–9: MNIST Non-IID Learning Curves (Ideal vs. Naive MSE-Min vs. Proposed Conv-Aware).
    - Exp 10: CIFAR-10 Benchmark under Severe Heterogeneity.
  - Subsection C: Technical Insights, Practical Limitations, and Design Guidelines.
- **Visual Elements**:
  - Fig. 4: Top-1 Test Accuracy vs. Communication Rounds for MNIST and CIFAR-10.
- **Section VI: Conclusion**:
  - Summary of contributions, confirmed performance gains, operational takeaways, and logical future research avenues.
- **References**:
  - Two-column balanced bibliography containing 20+ fully verified, complete IEEE citations with active DOIs and accurate metadata.
