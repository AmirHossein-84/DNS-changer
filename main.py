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
from core import cli, network, storage
from ui import display, menu


def run_app():
    # 1. Process Headless CLI Arguments if provided
    if len(sys.argv) > 1:
        if cli.handle_cli():
            return

    # 2. Initialize console window geometry (120 cols x 34 lines) and font size
    display.init_console_window(target_cols=120, target_lines=34)

    # 3. Attempt automatic elevation if not running as Administrator on Windows
    is_elevated = network.is_admin()
    if not is_elevated:
        elevated = network.elevate_privileges()
        if elevated:
            return

    # 4. High-speed single-pass adapter and config discovery (<50ms)
    adapters, active_adapter, dns_configs = network.get_all_adapters_and_config()
    if not adapters:
        display.print_error("No network interfaces found on this system.")
        input("Press Enter to exit...")
        sys.exit(1)

    if not active_adapter:
        active_adapter = adapters[0]["name"]

    # Pre-fetch providers list and favorites
    providers = storage.get_all_providers()
    favorites = storage.get_favorites()
    needs_refresh = False

    while True:
        try:
            display.clear_screen()
            display.print_banner()

            # Refresh live DNS status only when state changed
            if needs_refresh:
                adapters, _, dns_configs = network.get_all_adapters_and_config()
                providers = storage.get_all_providers()
                favorites = storage.get_favorites()
                needs_refresh = False

            current_dns = dns_configs.get(active_adapter) or network.get_current_dns(active_adapter)
            provider_name = storage.identify_dns_provider(current_dns.get("servers", []))
            previous_dns = storage.get_previous_dns(active_adapter)

            display.print_status_card(
                active_adapter,
                current_dns,
                provider_name,
                is_elevated=network.is_admin(),
                previous_dns=previous_dns,
            )

            # Display all DNS servers in clean 2-column numbered grid with favorites & badges
            display.print_quick_dns_grid(providers, favorites=favorites)

            # Fast 1-step number input or hotkey
            action = menu.handle_quick_input(providers, active_adapter, current_dns)

            if action == "exit_success":
                time.sleep(1.0)
                sys.exit(0)

            elif action == "exit":
                display.print_info("Exiting DNS Changer. Goodbye!")
                break

            elif action.startswith("switch:"):
                active_adapter = action.split(":", 1)[1]
                needs_refresh = True

            elif action == "continue":
                needs_refresh = True

        except KeyboardInterrupt:
            display.print_info("\nOperation interrupted by user. Exiting...")
            break
        except Exception as e:
            display.print_error(f"An unexpected error occurred: {e}")
            time.sleep(2.0)


if __name__ == "__main__":
    run_app()
