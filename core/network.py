import psutil
from typing import List, Dict, Any
def collect_network_artifacts() -> List[Dict[str, Any]]:
    network_data = []
    try:
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            laddr = f"{conn.laddr.ip}: {conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}: {conn.raddr.port}" if conn.raddr else "N/A"
            conn_entry = {
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type), 
                "local_address": laddr,
                "remote_address": raddr,
                "status": conn.status,
                "pid": conn.pid
            }
            network_data.append(conn_entry)
    except (psutil.AccessDenied, PermissionError):
        pass

    return network_data