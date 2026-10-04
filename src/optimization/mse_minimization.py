import numpy as np
from scipy.optimize import minimize
from src.aircomp.beamforming import compute_zf_scaling
from src.aircomp.mse import compute_analytical_mse

def optimize_mse_baseline(h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, a_max, P_RIS_max=2.0, num_restarts=3, random_seed=None):
    """
    Naively optimize the instantaneous MSE by finding the best (a, Theta) 
    using a numerical optimizer, assuming perfect/estimated CSI.
    
    Args:
        h_direct (np.ndarray): Direct channels
        G_H (np.ndarray): RIS to AP channel
        h_ris (np.ndarray): Users to RIS channel
        alphas (np.ndarray): Aggregation weights
        P_max (float): Max transmit power per user
        sigma_R (float): Active RIS noise std dev
        sigma_0 (float): AP noise std dev
        a_max (float): Maximum amplification factor
        num_restarts (int): Number of random initializations to avoid local minima
        random_seed (int): Random seed for initializations
        
    Returns:
        tuple: (best_Theta, best_b, best_c, best_mse)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        
    num_antennas = h_ris.shape[1]
    
    # Cost function for scipy.minimize
    def cost_fn(x):
        a = x[0]
        phases = x[1:]
        Theta = a * np.diag(np.exp(1j * phases))
        
        cascaded = np.squeeze(G_H @ Theta @ h_ris.T)
        h_eff = h_direct + cascaded if h_direct is not None else cascaded
        
        # Guard against zero effective channel
        h_eff_abs = np.maximum(np.abs(h_eff), 1e-12)
        
        c = np.max(alphas / (np.sqrt(P_max) * h_eff_abs))
        
        # Calculate MSE
        cascaded_gain = np.linalg.norm(G_H @ Theta, 'fro')**2
        mse = (c**2) * (sigma_R**2 * cascaded_gain + sigma_0**2)
        return mse
        
    def ris_power_constraint(x):
        a = x[0]
        incident_power = np.sum(P_max * np.abs(h_ris)**2) 
        output_power = (a**2) * incident_power + (a**2) * num_antennas * (sigma_R**2)
        return P_RIS_max - output_power

    bounds = [(1.0, a_max)] + [(0, 2*np.pi)] * num_antennas
    constraints = [{'type': 'ineq', 'fun': ris_power_constraint}]
    
    best_mse = float('inf')
    best_x = None
    
    for _ in range(num_restarts):
        # Random initialization
        x0 = np.zeros(1 + num_antennas)
        x0[0] = np.random.uniform(1.0, a_max)
        x0[1:] = np.random.uniform(0, 2*np.pi, num_antennas)
        
        res = minimize(cost_fn, x0, bounds=bounds, constraints=constraints, method='SLSQP')
        
        if res.fun < best_mse:
            best_mse = res.fun
            best_x = res.x
            
    # Reconstruct the best configuration
    a_opt = best_x[0]
    phases_opt = best_x[1:]
    Theta_opt = a_opt * np.diag(np.exp(1j * phases_opt))
    
    cascaded = np.squeeze(G_H @ Theta_opt @ h_ris.T)
    h_eff = h_direct + cascaded if h_direct is not None else cascaded
    
    b_opt, c_opt = compute_zf_scaling(h_eff, alphas, P_max)
    
    return Theta_opt, b_opt, c_opt, best_mse
