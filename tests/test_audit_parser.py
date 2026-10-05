import csv
import subprocess
import sys
from pathlib import Path


def test_audit_parser_generates_expected_summary():
    project_dir = Path(__file__).resolve().parent.parent
    input_file = project_dir / "sample_audit.log"
    output_file = project_dir / "tests" / "test_output.csv"

    result = subprocess.run(
        [
            sys.executable,
            str(project_dir / "audit_parser.py"),
            "--input",
            str(input_file),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Processed events: 12" in result.stdout
    assert "Skipped lines: 0" in result.stdout
    assert output_file.exists()

    with output_file.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 9

    assert {
        "date": "2026-10-05",
        "username": "adiba",
        "operation": "SELECT",
        "count": "3",
    } in rows

    assert {
        "date": "2026-10-05",
        "username": "rahul",
        "operation": "INSERT",
        "count": "2",
    } in rows

    assert {
        "date": "2026-10-06",
        "username": "sara",
        "operation": "SELECT",
        "count": "1",
    } in rows

    output_file.unlink()