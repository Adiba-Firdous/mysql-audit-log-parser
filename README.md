# MySQL Audit Log Parser

A lightweight Python parser that reads audit log entries line by line, extracts the timestamp, username, and operation type, and generates a daily user activity summary CSV.

## Task

Develop a Python parser that:

1. Reads an audit log file line by line
2. Extracts timestamp, username, and operation type
3. Aggregates activity per user per day
4. Writes the aggregated data to `daily_summary.csv`

## Features

- Line-by-line audit log parsing
- Timestamp validation
- Username and operation extraction
- Daily aggregation by user and operation
- Invalid-line warning and skip handling
- CSV output using Python's standard library
- Command-line input and output file options
- No external dependencies

## Project Structure

```text
mysql-audit-log-parser/
├── audit_parser.py
├── sample_audit.log
├── daily_summary.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Log Format

The parser expects entries in this format:

```text
YYYY-MM-DD HH:MM:SS | user=username | operation=OPERATION
```

Example:

```text
2026-10-05 09:15:22 | user=adiba | operation=SELECT
```

## Run the Parser

No package installation is required.

```bash
python audit_parser.py
```

Expected output:

```text
Reading audit log: sample_audit.log
Processed events: 12
Skipped lines: 0
Summary written to: daily_summary.csv
```

## Custom Input and Output

You can provide another audit log:

```bash
python audit_parser.py --input audit.log --output report.csv
```

## Example CSV Output

```csv
date,username,operation,count
2026-10-05,adiba,SELECT,2
2026-10-05,adiba,UPDATE,1
2026-10-05,rahul,INSERT,2
2026-10-05,rahul,SELECT,1
2026-10-05,sara,SELECT,1
2026-10-05,sara,UPDATE,1
2026-10-06,adiba,SELECT,1
2026-10-06,rahul,UPDATE,1
2026-10-06,sara,SELECT,1
```

## Error Handling

Malformed log lines are skipped with a warning instead of stopping the complete parsing process.

Example:

```text
Warning: skipped invalid line 7
```

## Technologies

- Python 3
- `csv`
- `re`
- `datetime`
- `collections.Counter`
- `argparse`

All modules are part of Python's standard library.

## Future Improvements

- Support additional audit-log formats
- Add JSON output
- Add date-range filtering
- Add automated scheduled reports
- Add unit tests with `pytest`

## Author

Adiba-Firdous
