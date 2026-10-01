import numpy as np
from src.ris.active_ris import ActiveRIS

class PassiveRIS(ActiveRIS):
    """
    Model for a standard Passive RIS.
    Can only phase-shift incident signals. Amplification is fixed to 1.0,
    and no active thermal noise is introduced.
    """
    def __init__(self, num_elements):
        # Passive RIS has max amplification 1.0 and no active thermal noise
        super().__init__(num_elements, max_amplification=1.0, noise_variance=0.0)
        self.amplification = 1.0

    def set_amplification(self, a):
        if a != 1.0:
            raise ValueError("Passive RIS must have amplification exactly 1.0")
