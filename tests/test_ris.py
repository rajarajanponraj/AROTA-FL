import numpy as np
from src.ris.active_ris import ActiveRIS
from src.ris.passive_ris import PassiveRIS
from src.ris.phase_control import align_phases_to_target, quantize_phases

def test_active_ris():
    ris = ActiveRIS(num_elements=16, max_amplification=3.0, noise_variance=0.1)
    ris.set_amplification(2.0)
    ris.set_phases(np.zeros(16))
    theta = ris.get_reflection_matrix()
    
    assert theta.shape == (16, 16)
    assert np.isclose(np.abs(theta[0, 0]), 2.0)
    
    np.random.seed(42)
    noise = ris.generate_thermal_noise()
    assert noise.shape == (16,)
    
    # Test bounds
    try:
        ris.set_amplification(4.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_passive_ris():
    ris = PassiveRIS(num_elements=16)
    ris.set_phases(np.zeros(16))
    theta = ris.get_reflection_matrix()
    
    assert np.isclose(np.abs(theta[0, 0]), 1.0)
    
    # Setting amplification other than 1.0 should raise ValueError
    try:
        ris.set_amplification(2.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
        
    noise = ris.generate_thermal_noise()
    assert np.all(noise == 0)

def test_phase_alignment():
    h = np.array([1j, -1, -1j, 1])
    G = np.array([1, 1, 1, 1])
    phases = align_phases_to_target(h, G)
    
    # Expected: arg(h) + arg(G) + phase = 0 => phase = -arg(h) - arg(G)
    # arg(1j) = pi/2 -> phase = -pi/2
    assert np.isclose(phases[0], -np.pi/2)
    assert np.isclose(phases[1], -np.pi)
    assert np.isclose(phases[2], np.pi/2)
    assert np.isclose(phases[3], 0)

def test_phase_quantization():
    phases = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
    quantized = quantize_phases(phases, num_levels=4)
    # Levels are 0, pi/2, pi, 3pi/2
    expected = np.array([0, np.pi/2, np.pi/2, np.pi, np.pi])
    
    assert np.allclose(quantized, expected % (2*np.pi))
