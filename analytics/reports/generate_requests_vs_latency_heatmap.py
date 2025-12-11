import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from analytics.utils.cli_utils import parse_csv_image_args


def extract_experiment_metadata(filename: str) -> dict:
    # Extract only relevant numeric metadata
    base = os.path.basename(filename)
    metadata = {}
    for key in ("maxpods", "duration"):
        match = re.search(rf"{key}=(\d+)", base)
        if match:
            metadata[key] = match.group(1)
    return metadata


def build_output_filename(output_dir: str, metadata: dict) -> str:
    # Filename: requests_vs_latency_heatmap_maxpods=XX_duration=YY.png
    parts = ["requests_vs_latency_heatmap"] + [f"{k}={metadata[k]}" for k in ("maxpods", "duration") if k in metadata]
    return os.path.join(output_dir, "_".join(parts) + ".png")


def format_metadata_for_title(metadata: dict) -> str:
    return ", ".join(f"{k}={v}" for k, v in metadata.items()) if metadata else ""


def plot_requests_vs_latency(csv_path: str, output_dir: str):
    df = pd.read_csv(csv_path)
    x, y = df["requests_in_flight"], df["latency_ms"]
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=30)

    metadata = extract_experiment_metadata(csv_path)
    meta_text = format_metadata_for_title(metadata)

    os.makedirs(output_dir, exist_ok=True)
    output_path = build_output_filename(output_dir, metadata)

    plt.figure(figsize=(10, 7))
    plt.imshow(heatmap.T, origin="lower", aspect="auto", cmap="viridis")
    plt.xlabel("Requests in Flight")
    plt.ylabel("Latency (ms)")
    plt.xticks(np.linspace(0, len(xedges)-1, 6),
               [f"{int(v)}" for v in np.linspace(xedges[0], xedges[-1], 6)])
    plt.yticks(np.linspace(0, len(yedges)-1, 6),
               [f"{int(v)}" for v in np.linspace(yedges[0], yedges[-1], 6)])
    plt.colorbar().set_label("Density")
    plt.title(f"Requests vs Latency Heatmap\n{meta_text}" if meta_text else "Requests vs Latency Heatmap")

    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_requests_vs_latency(args.csv, args.output)
