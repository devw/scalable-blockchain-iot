import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info
from analytics.utils.cli_utils import parse_csv_image_args

def plot_requests_vs_latency(csv_path: str, output_path: str):
    log_info(f"Loading CSV from: {csv_path}")
    df = load_csv(csv_path)

    # Aggiungiamo una colonna "count" per compatibilità con histplot
    df['count'] = 1

    plt.figure(figsize=(10, 6))

    # Heatmap: densità dei punti
    sns.histplot(
        data=df,
        x='requests_in_flight',
        y='latency_ms',
        weights='count',
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

    # Stampiamo la heatmap ASCII
    print_requests_vs_latency_ascii(df)


def print_requests_vs_latency_ascii(df: pd.DataFrame, x_bins: int = 20, y_bins: int = 10):
    """
    Stampa una heatmap ASCII dei dati rps/latency usando numeri da 1 a 5.
    """
    # Definiamo gli intervalli
    x_edges = np.linspace(df['requests_in_flight'].min(), df['requests_in_flight'].max(), x_bins + 1)
    y_edges = np.linspace(df['latency_ms'].min(), df['latency_ms'].max(), y_bins + 1)

    # Histogram 2D
    hist, _, _ = np.histogram2d(df['latency_ms'], df['requests_in_flight'], bins=[y_edges, x_edges])

    # Normalizziamo la densità da 1 a 5
    # Consideriamo solo i bin non vuoti
    nonzero = hist[hist > 0]
    if len(nonzero) == 0:
        print("No data to display in ASCII heatmap.")
        return

    quantiles = np.percentile(nonzero, [20, 40, 60, 80])
    ascii_grid = np.full(hist.shape, ' ', dtype=str)

    for i in range(hist.shape[0]):
        for j in range(hist.shape[1]):
            count = hist[i, j]
            if count == 0:
                continue
            elif count <= quantiles[0]:
                ascii_grid[i, j] = '1'
            elif count <= quantiles[1]:
                ascii_grid[i, j] = '2'
            elif count <= quantiles[2]:
                ascii_grid[i, j] = '3'
            elif count <= quantiles[3]:
                ascii_grid[i, j] = '4'
            else:
                ascii_grid[i, j] = '5'

    # Stampiamo riga per riga (Y decrescente per avere alta latenza in alto)
    y_labels = np.round(y_edges[1:], 1)
    x_labels = np.round(x_edges[1:], 1)

    print("\nASCII Heatmap: Requests in Flight vs Latency (ms)\n")
    for i in reversed(range(ascii_grid.shape[0])):
        row = ''.join(ascii_grid[i, :])
        print(f"{y_labels[i]:>6} | {row}")
    print("       +" + "-" * ascii_grid.shape[1])
    x_tick_indices = np.linspace(0, ascii_grid.shape[1]-1, min(5, ascii_grid.shape[1]), dtype=int)
    x_tick_labels = [f"{x_labels[idx]:.0f}" for idx in x_tick_indices]
    x_tick_pos = [idx for idx in x_tick_indices]
    tick_line = [' ']*ascii_grid.shape[1]
    for pos, label in zip(x_tick_pos, x_tick_labels):
        tick_line[pos] = '|'
    print("       " + ''.join(tick_line))
    print("       " + ' '.join(x_tick_labels))

    print("\nLegend: 1 = low density, 5 = high density, ' ' = no points\n")


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_requests_vs_latency(args.csv, args.output)
