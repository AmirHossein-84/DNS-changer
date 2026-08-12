import json
import os
import re
from typing import Any, Dict, List, Optional

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dns_config.json")

DEFAULT_CATEGORIES = {
    "Anti-Sanction & Bypass": [
        {"name": "Shecan (178)", "dns1": "178.22.122.100", "dns2": "185.51.200.2", "desc": "Popular Iranian sanction-bypass DNS", "badge": "⚡ Anti-Sanction"},
        {"name": "Shecan (185)", "dns1": "185.51.200.2", "dns2": "178.22.122.100", "desc": "Alternative Shecan server", "badge": "⚡ Anti-Sanction"},
        {"name": "Electro", "dns1": "78.157.42.100", "dns2": "78.157.42.101", "desc": "Bypass & anti-sanction gaming DNS", "badge": "🎮 Gaming / Bypass"},
        {"name": "403 Online", "dns1": "10.202.10.202", "dns2": "10.202.10.102", "desc": "Sanction-bypass for developers and services", "badge": "💻 Dev / Docker"},
        {"name": "Radar Game", "dns1": "10.202.10.10", "dns2": "10.202.10.11", "desc": "Optimized for gaming & anti-sanction", "badge": "🎮 Gaming Low-Ping"},
        {"name": "Bogzar DNS", "dns1": "185.55.226.26", "dns2": "185.55.225.25", "desc": "Fast sanction bypass DNS", "badge": "⚡ Fast Bypass"},
        {"name": "Gozar DNS", "dns1": "185.55.225.25", "dns2": "185.55.225.26", "desc": "Iranian bypass DNS", "badge": "⚡ Bypass"},
        {"name": "Host Iran", "dns1": "172.29.2.100", "dns2": "172.29.0.100", "desc": "Host Iran infrastructure DNS", "badge": "🏢 Local Infra"},
        {"name": "Shatel DNS", "dns1": "85.15.1.15", "dns2": "85.15.1.14", "desc": "Shatel ISP DNS", "badge": "🌐 Shatel ISP"},
        {"name": "Pishgaman DNS", "dns1": "5.202.100.100", "dns2": "5.202.100.101", "desc": "Pishgaman ISP DNS", "badge": "🌐 Pishgaman ISP"},
    ],
    "Global & Fast": [
        {"name": "Cloudflare (1.1.1.1)", "dns1": "1.1.1.1", "dns2": "1.0.0.1", "desc": "Fastest privacy-first global DNS", "badge": "🌐 Ultra Fast"},
        {"name": "Google Public DNS", "dns1": "8.8.8.8", "dns2": "8.8.4.4", "desc": "Reliable & widely used global DNS", "badge": "🌐 Global High-Reliability"},
        {"name": "OpenDNS (Cisco)", "dns1": "208.67.222.222", "dns2": "208.67.220.220", "desc": "Enterprise-grade reliability by Cisco", "badge": "🏢 Cisco Enterprise"},
        {"name": "Alternate DNS", "dns1": "76.76.19.19", "dns2": "76.223.122.150", "desc": "Ad-blocking alternative DNS", "badge": "🛡️ Ad-Block Global"},
        {"name": "Verisign", "dns1": "64.6.64.6", "dns2": "64.6.65.6", "desc": "High stability global DNS", "badge": "🌐 Stable Anycast"},
        {"name": "Neustar UltraDNS", "dns1": "156.154.70.1", "dns2": "156.154.71.1", "desc": "Fast recursive enterprise DNS", "badge": "🏢 Neustar Cloud"},
        {"name": "Comodo Secure", "dns1": "8.26.56.26", "dns2": "8.20.247.20", "desc": "Security focused DNS", "badge": "🛡️ Threat Shield"},
        {"name": "Yandex DNS", "dns1": "77.88.8.8", "dns2": "77.88.8.1", "desc": "Fast eastern European & CIS DNS", "badge": "🌐 Yandex Fast"},
        {"name": "Dyn DNS", "dns1": "216.146.35.35", "dns2": "216.146.36.36", "desc": "Oracle Dyn public DNS", "badge": "🏢 Oracle Dyn"},
    ],
    "Privacy & Security": [
        {"name": "Quad9 (Malware Block)", "dns1": "9.9.9.9", "dns2": "149.112.112.112", "desc": "Blocks malicious domains & preserves privacy", "badge": "🛡️ Malware Block"},
        {"name": "AdGuard DNS (Default)", "dns1": "94.140.14.14", "dns2": "94.140.15.15", "desc": "Blocks ads, tracking & phishing", "badge": "🛡️ AdGuard Default"},
        {"name": "AdGuard DNS (Legacy)", "dns1": "176.103.130.130", "dns2": "176.103.130.131", "desc": "AdGuard legacy server addresses", "badge": "🛡️ AdGuard Legacy"},
        {"name": "CleanBrowsing (Security)", "dns1": "185.228.168.9", "dns2": "185.228.169.9", "desc": "Blocks malware, phishing & malicious domains", "badge": "🛡️ Clean Browsing"},
        {"name": "SafeDNS", "dns1": "195.46.39.39", "dns2": "195.46.39.40", "desc": "Cloud protection against cyber threats", "badge": "🛡️ Cloud Security"},
        {"name": "DNS.Watch", "dns1": "84.200.69.80", "dns2": "84.200.70.40", "desc": "Uncensored, no-logging DNS in Germany", "badge": "🔒 No-Logs Privacy"},
        {"name": "OpenNIC", "dns1": "46.151.208.154", "dns2": "128.199.248.105", "desc": "Decentralized, anti-censorship open DNS", "badge": "🌐 Open NIC"},
    ],
    "Gaming & Low Ping": [
        {"name": "Radar Game", "dns1": "10.202.10.10", "dns2": "10.202.10.11", "desc": "Optimized routing for gaming servers", "badge": "🎮 Radar Gaming"},
        {"name": "Electro Gaming", "dns1": "78.157.42.100", "dns2": "78.157.42.101", "desc": "Gaming anti-sanction provider", "badge": "🎮 Electro Gaming"},
        {"name": "Cloudflare Gaming", "dns1": "1.1.1.1", "dns2": "1.0.0.1", "desc": "Ultra low latency anycast network", "badge": "🎮 Cloudflare Gaming"},
        {"name": "Google DNS", "dns1": "8.8.8.8", "dns2": "8.8.4.4", "desc": "Global low ping edge routing", "badge": "🎮 Google Gaming"},
        {"name": "Quad9 Gaming", "dns1": "9.9.9.9", "dns2": "149.112.112.112", "desc": "Fast anycast secure gaming", "badge": "🎮 Quad9 Gaming"},
    ],
}


