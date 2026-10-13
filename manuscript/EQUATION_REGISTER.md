# Equation Register: AROTA-FL

This register documents every mathematical expression, variable definition, physical dimension, derivation trail, implementation mapping, and validation check for the manuscript.

---

## 1. Mathematical Symbol Inventory

| Symbol | Definition | Dimension / Type | Units | Physical Interpretation / Role |
| :--- | :--- | :--- | :--- | :--- |
| $K$ | Number of participating clients | $\mathbb{Z}^+$ (Scalar) | Dimensionless | User population in the FL cell (typically 10 to 20). |
| $N$ | Number of RIS reflecting elements | $\mathbb{Z}^+$ (Scalar) | Dimensionless | Surface array size ($N \in \{16, 32, 64, 128\}$). |
| $\mathbf{w} \in \mathbb{R}^d$ | Global model parameter vector | Vector ($d \times 1$) | Dimensionless | Trainable neural network weights/biases. |
| $F(\mathbf{w})$ | Global FL loss function | $\mathbb{R} \to \mathbb{R}$ | Loss | Global objective: $F(\mathbf{w}) = \sum_{k=1}^K p_k F_k(\mathbf{w})$. |
| $p_k, \alpha_k$ | Aggregation weight for client $k$ | $\mathbb{R}^+$ (Scalar) | Dimensionless | Normalized weighting factor ($\sum_{k=1}^K \alpha_k = 1$; $\alpha_k = 1/K$). |
| $\mathbf{g}_k^{(t)}$ | Local gradient / model difference | Vector ($d \times 1$) | Dimensionless | Client $k$'s local update at round $t$. |
| $\mathbf{g}^{(t)}$ | Target global aggregated update | Vector ($d \times 1$) | Dimensionless | Ideal target aggregate $\sum_{k=1}^K \alpha_k \mathbf{g}_k^{(t)}$. |
| $\eta$ | Global learning rate | $\mathbb{R}^+$ (Scalar) | Dimensionless | Server gradient descent step size ($\eta = 0.01$). |
| $\mathbf{h}_{d,k}$ | Direct channel from client $k$ to AP | Complex scalar $\mathbb{C}$ | Dimensionless | Rayleigh / Rician fading with path loss. |
| $\mathbf{h}_k$ | Uplink channel from client $k$ to RIS | $\mathbb{C}^{N \times 1}$ | Dimensionless | Multi-antenna channel response from user to RIS. |
| $\mathbf{G}^H$ | Uplink channel from RIS to AP | $\mathbb{C}^{1 \times N}$ | Dimensionless | Multi-element link from RIS array to AP receiver. |
| $\mathbf{e}_k$ | CSI estimation error on $\mathbf{h}_k$ | $\mathbb{C}^{N \times 1}$ | Dimensionless | Complex Gaussian error: $\mathbf{e}_k \sim \mathcal{CN}(0, \sigma_e^2 \mathbf{I}_N)$. |
| $\sigma_e^2$ | CSI estimation error variance | $\mathbb{R}^+$ (Scalar) | Dimensionless | Quality of channel knowledge ($\sigma_e^2 \in [0, 0.30]$). |
| $\hat{\mathbf{h}}_k$ | Estimated channel vector | $\mathbb{C}^{N \times 1}$ | Dimensionless | Available CSI: $\hat{\mathbf{h}}_k = \mathbf{h}_k + \mathbf{e}_k$. |
| $\mathbf{\Theta}$ | Active RIS reflection matrix | $\mathbb{C}^{N \times N}$ | Dimensionless | Diagonal matrix $\mathbf{\Theta} = a \operatorname{diag}(e^{j\theta_1}, \dots, e^{j\theta_N})$. |
| $a$ | Active RIS amplification factor | $\mathbb{R}^+$ (Scalar) | Voltage gain | Amplification magnitude ($1.0 \le a \le a_{\max}$). |
| $\theta_n$ | Phase shift of element $n$ | $\mathbb{R}$ (Scalar) | Radians | Continuous phase adjustment $\theta_n \in [0, 2\pi)$. |
| $\mathbf{n}_R$ | Active RIS thermal noise vector | $\mathbb{C}^{N \times 1}$ | Volts | Complex Gaussian noise $\mathbf{n}_R \sim \mathcal{CN}(0, \sigma_R^2 \mathbf{I}_N)$. |
| $\sigma_R^2$ | Active RIS noise variance | $\mathbb{R}^+$ (Scalar) | Watts / dBm | Internal hardware noise ($\sigma_R^2 = -80$ dBm $= 10^{-11}$ W). |
| $n_0$ | AP receiver background noise | Complex scalar $\mathbb{C}$ | Volts | Receiver AWGN: $n_0 \sim \mathcal{CN}(0, \sigma_0^2)$. |
| $\sigma_0^2$ | AP receiver noise variance | $\mathbb{R}^+$ (Scalar) | Watts / dBm | Receiver thermal noise ($\sigma_0^2 = -90$ dBm $= 10^{-12}$ W). |
| $s_k$ | Transmitted analog AirComp symbol | Complex scalar $\mathbb{C}$ | Normalized | Normalized analog symbol ($\mathbb{E}[\|s_k\|^2] = 1$). |
| $b_k$ | Transmit scaling factor of client $k$ | Complex scalar $\mathbb{C}$ | Voltage scale | Pre-inversion coefficient at client transmitter. |
| $c$ | Receive normalization scalar at AP | $\mathbb{R}^+$ (Scalar) | Voltage scale | Post-aggregation scaling factor applied at receiver. |
| $P_k, P_{\max}$ | Maximum transmit power per client | $\mathbb{R}^+$ (Scalar) | Watts / dBm | Individual power limit ($P_{\max} = 10$ dBm $= 0.01$ W). |
| $P_{\text{RIS},\max}$ | Active RIS total power budget | $\mathbb{R}^+$ (Scalar) | Watts | Surface amplification power budget ($P_{\text{RIS},\max} = 2.0$ W). |
| $h_k^{eff}$ | Effective composite channel | Complex scalar $\mathbb{C}$ | Dimensionless | $h_k^{eff} = h_{d,k} + \mathbf{G}^H \mathbf{\Theta} \mathbf{h}_k$. |
| $J_t$ | Expected MSE objective function | $\mathbb{R}^+$ (Scalar) | Error power | Convergence-Aware objective $\mathbb{E}_{\mathbf{e}}[\text{MSE} \mid \hat{\mathbf{h}}]$. |

