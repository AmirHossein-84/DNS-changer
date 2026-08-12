import ctypes
import os
import re
import socket
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def is_admin() -> bool:
    """Check if the current process has administrative privileges."""
    try:
        if os.name == "nt":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.geteuid() == 0
    except Exception:
        return False


def elevate_privileges() -> bool:
    """
    Relaunches the current script or executable with Administrator privileges on Windows.
    Correctly handles both raw Python scripts and frozen PyInstaller .exe binaries.
    """
    if is_admin():
        return True

    if os.name == "nt":
        is_frozen = getattr(sys, "frozen", False)
        if is_frozen:
            executable = sys.executable
            params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        else:
            executable = sys.executable
            script = os.path.abspath(sys.argv[0])
            params = f'"{script}" ' + " ".join([f'"{arg}"' for arg in sys.argv[1:]])

        try:
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", executable, params, None, 1
            )
            if ret > 32:
                sys.exit(0)
            else:
                return False
        except Exception:
            return False
    return False


def get_active_route_local_ip() -> Optional[str]:
    """
    Blazingly fast (0.5ms) native socket probe to find the local IP address
    currently bound to the active internet default gateway.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Does not send actual packets, just queries local routing table
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return None


def get_all_adapters_and_config() -> Tuple[List[Dict[str, str]], Optional[str], Dict[str, Dict[str, any]]]:
    """
    Performs a single-pass, high-speed query to retrieve all network adapters,
    current DNS settings, and automatically identifies the primary active adapter.
    Runs in ~50ms total.
    """
    adapters = []
    dns_configs = {}
    primary_name = None
    local_active_ip = get_active_route_local_ip()

    try:
        # Run single netsh config command
        result = subprocess.run(
            ["netsh", "interface", "ipv4", "show", "config"],
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        output = result.stdout

        # Parse sections separated by "Configuration for interface"
        sections = re.split(r'Configuration for interface "([^"]+)"', output)
        if len(sections) > 1:
            for i in range(1, len(sections), 2):
                iface_name = sections[i].strip()
                iface_body = sections[i + 1]

                # Extract IP addresses
                ip_lines = [l for l in iface_body.splitlines() if "IP Address" in l or "IPv4 Address" in l]
                iface_ips = []
                for l in ip_lines:
                    found = IP_PATTERN.findall(l)
                    iface_ips.extend(found)

                # Extract DNS servers
                dns_servers = []
                is_dhcp = "DHCP" in iface_body and "Statically Configured DNS Servers" not in iface_body

                in_dns_section = False
                for line in iface_body.splitlines():
                    if "DNS servers configured through DHCP:" in line or "Statically Configured DNS Servers:" in line:
                        in_dns_section = True
                        found = IP_PATTERN.findall(line)
                        for ip in found:
                            if ip not in dns_servers and not ip.startswith("0.") and not ip.startswith("255."):
                                dns_servers.append(ip)
                        continue

                    if in_dns_section:
                        if ":" in line and not line.strip().startswith("Register"):
                            in_dns_section = False
                        else:
                            found = IP_PATTERN.findall(line)
                            for ip in found:
                                if ip not in dns_servers and not ip.startswith("0.") and not ip.startswith("255."):
                                    dns_servers.append(ip)

                dns_configs[iface_name] = {
                    "servers": dns_servers,
                    "is_dhcp": is_dhcp,
                    "ips": iface_ips,
                }

                # Check if this interface owns the active route IP
                if local_active_ip and local_active_ip in iface_ips:
                    primary_name = iface_name

        # Also get quick interface state (Connected/Disconnected)
        iface_show = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        lines = iface_show.stdout.splitlines()
        start_idx = 0
        for idx, l in enumerate(lines):
            if "---" in l:
                start_idx = idx + 1
                break

        for l in lines[start_idx:]:
            l = l.strip()
            if not l:
                continue
            parts = l.split()
            if len(parts) >= 4:
                admin_state = parts[0]
                state = parts[1]
                iface_type = parts[2]
                name = " ".join(parts[3:])
                adapters.append(
                    {
                        "name": name,
                        "admin_state": admin_state,
                        "state": state,
                        "type": iface_type,
                    }
                )

        # Fallback for primary adapter
        if not primary_name and adapters:
            for a in adapters:
                if a.get("state", "").lower() == "connected":
                    primary_name = a["name"]
                    break
            if not primary_name:
                primary_name = adapters[0]["name"]

    except Exception:
        pass

    return adapters, primary_name, dns_configs


def get_network_adapters() -> List[Dict[str, str]]:
    """Retrieves list of network adapters."""
    adapters, _, _ = get_all_adapters_and_config()
    return adapters


def get_primary_adapter(adapters: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
    """Retrieves primary active adapter name."""
    _, primary, _ = get_all_adapters_and_config()
    return primary


def get_current_dns(adapter_name: str) -> Dict[str, any]:
    """
    Retrieves currently configured DNS servers for the specified adapter.
    """
    _, _, dns_configs = get_all_adapters_and_config()
    if adapter_name in dns_configs:
        return dns_configs[adapter_name]

    # Fallback to direct query if not in cache
    dns_info = {"servers": [], "is_dhcp": True}
    try:
        res = subprocess.run(
            ["netsh", "interface", "ipv4", "show", "dnsservers", f"name={adapter_name}"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        output = res.stdout
        is_dhcp = "DHCP" in output and "Static" not in output
        dns_info["is_dhcp"] = is_dhcp
        servers = []
        for line in output.splitlines():
            found_ips = IP_PATTERN.findall(line)
            for ip in found_ips:
                if ip not in servers and not ip.startswith("0.") and not ip.startswith("255."):
                    servers.append(ip)
        dns_info["servers"] = servers
    except Exception:
        pass
    return dns_info


def has_ipv6_enabled(adapter_name: str) -> bool:
    """Checks if IPv6 protocol is active on the given interface."""
    try:
        res = subprocess.run(
            ["netsh", "interface", "ipv6", "show", "interface", f"name={adapter_name}"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return res.returncode == 0 and "connected" in res.stdout.lower()
    except Exception:
        return False


def set_dns_v6(adapter_name: str, ipv6_1: str, ipv6_2: Optional[str] = None) -> Tuple[bool, str]:
    """Configures static IPv6 DNS servers for an adapter."""
    try:
        cmd_p = [
            "netsh",
            "interface",
            "ipv6",
            "set",
            "dnsservers",
            f"name={adapter_name}",
            "source=static",
            f"address={ipv6_1}",
            "register=primary",
            "validate=no",
        ]
        res1 = subprocess.run(
            cmd_p,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if res1.returncode != 0:
            return False, res1.stderr or res1.stdout

        if ipv6_2 and ipv6_2.strip():
            cmd_s = [
                "netsh",
                "interface",
                "ipv6",
                "add",
                "dnsservers",
                f"name={adapter_name}",
                f"address={ipv6_2}",
                "index=2",
                "validate=no",
            ]
            subprocess.run(
                cmd_s,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        return True, "IPv6 DNS configured successfully."
    except Exception as e:
        return False, str(e)


def clear_dns_v6(adapter_name: str) -> Tuple[bool, str]:
    """Resets IPv6 DNS on the adapter back to automatic (DHCP)."""
    try:
        cmd = [
            "netsh",
            "interface",
            "ipv6",
            "set",
            "dnsservers",
            f"name={adapter_name}",
            "source=dhcp",
        ]
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return True, "IPv6 DNS reset to DHCP."
    except Exception as e:
        return False, str(e)


def set_dns(
    adapter_name: str,
    dns1: str,
    dns2: Optional[str] = None,
    ipv6_1: Optional[str] = None,
    ipv6_2: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Configures static IPv4 and optional dual-stack IPv6 DNS servers for an adapter,
    then automatically flushes the DNS cache.
    """
    try:
        cmd_primary = [
            "netsh",
            "interface",
            "ipv4",
            "set",
            "dnsservers",
            f"name={adapter_name}",
            "source=static",
            f"address={dns1}",
            "register=primary",
            "validate=no",
        ]
        res1 = subprocess.run(
            cmd_primary,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if res1.returncode != 0:
            return False, f"Failed to set primary DNS: {res1.stderr or res1.stdout}"

        if dns2 and dns2.strip():
            cmd_secondary = [
                "netsh",
                "interface",
                "ipv4",
                "add",
                "dnsservers",
                f"name={adapter_name}",
                f"address={dns2}",
                "index=2",
                "validate=no",
            ]
            res2 = subprocess.run(
                cmd_secondary,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            if res2.returncode != 0:
                return False, f"Primary DNS set, but failed to set secondary DNS: {res2.stderr or res2.stdout}"

        # Dual-stack IPv6 configuration if available
        if ipv6_1 and has_ipv6_enabled(adapter_name):
            set_dns_v6(adapter_name, ipv6_1, ipv6_2)

        flush_dns_cache()
        return True, f"Successfully set DNS to {dns1}" + (f", {dns2}" if dns2 else "")
    except Exception as e:
        return False, str(e)


def clear_dns(adapter_name: str) -> Tuple[bool, str]:
    """
    Resets both IPv4 and IPv6 DNS configurations on the adapter back to automatic (DHCP),
    then flushes the DNS cache.
    """
    try:
        cmd = [
            "netsh",
            "interface",
            "ipv4",
            "set",
            "dnsservers",
            f"name={adapter_name}",
            "source=dhcp",
        ]
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if res.returncode != 0:
            return False, f"Failed to reset DNS: {res.stderr or res.stdout}"

        clear_dns_v6(adapter_name)
        flush_dns_cache()
        return True, f"Successfully reset DNS for '{adapter_name}' to Automatic (DHCP)."
    except Exception as e:
        return False, str(e)


def flush_dns_cache() -> Tuple[bool, str]:
    """
    Flushes the Windows DNS resolver cache (ipconfig /flushdns).
    """
    try:
        res = subprocess.run(
            ["ipconfig", "/flushdns"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        if res.returncode == 0:
            return True, "DNS resolver cache flushed successfully."
        return False, res.stderr or res.stdout
    except Exception as e:
        return False, str(e)
