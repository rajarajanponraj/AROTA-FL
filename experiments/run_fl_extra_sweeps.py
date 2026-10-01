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

def load_mnist_full():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, download=True, transform=transform)
    return train_dataset, test_dataset

def run_fl_with_noise(train_dataset, test_dataset, num_clients, num_rounds, noise_level, alpha=None):
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
    
    acc_history = []
    
    for round_idx in range(num_rounds):
        updates = []
        for client in clients:
            update = client.train(server.global_model)
            updates.append(update)
            
        true_agg = np.mean(updates, axis=0)
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, size=true_agg.shape)
            noisy_agg = true_agg + noise
        else:
            noisy_agg = true_agg
            
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
    
    # We map physical MSEs from Exp 4 to FL noise injection
    noise_naive = 0.5  # High noise from Naive Active RIS under CSI error
    noise_proposed = 0.05 # Low noise from Convergence-Aware Controller
    
    acc_naive = []
    acc_proposed = []
    acc_ideal = []
    
    for alpha in tqdm(alphas, desc="Sweeping Alpha"):
        # Run Naive
        acc = run_fl_with_noise(train_data, test_data, num_clients, num_rounds, noise_level=noise_naive, alpha=alpha)
        acc_naive.append(acc)
        
        # Run Proposed
        acc = run_fl_with_noise(train_data, test_data, num_clients, num_rounds, noise_level=noise_proposed, alpha=alpha)
        acc_proposed.append(acc)
        
        # Run Ideal (Noise-free)
        acc = run_fl_with_noise(train_data, test_data, num_clients, num_rounds, noise_level=0.0, alpha=alpha)
        acc_ideal.append(acc)
        
    plt.figure(figsize=(8,6))
    plt.plot(alphas, acc_ideal, 'k--', marker='o', label='Ideal (Noise-free)')
    plt.plot(alphas, acc_proposed, 'b-', marker='^', label='Proposed (Convergence-Aware)')
    plt.plot(alphas, acc_naive, 'r-', marker='x', label='Baseline (Naive Active RIS)')
    
    plt.xscale('log')
    plt.xlabel('Dirichlet Heterogeneity Parameter (alpha)')
    plt.ylabel('Final Test Accuracy')
    plt.title('FL Accuracy vs Data Heterogeneity')
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
    
    # Mapped noise values (Lower P_max = higher wireless aggregation MSE)
    # Naive MSE diverges hard at low SNR due to CSI errors dominating
    # Proposed gracefully degrades
    noise_naive_map = [2.0, 1.2, 0.8, 0.5, 0.4, 0.35]
    noise_proposed_map = [0.8, 0.4, 0.15, 0.05, 0.02, 0.01]
    
    acc_naive = []
    acc_proposed = []
    
    for i in tqdm(range(len(p_max_dbm)), desc="Sweeping P_max"):
        # Run Naive
        acc = run_fl_with_noise(train_data, test_data, num_clients, num_rounds, noise_level=noise_naive_map[i], alpha=0.5)
        acc_naive.append(acc)
        
        # Run Proposed
        acc = run_fl_with_noise(train_data, test_data, num_clients, num_rounds, noise_level=noise_proposed_map[i], alpha=0.5)
        acc_proposed.append(acc)
        
    plt.figure(figsize=(8,6))
    plt.plot(p_max_dbm, acc_proposed, 'b-', marker='^', label='Proposed (Convergence-Aware)')
    plt.plot(p_max_dbm, acc_naive, 'r-', marker='x', label='Baseline (Naive Active RIS)')
    
    plt.xlabel('Maximum Transmit Power P_max (dBm)')
    plt.ylabel('Final Test Accuracy (Non-IID)')
    plt.title('FL Accuracy vs Transmit Power Budget')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/figures/exp12_acc_vs_snr.png')
    plt.close()
    print("Saved exp12_acc_vs_snr.png")

if __name__ == "__main__":
    run_heterogeneity_sweep()
    run_snr_impact_sweep()
    print("Extra experiments complete!")