def _read_config_raw() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_config_raw(data: Dict[str, Any]) -> bool:
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def load_custom_dns() -> List[Dict[str, str]]:
    """Loads user-created custom DNS servers from config file."""
    return _read_config_raw().get("custom_dns", [])


def save_custom_dns(custom_list: List[Dict[str, str]]) -> bool:
    """Saves custom DNS servers to config file."""
    cfg = _read_config_raw()
    cfg["custom_dns"] = custom_list
    return _write_config_raw(cfg)


def add_custom_dns(name: str, dns1: str, dns2: Optional[str] = None, desc: str = "Custom DNS") -> bool:
    """Adds or updates a custom DNS configuration."""
    customs = load_custom_dns()
    customs = [c for c in customs if c["name"].lower() != name.lower()]
    customs.append({
        "name": name,
        "dns1": dns1,
        "dns2": dns2 or "",
        "desc": desc,
        "badge": "⭐ Custom Profile",
    })
    return save_custom_dns(customs)


def remove_custom_dns(name: str) -> bool:
    """Removes a custom DNS configuration by name."""
    customs = load_custom_dns()
    filtered = [c for c in customs if c["name"].lower() != name.lower()]
    if len(filtered) == len(customs):
        return False
    return save_custom_dns(filtered)


def get_favorites() -> List[str]:
    """Retrieves list of pinned favorite provider names."""
    return _read_config_raw().get("favorites", ["Shecan (178)", "Electro", "Cloudflare (1.1.1.1)"])


