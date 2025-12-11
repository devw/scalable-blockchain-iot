import statistics

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
