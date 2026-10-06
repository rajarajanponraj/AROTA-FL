import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from src.channels.rician import generate_rician_channel
from src.channels.path_loss import compute_path_loss
from src.optimization.baselines import passive_ris_baseline
from src.optimization.mse_minimization import optimize_mse_baseline
from src.optimization.convergence_aware import optimize_convergence_aware
from src.aircomp.mse import compute_expected_mse

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

def run_exp5_ris_size_sweep(num_seeds=5):
    print("Running Exp 5: RIS Size Sweep...")
    K = 10
    d_AP = np.random.uniform(100, 150, K)
    d_RIS_users = np.random.uniform(20, 50, K)
    d_RIS_AP = 80.0
    alphas = np.ones(K) / K
    P_max = 10 ** (10 / 10) / 1000
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    N_range = [16, 32, 64, 128]
    res_mse = {'Passive': [], 'MSE-Min Active': [], 'Conv-Aware Active': []}
    
    for N in tqdm(N_range):
        m_pass, m_opt, m_conv = 0, 0, 0
        for seed in range(num_seeds):
            np.random.seed(seed)
            hd, G, hr = get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP)
            
            Tp, bp, cp = passive_ris_baseline(hd, G, hr, alphas, P_max)
            m_pass += compute_expected_mse(hd+np.squeeze(G@Tp@hr.T), bp, cp, alphas, G, Tp, sigma_R, sigma_0, sigma_e)
            
            Tm, bm, cm, _ = optimize_mse_baseline(hd, G, hr, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
            m_opt += compute_expected_mse(hd+np.squeeze(G@Tm@hr.T), bm, cm, alphas, G, Tm, sigma_R, sigma_0, sigma_e)
            
            Tc, bc, cc, _ = optimize_convergence_aware(hd, G, hr, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=1)
            m_conv += compute_expected_mse(hd+np.squeeze(G@Tc@hr.T), bc, cc, alphas, G, Tc, sigma_R, sigma_0, sigma_e)
            
        res_mse['Passive'].append(m_pass / num_seeds)
        res_mse['MSE-Min Active'].append(m_opt / num_seeds)
        res_mse['Conv-Aware Active'].append(m_conv / num_seeds)
        
    plot_and_save(N_range, res_mse, 'Number of RIS Elements ($N$)', 'Expected MSE', 'Exp 5: Impact of RIS Size', 'exp5_ris_size.eps')

def run_exp6_client_count_sweep(num_seeds=5):
    print("Running Exp 6: Client Count Sweep...")
    N = 32
    d_RIS_AP = 80.0
    P_max = 10 ** (10 / 10) / 1000
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    K_range = [5, 10, 20]
    res_mse = {'MSE-Min Active': [], 'Conv-Aware Active': []}
    
    for K in tqdm(K_range):
        np.random.seed(42) # Ensure consistent distances for same K
        d_AP = np.random.uniform(100, 150, K)
        d_RIS_users = np.random.uniform(20, 50, K)
        alphas = np.ones(K) / K
        
        m_opt, m_conv = 0, 0
        for seed in range(num_seeds):
            np.random.seed(seed)
            hd, G, hr = get_channel_realization(K, N, d_AP, d_RIS_users, d_RIS_AP)
            
            Tm, bm, cm, _ = optimize_mse_baseline(hd, G, hr, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
            m_opt += compute_expected_mse(hd+np.squeeze(G@Tm@hr.T), bm, cm, alphas, G, Tm, sigma_R, sigma_0, sigma_e)
            
            Tc, bc, cc, _ = optimize_convergence_aware(hd, G, hr, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=1)
            m_conv += compute_expected_mse(hd+np.squeeze(G@Tc@hr.T), bc, cc, alphas, G, Tc, sigma_R, sigma_0, sigma_e)
            
        res_mse['MSE-Min Active'].append(m_opt / num_seeds)
        res_mse['Conv-Aware Active'].append(m_conv / num_seeds)
        
    plot_and_save(K_range, res_mse, 'Number of Clients ($K$)', 'Expected MSE', 'Exp 6: Impact of Client Scalability', 'exp6_client_count.eps')

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    run_exp5_ris_size_sweep(num_seeds=500)
    run_exp6_client_count_sweep(num_seeds=500)
    print("Done! Check results/figures for the output.")
