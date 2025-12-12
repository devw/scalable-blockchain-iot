import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics.utils.file_utils import load_csv, build_output_filename
from analytics.utils.logging_utils import log_csv_loaded, log_saved_plot
from analytics.utils.cli_utils import parse_csv_image_args


def plot_scaling_events(csv_path: str, output_path: str):
    df = load_csv(csv_path)
    log_csv_loaded(csv_path)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.groupby('timestamp', as_index=False).agg({'pod_count': 'max'})

    df['prev_pod_count'] = df['pod_count'].shift(1)
    df['scaling_event'] = df['pod_count'] != df['prev_pod_count']

    plt.figure(figsize=(10, 4))
    plt.step(df['timestamp'], df['pod_count'], where='post')
    events = df[df['scaling_event']]
    plt.scatter(events['timestamp'], events['pod_count'], color='red', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Pod Count')
    plt.title('Pod Scaling Events')
    plt.grid(True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    log_saved_plot(output_path)


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_scaling_events(args.csv, build_output_filename(args.output, args.csv))
