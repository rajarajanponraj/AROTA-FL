import numpy as np
import torch
from torch.utils.data import TensorDataset
from src.federated_learning.model import get_model
from src.federated_learning.server import FLServer
from src.federated_learning.client import FLClient
from src.aircomp.aggregation import aggregate_updates_aircomp

def test_aircomp_degrades_accuracy():
    # Set seeds for reproducibility
    np.random.seed(42)
    torch.manual_seed(42)
    
    num_users = 3
    num_antennas = 4
    
    # Create a simple synthetic dataset that is easy to overfit
    X = torch.randn(60, 1, 28, 28)
    # Simple binary classification-like target
    y = (X.sum(dim=(1,2,3)) > 0).long()
    
    # Run two parallel scenarios: Low Noise and High Noise
    # to prove that high noise degrades the model updates.
    
    def run_scenario(sigma_R, sigma_0):
        torch.manual_seed(42)
        global_model = get_model('mnist')
        server = FLServer(global_model)
        
        # Partition data trivially
        clients = []
        for k in range(num_users):
            subset = TensorDataset(X[k*20:(k+1)*20], y[k*20:(k+1)*20])
            clients.append(FLClient(k, subset, batch_size=10, local_epochs=1, lr=0.1))
            
        # 1 round of FL
        updates = []
        for client in clients:
            update = client.train(server.global_model)
            updates.append(update)
            
        # Mock optimal channel and beamforming
        h_eff = np.ones(num_users)
        b = np.ones(num_users) / num_users
        c = 1.0
        G_H = np.ones((1, num_antennas))
        Theta = np.eye(num_antennas)
        
        # AirComp Aggregation
        noisy_aggregated_update = aggregate_updates_aircomp(
            updates, h_eff, b, c, G_H, Theta, sigma_R, sigma_0
        )
        
        # Update server
        server.update_model(noisy_aggregated_update)
        
        # Evaluate training loss
        # (For a proper test, test loss/acc is better, but training loss shows if we learned anything)
        test_dataset = TensorDataset(X, y)
        test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=60)
        acc, loss = server.evaluate(test_loader)
        return acc, loss
        
    acc_low_noise, loss_low_noise = run_scenario(sigma_R=0.001, sigma_0=0.001)
    acc_high_noise, loss_high_noise = run_scenario(sigma_R=5.0, sigma_0=5.0)
    
    # High noise should result in a worse model (higher loss, lower accuracy)
    assert loss_high_noise > loss_low_noise
    # Accuracy can be highly volatile on tiny datasets, but typically degraded
    assert acc_high_noise <= acc_low_noise
