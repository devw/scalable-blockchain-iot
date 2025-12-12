import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info
from analytics.utils.cli_utils import parse_csv_image_args

def plot_pods_over_time(csv_path: str, output_path: str):
    """📈 Line chart of pod count over time."""
    log_info(f"Loading CSV from: {csv_path}")
    df = load_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['pod_count'], marker='o', label='Pod Count')
    plt.xlabel('Time')
    plt.ylabel('Number of Pods')
    plt.title('Number of Pods Over Time (Response to IoT Requests)')
    plt.grid(True)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    log_info(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_pods_over_time(args.csv, args.output)
