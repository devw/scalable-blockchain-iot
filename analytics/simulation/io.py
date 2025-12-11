import os
import csv
from ..utils.csv_schema import CSV_FIELDS

def write_csv(rows, output_file):
    """Write rows to CSV file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
