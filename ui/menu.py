import re
import time
from typing import Dict, List, Optional
import questionary
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from core import benchmark, network, storage
from ui import display
from ui.display import console


IP_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?)$"
)


def validate_ip(val: str) -> bool:
    """Validates IPv4 string format."""
    return bool(IP_REGEX.match(val.strip()))


def handle_quick_input(providers: List[Dict[str, str]], active_adapter: str) -> str:
    """
    Prompts for fast single-step input:
    - Number (1..N): Sets DNS and returns 'exit_success' to auto-close.
    - Number 0: Resets DNS to DHCP and returns 'exit_success' to auto-close.
    - Hotkeys (B, M, S, F, Q): Launches respective tools or exits.
    """
    total = len(providers)
    try:
        raw = console.input(
            f"\n[bold cyan]👉 Enter DNS number [bold yellow][0-{total}][/bold yellow] or Hotkey [bold yellow](B/M/S/F/Q)[/bold yellow]: [/bold cyan]"
        ).strip()
    except (KeyboardInterrupt, EOFError):
        return "exit"

    if not raw:
        return "continue"

    # Check for digit selection
    if raw.isdigit():
        val = int(raw)
        if val == 0:
            ok, msg = network.clear_dns(active_adapter)
            if ok:
                display.print_success(f"DNS reset to Automatic (DHCP) for '{active_adapter}' & cache flushed!")
                return "exit_success"
            else:
                display.print_error(msg)
                time.sleep(2.0)
                return "continue"
        elif 1 <= val <= total:
            target = providers[val - 1]
            ok, msg = network.set_dns(active_adapter, target["dns1"], target.get("dns2"))
            if ok:
                display.print_success(
                    f"Applied [bold white]{target['name']}[/bold white] ({target['dns1']}"
                    + (f", {target['dns2']}" if target.get('dns2') else "")
                    + f") on [bold cyan]{active_adapter}[/bold cyan] & cache flushed!"
                )
                return "exit_success"
            else:
                display.print_error(msg)
                time.sleep(2.0)
                return "continue"
        else:
            display.print_warning(f"Number out of range. Please enter 0 to {total}.")
            time.sleep(1.0)
            return "continue"

    # Check hotkeys
    cmd = raw.lower()
    if cmd == "b":
        handle_benchmark(active_adapter)
        return "continue"
    elif cmd == "m":
        handle_custom_dns_mgr()
        return "continue"
    elif cmd == "s":
        new_adapter = handle_switch_adapter(active_adapter)
        return f"switch:{new_adapter}"
    elif cmd == "f":
        ok, msg = network.flush_dns_cache()
        if ok:
            display.print_success("DNS resolver cache flushed successfully.")
        else:
            display.print_error(f"Failed to flush cache: {msg}")
        time.sleep(1.2)
        return "continue"
    elif cmd in ("q", "exit", "quit"):
        return "exit"
    else:
        display.print_warning(f"Unknown command '{raw}'. Enter a DNS number or B/M/S/F/Q.")
        time.sleep(1.0)
        return "continue"


def handle_benchmark(adapter_name: str):
    """Runs concurrent DNS speed tests and presents sorted table and auto-connect option."""
    providers = storage.get_all_providers()
    display.print_info(f"Testing real UDP query latency for {len(providers)} DNS servers...")

    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=display.console,
    ) as progress:
        task_id = progress.add_task("[cyan]Benchmarking DNS resolution...", total=len(providers))

        def on_progress(done, total, current_name):
            progress.update(task_id, completed=done, description=f"[cyan]Testing {current_name}...")

        results = benchmark.run_benchmark(providers, progress_callback=on_progress)

    display.print_benchmark_table(results)

    valid_results = [r for r in results if r["status"] == "ok" and r["best_latency"] is not None]
    if not valid_results:
        display.print_warning("No DNS servers responded successfully to query resolution.")
        questionary.press_any_key_to_continue("Press any key to continue...").ask()
        return

    fastest = valid_results[0]
    choices = [
        questionary.Choice(
            f"⚡ Connect to Fastest: {fastest['name']} ({fastest['best_latency']} ms)",
            value=fastest["provider"],
        ),
        questionary.Choice("🔍 Choose another server from results", value="choose"),
        questionary.Choice("⬅️ Back to Main Screen", value="back"),
    ]

    action = questionary.select("Benchmark Options:", choices=choices).ask()

    if not action or action == "back":
        return

    target = fastest["provider"]
    if action == "choose":
        choice_list = [
            questionary.Choice(
                f"{r['name']} ({r['best_latency']} ms) - {r['dns1']}",
                value=r["provider"],
            )
            for r in valid_results
        ]
        choice_list.append(questionary.Choice("⬅️ Cancel", value=None))
        picked = questionary.select("Select server to apply:", choices=choice_list).ask()
        if not picked:
            return
        target = picked

    ok, msg = network.set_dns(adapter_name, target["dns1"], target.get("dns2"))
    if ok:
        display.print_success(f"Applied {target['name']} on {adapter_name} & flushed cache!")
    else:
        display.print_error(msg)
    time.sleep(1.5)


