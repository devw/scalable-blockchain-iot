"""Generate LaTeX tables from performance metrics."""

from pathlib import Path
from typing import List
from analytics.utils.metrics_calculator import MetricsCalculator
from analytics.utils.latex_formatter import LaTeXFormatter

class PerformanceTableGenerator:
    """Generates performance comparison tables in LaTeX format."""
    
    def __init__(self):
        self.calculator = MetricsCalculator()
        self.formatter = LaTeXFormatter()
    
    def generate(self, csv_files: List[Path]) -> str:
        """Generate LaTeX table from CSV files.
        
        Args:
            csv_files: List of CSV file paths to process
            
        Returns:
            LaTeX formatted table string
        """
        configs_data = []
        
        for csv_file in csv_files:
            config_name = self._extract_config_name(csv_file)
            metrics = self.calculator.calculate(csv_file)
            configs_data.append((config_name, metrics))
        
        return self.formatter.format_table(configs_data)
    
    def _extract_config_name(self, csv_file: Path) -> str:
        """Extract configuration name from filename."""
        parts = csv_file.stem.split("__")
        for part in parts:
            if part.startswith("maxpods="):
                return part
        return csv_file.stem