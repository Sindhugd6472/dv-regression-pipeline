# EDA Regression Automation Toolkit

![CI](https://github.com/Sindhugd6472/dv-regression-pipeline/actions/workflows/regression.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![SystemVerilog](https://img.shields.io/badge/SystemVerilog-RTL%20Verification-orange)
![CI/CD](https://img.shields.io/badge/CI-GitHub%20Actions-success)

A lightweight EDA/verification automation project that demonstrates how Python, shell-style flow orchestration, CI, and structured reporting can be used to make RTL regressions easier to run and analyze.

## Why this project

Semiconductor teams rely on repeatable automation around compile, simulation, regression, log parsing, reporting, and CI. This repository models that workflow with open-source tools so the full pipeline can be run locally or in GitHub Actions.

The project is intentionally split into reusable tooling and example RTL workloads. The Python utilities are not tied to a single DUT.

## What it demonstrates

- Config-driven regression execution
- Python command-line tooling
- Compile and simulation orchestration
- PASS/FAIL and functional-coverage log parsing
- JSON report generation
- Automated unit tests
- GitHub Actions CI
- Matrix regression across multiple designs
- Reusable flow structure for EDA/verification infrastructure

## Architecture

```text
config/regression_jobs.json
          |
          v
tools/run_regression.py
          |
          +--> compile RTL
          +--> launch simulation
          +--> capture logs
                    |
                    v
        coverage/parse_coverage.py
                    |
                    v
          structured JSON report
                    |
                    v
             CI artifacts
```

## Repository structure

```text
.
├── config/
│   └── regression_jobs.json     # Declarative regression job definitions
├── coverage/
│   ├── __init__.py
│   └── parse_coverage.py        # Reusable log/report parser
├── tools/
│   └── run_regression.py        # Config-driven regression launcher
├── tests/
│   └── test_parse_coverage.py   # Python unit tests
├── rtl/                         # FIFO RTL example
├── tb/                          # FIFO verification workload
├── rtl2/                        # Counter RTL example
├── tb2/                         # Counter verification workload
└── .github/workflows/
    └── regression.yml           # CI + matrix regression
```

## Quick start

### Requirements

- Python 3.10+
- Icarus Verilog
- Make is optional

Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y iverilog
```

macOS:

```bash
brew install icarus-verilog
```

### List configured jobs

```bash
python tools/run_regression.py --list
```

### Run one regression

```bash
python tools/run_regression.py --job fifo
```

### Run all configured regressions

```bash
python tools/run_regression.py
```

### Parse a log into JSON

```bash
python coverage/parse_coverage.py \
  sim/fifo_results.log \
  --design fifo \
  --output coverage/fifo_report.json \
  --fail-on-test-failure
```

### Run unit tests

```bash
python -m unittest discover -s tests -v
```

## Example configuration

```json
{
  "jobs": [
    {
      "name": "fifo",
      "compile": "iverilog -g2012 -o sim/fifo_sim rtl/fifo.sv tb/fifo_tb.sv",
      "run": "vvp sim/fifo_sim",
      "log": "sim/fifo_results.log"
    }
  ]
}
```

The runner reads this configuration rather than hard-coding each design into the Python implementation. This makes it straightforward to add another regression workload without changing the orchestration code.

## CI workflow

Every pull request runs:

1. Python unit tests
2. Configuration validation
3. FIFO regression
4. Counter regression
5. Structured report generation
6. Artifact upload

The RTL jobs run through a GitHub Actions matrix so additional designs can be added with minimal workflow duplication.

## Skills demonstrated

**Software / automation**
- Python
- CLI design
- Configuration-driven tooling
- JSON
- Unit testing
- Error handling
- Git / GitHub Actions
- CI/CD

**Semiconductor / EDA context**
- RTL simulation
- Regression execution
- Verification log parsing
- Functional coverage reporting
- SystemVerilog
- Icarus Verilog

## Roadmap

Planned improvements include:

- parallel/local job execution
- runtime and failure-signature collection
- regression history/trend reports
- YAML configuration support
- richer HTML dashboard generation
- Tcl/shell integration examples
- pluggable simulator adapters

## Author

**Sindhu Govindareddy Doddamane**

Semiconductor verification engineer building toward EDA software, design-enablement, and flow-automation roles.

- GitHub: https://github.com/Sindhugd6472
- LinkedIn: https://linkedin.com/in/sindhu-govindareddy-doddamane-801300237

## License

MIT

## Regression correctness

FIFO pointers wrap at DEPTH, including non-power-of-two depths and DEPTH=1. The reference-model test checks returned data, flags, blocked boundary operations, simultaneous transfers and reset. FIFO CI exercises depths 1, 3, 8 and 9. Counter checks include load priority, hold, both directions, wrap, boundary flags and reset. Functional coverage here means only the listed observed testbench events; it is not code coverage or signoff coverage.

The runner preserves simulator exit status while logging. The parser rejects an empty result log when `--fail-on-test-failure` is enabled. Run `python -m unittest discover -s tests -v` and `python tools/run_regression.py`.
