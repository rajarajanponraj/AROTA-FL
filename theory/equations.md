# Key Equations

## 1. Federated Learning Aggregation
$$ g^{(t)} = \sum_{k=1}^K \alpha_k g_k^{(t)}, \quad \sum_{k=1}^K \alpha_k = 1 $$

## 2. Global Model Update
$$ w_{t+1} = w_t - \eta \hat{g}_t, \quad \hat{g}_t = g_t + e_t $$

## 3. Wireless Channel (Rayleigh Fading)
$$ h_k \sim \mathcal{CN}(0, \beta_k I_N), \quad G \sim \mathcal{CN}(0, \beta_G I_N) $$

## 4. Imperfect CSI Model
$$ \hat{h}_k = h_k + e_k, \quad e_k \sim \mathcal{CN}(0, \sigma_e^2 I_N) $$

## 5. Active RIS Matrix
$$ \Theta = \text{diag}(a_1 e^{j\theta_1}, \dots, a_N e^{j\theta_N}) = a \text{diag}(e^{j\theta_1}, \dots, e^{j\theta_N}) \quad \text{s.t.} \quad 0 \le a \le a_{\max} $$

## 6. Active RIS Noise
$$ n_R \sim \mathcal{CN}(0, \sigma_R^2 I_N) $$

## 7. Effective Channel
$$ h_k^{eff} = G^H \Theta h_k $$

## 8. Received AirComp Signal
$$ y = \sum_{k=1}^K h_k^{eff} b_k s_k + G^H \Theta n_R + n_0 $$

## 9. AirComp Estimator
$$ \hat{s} = c y $$

## 10. Analytical AirComp MSE (True Channel)
$$ \text{MSE} = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|G^H \Theta\|^2 + |c|^2 \sigma_0^2 $$

## 11. Empirical Monte Carlo MSE
$$ \widehat{\text{MSE}}_{MC} = \frac{1}{S} \sum_{s=1}^S |\hat{s}_s - s_s|^2 $$

## 12. Power Constraints
$$ |b_k|^2 \le P_k, \quad \forall k \in \{1, \dots, K\} $$

## 13. MSE-Minimization Objective (Baseline)
$$ x_{MSE}^* = \arg\min_x \widehat{\text{MSE}}_t(x) $$
where $x = \{a, \Theta, b_1, \dots, b_K, c\}$, evaluated purely at $\hat{h}_k$.

## 14. Convergence-Aware Objective (Proposed)
$$ J_t(x) = \mathbb{E}_{e_k}[\text{MSE}_t(x) \mid \hat{h}_k] = \lambda_1 \widehat{\text{MSE}}_t(x) + \lambda_2 C_t(x) $$
where $C_t(x)$ represents the convergence penalty induced by CSI uncertainty bounding the FL aggregation error:
$$ C_t(x) = |c|^2 \|G^H \Theta\|^2 \sum_{k=1}^K |b_k|^2 $$
with weights $\lambda_1 = 1$, $\lambda_2 = \sigma_e^2$.
