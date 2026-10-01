import numpy as np
from src.aircomp.mse import compute_analytical_mse, compute_expected_mse
from src.aircomp.received_signal import generate_received_signal
from src.aircomp.beamforming import apply_receive_scaling

def test_analytical_vs_empirical_mse_perfect_csi():
    np.random.seed(42)
    num_users = 4
    num_antennas = 8
    num_symbols = 50000 # High number for accurate Monte Carlo
    
    # Parameters
    sigma_R = 0.1
    sigma_0 = 0.05
    c = 1.2 + 0.3j
    
    alphas = np.ones(num_users) / num_users
    
    # Random channels and variables
    h_eff = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    b = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    Theta = np.diag(np.exp(1j * np.random.rand(num_antennas) * 2 * np.pi))
    
    # Generate symbols
    s = np.random.randn(num_users, num_symbols) + 1j * np.random.randn(num_users, num_symbols)
    # Ensure E[|s|^2] = 1 approximately or normalize
    s = s / np.sqrt(2.0)
    
    target_s = np.sum(alphas[:, None] * s, axis=0)
    
    # Generate received signals
    y = generate_received_signal(s, h_eff, b, G_H, Theta, sigma_R, sigma_0, num_antennas)
    s_hat = apply_receive_scaling(y, c)
    
    # Empirical MSE
    empirical_mse = np.mean(np.abs(s_hat - target_s)**2)
    
    # Analytical MSE
    analytical_mse = compute_analytical_mse(h_eff, b, c, alphas, G_H, Theta, sigma_R, sigma_0)
    
    assert np.isclose(empirical_mse, analytical_mse, rtol=0.05)

def test_expected_mse_imperfect_csi():
    np.random.seed(42)
    num_users = 4
    num_antennas = 8
    num_symbols = 50000
    
    sigma_R = 0.1
    sigma_0 = 0.05
    sigma_e = 0.2
    c = 1.2 + 0.3j
    alphas = np.ones(num_users) / num_users
    
    # Estimated channels
    h_hat = np.random.randn(num_users, num_antennas) + 1j * np.random.randn(num_users, num_antennas)
    G = np.random.randn(num_antennas, 1) + 1j * np.random.randn(num_antennas, 1)
    G_H = G.conj().T
    Theta = np.diag(np.exp(1j * np.random.rand(num_antennas) * 2 * np.pi))
    
    b = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    
    # Estimated effective channel
    h_hat_eff = np.squeeze(G_H @ Theta @ h_hat.T)
    
    # Generate true channels for Monte Carlo by adding error e_k
    # e_k ~ CN(0, sigma_e^2)
    
    s = (np.random.randn(num_users, num_symbols) + 1j * np.random.randn(num_users, num_symbols)) / np.sqrt(2.0)
    target_s = np.sum(alphas[:, None] * s, axis=0)
    
    # Empirical expectation over both noise and CSI errors
    # Generate independent e_k for each symbol realization to capture the expectation over CSI error properly
    e_k = np.sqrt(sigma_e**2 / 2) * (np.random.randn(num_users, num_antennas, num_symbols) + 1j * np.random.randn(num_users, num_antennas, num_symbols))
    
    # True channel = h_hat - e_k
    # True effective channel h_eff = h_hat_eff - G^H Theta e_k
    # But wait, our generate_received_signal expects a constant h_eff or we can construct it manually
    
    # Manual signal construction for varying h_eff
    # b_s = b[:, None] * s
    # h_eff (num_users, num_symbols)
    # G_H_Theta = G_H @ Theta (1, num_antennas)
    G_H_Theta = G_H @ Theta
    # G_H_Theta @ e_k is (1, num_antennas) @ (num_users, num_antennas, num_symbols) -> we need batch matmul
    # e_k is (num_users, num_antennas, num_symbols)
    # G_H_Theta is (1, num_antennas)
    e_eff = np.tensordot(G_H_Theta, e_k, axes=([1], [1])).squeeze(0) # -> (num_users, num_symbols)
    
    h_eff_true = h_hat_eff[:, None] - e_eff
    
    y_noiseless = np.sum(h_eff_true * (b[:, None] * s), axis=0)
    
    n_R = np.sqrt(sigma_R**2 / 2) * (np.random.randn(num_antennas, num_symbols) + 1j * np.random.randn(num_antennas, num_symbols))
    n_0 = np.sqrt(sigma_0**2 / 2) * (np.random.randn(num_symbols) + 1j * np.random.randn(num_symbols))
    
    cascaded_noise = G_H_Theta @ n_R
    y = y_noiseless + cascaded_noise.squeeze() + n_0
    
    s_hat = c * y
    
    empirical_expected_mse = np.mean(np.abs(s_hat - target_s)**2)
    
    analytical_expected_mse = compute_expected_mse(h_hat_eff, b, c, alphas, G_H, Theta, sigma_R, sigma_0, sigma_e)
    
    assert np.isclose(empirical_expected_mse, analytical_expected_mse, rtol=0.05)
