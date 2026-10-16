import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RegressionExitTests(unittest.TestCase):
    def test_simulator_failure_is_not_masked_by_logging(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / 'jobs.json'
            config.write_text(json.dumps({'jobs': [{'name': 'bad', 'compile': f'{sys.executable} -c "pass"', 'run': f'{sys.executable} -c "import sys; print(\'failure details\'); sys.exit(7)"', 'log': str(root / 'run.log')}]}))
            result = subprocess.run([sys.executable, str(ROOT / 'tools/run_regression.py'), '--config', str(config)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('failure details', (root / 'run.log').read_text())

    def test_empty_log_is_not_a_passing_regression(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'run.log').write_text('simulator stopped before testing\n')
            result = subprocess.run([sys.executable, str(ROOT / 'coverage/parse_coverage.py'), str(root / 'run.log'), '--output', str(root / 'report.json'), '--fail-on-test-failure'], capture_output=True)
            self.assertEqual(result.returncode, 1)
