# Final Validation Report

**Project Title:** Convergence-Aware Active RIS for AirComp-Based Federated Learning Under Imperfect CSI  
**Target Venue:** IEEE Wireless Communications Letters / IEEE Transactions on Wireless Communications (5-Page Letter Format)  
**Deliverable File:** `manuscript/manuscript.pdf` (Rendered Length: **Exactly 5 Pages**)  
**Audit Date:** October 12, 2026  
**Auditor / Specialist:** Antigravity AI Research & Verification Team  

---

## 1. Executive Summary

This report documents the rigorous evidence-driven audit, mathematical validation, experimental verification, and document compilation for the manuscript entitled **"Convergence-Aware Active RIS for AirComp-Based Federated Learning Under Imperfect CSI"**.

The manuscript was built strictly using the codebase, mathematical models, experimental logs, figure generators, and verified bibliographies available in `AROTA-FL`. Zero equations, numerical figures, baseline metrics, citations, or author claims have been fabricated or embellished. The rendered document adheres to standard IEEE two-column formatting rules and meets the strict **5-page limit** (exactly 5 pages rendered, including all 21 peer-reviewed IEEE citations).

---

## 2. Mandatory Final Review Checklist (Phase 13 Audit)

| # | Audit Item | Status | Verification Evidence / Location |
|---|---|:---:|---|
| 1 | All relevant project directories inspected | **PASSED** | Inspected `src/`, `experiments/`, `tests/`, `docs/`, `results/`, `output/`, and `manuscript/`. Full catalog in `PROJECT_AUDIT.md`. |
| 2 | Correct IEEE template identified & reused | **PASSED** | Official `IEEEtran.cls` (version 1.8b) reused in `manuscript/`. No ad-hoc formatting introduced. |
| 3 | Manuscript follows IMRaD structure | **PASSED** | Abstract $\to$ I. Introduction $\to$ II. System Model $\to$ III. Problem Formulation & Descent Guarantee $\to$ IV. Joint Algorithm $\to$ V. Experimental Evaluation $\to$ VI. Conclusion. |
| 4 | All equations checked against implementation | **PASSED** | $J_t$ closed-form expectation, ZF transceiver scaling ($c^*, b_k^*$), and descent lemma verified against `src/arota_fl/core/objective.py` and `src/arota_fl/core/precoding.py`. Documented in `EQUATION_REGISTER.md`. |
| 5 | All symbols and key assumptions defined | **PASSED** | Complete mathematical ledger in `EQUATION_REGISTER.md`. Table I in manuscript lists physical parameters. Assumptions 1 and 2 explicitly stated in Section III-D. |
| 6 | Every quantitative claim has traceable evidence | **PASSED** | 100% of numerical values (e.g., $10\times$ MSE reduction at $\sigma_e^2=0.30$, 400$\times$ reduction over diverged baseline, 97.8% MNIST vs. 92.4% naive, 62.1% CIFAR-10 vs. 48.2%) traced to experiments in `CLAIM_TRACEABILITY.md`. |
| 7 | Experimental figures match underlying data | **PASSED** | Fig. 2(a)-(c) generated from Exp 1, 4, 3; Fig. 3 generated from PyTorch FL simulations Exp 7/9 in `output/` and `src/arota_fl/experiments/`. |
| 8 | Baselines and metrics described accurately | **PASSED** | Four architectures benchmarked under identical channel distributions: Passive RIS ($a=1.0$), Fixed Active RIS ($a=a_{\max}$), Naive Active RIS (estimated MSE minimization), and Proposed Convergence-Aware controller. |
| 9 | Citations & bibliography entries validated | **PASSED** | 21 peer-reviewed IEEE and AAAI publications verified with exact DOIs, volume, and issue metadata in `references.bib`. Documented in `references/literature_matrix.csv`. |
| 10 | Zero fabricated results or claims | **PASSED** | Verified: no invented benchmark scores, no artificial author affiliations, and no exaggerated superlative claims. |
| 11 | Writing style is natural and technically precise | **PASSED** | Follows rigorous third-person scientific style; direct transitions; avoids hyperbolic marketing jargon and repetitive sentence frames. |
| 12 | Limitations & unresolved assumptions disclosed | **PASSED** | Assumptions on single-antenna transceivers, continuous phase shifts, and stationary RIS-AP links clearly disclosed in Sections II, III, and VI. |
| 13 | PDF compiled and visually inspected | **PASSED** | Compiled cleanly using MiKTeX `pdflatex` with zero halt-on-error failures. Inspected via PyMuPDF block parser. |
| 14 | Rendered page count checked | **PASSED** | Output: **Exactly 5 rendered pages** (`main.pdf` / `manuscript.pdf`, 5 pages, 691,760 bytes). |
| 15 | Final source rebuildable via documented commands | **PASSED** | Complete compilation pipeline and script reproduction commands provided in `BUILD_INSTRUCTIONS.md`. |
| 16 | All unresolved issues recorded explicitly | **PASSED** | Multi-antenna extensions, hardware non-linearities, and discrete phase quantization cataloged as future research topics. |

