import random

def bounded_random(mean: float, spread: float, min_v: float = 0):
    """Gaussian random number clamped to a minimum."""
    value = random.gauss(mean, spread)
    return max(value, min_v)

def spike_probability(chance: float) -> bool:
    return random.random() < chance
