from datetime import datetime
from .data_generator import generate_minute_data
from ..utils.time_utils import generate_time_series

def run_simulation(cfg):
    """Simulate data and return list of rows."""
    rows = []
    start = datetime.utcnow()
    for ts in generate_time_series(start, cfg.duration_minutes):
        row = generate_minute_data()
        rows.append(row)
    return rows
