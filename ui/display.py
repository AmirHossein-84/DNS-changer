import os
import sys
from typing import Any, Dict, List, Optional
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


def init_console_window(target_cols: int = 120, target_lines: int = 34):
    """
    Initializes terminal window geometry and font size for clean, single-screen rendering.
    """
    if sys.platform == "win32":
        try:
            os.system(f"mode con: cols={target_cols} lines={target_lines}")
        except Exception:
            pass
        adjust_console_font(target_height=18)
    elif sys.platform == "darwin":
        try:
            sys.stdout.write(f"\x1b[8;{target_lines};{target_cols}t")
            sys.stdout.flush()
        except Exception:
            pass


def adjust_console_font(target_height: int = 18):
    """
    Slightly increases the console font size proportionally (height=18pt)
    while preserving the active font face and aspect ratio.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes

        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        class CONSOLE_FONT_INFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * 32),
            ]

        STD_OUTPUT_HANDLE = -11
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        font_info = CONSOLE_FONT_INFOEX()
        font_info.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)

        if ctypes.windll.kernel32.GetCurrentConsoleFontEx(handle, False, ctypes.byref(font_info)):
            font_info.dwFontSize.X = 0
            font_info.dwFontSize.Y = target_height
            ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, False, ctypes.byref(font_info))
        else:
            font_info.FaceName = "Consolas"
            font_info.dwFontSize.X = 0
            font_info.dwFontSize.Y = target_height
            font_info.FontFamily = 54
            font_info.FontWeight = 400
            ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, False, ctypes.byref(font_info))
    except Exception:
        pass


def clear_screen():
    """Clears the console screen cleanly."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Renders the top branding banner in a compact format."""
    banner_text = Text()
    banner_text.append("⚡ DNS CHANGER PRO ⚡", style="bold cyan")
    banner_text.append("   Instant 1-Step DNS Switcher • Windows Native", style="dim white")

    panel = Panel(
        Align.center(banner_text),
        box=ROUNDED,
        border_style="cyan",
        padding=(0, 1),
    )
    console.print(panel)


def print_status_card(
    adapter_name: str,
    current_dns: Dict[str, any],
    provider_name: Optional[str] = None,
    is_elevated: bool = True,
    previous_dns: Optional[Dict[str, any]] = None,
):
    """
    Renders a compact, clean live status panel displaying current network, DNS state, and undo info.
    """
    table = Table.grid(padding=(0, 3), expand=True)
    table.add_column(justify="left")
    table.add_column(justify="right")

    icon = "📶" if "wi-fi" in adapter_name.lower() or "wireless" in adapter_name.lower() else "🔌"
    adapter_str = f"{icon} [bold cyan]{adapter_name}[/bold cyan]"
    admin_str = (
        "[bold green]🛡️ Administrator[/bold green]"
        if is_elevated
        else "[bold red]⚠️ Standard User (Elevation Recommended)[/bold red]"
    )
    table.add_row(f"[bold white]Interface:[/bold white] {adapter_str}", f"[bold white]Privileges:[/bold white] {admin_str}")

    servers = current_dns.get("servers", [])
    is_router_default = current_dns.get("is_router_default", False)

    if not servers or (is_router_default and not provider_name):
        dns_display = "[italic yellow]Automatic (DHCP / Router Default)[/italic yellow]"
    else:
        dns_display = "  |  ".join(f"[bold green]{ip}[/bold green]" for ip in servers)

    profile_str = f"✨ [bold magenta]{provider_name}[/bold magenta]" if provider_name else ("[dim]Router Default[/dim]" if is_router_default else "[dim]Custom Profile[/dim]")
    table.add_row(f"[bold white]Configured DNS:[/bold white] {dns_display}", f"[bold white]Profile:[/bold white] {profile_str}")

    if previous_dns and previous_dns.get("servers"):
        prev_str = ", ".join(previous_dns["servers"])
        table.add_row(f"[bold yellow]Previous DNS:[/bold yellow] [dim cyan]{prev_str}[/dim cyan]", "[dim yellow](Press [U] to revert)[/dim yellow]")

    panel = Panel(
        table,
        title="[bold yellow]📡 Live System Status[/bold yellow]",
        box=ROUNDED,
        border_style="blue",
        padding=(0, 1),
    )
    console.print(panel)