def toggle_favorite(provider_name: str) -> bool:
    """Toggles pinning a provider in favorites."""
    cfg = _read_config_raw()
    favs = cfg.get("favorites", ["Shecan (178)", "Electro", "Cloudflare (1.1.1.1)"])
    if provider_name in favs:
        favs.remove(provider_name)
    else:
        favs.append(provider_name)
    cfg["favorites"] = favs
    return _write_config_raw(cfg)


def save_previous_dns(adapter_name: str, dns_info: Dict[str, Any]) -> bool:
    """Saves previous DNS state before modifying for 1-click Undo."""
    cfg = _read_config_raw()
    history = cfg.get("history", {})
    history[adapter_name] = {
        "servers": dns_info.get("servers", []),
        "is_dhcp": dns_info.get("is_dhcp", True),
    }
    cfg["history"] = history
    return _write_config_raw(cfg)


def get_previous_dns(adapter_name: str) -> Optional[Dict[str, Any]]:
    """Loads previously saved DNS state for the adapter."""
    cfg = _read_config_raw()
    return cfg.get("history", {}).get(adapter_name)


def get_all_providers() -> List[Dict[str, str]]:
    """Returns a flat list of all unique DNS providers (default + custom)."""
    providers = []
    seen = set()

    # Add custom providers first
    for item in load_custom_dns():
        key = (item["dns1"], item.get("dns2", ""))
        if key not in seen:
            seen.add(key)
            item_copy = dict(item)
            item_copy["category"] = "Custom"
            providers.append(item_copy)

    # Add default categorized providers
    for cat_name, servers in DEFAULT_CATEGORIES.items():
        for item in servers:
            key = (item["dns1"], item.get("dns2", ""))
            if key not in seen:
                seen.add(key)
                item_copy = dict(item)
                item_copy["category"] = cat_name
                providers.append(item_copy)

    return providers


def get_categories() -> List[str]:
    """Returns list of category names."""
    cats = list(DEFAULT_CATEGORIES.keys())
    if load_custom_dns():
        cats.insert(0, "Custom")
    return cats


def get_providers_by_category(category: str) -> List[Dict[str, str]]:
    """Returns providers in a specific category."""
    if category == "Custom":
        return load_custom_dns()
    return DEFAULT_CATEGORIES.get(category, [])


def identify_dns_provider(dns_ips: List[str]) -> Optional[str]:
    """
    Given a list of active DNS IP addresses, returns the matching provider name if known.
    """
    if not dns_ips:
        return None

    primary_ip = dns_ips[0].strip()
    secondary_ip = dns_ips[1].strip() if len(dns_ips) > 1 else None

    # Check exact match first
    for p in get_all_providers():
        p_d1 = p["dns1"].strip()
        p_d2 = p.get("dns2", "").strip()

        if secondary_ip and p_d2:
            if primary_ip == p_d1 and secondary_ip == p_d2:
                return p["name"]
        if primary_ip == p_d1:
            return p["name"]

    return None


def find_provider_by_query(query: str, providers: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, str]]:
    """
    High-speed resolution of user CLI or search query to a DNS provider dict:
    - Number index (e.g. '1' -> first provider)
    - Name fuzzy match (e.g. 'electro', 'shecan', 'cloudflare')
    - Custom IP format (e.g. '1.1.1.1,1.0.0.1' or '1.1.1.1')
    """
    if not query:
        return None

    q = query.strip()
    if not providers:
        providers = get_all_providers()

    # Case 1: Numeric index
    if q.isdigit():
        idx = int(q)
        if 1 <= idx <= len(providers):
            return providers[idx - 1]
        return None

    # Case 2: Custom IP format
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    ips = ip_pattern.findall(q)
    if ips:
        dns1 = ips[0]
        dns2 = ips[1] if len(ips) > 1 else ""
        return {
            "name": f"Custom ({dns1})",
            "dns1": dns1,
            "dns2": dns2,
            "desc": "Command-line specified DNS",
            "badge": "⚡ CLI Custom",
            "category": "Custom",
        }

    # Case 3: Name exact or substring match
    q_lower = q.lower()
    for p in providers:
        if p["name"].lower() == q_lower:
            return p

    for p in providers:
        if q_lower in p["name"].lower():
            return p

    return None
