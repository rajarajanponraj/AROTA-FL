import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from src.channels.rician import generate_rician_channel
from src.channels.path_loss import compute_path_loss
from src.optimization.baselines import (
    passive_ris_baseline, 
    fixed_active_ris_baseline,
    no_ris_baseline
)
from src.optimization.mse_minimization import optimize_mse_baseline
from src.optimization.convergence_aware import optimize_convergence_aware
from src.aircomp.mse import compute_expected_mse

# Common setup for all experiments
def get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP):
    pl_direct = [compute_path_loss(d_AP[k])[1] for k in range(K)]
    pl_ris_users = [compute_path_loss(d_RIS_users[k])[1] for k in range(K)]
    pl_ris_ap = compute_path_loss(d_RIS_AP)[1]
    
    h_direct = np.array([generate_rician_channel(1, 1, k_factor_linear=10.0)[0,0] * np.sqrt(pl_direct[k]) for k in range(K)])
    h_ris = np.array([generate_rician_channel(N, 1, k_factor_linear=10.0)[0] * np.sqrt(pl_ris_users[k]) for k in range(K)])
    G_H = generate_rician_channel(N, 1, k_factor_linear=10.0)[0].reshape(1, N) * np.sqrt(pl_ris_ap)
    
    return h_direct, G_H, h_ris

def plot_and_save(x_data, y_dict, xlabel, ylabel, title, filename):
    plt.figure(figsize=(8,6))
    markers = ['o', 's', '^', 'd', 'x']
    colors = ['r', 'b', 'g', 'm', 'k']
    
    for i, (label, y_data) in enumerate(y_dict.items()):
        plt.plot(x_data, y_data, marker=markers[i%len(markers)], color=colors[i%len(colors)], label=label)
        
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if 'MSE' in ylabel:
        plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.title(title)
    plt.savefig(f'results/figures/{filename}')
    plt.close()

