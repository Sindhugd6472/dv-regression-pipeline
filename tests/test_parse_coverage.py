import tempfile
import unittest
from pathlib import Path

from coverage.parse_coverage import parse_results


class ParseCoverageTests(unittest.TestCase):
    def test_parses_pass_fail_and_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "sim.log"
            log.write_text(
                "PASS: reset test\n"
                "FAIL: overflow test\n"
                "Functional Coverage: 98.50%\n",
                encoding="utf-8",
            )

            results = parse_results(log, "fifo")

            self.assertEqual(results["design_name"], "fifo")
            self.assertEqual(results["summary"], {"passed": 1, "failed": 1, "total": 2})
            self.assertEqual(results["coverage"], 98.5)

    def test_missing_log_raises(self):
        with self.assertRaises(FileNotFoundError):
            parse_results(Path("/definitely/missing.log"), "fifo")


if __name__ == "__main__":
    unittest.main()
