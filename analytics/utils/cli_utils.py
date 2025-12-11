import argparse

def parse_csv_image_args():
    """
    Parse command-line arguments for scripts that need a CSV input and an output image path.
    Returns:
        argparse.Namespace: contains csv_path and output_path
    """
    parser = argparse.ArgumentParser(
        description="Generate heatmap from CSV and save as image"
    )
    parser.add_argument(
        "--csv", "-c",
        required=True,
        help="Path to input CSV file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output image file"
    )
    return parser.parse_args()
