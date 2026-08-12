import os
import sys
from typing import Dict, List, Optional
from rich.align import Align
from rich.box import ROUNDED, SIMPLE_HEAVY
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Configure standard streams for UTF-8 support on Windows
if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if sys.stderr and hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

console = Console(force_terminal=True)


def clear_screen():
    """Clears the console screen cleanly."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Renders the top branding banner."""
    banner_text = Text()
    banner_text.append("⚡ DNS CHANGER PRO ⚡\n", style="bold cyan")
    banner_text.append("Fast 1-Step DNS Switcher • Anti-Sanction & Gaming • Privacy", style="dim white")

    panel = Panel(
        Align.center(banner_text),
        box=ROUNDED,
        border_style="cyan",
        padding=(0, 2),
    )
    console.print(panel)


def print_status_card(
    adapter_name: str,
    current_dns: Dict[str, any],
    provider_name: Optional[str] = None,
    is_elevated: bool = True,
):
    """
    Renders an informative live status panel displaying current network and DNS state.
    """
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold white", justify="right")
    table.add_column()

    admin_badge = (
        "[bold green]🛡️ Administrator[/bold green]"
        if is_elevated
        else "[bold red]⚠️ Standard User (Elevation Recommended)[/bold red]"
    )
    table.add_row("Privileges:", admin_badge)

    icon = "📶" if "wi-fi" in adapter_name.lower() or "wireless" in adapter_name.lower() else "🔌"
    table.add_row("Active Interface:", f"{icon} [bold cyan]{adapter_name}[/bold cyan]")

    servers = current_dns.get("servers", [])
    is_dhcp = current_dns.get("is_dhcp", False)

    if not servers or is_dhcp:
        dns_display = "[italic yellow]Automatic (DHCP / Router Default)[/italic yellow]"
    else:
        dns_str = "  |  ".join(f"[bold green]{ip}[/bold green]" for ip in servers)
        dns_display = dns_str

    table.add_row("Configured DNS:", dns_display)

    if provider_name:
        table.add_row("Active Profile:", f"✨ [bold magenta]{provider_name}[/bold magenta]")
    elif not is_dhcp and servers:
        table.add_row("Active Profile:", "[dim]Custom / Unrecognized[/dim]")

    panel = Panel(
        table,
        title="[bold yellow]📡 Live System Status[/bold yellow]",
        box=ROUNDED,
        border_style="blue",
        padding=(0, 1),
    )
    console.print(panel)


def print_quick_dns_grid(providers: List[Dict[str, str]]):
    """
    Renders all DNS servers in a clean, high-visibility 2-column grid.
    """
    table = Table(
        box=ROUNDED,
        border_style="bright_blue",
        header_style="bold yellow",
        expand=True,
    )

    table.add_column("#", justify="right", style="bold cyan", no_wrap=True)
    table.add_column("Provider Name", style="bold white")
    table.add_column("Primary IP", style="green", no_wrap=True)
    table.add_column("#", justify="right", style="bold cyan", no_wrap=True)
    table.add_column("Provider Name", style="bold white")
    table.add_column("Primary IP", style="green", no_wrap=True)

    half = (len(providers) + 1) // 2
    for i in range(half):
        p1 = providers[i]
        idx1 = i + 1

        idx2_num = i + half
        if idx2_num < len(providers):
            p2 = providers[idx2_num]
            idx2 = idx2_num + 1
            table.add_row(
                f"{idx1}.",
                p1["name"],
                p1["dns1"],
                f"{idx2}.",
                p2["name"],
                p2["dns1"],
            )
        else:
            table.add_row(
                f"{idx1}.",
                p1["name"],
                p1["dns1"],
                "",
                "",
                "",
            )

    console.print(table)

    # DHCP reset & Hotkeys bar
    hotkey_table = Table.grid(expand=True, padding=(0, 1))
    hotkey_table.add_column(justify="left")
    hotkey_table.add_column(justify="right")

    hotkey_table.add_row(
        "[bold green]0. Reset to Automatic (DHCP)[/bold green]",
        "[bold cyan][B][/bold cyan] Benchmark Speed  •  [bold cyan][M][/bold cyan] Custom DNS  •  [bold cyan][S][/bold cyan] Switch Adapter  •  [bold cyan][F][/bold cyan] Flush  •  [bold red][Q][/bold red] Exit",
    )

    console.print(
        Panel(
            hotkey_table,
            box=SIMPLE_HEAVY,
            border_style="yellow",
            padding=(0, 1),
        )
    )


def print_benchmark_table(results: List[Dict[str, any]]):
    """
    Displays DNS benchmark results in a formatted Rich Table with colorized latency badges.
    """
    table = Table(
        title="🚀 DNS Query Benchmark Results (Fastest to Slowest)",
        box=ROUNDED,
        border_style="cyan",
        header_style="bold magenta",
        title_style="bold yellow",
    )

    table.add_column("#", justify="center", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Provider Name", style="bold white")
    table.add_column("Category", style="cyan")
    table.add_column("Primary DNS", style="green")
    table.add_column("Secondary DNS", style="dim green")
    table.add_column("Latency", justify="right")

    for i, res in enumerate(results, 1):
        status = res["status"]
        latency = res["best_latency"]

        if status == "ok" and latency is not None:
            if latency < 45:
                lat_str = f"[bold green]{latency} ms[/bold green]"
                badge = "⚡ FAST"
            elif latency < 100:
                lat_str = f"[bold yellow]{latency} ms[/bold yellow]"
                badge = "✔ OK"
            else:
                lat_str = f"[bold red]{latency} ms[/bold red]"
                badge = "⚠ SLOW"
        else:
            lat_str = "[dim red]Timed out[/dim red]"
            badge = "✖ FAIL"

        table.add_row(
            str(i),
            badge,
            res["name"],
            res["category"],
            res["dns1"],
            res["dns2"] or "-",
            lat_str,
        )

    console.print()
    console.print(table)
    console.print()


def print_success(message: str):
    """Prints a styled success alert."""
    console.print(f"\n[bold green]✔ SUCCESS:[/bold green] {message}\n")


def print_error(message: str):
    """Prints a styled error alert."""
    console.print(f"\n[bold red]✖ ERROR:[/bold red] {message}\n")


def print_warning(message: str):
    """Prints a styled warning alert."""
    console.print(f"\n[bold yellow]⚠ WARNING:[/bold yellow] {message}\n")


def print_info(message: str):
    """Prints a styled info alert."""
    console.print(f"\n[bold cyan]ℹ INFO:[/bold cyan] {message}\n")
