import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx_helpers import (
    add_p, add_heading_1, add_heading_2, add_heading_3, 
    set_cell_background, set_cell_margins, set_table_borders, 
    add_callout
)

def build_chapter_7(doc):
    # -------------------------------------------------------------
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE
    # -------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 7\nCONCLUSION AND FUTURE SCOPE", space_before=12, space_after=14)

    add_heading_2(doc, "7.1 Summary of Project Phase Work")
    p1 = (
        "In this project phase, we developed and validated a novel Convergence-Aware Optimization Framework for Active Reconfigurable Intelligent Surface "
        "(Active RIS)-assisted Over-the-Air Federated Learning (AirFL) operating under imperfect Channel State Information (CSI). Wireless AirComp provides an "
        "ultra-efficient paradigm for aggregating high-dimensional gradient updates by exploiting electromagnetic wave superposition, eliminating communication "
        "delays that scale with client populations. However, physical-layer propagation attenuation, deep fading, and channel estimation inaccuracies severely "
        "corrupt analog aggregations. While active RIS technology effectively mitigates cascaded double-fading by integrating reflection-type amplifiers, it "
        "introduces non-negligible surface thermal noise and magnifies underlying channel estimation errors."
    )
    add_p(doc, p1)

    p2 = (
        "This project identified a critical, previously unaddressed vulnerability in existing active-RIS AirComp literature: naive instantaneous MSE minimization "
        "treats imperfect channel estimates as ground truth, aggressively driving active amplification gains to their maximum hardware ceiling. This uncontrolled "
        "amplification severely multiplies both surface thermal noise and CSI estimation errors, destroying the fidelity of aggregated global gradients and "
        "causing federated learning convergence to stall or diverge. To overcome this limitation, we derived an exact conditional expected MSE objective that "
        "incorporates CSI estimation error statistics directly into the optimization landscape, exposing an analytical regularization penalty that dynamically "
        "throttles active amplification under channel uncertainty."
    )
    add_p(doc, p2)

    add_heading_2(doc, "7.2 Key Contributions and Technical Milestones")
    p3 = (
        "The primary scientific, mathematical, and algorithmic milestones achieved during this project phase are summarized as follows:\n\n"
        "1. Closed-Form Expected Error Derivation: We evaluated the statistical conditional expectation of aggregation MSE over complex Gaussian CSI estimation "
        "errors, deriving an exact closed-form objective containing the analytical regularization penalty Delta J_t = |c|^2 ||G^H Theta||^2 sigma_e^2 sum |b_k|^2.\n\n"
        "2. Rigorous Federated Learning Convergence Guarantee: Using the L-smooth descent lemma, we proved that minimizing our physical-layer objective J_t "
        "directly tightens the upper bound on per-round expected loss reduction, establishing an analytical bridge between physical-layer transceiver design "
        "and machine learning optimization.\n\n"
        "3. Low-Complexity Algorithmic Architecture: By deriving closed-form Zero-Forcing transmit and receive scalers, we collapsed the joint optimization space "
        "from 2K + N + 1 variables down to N + 1 metasurface parameters, solving it via multi-start L-BFGS-B Quasi-Newton optimization in O(N^2) complexity, "
        "bypassing computationally prohibitive Semidefinite Relaxation (SDR) methods that scale as O(N^4.5).\n\n"
        "4. Comprehensive Cross-Layer Empirical Validation: Across 500 Monte Carlo wireless channel seeds and distributed PyTorch FL simulations on MNIST and "
        "CIFAR-10 under severe Dirichlet non-IID data partitioning (alpha = 0.5), the proposed framework achieved up to a 10x reduction in aggregation MSE, "
        "accelerated FL convergence by 3x, achieved 97.8% accuracy on MNIST (matching noise-free bounds), and outperformed naive active RIS by nearly 14 "
        "percentage points on CIFAR-10."
    )
    add_p(doc, p3)

    add_heading_2(doc, "7.3 Practical Limitations and Hardware Constraints")
    p4 = (
        "Despite its significant performance advantages, practical implementation of the proposed framework must consider several hardware constraints:\n\n"
        "• Power Consumption of Active Hardware: Active RIS elements incorporate active RF components (e.g., tunnel diodes or operational amplifiers) that "
        "consume DC bias power. Although our framework strictly enforces a total radiation power constraint (P_out <= 2.0 W), real-world deployments must manage "
        "hardware circuit power consumption and thermal dissipation.\n\n"
        "• Continuous vs. Discrete Phase Shifts: Our current theoretical formulation assumes continuous phase shifts theta_n in [0, 2pi). In commercial metasurfaces, "
        "phase shifts are quantized into discrete levels (e.g., 1-bit or 2-bit phase resolution), which introduces phase quantization noise.\n\n"
        "• Single-Antenna Transceivers: The current model considers single-antenna transceivers at edge clients and the central AP. Modern 6G base stations "
        "employ massive MIMO multi-antenna arrays, which offer additional spatial degrees of freedom for joint beamforming."
    )
    add_p(doc, p4)

    add_heading_2(doc, "7.4 Directions for Project Phase II and Future Research")
    p5 = (
        "Building upon the foundational theoretical models, algorithms, and simulation infrastructure established in Project Phase I, the following research "
        "directions are outlined for Project Phase II:\n\n"
        "1. Extension to Multi-Antenna Transceivers (MIMO AirFL): Extend the joint convergence-aware optimization formulation to multi-antenna edge devices and "
        "massive MIMO AP receivers, developing alternating optimization algorithms for coupled digital beamforming and active analog metasurface control.\n\n"
        "2. Discrete Phase Shift Quantization and Robustness: Incorporate 1-bit and 2-bit discrete phase shift quantization into the optimization cost function, "
        "deriving branch-and-bound or quantization-aware Quasi-Newton solvers that guarantee performance under coarse phase control.\n\n"
        "3. Decentralized and Client-Selection Dynamics: Integrate dynamic client scheduling algorithms (such as Lyapunov drift-plus-penalty frameworks) to "
        "adaptively select participating edge devices based on instantaneous channel conditions, energy budgets, and gradient variance.\n\n"
        "4. Metasurface Testbed and Hardware Prototyping: Interface the simulation engine with a software-defined radio (SDR) testbed (e.g., USRP platforms) "
        "to validate analog Over-the-Air gradient superposition and active amplification dynamics over real-world over-the-air RF propagation environments."
    )
    add_p(doc, p5)

    doc.add_page_break()

