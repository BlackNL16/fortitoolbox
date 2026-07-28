"""Regression tests for FortiGate SSH command execution."""

import unittest

from fortitoolbox.connectors.ssh import SSHConnector


class _FakeConnection:
    def __init__(self):
        self.calls = []
        self.timing_calls = []

    def send_command(self, command, **kwargs):
        self.calls.append((command, kwargs))
        return f"{command}\nresult\nFortiGate #"

    def send_command_timing(self, command, **kwargs):
        self.timing_calls.append((command, kwargs))
        return f"{command}\nresult\nFortiGate #"


class SSHConnectorTests(unittest.TestCase):
    def setUp(self):
        self.connector = SSHConnector("fortigate.example", "readonly", "secret")
        self.connection = _FakeConnection()
        self.connector._conn = self.connection

    def test_read_command_does_not_require_command_echo(self):
        result = self.connector.run("get system status")

        self.assertIn("result", result)
        self.assertFalse(self.connection.calls[0][1]["cmd_verify"])

    def test_scoped_commands_disable_echo_verification(self):
        self.connector._vdom_mode = True

        self.connector.run("get system status", scope="vdom", vdom="root")

        self.assertEqual(
            ["config vdom", "edit root", "get system status", "end"],
            [command for command, _ in self.connection.calls],
        )
        self.assertTrue(
            all(kwargs["cmd_verify"] is False for _, kwargs in self.connection.calls)
        )

    def test_connection_probes_use_short_timeouts(self):
        self.connector.probe_sysdiag()
        self.connector.device_info()

        self.assertEqual(3, self.connection.timing_calls[0][1]["read_timeout"])
        self.assertEqual(15, self.connection.calls[0][1]["read_timeout"])


if __name__ == "__main__":
    unittest.main()
