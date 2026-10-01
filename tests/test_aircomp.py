import numpy as np
import pytest
from src.aircomp.beamforming import compute_zf_scaling, apply_transmit_scaling, apply_receive_scaling
from src.aircomp.received_signal import generate_received_signal

def test_zf_scaling_no_noise():
    num_users = 5
    num_antennas = 16
    P_max = 10.0
    
    # Mock channels
    h_eff = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    alphas = np.ones(num_users) / num_users
    
    b, c = compute_zf_scaling(h_eff, alphas, P_max)
    
    # Check power constraint
    assert np.all(np.abs(b)**2 <= P_max + 1e-9)
    
    # Check perfect aggregation without noise
    s = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    s_scaled = apply_transmit_scaling(s, b)
    
    # Noiseless reception
    y_noiseless = np.sum(h_eff * s_scaled)
    s_hat = apply_receive_scaling(y_noiseless, c)
    
    s_target = np.sum(alphas * s)
    np.testing.assert_allclose(s_hat, s_target, rtol=1e-5, atol=1e-5)

def test_generate_received_signal_shapes():
    num_users = 3
    num_symbols = 100
    num_antennas = 8
    
    s = np.random.randn(num_users, num_symbols) + 1j * np.random.randn(num_users, num_symbols)
    h_eff = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    b = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    Theta = np.eye(num_antennas)
    
    sigma_R = 0.1
    sigma_0 = 0.1
    
    y = generate_received_signal(s, h_eff, b, G_H, Theta, sigma_R, sigma_0, num_antennas)
    
    assert y.shape == (num_symbols,)
    assert y.dtype == complex

def test_generate_received_signal_scalar_shape():
    num_users = 3
    num_antennas = 8
    
    s = np.random.randn(num_users) + 1j * np.random.randn(num_users) # Single symbol per user
    h_eff = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    b = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    Theta = np.eye(num_antennas)
    
    sigma_R = 0.1
    sigma_0 = 0.1
    
    y = generate_received_signal(s, h_eff, b, G_H, Theta, sigma_R, sigma_0, num_antennas)
    
    assert np.isscalar(y)
    assert isinstance(y, complex)
