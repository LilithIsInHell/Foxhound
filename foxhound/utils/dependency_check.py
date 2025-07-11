# utils/dependency_check.py
import shutil
from foxhound.utils import logger

REQUIRED_TOOLS = [
    "nmap",
    "rustscan",
    "ffuf",
    "smbclient"
]

def check_dependencies():
    logger.log("[*] Checking required tools...")
    missing = []

    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) is None:
            missing.append(tool)
            logger.log(f"[!] Missing: {tool}", level="ERROR")

    if missing:
        logger.log("[!] Some tools are missing. Please install them before continuing.", level="ERROR")
        logger.log("    Try: sudo apt install " + " ".join(missing), level="ERROR")
        return False

    logger.log("[+] All required tools found.", level="SUCCESS")
    return True
