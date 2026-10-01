import torch
import torch.nn as nn
import numpy as np

class FLServer:
    """
    Federated Learning Server handling global model updates.
    """
    def __init__(self, model, device='cpu'):
        self.global_model = model
        self.device = device
        self.global_model.to(self.device)
        
        # Store original shapes of parameters to reconstruct the model from a flattened vector
        self.param_shapes = [p.shape for p in self.global_model.parameters()]
        self.param_numel = [p.numel() for p in self.global_model.parameters()]
        
    def update_model(self, aggregated_update_vector):
        """
        Update the global model using the aggregated flattened update vector.
        w_new = w_global + aggregated_update
        
        Args:
            aggregated_update_vector (np.ndarray): The 1D vector representing the aggregated updates
            from the AirComp channel (after receiving and scaling).
        """
        # Convert numpy array to torch tensor
        aggregated_update = torch.tensor(aggregated_update_vector, dtype=torch.float32, device=self.device)
        
        pointer = 0
        with torch.no_grad():
            for param, shape, numel in zip(self.global_model.parameters(), self.param_shapes, self.param_numel):
                # Extract the corresponding slice for this parameter
                param_update = aggregated_update[pointer:pointer + numel].view(shape)
                
                # Apply the update
                param.data += param_update
                
                pointer += numel
                
    def evaluate(self, test_loader):
        """
        Evaluate the global model on the test dataset.
        
        Args:
            test_loader: DataLoader for the test dataset
            
        Returns:
            tuple: (accuracy, loss)
        """
        self.global_model.eval()
        test_loss = 0
        correct = 0
        criterion = nn.CrossEntropyLoss(reduction='sum')
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.global_model(data)
                
                test_loss += criterion(output, target).item()
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                
        test_loss /= len(test_loader.dataset)
        accuracy = 100. * correct / len(test_loader.dataset)
        
        return accuracy, test_loss
