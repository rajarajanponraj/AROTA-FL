from src.federated_learning import model
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class FLClient:
    """
    Federated Learning Client performing local training.
    """
    def __init__(self, client_id, dataset, batch_size=32, local_epochs=1, lr=0.01, device='cpu'):
        self.client_id = client_id
        self.dataset = dataset
        self.batch_size = batch_size
        self.local_epochs = local_epochs
        self.lr = lr
        self.device = device
        
        self.dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True, 
                                     num_workers=2, pin_memory=True if device == 'cuda' else False)
        self.criterion = nn.CrossEntropyLoss()
        self.model = None

    def train(self, global_model):
        """
        Train the model locally for a specified number of epochs.
        
        Args:
            global_model: The global PyTorch model (nn.Module) received from the server.
            
        Returns:
            model_update: The difference in weights (w_t - w_t_local) or the new weights.
            We will return the model parameters as a flattened 1D tensor to represent the gradient/update,
            since AirComp operates on flattened vectors (symbols).
        """
        # Reuse the model instance to avoid expensive CPU/GPU allocations every round
        if self.model is None:
            self.model = type(global_model)().to(self.device)
            
        self.model.load_state_dict(global_model.state_dict())
        self.model.train()
        
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr, momentum=0.5)
        
        for epoch in range(self.local_epochs):
            for batch_idx, (images, labels) in enumerate(self.dataloader):
                images, labels = images.to(self.device), labels.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
        # Return the pseudo-gradient (w_global - w_local) / lr or just the difference
        # Here we return the weight difference (w_local - w_global)
        # So Server does: w_new = w_global + sum(alpha_k * weight_diff_k)
        weight_diff = []
        with torch.no_grad():
            for param_global, param_local in zip(global_model.parameters(), self.model.parameters()):
                # Both params should already be on self.device
                diff = param_local.data - param_global.data
                weight_diff.append(diff.view(-1))
                
        # Flatten all parameter differences into a single 1D vector
        update_vector = torch.cat(weight_diff).cpu().numpy()
        
        return update_vector
