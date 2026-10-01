import numpy as np

def generate_imperfect_csi(true_channel, error_variance):
    """
    Generate imperfect CSI by adding complex Gaussian noise to the true channel.
    
    Args:
        true_channel (np.ndarray): The actual channel coefficients.
        error_variance (float): The variance of the estimation error (sigma_e^2).
        
    Returns:
        np.ndarray: The estimated channel coefficients.
    """
    noise = np.sqrt(error_variance / 2.0) * (
        np.random.randn(*true_channel.shape) + 1j * np.random.randn(*true_channel.shape)
    )
    return true_channel + noise
