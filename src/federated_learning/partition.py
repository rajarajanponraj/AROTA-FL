import numpy as np
from torch.utils.data import Subset

def partition_dataset_iid(dataset, num_clients):
    """
    Partition the dataset into `num_clients` identical and independent (IID) subsets.
    
    Args:
        dataset: PyTorch Dataset
        num_clients: Number of subsets to create
        
    Returns:
        List of Subsets
    """
    num_items = int(len(dataset) / num_clients)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    
    for i in range(num_clients):
        dict_users[i] = set(np.random.choice(all_idxs, num_items, replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
        
    return [Subset(dataset, list(dict_users[i])) for i in range(num_clients)]

def partition_dataset_non_iid(dataset, num_clients, num_classes=10, alpha=0.5):
    """
    Partition dataset in a non-IID manner using Dirichlet distribution.
    
    Args:
        dataset: PyTorch Dataset (must have .targets attribute or similar)
        num_clients: Number of clients
        num_classes: Number of labels
        alpha: Dirichlet parameter. Smaller alpha -> higher non-IID (more label imbalance).
        
    Returns:
        List of Subsets
    """
    try:
        # For torchvision datasets, targets might be a list or tensor
        targets = np.array(dataset.targets)
    except AttributeError:
        # Fallback if targets are not easily accessible (e.g., custom dataset)
        targets = np.array([y for _, y in dataset])
        
    min_size = 0
    min_require_size = 10
    
    N = len(targets)
    dict_users = {i: [] for i in range(num_clients)}
    
    while min_size < min_require_size:
        idx_batch = [[] for _ in range(num_clients)]
        for k in range(num_classes):
            idx_k = np.where(targets == k)[0]
            np.random.shuffle(idx_k)
            proportions = np.random.dirichlet(np.repeat(alpha, num_clients))
            
            # Balance
            proportions = np.array([p * (len(idx_j) < N / num_clients) for p, idx_j in zip(proportions, idx_batch)])
            proportions = proportions / proportions.sum()
            proportions = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]
            
            idx_batch = [idx_j + idx.tolist() for idx_j, idx in zip(idx_batch, np.split(idx_k, proportions))]
            
        min_size = min([len(idx_j) for idx_j in idx_batch])
        
    for j in range(num_clients):
        np.random.shuffle(idx_batch[j])
        dict_users[j] = idx_batch[j]
        
    return [Subset(dataset, dict_users[i]) for i in range(num_clients)]
