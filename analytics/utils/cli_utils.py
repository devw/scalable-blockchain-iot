import argparse
import os

def parse_csv_image_args(default_csv: str = None, default_output: str = None):
    """
    Parse CLI args for CSV input and output image path.
    If not provided, uses default paths.
    
    Args:
        default_csv (str, optional): default CSV path
        default_output (str, optional): default image output path

    Returns:
        Namespace: with `csv` and `output` attributes
    """
    # Determine reasonable defaults if none provided
    if default_csv is None or default_output is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        if default_csv is None:
            default_csv = os.path.join(base_dir, "data", "simulation", "simulated_api_metrics.csv")
        if default_output is None:
            default_output = os.path.join(base_dir, "data", "reports", "requests_vs_latency_heatmap.png")

    parser = argparse.ArgumentParser(
        description="Generate heatmap from CSV and save as image"
    )
    parser.add_argument(
        "--csv", "-c",
        default=default_csv,
        help=f"Path to input CSV file (default: {default_csv})"
    )
    parser.add_argument(
        "--output", "-o",
        default=default_output,
        help=f"Path to output image file (default: {default_output})"
    )
    return parser.parse_args()
