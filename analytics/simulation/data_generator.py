from datetime import datetime
from .correlations import correlate_latency
from ..utils.random_utils import bounded_random, spike_probability
from .config import load_config

def generate_minute_data():
    cfg = load_config()
    base = cfg.base_rps

    # traffic spike?
    if spike_probability(cfg.spike_chance):
        base *= 4

    rps = int(bounded_random(base, base * 0.2, min_v=1))
    requests_in_flight = int(rps * bounded_random(1.2, 0.1))

    latency = correlate_latency(
        requests_in_flight,
        bounded_random(cfg.latency_base_ms, cfg.latency_jitter_ms)
    )

    # naive autoscaling
    pod_count = max(1, requests_in_flight // 200)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "rps": rps,
        "requests_in_flight": requests_in_flight,
        "latency_ms": round(latency, 2),
        "pod_count": pod_count,
    }
