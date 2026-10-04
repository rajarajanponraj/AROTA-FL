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
from src.federated_learning.partition import partition_dataset_non_iid
from src.aircomp.aggregation import aggregate_updates_aircomp
from src.channels.rician import generate_rician_channel
from src.channels.path_loss import compute_path_loss
from src.optimization.convergence_aware import optimize_convergence_aware
from src.optimization.mse_minimization import optimize_mse_baseline

def load_cifar10_full():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    train_dataset = datasets.CIFAR10('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.CIFAR10('./data', train=False, download=True, transform=transform)
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

def run_exp10_cifar10_seed(train_data, test_data, num_clients, num_rounds, method, seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    client_datasets = partition_dataset_non_iid(train_data, num_clients, num_classes=10, alpha=0.5)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    server = FLServer(get_model('cifar10'), device=device)
    clients = [FLClient(k, client_datasets[k], batch_size=32, local_epochs=1, lr=0.01, device=device) for k in range(num_clients)]
    test_loader = DataLoader(test_data, batch_size=500, num_workers=0, pin_memory=True)
    
    N = 32
    alphas = np.ones(num_clients) / num_clients
    P_max = 10 ** (10 / 10) / 1000
    P_RIS_max = 2.0
    sigma_0, sigma_R, sigma_e = 1e-12, 1e-11, 0.1
    a_max = 15.0
    
    h_direct_true, G_H_true, h_ris_true = generate_channel(num_clients, N)
    
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
    
    for _ in range(num_rounds):
        updates = [client.train(server.global_model) for client in clients]
            
        if method == "ideal":
            noisy_agg = np.mean(updates, axis=0)
        else:
            noisy_agg = aggregate_updates_aircomp(updates, h_eff_true, b, c, G_H_true, Theta, sigma_R, sigma_0)
            
        server.update_model(noisy_agg)
        acc_history.append(server.evaluate(test_loader)[0])
        
    return acc_history

def run_multiseed_scenario(train_data, test_data, num_clients, num_rounds, method, label, num_seeds=3):
    print(f"Running CIFAR-10 {label} over {num_seeds} seeds...")
    acc_seeds = []
    for seed in tqdm(range(num_seeds)):
        acc_seeds.append(run_exp10_cifar10_seed(train_data, test_data, num_clients, num_rounds, method, seed))
    return np.mean(acc_seeds, axis=0), np.std(acc_seeds, axis=0)

def run_exp10_cifar10():
    print("Running Exp 10: CIFAR-10 FL Convergence under True AirComp...")
    num_clients = 20
    num_rounds = 100
    num_seeds = 3
    
    train_data, test_data = load_cifar10_full()
    
    mean_ideal, _ = run_multiseed_scenario(train_data, test_data, num_clients, num_rounds, "ideal", "Ideal Channel", num_seeds)
    mean_mse, std_mse = run_multiseed_scenario(train_data, test_data, num_clients, num_rounds, "mse_min", "MSE-Min", num_seeds)
    mean_conv, std_conv = run_multiseed_scenario(train_data, test_data, num_clients, num_rounds, "conv_aware", "Conv-Aware", num_seeds)
    
    plt.figure(figsize=(8,6))
    rounds_range = range(num_rounds + 1)
    
    plt.plot(rounds_range, mean_ideal, 'k--', label='Ideal Channel')
    
    plt.plot(rounds_range, mean_mse, 'r-', label='MSE-Min Active RIS')
    plt.fill_between(rounds_range, mean_mse - std_mse, mean_mse + std_mse, color='r', alpha=0.2)
    
    plt.plot(rounds_range, mean_conv, 'g-', label='Conv-Aware Active RIS')
    plt.fill_between(rounds_range, mean_conv - std_conv, mean_conv + std_conv, color='g', alpha=0.2)
    
    plt.xlabel('Communication Round')
    plt.ylabel('Test Accuracy (%)')
    plt.legend()
    plt.grid(True)
    plt.title('Exp 10: CIFAR-10 FL Convergence (Non-IID, Multi-seed)')
    plt.savefig('results/figures/exp10_cifar10_convergence_stat.png')
    plt.close()

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    run_exp10_cifar10()
    print("Done! Check results/figures for the output.")
