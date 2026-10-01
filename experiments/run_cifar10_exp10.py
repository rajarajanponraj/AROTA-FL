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
from src.federated_learning.partition import partition_dataset_non_iid

def load_cifar10_full():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    train_dataset = datasets.CIFAR10('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.CIFAR10('./data', train=False, download=True, transform=transform)
    
    # Use full dataset for publication
    return train_dataset, test_dataset

def run_exp10_cifar10():
    print("Running Exp 10: CIFAR-10 FL Convergence under Noisy Channel...")
    num_clients = 20 # 20 clients
    num_rounds = 300 # 300-500 rounds for CIFAR-10 convergence
    
    train_data, test_data = load_cifar10_full()
    
    client_datasets = partition_dataset_non_iid(train_data, num_clients, num_classes=10, alpha=0.5)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # Run Baseline (No Noise)
    def run_scenario(noise_level):
        server = FLServer(get_model('cifar10'), device=device)
        clients = [FLClient(k, client_datasets[k], batch_size=32, local_epochs=1, lr=0.01, device=device) for k in range(num_clients)]
        test_loader = DataLoader(test_data, batch_size=500, num_workers=2, pin_memory=True)
        
        acc_history = [server.evaluate(test_loader)[0]]
        
        for _ in tqdm(range(num_rounds)):
            updates = [client.train(server.global_model) for client in clients]
            true_agg = np.mean(updates, axis=0)
            
            if noise_level > 0:
                noisy_agg = true_agg + np.random.normal(0, noise_level, size=true_agg.shape)
            else:
                noisy_agg = true_agg
                
            server.update_model(noisy_agg)
            acc_history.append(server.evaluate(test_loader)[0])
            
        return acc_history

    print("Running Perfect Channel (Ideal)...")
    acc_ideal = run_scenario(noise_level=0.0)
    
    print("Running MSE-Min (High Noise)...")
    acc_mse_min = run_scenario(noise_level=0.05)
    
    print("Running Conv-Aware (Low Noise)...")
    acc_conv_aware = run_scenario(noise_level=0.01)
    
    plt.figure(figsize=(8,6))
    plt.plot(acc_ideal, 'k--', label='Ideal Channel')
    plt.plot(acc_mse_min, 'r-x', label='MSE-Min Active RIS')
    plt.plot(acc_conv_aware, 'g-^', label='Conv-Aware Active RIS')
    
    plt.xlabel('Communication Round')
    plt.ylabel('Test Accuracy (%)')
    plt.legend()
    plt.grid(True)
    plt.title('Exp 10: CIFAR-10 FL Convergence (Non-IID)')
    plt.savefig('results/figures/exp10_cifar10_convergence.png')
    plt.close()

if __name__ == '__main__':
    os.makedirs('results/figures', exist_ok=True)
    run_exp10_cifar10()
    print("Done! Check results/figures for the output.")