---

## 2. Equation Formulations and Validation

### Equation 1: Received AirComp Signal
$$y = \sum_{k=1}^K h_k^{eff} b_k s_k + \mathbf{G}^H \mathbf{\Theta} \mathbf{n}_R + n_0$$
- **Assumptions**: Flat block fading, perfect device time synchronization, mutually independent zero-mean symbol updates $\mathbb{E}[|s_k|^2]=1$, independent thermal noises.
- **Code Mapping**: `src/aircomp/received_signal.py:generate_received_signal`.
- **Validation**: Pass. Signal shape and noise statistics confirmed in `tests/test_aircomp.py`.

### Equation 2: Received Aggregation Estimator
$$\hat{s} = c y = \sum_{k=1}^K c h_k^{eff} b_k s_k + c \mathbf{G}^H \mathbf{\Theta} \mathbf{n}_R + c n_0$$
- **Assumptions**: Linear receive scaling at the single-antenna AP.
- **Code Mapping**: `src/aircomp/beamforming.py:apply_receive_scaling`.
- **Validation**: Pass. Tested in `tests/test_aircomp.py`.

### Equation 3: True Instantaneous Aggregation MSE
$$\text{MSE} = \mathbb{E}_{s, \mathbf{n}_R, n_0}[|\hat{s} - s|^2] = \sum_{k=1}^K |c h_k^{eff} b_k - \alpha_k|^2 + |c|^2 \sigma_R^2 \|\mathbf{G}^H \mathbf{\Theta}\|^2 + |c|^2 \sigma_0^2$$
- **Derivation**: Cross-terms between $s_k$, $\mathbf{n}_R$, and $n_0$ vanish due to zero-mean independence.
- **Code Mapping**: `src/aircomp/mse.py:compute_analytical_mse`.
- **Validation**: Pass. Validated against empirical Monte Carlo iterations in `tests/test_mse.py:test_analytical_vs_empirical_mse`.

