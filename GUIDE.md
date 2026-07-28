# FortiToolbox — User Guide

Written for operators: each section contains only what you need.

## Connection

- **Connect** opens the connection dialog. **Demo mode** uses a simulated device for demos and testing. For a real device, enter the host, read-only username, and password; press **Enter** to connect.
- The app runs one bounded, read-only command to detect whether the account profile includes `system-diagnostics enable`. If diagnose access is unavailable, those checks are marked SKIPPED; you can override the result later by clicking the `diagnose: OFF` chip in the top bar.
- On multi-VDOM devices, use the VDOM selector to choose the active VDOM (default: `root`). Per-VDOM checks run there; global checks run in the global context.
- The top bar shows the model, version, **masked serial number**, and hostname.

## Dashboard and checks

- Run **Quick health**, **Full sweep**, **Run all in <tab>**, or the **▶** button on an individual check.
- Click a FAIL/WARN/PASS/INFO counter to filter cards across all tabs. Click **Show all** to clear the filter.
- Each card contains a status indicator, a conclusion, the metric that matters, and collapsible raw output.

## Copy for LLM

Click **Copy for LLM** to obfuscate all output and copy it in a form ready to paste into an LLM. Serial numbers, IP addresses, MAC addresses, hostnames, and email addresses become reversible tokens; secrets are removed. Enable **mask** to show discarded secret fields as `<SECRET_n>`. Copying is blocked if the leak check fails.

## PDF report

Click **Report** to generate a PDF containing the masked device identity, verdict summary, and all checks grouped by module. It is suitable for attaching to a ticket or delivering to a customer.

## SSH console

Click **Console** to open the right-hand panel and run live commands against the device. Console output is raw and **not obfuscated**, as the warning banner explains. Available actions are Send, Ctrl-C, Kill debug, Clear, and **Obfuscate & copy**. The console uses a dedicated channel and does not interfere with checks.

## Advanced — Debug Flow

1. Enter a target IP address, port, and/or protocol on one line, such as `tcp,443,1.1.1.1`. Without an interface, the active VDOM context is used. The default packet count is 10.
2. Click **Run flow** to start a live capture with a counter and **Stop** button. Debug state is always cleaned up.
3. Results show conclusions first, such as an RPF drop caused by a missing return route. The IN→ROUTE→POLICY→NAT→UTM→OUT pipeline shows only stages that occurred, with drops highlighted in red. Per-packet steps and raw output are also available.
4. Use **Live session** to inspect NAT, offload, and byte counters for the tuple; **Sniff this flow** to prefill the packet sniffer; or **Copy for LLM** to export safely.

## Advanced — Packet Sniffer

1. Enter a smart filter such as `wan1 tcp 443` or `tcp,443,8.8.8.8`. Without an interface, all interfaces are used. The default maximum is 5,000 packets and can be changed.
2. Click **Capture** to start a live capture with a **Stop** button. Each packet is summarized by time, interface, source, destination, and protocol details; expand it to view hexadecimal data.
3. Click **Download .pcap** and open the file in Wireshark.

## Advanced — Authentication Test

1. Click **Load servers**, then choose a protocol and server. RADIUS adds a scheme selector for PAP, CHAP, MSCHAP, or MSCHAPv2.
2. Enter a username and password. The password is masked and never stored.
3. Click **Test auth** to see the result, returned groups, and conclusions. Enable **fnbamd verbose** for detailed negotiation output. SAML cannot be tested through the CLI.
