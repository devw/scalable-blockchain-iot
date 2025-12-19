"""Generate LaTeX performance comparison table from simulation CSV files."""

import argparse
from pathlib import Path
import sys

from analytics.utils.cli_utils import setup_logging
from analytics.utils.file_utils import validate_input_files, ensure_output_directory
from analytics.utils.table_generator import PerformanceTableGenerator


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate performance comparison table in LaTeX format"
    )
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="Input CSV files to compare"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output LaTeX file path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    logger = setup_logging(verbose=args.verbose)
    
    try:
        input_files = [Path(f) for f in args.input]
        validate_input_files(input_files)
        
        output_path = Path(args.output)
        ensure_output_directory(output_path)
        
        generator = PerformanceTableGenerator()
        latex_content = generator.generate(input_files)
        
        output_path.write_text(latex_content)
        logger.info(f"Table generated successfully: {output_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to generate table: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())