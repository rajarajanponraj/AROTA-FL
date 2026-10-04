import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
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
    
    # Use full dataset for publication
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

def run_fl_simulation(train_dataset, test_dataset, num_clients, num_rounds, method="ideal", iid=True, label=""):
    print(f"Running FL Simulation: {label} (Method: {method})")
    
    if iid:
        client_datasets = partition_dataset_iid(train_dataset, num_clients)
    else:
        client_datasets = partition_dataset_non_iid(train_dataset, num_clients, num_classes=10, alpha=0.5)
        
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    global_model = get_model('mnist')
    server = FLServer(global_model, device=device)
    
    clients = []
    for k in range(num_clients):
        # Batch size 64 is standard for full FL simulations
        clients.append(FLClient(k, client_datasets[k], batch_size=64, local_epochs=1, lr=0.01, device=device))
        
    # Larger batch size for faster evaluation
    test_loader = DataLoader(test_dataset, batch_size=500, num_workers=0, pin_memory=True)
    
    # Pre-generate Channel & Optimization exactly once to simulate a block-fading environment
    # In a fully dynamic channel, this would be computed per-round.
    N = 32
    alphas = np.ones(num_clients) / num_clients
    P_max = 10 ** (10 / 10) / 1000
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
    
    # Pre-evaluate
    acc, _ = server.evaluate(test_loader)
    acc_history.append(acc)
    
    for round_idx in tqdm(range(num_rounds)):
        updates = []
        for client in clients:
            update = client.train(server.global_model)
            updates.append(update)
            
        if method == "ideal":
            noisy_agg = np.mean(updates, axis=0)
        else:
            # Here we actually demonstrate the Convergence-Aware Active RIS in the FL loop!
            # The updates are physically aggregated over-the-air.
            noisy_agg = aggregate_updates_aircomp(updates, h_eff, b, c, G_H, Theta, sigma_R, sigma_0)
            
        server.update_model(noisy_agg)
        
        acc, _ = server.evaluate(test_loader)
        acc_history.append(acc)
        
    return acc_history

def run_exp7_8_9():
    num_clients = 20 # 20 clients is standard for wireless FL papers
    num_rounds = 100 # 100 rounds to show full convergence
    
    train_data, test_data = load_mnist_full()
    
    # 1. Baseline IID vs Non-IID (No noise)
    acc_iid = run_fl_simulation(train_data, test_data, num_clients, num_rounds, method="ideal", iid=True, label="IID (Perfect Channel)")
    acc_non_iid = run_fl_simulation(train_data, test_data, num_clients, num_rounds, method="ideal", iid=False, label="Non-IID (Perfect Channel)")
    
    # 2. Noisy channel (Actual AirComp with Convergence-Aware vs MSE-Min)
    acc_mse_min = run_fl_simulation(train_data, test_data, num_clients, num_rounds, method="mse_min", iid=False, label="Non-IID (Active RIS - MSE Min)")
    acc_conv_aware = run_fl_simulation(train_data, test_data, num_clients, num_rounds, method="conv_aware", iid=False, label="Non-IID (Active RIS - Conv-Aware)")
    
    plt.figure(figsize=(8,6))
    plt.plot(acc_iid, 'k-o', label='IID (Perfect Channel)')
    plt.plot(acc_non_iid, 'b-s', label='Non-IID (Perfect Channel)')
    plt.plot(acc_mse_min, 'r-x', label='Non-IID (Active RIS - MSE Min)')
    plt.plot(acc_conv_aware, 'g-^', label='Non-IID (Active RIS - Proposed Conv-Aware)')
    
    plt.xlabel('Communication Round')
    plt.ylabel('Test Accuracy (%)')
    plt.legend()
    plt.grid(True)
    plt.title('Exp 7-9: FL Convergence on MNIST (AirComp Integration)')
    plt.savefig('results/figures/exp7_9_fl_convergence.png')
    plt.close()

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    run_exp7_8_9()
    print("Done! Check results/figures for the output.")
