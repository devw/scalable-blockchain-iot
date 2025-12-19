import argparse
import logging
import os

DEFAULT_OUTPUT_DIR = "/tmp/"  # 📂 default output folder


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        verbose: Enable debug level logging
        
    Returns:
        Configured logger instance
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def parse_csv_image_args(default_csv: str = None, compression_level: int = 65):
    if default_csv is None:
        default_csv = os.path.join(os.getcwd(), "data", "simulated_api_metrics.csv")
    parser = argparse.ArgumentParser(description="Generate heatmap from CSV")
    parser.add_argument("--csv", "-c", default=default_csv,
                        help=f"CSV input file (default: {default_csv})")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_DIR,
                        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--compression-level", "-q", type=int, default=compression_level,
                        help=f"JPEG quality 0-100 (default {compression_level})")
    return parser.parse_args()