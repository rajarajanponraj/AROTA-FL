import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN_MNIST(nn.Module):
    """
    Simple CNN for MNIST and Fashion-MNIST (1 channel, 28x28 images).
    """
    def __init__(self, num_classes=10):
        super(SimpleCNN_MNIST, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        # 28x28 -> 14x14 -> 7x7
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class SimpleCNN_CIFAR10(nn.Module):
    """
    Simple CNN for CIFAR-10 (3 channels, 32x32 images).
    """
    def __init__(self, num_classes=10):
        super(SimpleCNN_CIFAR10, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        # 32x32 -> 16x16 -> 8x8 -> 4x4
        self.fc1 = nn.Linear(64 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 64 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def get_model(dataset_name):
    if dataset_name.lower() in ['mnist', 'fashion-mnist', 'fmnist']:
        return SimpleCNN_MNIST()
    elif dataset_name.lower() == 'cifar10':
        return SimpleCNN_CIFAR10()
    else:
        raise ValueError(f"Unknown dataset {dataset_name}")
