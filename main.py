import os
import sys

# Configure UTF-8 streams on Windows before any output
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

import time
from core import network, storage
from ui import display, menu


def run_app():
    # Slightly increase console font size proportionally (height=18pt)
    display.adjust_console_font(target_height=18)

    # Attempt automatic elevation if not running as Administrator on Windows
    is_elevated = network.is_admin()
    if not is_elevated:
        elevated = network.elevate_privileges()
        if elevated:
            return

    # Detect network adapters
    adapters = network.get_network_adapters()
    if not adapters:
        display.print_error("No network interfaces found on this system.")
        input("Press Enter to exit...")
        sys.exit(1)

    active_adapter = network.get_primary_adapter(adapters)
    if not active_adapter:
        active_adapter = adapters[0]["name"]

    while True:
        try:
            display.clear_screen()
            display.print_banner()

            # Refresh live DNS status
            current_dns = network.get_current_dns(active_adapter)
            provider_name = storage.identify_dns_provider(current_dns.get("servers", []))
            display.print_status_card(
                active_adapter,
                current_dns,
                provider_name,
                is_elevated=network.is_admin(),
            )

            # Display all DNS servers in clean 2-column numbered grid
            providers = storage.get_all_providers()
            display.print_quick_dns_grid(providers)

            # Fast 1-step number input or hotkey
            action = menu.handle_quick_input(providers, active_adapter)

            if action == "exit_success":
                time.sleep(1.2)
                sys.exit(0)

            elif action == "exit":
                display.print_info("Exiting DNS Changer. Goodbye!")
                break

            elif action.startswith("switch:"):
                active_adapter = action.split(":", 1)[1]

        except KeyboardInterrupt:
            display.print_info("\nOperation interrupted by user. Exiting...")
            break
        except Exception as e:
            display.print_error(f"An unexpected error occurred: {e}")
            time.sleep(2.0)


if __name__ == "__main__":
    run_app()
