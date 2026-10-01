import numpy as np
from src.optimization.baselines import no_ris_baseline, passive_ris_baseline, fixed_active_ris_baseline, evaluate_total_power

def test_no_ris_baseline():
    num_users = 4
    h_direct = np.random.randn(num_users) + 1j * np.random.randn(num_users)
    alphas = np.ones(num_users) / num_users
    P_max = 5.0
    
    Theta, b, c = no_ris_baseline(h_direct, alphas, P_max)
    
    assert Theta is None
    assert np.all(np.abs(b)**2 <= P_max + 1e-9)
    # Check ZF property
    assert np.allclose(c * h_direct * b, alphas)

def test_passive_ris_baseline():
    num_users = 4
    num_antennas = 16
    h_direct = np.zeros(num_users) # Blocked direct link
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    h_ris = np.random.randn(num_users, num_antennas) + 1j * np.random.randn(num_users, num_antennas)
    alphas = np.ones(num_users) / num_users
    P_max = 5.0
    
    Theta, b, c = passive_ris_baseline(h_direct, G_H, h_ris, alphas, P_max, random_seed=42)
    
    # Check Passive RIS property: |a_n| = 1
    diag = np.diag(Theta)
    assert np.allclose(np.abs(diag), 1.0)
    
    # Check power constraints
    assert np.all(np.abs(b)**2 <= P_max + 1e-9)
    
def test_fixed_active_ris_baseline():
    num_users = 4
    num_antennas = 16
    h_direct = np.zeros(num_users)
    G_H = np.random.randn(1, num_antennas) + 1j * np.random.randn(1, num_antennas)
    h_ris = np.random.randn(num_users, num_antennas) + 1j * np.random.randn(num_users, num_antennas)
    alphas = np.ones(num_users) / num_users
    P_max = 5.0
    a_max = 3.0
    
    Theta, b, c = fixed_active_ris_baseline(h_direct, G_H, h_ris, alphas, P_max, a_max, random_seed=42)
    
    # Check Active RIS property: |a_n| = a_max
    diag = np.diag(Theta)
    assert np.allclose(np.abs(diag), a_max)
    
    # Check power constraints
    assert np.all(np.abs(b)**2 <= P_max + 1e-9)
    
def test_evaluate_total_power():
    b = np.array([1.0, 1.0j]) # P_tx = 2.0
    Theta = 2.0 * np.eye(2) # ||Theta||_F^2 = 4 + 4 = 8
    
    # P_dc = 0.5
    # Total power = 2.0 + 8 * 0.5 = 6.0
    P_total = evaluate_total_power(b, Theta, P_dc_active=0.5)
    assert np.isclose(P_total, 6.0)