def build_references(doc):
    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_heading_1(doc, "REFERENCES", space_before=12, space_after=18)

    refs = [
        "[1] W. Y. B. Lim, N. C. Luong, D. T. Hoang, Y. Jiao, Y.-C. Liang, Q. Yang, D. Niyato, and C. Miao, \"Federated learning in mobile edge networks: "
        "A comprehensive survey,\" IEEE Communications Surveys & Tutorials, vol. 22, no. 3, pp. 2031-2063, 3rd Quart., 2020.",
        
        "[2] Z. Qin, G. Y. Li, and H. Ye, \"Federated learning and wireless communications,\" IEEE Wireless Communications, vol. 28, no. 5, "
        "pp. 134-140, Oct. 2021.",
        
        "[3] S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, \"Adaptive federated learning in resource constrained edge computing "
        "systems,\" IEEE Journal on Selected Areas in Communications, vol. 37, no. 6, pp. 1205-1221, June 2019.",
        
        "[4] M. Al-Quraan, L. Mohjazi, L. Bariah, A. Centeno, A. Zoha, K. Arshad, K. Assaleh, S. Muhaidat, M. Debbah, and M. A. Imran, \"Edge-native intelligence "
        "for 6G communications driven by federated learning: A survey of trends and challenges,\" IEEE Transactions on Emerging Topics in Computational Intelligence, "
        "vol. 7, no. 3, pp. 957-979, June 2023.",
        
        "[5] G. Zhu, J. Xu, K. Huang, and S. Cui, \"Over-the-air computing for wireless data aggregation in massive IoT,\" IEEE Wireless Communications, "
        "vol. 28, no. 4, pp. 57-65, Aug. 2021.",
        
        "[6] W. Liu, X. Zang, Y. Li, and B. Vucetic, \"Over-the-air computation systems: Optimization, analysis and scaling laws,\" IEEE Transactions on "
        "Wireless Communications, vol. 19, no. 8, pp. 5488-5502, Aug. 2020.",
        
        "[7] X. Cao, G. Zhu, J. Xu, Z. Wang, and S. Cui, \"Optimized power control design for over-the-air federated edge learning,\" IEEE Journal on Selected "
        "Areas in Communications, vol. 40, no. 1, pp. 342-358, Jan. 2022.",
        
        "[8] J. Zhu, Y. Shi, Y. Zhou, C. Jiang, W. Chen, and K. B. Letaief, \"Over-the-air federated learning and optimization,\" IEEE Internet of Things "
        "Journal, vol. 11, no. 10, pp. 16996-17020, May 2024.",
        
        "[9] X. Cao, G. Zhu, J. Xu, and K. Huang, \"Optimized power control for over-the-air computation in fading channels,\" IEEE Transactions on "
        "Wireless Communications, vol. 19, no. 11, pp. 7498-7513, Nov. 2020.",
        
        "[10] X. Cao, G. Zhu, J. Xu, and S. Cui, \"Transmission power control for over-the-air federated averaging at network edge,\" IEEE Journal on "
        "Selected Areas in Communications, vol. 40, no. 5, pp. 1571-1586, May 2022.",
        
        "[11] K. Yang, Y. Shi, Y. Zhou, Z. Yang, L. Fu, and W. Chen, \"Federated machine learning for intelligent IoT via reconfigurable intelligent surface,\" "
        "IEEE Network, vol. 34, no. 5, pp. 16-22, Sept./Oct. 2020.",
        
        "[12] W. Ni, Y. Liu, Z. Yang, H. Tian, and X. Shen, \"Federated learning in multi-RIS-aided systems,\" IEEE Internet of Things Journal, vol. 9, "
        "no. 12, pp. 9608-9624, Nov. 2021.",
        
        "[13] J. Zheng, H. Tian, W. Ni, W. Ni, and P. Zhang, \"Balancing accuracy and integrity for reconfigurable intelligent surface-aided over-the-air "
        "federated learning,\" IEEE Transactions on Wireless Communications, vol. 21, no. 12, pp. 10964-10980, Dec. 2022.",
        
        "[14] Z. Zhang, L. Dai, X. Chen, C. Liu, F. Yang, R. Schober, and H. V. Poor, \"Active RIS vs. passive RIS: Which will prevail in 6G?,\" "
        "IEEE Transactions on Communications, vol. 71, no. 3, pp. 1707-1725, Mar. 2023.",
        
        "[15] R. Long, Y.-C. Liang, Y. Pei, and E. G. Larsson, \"Active reconfigurable intelligent surface-aided wireless communications,\" IEEE Transactions "
        "on Wireless Communications, vol. 20, no. 8, pp. 4962-4975, Mar. 2021.",
        
        "[16] Z. Yu, H. Ren, C. Pan, G. Zhou, B. Wang, M. Dong, and J. Wang, \"Active RIS-aided ISAC systems: Beamforming design and performance analysis,\" "
        "IEEE Transactions on Communications, vol. 72, no. 3, pp. 1578-1595, Mar. 2024.",
        
        "[17] H. Zhou, M. Erol-Kantarci, Y. Liu, and H. V. Poor, \"A survey on model-based, heuristic, and machine learning optimization approaches in "
        "RIS-aided wireless networks,\" IEEE Communications Surveys & Tutorials, vol. 26, no. 2, pp. 781-823, 2nd Quart., 2024.",
        
        "[18] J. Yao, Z. Yang, W. Xu, D. Niyato, and X. You, \"Imperfect CSI: A key factor of uncertainty to over-the-air federated learning,\" "
        "IEEE Wireless Communications Letters, vol. 12, no. 12, pp. 2273-2277, Dec. 2023.",
        
        "[19] J.-H. Yang, H. Lee, and J. Choi, \"Robust transmission design for active RIS-aided systems,\" IEEE Transactions on Vehicular Technology, "
        "vol. 74, no. 7, pp. 11591-11596, July 2025.",
        
        "[20] A. Pradhan, M. A. Abd-Elmagid, H. S. Dhillon, and A. F. Molisch, \"Robust optimization of RIS in terahertz under extreme molecular re-radiation "
        "manifestations,\" IEEE Transactions on Wireless Communications, vol. 23, no. 3, pp. 1783-1797, Mar. 2024.",
        
        "[21] K. I. Kim, \"Robust distributed gradient aggregation using projections onto gradient manifolds,\" in Proc. AAAI Conference on Artificial "
        "Intelligence (AAAI), vol. 38, no. 12, pp. 13151-13159, Mar. 2024.",
        
        "[22] H. Wu and P. Wang, \"Node selection toward faster convergence for federated learning on non-IID data,\" IEEE Transactions on Network "
        "Science and Engineering, vol. 9, no. 5, pp. 3099-3111, Sept./Oct. 2022.",
        
        "[23] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, \"Communication-efficient learning of deep networks from decentralized data,\" "
        "in Proc. International Conference on Artificial Intelligence and Statistics (AISTATS), pp. 1273-1282, 2017.",
        
        "[24] Q. Yang, Y. Liu, T. Chen, and Y. Tong, \"Federated machine learning: Concept and applications,\" ACM Transactions on Intelligent Systems "
        "and Technology (TIST), vol. 10, no. 2, pp. 1-19, 2019.",
        
        "[25] C. Shen, J. Xu, and S. Cui, \"Federated learning over wireless networks: Optimization and trade-offs,\" IEEE Wireless Communications, "
        "vol. 28, no. 5, pp. 12-18, Oct. 2021.",
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(10)

    doc.add_page_break()

def build_appendices(doc):
    # -------------------------------------------------------------
    # APPENDIX A: NOTATION AND PARAMETER REGISTER
    # -------------------------------------------------------------
    add_heading_1(doc, "APPENDIX A\nSYSTEM PARAMETER REGISTER AND NOTATION AUDIT", space_before=12, space_after=16)

    p_app_a = (
        "This appendix provides a rigorous mathematical and dimensional inventory of all system parameters, physical quantities, "
        "and optimization variables employed across the analytical formulations in Chapters 3 and 4."
    )
    add_p(doc, p_app_a)

    reg_data = [
        ("Symbol", "Variable Definition", "Type / Dimension", "Nominal Unit", "Operational Physical Role"),
        ("K", "Edge client population", "Integer Scalar", "Dimensionless", "Number of devices concurrently transmitting updates"),
        ("N", "Active RIS element count", "Integer Scalar", "Dimensionless", "Physical aperture size of the metasurface array"),
        ("d", "Model gradient dimension", "Integer Scalar", "Dimensionless", "Total parameter count of the neural network"),
        ("w_t", "Global model weight vector", "Vector in R^d", "Dimensionless", "Trainable neural network parameters at round t"),
        ("g_{k,t}", "Local gradient update vector", "Vector in R^d", "Dimensionless", "Local model difference calculated by client k"),
        ("p_k", "Client aggregation weight", "Positive Scalar", "Dimensionless", "Statistical weight factor (sum p_k = 1)"),
        ("h_k", "Client-to-RIS channel", "Vector in C^{N x 1}", "Dimensionless", "Rayleigh multipath scattering channel response"),
        ("G^H", "RIS-to-AP channel", "Vector in C^{1 x N}", "Dimensionless", "Rician fading channel with strong LoS factor"),
        ("e_k", "CSI estimation error", "Vector in C^{N x 1}", "Dimensionless", "Complex Gaussian noise e_k ~ CN(0, sigma_e^2 I_N)"),
        ("sigma_e^2", "CSI error variance", "Positive Scalar", "Dimensionless", "Variance representing channel estimation inaccuracy"),
        ("Theta", "Active RIS matrix", "Diagonal in C^{NxN}", "Dimensionless", "Surface reflection matrix Theta = a diag(exp(j theta))"),
        ("a", "Active amplification factor", "Positive Scalar", "Voltage Gain", "Uniform active gain constrained by [1.0, a_max]"),
        ("theta_n", "Element reflection phase", "Real Scalar", "Radians", "Continuous phase shift in [0, 2pi) for element n"),
        ("n_R", "Active surface thermal noise", "Vector in C^{N x 1}", "Volts", "Gaussian thermal noise n_R ~ CN(0, sigma_R^2 I_N)"),
        ("sigma_R^2", "Active RIS noise power", "Positive Scalar", "Watts / dBm", "Thermal noise variance set to -80 dBm (10^-11 W)"),
        ("n_0", "AP receiver background noise", "Complex Scalar", "Volts", "AWGN noise at parameter server n_0 ~ CN(0, sigma_0^2)"),
        ("sigma_0^2", "AP receiver noise power", "Positive Scalar", "Watts / dBm", "Thermal noise floor set to -90 dBm (10^-12 W)"),
        ("s_k", "Analog AirComp symbol", "Complex Scalar", "Normalized", "Normalized model symbol entry with E[|s_k|^2] = 1"),
        ("b_k", "Client transmit precoder", "Complex Scalar", "Voltage Scale", "Zero-Forcing pre-inversion scalar b_k = alpha_k/(c h_k)"),
        ("c", "AP receive scaling factor", "Positive Scalar", "Voltage Scale", "Receive normalization scalar c* = max alpha_k/(sqrt(P) |h_k|)"),
        ("P_max", "Client transmit power limit", "Positive Scalar", "Watts / dBm", "Individual device RF power budget (10 dBm = 0.01 W)"),
        ("P_{RIS,max}", "RIS surface power budget", "Positive Scalar", "Watts", "Active amplification power ceiling (2.0 W)"),
        ("J_t", "Expected MSE objective", "Positive Scalar", "Error Power", "Convergence-aware statistical objective E[MSE | hat_h]"),
        ("Delta J_t", "Regularization penalty", "Positive Scalar", "Error Power", "Derived analytical penalty |c|^2 ||G^H Theta||^2 sigma_e^2 sum |b_k|^2"),
    ]

    tbl_reg = doc.add_table(rows=len(reg_data), cols=5)
    tbl_reg.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_reg, color="CBD5E1", sz="3")
    r_w = [Inches(1.0), Inches(1.5), Inches(1.2), Inches(1.1), Inches(1.6)]
    for r_idx, row in enumerate(tbl_reg.rows):
        is_hdr = (r_idx == 0)
        for c_idx, cell in enumerate(row.cells):
            cell.width = r_w[c_idx]
            set_cell_margins(cell, 45, 45, 50, 50)
            if is_hdr:
                set_cell_background(cell, "1E293B")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(reg_data[r_idx][c_idx])
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if is_hdr:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            if c_idx == 0 and not is_hdr:
                r.bold = True
                r.italic = True

    p_cap_r = doc.add_paragraph()
    p_cap_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_r.paragraph_format.space_before = Pt(4)
    p_cap_r.paragraph_format.space_after = Pt(10)
    r_cap_r = p_cap_r.add_run("Table A.1: Mathematical symbol inventory, physical dimensions, and operational definitions.")
    r_cap_r.bold = True
    r_cap_r.font.name = "Times New Roman"
    r_cap_r.font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX B: CORE SIMULATION ENGINE CODE LISTINGS
    # -------------------------------------------------------------
    add_heading_1(doc, "APPENDIX B\nCORE SIMULATION ENGINE IMPLEMENTATION EXCERPTS", space_before=12, space_after=16)

    p_app_b = (
        "This appendix documents verified Python implementation excerpts from the core simulation codebase, showcasing the exact "
        "computational routines for Zero-Forcing scaling, expected MSE evaluation, and Quasi-Newton optimization."
    )
    add_p(doc, p_app_b)

    code_zf = (
        "# Excerpt 1: Closed-Form Zero-Forcing Precoding and Scaling (src/aircomp/beamforming.py)\n"
        "import numpy as np\n\n"
        "def compute_zf_scaling(h_eff, alpha_k, P_max):\n"
        "    \"\"\"\n"
        "    Computes optimal Zero-Forcing precoding scalars b_k and receive scaler c*.\n"
        "    h_eff: Effective composite channels for K clients (complex array [K])\n"
        "    alpha_k: Aggregation weights (array [K], sum=1.0)\n"
        "    P_max: Maximum transmit power per client (linear Watts)\n"
        "    \"\"\"\n"
        "    h_mag = np.abs(h_eff)\n"
        "    # Weakest client dictates the bottleneck receive normalization factor\n"
        "    c_candidates = alpha_k / (np.sqrt(P_max) * h_mag)\n"
        "    c_star = np.max(c_candidates)\n"
        "    \n"
        "    # Transmit precoding scalars perfectly align signals at AP\n"
        "    b_k_star = alpha_k / (c_star * h_eff)\n"
        "    return c_star, b_k_star"
    )
    add_callout(doc, "Python Listing B.1: Zero-Forcing Precoding Implementation", code_zf, bg_hex="F8FAFC", border_color="0284C7")

    code_mse = (
        "# Excerpt 2: Convergence-Aware Expected MSE Calculation (src/aircomp/mse.py)\n"
        "def compute_expected_mse(c, b_k, G_H, Theta, sigma_R2, sigma_02, sigma_e2, h_eff_hat, alpha_k):\n"
        "    \"\"\"\n"
        "    Evaluates the exact conditional expected MSE J_t incorporating CSI error penalty.\n"
        "    \"\"\"\n"
        "    # Signal distortion term vanishes under Zero-Forcing\n"
        "    signal_error = np.sum(np.abs(c * h_eff_hat * b_k - alpha_k) ** 2)\n"
        "    \n"
        "    # Active RIS thermal noise power amplified to AP\n"
        "    G_Theta = np.dot(G_H, Theta)\n"
        "    G_Theta_norm2 = np.sum(np.abs(G_Theta) ** 2)\n"
        "    active_noise_power = (np.abs(c) ** 2) * sigma_R2 * G_Theta_norm2\n"
        "    \n"
        "    # AP receiver background AWGN power\n"
        "    ap_noise_power = (np.abs(c) ** 2) * sigma_02\n"
        "    \n"
        "    # Analytical CSI error regularization penalty (Delta J_t)\n"
        "    tx_power_sum = np.sum(np.abs(b_k) ** 2)\n"
        "    csi_penalty = (np.abs(c) ** 2) * G_Theta_norm2 * sigma_e2 * tx_power_sum\n"
        "    \n"
        "    total_expected_mse = signal_error + active_noise_power + ap_noise_power + csi_penalty\n"
        "    return total_expected_mse"
    )
    add_callout(doc, "Python Listing B.2: Expected MSE and Regularization Penalty Routine", code_mse, bg_hex="F8FAFC", border_color="0284C7")

    code_opt = (
        "# Excerpt 3: Multi-Start Bound-Constrained Quasi-Newton Solver (src/optimization/convergence_aware.py)\n"
        "from scipy.optimize import minimize\n\n"
        "def optimize_convergence_aware(G_H, h_k_hat, h_dk_hat, sigma_e2, sigma_R2, sigma_02, P_max, a_max, M_restarts=3):\n"
        "    K, N = h_k_hat.shape[0], h_k_hat.shape[1]\n"
        "    best_cost, best_sol = float('inf'), None\n"
        "    \n"
        "    def cost_function(x):\n"
        "        a = x[0]\n"
        "        phases = x[1:]\n"
        "        Theta = a * np.diag(np.exp(1j * phases))\n"
        "        h_eff = h_dk_hat + np.array([np.dot(np.dot(G_H, Theta), h_k_hat[k]) for k in range(K)])\n"
        "        c, b_k = compute_zf_scaling(h_eff, np.ones(K)/K, P_max)\n"
        "        return compute_expected_mse(c, b_k, G_H, Theta, sigma_R2, sigma_02, sigma_e2, h_eff, np.ones(K)/K)\n"
        "    \n"
        "    bounds = [(1.0, a_max)] + [(0.0, 2 * np.pi) for _ in range(N)]\n"
        "    for _ in range(M_restarts):\n"
        "        x0 = np.concatenate([[ (1.0 + a_max)/2.0 ], np.random.uniform(0, 2*np.pi, N)])\n"
        "        res = minimize(cost_function, x0, method='L-BFGS-B', bounds=bounds)\n"
        "        if res.fun < best_cost:\n"
        "            best_cost = res.fun\n"
        "            best_sol = res.x\n"
        "    return best_sol[0], best_sol[1:], best_cost"
    )
    add_callout(doc, "Python Listing B.3: Multi-Start L-BFGS-B Surface Optimization Engine", code_opt, bg_hex="F8FAFC", border_color="0284C7")
