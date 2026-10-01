import numpy as np

def generate_received_signal(s, h_eff, b, G_H, Theta, sigma_R, sigma_0, num_antennas):
    """
    Generate the received AirComp signal at the AP with Active RIS noise and AP noise.
    
    Args:
        s (np.ndarray): Transmitted symbols (num_users, num_symbols) or (num_users,)
        h_eff (np.ndarray): Effective channels (num_users,)
        b (np.ndarray): Transmit scaling (num_users,)
        G_H (np.ndarray): AP to RIS channel, usually (1, num_antennas) or (num_antennas,)
        Theta (np.ndarray): RIS reflection matrix (num_antennas, num_antennas)
        sigma_R (float): Standard deviation of active RIS noise
        sigma_0 (float): Standard deviation of AP receiver noise
        num_antennas (int): Number of RIS elements
        
    Returns:
        np.ndarray: Received signal (num_symbols,) or scalar
    """
    s = np.asarray(s)
    num_users = s.shape[0]
    num_symbols = s.shape[1] if s.ndim > 1 else 1
    
    # Received signal without noise
    b = np.asarray(b)
    s_scaled = s * b[:, None] if s.ndim > 1 else s * b
    y_noiseless = np.sum(h_eff[:, None] * s_scaled if s.ndim > 1 else h_eff * s_scaled, axis=0)
    
    # Active RIS noise: n_R ~ CN(0, sigma_R^2 I_N)
    n_R = np.sqrt(sigma_R**2 / 2) * (np.random.randn(num_antennas, num_symbols) + 1j * np.random.randn(num_antennas, num_symbols))
    
    # AP noise: n_0 ~ CN(0, sigma_0^2)
    n_0 = np.sqrt(sigma_0**2 / 2) * (np.random.randn(num_symbols) + 1j * np.random.randn(num_symbols))
    
    # Ensure G_H is 2D for matrix multiplication
    G_H_mat = np.atleast_2d(G_H)
    if G_H_mat.shape[0] > 1 and G_H_mat.shape[1] == 1: # if column vector, transpose it
        G_H_mat = G_H_mat.T
        
    # Cascaded noise: G^H @ Theta @ n_R
    cascaded_noise = G_H_mat @ Theta @ n_R
    
    # Combine everything
    y = y_noiseless + cascaded_noise.squeeze() + n_0.squeeze()
    
    # If single symbol, return scalar
    if s.ndim == 1 and y.size == 1:
        return y.item()
    return y
