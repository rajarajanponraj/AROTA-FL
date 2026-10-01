import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from src.federated_learning.model import get_model
from src.federated_learning.partition import partition_dataset_iid, partition_dataset_non_iid
from src.federated_learning.client import FLClient
from src.federated_learning.server import FLServer

def test_get_models():
    model_mnist = get_model('mnist')
    assert isinstance(model_mnist, torch.nn.Module)
    
    model_cifar = get_model('cifar10')
    assert isinstance(model_cifar, torch.nn.Module)

def test_partitioning():
    # Mock dataset
    num_samples = 100
    images = torch.randn(num_samples, 1, 28, 28)
    labels = torch.randint(0, 10, (num_samples,))
    
    # We must attach targets attribute for the Non-IID function
    class MockDataset(TensorDataset):
        def __init__(self, *tensors):
            super().__init__(*tensors)
            self.targets = tensors[1]
            
    dataset = MockDataset(images, labels)
    
    # IID
    subsets_iid = partition_dataset_iid(dataset, num_clients=5)
    assert len(subsets_iid) == 5
    assert len(subsets_iid[0]) == 20
    
    # Non-IID
    subsets_non_iid = partition_dataset_non_iid(dataset, num_clients=5, num_classes=10, alpha=0.5)
    assert len(subsets_non_iid) == 5
    
def test_client_server_training_loop():
    # Mock dataset
    images = torch.randn(10, 1, 28, 28)
    labels = torch.randint(0, 10, (10,))
    dataset = TensorDataset(images, labels)
    
    # Initialize models
    global_model = get_model('mnist')
    server = FLServer(global_model)
    
    client = FLClient(client_id=0, dataset=dataset, batch_size=5, local_epochs=1, lr=0.01)
    
    # Capture weights before
    weights_before = [p.clone().detach() for p in server.global_model.parameters()]
    
    # Client training step
    update_vector = client.train(server.global_model)
    
    # Ensure update vector shape matches total parameters
    total_params = sum(p.numel() for p in server.global_model.parameters())
    assert len(update_vector) == total_params
    
    # Server aggregation step (single client case: aggregated_update = update_vector)
    server.update_model(update_vector)
    
    # Ensure weights have changed
    weights_after = [p.clone().detach() for p in server.global_model.parameters()]
    
    changed = False
    for p_before, p_after in zip(weights_before, weights_after):
        if not torch.allclose(p_before, p_after):
            changed = True
            break
            
    assert changed
