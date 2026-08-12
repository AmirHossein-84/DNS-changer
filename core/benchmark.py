from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Callable, Dict, List, Optional
import dns.exception
import dns.resolver


def test_single_dns_latency(
    dns_ip: str, domain: str = "google.com", timeout: float = 1.5, runs: int = 2
) -> Dict[str, any]:
    """
    Measures actual DNS query resolution time (UDP Port 53) against a given DNS server.
    Returns dict with status ('ok', 'timeout', 'error'), average latency in ms, and resolved IP.
    """
    if not dns_ip or dns_ip == "0.0.0.0":
        return {"status": "error", "latency": None, "error": "Invalid IP"}

    latencies = []
    resolved_ip = None

    for _ in range(runs):
        try:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = [dns_ip]
            resolver.timeout = timeout
            resolver.lifetime = timeout

            t0 = time.perf_counter()
            answers = resolver.resolve(domain, "A")
            t1 = time.perf_counter()

            latencies.append((t1 - t0) * 1000.0)
            if answers:
                resolved_ip = str(answers[0])
        except (dns.resolver.Timeout, dns.resolver.LifetimeTimeout):
            return {
                "status": "timeout",
                "latency": None,
                "error": "Request timed out",
                "resolved_ip": None,
            }
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers) as e:
            return {
                "status": "error",
                "latency": None,
                "error": f"DNS error: {type(e).__name__}",
                "resolved_ip": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "latency": None,
                "error": str(e),
                "resolved_ip": None,
            }

    if latencies:
        avg_latency = round(sum(latencies) / len(latencies), 1)
        return {
            "status": "ok",
            "latency": avg_latency,
            "error": None,
            "resolved_ip": resolved_ip,
        }

    return {
        "status": "timeout",
        "latency": None,
        "error": "No response",
        "resolved_ip": None,
    }


def benchmark_provider(provider: Dict[str, str], domain: str = "google.com", timeout: float = 1.5) -> Dict[str, any]:
    """
    Tests both primary and secondary DNS for a provider and records metrics.
    """
    res1 = test_single_dns_latency(provider["dns1"], domain=domain, timeout=timeout)
    res2 = None
    if provider.get("dns2"):
        res2 = test_single_dns_latency(provider["dns2"], domain=domain, timeout=timeout)

    # Calculate combined / best rating
    best_latency = res1["latency"]
    if res1["status"] != "ok" and res2 and res2["status"] == "ok":
        best_latency = res2["latency"]
    elif res1["status"] == "ok" and res2 and res2["status"] == "ok":
        best_latency = min(res1["latency"], res2["latency"])

    status = "ok" if (res1["status"] == "ok" or (res2 and res2["status"] == "ok")) else "timeout"

    return {
        "provider": provider,
        "name": provider["name"],
        "category": provider.get("category", "General"),
        "dns1": provider["dns1"],
        "dns2": provider.get("dns2", ""),
        "res1": res1,
        "res2": res2,
        "best_latency": best_latency,
        "status": status,
    }


def run_benchmark(
    providers: List[Dict[str, str]],
    domain: str = "google.com",
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
    max_workers: int = 12,
) -> List[Dict[str, any]]:
    """
    Runs concurrent DNS query benchmarks across a list of providers.
    Calls progress_callback(completed_count, total_count, current_provider_name).
    Returns sorted list of results (fastest first).
    """
    results = []
    total = len(providers)
    completed_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(benchmark_provider, p, domain): p for p in providers
        }

        for future in as_completed(future_map):
            completed_count += 1
            provider = future_map[future]
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                results.append({
                    "provider": provider,
                    "name": provider["name"],
                    "category": provider.get("category", "General"),
                    "dns1": provider["dns1"],
                    "dns2": provider.get("dns2", ""),
                    "best_latency": None,
                    "status": "error",
                    "error": str(e),
                })

            if progress_callback:
                progress_callback(completed_count, total, provider["name"])

    # Sort results: OK status with lowest latency first, then errors/timeouts
    def sort_key(item):
        if item["status"] == "ok" and item["best_latency"] is not None:
            return (0, item["best_latency"])
        return (1, 999999)

    results.sort(key=sort_key)
    return results