def handle_custom_dns_mgr():
    """Add / Remove custom user DNS profiles."""
    while True:
        customs = storage.load_custom_dns()
        choices = [
            questionary.Choice("➕ Add New Custom DNS", value="add"),
        ]
        if customs:
            choices.append(questionary.Choice(f"🗑️ Remove Custom DNS ({len(customs)} configured)", value="remove"))
        choices.append(questionary.Choice("⬅️ Back to Main Screen", value="back"))

        action = questionary.select("Custom DNS Manager:", choices=choices).ask()
        if not action or action == "back":
            break

        if action == "add":
            name = questionary.text("Enter Provider Name (e.g. My NextDNS):").ask()
            if not name or not name.strip():
                continue

            dns1 = questionary.text(
                "Enter Primary DNS IPv4:",
                validate=lambda text: True if validate_ip(text) else "Please enter a valid IPv4 address (e.g. 1.1.1.1)",
            ).ask()
            if not dns1:
                continue

            dns2 = questionary.text(
                "Enter Secondary DNS IPv4 (Optional, press Enter to skip):",
                validate=lambda text: True if not text.strip() or validate_ip(text) else "Please enter a valid IPv4 or leave blank",
            ).ask()

            desc = questionary.text("Enter Description (Optional):").ask() or "User Custom DNS"

            storage.add_custom_dns(name.strip(), dns1.strip(), dns2.strip() if dns2 else "", desc.strip())
            display.print_success(f"Custom DNS profile '{name}' saved successfully!")
            time.sleep(1.2)

        elif action == "remove":
            remove_choices = [
                questionary.Choice(f"{c['name']} ({c['dns1']})", value=c["name"])
                for c in customs
            ]
            remove_choices.append(questionary.Choice("⬅️ Cancel", value=None))

            to_remove = questionary.select("Select custom profile to delete:", choices=remove_choices).ask()
            if to_remove:
                storage.remove_custom_dns(to_remove)
                display.print_success(f"Removed custom profile '{to_remove}'.")
                time.sleep(1.2)


def handle_switch_adapter(current_adapter: str) -> str:
    """Lets user select another active or available network adapter."""
    adapters = network.get_network_adapters()
    if not adapters:
        display.print_error("No network adapters detected on this machine.")
        time.sleep(1.5)
        return current_adapter

    choices = []
    for a in adapters:
        status_icon = "🟢" if a.get("state", "").lower() == "connected" else "⚪"
        is_cur = " [Active]" if a["name"].lower() == current_adapter.lower() else ""
        label = f"{status_icon} {a['name']} ({a.get('state', 'Unknown')}){is_cur}"
        choices.append(questionary.Choice(label, value=a["name"]))
    choices.append(questionary.Choice("⬅️ Cancel", value=current_adapter))

    new_iface = questionary.select(
        "Select network adapter:",
        choices=choices,
    ).ask()

    if new_iface and new_iface != current_adapter:
        display.print_success(f"Switched active adapter to: {new_iface}")
        time.sleep(1.0)
        return new_iface
    return current_adapter
