def correlate_latency(requests_in_flight: int, base_latency: int) -> float:
    """
    Stronger correlation:
    latency grows non-linearly as load increases.
    """
    load_factor = 1 + (requests_in_flight / 200)**2
    return base_latency * load_factor
