import numpy as np
from src.optimization.convergence_aware import optimize_convergence_aware
from src.optimization.baselines import fixed_active_ris_baseline
from src.aircomp.mse import compute_expected_mse

def test_convergence_aware_optimizer():
    num_users = 4
    num_antennas = 8
    
    # Mock parameters
    h_direct = np.zeros(num_users)
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    h_ris = np.random.randn(num_users, num_antennas) + 1j * np.random.randn(num_users, num_antennas)
    alphas = np.ones(num_users) / num_users
    P_max = 2.0
    sigma_R = 0.1
    sigma_0 = 0.05
    sigma_e = 0.2
    a_max = 5.0
    
    # Get MSE for a random configuration
    Theta_rand, b_rand, c_rand = fixed_active_ris_baseline(
        h_direct, G_H, h_ris, alphas, P_max, a_max, random_seed=42
    )
    cascaded = np.squeeze(G_H @ Theta_rand @ h_ris.T)
    h_eff_hat_rand = h_direct + cascaded
    
    J_rand = compute_expected_mse(
        h_eff_hat_rand, b_rand, c_rand, alphas, G_H, Theta_rand, sigma_R, sigma_0, sigma_e
    )
    
    # Get optimized Configuration
    Theta_opt, b_opt, c_opt, J_opt = optimize_convergence_aware(
        h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, sigma_e, a_max, num_restarts=3, random_seed=42
    )
    
    # Optimizer should find a configuration that is at least as good as the random one
    assert J_opt <= J_rand + 1e-6, f"Optimized J {J_opt} is worse than Random J {J_rand}"
    
    # Check max amplification constraint
    a_opt = np.abs(Theta_opt[0, 0])
    assert a_opt <= a_max + 1e-5
