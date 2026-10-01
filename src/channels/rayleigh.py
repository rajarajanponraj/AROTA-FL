import numpy as np

def generate_rayleigh_channel(num_antennas, num_users=1, variance=1.0):
    """
    Generate Rayleigh fading channel coefficients.
    
    Args:
        num_antennas (int): Number of antennas/elements.
        num_users (int): Number of independent channels (e.g., K users).
        variance (float): The variance of the complex channel (beta).
        
    Returns:
        np.ndarray: Complex channel matrix of shape (num_users, num_antennas).
    """
    return np.sqrt(variance / 2.0) * (
        np.random.randn(num_users, num_antennas) + 1j * np.random.randn(num_users, num_antennas)
    )