def print_quick_dns_grid(providers: List[Dict[str, str]], favorites: Optional[List[str]] = None):
    """
    Renders all DNS servers in a clean, strictly single-line 6-column grid with zero wrapping.
    """
    if favorites is None:
        favorites = []

    table = Table(
        box=ROUNDED,
        border_style="bright_blue",
        header_style="bold yellow",
        expand=True,
    )

    table.add_column("#", justify="right", style="bold cyan", no_wrap=True)
    table.add_column("Provider Name", style="bold white", no_wrap=True, ratio=3)
    table.add_column("Primary IP", style="green", no_wrap=True, ratio=2)
    table.add_column("#", justify="right", style="bold cyan", no_wrap=True)
    table.add_column("Provider Name", style="bold white", no_wrap=True, ratio=3)
    table.add_column("Primary IP", style="green", no_wrap=True, ratio=2)

    half = (len(providers) + 1) // 2
    for i in range(half):
        p1 = providers[i]
        idx1 = i + 1
        star1 = "⭐ " if p1["name"] in favorites else ""
        name1 = f"{star1}{p1['name']}"

        idx2_num = i + half
        if idx2_num < len(providers):
            p2 = providers[idx2_num]
            idx2 = idx2_num + 1
            star2 = "⭐ " if p2["name"] in favorites else ""
            name2 = f"{star2}{p2['name']}"

            table.add_row(
                f"{idx1}.",
                name1,
                p1["dns1"],
                f"{idx2}.",
                name2,
                p2["dns1"],
            )
        else:
            table.add_row(
                f"{idx1}.",
                name1,
                p1["dns1"],
                "",
                "",
                "",
            )

    console.print(table)

    # Clean, balanced hotkey footer
    hotkey_text = Text()
    hotkey_text.append("0. Reset DHCP", style="bold green")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[U] Undo", style="bold yellow")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[P] Fav Pin", style="bold yellow")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[C] Current DNS", style="bold green")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[L] Leak Test", style="bold magenta")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[B] Benchmark", style="bold cyan")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[M] Custom", style="bold cyan")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[S] Adapter", style="bold cyan")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[F] Flush", style="bold cyan")
    hotkey_text.append("  •  ", style="dim white")
    hotkey_text.append("[Q] Exit", style="bold red")

    console.print(
        Panel(
            Align.center(hotkey_text),
            box=SIMPLE_HEAVY,
            border_style="yellow",
            padding=(0, 1),
        )
    )


