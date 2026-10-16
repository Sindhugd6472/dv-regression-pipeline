import os
from pathlib import Path
import tempfile
import unittest
from dashboard.generate_dashboard import generate_dashboard

class DashboardTests(unittest.TestCase):
    def test_log_text_is_escaped(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                Path("dashboard").mkdir()
                generate_dashboard({"design_name": "<img>", "summary": {"passed": 1,"failed": 0,"total": 1}, "coverage": 100, "tests": [{"name": "<script>alert(1)</script>","status": "PASS"}]})
                html = Path("dashboard/index.html").read_text()
                self.assertNotIn("<script>", html)
                self.assertIn("&lt;script&gt;", html)
                self.assertIn("&lt;IMG&gt;", html)
            finally:
                os.chdir(previous)
