import argparse
import sys
import time
from typing import List, Optional
from core import benchmark, leak_test, network, storage
from ui.display import console


def create_parser() -> argparse.ArgumentParser:
    """Configures the command-line interface arguments."""
    parser = argparse.ArgumentParser(
        prog="DNS-Changer",
        description="⚡ DNS Changer Pro - High-Speed Terminal DNS Switcher for Windows",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--set",
        "-s",
        metavar="TARGET",
        help="Apply DNS by Preset Number (e.g. 1), Name (e.g. 'electro', 'shecan'), or IP ('1.1.1.1,1.0.0.1')",
    )
    parser.add_argument(
        "--auto-best",
        "-a",
        action="store_true",
        help="Silently benchmark all DNS servers and auto-connect to the lowest latency provider",
    )
    parser.add_argument(
        "--clear",
        "--dhcp",
        "-c",
        action="store_true",
        help="Reset network adapter DNS back to Automatic (DHCP) and flush cache",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display current network adapter, configured DNS IPs, and active provider profile",
    )
    parser.add_argument(
        "--leak-test",
        "-t",
        action="store_true",
        help="Run DNS leak, NXDOMAIN hijack, and query tampering security audit",
    )
    parser.add_argument(
        "--flush",
        "-f",
        action="store_true",
        help="Flush Windows DNS resolver cache (ipconfig /flushdns)",
    )
    parser.add_argument(
        "--benchmark",
        "-b",
        action="store_true",
        help="Run high-speed concurrent UDP DNS latency benchmark across all providers",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available DNS presets and custom profiles",
    )
    parser.add_argument(
        "--adapter",
        metavar="NAME",
        help="Target a specific network adapter name (e.g. 'Wi-Fi' or 'Ethernet')",
    )
    return parser


