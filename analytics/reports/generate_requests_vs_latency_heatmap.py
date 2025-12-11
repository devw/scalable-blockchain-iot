import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from analytics.utils.cli_utils import parse_csv_image_args


def extract_experiment_metadata(filename: str) -> dict:
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)

    matches = re.findall(r"([a-zA-Z0-9]+)=([a-zA-Z0-9_\-]+)", name)
    metadata = dict(matches)

    return metadata


def format_metadata_for_title(metadata: dict) -> str:
    if not metadata:
        return ""
    return ", ".join(f"{k}={v}" for k, v in metadata.items())


def plot_requests_vs_latency(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path)
    x, y = df["requests_in_flight"], df["latency_ms"]

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=30)

    metadata = extract_experiment_metadata(csv_path)
    meta_text = format_metadata_for_title(metadata)

    plt.figure(figsize=(10, 7))
    plt.imshow(heatmap.T, origin="lower", aspect="auto", cmap="viridis")
    plt.xlabel("Requests in Flight")
    plt.ylabel("Latency (ms)")

    plt.xticks(
        np.linspace(0, len(xedges)-1, 6),
        [f"{int(v)}" for v in np.linspace(xedges[0], xedges[-1], 6)]
    )
    plt.yticks(
        np.linspace(0, len(yedges)-1, 6),
        [f"{int(v)}" for v in np.linspace(yedges[0], yedges[-1], 6)]
    )

    plt.colorbar().set_label("Density")

    if meta_text:
        plt.title(f"Requests vs Latency Heatmap\n{meta_text}")
    else:
        plt.title("Requests vs Latency Heatmap")

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_requests_vs_latency(args.csv, args.output)
