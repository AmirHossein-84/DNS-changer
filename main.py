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

            choice = menu.get_main_choice()

            if not choice or choice == "exit":
                display.print_info("Exiting DNS Changer. Goodbye!")
                break

            elif choice == "category":
                menu.handle_category_menu(active_adapter)

            elif choice == "search":
                menu.handle_search_menu(active_adapter)

            elif choice == "benchmark":
                menu.handle_benchmark(active_adapter)

            elif choice == "custom_mgr":
                menu.handle_custom_dns_mgr()

            elif choice == "clear":
                ok, msg = network.clear_dns(active_adapter)
                if ok:
                    display.print_success(msg)
                else:
                    display.print_error(msg)
                time.sleep(1.5)

            elif choice == "flush":
                ok, msg = network.flush_dns_cache()
                if ok:
                    display.print_success("DNS resolver cache flushed successfully.")
                else:
                    display.print_error(f"Failed to flush DNS: {msg}")
                time.sleep(1.5)

            elif choice == "switch_adapter":
                active_adapter = menu.handle_switch_adapter(active_adapter)

        except KeyboardInterrupt:
            display.print_info("\nOperation interrupted by user. Exiting...")
            break
        except Exception as e:
            display.print_error(f"An unexpected error occurred: {e}")
            time.sleep(2.0)


if __name__ == "__main__":
    run_app()
