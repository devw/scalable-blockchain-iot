import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from analytics.utils.file_utils import load_csv
from analytics.utils.logging_utils import log_info
from analytics.utils.cli_utils import parse_csv_image_args

def plot_requests_vs_latency(csv_path: str, output_path: str):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    df = pd.read_csv(csv_path)
    x, y = df["requests_in_flight"], df["latency_ms"]
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=30)

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
    plt.title("Requests in Flight vs Latency Heatmap")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    args = parse_csv_image_args()
    plot_requests_vs_latency(args.csv, args.output)
