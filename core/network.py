import ctypes
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Tuple


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
    Relaunches the current script with Administrator privileges on Windows.
    Returns True if already elevated, or triggers UAC prompt and exits current process.
    """
    if is_admin():
        return True

    if os.name == "nt":
        # Format arguments with quotes to preserve spaces
        script = os.path.abspath(sys.argv[0])
        params = f'"{script}" ' + " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            # If ShellExecuteW succeeds, ret > 32
            if ret > 32:
                sys.exit(0)
            else:
                return False
        except Exception:
            return False
    return False


def get_network_adapters() -> List[Dict[str, str]]:
    """
    Retrieves all available network adapters on Windows.
    Correctly handles interface names containing spaces (e.g. 'Wi-Fi', 'Ethernet 2').
    """
    adapters = []
    try:
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"],
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        lines = result.stdout.splitlines()

        # Find where the data table starts (after the separator line containing dashes)
        start_idx = 0
        for i, line in enumerate(lines):
            if "---" in line:
                start_idx = i + 1
                break

        for line in lines[start_idx:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
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
    except Exception:
        pass

    return adapters


def get_primary_adapter(adapters: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
    """
    Detects the primary active network adapter that has internet connectivity / default gateway.
    """
    if adapters is None:
        adapters = get_network_adapters()

    if not adapters:
        return None

    # Try detecting via PowerShell default route
    try:
        ps_cmd = (
            "Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | "
            "Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty InterfaceAlias"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        primary_alias = result.stdout.strip()
        if primary_alias:
            for iface in adapters:
                if iface["name"].lower() == primary_alias.lower():
                    return iface["name"]
    except Exception:
        pass

    # Fallback 1: First adapter with state == 'Connected'
    for iface in adapters:
        if iface.get("state", "").lower() == "connected":
            return iface["name"]

    # Fallback 2: First adapter in list
    return adapters[0]["name"] if adapters else None


def get_current_dns(adapter_name: str) -> Dict[str, any]:
    """
    Retrieves the currently configured DNS servers for the specified adapter.
    Returns a dict with 'servers' (list of IP strings) and 'is_dhcp' (bool).
    """
    dns_info = {"servers": [], "is_dhcp": True, "raw": ""}
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    try:
        result = subprocess.run(
            ["netsh", "interface", "ipv4", "show", "dnsservers", f"name={adapter_name}"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        output = result.stdout
        dns_info["raw"] = output

        is_dhcp = "DHCP" in output and "Static" not in output
        dns_info["is_dhcp"] = is_dhcp

        # Extract all valid IPv4 addresses
        servers = []
        for line in output.splitlines():
            line = line.strip()
            # Ignore subnet mask or broadcast lines if any
            if "DNS servers" in line or "Statically Configured" in line or "Register with" in line:
                pass
            found_ips = ip_pattern.findall(line)
            for ip in found_ips:
                if ip not in servers and not ip.startswith("0.") and not ip.startswith("255."):
                    servers.append(ip)

        dns_info["servers"] = servers
    except Exception as e:
        dns_info["error"] = str(e)

    return dns_info


def set_dns(
    adapter_name: str, dns1: str, dns2: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Configures static primary and optional secondary DNS servers for an adapter,
    then automatically flushes the DNS cache.
    """
    try:
        # Set primary DNS
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

        # Add secondary DNS if provided
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

        # Auto-flush DNS cache
        flush_dns_cache()
        return True, f"Successfully set DNS to {dns1}" + (f", {dns2}" if dns2 else "")
    except Exception as e:
        return False, str(e)


def clear_dns(adapter_name: str) -> Tuple[bool, str]:
    """
    Resets DNS configuration on the adapter back to automatic (DHCP),
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
