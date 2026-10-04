import numpy as np
from scipy.optimize import minimize
from src.aircomp.beamforming import compute_zf_scaling
from src.aircomp.mse import compute_expected_mse

def optimize_convergence_aware(h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, P_RIS_max=2.0, num_restarts=3, random_seed=None):
    """
    Optimize the Convergence-Aware expected-MSE objective (J_t) which dynamically
    backs off extreme active RIS amplification when CSI errors are severe.
    
    Args:
        h_direct (np.ndarray): Estimated direct channels
        G_H (np.ndarray): Estimated RIS to AP channel
        h_ris (np.ndarray): Estimated Users to RIS channel
        alphas (np.ndarray): Aggregation weights
        P_max (float): Max transmit power per user
        sigma_R (float): Active RIS noise std dev
        sigma_0 (float): AP noise std dev
        sigma_e (float): CSI error standard deviation
        a_max (float): Maximum amplification factor
        num_restarts (int): Number of random initializations
        random_seed (int): Random seed
        
    Returns:
        tuple: (best_Theta, best_b, best_c, best_J)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        
    num_antennas = h_ris.shape[1]
    
    # Cost function for scipy.minimize representing the convergence-aware objective
    def cost_fn(x):
        a = x[0]
        phases = x[1:]
        Theta = a * np.diag(np.exp(1j * phases))
        
        cascaded = np.squeeze(G_H @ Theta @ h_ris.T)
        h_eff_hat = h_direct + cascaded if h_direct is not None else cascaded
        
        # Guard against zero effective channel
        h_eff_abs = np.maximum(np.abs(h_eff_hat), 1e-12)
        
        c = np.max(alphas / (np.sqrt(P_max) * h_eff_abs))
        b = alphas / (c * h_eff_hat)
        
        # Calculate Expected MSE (J_t)
        cascaded_gain = np.linalg.norm(G_H @ Theta, 'fro')**2
        
        ris_noise = (c**2) * (sigma_R**2) * cascaded_gain
        ap_noise = (c**2) * (sigma_0**2)
        
        # The penalty term strictly deriving from CSI errors magnifying FL aggregation error
        csi_penalty = (c**2) * cascaded_gain * (sigma_e**2) * np.sum(np.abs(b)**2)
        
        # Explicit FL Convergence Bound (Learning Progress Objective)
        # E[F(w_{t+1})] <= F(w_t) - eta * ||grad||^2 + (L * eta^2 / 2) * E[||noise_t||^2]
        FL_learning_rate = 0.01
        FL_smoothness_L = 10.0
        
        expected_aggregation_mse = ris_noise + ap_noise + csi_penalty
        fl_convergence_bound = (FL_smoothness_L / 2) * (FL_learning_rate ** 2) * expected_aggregation_mse
        
        return fl_convergence_bound
        
    def ris_power_constraint(x):
        a = x[0]
        # Active RIS Output Power Constraint:
        # P_out = E[|| Theta(G h s + n_R) ||^2] <= P_RIS_max
        # Approximation based on total incident power from clients
        incident_power = np.sum(P_max * np.abs(h_ris)**2) 
        output_power = (a**2) * incident_power + (a**2) * num_antennas * (sigma_R**2)
        return P_RIS_max - output_power

    bounds = [(1.0, a_max)] + [(0, 2*np.pi)] * num_antennas
    constraints = [{'type': 'ineq', 'fun': ris_power_constraint}]
    
    best_J = float('inf')
    best_x = None
    
    for _ in range(num_restarts):
        x0 = np.zeros(1 + num_antennas)
        x0[0] = np.random.uniform(1.0, a_max)
        x0[1:] = np.random.uniform(0, 2*np.pi, num_antennas)
        
        res = minimize(cost_fn, x0, bounds=bounds, constraints=constraints, method='SLSQP')
        
        if res.fun < best_J:
            best_J = res.fun
            best_x = res.x
            
    # Reconstruct the optimal configuration
    a_opt = best_x[0]
    phases_opt = best_x[1:]
    Theta_opt = a_opt * np.diag(np.exp(1j * phases_opt))
    
    cascaded = np.squeeze(G_H @ Theta_opt @ h_ris.T)
    h_eff_hat = h_direct + cascaded if h_direct is not None else cascaded
    
    b_opt, c_opt = compute_zf_scaling(h_eff_hat, alphas, P_max)
    
    return Theta_opt, b_opt, c_opt, best_J
