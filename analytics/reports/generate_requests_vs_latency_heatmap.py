import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info

def plot_requests_vs_latency(csv_path: str, output_path: str):
    log_info(f"Loading CSV from: {csv_path}")
    df = load_csv(csv_path)

    plt.figure(figsize=(10, 6))

    # Heatmap: densità dei punti
    sns.histplot(
        data=df,
        x='requests_in_flight',
        y='latency_ms',
        bins=20,
        pthresh=.1,
        cmap='viridis'
    )

    plt.xlabel('Requests in Flight')
    plt.ylabel('Latency (ms)')
    plt.title('Heatmap: Requests in Flight vs Latency')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()

    log_info(f"Saved heatmap to: {output_path}")


if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(BASE, "data", "simulation", "simulated_api_metrics.csv")
    output_path = os.path.join(BASE, "data", "reports", "requests_vs_latency_heatmap.png")
    plot_requests_vs_latency(csv_path, output_path)
