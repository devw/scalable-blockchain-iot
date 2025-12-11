import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """Loads a CSV file and returns a pandas DataFrame."""
    return pd.read_csv(path)