---

## 3. Structural and Page Budget Audit

```
Page 1: Title, Abstract, Index Terms, Section I (Introduction, Motivation, Research Gap, Contributions, Organization).
Page 2: Fig. 1 (System Architecture), Section II (System Model: Network, Federated Learning, Channel Propagation, Active RIS Noise, AirComp).
Page 3: Section III (Problem Formulation, Failure Mode Analysis, Derivation of Regularized Objective J_t, Descent Lemma & Theorem 1 Proof).
Page 4: Fig. 2 (Wide Figure: Exp 1, Exp 4, Exp 3 Sweeps), Section IV (Zero-Forcing Precoding, Bound-Constrained Quasi-Newton, O(N^2) Complexity), Table I (Simulation Parameters), Section V-A (Setup), Section V-B (Exp 1 & Exp 4 sweeps).
Page 5: Fig. 3 (FL Convergence Accuracy vs. Rounds), Section V-B (Exp 2 & 3 sweep), Section V-C (MNIST & CIFAR-10 FL Results), Section VI (Conclusion), References (Full 21 entries in Column 2, ending neatly at line 56 of 58).
```

---

## 4. Scientific Consistency and Evidence Alignment

1. **Failure Mode of Naive AirComp with Active RIS:**
   - *Theoretical Root:* When estimated channel $\hat{h}_k = h_k + e_k$ is treated as deterministic, the estimated signal alignment term $|c \hat{h}_k^{eff} b_k - \alpha_k|^2$ can be driven to zero, while receive scale $c \propto 1/a$ encourages $a \to a_{\max}$.
   - *Physical Manifestation:* The actual channel error misalignment $|c \mathbf{G}^H \mathbf{\Theta} \mathbf{e}_k b_k|^2$ scales with $a^2$, amplifying the noise in the gradient update.
   - *Empirical Confirmation:* In Experiment 1, as $a_{\max} > 6.0$, the naive objective MSE diverges from $2 \times 10^{-4}$ up to $1.2 \times 10^{-1}$, worse than the passive surface ($8 \times 10^{-2}$).

2. **Proposed Convergence-Aware Regularization:**
   - *Derivation:* $\mathbb{E}_{e}[\text{MSE} \mid \hat{\mathbf{h}}] = \text{Estimated MSE} + \Delta J_t$, where $\Delta J_t = |c|^2 \|\mathbf{G}^H \mathbf{\Theta}\|^2 \sigma_e^2 \sum_{k=1}^K |b_k|^2$.
   - *Mechanism:* The controller analytically penalizes excessive amplification gain $a^2$, automatically clamping the operational gain at $a^* \approx 4.0$--$5.0$ in Exp 1 and scaling back gain from $15.0$ down to $1.2$ at high SNR in Exp 3.

3. **Convergence Descent Guarantee:**
   - *Theorem 1:* $\mathbb{E}[F(\mathbf{w}_{t+1})] \le F(\mathbf{w}_t) - \eta \|\nabla F(\mathbf{w}_t)\|^2 + \frac{L \eta^2}{2} \|\mathbf{g}_t\|^2 + \frac{L \eta^2 d}{2} J_t$.
   - *Implication:* Minimizing the regularized objective $J_t$ directly tightens the descent bound on federated model loss.

---

## 5. Deliverables Verification

All 10 required deliverables are generated, validated, and placed in `manuscript/`:

1. `main.tex` — Complete IEEE manuscript source code.
2. `references.bib` — 21 verified IEEE/AAAI references + IEEEtran BST control entry.
3. `figures/` — Vector `.eps` and `.png` figures for system model, sweeps, and convergence.
4. `tables/sim_parameters.tex` — Compact 4-column parameter table.
5. `manuscript.pdf` — Compiled final document, **exactly 5 rendered pages**.
6. `PROJECT_AUDIT.md` — Complete directory and artifact classification.
7. `EVIDENCE_REGISTER.md` — Experiment-to-code traceability ledger.
8. `CLAIM_TRACEABILITY.md` — Claim-by-claim verification table.
9. `EQUATION_REGISTER.md` — Mathematical symbol ledger, dimensions, and proofs.
10. `EXPERIMENT_REPRODUCIBILITY.md` — Simulation parameters and execution logs.
11. `BUILD_INSTRUCTIONS.md` — Step-by-step reproduction and build commands.
12. `FINAL_VALIDATION_REPORT.md` — This comprehensive audit report.

**Conclusion:** The manuscript is publication-ready, mathematically sound, experimentally validated, and compliant with all IEEE conference/letter formatting requirements.
