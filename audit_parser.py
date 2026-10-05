import argparse
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r"\s*\|\s*user=(?P<username>\S+)"
    r"\s*\|\s*operation=(?P<operation>\S+)"
)


def parse_log_file(filename):
    """Read an audit log line by line and aggregate activity."""
    activity = Counter()
    skipped_lines = 0

    with open(filename, "r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            line = line.strip()

            if not line:
                continue

            match = LOG_PATTERN.match(line)

            if not match:
                skipped_lines += 1
                print(f"Warning: skipped invalid line {line_number}")
                continue

            try:
                timestamp = datetime.strptime(
                    match.group("timestamp"),
                    "%Y-%m-%d %H:%M:%S",
                )
            except ValueError:
                skipped_lines += 1
                print(f"Warning: invalid timestamp on line {line_number}")
                continue

            date = timestamp.date().isoformat()
            username = match.group("username")
            operation = match.group("operation").upper()

            activity[(date, username, operation)] += 1

    return activity, skipped_lines


def write_summary(activity, filename):
    """Write aggregated activity to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["date", "username", "operation", "count"])

        for (date, username, operation), count in sorted(activity.items()):
            writer.writerow([date, username, operation, count])


def main():
    parser = argparse.ArgumentParser(
        description="Parse audit logs and generate a daily user activity CSV."
    )
    parser.add_argument(
        "--input",
        default="sample_audit.log",
        help="Path to the audit log file (default: sample_audit.log)",
    )
    parser.add_argument(
        "--output",
        default="daily_summary.csv",
        help="Path to the summary CSV (default: daily_summary.csv)",
    )
    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        parser.error(f"Input file not found: {input_file}")

    print(f"Reading audit log: {input_file}")

    activity, skipped_lines = parse_log_file(input_file)
    write_summary(activity, output_file)

    processed_events = sum(activity.values())

    print(f"Processed events: {processed_events}")
    print(f"Skipped lines: {skipped_lines}")
    print(f"Summary written to: {output_file}")


if __name__ == "__main__":
    main()
