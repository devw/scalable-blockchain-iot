import argparse
from .simulator import run_simulation
from .io import write_csv
from .stats import compute_statistics, print_statistics
from .config import load_config
import os

def main():
    parser = argparse.ArgumentParser(description="Run synthetic data simulation")
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--duration", type=int)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    cfg = load_config()
    if args.duration: cfg.duration_minutes = args.duration
    if args.seed: import random; random.seed(args.seed)

    rows = run_simulation(cfg)
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, "simulated_api_metrics.csv")
    write_csv(rows, output_file)

    stats = compute_statistics(rows)
    print_statistics(stats)
    print(f"\n💾 CSV saved to: {output_file}")

if __name__ == "__main__":
    main()
