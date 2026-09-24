import sys
import platform
from datetime import datetime, timezone
from core.processes import collect_process_artifacts
from core.network import collect_network_artifacts
from utils.reporter import save_and_package_triage
def main():
    print("=" * 60)
    print("LIVE HOST TRIAGE & ARTIFACT COLLECTOR (DFIR) ")
    print("=" * 60)
    print("[*] Iniciando coleta de evidências voláteis...")
    system_info = {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }
    print("[+] Coletando artefatos de processos e calculando hashes SHA-256...")
    processes = collect_process_artifacts()
    print(f"  -> {len(processes)} processos analisados.")
    print("[+] Coletando conexões de rede e sockets ativos...")
    network = collect_network_artifacts()
    print(f"  -> {len(network)}conexões encontradas.")
    triage_playload = {
        "sytem_info": system_info,
        "processes": processes,
        "network_connections": network
    }
    print("[+] Empacotando gerando manifesto de integridade...")
    zip_path = save_and_package_triage(triage_playload)
    print(f"[✓] Coleta concluída com sucesso!")
    print(f"[✓] Pacote de evidências salvo em: {zip_path}")
    print("=" * 60)
if __name__ == "__main__":
    main()