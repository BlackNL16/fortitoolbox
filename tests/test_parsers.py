"""Regression tests for the catalog-to-parser diagnostic pipeline."""

import unittest

from fortitoolbox.connectors.mock import MockConnector
from fortitoolbox.engine import Engine
from fortitoolbox.parsers import get_parser
from fortitoolbox.verdict import Status


class ParserPipelineTests(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(MockConnector())
        self.engine.connect_and_probe()

    def tearDown(self):
        self.engine.close()

    def test_every_noninteractive_check_has_a_registered_parser(self):
        missing = [
            check["id"]
            for check in self.engine.selectable()
            if get_parser(check["id"]).__name__ == "_generic"
        ]
        self.assertEqual([], missing, f"Missing parsers: {', '.join(missing)}")

    def test_every_noninteractive_check_runs_against_mock_device(self):
        results = self.engine.run_many(
            [check["id"] for check in self.engine.selectable()]
        )
        failures = [
            f"{result.id}: {result.headline}"
            for result in results
            if result.status in {Status.ERROR, Status.SKIPPED}
        ]
        self.assertEqual([], failures, "Mock pipeline failures:\n" + "\n".join(failures))
        self.assertTrue(all(result.headline for result in results))

    def test_mock_device_preserves_representative_verdicts(self):
        expected = {
            "version_model": Status.PASS,
            "resources": Status.PASS,
            "certificates": Status.WARN,
            "ntp": Status.WARN,
            "config_error_log": Status.PASS,
        }
        actual = {
            check_id: self.engine.run_check(check_id).status
            for check_id in expected
        }
        self.assertEqual(expected, actual)

    def test_unknown_parser_uses_safe_generic_result(self):
        result = get_parser("not_in_catalog")(
            {"id": "not_in_catalog", "module": "Test", "title": "Unknown"},
            {"show example": "sample output"},
            self.engine.device,
        )
        self.assertEqual(Status.INFO, result.status)
        self.assertEqual("Captured", result.headline)


if __name__ == "__main__":
    unittest.main()
