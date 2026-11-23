import re
import subprocess
import sys
import unittest

from simulator import format_report, simulate


class SimulatorTests(unittest.TestCase):
    def test_seed_reproduces_history(self):
        self.assertEqual(simulate(42), simulate(42))
        self.assertNotEqual(simulate(42), simulate(43))

    def test_reports_cover_every_century_and_keep_snapshots(self):
        reports = simulate(42)
        self.assertEqual([(r.start_year, r.end_year) for r in reports],
                         [(year - 99, year) for year in range(100, 1001, 100)])
        self.assertTrue(all(report.cities for report in reports))
        self.assertTrue(all(len(report.records) >= 10 for report in reports))
        for report in reports:
            for record in report.records:
                year = int(re.match(r"Year (\d+):", record).group(1))
                self.assertLessEqual(report.start_year, year)
                self.assertLessEqual(year, report.end_year)
            self.assertTrue(all(event in report.records for event in report.wars))
            self.assertTrue(all(event in report.records for event in report.discoveries))
            self.assertTrue(all(city.founded <= report.end_year for city in report.cities))
        self.assertTrue(any(report.wars for report in reports))
        self.assertTrue(any(report.discoveries for report in reports))
        first_population = reports[0].cities[0].population
        reports[-1].cities[0].population += 1
        self.assertEqual(reports[0].cities[0].population, first_population)

    def test_report_and_cli_include_requested_sections(self):
        text = format_report(simulate(0)[0])
        for heading in ("Government", "Economy", "Cities and religions",
                        "Technologies", "Discoveries", "Wars", "Historical records"):
            self.assertIn(heading, text)
        output = subprocess.check_output(
            [sys.executable, "simulator.py", "--seed", "0"], text=True
        )
        self.assertEqual(output.count("=== Years "), 10)
        self.assertIn("=== Years 901-1000 ===", output)


if __name__ == "__main__":
    unittest.main()
