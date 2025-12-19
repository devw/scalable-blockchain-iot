"""Format metrics as LaTeX tables."""

from typing import List, Tuple, Dict


class LaTeXFormatter:
    """Formats performance metrics as LaTeX tables."""
    
    METRICS_SPEC = [
        ('total_requests', 'Total Requests', '{:,}', 'req'),
        ('successful_requests', 'Successful Requests', '{:,}', 'req'),
        ('success_rate', 'Success Rate', '{:.2f}', '\\%'),
        ('mean_latency', 'Mean Latency', '{:.2f}$\\pm${:.2f}', 'ms'),
        ('median_latency', 'Median Latency', '{:.2f}', 'ms'),
        ('p95_latency', 'P95 Latency', '{:.2f}', 'ms'),
        ('p99_latency', 'P99 Latency', '{:.2f}', 'ms'),
        ('max_latency', 'Max Latency', '{:.2f}', 'ms'),
        ('mean_requests_in_flight', 'Mean Requests in Flight', '{:.2f}', 'req'),
        ('max_concurrent_requests', 'Max Concurrent Requests', '{:.0f}', 'req'),
        ('throughput', 'Throughput', '{:.2f}', 'req/s'),
    ]
    
    def format_table(self, configs_data: List[Tuple[str, Dict]]) -> str:
        """Format configurations and metrics as LaTeX table."""
        table_rows = []
        
        for config_name, metrics in configs_data:
            table_rows.extend(self._format_config_rows(config_name, metrics))
        
        return self._build_latex_table(table_rows)
    
    def _format_config_rows(self, config: str, metrics: Dict) -> List[str]:
        """Format rows for a single configuration."""
        rows = []
        
        for i, (key, label, fmt, unit) in enumerate(self.METRICS_SPEC):
            if key == 'mean_latency':
                value = fmt.format(metrics[key], metrics['std_latency'])
            else:
                value = fmt.format(metrics[key])
            
            if i == 0:
                rows.append(f"{config} & {label} & {value} & {unit} \\\\")
            else:
                rows.append(f" & {label} & {value} & {unit} \\\\")
        
        return rows
    
    def _build_latex_table(self, rows: List[str]) -> str:
        """Build complete LaTeX table."""
        header = [
            "\\begin{table}[h]",
            "\\centering",
            "\\caption{Performance Comparison Between Autoscaling Configurations}",
            "\\begin{tabular}{|l|l|r|l|}",
            "\\hline",
            "\\textbf{Configuration} & \\textbf{Metric} & \\textbf{Value} & \\textbf{Unit} \\\\",
            "\\hline"
        ]
        
        footer = [
            "\\hline",
            "\\end{tabular}",
            "\\end{table}"
        ]
        
        return "\n".join(header + rows + footer)