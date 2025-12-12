import os
import numpy as np
import matplotlib.pyplot as plt

from analytics.utils.cli_utils import parse_csv_image_args
from analytics.utils.file_utils import load_csv, build_output_filename, extract_metadata
from analytics.utils.logging_utils import log_csv_loaded, log_saved_plot

def plot_requests_vs_latency(csv_path: str, output_dir: str):
    df = load_csv(csv_path)
    log_csv_loaded(csv_path)

    x, y = df["requests_in_flight"], df["latency_ms"]
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=30)

    metadata = extract_metadata(csv_path)
    meta_text = ", ".join(f"{k}={v}" for k, v in metadata.items())

    os.makedirs(output_dir, exist_ok=True)
    output_path = build_output_filename(output_dir, csv_path, prefix="requests_vs_latency_heatmap")

    plt.figure(figsize=(10, 7))
    plt.imshow(heatmap.T, origin="lower", aspect="auto", cmap="viridis")

    plt.xlabel("Requests in Flight")
    plt.ylabel("Latency (ms)")
    plt.colorbar(label="Density")

    # Tick labels
    plt.xticks(
        np.linspace(0, len(xedges)-1, 6),
        [f"{int(v)}" for v in np.linspace(xedges[0], xedges[-1], 6)]
    )
    plt.yticks(
        np.linspace(0, len(yedges)-1, 6),
        [f"{int(v)}" for v in np.linspace(yedges[0], yedges[-1], 6)]
    )

    title = "Requests vs Latency Heatmap"
    plt.title(f"{title}\n{meta_text}" if meta_text else title)

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    log_saved_plot(output_path)


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_requests_vs_latency(args.csv, args.output)
