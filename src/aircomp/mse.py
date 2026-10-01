import numpy as np

def compute_analytical_mse(h_eff, b, c, alphas, G_H, Theta, sigma_R, sigma_0):
    """
    Compute the analytical Mean Squared Error (MSE) assuming perfect CSI.
    
    Args:
        h_eff (np.ndarray): True effective channels (num_users,)
        b (np.ndarray): Transmit scaling (num_users,)
        c (complex): Receive scaling factor
        alphas (np.ndarray): Target aggregation weights (num_users,)
        G_H (np.ndarray): AP to RIS channel, usually (1, num_antennas)
        Theta (np.ndarray): RIS reflection matrix (num_antennas, num_antennas)
        sigma_R (float): Standard deviation of active RIS noise
        sigma_0 (float): Standard deviation of AP receiver noise
        
    Returns:
        float: The calculated MSE value
    """
    h_eff = np.asarray(h_eff)
    b = np.asarray(b)
    alphas = np.asarray(alphas)
    G_H_mat = np.atleast_2d(G_H)
    if G_H_mat.shape[0] > 1 and G_H_mat.shape[1] == 1:
        G_H_mat = G_H_mat.T
        
    # Signal misalignment term: sum |c * h_eff_k * b_k - alpha_k|^2
    misalignment = np.sum(np.abs(c * h_eff * b - alphas)**2)
    
    # Active RIS noise term: |c|^2 * sigma_R^2 * ||G^H * Theta||^2
    cascaded_gain = np.linalg.norm(G_H_mat @ Theta, 'fro')**2
    ris_noise = np.abs(c)**2 * (sigma_R**2) * cascaded_gain
    
    # AP noise term: |c|^2 * sigma_0^2
    ap_noise = np.abs(c)**2 * (sigma_0**2)
    
    return misalignment + ris_noise + ap_noise

def compute_expected_mse(h_hat_eff, b, c, alphas, G_H, Theta, sigma_R, sigma_0, sigma_e):
    """
    Compute the expected MSE bounding the aggregation error under imperfect CSI.
    (This is the Convergence-Aware Objective J_t)
    
    Args:
        h_hat_eff (np.ndarray): Estimated effective channels (num_users,)
        ...
        sigma_e (float): Standard deviation of the CSI error
        
    Returns:
        float: Expected MSE value J_t
    """
    h_hat_eff = np.asarray(h_hat_eff)
    b = np.asarray(b)
    alphas = np.asarray(alphas)
    G_H_mat = np.atleast_2d(G_H)
    if G_H_mat.shape[0] > 1 and G_H_mat.shape[1] == 1:
        G_H_mat = G_H_mat.T
        
    # Signal misalignment evaluated at estimated channel
    misalignment = np.sum(np.abs(c * h_hat_eff * b - alphas)**2)
    
    cascaded_gain = np.linalg.norm(G_H_mat @ Theta, 'fro')**2
    
    # Active RIS thermal noise
    ris_noise = np.abs(c)**2 * (sigma_R**2) * cascaded_gain
    
    # CSI uncertainty penalty term
    csi_penalty = np.abs(c)**2 * cascaded_gain * (sigma_e**2) * np.sum(np.abs(b)**2)
    
    # AP noise
    ap_noise = np.abs(c)**2 * (sigma_0**2)
    
    return misalignment + ris_noise + csi_penalty + ap_noise