### Equation 4: Zero-Forcing Precoding Conditions
$$c = \max_{k \in \{1,\dots,K\}} \frac{\alpha_k}{\sqrt{P_{\max}} |\hat{h}_k^{eff}|}, \qquad b_k = \frac{\alpha_k}{c \hat{h}_k^{eff}}$$
- **Derivation**: Enforces perfect signal phase alignment on estimated channels $c \hat{h}_k^{eff} b_k = \alpha_k$, with $|b_k|^2 \le P_{\max}$. The bottleneck user with minimal $|\hat{h}_k^{eff}|$ determines $c$.
- **Code Mapping**: `src/aircomp/beamforming.py:compute_zf_scaling`.
- **Validation**: Pass. Tested in `tests/test_baselines.py`.

### Equation 5: Convergence-Aware Expected MSE ($J_t$)
$$J_t = \mathbb{E}_{\mathbf{e}_k}[\text{MSE} \mid \hat{\mathbf{h}}] = \widehat{\text{MSE}} + |c|^2 \|\mathbf{G}^H \mathbf{\Theta}\|^2 \sigma_e^2 \sum_{k=1}^K |b_k|^2$$
- **Derivation**:
  $$\mathbb{E}_{\mathbf{e}_k}[|c (\hat{h}_k^{eff} - \mathbf{G}^H \mathbf{\Theta} \mathbf{e}_k) b_k - \alpha_k|^2] = |c \hat{h}_k^{eff} b_k - \alpha_k|^2 + |c|^2 |b_k|^2 \operatorname{Tr}(\mathbf{\Theta}^H \mathbf{G} \mathbf{G}^H \mathbf{\Theta} \mathbb{E}[\mathbf{e}_k \mathbf{e}_k^H])$$
  Since $\mathbb{E}[\mathbf{e}_k \mathbf{e}_k^H] = \sigma_e^2 \mathbf{I}_N$, the trace simplifies to $\sigma_e^2 \|\mathbf{G}^H \mathbf{\Theta}\|^2$. Summing over $k=1,\dots,K$ yields the exact closed-form expression.
- **Code Mapping**: `src/aircomp/mse.py:compute_expected_mse` and `src/optimization/convergence_aware.py:cost_fn`.
- **Validation**: Pass. Unit tested in `tests/test_convergence_aware.py`.

### Equation 6: FL Expected Convergence Bound
$$\mathbb{E}[F(\mathbf{w}_{t+1})] \le F(\mathbf{w}_t) - \eta \|\nabla F(\mathbf{w}_t)\|^2 + \frac{L \eta^2}{2} \|\mathbf{g}_t\|^2 + \frac{L \eta^2}{2} J_t$$
- **Derivation**: Standard descent lemma for $L$-smooth loss with noisy gradient $\hat{\mathbf{g}}_t = \mathbf{g}_t + \mathbf{e}_t^{aggr}$, where $\mathbb{E}[\|\mathbf{e}_t^{aggr}\|^2] = J_t$.
- **Code Mapping**: `src/optimization/convergence_aware.py` lines 58-64 (`fl_convergence_bound = (FL_smoothness_L / 2) * (FL_learning_rate ** 2) * expected_aggregation_mse`).
- **Validation**: Pass. Direct linear scaling implies minimizing $J_t$ directly optimizes the per-round learning guarantee.
