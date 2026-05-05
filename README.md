# dv-regression-pipeline
Automated RTL verification pipeline with CI/CD and live coverage dashboard

markdown# 🔬 DV Regression Pipeline

![CI](https://github.com/Sindhugd6472/dv-regression-pipeline/actions/workflows/regression.yml/badge.svg)
![Language](https://img.shields.io/badge/Language-SystemVerilog-blue)
![Python](https://img.shields.io/badge/Python-3.10-green)
![Coverage](https://img.shields.io/badge/Functional%20Coverage-98%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Automated RTL verification pipeline with CI/CD and live coverage dashboard — built for a synchronous FIFO controller using SystemVerilog, Icarus Verilog, Python, and GitHub Actions.

---

## 📌 Project Overview

This project demonstrates a **production-style verification pipeline** that:
- ✅ Compiles and simulates RTL automatically on every Git push
- ✅ Parses simulation logs and extracts functional coverage
- ✅ Generates a live HTML coverage dashboard
- ✅ Runs end-to-end in the cloud using GitHub Actions CI/CD

---

## 🗂️ Project Structure

'''
dv-regression-pipeline/
│
├── rtl/
│   └── fifo.sv                  # Synchronous FIFO DUT (8x8)
├── tb/
│   └── fifo_tb.sv               # SystemVerilog Testbench + Coverage
├── sim/
│   └── Makefile                 # Simulation automation
├── coverage/
│   └── parse_coverage.py        # Python coverage log parser
├── dashboard/
│   └── generate_dashboard.py    # HTML dashboard generator
├── .github/
│   └── workflows/
│       └── regression.yml       # GitHub Actions CI/CD pipeline
└── README.md

'''

## 🧪 Test Cases

| Test | Description | Status |
|------|-------------|--------|
| Fill FIFO | Write until FULL flag asserts | ✅ PASS |
| Overflow Protection | Write when FULL is ignored | ✅ PASS |
| Drain FIFO | Read until EMPTY flag asserts | ✅ PASS |
| Underflow Protection | Read when EMPTY is ignored | ✅ PASS |
| Simultaneous RD/WR | Concurrent read and write | ✅ PASS |

---

## 📊 Coverage Results

| Coverage Type | Result |
|---------------|--------|
| Functional Coverage | 98%+ |
| Full Flag | ✅ Covered |
| Empty Flag | ✅ Covered |
| Write Enable | ✅ Covered |
| Read Enable | ✅ Covered |

---

## 🚀 How to Run Locally

### Prerequisites
```bash
# Install Icarus Verilog
sudo apt-get install iverilog   # Linux
brew install icarus-verilog     # Mac
```

### Run Everything
```bash
cd sim
make all
```

### Run Steps Individually
```bash
make compile    # Compile RTL + Testbench
make simulate   # Run simulation
make coverage   # Parse coverage report
make clean      # Clean generated files
```

### Generate Dashboard
```bash
python3 dashboard/generate_dashboard.py
# Open dashboard/index.html in your browser
```

---

## ⚙️ CI/CD Pipeline

Every push to `main` automatically:
Push to GitHub
↓
Install Icarus Verilog
↓
Compile RTL + Testbench
↓
Run Simulation
↓
Parse Coverage Log
↓
Generate HTML Dashboard
↓
Upload Dashboard Artifact

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| SystemVerilog | RTL Design & Testbench |
| Icarus Verilog | Open-source Simulator |
| Python 3.10 | Coverage parsing & Dashboard |
| GitHub Actions | CI/CD Automation |
| GTKWave | Waveform Viewing |
| Make | Build Automation |

---

## 👩‍💻 Author

**Sindhu Govindareddy Doddamane**  
Design Verification Engineer  
📧 sindhug6472@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/sindhu-govindareddy-doddamane-801300237)  
🐙 [GitHub](https://github.com/Sindhugd6472)

---

## 📄 License
MIT License — free to use and modify.
