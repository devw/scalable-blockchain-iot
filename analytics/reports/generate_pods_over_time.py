import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info

def plot_pods_over_time(csv_path: str, output_path: str):
    """
    Generates a line chart showing number of pods over time.
    """


    log_info(f"Loading CSV data from: {csv_path}")
    df = load_csv(csv_path)


    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')


    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['pod_count'], marker='o', label='Pod count')


    plt.xlabel('Time')
    plt.ylabel('Number of Pods')
    plt.title('Number of Pods Over Time (Response to IoT Requests)')
    plt.grid(True)


    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


    log_info(f"Saved plot to: {output_path}")

if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_file = os.path.join(BASE, "data", "simulation", "simulated_api_metrics.csv")
    output_file = os.path.join(BASE, "data", "reports", "pods_over_time.png")


plot_pods_over_time(csv_file, output_file)