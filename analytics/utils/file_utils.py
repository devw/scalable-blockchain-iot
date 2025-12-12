import pandas as pd
import os, sys, re

def load_csv(path: str) -> pd.DataFrame:
    """Loads a CSV file and returns a pandas DataFrame."""
    return pd.read_csv(path)

def build_output_filename(output_dir: str, csv_path: str, prefix: str = None) -> str:
    if prefix is None:
        script_name = os.path.basename(sys.argv[0])  # e.g., generate_pods_over_time.py
        prefix = os.path.splitext(script_name)[0]    # remove .py -> generate_pods_over_time
    base = os.path.basename(csv_path).replace(".csv", "")
    filename = f"{prefix}_{base}.png"
    return os.path.join(output_dir, filename)

def extract_metadata(filename: str, keys=("maxpods", "duration")) -> dict:
    base = os.path.basename(filename)
    return {
        key: match.group(1)
        for key in keys
        if (match := re.search(rf"{key}=(\d+)", base))
    }