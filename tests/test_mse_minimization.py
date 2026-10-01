import numpy as np
from src.optimization.mse_minimization import optimize_mse_baseline
from src.optimization.baselines import fixed_active_ris_baseline
from src.aircomp.mse import compute_analytical_mse

def test_mse_minimization_vs_random():
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
    a_max = 5.0
    
    # Get MSE for a random Fixed Active RIS configuration
    Theta_rand, b_rand, c_rand = fixed_active_ris_baseline(
        h_direct, G_H, h_ris, alphas, P_max, a_max, random_seed=42
    )
    cascaded = np.squeeze(G_H @ Theta_rand @ h_ris.T)
    h_eff_rand = h_direct + cascaded
    mse_rand = compute_analytical_mse(h_eff_rand, b_rand, c_rand, alphas, G_H, Theta_rand, sigma_R, sigma_0)
    
    # Get optimized MSE
    Theta_opt, b_opt, c_opt, mse_opt = optimize_mse_baseline(
        h_direct, G_H, h_ris, alphas, P_max, sigma_R, sigma_0, a_max, num_restarts=5, random_seed=42
    )
    
    # Optimizer should find a configuration that is AT LEAST as good as the random one, 
    # and realistically much better.
    assert mse_opt <= mse_rand + 1e-6, f"Optimized MSE {mse_opt} is worse than Random MSE {mse_rand}"
    
    # Also verify that the configuration satisfies a <= a_max
    a_opt = np.abs(Theta_opt[0, 0])
    assert a_opt <= a_max + 1e-5
