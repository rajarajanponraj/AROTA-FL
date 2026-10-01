import numpy as np
from src.channels.rayleigh import generate_rayleigh_channel

def generate_rician_channel(num_antennas, num_users=1, k_factor_linear=10.0, variance=1.0, los_angles=None):
    """
    Generate Rician fading channel coefficients.
    
    Args:
        num_antennas (int): Number of antennas/elements.
        num_users (int): Number of independent channels (e.g., K users).
        k_factor_linear (float): Rician K-factor in linear scale (ratio of LoS power to NLoS power).
        variance (float or np.ndarray): Total channel variance (beta) including LoS and NLoS.
        los_angles (np.ndarray): Optional. Angles of arrival/departure for the LoS component. 
                                 Shape should be (num_users,). If None, broadside (0) is assumed.
        
    Returns:
        np.ndarray: Complex channel matrix of shape (num_users, num_antennas).
    """
    # Generate NLoS component (Rayleigh) with normalized power (variance=1.0)
    nlos_component = generate_rayleigh_channel(num_antennas, num_users, variance=1.0)
    
    # Generate LoS component (Uniform Linear Array assumption)
    if los_angles is None:
        los_angles = np.zeros(num_users)
        
    # Standard array response vector for ULA with half-wavelength spacing
    # a(theta) = [1, exp(-j*pi*sin(theta)), ..., exp(-j*(N-1)*pi*sin(theta))]
    element_indices = np.arange(num_antennas)
    
    los_component = np.zeros((num_users, num_antennas), dtype=complex)
    for k in range(num_users):
        phase_shifts = np.pi * np.sin(los_angles[k]) * element_indices
        los_component[k, :] = np.exp(-1j * phase_shifts)
        
    # Scale components according to K-factor
    # Total power = variance
    # LoS power = K / (K + 1) * variance
    # NLoS power = 1 / (K + 1) * variance
    
    los_scaling = np.sqrt(k_factor_linear / (k_factor_linear + 1.0))
    nlos_scaling = np.sqrt(1.0 / (k_factor_linear + 1.0))
    
    variance = np.asarray(variance)
    if variance.ndim == 1:
        variance = variance[:, None]
        
    channel = np.sqrt(variance) * (los_scaling * los_component + nlos_scaling * nlos_component)
    return channel
