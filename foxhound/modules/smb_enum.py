# modules/smb_enum.py
import subprocess
import os
from utils import logger

def enum_smb(target, output_dir):
    output_file = os.path.join(output_dir, "smb_enum.txt")
    logger.log(f"[*] Starting SMB enumeration on {target}")

    try:
        with open(output_file, 'w') as out:
            subprocess.run(["smbclient", "-L", f"//{target}/", "-N"], stdout=out, stderr=subprocess.STDOUT, check=True)
        logger.log(f"[+] SMB enumeration complete. Output saved to {output_file}")
    except subprocess.CalledProcessError:
        logger.log("[!] smbclient failed to enumerate SMB shares.", level="ERROR")
    except FileNotFoundError:
        logger.log("[!] smbclient not found. Make sure it is installed and in your PATH.", level="ERROR")
