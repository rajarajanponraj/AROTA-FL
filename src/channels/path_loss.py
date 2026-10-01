import numpy as np

def compute_path_loss(distance, path_loss_exponent=2.0, reference_distance=1.0, reference_path_loss_db=30.0):
    """
    Compute the distance-dependent path loss in dB and linear variance (beta).
    
    Args:
        distance (float or np.ndarray): Distance between transmitter and receiver (meters)
        path_loss_exponent (float): Path loss exponent (alpha). Default is 2.0 (free space).
        reference_distance (float): Reference distance d0 in meters. Default is 1.0m.
        reference_path_loss_db (float): Path loss at the reference distance in dB. Default is 30 dB.
        
    Returns:
        tuple: (path_loss_db, beta)
            - path_loss_db: Path loss in dB
            - beta: Channel variance in linear scale (10^(-PL/10))
    """
    distance = np.maximum(distance, reference_distance) # Prevent unrealistic distances
    path_loss_db = reference_path_loss_db + 10 * path_loss_exponent * np.log10(distance / reference_distance)
    beta = 10 ** (-path_loss_db / 10)
    return path_loss_db, beta
