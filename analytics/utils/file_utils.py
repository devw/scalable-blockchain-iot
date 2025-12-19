import pandas as pd
import os, sys, re
from pathlib import Path
from typing import List

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

def validate_input_files(files: List[Path]) -> None:
    """Validate that input files exist and are readable CSV files.
    
    Args:
        files: List of file paths to validate
        
    Raises:
        FileNotFoundError: If a file doesn't exist
        ValueError: If a path is not a file or not a CSV
    """
    for file in files:
        if not file.exists():
            raise FileNotFoundError(f"Input file not found: {file}")
        if not file.is_file():
            raise ValueError(f"Path is not a file: {file}")
        if file.suffix != '.csv':
            raise ValueError(f"File must be CSV: {file}")

def ensure_output_directory(output_path: Path) -> None:
    """Ensure output directory exists.
    
    Args:
        output_path: Output file path
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)