import numpy as np
from src.channels.rayleigh import generate_rayleigh_channel
from src.channels.channel_estimation import generate_imperfect_csi
from src.channels.channel_utils import compute_channel_gain
from src.channels.path_loss import compute_path_loss
from src.channels.rician import generate_rician_channel

def test_rayleigh_channel_statistics():
    np.random.seed(42)
    variance = 2.0
    h = generate_rayleigh_channel(num_antennas=10000, num_users=1, variance=variance)
    
    # Assert correct shape
    assert h.shape == (1, 10000)
    
    # Assert variance is close to specified
    empirical_variance = np.var(h)
    assert np.isclose(empirical_variance, variance, rtol=0.05)

def test_imperfect_csi_error_variance():
    np.random.seed(42)
    true_channel = np.ones((1, 10000)) + 1j * np.ones((1, 10000))
    error_variance = 0.5
    
    est_channel = generate_imperfect_csi(true_channel, error_variance)
    error = est_channel - true_channel
    
    # Check if error variance matches the CSI uncertainty
    empirical_variance = np.var(error)
    assert np.isclose(empirical_variance, error_variance, rtol=0.05)

def test_path_loss():
    # Distance = 10m, reference = 1m, exponent = 2.0, ref_loss = 30 dB
    # PL = 30 + 10 * 2.0 * log10(10) = 30 + 20 = 50 dB
    pl_db, beta = compute_path_loss(10.0, path_loss_exponent=2.0, reference_distance=1.0, reference_path_loss_db=30.0)
    assert np.isclose(pl_db, 50.0)
    assert np.isclose(beta, 10**(-5.0))

def test_rician_channel_statistics():
    np.random.seed(42)
    # K-factor = 10, total variance = 2.0
    h = generate_rician_channel(num_antennas=10000, num_users=1, k_factor_linear=10.0, variance=2.0)
    
    assert h.shape == (1, 10000)
    empirical_variance = np.var(h)
    
    # In Rician, the variance of the zero-mean part is 1/(K+1) of total power. 
    # The mean is not zero, so the total power (mean^2 + variance) should be approx 2.0
    total_power = np.mean(np.abs(h)**2)
    assert np.isclose(total_power, 2.0, rtol=0.05)
