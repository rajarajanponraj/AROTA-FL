import numpy as np

class ActiveRIS:
    """
    Model for an Active Reconfigurable Intelligent Surface.
    Can dynamically amplify and phase-shift incident signals,
    introducing active thermal noise in the process.
    """
    def __init__(self, num_elements, max_amplification=3.0, noise_variance=0.01):
        self.num_elements = num_elements
        self.max_amplification = max_amplification
        self.noise_variance = noise_variance
        
        self.amplification = 1.0
        self.phases = np.zeros(num_elements)

    def set_amplification(self, a):
        """Set a uniform amplification factor for all elements."""
        if a < 0 or a > self.max_amplification:
            raise ValueError(f"Amplification {a} out of bounds [0, {self.max_amplification}]")
        self.amplification = a

    def set_phases(self, phases):
        """Set the phase shifts for each element."""
        if len(phases) != self.num_elements:
            raise ValueError("Phase array length must match number of RIS elements")
        self.phases = np.asarray(phases)

    def get_reflection_matrix(self):
        """Returns the diagonal Theta matrix."""
        return self.amplification * np.diag(np.exp(1j * self.phases))

    def generate_thermal_noise(self):
        """
        Generates thermal noise introduced by the active RIS components.
        Returns array of shape (num_elements, )
        """
        return np.sqrt(self.noise_variance / 2.0) * (
            np.random.randn(self.num_elements) + 1j * np.random.randn(self.num_elements)
        )