def run_exp1_mse_vs_amplification(num_seeds=5):
    print("Running Exp 1: MSE vs Amplification...")
    K, N = 10, 32
    d_AP = np.random.uniform(100, 150, K)
    d_RIS_users = np.random.uniform(20, 50, K)
    d_RIS_AP = 80.0
    alphas = np.ones(K) / K
    P_max = 10 ** (10 / 10) / 1000
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    
    a_max_range = np.linspace(1.0, 20.0, 10)
    res = {'Passive': [], 'Fixed Active': [], 'MSE-Min Active': [], 'Conv-Aware Active': []}
    
    for a_max in tqdm(a_max_range):
        m_pass, m_act, m_opt, m_conv = 0, 0, 0, 0
        for seed in range(num_seeds):
            np.random.seed(seed)
            hd, G, hr = get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP)
            
            Tp, bp, cp = passive_ris_baseline(hd, G, hr, alphas, P_max)
            m_pass += compute_expected_mse(hd+np.squeeze(G@Tp@hr.T), bp, cp, alphas, G, Tp, sigma_R, sigma_0, sigma_e)
            
            Ta, ba, ca = fixed_active_ris_baseline(hd, G, hr, alphas, P_max, a_max)
            m_act += compute_expected_mse(hd+np.squeeze(G@Ta@hr.T), ba, ca, alphas, G, Ta, sigma_R, sigma_0, sigma_e)
            
            Tm, bm, cm, _ = optimize_mse_baseline(hd, G, hr, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
            m_opt += compute_expected_mse(hd+np.squeeze(G@Tm@hr.T), bm, cm, alphas, G, Tm, sigma_R, sigma_0, sigma_e)
            
            Tc, bc, cc, _ = optimize_convergence_aware(hd, G, hr, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=1)
            m_conv += compute_expected_mse(hd+np.squeeze(G@Tc@hr.T), bc, cc, alphas, G, Tc, sigma_R, sigma_0, sigma_e)
            
        res['Passive'].append(m_pass / num_seeds)
        res['Fixed Active'].append(m_act / num_seeds)
        res['MSE-Min Active'].append(m_opt / num_seeds)
        res['Conv-Aware Active'].append(m_conv / num_seeds)
        
    plot_and_save(a_max_range, res, 'Max Amplification ($a_{max}$)', 'Expected MSE', 'Exp 1: MSE vs Amplification', 'exp1_mse_vs_amp.png')

def run_exp2_3_snr_sweep(num_seeds=5):
    print("Running Exp 2 & 3: MSE and Amplification vs SNR...")
    K, N = 10, 32
    d_AP = np.random.uniform(100, 150, K)
    d_RIS_users = np.random.uniform(20, 50, K)
    d_RIS_AP = 80.0
    alphas = np.ones(K) / K
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    # SNR sweep effectively by varying P_max from -10 dBm to 30 dBm
    P_dbm_range = np.linspace(-10, 30, 8)
    
    res_mse = {'Passive': [], 'MSE-Min Active': [], 'Conv-Aware Active': []}
    res_amp = {'MSE-Min Active': [], 'Conv-Aware Active': []}
    
    for p_dbm in tqdm(P_dbm_range):
        P_max = 10 ** (p_dbm / 10) / 1000
        m_pass, m_opt, m_conv = 0, 0, 0
        a_opt_mean, a_conv_mean = 0, 0
        
        for seed in range(num_seeds):
            np.random.seed(seed)
            hd, G, hr = get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP)
            
            Tp, bp, cp = passive_ris_baseline(hd, G, hr, alphas, P_max)
            m_pass += compute_expected_mse(hd+np.squeeze(G@Tp@hr.T), bp, cp, alphas, G, Tp, sigma_R, sigma_0, sigma_e)
            
            Tm, bm, cm, _ = optimize_mse_baseline(hd, G, hr, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
            m_opt += compute_expected_mse(hd+np.squeeze(G@Tm@hr.T), bm, cm, alphas, G, Tm, sigma_R, sigma_0, sigma_e)
            a_opt_mean += np.abs(Tm[0,0])
            
            Tc, bc, cc, _ = optimize_convergence_aware(hd, G, hr, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=1)
            m_conv += compute_expected_mse(hd+np.squeeze(G@Tc@hr.T), bc, cc, alphas, G, Tc, sigma_R, sigma_0, sigma_e)
            a_conv_mean += np.abs(Tc[0,0])
            
        res_mse['Passive'].append(m_pass / num_seeds)
        res_mse['MSE-Min Active'].append(m_opt / num_seeds)
        res_mse['Conv-Aware Active'].append(m_conv / num_seeds)
        
        res_amp['MSE-Min Active'].append(a_opt_mean / num_seeds)
        res_amp['Conv-Aware Active'].append(a_conv_mean / num_seeds)
        
    plot_and_save(P_dbm_range, res_mse, 'Transmit Power Budget $P_{max}$ (dBm)', 'Expected MSE', 'Exp 2: MSE vs Power Budget', 'exp2_mse_vs_snr.png')
    plot_and_save(P_dbm_range, res_amp, 'Transmit Power Budget $P_{max}$ (dBm)', 'Optimal Amplification Factor', 'Exp 3: Amplification vs Power Budget', 'exp3_amp_vs_snr.png')

def run_exp4_csi_error_sweep(num_seeds=5):
    print("Running Exp 4: CSI Error Sweep...")
    K, N = 10, 32
    d_AP = np.random.uniform(100, 150, K)
    d_RIS_users = np.random.uniform(20, 50, K)
    d_RIS_AP = 80.0
    alphas = np.ones(K) / K
    P_max = 10 ** (10 / 10) / 1000
    sigma_0, sigma_R = 1e-12, 1e-11
    a_max = 15.0
    
    error_range = np.linspace(0.0, 0.3, 8)
    res_mse = {'MSE-Min Active': [], 'Conv-Aware Active': []}
    
    for err in tqdm(error_range):
        m_opt, m_conv = 0, 0
        for seed in range(num_seeds):
            np.random.seed(seed)
            hd, G, hr = get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP)
            
            Tm, bm, cm, _ = optimize_mse_baseline(hd, G, hr, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
            m_opt += compute_expected_mse(hd+np.squeeze(G@Tm@hr.T), bm, cm, alphas, G, Tm, sigma_R, sigma_0, err)
            
            Tc, bc, cc, _ = optimize_convergence_aware(hd, G, hr, alphas, P_max, sigma_R, sigma_0, err, a_max, num_restarts=1)
            m_conv += compute_expected_mse(hd+np.squeeze(G@Tc@hr.T), bc, cc, alphas, G, Tc, sigma_R, sigma_0, err)
            
        res_mse['MSE-Min Active'].append(m_opt / num_seeds)
        res_mse['Conv-Aware Active'].append(m_conv / num_seeds)
        
    plot_and_save(error_range, res_mse, 'CSI Error Variance $\sigma_e^2$', 'Expected MSE', 'Exp 4: Robustness to CSI Error', 'exp4_csi_sweep.png')

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    # Publication scale (500 seeds)
    run_exp1_mse_vs_amplification(num_seeds=500)
    run_exp2_3_snr_sweep(num_seeds=500)
    run_exp4_csi_error_sweep(num_seeds=500)
    print("Done! Check results/figures for the output.")
