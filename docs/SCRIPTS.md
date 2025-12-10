# 📜 SCRIPTS.md

This document collects all command-line utilities for the project, including scripts to generate synthetic data, perform analysis, generate reports, launch containers, and more.
More commands will be added as the project evolves.

---

## ▶️ Generate Simulation CSV

Generate synthetic API metrics (RPS, latency, pods, requests in flight) using the Monte Carlo simulation engine.

### **Command**

```sh
python -m analytics.simulation.run_simulation --output-dir ./data/
```

### **Description**

* Runs the simulation based on the configuration in `analytics/simulation/config.py`
* Produces a CSV file with Prometheus-like metrics
* File is written to the path provided as argument

### **Example Output**

```
timestamp,rps,requests_in_flight,latency_ms,pod_count
2025-01-01T12:00:00Z,48,65,110.33,1
2025-01-01T12:01:00Z,210,280,290.11,2
...
```

---

➡️ *New commands will be added in the next iterations.*
