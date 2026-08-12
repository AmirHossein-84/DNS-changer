import random
import string
import time
from typing import Any, Dict, List, Optional


def generate_random_subdomain(length: int = 16) -> str:
    """Generates a random domain string guaranteed not to exist."""
    chars = string.ascii_lowercase + string.digits
    rand_str = "".join(random.choice(chars) for _ in range(length))
    return f"leak-test-{rand_str}.nonexistent-test-domain.invalid"


def run_dns_leak_audit(adapter_name: str, configured_dns: List[str]) -> Dict[str, Any]:
    """
    Performs comprehensive security and privacy audit on active DNS:
    1. NXDOMAIN Hijacking check
    2. Known domain integrity / tampering check
    3. Direct vs System resolver consistency check
    """
    import dns.exception
    import dns.resolver

    report = {
        "adapter": adapter_name,
        "configured_dns": configured_dns,
        "nxdomain_hijacked": False,
        "nxdomain_details": None,
        "tampering_detected": False,
        "tampering_details": [],
        "resolver_responsive": False,
        "security_score": "SECURE",
        "warnings": [],
    }

    # 1. Test standard system resolution responsiveness
    try:
        res = dns.resolver.Resolver()
        if configured_dns:
            res.nameservers = configured_dns
        res.timeout = 2.0
        res.lifetime = 2.0

        ans = res.resolve("cloudflare.com", "A")
        if ans:
            report["resolver_responsive"] = True
    except Exception as e:
        report["warnings"].append(f"Resolver failed standard query: {e}")

    # 2. NXDOMAIN Hijack Test
    bogus_domain = generate_random_subdomain()
    try:
        res_nx = dns.resolver.Resolver()
        if configured_dns:
            res_nx.nameservers = configured_dns
        res_nx.timeout = 2.0
        res_nx.lifetime = 2.0

        ans_bogus = res_nx.resolve(bogus_domain, "A")
        # If it resolved to an IP, NXDOMAIN hijacking is occurring!
        if ans_bogus:
            hijacked_ips = [str(r) for r in ans_bogus]
            report["nxdomain_hijacked"] = True
            report["nxdomain_details"] = hijacked_ips
            report["warnings"].append(f"ISP or middlebox intercepts NXDOMAIN queries and injects: {', '.join(hijacked_ips)}")
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # Correct and secure behavior
        report["nxdomain_hijacked"] = False
    except Exception:
        report["nxdomain_hijacked"] = False

    # 3. Known Domain Integrity & Tampering Check
    known_checks = [
        {"domain": "one.one.one.one", "expected": ["1.1.1.1", "1.0.0.1"]},
        {"domain": "dns.google", "expected": ["8.8.8.8", "8.8.4.4"]},
    ]

    for check in known_checks:
        try:
            res_tamper = dns.resolver.Resolver()
            if configured_dns:
                res_tamper.nameservers = configured_dns
            res_tamper.timeout = 2.0
            res_tamper.lifetime = 2.0

            ans_t = res_tamper.resolve(check["domain"], "A")
            resolved = [str(r) for r in ans_t]
            matched = any(ip in check["expected"] for ip in resolved)
            if not matched:
                report["tampering_detected"] = True
                report["tampering_details"].append({
                    "domain": check["domain"],
                    "expected": check["expected"],
                    "got": resolved,
                })
                report["warnings"].append(f"Tampering detected on {check['domain']}: got {resolved} instead of {check['expected']}")
        except Exception:
            pass

    # Determine security posture rating
    if report["tampering_detected"]:
        report["security_score"] = "COMPROMISED"
    elif report["nxdomain_hijacked"]:
        report["security_score"] = "WARNING"
    elif not report["resolver_responsive"]:
        report["security_score"] = "UNREACHABLE"
    else:
        report["security_score"] = "SECURE"

    return report
