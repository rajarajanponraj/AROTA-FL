import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.federated_learning.model import get_model
from src.federated_learning.server import FLServer
from src.federated_learning.client import FLClient
from src.federated_learning.partition import partition_dataset_iid, partition_dataset_non_iid
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
    
    h_direct_true = np.array([generate_rician_channel(1, 1, k_factor_linear=10.0)[0,0] * np.sqrt(pl_direct[k]) for k in range(K)])
    h_ris_true = np.array([generate_rician_channel(N, 1, k_factor_linear=10.0)[0] * np.sqrt(pl_ris_users[k]) for k in range(K)])
    G_H_true = generate_rician_channel(N, 1, k_factor_linear=10.0)[0].reshape(1, N) * np.sqrt(pl_ris_ap)
    
    return h_direct_true, G_H_true, h_ris_true

def run_fl_simulation_seed(train_dataset, test_dataset, num_clients, num_rounds, method, iid, seed):
    # Set identical random seeds for identical data partitions and network initializations
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if iid:
        client_datasets = partition_dataset_iid(train_dataset, num_clients)
    else:
        client_datasets = partition_dataset_non_iid(train_dataset, num_clients, num_classes=10, alpha=0.5)
        
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    global_model = get_model('mnist')
    server = FLServer(global_model, device=device)
    
    clients = []
    for k in range(num_clients):
        clients.append(FLClient(k, client_datasets[k], batch_size=64, local_epochs=1, lr=0.01, device=device))
        
    test_loader = DataLoader(test_dataset, batch_size=500, num_workers=0, pin_memory=True)
    
    N = 32
    alphas = np.ones(num_clients) / num_clients
    P_max = 10 ** (10 / 10) / 1000
    P_RIS_max = 2.0
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    # 1. True Channels
    h_direct_true, G_H_true, h_ris_true = generate_channel(num_clients, N)
    
    # 2. Estimated Channels (CSI Uncertainty)
    h_direct_hat = h_direct_true + (np.random.randn(*h_direct_true.shape) + 1j*np.random.randn(*h_direct_true.shape)) * np.sqrt(sigma_e**2 / 2)
    G_H_hat = G_H_true + (np.random.randn(*G_H_true.shape) + 1j*np.random.randn(*G_H_true.shape)) * np.sqrt(sigma_e**2 / 2)
    h_ris_hat = h_ris_true + (np.random.randn(*h_ris_true.shape) + 1j*np.random.randn(*h_ris_true.shape)) * np.sqrt(sigma_e**2 / 2)
    
    if method == "conv_aware":
        Theta, b, c, _ = optimize_convergence_aware(h_direct_hat, G_H_hat, h_ris_hat, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, P_RIS_max=P_RIS_max, num_restarts=1)
        h_eff_true = h_direct_true + np.squeeze(G_H_true @ Theta @ h_ris_true.T)
    elif method == "mse_min":
        Theta, b, c, _ = optimize_mse_baseline(h_direct_hat, G_H_hat, h_ris_hat, alphas, P_max, sigma_R, sigma_0, a_max, P_RIS_max=P_RIS_max, num_restarts=1)
        h_eff_true = h_direct_true + np.squeeze(G_H_true @ Theta @ h_ris_true.T)
    else:
        Theta, b, c, h_eff_true = None, None, None, None
        
    acc_history = [server.evaluate(test_loader)[0]]
    
    for round_idx in tqdm(range(num_rounds), desc="Rounds", leave=False):
        updates = [client.train(server.global_model) for client in clients]
            
        if method == "ideal":
            noisy_agg = np.mean(updates, axis=0)
        else:
            # Physical Layer Simulation: Pass True channel, but Optimization used Hat channels!
            noisy_agg = aggregate_updates_aircomp(updates, h_eff_true, b, c, G_H_true, Theta, sigma_R, sigma_0)
            
        server.update_model(noisy_agg)
        acc_history.append(server.evaluate(test_loader)[0])
        
    return acc_history

def run_fl_simulation_multiseed(train_data, test_data, num_clients, num_rounds, method, iid, label, num_seeds=3):
    print(f"Running: {label} (Method: {method}) over {num_seeds} seeds")
    acc_seeds = []
    for seed in tqdm(range(num_seeds), desc="Seeds"):
        acc = run_fl_simulation_seed(train_data, test_data, num_clients, num_rounds, method, iid, seed)
        acc_seeds.append(acc)
        
    acc_mean = np.mean(acc_seeds, axis=0)
    acc_std = np.std(acc_seeds, axis=0)
    return acc_mean, acc_std

def run_exp7_8_9():
    num_clients = 20
    num_rounds = 60
    num_seeds = 3
    
    train_data, test_data = load_mnist_full()
    
    mean_iid, _ = run_fl_simulation_multiseed(train_data, test_data, num_clients, num_rounds, "ideal", True, "IID Ideal", num_seeds)
    mean_non_iid, _ = run_fl_simulation_multiseed(train_data, test_data, num_clients, num_rounds, "ideal", False, "Non-IID Ideal", num_seeds)
    mean_mse, std_mse = run_fl_simulation_multiseed(train_data, test_data, num_clients, num_rounds, "mse_min", False, "MSE-Min", num_seeds)
    mean_conv, std_conv = run_fl_simulation_multiseed(train_data, test_data, num_clients, num_rounds, "conv_aware", False, "Conv-Aware", num_seeds)
    
    plt.figure(figsize=(8,6))
    rounds_range = range(num_rounds + 1)
    
    plt.plot(rounds_range, mean_iid, 'k--', label='IID (Perfect Channel)')
    plt.plot(rounds_range, mean_non_iid, 'b-', label='Non-IID (Perfect Channel)')
    
    plt.plot(rounds_range, mean_mse, 'r-', label='Non-IID (Active RIS - MSE Min)')
    plt.fill_between(rounds_range, mean_mse - std_mse, mean_mse + std_mse, color='r', alpha=0.2)
    
    plt.plot(rounds_range, mean_conv, 'g-', label='Non-IID (Active RIS - Proposed Conv-Aware)')
    plt.fill_between(rounds_range, mean_conv - std_conv, mean_conv + std_conv, color='g', alpha=0.2)
    
    plt.xlabel('Communication Round')
    plt.ylabel('Test Accuracy (%)')
    plt.legend()
    plt.grid(True)
    plt.title('Exp 7-9: FL Convergence on MNIST (True AirComp + CSI Errors)')
    plt.savefig('results/figures/exp7_9_fl_convergence_stat.eps')
    plt.close()

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    run_exp7_8_9()
    print("Done! Check results/figures for the output.")
