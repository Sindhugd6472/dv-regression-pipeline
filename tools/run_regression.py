#!/usr/bin/env python3
"""Config-driven regression runner for small RTL/EDA flows."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Job:
    name: str
    compile: str
    run: str
    log: Path


def load_config(path: Path) -> list[Job]:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    jobs = []
    for item in data.get("jobs", []):
        jobs.append(
            Job(
                name=item["name"],
                compile=item["compile"],
                run=item["run"],
                log=Path(item["log"]),
            )
        )
    if not jobs:
        raise ValueError("Configuration contains no jobs")
    return jobs


def run_command(command: str) -> int:
    print(f"$ {command}")
    completed = subprocess.run(command, shell=True)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run configured RTL regression jobs")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/regression_jobs.json"),
        help="Regression configuration file",
    )
    parser.add_argument("--job", help="Run only one named job")
    parser.add_argument("--list", action="store_true", help="List configured jobs")
    args = parser.parse_args()

    try:
        jobs = load_config(args.config)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if args.list:
        for job in jobs:
            print(job.name)
        return 0

    if args.job:
        jobs = [job for job in jobs if job.name == args.job]
        if not jobs:
            print(f"ERROR: unknown job '{args.job}'")
            return 2

    failures = 0
    for job in jobs:
        print(f"\n=== {job.name} ===")
        if run_command(job.compile) != 0:
            print(f"{job.name}: compile failed")
            failures += 1
            continue

        job.log.parent.mkdir(parents=True, exist_ok=True)
        run_with_log = f"{job.run} | tee {shlex.quote(str(job.log))}"
        if run_command(run_with_log) != 0:
            print(f"{job.name}: simulation failed")
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
