from datetime import datetime


def log_info(message: str):
    """Simple logger that prints timestamps and messages."""
    timestamp = datetime.now().isoformat()
    print(f"[INFO] {timestamp} - {message}")