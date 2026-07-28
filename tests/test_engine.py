"""Tests for connection lifecycle and capability handling."""

import unittest

from fortitoolbox.connectors.base import Connector, DeviceInfo
from fortitoolbox.engine import Engine


class _ProbeTrackingConnector(Connector):
    def __init__(self):
        self.probe_calls = 0

    def connect(self):
        pass

    def close(self):
        pass

    def run(self, command, scope=None, vdom=None, read_timeout=None):
        return ""

    def device_info(self):
        return DeviceInfo(model="FortiGate-Test", version="7.6")

    def probe_sysdiag(self):
        self.probe_calls += 1
        return True


class EngineConnectionTests(unittest.TestCase):
    def test_explicit_capability_skips_probe(self):
        connector = _ProbeTrackingConnector()
        engine = Engine(connector)

        device = engine.connect_and_probe(force_sysdiag=False)

        self.assertFalse(device.sysdiag_enabled)
        self.assertEqual(0, connector.probe_calls)

    def test_unspecified_capability_runs_probe(self):
        connector = _ProbeTrackingConnector()
        engine = Engine(connector)

        device = engine.connect_and_probe()

        self.assertTrue(device.sysdiag_enabled)
        self.assertEqual(1, connector.probe_calls)


if __name__ == "__main__":
    unittest.main()
