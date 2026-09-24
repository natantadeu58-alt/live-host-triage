import json
import os
import zipfile
import hashlib
from datetime import datetime
from typing import Dict, Any 
def save_and_package_triage(data: Dict[str, Any], output_dir: str = "triage_output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_filename = f"triage_data_{timestamp}.json"
    json_path = os.path.join(output_dir, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        zip_filename = f"triage_package_{timestamp}.zip"
        zip_path = os.path.join(output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_path, arcname=json_filename)
            sha256_hash = hashlib.sha256()
            with open(zip_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                    manifest_path = os.path.join(output_dir, f"manifest_{timestamp}.txt")
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        f.write(f"Triage Package: {zip_filename}\n")
                        f.write(f"Timestamp (UTC): {zip_filename}\n")
                        f.write(f"SHA-256: {sha256_hash.hexdigest()}\n")
                    try:
                        if os.path.exists(json_path):
                            os.remove(json_path)
                    except OSError:
                        pass
                    return zip_path