def handle_cli(args: Optional[List[str]] = None) -> bool:
    """
    Parses CLI arguments.
    Returns True if a CLI command was processed (application should exit).
    Returns False if no CLI flags were passed (launch interactive TUI).
    """
    parser = create_parser()
    parsed, unknown = parser.parse_known_args(args)

    # Check if any actionable flag was supplied
    has_flags = any([
        parsed.set,
        parsed.auto_best,
        parsed.clear,
        parsed.status,
        parsed.leak_test,
        parsed.flush,
        parsed.benchmark,
        parsed.list,
    ])

    if not has_flags:
        return False

    # Check admin privileges for modifying actions
    requires_admin = parsed.set or parsed.auto_best or parsed.clear or parsed.flush
    if requires_admin and not network.is_admin():
        if not network.elevate_privileges():
            console.print("[bold red]❌ Error: Administrator privileges required to change DNS settings.[/bold red]")
            sys.exit(1)
        return True

    # Identify target adapter
    adapters, auto_primary, dns_configs = network.get_all_adapters_and_config()
    target_adapter = parsed.adapter or auto_primary
    if not target_adapter:
        if adapters:
            target_adapter = adapters[0]["name"]
        else:
            console.print("[bold red]❌ Error: No network adapters detected on this machine.[/bold red]")
            sys.exit(1)

    # 1. Flush Cache
    if parsed.flush:
        ok, msg = network.flush_dns_cache()
        if ok:
            console.print(f"[bold green]✔ {msg}[/bold green]")
            sys.exit(0)
        else:
            console.print(f"[bold red]❌ {msg}[/bold red]")
            sys.exit(1)

    # 2. Reset / Clear to DHCP
    if parsed.clear:
        # Save previous state for undo
        cur_dns = dns_configs.get(target_adapter) or network.get_current_dns(target_adapter)
        storage.save_previous_dns(target_adapter, cur_dns)

        ok, msg = network.clear_dns(target_adapter)
        if ok:
            console.print(f"[bold green]✔ DNS reset to Automatic (DHCP) for '{target_adapter}' & cache flushed.[/bold green]")
            sys.exit(0)
        else:
            console.print(f"[bold red]❌ {msg}[/bold red]")
            sys.exit(1)

    # 3. Status
    if parsed.status:
        cur_dns = dns_configs.get(target_adapter) or network.get_current_dns(target_adapter)
        provider_name = storage.identify_dns_provider(cur_dns.get("servers", [])) or "Custom / Automatic"
        dhcp_str = "DHCP (Automatic)" if cur_dns.get("is_dhcp") else "Static"
        servers_str = ", ".join(cur_dns.get("servers", [])) or "None (Router Default)"

        console.print(f"[bold cyan]Adapter:  [/bold cyan] [bold white]{target_adapter}[/bold white]")
        console.print(f"[bold cyan]Status:   [/bold cyan] [bold yellow]{dhcp_str}[/bold yellow]")
        console.print(f"[bold cyan]Servers:  [/bold cyan] [bold green]{servers_str}[/bold green]")
        console.print(f"[bold cyan]Profile:  [/bold cyan] [bold magenta]{provider_name}[/bold magenta]")
        sys.exit(0)

    # 4. Leak Test
    if parsed.leak_test:
        from ui import display
        cur_dns = dns_configs.get(target_adapter) or network.get_current_dns(target_adapter)
        console.print(f"[bold cyan]🕵️ Auditing DNS integrity and leak posture on '{target_adapter}'...[/bold cyan]")
        report = leak_test.run_dns_leak_audit(target_adapter, cur_dns.get("servers", []))
        display.print_leak_test_report(report)
        sys.exit(0)

    # 5. List Presets
    if parsed.list:
        from ui import display
        providers = storage.get_all_providers()
        display.print_quick_dns_grid(providers)
        sys.exit(0)

    # 6. Benchmark Only
    if parsed.benchmark:
        from ui import display
        providers = storage.get_all_providers()
        console.print(f"[bold cyan]🚀 Benchmarking {len(providers)} DNS servers...[/bold cyan]")
        results = benchmark.run_benchmark(providers, max_workers=26)
        display.print_benchmark_table(results)
        sys.exit(0)

    # 7. Auto-Best DNS
    if parsed.auto_best:
        providers = storage.get_all_providers()
        console.print("[bold cyan]🚀 Benchmarking all DNS servers for best latency...[/bold cyan]")
        results = benchmark.run_benchmark(providers, max_workers=26)
        valid_results = [r for r in results if r["status"] == "ok" and r["best_latency"] is not None]

        if not valid_results:
            console.print("[bold red]❌ No DNS servers responded successfully to UDP query benchmark.[/bold red]")
            sys.exit(1)

        fastest = valid_results[0]
        target = fastest["provider"]

        # Save previous state for undo
        cur_dns = dns_configs.get(target_adapter) or network.get_current_dns(target_adapter)
        storage.save_previous_dns(target_adapter, cur_dns)

        ok, msg = network.set_dns(
            target_adapter,
            target["dns1"],
            target.get("dns2"),
            ipv6_1=target.get("ipv6_1"),
            ipv6_2=target.get("ipv6_2"),
        )
        if ok:
            console.print(
                f"[bold green]✔ Auto-Connected to Fastest: [bold white]{target['name']}[/bold white] "
                f"({fastest['best_latency']} ms) on [bold cyan]{target_adapter}[/bold cyan] & cache flushed.[/bold green]"
            )
            sys.exit(0)
        else:
            console.print(f"[bold red]❌ {msg}[/bold red]")
            sys.exit(1)

    # 8. Set Specific DNS
    if parsed.set:
        providers = storage.get_all_providers()
        target = storage.find_provider_by_query(parsed.set, providers)
        if not target:
            console.print(f"[bold red]❌ Error: Could not find any DNS preset or valid IP matching '{parsed.set}'.[/bold red]")
            sys.exit(1)

        # Save previous state for undo
        cur_dns = dns_configs.get(target_adapter) or network.get_current_dns(target_adapter)
        storage.save_previous_dns(target_adapter, cur_dns)

        ok, msg = network.set_dns(
            target_adapter,
            target["dns1"],
            target.get("dns2"),
            ipv6_1=target.get("ipv6_1"),
            ipv6_2=target.get("ipv6_2"),
        )
        if ok:
            sec_str = f", {target['dns2']}" if target.get("dns2") else ""
            console.print(
                f"[bold green]✔ Applied [bold white]{target['name']}[/bold white] "
                f"({target['dns1']}{sec_str}) on [bold cyan]{target_adapter}[/bold cyan] & cache flushed.[/bold green]"
            )
            sys.exit(0)
        else:
            console.print(f"[bold red]❌ {msg}[/bold red]")
            sys.exit(1)

    return True
