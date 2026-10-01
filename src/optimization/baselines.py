import numpy as np
from src.aircomp.beamforming import compute_zf_scaling

def no_ris_baseline(h_direct, alphas, P_max):
    """
    Baseline with No RIS (Theta = 0). Only the direct channel is used.
    
    Args:
        h_direct (np.ndarray): Direct channels (num_users,)
        alphas (np.ndarray): Target aggregation weights
        P_max (float): Maximum transmit power constraint per user
    """
    b, c = compute_zf_scaling(h_direct, alphas, P_max)
    return None, b, c  # Theta is None (or 0)

def passive_ris_baseline(h_direct, G_H, h_ris, alphas, P_max, random_seed=None):
    """
    Baseline with Passive RIS (amplification = 1.0). Random phases.
    
    Args:
        h_direct (np.ndarray): Direct channels (num_users,) - can be zeros if blocked
        G_H (np.ndarray): RIS to AP channel (1, num_antennas)
        h_ris (np.ndarray): User to RIS channels (num_users, num_antennas)
        alphas (np.ndarray): Target aggregation weights
        P_max (float): Maximum transmit power per user
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        
    num_antennas = h_ris.shape[1]
    phases = np.random.uniform(0, 2 * np.pi, num_antennas)
    Theta = np.diag(np.exp(1j * phases))
    
    # Effective channel: h_direct + G^H @ Theta @ h_ris
    cascaded = np.squeeze(G_H @ Theta @ h_ris.T)
    h_eff = h_direct + cascaded if h_direct is not None else cascaded
    
    b, c = compute_zf_scaling(h_eff, alphas, P_max)
    return Theta, b, c

def fixed_active_ris_baseline(h_direct, G_H, h_ris, alphas, P_max, a_max, random_seed=None):
    """
    Baseline with Fixed Active RIS (amplification = a_max). Random phases.
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        
    num_antennas = h_ris.shape[1]
    phases = np.random.uniform(0, 2 * np.pi, num_antennas)
    Theta = a_max * np.diag(np.exp(1j * phases))
    
    cascaded = np.squeeze(G_H @ Theta @ h_ris.T)
    h_eff = h_direct + cascaded if h_direct is not None else cascaded
    
    b, c = compute_zf_scaling(h_eff, alphas, P_max)
    return Theta, b, c

def evaluate_total_power(b, Theta, P_dc_active=0.0):
    """
    Evaluate total power consumption of the system for fair comparisons.
    P_total = P_tx + P_RIS
    P_tx = sum(|b_k|^2)
    P_RIS = Tr(Theta^H Theta) * P_dc_active (Simplified Active RIS power model)
    """
    P_tx = np.sum(np.abs(b)**2)
    if Theta is None:
        return P_tx
    P_ris = np.linalg.norm(Theta, 'fro')**2 * P_dc_active
    return P_tx + P_ris
