import os
import csv

def write_csv(rows, output_file):
    """Write rows to CSV file, auto-detecting columns."""
    if not rows:
        return
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    fieldnames = list(rows[0].keys())  # Auto-detect from first row
    
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)  # Use writerows() instead of loop