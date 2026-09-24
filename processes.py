import hashlib
import os
from typing import Any, Dict, List

import psutil


def calculate_sha256(file_path: str) -> str:
    if not file_path or not os.path.exists(file_path):
        return "N/A (Ficheiro não encontrado)"

    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError, OSError):
        return "Acesso Negado / Erro de leitura"


def collect_process_artifacts() -> List[Dict[str, Any]]:
    processes_data = []
    for proc in psutil.process_iter(
        ["pid", "name", "username", "cmdline", "exe", "create_time", "ppid"]
    ):
        try:
            pinfo = proc.info
            exe_path = pinfo.get("exe") or ""
            processes_data.append(
                {
                    "pid": pinfo.get("pid"),
                    "ppid": pinfo.get("ppid"),
                    "name": pinfo.get("name"),
                    "username": pinfo.get("username") or "N/A",
                    "cmdline": pinfo.get("cmdline") or [],
                    "exe": exe_path or "N/A",
                    "sha256": calculate_sha256(exe_path) if exe_path else "N/A",
                    "create_time": pinfo.get("create_time"),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes_data