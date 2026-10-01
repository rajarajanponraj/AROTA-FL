# Mathematical Model

## 1. System Overview
The system integrates Active-RIS-assisted Over-the-Air Computation (AirComp) for Wireless Federated Learning (AirFL). A set of $K$ clients transmit their local gradients to an edge server, aided by an $N$-element Active RIS that can both reflect and amplify the incident signals.

## 2. Federated Learning (FL) Formulation
At communication round $t$, each client $k$ computes a local gradient $g_k^{(t)}$ based on its local dataset.
The server aims to receive the ideally aggregated gradient:
$$ g^{(t)} = \sum_{k=1}^K \alpha_k g_k^{(t)} $$
where typically $\alpha_k = 1/K$.
Due to wireless impairments, fading, and noise, the server receives an imperfect estimate $\hat{g}_t = g_t + e_t$. 
The global model is then updated using:
$$ w_{t+1} = w_t - \eta \hat{g}_t $$

## 3. Communication Model
### Channels and Imperfect CSI
- **True channel (Client $k$ to RIS):** $h_k \in \mathbb{C}^{N \times 1}$
- **Imperfect CSI:** The estimated channel is $\hat{h}_k = h_k + e_k$, where $e_k \sim \mathcal{CN}(0, \sigma_e^2 I_N)$.
- **True channel (RIS to Server):** $G \in \mathbb{C}^{N \times 1}$

### Active RIS Operations
The Active RIS operates with an amplification and phase-shift matrix:
$$ \Theta = a \cdot \text{diag}(e^{j\theta_1}, \dots, e^{j\theta_N}) $$
subject to a maximum amplification gain $a_{\max}$.
Active electronics introduce thermal noise $n_R \sim \mathcal{CN}(0, \sigma_R^2 I_N)$ which gets reflected and amplified toward the server.

### Effective Channel
The true effective channel from client $k$ to the server through the RIS is:
$$ h_k^{eff} = G^H \Theta h_k $$
Conversely, the effective channel perceived by the server based on estimation is:
$$ \hat{h}_k^{eff} = G^H \Theta \hat{h}_k $$

## 4. AirComp Received Signal
Clients analogically transmit symbols $s_k$ scaled by a transmit factor $b_k$. The received signal at the server antenna is the superposition:
$$ y = \sum_{k=1}^K h_k^{eff} b_k s_k + G^H \Theta n_R + n_0 $$
where $n_0 \sim \mathcal{CN}(0, \sigma_0^2)$ is the thermal receiver noise at the server.

The server scales the received signal by a scalar factor $c$ to obtain the final AirComp estimate:
$$ \hat{s} = c y $$

## 5. Mean Squared Error (MSE)
The true instantaneous Mean Squared Error (MSE) of the AirComp aggregation for a given channel realization (assuming independent, unit-variance data symbols $s_k$) is given by:
$$ \text{MSE} = \mathbb{E}_{s, n_R, n_0}[|\hat{s} - s|^2] = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2 $$

## 6. Optimization Problems
### MSE-Minimizing Baseline (Naïve)
The standard standard methodology formulates the problem by minimizing the MSE evaluated at the estimated CSI, essentially treating the estimates as perfect ground truth:
$$ \min_{a, \{\theta_n\}, \{b_k\}, c} \widehat{\text{MSE}} $$
where $\widehat{\text{MSE}} = \sum_{k=1}^K |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2$
subject to $|b_k|^2 \le P_k$ and $0 \le a \le a_{\max}$.

### Convergence-Aware Proposed Method
Under imperfect CSI ($\sigma_e^2 > 0$), treating estimates as perfect yields mismatched $\{b_k\}$ and $c$. When the active RIS amplification $a$ is excessively high, it drastically amplifies the hidden CSI errors, resulting in massive instantaneous aggregation errors $e_t$ that degrade FL convergence.

A robust convergence-aware objective considers the statistical expectation of the true MSE over the CSI uncertainty distribution:
$$ J_t = \mathbb{E}_{e_k}[\text{MSE} \mid \hat{h}_k] $$

Let $h_k = \hat{h}_k - e_k$. Substituting this into the true MSE yields an expanded objective containing a penalty term strictly proportional to the CSI variance $\sigma_e^2$. This term naturally limits excessive active-RIS amplification and aggressive power allocations when the channel estimates are highly uncertain, resulting in stabler FL convergence.
