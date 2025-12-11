import os
import pandas as pd
import matplotlib.pyplot as plt

from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info


def plot_scaling_events(csv_path: str, output_path: str):
    log_info(f"Loading CSV from: {csv_path}")
    df = load_csv(csv_path)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Detect scaling events
    df['prev_pod_count'] = df['pod_count'].shift(1)
    df['scaling_event'] = df['pod_count'] != df['prev_pod_count']

    # Scaling direction
    df['scaling_direction'] = df.apply(
        lambda row: 'up' if row['pod_count'] > row['prev_pod_count'] else
                    ('down' if row['pod_count'] < row['prev_pod_count'] else None),
        axis=1
    )

    plt.figure(figsize=(10, 4))
    plt.step(df['timestamp'], df['pod_count'], where='post', label='Pod Count')

    # Mark scaling events
    events = df[df['scaling_event']]
    plt.scatter(events['timestamp'], events['pod_count'], color='red', label='Scaling Event', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Pod Count')
    plt.title('Pod Scaling Events (Step Chart)')
    plt.legend()
    plt.grid(True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    log_info(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(BASE, "data", "simulation", "simulated_api_metrics.csv")
    output_path = os.path.join(BASE, "data", "reports", "scaling_events.png")
    plot_scaling_events(csv_path, output_path)
