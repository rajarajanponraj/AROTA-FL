import numpy as np

def compute_active_ris_power(amplification, num_elements, incident_power_sum, noise_variance):
    """
    Compute power emitted by the active RIS.
    P_RIS = a^2 * (incident_power_sum + num_elements * noise_variance)
    """
    return (amplification**2) * (incident_power_sum + num_elements * noise_variance)
