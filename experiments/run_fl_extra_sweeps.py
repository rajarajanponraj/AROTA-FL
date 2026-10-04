import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from src.federated_learning.model import get_model
from src.federated_learning.server import FLServer
from src.federated_learning.client import FLClient
from src.federated_learning.partition import partition_dataset_non_iid, partition_dataset_iid
from src.aircomp.aggregation import aggregate_updates_aircomp
from src.channels.rician import generate_rician_channel
from src.channels.path_loss import compute_path_loss
from src.optimization.convergence_aware import optimize_convergence_aware
from src.optimization.mse_minimization import optimize_mse_baseline

def load_mnist_full():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, download=True, transform=transform)
    return train_dataset, test_dataset

def generate_channel(K, N=32):
    d_AP = np.random.uniform(100, 150, K)
    d_RIS_users = np.random.uniform(20, 50, K)
    d_RIS_AP = 80.0
    
    pl_direct = [compute_path_loss(d_AP[k])[1] for k in range(K)]
    pl_ris_users = [compute_path_loss(d_RIS_users[k])[1] for k in range(K)]
    pl_ris_ap = compute_path_loss(d_RIS_AP)[1]
    
    h_direct = np.array([generate_rician_channel(1, 1, k_factor_linear=10.0)[0,0] * np.sqrt(pl_direct[k]) for k in range(K)])
    h_ris = np.array([generate_rician_channel(N, 1, k_factor_linear=10.0)[0] * np.sqrt(pl_ris_users[k]) for k in range(K)])
    G_H = generate_rician_channel(N, 1, k_factor_linear=10.0)[0].reshape(1, N) * np.sqrt(pl_ris_ap)
    
    return h_direct, G_H, h_ris

def run_fl_with_aircomp(train_dataset, test_dataset, num_clients, num_rounds, method, alpha=None, P_max_dbm=10.0):
    if alpha is None:
        client_datasets = partition_dataset_iid(train_dataset, num_clients)
    else:
        client_datasets = partition_dataset_non_iid(train_dataset, num_clients, num_classes=10, alpha=alpha)
        
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    global_model = get_model('mnist')
    server = FLServer(global_model, device=device)
    
    clients = []
    for k in range(num_clients):
        clients.append(FLClient(k, client_datasets[k], batch_size=64, local_epochs=1, lr=0.01, device=device))
        
    test_loader = DataLoader(test_dataset, batch_size=500, num_workers=0, pin_memory=True)
    
    # Wireless Setup
    N = 32
    alphas = np.ones(num_clients) / num_clients
    P_max = 10 ** (P_max_dbm / 10) / 1000
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    h_direct, G_H, h_ris = generate_channel(num_clients, N)
    
    if method == "conv_aware":
        Theta, b, c, _ = optimize_convergence_aware(h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=1)
        h_eff = h_direct + np.squeeze(G_H @ Theta @ h_ris.T)
    elif method == "mse_min":
        Theta, b, c, _ = optimize_mse_baseline(h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=1)
        h_eff = h_direct + np.squeeze(G_H @ Theta @ h_ris.T)
    else:
        Theta, b, c, h_eff = None, None, None, None
        
    acc_history = []
    
    for round_idx in range(num_rounds):
        updates = []
        for client in clients:
            update = client.train(server.global_model)
            updates.append(update)
            
        if method == "ideal":
            noisy_agg = np.mean(updates, axis=0)
        else:
            noisy_agg = aggregate_updates_aircomp(updates, h_eff, b, c, G_H, Theta, sigma_R, sigma_0)
            
        server.update_model(noisy_agg)
        
        # Evaluate only every 5 rounds to save time
        if round_idx % 5 == 0 or round_idx == num_rounds - 1:
            acc, _ = server.evaluate(test_loader)
            acc_history.append(acc)
            
    return acc_history[-1] # Return final accuracy

def run_heterogeneity_sweep():
    print("Running Exp 11: FL Accuracy vs. Data Heterogeneity (Dirichlet alpha)...")
    os.makedirs('results/figures', exist_ok=True)
    train_data, test_data = load_mnist_full()
    
    num_clients = 20
    num_rounds = 100
    
    alphas = [0.1, 0.3, 0.5, 1.0, 3.0, 10.0]
    
    acc_naive = []
    acc_proposed = []
    acc_ideal = []
    
    for alpha in tqdm(alphas, desc="Sweeping Alpha"):
        # Run Naive (MSE-Min)
        acc = run_fl_with_aircomp(train_data, test_data, num_clients, num_rounds, method="mse_min", alpha=alpha)
        acc_naive.append(acc)
        
        # Run Proposed (Convergence-Aware)
        acc = run_fl_with_aircomp(train_data, test_data, num_clients, num_rounds, method="conv_aware", alpha=alpha)
        acc_proposed.append(acc)
        
        # Run Ideal (Noise-free)
        acc = run_fl_with_aircomp(train_data, test_data, num_clients, num_rounds, method="ideal", alpha=alpha)
        acc_ideal.append(acc)
        
    plt.figure(figsize=(8,6))
    plt.plot(alphas, acc_ideal, 'k--', marker='o', label='Ideal (Noise-free)')
    plt.plot(alphas, acc_proposed, 'b-', marker='^', label='Proposed (Convergence-Aware)')
    plt.plot(alphas, acc_naive, 'r-', marker='x', label='Baseline (MSE-Min Active RIS)')
    
    plt.xscale('log')
    plt.xlabel('Dirichlet Heterogeneity Parameter (alpha)')
    plt.ylabel('Final Test Accuracy')
    plt.title('FL Accuracy vs Data Heterogeneity (AirComp Simulation)')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/figures/exp11_acc_vs_heterogeneity.png')
    plt.close()
    print("Saved exp11_acc_vs_heterogeneity.png")

def run_snr_impact_sweep():
    print("Running Exp 12: FL Accuracy vs. Transmit Power Limit (P_max)...")
    train_data, test_data = load_mnist_full()
    
    num_clients = 20
    num_rounds = 100
    
    # Transmit power values in dBm
    p_max_dbm = [-10, -5, 0, 5, 10, 15]
    
    acc_naive = []
    acc_proposed = []
    
    for p_dbm in tqdm(p_max_dbm, desc="Sweeping P_max"):
        # Run Naive
        acc = run_fl_with_aircomp(train_data, test_data, num_clients, num_rounds, method="mse_min", alpha=0.5, P_max_dbm=p_dbm)
        acc_naive.append(acc)
        
        # Run Proposed
        acc = run_fl_with_aircomp(train_data, test_data, num_clients, num_rounds, method="conv_aware", alpha=0.5, P_max_dbm=p_dbm)
        acc_proposed.append(acc)
        
    plt.figure(figsize=(8,6))
    plt.plot(p_max_dbm, acc_proposed, 'b-', marker='^', label='Proposed (Convergence-Aware)')
    plt.plot(p_max_dbm, acc_naive, 'r-', marker='x', label='Baseline (MSE-Min Active RIS)')
    
    plt.xlabel('Maximum Transmit Power P_max (dBm)')
    plt.ylabel('Final Test Accuracy (Non-IID)')
    plt.title('FL Accuracy vs Transmit Power Budget (AirComp Simulation)')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/figures/exp12_acc_vs_snr.png')
    plt.close()
    print("Saved exp12_acc_vs_snr.png")

if __name__ == "__main__":
    run_heterogeneity_sweep()
    run_snr_impact_sweep()
    print("Extra experiments complete!")
