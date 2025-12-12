import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info
from analytics.utils.cli_utils import parse_csv_image_args

def build_scaling_output_filename(output_dir: str, csv_path: str) -> str:
    base = os.path.basename(csv_path).replace(".csv", "")
    filename = f"scaling_events_{base}.png"
    return os.path.join(output_dir, filename)

def plot_scaling_events(csv_path: str, output_path: str):
    log_info(f"Loading CSV from: {csv_path}")
    df = load_csv(csv_path)

    # Convert timestamp and aggregate pod_count per timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.groupby('timestamp', as_index=False).agg({'pod_count': 'max'})

    # Detect scaling events
    df['prev_pod_count'] = df['pod_count'].shift(1)
    df['scaling_event'] = df['pod_count'] != df['prev_pod_count']
    df['scaling_direction'] = df['pod_count'].sub(df['prev_pod_count']).apply(
        lambda x: 'up' if x > 0 else ('down' if x < 0 else None)
    )

    # Plot step chart with scaling events
    plt.figure(figsize=(10, 4))
    plt.step(df['timestamp'], df['pod_count'], where='post', label='Pod Count')
    events = df[df['scaling_event']]
    plt.scatter(events['timestamp'], events['pod_count'], color='red', label='Scaling Event', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Pod Count')
    plt.title('Pod Scaling Events (Step Chart)')
    plt.legend()
    plt.grid(True)

    # Save plot
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    log_info(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    args = parse_csv_image_args()
    output_path = build_scaling_output_filename(args.output, args.csv)
    plot_scaling_events(args.csv, output_path)
