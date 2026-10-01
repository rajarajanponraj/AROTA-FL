# Mathematical Derivations

## 1. Analytical AirComp MSE
The server receives the superimposed signal:
$$ y = \sum_{k=1}^K h_k^{eff} b_k s_k + G^H \Theta n_R + n_0 $$
Applying the receive scaler $c$, the estimate is:
$$ \hat{s} = c y = \sum_{k=1}^K c h_k^{eff} b_k s_k + c G^H \Theta n_R + c n_0 $$
The desired aggregated signal is $s = \sum_{k=1}^K \alpha_k s_k$.
The instantaneous estimation error is therefore:
$$ \hat{s} - s = \sum_{k=1}^K (c h_k^{eff} b_k - \alpha_k) s_k + c G^H \Theta n_R + c n_0 $$
Assuming the transmitted symbols $s_k$, active RIS thermal noise $n_R$, and receiver noise $n_0$ are mutually independent, zero-mean, with $\mathbb{E}[|s_k|^2] = 1$, $\mathbb{E}[n_R n_R^H] = \sigma_R^2 I_N$, and $\mathbb{E}[|n_0|^2] = \sigma_0^2$, we can compute the expectation of the Mean Squared Error (MSE):
$$ \text{MSE} = \mathbb{E}_{s, n_R, n_0}[|\hat{s} - s|^2] $$
$$ \text{MSE} = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + \mathbb{E}[|c G^H \Theta n_R|^2] + \mathbb{E}[|c n_0|^2] $$
$$ \text{MSE} = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2 $$

## 2. FL Aggregation Error and Convergence
Let $L(w)$ be the global FL loss function. Assume $L$ is $L$-smooth. The FL update is $w_{t+1} = w_t - \eta \hat{g}_t$, where $\hat{g}_t = g_t + e_t$, and $e_t$ is the aggregation error originating from AirComp.
From the standard $L$-smoothness inequality:
$$ L(w_{t+1}) \le L(w_t) + \langle \nabla L(w_t), w_{t+1} - w_t \rangle + \frac{L}{2} \|w_{t+1} - w_t\|^2 $$
$$ L(w_{t+1}) \le L(w_t) - \eta \langle \nabla L(w_t), g_t + e_t \rangle + \frac{L \eta^2}{2} \|g_t + e_t\|^2 $$
Taking expectations over the communication noise and assuming $\mathbb{E}[e_t] = 0$ (unbiased estimator) and $e_t$ is independent of $g_t$:
$$ \mathbb{E}[L(w_{t+1})] \le \mathbb{E}[L(w_t)] - \eta \|\nabla L(w_t)\|^2 + \frac{L \eta^2}{2} \|g_t\|^2 + \frac{L \eta^2}{2} \mathbb{E}[\|e_t\|^2] $$
The term $\mathbb{E}[\|e_t\|^2]$ corresponds identically to the AirComp MSE. Therefore, minimizing the aggregation MSE strictly bounds the deviation of the loss function, proving analytically that controlling the MSE improves FL convergence.

## 3. Convergence-Aware Objective under Imperfect CSI
Under practical imperfect CSI, the actual channels are $h_k = \hat{h}_k - e_k$. The true effective channel becomes: 
$$ h_k^{eff} = G^H \Theta (\hat{h}_k - e_k) = \hat{h}_k^{eff} - G^H \Theta e_k $$
When optimizing $\{b_k\}, c, \Theta$, a reliable convergence-aware objective should compute the expectation over the CSI error realization $e_k$.
$$ J_t(x) = \mathbb{E}_{e_k}[\text{MSE}(x) \mid \hat{h}_k] $$
Expanding the expectation of the signal misalignment term:
$$ \mathbb{E}_{e_k} \left[ |c ( \hat{h}_k^{eff} - G^H \Theta e_k ) b_k - \alpha_k|^2 \right] $$
Since $e_k \sim \mathcal{CN}(0, \sigma_e^2 I_N)$ and $\mathbb{E}[e_k] = 0$, the cross terms strictly vanish:
$$ = |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 |b_k|^2 \mathbb{E}[e_k^H \Theta^H G G^H \Theta e_k] $$
The quadratic form simplifies as follows:
$$ \mathbb{E}[e_k^H \Theta^H G G^H \Theta e_k] = \text{Tr}(\Theta^H G G^H \Theta \mathbb{E}[e_k e_k^H]) = \sigma_e^2 \text{Tr}(G G^H \Theta \Theta^H) = \sigma_e^2 \|G^H \Theta\|^2 $$
Substituting this back yields:
$$ = |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 |b_k|^2 \sigma_e^2 \|G^H \Theta\|^2 $$

Thus, the final convergence-aware objective function evaluates to:
$$ J_t(x) = \sum_{k=1}^K |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 \|G^H \Theta\|^2 \left( \sigma_R^2 + \sigma_e^2 \sum_{k=1}^K |b_k|^2 \right) + |c|^2 \sigma_0^2 $$

### Summary of Differences
This derivation exposes the core trade-off evaluated in this project:
- The standard **MSE-minimizing** approach ignores $\sigma_e^2$ and optimizes:
  $$ \widehat{\text{MSE}} = \sum_{k=1}^K |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2 $$
- The true expected error **$J_t(x)$** introduces an extra penalty:
  $$ \Delta J_t = |c|^2 \|G^H \Theta\|^2 \sigma_e^2 \sum_{k=1}^K |b_k|^2 $$

High active-RIS amplification ($\|\Theta\|^2$) coupled with large client transmit powers ($\sum |b_k|^2$) massively magnifies the CSI uncertainty. 
A **Convergence-Aware** controller optimizes $J_t(x)$ directly, automatically backing off from extreme active-RIS amplification when the CSI error ($\sigma_e^2$) is severe, thereby preventing catastrophic aggregation errors during the FL process.
