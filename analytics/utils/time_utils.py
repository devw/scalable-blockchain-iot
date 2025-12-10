from datetime import datetime, timedelta

def generate_time_series(start: datetime, minutes: int):
    """Yield timestamps minute by minute."""
    for delta in range(minutes):
        yield start + timedelta(minutes=delta)
