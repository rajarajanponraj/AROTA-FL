# System and Model Assumptions

## 1. Network Topology
- The system consists of $K$ single-antenna Federated Learning (FL) clients.
- A single-antenna edge server coordinates the FL process.
- An Active Reconfigurable Intelligent Surface (RIS) with $N$ reflecting/amplifying elements assists the communication.
- Direct links between the clients and the server are assumed negligible due to severe blockage (unless explicitly evaluated in an ablation study).

## 2. Federated Learning Model
- **Task:** Clients collaboratively train a global model parameter vector $w$.
- **Aggregation:** The desired global model update at round $t$ is a weighted sum of local gradients: $g^{(t)} = \sum_{k=1}^K \alpha_k g_k^{(t)}$.
- **Weights:** Initially assumed uniform across all clients, $\alpha_k = 1/K$, subject to $\sum_{k=1}^K \alpha_k = 1$.
- **Update Rule:** The server updates the model via standard Gradient Descent: $w_{t+1} = w_t - \eta \hat{g}_t$, where $\eta$ is the learning rate and $\hat{g}_t = g_t + e_t$ is the estimated aggregation corrupted by an error $e_t$.

## 3. Wireless Channel Model
- **Fading Distribution:** Rayleigh fading is used. The channel from client $k$ to the RIS is modeled as $h_k \sim \mathcal{CN}(0, \beta_k I_N)$. The channel from the RIS to the server is $G \sim \mathcal{CN}(0, \beta_G I_N)$.
- **Time Dynamics:** Block fading is assumed; channels remain constant over one entire FL communication round but change independently between successive rounds.
- **Normalization:** Initial channels are normalized unless specific path-loss exponents are explicitly integrated in later simulation stages.

## 4. Channel State Information (CSI)
- **Imperfect Client-RIS CSI:** The system operates under imperfect CSI for the client-to-RIS links. The estimated channel is $\hat{h}_k = h_k + e_k$, where the error follows $e_k \sim \mathcal{CN}(0, \sigma_e^2 I_N)$.
- **Server CSI:** The server possesses the estimated CSI $\hat{h}_k$ and the perfect RIS-to-server CSI $G$ (this can be extended to imperfect $G$ if necessitated by the selected baseline models).

## 5. Active RIS Model
- **Amplification Matrix:** The RIS can actively amplify the incident signal. The reflection/amplification matrix is $\Theta = \text{diag}(a_1 e^{j\theta_1}, \dots, a_N e^{j\theta_N})$.
- **Uniform Gain Constraint:** Initially, a common amplification factor $a_1 = \dots = a_N = a$ is enforced, such that $0 \le a \le a_{\max}$.
- **Active RIS Thermal Noise:** Amplification inherently introduces dynamic noise $n_R \sim \mathcal{CN}(0, \sigma_R^2 I_N)$ at the RIS elements. This noise is amplified and forwarded to the server.

## 6. Over-the-Air Computation (AirComp)
- **Modulation:** Analog amplitude modulation is assumed for AirComp.
- **Transmitter Constraint:** Client $k$ employs a transmit scaling factor $b_k$, constrained by an average/peak power limit $|b_k|^2 \le P_k$.
- **Receiver Processing:** The server utilizes a scalar receive normalization factor $c$.
- **Signal Power:** The transmitted data symbols $s_k$ (representing the gradient updates) are assumed to be mutually independent and have normalized power ($\mathbb{E}[|s_k|^2] = 1$) for the purpose of the MSE formulation.

## 7. Optimization Objectives
- **Baseline (MSE-Minimization):** The standard approach designs the configuration to minimize the instantaneous AirComp MSE based exclusively on the estimated channels, implicitly assuming the estimates are perfect.
- **Proposed (Convergence-Aware):** The proposed method explicitly considers the expectation over the CSI error distributions, formulating an objective that relates to the degradation of the FL convergence bound rather than just the estimated instantaneous MSE.
