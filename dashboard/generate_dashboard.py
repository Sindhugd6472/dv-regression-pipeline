# Coverage Dashboard Generator
# Reads coverage_report.json and generates HTML dashboard
# Author: Sindhu Govindareddy Doddamane

import json
import os

def load_report(json_file="coverage/coverage_report.json"):
    """Load coverage report from JSON"""
    if not os.path.exists(json_file):
        print(f"ERROR: '{json_file}' not found! Run simulation first.")
        return None
    with open(json_file, 'r') as f:
        return json.load(f)

def generate_dashboard(results):
    """Generate HTML dashboard from results"""

    passed  = results["summary"]["passed"]
    failed  = results["summary"]["failed"]
    total   = results["summary"]["total"]
    coverage = results["coverage"]

    # Build test rows
    test_rows = ""
    for test in results["tests"]:
        icon   = "✅" if test["status"] == "PASS" else "❌"
        color  = "#d4edda" if test["status"] == "PASS" else "#f8d7da"
        test_rows += f"""
        <tr style="background:{color}">
            <td>{icon}</td>
            <td>{test['name']}</td>
            <td><b>{test['status']}</b></td>
        </tr>"""

    # Coverage bar color
    if coverage >= 90:
        bar_color = "#28a745"
    elif coverage >= 70:
        bar_color = "#ffc107"
    else:
        bar_color = "#dc3545"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DV Regression Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 30px;
        }}
        h1 {{
            text-align: center;
            color: #58a6ff;
            font-size: 2em;
            margin-bottom: 5px;
        }}
        .subtitle {{
            text-align: center;
            color: #8b949e;
            margin-bottom: 30px;
            font-size: 0.95em;
        }}
        .cards {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 35px;
            flex-wrap: wrap;
        }}
        .card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px 35px;
            text-align: center;
            min-width: 160px;
        }}
        .card h2 {{
            font-size: 2.5em;
            margin-bottom: 5px;
        }}
        .card p {{
            color: #8b949e;
            font-size: 0.9em;
        }}
        .green {{ color: #3fb950; }}
        .red   {{ color: #f85149; }}
        .blue  {{ color: #58a6ff; }}

        .coverage-section {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px;
            max-width: 700px;
            margin: 0 auto 35px auto;
        }}
        .coverage-section h3 {{
            color: #58a6ff;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        .bar-bg {{
            background: #21262d;
            border-radius: 50px;
            height: 28px;
            width: 100%;
        }}
        .bar-fill {{
            background: {bar_color};
            height: 28px;
            border-radius: 50px;
            width: {coverage}%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            font-weight: bold;
            font-size: 0.9em;
            color: white;
            transition: width 1s ease;
        }}

        .table-section {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px;
            max-width: 700px;
            margin: 0 auto;
        }}
        .table-section h3 {{
            color: #58a6ff;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}
        th {{
            background: #21262d;
            padding: 12px;
            text-align: left;
            color: #8b949e;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #21262d;
            color: #333;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #8b949e;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>

    <h1>🔬 DV Regression Dashboard</h1>
    <p class="subtitle">{results.get('design_name', 'Design').upper()} Verification | Sindhu Govindareddy Doddamane</p>

    <!-- Summary Cards -->
    <div class="cards">
        <div class="card">
            <h2 class="blue">{total}</h2>
            <p>Total Tests</p>
        </div>
        <div class="card">
            <h2 class="green">{passed}</h2>
            <p>Passed</p>
        </div>
        <div class="card">
            <h2 class="red">{failed}</h2>
            <p>Failed</p>
        </div>
        <div class="card">
            <h2 class="{'green' if coverage >= 90 else 'red'}">{coverage:.1f}%</h2>
            <p>Coverage</p>
        </div>
    </div>

    <!-- Coverage Bar -->
    <div class="coverage-section">
        <h3>📊 Functional Coverage</h3>
        <div class="bar-bg">
            <div class="bar-fill">{coverage:.1f}%</div>
        </div>
    </div>

    <!-- Test Results Table -->
    <div class="table-section">
        <h3>📋 Test Results</h3>
        <table>
            <tr>
                <th>Status</th>
                <th>Test Name</th>
                <th>Result</th>
            </tr>
            {test_rows}
        </table>
    </div>

    <div class="footer">
        <p>Generated by DV Regression Pipeline | github.com/Sindhugd6472</p>
    </div>

</body>
</html>"""

    output_file = "dashboard/index.html"
    with open(output_file, 'w') as f:
        f.write(html)
    print(f"🎨 Dashboard generated: {output_file}")
    print(f"👉 Open it in your browser to view!")


if __name__ == "__main__":
    results = load_report()
    if results:
        generate_dashboard(results)
