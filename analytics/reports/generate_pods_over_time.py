import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics.utils.file_utils import load_csv, build_output_filename
from analytics.utils.logging_utils import log_csv_loaded, log_saved_plot
from analytics.utils.cli_utils import parse_csv_image_args


def plot_pods_over_time(csv_path: str, output_path: str):
    df = load_csv(csv_path)
    log_csv_loaded(csv_path)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.sort_values('timestamp', inplace=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df['timestamp'], df['pod_count'], marker='o')
    plt.xlabel('Time')
    plt.ylabel('Number of Pods')
    plt.title('Pods Over Time')
    plt.grid(True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    log_saved_plot(output_path)


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_pods_over_time(args.csv, build_output_filename(args.output, args.csv))
