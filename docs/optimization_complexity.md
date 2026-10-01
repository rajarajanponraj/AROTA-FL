# Optimization Algorithm and Complexity Analysis

## 1. Algorithm Formulation
The objective of the proposed Convergence-Aware Controller is to minimize the expected MSE bound $J_t(x)$ over the Active RIS amplification factor $a$ and phase shifts $\Theta = \text{diag}(a e^{j\theta_1}, \dots, a e^{j\theta_N})$.

The problem is highly non-convex due to the coupling between the variables ($a, \Theta, b_k, c$). To solve this efficiently while avoiding local minima traps, we employ a multi-start **Quasi-Newton Method (L-BFGS-B)**.

### Sub-problems:
For any given configuration of the Active RIS $\Theta$, the optimal transmit scalers $b_k$ and receive scaler $c$ are computed in closed-form using Zero-Forcing (ZF) conditions:
1. $c = \max_k \frac{\alpha_k}{\sqrt{P_k} |\hat{h}_k^{eff}|}$
2. $b_k = \frac{\alpha_k}{c \hat{h}_k^{eff}}$

By substituting these optimal sub-problem solutions back into the objective function, the problem dimensionality is drastically reduced. We only optimize over:
- Amplification factor: $a \in [1, a_{\max}]$
- Phase shifts: $\theta_n \in [0, 2\pi)$ for $n=1,\dots,N$

## 2. Complexity Analysis (Big-O)

### Objective Function Evaluation:
In each iteration of the L-BFGS-B algorithm, we evaluate the cost function:
1. Matrix multiplication to compute effective channel $G^H \Theta H_{RIS}$: $O(K \times N)$ complex multiplications, where $K$ is the number of clients and $N$ is the number of RIS elements.
2. Computing $c$ and $b_k$: $O(K)$ operations.
3. Total Objective Evaluation: $O(K \times N)$.

### Optimization Routine:
The L-BFGS-B algorithm has a time complexity per iteration of $O(D^2)$, where $D$ is the number of optimization variables. Here, $D = N + 1$.
Therefore, the per-iteration complexity of the optimizer is $O(N^2)$.
Assuming the algorithm takes $I_{iter}$ iterations to converge and we perform $M$ random restarts to avoid local minima, the total computational complexity is:

$$ \mathcal{O}\left( M \times I_{iter} \times (K \cdot N + N^2) \right) $$

For a standard setup where $N$ (e.g., 64) is generally larger than $K$ (e.g., 10), the complexity scales quadratically with the number of RIS elements $O(N^2)$, which is highly efficient and feasible for real-time deployment at the edge server (AP). 

This is significantly less complex than full Semidefinite Relaxation (SDR) methods, which generally scale with $O(N^{4.5})$. By utilizing the closed-form derivations for the transmit/receive scalers, our approach reduces the search space and ensures practical convergence times.
