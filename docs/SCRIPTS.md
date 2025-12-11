# 📜 SCRIPTS.md

This document collects all command-line utilities for the project, including scripts to generate synthetic data, perform analysis, generate reports, launch containers, and more.

---

## ▶️ Generate Simulation CSV

Generate synthetic API metrics (RPS, latency, pods, requests in flight) using the Monte Carlo simulation engine.

### **Command**

```sh
python -m analytics.simulation.run_simulation \
    --output-dir ./data/simulation \
    --duration 120 \
    --max-pods 5 \
    --seed 42
```

### **Parameters**

| Parameter      | Type | Default  | Description                                      |
| -------------- | ---- | -------- | ------------------------------------------------ |
| `--output-dir` | str  | `./data` | Directory where the CSV file will be saved       |
| `--duration`   | int  | 60       | Duration of the simulation in minutes            |
| `--seed`       | int  | None     | Random seed for reproducibility                  |
| `--max-pods`   | int  | 5        | Maximum number of pods allowed in the simulation |
