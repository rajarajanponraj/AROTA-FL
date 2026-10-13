# Evidence Register: AROTA-FL

This register establishes a single source of truth linking every experimental and analytical result to its underlying codebase module, simulation configuration, data outputs, and baseline comparisons.

---

## 1. Experimental Evidence Register

| Exp ID | Research Hypothesis & Focus | Source Script | Key Configurations & Parameters | Evaluation Metric | Baselines Evaluated | Output File / Figure | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-01** | Increasing active RIS maximum gain $a_{\max}$ causes naive MSE minimization to diverge due to amplified thermal and CSI error noise, whereas Convergence-Aware control clamps amplification. | `experiments/run_wireless_sweeps.py` (`run_exp1_mse_vs_amplification`) | $K=10$, $N=32$, $d_{AP} \in [100, 150]$ m, $d_{RIS,k} \in [20, 50]$ m, $d_{RIS,AP}=80$ m, $P_{\max}=10$ dBm, $\sigma_0^2=-90$ dBm ($10^{-12}$ W), $\sigma_R^2=-80$ dBm ($10^{-11}$ W), $\sigma_e=0.1$, $a_{\max} \in [1.0, 20.0]$, 500 seeds. | Expected Aggregation MSE ($J_t$) [log scale] | Passive RIS, Fixed Active RIS, MSE-Min Active RIS | `results/figures/exp1_mse_vs_amp.eps`, `exp1_mse_vs_amplification.eps` | **Verified**: Naive MSE-Min diverges past $a_{\max} \approx 6.0$, whereas Proposed Conv-Aware maintains stable minimum error. |
| **EXP-02** | As transmit power $P_{\max}$ (SNR) increases, aggregation MSE decreases across all architectures, with Convergence-Aware maintaining superiority. | `experiments/run_wireless_sweeps.py` (`run_exp2_3_snr_sweep`) | $K=10$, $N=32$, $a_{\max}=15.0$, $\sigma_e=0.1$, $\sigma_0=10^{-6}$, $\sigma_R=3.16 \times 10^{-6}$, $P_{\max} \in [-10, 30]$ dBm, 500 seeds. | Expected Aggregation MSE ($J_t$) | Passive RIS, MSE-Min Active RIS | `results/figures/exp2_mse_vs_snr.eps` | **Verified**: At high SNR ($P_{\max} \ge 10$ dBm), Conv-Aware achieves $>15$ dB lower MSE than naive MSE-Min. |
| **EXP-03** | At low SNR, both schemes maximize gain $a$, but at high SNR, Convergence-Aware automatically backs off $a$ to suppress amplified CSI error. | `experiments/run_wireless_sweeps.py` (`run_exp2_3_snr_sweep`) | Identical to EXP-02 ($P_{\max} \in [-10, 30]$ dBm, $a_{\max}=15.0$, 500 seeds). | Optimal Active RIS Amplification Factor ($a^*$) | MSE-Min Active RIS vs. Proposed Conv-Aware | `results/figures/exp3_amp_vs_snr.eps` | **Verified**: MSE-Min saturates at $a=15.0$ constantly, while Conv-Aware smoothly reduces $a$ from $15.0$ down to $1.2$ as $P_{\max}$ grows. |
| **EXP-04** | Increasing CSI estimation error $\sigma_e^2$ degrades MSE-Min catastrophically, while Convergence-Aware adaptively attenuates gain. | `experiments/run_wireless_sweeps.py` (`run_exp4_csi_error_sweep`) | $K=10$, $N=32$, $P_{\max}=10$ dBm, $a_{\max}=15.0$, $\sigma_e^2 \in [0.0, 0.30]$, 500 seeds. | Expected Aggregation MSE ($J_t$) | MSE-Min Active RIS vs. Proposed Conv-Aware | `results/figures/exp4_csi_sweep.eps` | **Verified**: At $\sigma_e^2 = 0.3$, Conv-Aware achieves ~10x lower MSE than naive MSE-Min. |
| **EXP-05** | Scaling RIS elements $N$ enhances beamforming gain for both passive and active architectures, with Conv-Aware retaining optimal scaling. | `experiments/run_wireless_sweeps_2.py` (`run_exp5_ris_size_sweep`) | $K=10$, $N \in \{16, 32, 64, 128\}$, $P_{\max}=10$ dBm, $\sigma_e=0.1$, $a_{\max}=15.0$, 500 seeds. | Expected Aggregation MSE ($J_t$) | Passive RIS, MSE-Min Active RIS, Proposed Conv-Aware | `results/figures/exp5_ris_size.eps` | **Verified**: Confirms monotonic error reduction with increasing $N$; Conv-Aware outperforms Passive by ~20 dB and MSE-Min by ~6 dB. |
| **EXP-06** | AirComp bottleneck effect worsens as client count $K$ increases; Conv-Aware scales robustly. | `experiments/run_wireless_sweeps_2.py` (`run_exp6_client_count_sweep`) | $N=32$, $K \in \{5, 10, 20\}$, $P_{\max}=10$ dBm, $\sigma_e=0.1$, $a_{\max}=15.0$, 500 seeds. | Expected Aggregation MSE ($J_t$) | MSE-Min Active RIS vs. Proposed Conv-Aware | `results/figures/exp6_client_count.eps` | **Verified**: With $K=20$, MSE-Min error increases sharply due to weak client scaling penalty; Conv-Aware remains resilient. |
| **EXP-07-09** | Physical AirComp aggregation errors degrade end-to-end FL learning curves; Conv-Aware accelerates convergence and achieves near-ideal accuracy. | `experiments/run_fl_sweeps.py` (`run_exp7_8_9`) | MNIST CNN, $K=20$ clients, 60 rounds, $\eta=0.01$, batch size 64, Non-IID Dirichlet $\alpha=0.5$, $\sigma_e=0.1$, multi-seed (3-30 seeds). | Top-1 Test Accuracy (%) & Variance Shading over Rounds | Ideal Noise-Free Channel (IID & Non-IID), Non-IID MSE-Min Active RIS | `results/figures/exp7_9_fl_convergence.eps`, `exp7_9_fl_convergence_stat.eps` | **Verified**: Conv-Aware reaches ~97.8% accuracy closely tracking the ideal non-IID curve, while MSE-Min oscillates heavily around 91-93%. |
| **EXP-10** | Complex image classification (CIFAR-10) under severe non-IID data partitions confirms robustness of proposed framework. | `experiments/run_cifar10_exp10.py` (`run_exp10_cifar10`) | CIFAR-10 CNN, $K=20$ clients, 100 rounds, $\eta=0.01$, batch size 32, Dirichlet $\alpha=0.5$, $\sigma_e=0.1$. | Top-1 Test Accuracy (%) over 100 rounds | Ideal Channel, MSE-Min Active RIS | `docs/dreft/results_figures/results/figures/exp10_cifar10_convergence.png` | **Verified**: Conv-Aware avoids catastrophic divergence, achieving ~62% final test accuracy compared to ~48% for naive MSE-Min. |

