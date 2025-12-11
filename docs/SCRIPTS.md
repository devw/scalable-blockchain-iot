# 📜 SCRIPTS.md

This document collects all command-line utilities for the project, including scripts to generate synthetic data, perform analysis, generate reports, launch containers, and more.

---

## ▶️ Generate Simulation CSV

Generate synthetic API metrics (RPS, latency, pods, requests in flight) using the Monte Carlo simulation engine.

### **Command**

```sh
python -m analytics.simulation.run_simulation \
  --duration 5 \
  --per-request \
  --output-dir ./data/test \
  --seed 42
```

### **Parameters**

| Parameter      | Type | Default  | Description                                      |
| -------------- | ---- | -------- | ------------------------------------------------ |
| `--output-dir` | str  | `./data` | Directory where the CSV file will be saved       |
| `--duration`   | int  | 60       | Duration of the simulation in minutes            |
| `--seed`       | int  | None     | Random seed for reproducibility                  |
| `--max-pods`   | int  | 5        | Maximum number of pods allowed in the simulation |

---

## ▶️ Generate Graphical Reports

Scripts generate charts from simulation CSVs and save them in `data/reports`.

| Script                           | Output               | Description                                       |
| -------------------------------- | -------------------- | ------------------------------------------------- |
| `generate_pods_over_time.py`     | `pods_over_time.png` | Line chart of pod count over time vs IoT requests |
| `generate_pod_scaling_events.py` | `scaling_events.png` | Step chart showing pod scaling events (up/down)   |

### **Command Examples**

From project root:

```sh
python -m analytics.reports.generate_pods_over_time
python -m analytics.reports.generate_scaling_events

python -m analytics.reports.generate_requests_vs_latency_heatmap \
        --csv data/test/simulated_api_metrics.csv \
        --output /tmp/output.png
```

Notes:

* Ensure simulation CSV exists before generating reports.
* Output files are saved in `data/reports/`.
* Utilities for logging and CSV loading are in `analytics/utils/`.
