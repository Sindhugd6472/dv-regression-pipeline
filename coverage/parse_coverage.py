#!/usr/bin/env python3
"""Parse simulation logs into a structured regression report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PASS_PREFIX = "PASS:"
FAIL_PREFIX = "FAIL:"
COVERAGE_RE = re.compile(r"Functional Coverage:\s*(\d+(?:\.\d+)?)%")


def parse_results(log_file: Path, design_name: str) -> dict[str, Any]:
    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    results: dict[str, Any] = {
        "design_name": design_name,
        "tests": [],
        "summary": {"passed": 0, "failed": 0, "total": 0},
        "coverage": 0.0,
    }

    for raw_line in log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()

        if line.startswith(PASS_PREFIX):
            name = line.removeprefix(PASS_PREFIX).strip()
            results["tests"].append({"name": name, "status": "PASS"})
            results["summary"]["passed"] += 1
        elif line.startswith(FAIL_PREFIX):
            name = line.removeprefix(FAIL_PREFIX).strip()
            results["tests"].append({"name": name, "status": "FAIL"})
            results["summary"]["failed"] += 1

        match = COVERAGE_RE.search(line)
        if match:
            results["coverage"] = float(match.group(1))

    results["summary"]["total"] = (
        results["summary"]["passed"] + results["summary"]["failed"]
    )
    return results


def save_json(results: dict[str, Any], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(results, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse PASS/FAIL markers and functional coverage from a simulation log."
    )
    parser.add_argument("log_file", type=Path, help="Simulation log to parse")
    parser.add_argument(
        "--design",
        default="unknown-design",
        help="Friendly design name stored in the report",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("coverage/coverage_report.json"),
        help="JSON report path",
    )
    parser.add_argument(
        "--fail-on-test-failure",
        action="store_true",
        help="Return a non-zero exit code when one or more tests fail",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        results = parse_results(args.log_file, args.design)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 2

    save_json(results, args.output)

    summary = results["summary"]
    print(
        f"{args.design}: {summary['passed']} passed, "
        f"{summary['failed']} failed, coverage={results['coverage']:.2f}%"
    )
    print(f"Report: {args.output}")

    if args.fail_on_test_failure and summary["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
