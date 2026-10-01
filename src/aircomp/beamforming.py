import numpy as np

def compute_zf_scaling(h_eff, alphas, P_max):
    """
    Compute Zero-Forcing transmit scaling (b_k) and receive scaling (c).
    
    Args:
        h_eff (np.ndarray): Effective channels (num_users,)
        alphas (np.ndarray): Aggregation weights (num_users,)
        P_max (float or np.ndarray): Maximum transmit power per user
        
    Returns:
        tuple: (b, c) where b is the transmit scaling array and c is the receive scalar
    """
    h_eff = np.asarray(h_eff)
    alphas = np.asarray(alphas)
    
    # |c| >= alpha_k / (sqrt(P_max) * |h_eff_k|) for all k
    c_mag = np.max(alphas / (np.sqrt(P_max) * np.abs(h_eff)))
    c = c_mag  # Can just be real
    
    b = alphas / (c * h_eff)
    return b, c

def apply_transmit_scaling(s, b):
    """
    Apply transmit scaling to symbols.
    
    Args:
        s (np.ndarray): Symbols of shape (num_users, num_symbols) or (num_users,)
        b (np.ndarray): Transmit scaling factors (num_users,)
        
    Returns:
        np.ndarray: Scaled symbols
    """
    b = np.asarray(b)
    if s.ndim == 2:
        return s * b[:, None]
    return s * b

def apply_receive_scaling(y, c):
    """
    Apply receive scaling factor to the received signal.
    
    Args:
        y (np.ndarray): Received signal
        c (complex): Receive scaling factor
        
    Returns:
        np.ndarray: Estimated aggregated symbols
    """
    return c * y
