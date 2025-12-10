import random
from dataclasses import dataclass

@dataclass
class SimulationConfig:
    duration_minutes: int = 60
    base_rps: int = 50
    spike_chance: float = 0.05
    latency_base_ms: int = 80
    latency_jitter_ms: int = 40
    seed: int = 42

def load_config() -> SimulationConfig:
    cfg = SimulationConfig()
    random.seed(cfg.seed)
    return cfg