def print_current_dns_inspector(adapter_name: str, current_dns: Dict[str, any], match_info: Optional[Dict[str, any]]):
    """
    Renders a dedicated details card for current active DNS configuration and preset match.
    """
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold white", justify="right")
    table.add_column()

    icon = "📶" if "wi-fi" in adapter_name.lower() or "wireless" in adapter_name.lower() else "🔌"
    table.add_row("Network Adapter:", f"{icon} [bold cyan]{adapter_name}[/bold cyan]")

    servers = current_dns.get("servers", [])
    is_router_default = current_dns.get("is_router_default", False)
    is_static = current_dns.get("is_static", False)

    if match_info:
        dns_str = "  |  ".join(f"[bold green]{ip}[/bold green]" for ip in servers)
        table.add_row("DNS Configuration:", "[bold green]Active DNS Profile[/bold green]")
        table.add_row("Server IP(s):", dns_str)
        table.add_row("Provider Name:", f"✨ [bold magenta]{match_info['name']}[/bold magenta]")
        table.add_row("Preset Number:", f"[bold yellow]Preset #{match_info['index']}[/bold yellow]")
        table.add_row("Category:", f"[cyan]{match_info.get('category', 'General')}[/cyan]")
        if match_info.get("badge"):
            table.add_row("Badge:", f"[dim cyan]{match_info['badge']}[/dim cyan]")
        if match_info.get("desc"):
            table.add_row("Description:", f"[dim white]{match_info['desc']}[/dim white]")
    elif not servers or is_router_default:
        table.add_row("DNS Configuration:", "[italic yellow]Automatic (DHCP / Router Default)[/italic yellow]")
        table.add_row("Server IP(s):", "[dim]Assigned automatically by local router/gateway[/dim]")
        table.add_row("Matching Preset:", "[dim]None (Default DHCP)[/dim]")
    else:
        dns_str = "  |  ".join(f"[bold green]{ip}[/bold green]" for ip in servers)
        config_type = "Static IPv4 DNS" if is_static else "DHCP Assigned DNS"
        table.add_row("DNS Configuration:", f"[bold green]{config_type}[/bold green]")
        table.add_row("Server IP(s):", dns_str)
        table.add_row("Matching Preset:", "[dim yellow]Custom / Unrecognized Provider[/dim yellow]")

    console.print()
    console.print(
        Panel(
            table,
            title="[bold yellow]🔍 Active DNS Configuration Inspector[/bold yellow]",
            box=ROUNDED,
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


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

    table.add_column("#", justify="center", style="dim", width=4)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Provider Name", style="bold white", no_wrap=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Primary DNS", style="green", no_wrap=True)
    table.add_column("Secondary DNS", style="dim green", no_wrap=True)
    table.add_column("Latency", justify="right", width=12)

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


def print_leak_test_report(report: Dict[str, Any]):
    """
    Displays the DNS leak, hijack, and tampering audit security report.
    """
    score = report.get("security_score", "SECURE")
    if score == "SECURE":
        badge = "[bold green]🛡️ SECURE (Clean & Untampered)[/bold green]"
        border_color = "green"
    elif score == "WARNING":
        badge = "[bold yellow]⚠️ WARNING (NXDOMAIN Hijacking Detected)[/bold yellow]"
        border_color = "yellow"
    else:
        badge = "[bold red]🔴 COMPROMISED (DNS Interception / Tampering Detected)[/bold red]"
        border_color = "red"

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold white", justify="right")
    table.add_column()

    table.add_row("Target Adapter:", f"[bold cyan]{report['adapter']}[/bold cyan]")
    servers_str = ", ".join(report.get("configured_dns", [])) or "None / DHCP"
    table.add_row("Configured DNS:", f"[bold green]{servers_str}[/bold green]")
    table.add_row("Security Posture:", badge)

    resp_str = "[bold green]✔ Yes[/bold green]" if report["resolver_responsive"] else "[bold red]✖ No Response[/bold red]"
    table.add_row("Resolver Responsive:", resp_str)

    nx_str = (
        f"[bold red]✖ Hijacked! (Injected: {', '.join(report['nxdomain_details'] or [])})[/bold red]"
        if report["nxdomain_hijacked"]
        else "[bold green]✔ Clean (Standard NXDOMAIN behavior)[/bold green]"
    )
    table.add_row("NXDOMAIN Hijacking:", nx_str)

    tamper_str = (
        "[bold red]✖ Tampered! (Known queries rewritten)[/bold red]"
        if report["tampering_detected"]
        else "[bold green]✔ Clean (Authentic query results)[/bold green]"
    )
    table.add_row("Domain Tampering:", tamper_str)

    if report.get("warnings"):
        table.add_row("", "")
        table.add_row("[bold yellow]Details & Notes:[/bold yellow]", "")
        for w in report["warnings"]:
            table.add_row("•", f"[dim yellow]{w}[/dim yellow]")

    console.print()
    console.print(
        Panel(
            table,
            title="[bold cyan]🕵️ DNS Leak & Security Audit Report[/bold cyan]",
            box=ROUNDED,
            border_style=border_color,
            padding=(1, 2),
        )
    )
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
