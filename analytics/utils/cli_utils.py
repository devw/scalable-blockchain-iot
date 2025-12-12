import argparse
import os

DEFAULT_OUTPUT_DIR = "/tmp/"  # 📂 default output folder

def parse_csv_image_args(default_csv: str = None, compression_level: int = 65):
    """
    ✨ Parse CLI args for CSV input & image output.
    """
    default_output = os.path.join(DEFAULT_OUTPUT_DIR, "requests_vs_latency_heatmap.png")  # 🖼️ default image path
    if default_csv is None:
        default_csv = os.path.join(os.getcwd(), "data", "simulated_api_metrics.csv")  # 📄 default CSV path

    parser = argparse.ArgumentParser(description="Generate heatmap from CSV")
    parser.add_argument("--csv", "-c", default=default_csv, help=f"CSV input file (default: {default_csv})")  # 📥 CSV
    parser.add_argument("--output", "-o", default=default_output, help=f"Output image (default: {default_output})")  # 📤 output
    parser.add_argument(
        "--compression-level", "-q", type=int, default=compression_level,
        help=f"JPEG quality 0-100 (lower → smaller file, default {compression_level})"  # 📉 compress
    )
    return parser.parse_args()
