# Coverage Parser
# Parses simulation log and extracts coverage + test results
# Author: Sindhu Govindareddy Doddamane

import sys
import re
import json
import os

def parse_results(log_file):
    """Parse simulation log file for test results and coverage"""
    
    results = {
        "tests": [],
        "summary": {
            "passed": 0,
            "failed": 0,
            "total": 0
        },
        "coverage": 0.0
    }

    if not os.path.exists(log_file):
        print(f"ERROR: Log file '{log_file}' not found!")
        sys.exit(1)

    with open(log_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # Parse PASS/FAIL lines
        if line.startswith("PASS:"):
            results["tests"].append({
                "name": line.replace("PASS:", "").strip(),
                "status": "PASS"
            })
            results["summary"]["passed"] += 1

        elif line.startswith("FAIL:"):
            results["tests"].append({
                "name": line.replace("FAIL:", "").strip(),
                "status": "FAIL"
            })
            results["summary"]["failed"] += 1

        # Parse Coverage
        elif "Functional Coverage:" in line:
            match = re.search(r"(\d+\.\d+)%", line)
            if match:
                results["coverage"] = float(match.group(1))

    results["summary"]["total"] = (
        results["summary"]["passed"] + 
        results["summary"]["failed"]
    )

    return results


def print_report(results):
    """Print a clean summary report"""
    print("\n" + "="*45)
    print("       VERIFICATION COVERAGE REPORT")
    print("="*45)

    for test in results["tests"]:
        icon = "✅" if test["status"] == "PASS" else "❌"
        print(f"  {icon}  {test['name']}")

    print("-"*45)
    print(f"  Total Tests : {results['summary']['total']}")
    print(f"  Passed      : {results['summary']['passed']}")
    print(f"  Failed      : {results['summary']['failed']}")
    print(f"  Coverage    : {results['coverage']:.2f}%")
    print("="*45 + "\n")


def save_json(results, output_file="coverage/coverage_report.json"):
    """Save results as JSON for dashboard"""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📊 Report saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_coverage.py <sim_results.log>")
        sys.exit(1)

    log_file = sys.argv[1]
    results  = parse_results(log_file)

    print_report(results)
    save_json(results)
