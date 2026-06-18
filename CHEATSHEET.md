# FortiToolbox — Command Cheat Sheet

These are the exact diagnostic commands used by each check, provided for manual use. On **multi-VDOM** devices, commands with `vdom` scope are wrapped in `config vdom → edit <vdom> → … → end`; commands with `global` scope are wrapped in `config global → … → end`. List VDOMs from the global context with `diagnose sys vd list`.

`[diag]` requires `system-diagnostics enable` in the administrator access profile.

## System & Health

| Check | Command | Detects |
|---|---|---|
| Version & model | `get system status` | Model, version, serial number, hostname, and clock |
| Resources & conserve | `get system performance status` | Memory, CPU, and conserve mode |
| Conserve (kernel + SHM) `[diag]` | `diagnose hardware sysinfo conserve` · `diagnose hardware sysinfo shm` | Kernel versus proxy/shared-memory conserve state |
| FortiGuard `[diag]` | `get system fortiguard` · `diagnose autoupdate versions` | FDS status and per-module licence expiry |
| HA `[diag]` | `get system ha status` · `diagnose sys ha checksum cluster` · `diagnose sys ha history read` | Out-of-sync members and recent failovers |
| NTP `[diag]` | `diagnose sys ntp status` | Clock synchronization |
| Crash log `[diag]` | `diagnose debug crashlog read` | Recent crashes |
| Configuration error log `[diag]` | `diagnose debug config-error-log read` | Configuration that was not fully applied |
| Certificates (per VDOM) | `get vpn certificate local detail` | Expiry within 30 days and certificate chain |
| Hardware/factory certificate `[diag]` | `diagnose hardware certificate` | Hardware certificate health |
| Sensors | `execute sensor list` | Temperature, fan, and PSU state |
| FortiAnalyzer | `execute log fortianalyzer test-connectivity` | Log delivery to FortiAnalyzer |

## Network

| Check | Command | Detects |
|---|---|---|
| Interfaces (NIC) | `get system interface physical` plus `diagnose hardware deviceinfo nic <port>` for each port | Addressed ports should be up, full duplex, and at expected speed |
| Routing | `get router info routing-table all` | Default route and blackhole routes |
| Dynamic routing | `get router info bgp summary` · `get router info ospf neighbor` | BGP and OSPF adjacencies |
| Sessions `[diag]` | `diagnose sys session full-stat` | Count, setup rate, clashes, and conserve drops |
| Interface errors `[diag]` | `diagnose netlink interface list` (management context, no wrapper) | RX/TX errors and drops |
| ARP | `get system arp` | Unresolved next hops |
| Policy routes `[diag]` | `diagnose firewall proute list` | Policy routes or SD-WAN rules overriding the routing table |

## SD-WAN `[diag]`

| Check | Command |
|---|---|
| Health check | `diagnose sys sdwan health-check` |
| Rules/path selection | `diagnose sys sdwan service4` |
| Members | `diagnose sys sdwan member` |
| SLA log (flaps) | `diagnose sys sdwan sla-log` |

## VPN

| Check | Command |
|---|---|
| IPsec summary | `get vpn ipsec tunnel summary` |
| IKE phase 1 `[diag]` | `diagnose vpn ike gateway list` |
| SSL-VPN | `get vpn ssl monitor` |
| IPsec traffic/SA `[diag]` | `diagnose vpn tunnel list` |

## Security / Policy `[diag]`

| Check | Command |
|---|---|
| Unused policies | `diagnose firewall iprope show 100004 0` |
| Web filter rating | `diagnose debug rating` |

## DNS

| Check | Command | Scope |
|---|---|---|
| DNS configuration | `get system dns` | Global |
| Server readiness | `diagnose test application dnsproxy 3` | **Global**; output contains per-VDOM details |
| Resolution | `execute ping update.fortiguard.net` | VDOM |

## Interactive tools (Advanced)

**Debug Flow** (per VDOM, bounded, with guaranteed cleanup):

```text
diagnose debug reset
diagnose debug flow filter addr <IP> / port <PORT> / proto <N>
diagnose debug flow show function-name enable
diagnose debug flow show iprope enable
diagnose debug flow trace start <N>
diagnose debug enable
  ... [capture] ...
diagnose debug flow trace stop
diagnose debug disable ; diagnose debug flow filter clear ; diagnose debug reset
```

**Packet Sniffer** (verbosity 6 captures full frames for `.pcap`):

```text
diagnose sniffer packet <iface|any> '<bpf>' 6 <count> a
# Stop with Ctrl-C
```

**Authentication test:**

```text
diagnose test authserver ldap    <server> <user> <pass>
diagnose test authserver tacacs+ <server> <user> <pass>
diagnose test authserver radius  <server> <pap|chap|mschap|mschap2> <user> <pass>
# Verbose: diagnose debug application fnbamd -1 ; diagnose debug enable
```

**Useful companion commands:**

```text
diagnose firewall iprope lookup <src> <sport> <dst> <dport> <proto> <iface> policy   # Find the matching policy without generating traffic
diagnose sys session filter dst <ip> ; diagnose sys session list                      # Find a live session by tuple
```
