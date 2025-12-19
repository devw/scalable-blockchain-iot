"""Calculate performance metrics from simulation data."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict


class MetricsCalculator:
    """Calculates performance metrics from CSV simulation data."""
    
    def calculate(self, csv_file: Path) -> Dict[str, float]:
        """Calculate all metrics from a CSV file.
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            Dictionary of metric names and values
        """
        df = pd.read_csv(csv_file)
        
        total_requests = len(df)
        successful = df['success'].sum()
        success_rate = (successful / total_requests * 100) if total_requests > 0 else 0
        
        latencies = df['latency_ms']
        duration = df['timestamp'].max() - df['timestamp'].min()
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful,
            'success_rate': success_rate,
            'mean_latency': latencies.mean(),
            'std_latency': latencies.std(),
            'median_latency': latencies.median(),
            'p95_latency': latencies.quantile(0.95),
            'p99_latency': latencies.quantile(0.99),
            'max_latency': latencies.max(),
            'mean_requests_in_flight': df['requests_in_flight'].mean(),
            'max_concurrent_requests': df['requests_in_flight'].max(),
            'throughput': total_requests / duration if duration > 0 else 0
        }