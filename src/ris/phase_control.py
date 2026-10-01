import numpy as np

def align_phases_to_target(channel_to_ris, channel_from_ris):
    """
    A simple baseline to align RIS phases to maximize the combined channel gain.
    Target phase is aligned to 0 radians.
    theta_n = - (arg(h_n) + arg(G_n))
    """
    combined_phase = np.angle(channel_to_ris) + np.angle(channel_from_ris)
    return -combined_phase

def quantize_phases(phases, num_levels):
    """
    Quantize continuous phases into discrete levels.
    """
    step = 2 * np.pi / num_levels
    quantized = np.floor(phases / step + 0.5) * step
    return quantized % (2 * np.pi)
