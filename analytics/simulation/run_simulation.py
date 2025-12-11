import argparse
import os
import random
from datetime import datetime, timedelta

from .io import write_csv
from .data_generator import DataGenerator
from .config import load_config

def generate_time_series(start: datetime, minutes: int):
    """Generate list of timestamps, one per simulated minute."""
    return [start + timedelta(minutes=i) for i in range(minutes)]

def run_simulation_cli(cfg, max_pods=5):
    """Run high-resolution (per-request) simulation."""
    generator = DataGenerator(
        max_pods=max_pods,
        pod_scale_threshold=getattr(cfg, "pod_scale_threshold", 50)
    )
    
    rows = []
    start = datetime.utcnow()

    for minute_index in range(cfg.duration_minutes):
        for second in range(60):
            ts = start + timedelta(minutes=minute_index, seconds=second)
            rows.extend(
                generator.generate_request_data(ts, duration_seconds=1)
            )

    return rows

def main():
    parser = argparse.ArgumentParser(description="Run synthetic data simulation")
    parser.add_argument("--output-dir", type=str, default="./data",
                        help="Directory to store output artifacts")
    parser.add_argument("--duration", type=int,
                        help="Simulation duration in minutes")
    parser.add_argument("--seed", type=int,
                        help="Random seed for reproducibility")
    parser.add_argument("--max-pods", type=int, default=5,
                        help="Maximum number of pods")
    args = parser.parse_args()

    cfg = load_config()

    if args.duration:
        cfg.duration_minutes = args.duration
    if args.seed:
        random.seed(args.seed)

    # Run simulation (single mode)
    rows = run_simulation_cli(cfg, max_pods=args.max_pods)

    # Scientific filename
    label_parts = [
        f"duration={cfg.duration_minutes}",
        f"seed={args.seed if args.seed is not None else 'none'}",
        f"maxpods={args.max_pods}"
    ]
    label = "__".join(label_parts)

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, f"sim__{label}.csv")

    write_csv(rows, output_file)

    print(f"\nCSV saved to: {output_file} ({len(rows)} records)")

if __name__ == "__main__":
    main()