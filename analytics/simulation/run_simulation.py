import argparse
import os
import random
from datetime import datetime, timedelta

from .io import write_csv
from .stats import compute_statistics, print_statistics
from .data_generator import DataGenerator
from .config import load_config

def generate_time_series(start: datetime, minutes: int):
    """Generate list of timestamps, one per simulated minute."""
    return [start + timedelta(minutes=i) for i in range(minutes)]

def run_simulation_cli(cfg, max_pods=5, per_request=False):
    """Run simulation: aggregated (minute-level) or per-request logs."""
    generator = DataGenerator(
        max_pods=max_pods, 
        pod_scale_threshold=getattr(cfg, "pod_scale_threshold", 50)
    )
    rows = []
    start = datetime.utcnow()
    
    for minute_index in range(cfg.duration_minutes):
        if per_request:
            # Generate per-request logs for each second in this minute
            for second in range(60):
                ts = start + timedelta(minutes=minute_index, seconds=second)
                rows.extend(generator.generate_request_data(ts, duration_seconds=1))
        else:
            # Original: one aggregated row per minute
            timestamp = start + timedelta(minutes=minute_index)
            row = generator.generate_minute_data()
            row["timestamp"] = timestamp.isoformat()
            rows.append(row)
    
    return rows

def main():
    parser = argparse.ArgumentParser(description="Run synthetic data simulation")
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--duration", type=int, help="Simulation duration in minutes")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--max-pods", type=int, default=5, help="Maximum number of pods")
    parser.add_argument("--per-request", action="store_true", 
                       help="Generate per-request logs instead of aggregated")
    args = parser.parse_args()

    cfg = load_config()
    if args.duration:
        cfg.duration_minutes = args.duration
    if args.seed:
        random.seed(args.seed)

    # Run simulation
    rows = run_simulation_cli(cfg, max_pods=args.max_pods, per_request=args.per_request)

    # Save CSV
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, "simulated_api_metrics.csv")
    write_csv(rows, output_file)

    # Compute stats only for aggregated mode
    if not args.per_request:
        stats = compute_statistics(rows)
        print_statistics(stats)
    
    print(f"\n💾 CSV saved to: {output_file} ({len(rows)} records)")

if __name__ == "__main__":
    main()