---

## 2. Analytical and Derived Evidence

1. **Analytical AirComp MSE Closed-Form**:
   - Proven in `theory/derivations.md` (Section 1) and implemented in `src/aircomp/mse.py:compute_analytical_mse`.
   - Expression:
     $$\text{MSE} = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2$$
   - Verification: Rigorously cross-validated via Monte Carlo unit tests in `tests/test_mse.py` with tolerance $< 10^{-4}$.

2. **CSI Uncertainty Bounded Aggregation Objective ($J_t$)**:
   - Proven in `theory/derivations.md` (Section 3) and implemented in `src/optimization/convergence_aware.py`.
   - Statistical expectation over $e_k \sim \mathcal{CN}(0, \sigma_e^2 I_N)$:
     $$J_t = \widehat{\text{MSE}} + |c|^2 \|G^H \Theta\|^2 \sigma_e^2 \sum_{k=1}^K |b_k|^2$$
   - Verification: Confirmed via `tests/test_convergence_aware.py`.

3. **FL Convergence Bound Connection**:
   - Derived from standard $L$-smooth optimization:
     $$\mathbb{E}[F(\mathbf{w}_{t+1})] \le F(\mathbf{w}_t) - \eta \|\nabla F(\mathbf{w}_t)\|^2 + \frac{L \eta^2}{2} \|\mathbf{g}_t\|^2 + \frac{L \eta^2}{2} \mathbb{E}[\|\mathbf{e}_t\|^2]$$
   - Where $\mathbb{E}[\|\mathbf{e}_t\|^2] \equiv J_t$. Minimizing $J_t$ directly minimizes the upper bound on per-round expected loss degradation.
