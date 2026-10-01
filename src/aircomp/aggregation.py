import numpy as np
from src.aircomp.received_signal import generate_received_signal
from src.aircomp.beamforming import apply_receive_scaling

def aggregate_updates_aircomp(client_updates, h_eff, b, c, G_H, Theta, sigma_R, sigma_0):
    """
    Simulate the over-the-air aggregation of FL client updates.
    
    Args:
        client_updates (list of np.ndarray): List of 1D numpy arrays representing client model updates.
        h_eff (np.ndarray): Effective channel (num_users,)
        b (np.ndarray): Transmit scaling factors (num_users,)
        c (complex): Receive scaling factor
        G_H (np.ndarray): RIS to AP channel
        Theta (np.ndarray): Active RIS reflection matrix
        sigma_R (float): Active RIS thermal noise
        sigma_0 (float): AP noise
        
    Returns:
        np.ndarray: The noisy aggregated update vector (real-valued).
    """
    num_users = len(client_updates)
    num_antennas = Theta.shape[0]
    
    # Stack updates into shape (num_users, num_symbols)
    # We transmit them as the real part of complex symbols
    s = np.stack(client_updates, axis=0).astype(complex)
    
    # Generate noisy received signal through the AirComp channel
    y = generate_received_signal(s, h_eff, b, G_H, Theta, sigma_R, sigma_0, num_antennas)
    
    # Apply receiver scaling
    s_hat = apply_receive_scaling(y, c)
    
    # Since original updates were real, we take the real part of the received scaled signal
    aggregated_update = np.real(s_hat)
    
    return aggregated_update
