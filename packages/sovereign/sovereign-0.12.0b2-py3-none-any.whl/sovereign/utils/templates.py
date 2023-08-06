from typing import List, Any, Dict


def healthchecks_enabled(healthchecks: List[Dict[str, Any]]) -> bool:
    for healthcheck in healthchecks:
        if healthcheck.get("path") in ("no", False):
            return False
    return True


def upstream_requires_tls(cluster: Dict[str, Any]) -> bool:
    for host in cluster.get("hosts", []):
        if "443" in str(host.get("port")):
            return True
    return False
