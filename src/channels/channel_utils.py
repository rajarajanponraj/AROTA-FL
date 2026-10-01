import numpy as np

def compute_channel_gain(channel):
    """
    Compute the squared magnitude (power gain) of the channel.
    """
    return np.abs(channel)**2
