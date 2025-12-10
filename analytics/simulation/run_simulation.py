import os
import csv
import statistics
from datetime import datetime
from .data_generator import generate_minute_data
from ..utils.time_utils import generate_time_series
from ..utils.csv_schema import CSV_FIELDS
from .config import load_config

def run_simulation(cfg):
    """Simulate data and return list of rows."""
    rows = []
    start = datetime.utcnow()
    for ts in generate_time_series(start, cfg.duration_minutes):
        row = generate_minute_data()
        rows.append(row)
    return rows

def write_csv(rows, output_file):
    """Write rows to CSV file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def compute_statistics(rows):
    """Compute aggregated statistics."""
    rps_list = [r['rps'] for r in rows]
    latency_list = [r['latency_ms'] for r in rows]
    pods_list = [r['pod_count'] for r in rows]
    return {
        "num_rows": len(rows),
        "avg_rps": statistics.mean(rps_list),
        "avg_latency": statistics.mean(latency_list),
        "avg_pods": statistics.mean(pods_list)
    }

def print_statistics(stats):
    """Print statistics to console."""
    print("\n--- Simulation Summary ---")
    print(f"Total rows generated: {stats['num_rows']}")
    print(f"Average RPS: {stats['avg_rps']:.2f}")
    print(f"Average latency (ms): {stats['avg_latency']:.2f}")
    print(f"Average pods: {stats['avg_pods']:.2f}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run synthetic data simulation")
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--duration", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    cfg = load_config()
    if args.duration:
        cfg.duration_minutes = args.duration
    if args.seed:
        import random
        random.seed(args.seed)

    rows = run_simulation(cfg)
    output_file = os.path.join(args.output_dir, "simulated_api_metrics.csv")
    write_csv(rows, output_file)

    stats = compute_statistics(rows)
    print_statistics(stats)
    print(f"\n💾 CSV saved to: {output_file}")

if __name__ == "__main__":
    main()
